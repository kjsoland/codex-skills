# Cable BOM Impact Map

Read this reference whenever a Sol change package changes one of the cable-related To/From ICD families below.

## ICD-to-BOM Mapping

The product-structure root is `BOMs/Sol Computer/System Interconnect` in the synced Sol Project Team Channel.

| Changed ICD family | Associated product-structure folder | Expected BOM |
| --- | --- | --- |
| AC Power and Ground ICD | `AC Power and Ground Cable Kit` | `AC Power and Ground Cable Kit BOM *.xlsx` |
| BD Beamplate Electrical ICD | `BD Beamplate Cable Kit` | `BD Beamplate Cable Kit BOM *.xlsx` |
| Cooling ICD | `Cooling Interconnect Kit` | `Cooling Interconnect Kit BOM *.xlsx` |
| Core Control Signal Map ICD | `Core Control System Cable Kit` | `Core Control System Cable Kit BOM *.xlsx` |
| Electrode Signal Map ICD | `Electrode Cable Kit` | `Electrode Cable Kit BOM *.xlsx` |
| Sol Fiber ICD | `Fiber Optic Kit` | `Fiber Optic Kit BOM *.xlsx` |
| Frequency Reference ICD | `Frequency Reference Cable Kit` | `Frequency Reference Cable Kit BOM *.xlsx` |
| Gates-LSC Electrical ICD | `Gates, LSC Electrical Cable Kit` | `Gates, LSC Electrical Cable Kit BOM *.xlsx` |
| Network and Comm ICD | `Network and Comm Cable Kit` | `Network and Comm Cable Kit BOM *.xlsx` |
| QPA and Physics Package Control ICD | `QPA and Physics Package Control Cable Kit` | `QPA and Physics Package Control Cable Kit BOM *.xlsx` |
| System Monitor ICD | `System Monitor Cable Kit` | `System Monitor Cable Kit BOM *.xlsx` |

`Cable and Fiber Structure` is not mapped because it is a structural product assembly rather than an ICD-derived cable-kit BOM.

## Required Review

1. Compare the released ICD baseline with the current/proposed ICD using stable logical records, not raw row coordinates alone.
2. Identify every delta that can change a purchasing line: physical cable/run added or removed, external/internal status, vendor or vendor part number, part-selection conflict, quantity, length, cable/fiber/hose type, description, ordered identifier, or multichannel-assembly grouping.
3. Inspect the latest associated BOM. Use the `sol-cable-bom` skill's profile for that ICD when producing an expected BOM or tracing aggregation rules.
4. Compare the expected purchasing lines with the current BOM by vendor part number, compatible description/type/length, and quantity. Keep Arena Part Number and drawing Notes outside the comparison unless the change explicitly affects them.
5. Classify the result as one of:
   - `No BOM impact`: the ICD change does not alter purchasing identity, compatibility, or quantity.
   - `BOM update required`: one or more purchasing lines must be added, removed, split, merged, renumbered, or requantified.
   - `BOM review blocked`: the BOM is missing/unreadable or the ICD lacks enough purchasing data to determine the result.
6. Preserve a concise comparison artifact under `smartsheet-dry-run/` when the delta is nontrivial. Do not overwrite the product-structure BOM unless implementation is in scope.

## Change-Summary Section

Include this section for every mapped ICD change, including no-impact results:

```markdown
## Associated Cable BOM Impact Review

| Associated BOM | Current file reviewed | ICD purchasing delta | Assessment | Required action |
|---|---|---|---|---|
| <mapped cable-kit BOM> | `<SharePoint-relative label or missing>` | <part/quantity/length/type changes or none> | <No BOM impact / BOM update required / BOM review blocked> | <none, regenerate/update, or resolve missing data> |
```

When a controlled/released BOM requires revision, also place it in `Likely Impacted Released Docs` and `Related Docs?` after the changed ICD. When a working-only BOM needs an update, keep it out of `Related Docs?` unless the applicable configuration-management rules treat it as a controlled impacted document; still record the action in this section.
