#!/usr/bin/env python3
"""Create a macro-preserving port waiver with redlined requirement values."""

from __future__ import annotations

import argparse
import json
import os
import re
import secrets
import shutil
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
from typing import Any
from zipfile import ZIP_DEFLATED, ZipFile

from lxml import etree


W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W14 = "http://schemas.microsoft.com/office/word/2010/wordml"
XML = "http://www.w3.org/XML/1998/namespace"
NS = {"w": W, "w14": W14}
q = lambda name: f"{{{W}}}{name}"


def require_text(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Missing non-empty string: {key}")
    return value.strip()


def find_sdt(root, tag: str):
    nodes = root.xpath(
        f'.//w:sdt[w:sdtPr/w:tag[@w:val="{tag}"]]', namespaces=NS
    )
    if len(nodes) != 1:
        raise ValueError(f"Expected one content control {tag}, found {len(nodes)}")
    return nodes[0]


def normalize_run(run, color: str = "000000", strike: bool = False, underline: bool = False):
    rpr = run.find(q("rPr"))
    if rpr is None:
        rpr = etree.Element(q("rPr"))
        run.insert(0, rpr)
    for child_name in ("i", "iCs", "color", "strike", "dstrike", "u"):
        for node in rpr.findall(q(child_name)):
            rpr.remove(node)
    color_node = etree.SubElement(rpr, q("color"))
    color_node.set(q("val"), color)
    if strike:
        etree.SubElement(rpr, q("strike"))
    if underline:
        u = etree.SubElement(rpr, q("u"))
        u.set(q("val"), "single")
    if rpr.find(q("sz")) is None:
        size = etree.SubElement(rpr, q("sz"))
        size.set(q("val"), "18")
    if rpr.find(q("szCs")) is None:
        size_cs = etree.SubElement(rpr, q("szCs"))
        size_cs.set(q("val"), "18")


def set_plain(root, tag: str, value: str):
    sdt = find_sdt(root, tag)
    texts = sdt.xpath(".//w:sdtContent//w:t", namespaces=NS)
    if not texts:
        raise ValueError(f"No text node for content control {tag}")
    texts[0].text = value
    texts[0].set(f"{{{XML}}}space", "preserve")
    normalize_run(texts[0].getparent())
    for node in texts[1:]:
        node.text = ""
    properties = sdt.find(q("sdtPr"))
    if properties is not None:
        for node in properties.findall(q("showingPlcHdr")):
            properties.remove(node)


def set_redline(root, tag: str, requirement: dict[str, Any]):
    sdt = find_sdt(root, tag)
    content = sdt.find(q("sdtContent"))
    old_p = content.find(q("p"))
    ppr = (
        deepcopy(old_p.find(q("pPr")))
        if old_p is not None and old_p.find(q("pPr")) is not None
        else None
    )
    for child in list(content):
        content.remove(child)
    paragraph = etree.SubElement(content, q("p"))
    if ppr is not None:
        paragraph.append(ppr)
    fragments = [
        (require_text(requirement, "prefix"), "000000", False, False),
        (require_text(requirement, "old_value"), "FF0000", True, False),
        (" " + require_text(requirement, "new_value"), "FF0000", False, True),
        (require_text(requirement, "suffix"), "000000", False, False),
    ]
    for text, color, strike, underline in fragments:
        run = etree.SubElement(paragraph, q("r"))
        normalize_run(run, color=color, strike=strike, underline=underline)
        node = etree.SubElement(run, q("t"))
        node.set(f"{{{XML}}}space", "preserve")
        node.text = text


def add_requirement_rows(root, count: int):
    table = root.xpath("./w:body/w:tbl", namespaces=NS)[2]
    rows = table.xpath("./w:tr", namespaces=NS)
    if len(rows) != 4:
        raise ValueError(f"Expected four Section 4 rows in template, found {len(rows)}")
    while len(table.xpath("./w:tr", namespaces=NS)) - 2 < count:
        source = table.xpath("./w:tr", namespaces=NS)[-1]
        clone = deepcopy(source)
        new_index = len(table.xpath("./w:tr", namespaces=NS)) - 1
        for tag_node in clone.xpath(".//w:sdtPr/w:tag", namespaces=NS):
            value = tag_node.get(q("val"))
            if value:
                tag_node.set(q("val"), re.sub(r"Row\d+$", f"Row{new_index}", value))
        for id_node in clone.xpath(".//w:sdtPr/w:id", namespaces=NS):
            id_node.set(q("val"), str(secrets.randbelow(2_000_000_000) + 1))
        for node in clone.xpath(".//*[@w14:paraId]", namespaces=NS):
            node.set(f"{{{W14}}}paraId", secrets.token_hex(4).upper())
        table.append(clone)


def populate(root, config: dict[str, Any]):
    requirements = config.get("requirements")
    if not isinstance(requirements, list) or not requirements:
        raise ValueError("requirements must be a non-empty list")
    add_requirement_rows(root, len(requirements))

    documents = config.get("requirements_documents", [])
    if not isinstance(documents, list) or len(documents) > 2:
        raise ValueError("requirements_documents must contain zero to two entries")
    while len(documents) < 2:
        documents.append({"arena_doc_no": "N/A", "revision": "N/A", "title": "N/A"})

    impacts = config.get("impacts", [])
    if not isinstance(impacts, list) or len(impacts) > 4:
        raise ValueError("impacts must contain zero to four entries")
    if re.search(r"\b(?:BRD|BDR)_\d+\b", json.dumps(impacts), re.IGNORECASE):
        raise ValueError("Do not repeat requirement IDs in Section 8 impacts; keep them in Section 4")
    while len(impacts) < 4:
        impacts.append({"item": "N/A", "description": "N/A"})

    values = {
        "WaiverNumber": config.get("waiver_number", "WAIVER_TBD"),
        "WaiverTitle": require_text(config, "title"),
        "ArenaDocNo": documents[0].get("arena_doc_no", "N/A"),
        "Revision": documents[0].get("revision", "N/A"),
        "RequirementsDocumentTitle": documents[0].get("title", "N/A"),
        "ArenaDocNoRow2": documents[1].get("arena_doc_no", "N/A"),
        "RevisionRow2": documents[1].get("revision", "N/A"),
        "RequirementsDocumentTitleRow2": documents[1].get("title", "N/A"),
        "WaiverRationale": require_text(config, "rationale"),
        "SystemImpacts": require_text(config, "system_impacts"),
        "EffortsToBringIntoCompliance": require_text(config, "efforts"),
        "CorrectionAction": require_text(config, "correction_action"),
    }
    for index, impact in enumerate(impacts, 1):
        values[f"ImpactedHWSWRow{index}"] = impact.get("item", "N/A") or "N/A"
        values[f"ImpactDescriptionRow{index}"] = impact.get("description", "N/A") or "N/A"

    template_rows = max(2, len(requirements))
    for index in range(1, template_rows + 1):
        if index <= len(requirements):
            requirement = requirements[index - 1]
            values[f"SharedREQIDRow{index}"] = require_text(requirement, "id")
            values[f"ISRequirementTextRow{index}"] = require_text(requirement, "is_text")
        else:
            values[f"SharedREQIDRow{index}"] = "N/A"
            values[f"ISRequirementTextRow{index}"] = "N/A"
            values[f"ProposedRequirementTextRow{index}"] = "N/A"

    for tag, value in values.items():
        set_plain(root, tag, str(value))
    for index, requirement in enumerate(requirements, 1):
        set_redline(root, f"ProposedRequirementTextRow{index}", requirement)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--template",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "assets"
        / "Quantinuum_Requirement_Waiver_Template_v4p1.docm",
    )
    args = parser.parse_args()

    if not args.config.is_file():
        parser.error(f"Config not found: {args.config}")
    if not args.template.is_file():
        parser.error(f"Template not found: {args.template}")
    if args.output.exists():
        parser.error(f"Refusing to overwrite output: {args.output}")
    args.output.parent.mkdir(parents=True, exist_ok=True)

    config = json.loads(args.config.read_text(encoding="utf-8"))
    shutil.copy2(args.template, args.output)
    temp = args.output.with_suffix(args.output.suffix + ".tmp")
    try:
        with ZipFile(args.output, "r") as source:
            original_vba = source.read("word/vbaProject.bin")
            root = etree.fromstring(source.read("word/document.xml"))
            populate(root, config)
            document_xml = etree.tostring(
                root, xml_declaration=True, encoding="UTF-8", standalone=True
            )
            with ZipFile(temp, "w", ZIP_DEFLATED) as target:
                for info in source.infolist():
                    data = document_xml if info.filename == "word/document.xml" else source.read(info.filename)
                    target.writestr(info, data)
        os.replace(temp, args.output)

        with ZipFile(args.output, "r") as check:
            if check.testzip() is not None:
                raise ValueError("Generated DOCM package validation failed")
            if sha256(original_vba).digest() != sha256(check.read("word/vbaProject.bin")).digest():
                raise ValueError("Embedded waiver macros changed during generation")
            check_root = etree.fromstring(check.read("word/document.xml"))
            requirement_ids = [
                "".join(node.xpath(".//w:sdtContent//w:t/text()", namespaces=NS))
                for node in check_root.xpath(
                    './/w:sdt[w:sdtPr/w:tag[starts-with(@w:val,"SharedREQID")]]',
                    namespaces=NS,
                )
            ]
        print(f"OUTPUT={args.output}")
        print("REQUIREMENTS=" + ",".join(requirement_ids))
        print("MACROS_PRESERVED=true")
        return 0
    except Exception:
        if temp.exists():
            temp.unlink()
        if args.output.exists():
            args.output.unlink()
        raise


if __name__ == "__main__":
    raise SystemExit(main())
