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

Default to Excel plus UTF-8 CSV in the workspace output folder, and copy both validated exports into the authoritative source ICD folder. When the source is inside a dated release subfolder, put the exports in the parent ICD folder, leaving the release package unchanged. Include the source revision in the export filenames and verify that the ICD-folder copies match the workspace files. Honor a user-specified destination instead when provided. Use exactly one column, no header, no separators, and two consecutive rows per cable: From Side, then To Side. Each cell contains:

```text
<FROM SIDE or TO SIDE> <Designator>    ICD: <ACRONYM>
FROM: <From Location> / <From Component> / <From Connection>
TO: <To Location> / <To Component> / <To Connection>
```

Keep the full FROM and TO definitions in the same order on both labels; only the side indicator changes. Use source fields verbatim apart from surrounding whitespace. If the ICD has no designator column or value, leave that area blank. Governing ICD acronyms: SYS = Sol System; AC = AC Power & Ground; NET = Network and Comm; COOL = Cooling; FREQ = Frequency Reference; FIBER = Sol Fiber; G-LSC = Gates, LSC Electrical; CORE = Core Control System; MON = System Monitor; QPA/PP = QPA and Physics Package Control; ELEC = Electrode Signal Map; BD-E = BD Beamplate. Verify unfamiliar ICD acronyms against the procedure rather than inventing them. Keep identifiers and leading zeros intact. Embedded newlines belong inside a single cell/quoted CSV field, not separate records. If the source already defines explicit From Side and To Side label text, preserve those labels instead of reconstructing them. Honor any user-specified label text or printer format over these defaults.

Do not invent missing endpoints or export unevaluated formulas. Report incomplete rows and resolve them before producing an apparently complete label set. Ignore fully empty source rows only. Missing designators are allowed by the procedure; missing endpoint definitions are not.

## Export helper

Requires Python and `openpyxl`. For the standard Cabling columns (`Designator`, `From Location`, `From Component`, `From Connection`, `To Location`, `To Component`, `To Connection`), run:

```text
python scripts/export_labels.py "path/to/map.xlsx" "path/to/output/Map Labels.xlsx" --icd ELEC
```

The helper reads cached formula results, creates XLSX and CSV, and verifies the saved values and single-column structure. Inspect formula-dependent inputs for usable caches before relying on them. Adapt extraction when a different ICD schema or existing label columns are present; do not force the standard schema onto unrelated workbooks.

Electrode maps may include unused channel rows whose designator and all three To fields are literal `NONE`. These are not cables: after verifying that pattern, use `--skip-unused` and report the excluded count. Do not apply this exclusion to partially specified real cables.

Validate that the output has twice the eligible source cable count, each pair matches its source endpoints, and neither export has extra headers or blank rows. Keep source workbooks unchanged. Report the source revision, cable count, label count, and output links. Printer-specific sizing requires the actual stock dimensions; the default spreadsheet is a label list/import file.
