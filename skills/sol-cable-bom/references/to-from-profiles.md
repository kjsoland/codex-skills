# Sol To/From ICD BOM Profiles

Use these profiles for the Sol Computer `System Interconnect` cable-kit folders other than Network and Comm.

| Product-structure folder | ICD worksheet(s) | Physical-item rule |
| --- | --- | --- |
| AC Power and Ground Cable Kit | `Electrical Cabling` | Count populated Power and Ground runs. Keep unresolved selections as `TBD`. |
| BD Beamplate Cable Kit | `Electrical Cabling` | Count populated vendor cable part numbers inside the ICD data table; ignore calculation rows below it. |
| Cooling Interconnect Kit | `Water Tubes` | Sum each vendor hose/tube part and color by cut length, convert inches to purchasing feet, and state the unit in Description. |
| Core Control System Cable Kit | `DDS Channel Map`, `ADC Channel Map`, `TTL Channel Map`, `PMT Channel Map` | Count DDS/ADC rows only when `External Cable Present?` is Yes, count populated TTL cable rows, and expand repeated PMT part tokens into physical cables. |
| Electrode Cable Kit | `Cabling` | Count populated cable part rows, exclude explicit `NONE` rows, and retain explicit `TBD` selections. |
| Fiber Optic Kit | `External Fibers` | Count populated From/To fiber rows and aggregate calculated QTM part numbers using cached formula values. Ordering status does not remove a required design item. |
| Frequency Reference Cable Kit | `Electrical Cabling_All` | Count only `External` rows and exclude rows delegated to a CE Rack BOM. Preserve source placeholder part families. |
| Gates, LSC Electrical Cable Kit | `Electrical Cabling` | Count populated cable part rows. Keep a separate line when the same part number has a conflicting ICD length. |
| QPA and Physics Package Control Cable Kit | `Electrical Cabling` | Count physical assemblies, not `-` signal rows carried inside another assembly. Group unresolved assemblies by compatible description and length. |
| System Monitor Cable Kit | `Electrical Cabling` | Count individual sensor/signal runs plus populated multiconductor assemblies. For repeated MECH monitor channels, count only the physical assembly row that contains its part number. |

For every profile, aggregate only compatible physical items. Leave Arena Part Number and Notes blank. Do not use Notes for audit findings; put a concise purchasing caveat in Description when the ICD itself is incomplete or conflicting.
