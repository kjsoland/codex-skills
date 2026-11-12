# Production notes

## Layout starting point

For a 792 x 612-point page, reserve about 20 points at the edges and a 50-point title band. A central system image approximately 550 points wide can dominate the page while smaller photo panels occupy the surrounding corners. Its transparent or white margins can overlap the panels' bounding regions only when no depicted equipment is obscured.

An example arrangement is a tall reference photo at upper left, a rack view at upper right, another rack view at lower left, and a small operating-position detail at lower right. This is a starting point, not a requirement for exactly four panels or three numbered locations. Map the arrangement to the actual locations and number of hazards. Route leaders through free space and stop them precisely on the relevant physical feature. Put contact/response content in remaining space beneath the map, without hiding the doorway.

Keep supporting photo headers visually quieter than the main title and numbered markers. Preserve a useful crop when reducing a photo; prefer a smaller region containing readable labels over a large amount of irrelevant hose or background. Check at printed-page scale, not only while zoomed in.

## Faithful image and annotation handling

A presentation can contain both an old version of the whole poster and the replacement photo. Identify the intended picture by viewing the slide, reading shape names/relationships, and comparing the image content. Do not blindly use the first embedded image.

Inspect `p:pic` for its embedded image relationship, `a:srcRect` crop, `a:xfrm` bounds/rotation, and any native overlays. A colored annotation may be a separate `p:sp`; extracting only the PNG silently loses it. The bundled helper supports unrotated top-level pictures and unfilled rectangle overlays. It stops on grouped, rotated, or more complex annotations; render/export the corresponding group or use document-native tools in those cases.

```text
python scripts/extract_slide_graphic.py reference.pptx --slide 5 --list
python scripts/extract_slide_graphic.py reference.pptx --slide 5 \
  --picture "Picture 5" --rectangle "Rectangle 6" --out extracted
```

The slide number refers to presentation order, not an assumed `slideN.xml` filename. The output manifest contains the original image path/hash, normalized visible crop, annotation bounds relative to the displayed photo, stroke color, and stroke width relative to displayed photo width. When fitting the photo into a panel, map all rectangle coordinates and line thickness using that same display transform. Preserve full-resolution source bytes and use editable crops (`a:srcRect`) in PowerPoint.

For DOCX ICDs, follow the paragraph/figure relationship to the image. Save nearby captions and rack-unit/location text with each extracted figure; the media filename alone is not a sufficient citation. If an apparent figure is an EMF, WMF, grouped object, or native drawing, render it through a compatible document application rather than approximating it.

## Existing project builders

Prefer adapting the accepted project's source generator over rebuilding its styling and drawing pipeline. Generalize inputs for hazard labels, image paths, location anchors, response steps, and contacts. Remove the previous hazard's operational instructions and obsolete source notes from the new output.

If no builder is available, create the composition with the document tools/libraries available in the environment. Suitable local approaches include PyMuPDF for exact PDF placement and native PowerPoint shapes via document-control tools, python-pptx, or Office automation. A single raster slide is not an editable substitute for the requested PowerPoint.

On Windows, inspect the actual Python installation if `python` or `py` resolves to an inaccessible WindowsApps alias. For Office preview automation, open only the selected document read-only and without a visible window; export to the task directory, close the opened document, and release its COM objects. Do not terminate a user's Office process or call `Quit` on an application that may contain unrelated work.

## Final inspection

- PDF: exactly one page at the requested dimensions; labels and numbers fit their boxes.
- PowerPoint: matching page dimensions, native editable markers/text, and the intended original images/crops.
- Visuals: central map is dominant; photos support it; no annotation, doorway, or location marker is obscured; leaders point to the correct equipment face.
- Source fidelity: original image hashes remain traceable; colored annotations align with the same valves/features as in the source; units and phone digits match exactly.
- Content: inherited text from the previous hazard is removed unless intentionally applicable; an incomplete draft is identifiable.

Render after changes to placement, crops, text, or annotations. Once the required checks pass, do not repeatedly rebuild unchanged outputs.
