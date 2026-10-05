# Core Control physical label segments

The user's confirmed mapping for Core Control ICD v3p0 is a physical cable chain, not alternate labels for the same end-to-end endpoints. In the DDS tab's layout:

| Label segment | From columns | To columns |
| --- | --- | --- |
| External | D, H, I | J, K, L |
| Secondary External | J, K, L | M, N, O |

Print External labels only. Do not produce Internal label files for any Core Control tab. The previously specified Internal mapping D/E/F to D/H/I is topology context, not a print requirement. Use column D for the External source location, even if G (Secondary From Location) is blank. Preserve each endpoint's full location/component/connection. Skip explicitly disconnected `NONE` ports, reference tables, and worksheet summary rows.

Confirm headers before applying letters to other tabs or revisions. TTL shares the External D/H/I to J/K/L layout, but M/N/O are purchasing fields rather than Secondary To fields. ADC External labels use C/D/E as FROM and G/H/I as TO, and only rows with `External Cable Present?` = `Yes` are eligible (trim whitespace and compare without case sensitivity). Exclude ADC `No`/blank rows rather than generating PN-unspecified files for them. Do not print ADC Secondary connections or its breakout-to-MTCA Internal segment. This Yes-only filter is specific to ADC; do not apply it to other tabs without instruction. Do not interpret TTL purchasing columns as endpoints. DDS Secondary External labels remain J/K/L to M/N/O. Tertiary DDS endpoints remain outside the requested mapping until explicitly specified.

Assign purchasing PN/length only to its defined segment. Do not automatically reuse the main External PN/length for Secondary External segments. When endpoint text is complete but segment identity is unspecified, provide separate clearly marked `PN_UNSPECIFIED` label files and list the missing purchasing identity in the workspace manifest; these are not confirmed homogeneous automation batches. Endpoint-incomplete/TBD segments remain held with no print import file. Preserve source row order within each file, keep tabs and physical segments in separate files, and deliver raw label files in one flat BOM label folder with audits elsewhere.
