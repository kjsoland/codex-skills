---
name: sol-cable-bom
description: Create and audit Sol cable-kit BOM workbooks from working ICD Excel files and the SharePoint-backed Sol Product Structure. Use when Codex needs to extract cable purchasing lines, aggregate quantities by vendor part or order identifier, leave Arena part numbers ready for later entry, flag ICD purchasing conflicts or TBDs, and save an Excel BOM in the applicable Sol Computer product-structure folder.
---

# Sol Cable BOM

Create a traceable purchasing BOM from a Sol cable-related ICD without silently repairing incomplete or conflicting design inputs.

## Workflow

1. Find the latest working ICD beside its dated release folders. Prefer the undated active workbook with the highest version unless the user names a baseline.
2. Locate the matching folder under `BOMs/Sol Computer`. Treat the product-structure folder as the BOM output location.
3. If the source workbook is open and locked, use the existing Excel application to `SaveCopyAs` a temporary `.xlsx`; do not save, close, or modify the user's workbook.
4. Read the relevant ICD cable sheets and count one cable instance per populated design row.
5. Aggregate only records that resolve to the same orderable identifier and compatible cable type/length.
6. Set `Quantity` to the exact number of units required by the design. Never replace it with a pack count or round it up to a supplier package quantity.
7. Keep the Arena part-number cells blank. Use `TBD` for an unresolved vendor part number so missing purchasing data is visible.
8. Leave every Notes cell blank. The Notes column is reserved for drawing notes that link back to BOM items.
9. If an order link conflicts with the source cable type or other purchasing fields, create a separate `TBD` line and identify the needed correction in Description. Never infer a replacement part.
10. Validate headers, exact required quantities, source coverage, ordering-package math, blank Notes cells, filter range, and freeze panes before delivery.

## To/From ICD Cable Kits

Read `references/to-from-profiles.md` before processing the product-structure To/From ICD set. Use the batch builder for the ten cable-kit BOMs other than Network and Comm:

```powershell
python scripts/build_to_from_boms.py `
  "<SharePoint Systems\ICDs folder>" `
  "<SharePoint BOMs\Sol Computer\System Interconnect folder>" `
  --system-monitor-xlsx "<temporary readable copy of the latest System Monitor ICD.xlsx>"
```

The System Monitor source is currently `.xlsb`. Open it read-only in Excel and save a temporary `.xlsx` copy before running the builder; never modify the SharePoint source. The batch builder prefers an active workbook in the ICD folder and otherwise selects the highest-version file in the dated release folders.

## Network and Comm ICD

Read `references/network-comm-profile.md` before processing this ICD. Use the bundled builder for the standard six-column output:

```powershell
python scripts/build_network_comm_bom.py `
  "<readable Network and Comm ICD copy.xlsx>" `
  "<Network and Comm Cable Kit product folder>\Network and Comm Cable Kit BOM v0p1.xlsx"
```

The script uses `references/network-comm-catalog.json` to translate the purchasing links already present in the ICD into stable order identifiers and concise descriptions. Extend the catalog only after resolving a new link and confirming its identity.

## Output Standard

Create one worksheet named `Cable BOM` with these columns in this order:

1. Item No.
2. Arena Part Number
3. Vendor Part Number
4. Quantity
5. Description
6. Notes

Use plain cells with no color formatting. Bold only the header row, freeze it, enable filtering, and wrap long descriptions. Leave the Notes column completely blank and do not add comments, banding, colored fills, or colored fonts. Do not add hyperlinks unless the workbook includes ordering information as described below. Keep the workbook purchasing-focused; do not add unrelated ICD data sheets.

When ordering information is included, append these columns after `Notes`:

7. Ordering Information
8. Order Packaging
9. Spares

Place any additional sourcing column, such as `Distributor`, after `Spares`. `Quantity` remains the exact design requirement. For a multi-pack, record the actual purchase package in `Order Packaging`, for example `1 x 10-pack (10 units ordered)`, and set numeric `Spares` to total units ordered minus `Quantity`. Leave `Order Packaging` blank for ordinary per-each purchases; set `Spares` to `0` when exact per-each ordering is known and leave it blank when the order unit is unresolved. Hyperlinks are allowed only in `Ordering Information` and sourcing columns when the user requests order links.

## Setup and Example

Require Python 3.11 or newer and `openpyxl`. Example request: "Use the latest Network and Comm ICD to regenerate the Network and Comm Cable Kit BOM and flag any part-selection conflicts."
