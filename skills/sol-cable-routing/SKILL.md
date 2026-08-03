---
name: sol-cable-routing
description: Maintain Sol cable routing workbook, routing-training slide deck, route-length audit, cable tape-marking examples, and ICD traceback outputs. Use when Codex is asked to edit or audit the Sol Floor Plan ICD cable route workbook, update cable routing/training slides, apply Sol routing rules such as waterfall-entry lengths or Tripp Lite rack assumptions, expand the deck to more route blocks, or explain route-file tape-marker calculations.
---

# Sol Cable Routing

Use this skill for the Sol cable-routing workbook/training package. This is not the harness drawing workflow; it is a workbook + route-training + audit maintenance workflow.

## Before acting

Read the relevant reference before making changes:

- `references/routing-rules.md` for durable routing assumptions and tape-marker rules.
- `references/files-and-workflow.md` for paths, scripts, rebuild commands, and verification.

Prefer the old slide/PDF training format unless the user explicitly asks for a written procedure. Do not create a standalone Markdown/PDF procedure as the default deliverable.

## Standard workflow

1. Locate the synced SharePoint workbook locally; do not browse SharePoint first.
2. Inspect the workbook before editing. Count affected rows and note excluded row families.
3. Back up the workbook before changing it.
4. Edit only the requested route labels/lengths/formulas. Do not modify `Actual` cable lengths unless the user explicitly says to.
5. Preserve formulas where possible. If changing a formula that uses a Tripp Lite base value, replace only the base term and preserve offsets.
6. Recalculate and save with Excel after direct `.xlsx` edits so cached formula values are available to `openpyxl(data_only=True)`.
7. Regenerate slide images/audit outputs, then rebuild the PowerPoint/PDF when the training package should stay current.
8. Verify from a fresh workbook copy and report counts, audit totals, and rebuilt output paths.

## Safety notes

- Never kill Excel or PowerPoint. If a workbook is locked by a visible user session, ask the user to close it or work from a safe copy.
- Preserve unrelated workbook content, formatting, and conditional formatting. Row insertion is higher risk than value/label edits; use Excel automation and re-check conditional formatting when inserting rows.
- Treat route workbook `Total` as authoritative after the route-detail rows have been added. Do not apply off-sheet waterfall or endpoint corrections to audits.
