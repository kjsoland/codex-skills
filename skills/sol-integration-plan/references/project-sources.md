# Project sources

## Contents

- [Local source hierarchy](#local-source-hierarchy)
- [Schedule authority](#schedule-authority)
- [Cable and RF status](#cable-and-rf-status)
- [Access and safety](#access-and-safety)

## Local source hierarchy

The canonical local SharePoint sync is beneath the current user's profile:

```text
Quantinuum LLC/
  Sol Hardware Project Team - Sol Project Team Channel/
    Integration/
      Integration Plan/
        _source/
        _generated/
        Sol_Integration_Plan_v2.html
        Update_Integration_Plan_From_Smartsheet.bat
    Systems/
      ICDs/
```

The plan's cable generator resolves ICDs from the sibling `Systems/ICDs` SharePoint tree. Prefer current working/root ICD copies when the generator recognizes them; otherwise use its released-file fallback and verify the generated ICD Source Basis table.

## Schedule authority

Use the correct schedule for each type of date:

- Sol Project Schedule — non-rack product-structure hardware:
  `https://app.smartsheet.com/sheets/vRQFPM3hHRGf2574pq82vfHfMJr8wWJ9JMq86Rj1`
- Sol Control Electronics Rack Deliveries Schedule — CE Rack 1–6 plus the BD and Detection Rack:
  `https://app.smartsheet.com/sheets/JRM2Fvr7fQ5pVxVj5cH9CX9cWp54Xq32Pv3Fwr81`
- Sol Beam Delivery Plates Schedule — beam-delivery plate receive dates:
  `https://app.smartsheet.com/sheets/qcWMJJ3V5fwXMXgpqC2PFMVM9mw4P6MrRH6ghq21`

For each beam-delivery plate, use the finish date of `Final Laser Alignment & Verification` as the receive date.

Do not substitute the Sol Project Schedule for rack or beam-delivery plate milestones when the dedicated schedule applies.

## Cable and RF status

Gates LSC EICD RF Powers:

`https://app.smartsheet.com/sheets/mr5cFRg7H2JqQ825xVFhmpX5JgXGjJhXRJfXj9F1`

This sheet is intentionally limited to Gates/LSC Electrical ICD (`G-LSC`) cable RF checkout rows. Do not expand it to unrelated ICD cable families.

The cable refresh sequence is:

1. Build current cable keys from the plan and ICD sources.
2. Ensure the RF-status sheet has rows for the current `G-LSC` keys when external writes are authorized.
3. Pull user-entered completion and RF values.
4. Rebuild the Markdown cable tables.
5. Regenerate the HTML.

## Access and safety

- Obtain Smartsheet access through the environment variable `SMARTSHEET_ACCESS_TOKEN`.
- Never copy the token into scripts, Markdown, logs, ZIP files, or chat.
- Confirm write authorization before running the `ensure` operation because it can add Smartsheet rows.
- Treat generated HTML, SVG, CSV, and audit files as derivatives, not independent source documents.
