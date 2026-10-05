---
name: cable-labels
description: Create single-column cable-label Excel and CSV exports from ICD cabling tables, with each cable's From Side row immediately followed by its To Side row. Use for cable label lists and label-printer import files, rather than harness drawings or routing tape markers.
---

# Cable Labels

## Source selection

Use the user-selected ICD. When asked for the latest map, locate the authoritative working folder and compare revision numbers; do not select an older revision merely because its modification timestamp is newer. Prefer locally synced files for SharePoint sources. Exclude recovery, archive, and review copies unless requested. State the source revision used. If the user requests a released revision, use release evidence rather than assuming the newest working file is released.

For electrode signal maps, use the `Cabling` sheet, not the per-pin `Signal Map` sheet. Preserve source cable order and every cable occurrence; do not deduplicate by designator or sort unless requested.

## Governing procedure

The label rules come from the Sol Cable Routing Procedure, `Sol_Cable_Routing_Training_Examples_Draft` slide 1, "Cable Labeling, ICD Acronyms, and Tape Workflow". Locate the current local procedure in `Sol Cable Routing Procedure` and check that slide when applying this skill; the rules below capture the verified convention. The single-column alternating-row export layout is the user's additional preference.

## Label layout

Use 6-point font for all cable-label text, including the side/designator/ICD line and both endpoint lines. The Excel export uses Arial 6 pt. CSV cannot store font formatting; apply 6 pt in the label-printer import template. Honor an explicit user font override.

Default to Excel plus UTF-8 CSV, staged in the workspace and delivered into the applicable SharePoint-synced cable-kit BOM folder beside its BOM. Locate that folder under `BOMs/Sol Computer/System Interconnect` using the existing product structure; do not default to the source ICD folder. A workspace-only export does not complete delivery. Honor a user-specified destination instead when provided. Include the source revision in the export filenames, preserve differing existing deliverables, and verify that delivered copies match the validated workspace files. Keep source ICDs and release packages unchanged. Use exactly one column, no header, no separators, and two consecutive rows per cable: From Side, then To Side. Each cell contains:

```text
<FROM SIDE or TO SIDE> <Designator>    ICD: <ACRONYM>
FROM: <From Location> / <From Component> / <From Connection>
TO: <To Location> / <To Component> / <To Connection>
```

Keep the full FROM and TO definitions in the same order on both labels; only the side indicator changes. Use source fields verbatim apart from surrounding whitespace. If the ICD has no designator column or value, leave that area blank. Governing ICD acronyms: SYS = Sol System; AC = AC Power & Ground; NET = Network and Comm; COOL = Cooling; FREQ = Frequency Reference; FIBER = Sol Fiber; G-LSC = Gates, LSC Electrical; CORE = Core Control System; MON = System Monitor; QPA/PP = QPA and Physics Package Control; ELEC = Electrode Signal Map; BD-E = BD Beamplate. Verify unfamiliar ICD acronyms against the procedure rather than inventing them. Keep identifiers and leading zeros intact. Embedded newlines belong inside a single cell/quoted CSV field, not separate records. If the source already defines explicit From Side and To Side label text, preserve those labels instead of reconstructing them. Honor any user-specified label text or printer format over these defaults.

Do not invent missing endpoints or export unevaluated formulas. Report incomplete rows and resolve them before producing an apparently complete label set. Ignore fully empty source rows only. Missing designators are allowed by the procedure; missing endpoint definitions are not.

Deliver raw XLSX/CSV label files in one flat label folder within the applicable BOM folder. Encode tab, physical segment, PN/type, and revision in filenames rather than creating nested status or tab folders. Keep manifests, tracebacks, validation reports, build sources, and superseded archives elsewhere, normally in the workspace audit area. Preserve `PN_UNSPECIFIED` in applicable filenames and keep their review status in the separate manifest. When moving labels, update audit links to their delivered paths.

## Grouped labeling runs

When grouping labels for physical labeling automation, keep source tabs separate and split each tab by cable vendor/part number/type and specified length. A shared base part number with different lengths does not identify identical cables. Preserve source order within each group. Put Primary and Secondary endpoint sets in separate files, and include the source revision, tab, endpoint set, and cable identity in filenames or their folder path. Keep the standard one-column From Side/To Side pair layout in every import file; put counts and source-row traceability in a separate manifest.

Inspect the actual endpoint schema before pairing Primary and Secondary endpoints. Confirm whether these are alternate representations of the same cable or separate physical segments; never silently count alternate label sets as additional purchased cables. If only one side has Secondary fields, confirm how the opposite side is paired. Inspect Tertiary fields when present and report their disposition. For Core Control ICD labeling, use the confirmed physical-segment mapping in [references/core-control-segments.md](references/core-control-segments.md). Do not invent missing endpoints, part numbers, or internal jumper lengths. Keep unresolved identities/endpoints out of production print groups and list them in a review report. Endpoint-complete labels with unspecified segment PN may be supplied in separate clearly marked review import files; do not claim these as confirmed homogeneous automation batches.

Channel-map rows can represent multiple channels in one physical cable assembly. Use purchasing metadata and endpoint evidence to distinguish channel rows from cable occurrences; document that distinction in the manifest. Do not generate one physical cable label pair per channel or expand a multi-piece assembly into connector-specific labels without a defined segment map.

## Export helper

Requires Python and `openpyxl`. For the standard Cabling columns (`Designator`, `From Location`, `From Component`, `From Connection`, `To Location`, `To Component`, `To Connection`), run:

```text
python scripts/export_labels.py "path/to/map.xlsx" "path/to/output/Map Labels.xlsx" --icd ELEC
```

The helper reads cached formula results, creates XLSX and CSV, and verifies the saved values and single-column structure. Inspect formula-dependent inputs for usable caches before relying on them. Adapt extraction when a different ICD schema or existing label columns are present; do not force the standard schema onto unrelated workbooks.

Electrode maps may include unused channel rows whose designator and all three To fields are literal `NONE`. These are not cables: after verifying that pattern, use `--skip-unused` and report the excluded count. Do not apply this exclusion to partially specified real cables.

Validate that the output has twice the eligible source cable count, each pair matches its source endpoints, and neither export has extra headers or blank rows. Keep source workbooks unchanged. Report the source revision, cable count, label count, and output links. Printer-specific sizing requires the actual stock dimensions; the default spreadsheet is a label list/import file.
