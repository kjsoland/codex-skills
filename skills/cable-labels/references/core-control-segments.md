# Core Control physical label segments

The user's confirmed mapping for Core Control ICD v3p0 is a physical cable chain, not alternate labels for the same end-to-end endpoints. In the DDS tab's layout:

| Label segment | From columns | To columns |
| --- | --- | --- |
| Internal | D, E, F | D, H, I |
| External | D, H, I | J, K, L |
| Secondary External | J, K, L | M, N, O |

Use column D for the internal destination and external source location, even if G (Secondary From Location) is blank. Preserve each endpoint's full location/component/connection. Emit a pair for each populated physical segment; an unassigned downstream external endpoint does not remove a valid Internal connection. Skip explicitly disconnected `NONE` ports, reference tables, and worksheet summary rows.

Confirm headers before applying letters to other tabs or revisions. TTL shares the Internal/External layout, but M/N/O are purchasing fields rather than Secondary To fields. ADC runs device-to-breakout-to-MTCA: External C/D/E to G/H/I; Internal G/H/I to J/K/L. Do not interpret TTL purchasing columns as endpoints. Tertiary DDS endpoints remain outside this three-segment mapping until explicitly specified.

Assign purchasing PN/length only to its defined segment. Do not automatically reuse the External PN/length for Internal or Secondary External segments. When endpoint text is complete but segment identity is unspecified, provide separate clearly marked `PN Unspecified` label files and list the missing purchasing identity in the manifest; these are not confirmed homogeneous automation batches. Endpoint-incomplete/TBD segments remain held with no print import file. Preserve source row order within each file and keep tabs and physical segment categories separate.
