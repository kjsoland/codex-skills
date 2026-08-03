# Automation inputs

## Contents

1. Prerequisites
2. Extract test results
3. Update a verification workbook
4. Create a port waiver

## 1. Prerequisites

- Windows with desktop Microsoft Excel for the fidelity-preserving workbook writer.
- Python 3 with `openpyxl` for result extraction.
- Python 3 with `lxml` for macro-preserving waiver generation.

## 2. Extract test results

```powershell
python scripts/extract_beam_delivery_results.py `
  "C:\path\Sol BD Assembly - P315.xlsx" `
  --output "C:\working\P315-results.json"
```

The extractor reports workbook locations and extrema. Review its output against the workbook before making a compliance determination.

## 3. Update a verification workbook

Create an entries JSON array:

```json
[
  {
    "requirement_id": "BRD_00108",
    "procedure": "Sol BD Assembly - P315.xlsx\nCompliance tab, rows 6-7",
    "compliance": "Non-compliant",
    "verification_value": "Port 315 Col_Low2 v = -729 um",
    "artifacts": "Sol BD Assembly - P315.xlsx (Compliance tab, rows 6-7)",
    "summary": "Test method, all results, limiting result, failures, comparison, and disposition.",
    "status": "In Work"
  }
]
```

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/update_verification_workbook.ps1 `
  -RequirementsPath "C:\working\Beam_Delivery_Requirements_v4p1.xlsx" `
  -Port P315 `
  -EntriesJson "C:\working\P315-entries.json" `
  -OutputPath "C:\working\Beam_Delivery_Requirements_v4p1_P315_working.xlsx"
```

The script refuses to overwrite the input or an existing output. Review the output diff before adopting it as the workspace copy.

## 4. Create a port waiver

Create a waiver configuration:

```json
{
  "waiver_number": "WAIVER_TBD",
  "title": "Port 315 Optical Performance",
  "requirements_documents": [
    {"arena_doc_no": "NA", "revision": "4p1", "title": "Beam_Delivery_Requirements_v4p1"},
    {"arena_doc_no": "NA", "revision": "v9", "title": "Sol Beam Spec Table_v9"}
  ],
  "requirements": [
    {
      "id": "BRD_00108",
      "is_text": "Beam waist axial position tolerance shall be +/- 500 um from nominal.",
      "prefix": "Beam waist axial position tolerance shall be +/- ",
      "old_value": "500",
      "new_value": "729",
      "suffix": " um from nominal for Port 315."
    }
  ],
  "rationale": "Factual draft rationale; identify pending engineering decisions.",
  "system_impacts": "Potential system impacts and required review.",
  "efforts": "Testing, rework, and retest efforts performed to date.",
  "impacts": [
    {"item": "Port 315 Beam Delivery assembly", "description": "Affected as-tested hardware."},
    {"item": "Sol BD Assembly - P315.xlsx", "description": "Verification evidence record."},
    {"item": "Physics Package Port 315 interface", "description": "Integration interface requiring review."}
  ],
  "correction_action": "Required review, rework/retest, and closure actions."
}
```

Do not put requirement IDs in `impacts`; the generator rejects them because requirements belong in Section 4.

Run:

```powershell
python scripts/create_port_waiver.py `
  --config "C:\working\P315-waiver.json" `
  --output "C:\working\DRAFT_WAIVER_TBD_P315.docm"
```

The generator defaults to the bundled v4p1 template, refuses to overwrite an existing output, preserves embedded macros, expands Section 4 for any number of requirements, and marks unused Section 8 rows `N/A`.
