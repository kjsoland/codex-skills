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
6. Keep the Arena part-number cells blank. Use `TBD` for an unresolved vendor part number so missing purchasing data is visible.
7. Leave every Notes cell blank. The Notes column is reserved for drawing notes that link back to BOM items.
8. If an order link conflicts with the source cable type or other purchasing fields, create a separate `TBD` line and identify the needed correction in Description. Never infer a replacement part.
9. Validate headers, quantities, source coverage, blank Notes cells, filter range, and freeze panes before delivery.

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

Use plain cells with no color formatting. Bold only the header row, freeze it, enable filtering, and wrap long descriptions. Leave the Notes column completely blank and do not add hyperlinks, comments, banding, colored fills, or colored fonts. Keep the workbook purchasing-focused; do not add unrelated ICD data sheets.

## Setup and Example

Require Python 3.11 or newer and `openpyxl`. Example request: "Use the latest Network and Comm ICD to regenerate the Network and Comm Cable Kit BOM and flag any part-selection conflicts."
