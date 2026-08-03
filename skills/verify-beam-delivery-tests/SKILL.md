---
name: verify-beam-delivery-tests
description: Map Sol Beam Delivery port test workbooks into Beam Delivery requirements verification columns and create or update port-specific requirement waiver drafts. Use when Codex must review Sol BD Assembly Excel results, select limiting or worst-case port values, populate O-Z verification evidence without modifying SharePoint sources, classify compliance and waiver status, or generate macro-enabled waiver redlines for noncompliant Beam Delivery requirements.
---

# Verify Beam Delivery Tests

Use the controlled requirements, port test workbook, and applicable Beam Spec Table to build traceable port-level verification evidence. Work only on a workspace copy unless the user explicitly authorizes a controlled-source edit.

## Required references

Read [references/verification-workflow.md](references/verification-workflow.md) before evaluating or writing verification evidence. Read [references/automation-inputs.md](references/automation-inputs.md) before using the bundled scripts.

## Workflow

1. Resolve the latest SharePoint-synced Beam Delivery requirements workbook and the requested `Sol BD Assembly - <port>.xlsx` result workbook. Use the result workbook, not its raw `.wcf` instrument folder, unless raw-data review is explicitly requested.
2. Copy controlled inputs into a workspace working folder. Preserve the SharePoint files as sources of truth and never overwrite them during verification drafting.
3. Run `scripts/extract_beam_delivery_results.py` or inspect the workbook directly. Separate direct test evidence from supporting inspection evidence.
4. For each direct requirement, compare every applicable collimator and axis against the controlled value. Put the limiting signed datum in the port's verification-value column and put the full population, failures, method, and caveats in the verification summary.
5. Prepare reviewed JSON entries and run `scripts/update_verification_workbook.ps1`. The script writes a new workbook; validate its cell-level diff before replacing a workspace working copy.
6. Keep `Verified By` blank until an authorized verifier signs. Keep every row `In Work` during draft review.
7. For each noncompliant port, keep the compliance statement `Non-compliant`. If a waiver is requested, include every noncompliant requirement for that port in one waiver and generate it with `scripts/create_port_waiver.py` and the bundled macro-enabled template.
8. Add the waiver filename to `Verification Artifact(s)` and state the proposed redline in the summary. An unsigned waiver does not change compliance. After approval, update the covered rows to `Compliant with Waiver` and complete status/signature fields only as authorized.
9. Validate the output package, macro preservation, requirement IDs, artifacts, summaries, and unchanged controlled sources.

## Guardrails

- Do not invent waiver numbers, approvers, signatures, test execution, measurement uncertainty, or engineering rationale.
- Do not convert planned ranges or checklist targets into completed test evidence without confirmation.
- Do not round an out-of-limit result into compliance unless an approved convention or uncertainty disposition explicitly allows it.
- Do not put requirement rows in waiver Section 8; Section 4 is the requirements list.
- Do not mark `Compliant with Waiver` before waiver approval.
- Preserve Excel fidelity with Excel automation and DOCM macros with package-preserving edits.

## Resources

- `scripts/extract_beam_delivery_results.py`: extract common Beam Delivery result tables and extrema to JSON.
- `scripts/update_verification_workbook.ps1`: write reviewed verification entries to a new Excel workbook.
- `scripts/create_port_waiver.py`: generate a port waiver with red strikethrough/underline values while preserving macros.
- `assets/Quantinuum_Requirement_Waiver_Template_v4p1.docm`: waiver template copied into generated waiver outputs.
