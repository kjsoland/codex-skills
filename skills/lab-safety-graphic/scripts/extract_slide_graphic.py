#!/usr/bin/env python3
"""Extract original PowerPoint picture bytes and aligned rectangle annotations."""
import argparse
import hashlib
import json
import posixpath
from pathlib import Path, PurePosixPath
import xml.etree.ElementTree as ET
from zipfile import ZipFile

NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def relationships(archive, part):
    folder, filename = posixpath.split(part)
    relpart = posixpath.join(folder, '_rels', filename + '.rels')
    return {el.get('Id'): el for el in ET.fromstring(archive.read(relpart))}


def resolve_part(part, relationship):
    if relationship.get('TargetMode') == 'External':
        raise ValueError('Linked external media is unsupported; use an embedded graphic.')
    target = relationship.get('Target', '')
    if target.startswith('/'):
        target = target.lstrip('/')
    else:
        target = posixpath.normpath(posixpath.join(posixpath.dirname(part), target))
    if target.startswith('../') or '\\' in target:
        raise ValueError('Invalid package relationship target.')
    return target


def name_of(shape):
    el = shape.find('.//p:cNvPr', NS)
    return el.get('name') if el is not None else None


def geometry(shape):
    transform = shape.find('p:spPr/a:xfrm', NS)
    if transform is None:
        raise ValueError('Shape has inherited or grouped geometry; render the source group.')
    if int(transform.get('rot', '0')) % 21600000 or any(
        transform.get(k, '0') in ('1', 'true') for k in ('flipH', 'flipV')
    ):
        raise ValueError('Rotated/flipped shapes require document-native group export.')
    offset, extent = transform.find('a:off', NS), transform.find('a:ext', NS)
    if offset is None or extent is None:
        raise ValueError('Shape has incomplete bounds.')
    result = [int(offset.get('x')), int(offset.get('y')),
              int(extent.get('cx')), int(extent.get('cy'))]
    if min(result[2:]) <= 0:
        raise ValueError('Shape has nonpositive extent.')
    return result


def inspect_or_extract(source, slide_number, picture_name=None, rectangle_names=(), out=None):
    source = Path(source).resolve()
    with ZipFile(source) as archive:
        presentation_part = 'ppt/presentation.xml'
        presentation = ET.fromstring(archive.read(presentation_part))
        ids = presentation.findall('p:sldIdLst/p:sldId', NS)
        if not 1 <= slide_number <= len(ids):
            raise ValueError(f'Slide must be between 1 and {len(ids)}.')
        slide_id = ids[slide_number - 1].get('{' + NS['r'] + '}id')
        slide_part = resolve_part(presentation_part, relationships(archive, presentation_part)[slide_id])
        slide = ET.fromstring(archive.read(slide_part))
        shapes = slide.find('p:cSld/p:spTree', NS)
        inventory = []
        for shape in shapes:
            name = name_of(shape)
            if name is None:
                continue
            item = {'name': name, 'type': shape.tag.rsplit('}', 1)[-1]}
            item['text'] = ' '.join(el.text or '' for el in shape.findall('.//a:t', NS))
            try:
                item['bounds_emu'] = geometry(shape)
            except ValueError as error:
                item['geometry_note'] = str(error)
            inventory.append(item)
        if picture_name is None:
            return {'source': str(source), 'slide': slide_number,
                    'slide_part': slide_part, 'shapes': inventory}

        def named(name):
            matches = [el for el in shapes if name_of(el) == name]
            if len(matches) != 1:
                raise ValueError(f'Expected one top-level shape named {name!r}, found {len(matches)}.')
            return matches[0]

        picture = named(picture_name)
        if picture.tag != '{' + NS['p'] + '}pic':
            raise ValueError('Select an embedded top-level picture, not a group or text box.')
        if picture.find('p:blipFill/a:stretch', NS) is None:
            raise ValueError('Tiled picture fills require document-native export.')
        blip = picture.find('p:blipFill/a:blip', NS)
        if blip is None or not blip.get('{' + NS['r'] + '}embed'):
            raise ValueError('No embedded raster picture found.')
        # Do not silently omit image recoloring, transforms, or other effects.
        if any(child.tag.rsplit('}', 1)[-1] != 'extLst' for child in blip):
            raise ValueError('Picture effects require document-native export.')
        rid = blip.get('{' + NS['r'] + '}embed')
        image_part = resolve_part(slide_part, relationships(archive, slide_part)[rid])
        suffix = PurePosixPath(image_part).suffix.lower()
        if suffix not in ('.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp', '.gif'):
            raise ValueError('Non-raster image: render/export with the source application.')
        data = archive.read(image_part)
        px, py, pw, ph = geometry(picture)
        src = picture.find('p:blipFill/a:srcRect', NS)
        c = {k: int(src.get(k, '0')) / 100000 if src is not None else 0
             for k in ('l', 't', 'r', 'b')}
        crop = [c['l'], c['t'], 1 - c['r'], 1 - c['b']]
        if not (0 <= crop[0] < crop[2] <= 1 and 0 <= crop[1] < crop[3] <= 1):
            raise ValueError('Outset/nonstandard picture crop requires native export.')
        annotations = []
        for name in rectangle_names:
            rectangle = named(name)
            props = rectangle.find('p:spPr', NS)
            shape_type = props.find('a:prstGeom', NS) if props is not None else None
            if shape_type is None or shape_type.get('prst') != 'rect':
                raise ValueError(f'{name!r} is not a plain rectangle.')
            if props.find('a:noFill', NS) is None:
                raise ValueError('Filled overlays require document-native export.')
            stroke = props.find('a:ln', NS)
            color = stroke.find('a:solidFill/a:srgbClr', NS) if stroke is not None else None
            if color is None or list(color) or not stroke.get('w'):
                raise ValueError('Inherited/transformed stroke color or width is unsupported.')
            if stroke.find('a:prstDash', NS) is not None:
                raise ValueError('Dashed overlays require document-native export.')
            bx, by, bw, bh = geometry(rectangle)
            annotations.append({
                'shape': name,
                'bounds_relative_to_displayed_photo': [(bx-px)/pw, (by-py)/ph,
                                                       (bx+bw-px)/pw, (by+bh-py)/ph],
                'stroke_color': color.get('val'),
                'stroke_width_relative_to_photo_width': int(stroke.get('w')) / pw,
            })
        if out is None:
            raise ValueError('Extraction requires --out.')
        out = Path(out).resolve()
        out.mkdir(parents=True, exist_ok=True)
        filename = 'photo' + suffix
        result = {
            'source': str(source), 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'slide': slide_number, 'slide_part': slide_part, 'picture_shape': picture_name,
            'photo': filename, 'photo_sha256': hashlib.sha256(data).hexdigest(),
            'source_media_part': image_part, 'display_bounds_emu': [px, py, pw, ph],
            'visible_crop_normalized': crop, 'annotations': annotations,
        }
        (out / filename).write_bytes(data)
        (out / 'graphic_manifest.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--slide', required=True, type=int, help='1-based presentation-order slide number')
    parser.add_argument('--list', action='store_true', help='List top-level shapes without extracting')
    parser.add_argument('--picture', help='Exact picture shape name')
    parser.add_argument('--rectangle', action='append', default=[], help='Rectangle shape name; repeatable')
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    if not args.list and (not args.picture or args.out is None):
        parser.error('Choose --list, or provide --picture and --out.')
    try:
        result = inspect_or_extract(args.source, args.slide,
                                    None if args.list else args.picture, args.rectangle, args.out)
    except (ValueError, KeyError, OSError, ET.ParseError) as error:
        parser.exit(2, f'Cannot extract graphic: {error}\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
