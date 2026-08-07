# Network and Comm ICD Profile

## Source Selection

- Use the active `Network and Comm ICD v*.xlsx` in the ICD folder.
- Treat dated `*_Release_*` subfolders as released snapshots, not the latest working copy, unless the user asks for one.
- The target product-structure folder is `BOMs/Sol Computer/System Interconnect/Network and Comm Cable Kit`.

## Cable Sources

### Interrack Cabling

Count every populated `Designator` row. Use:

- `Cable Type`
- `Actual length (m)` (despite the header, values may be in meters or feet)
- `Vendor`
- `Cable Part Number`
- the from/to location, component, and connection fields for extraction auditing

The `Cable Part Number` cells may contain purchasing URLs instead of literal part numbers. Resolve known URLs through `network-comm-catalog.json`. When multiple links resolve to the same order identifier and cable type/length, aggregate their quantities.

### Non-Ethernet Communication

Include rows whose `External Cable Present?` value is `Yes`. Use the cable vendor, cable part number, cable length, plan, and endpoint fields. Exclude rows marked `No`; those rows describe communication paths without a separate external cable.

## Audit Rules

- Source-row count must equal the sum of BOM quantities.
- Do not count blank formatted table rows.
- Do not merge records with different cable types or actual lengths solely because they share a URL.
- If a URL used for a copper part appears on a fiber row, leave the fiber vendor part number `TBD`, retain its quantity, and identify the needed correction in Description.
- Keep missing length values visible in Description and use `TBD` for missing vendor part numbers.
- Treat Amazon ASINs resolved from ICD purchasing links as order identifiers. Confirm manufacturer part numbers before Arena release.
- Use the literal manufacturer part number when the ICD already supplies one, such as `U328F-15M` or `788302-30`.
- Leave every Notes cell blank; the column is reserved for drawing notes that link back to BOM items.
- Use no color formatting, hyperlinks, cell comments, or table styles. Bold only the header row.
