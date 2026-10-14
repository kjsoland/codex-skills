---
name: sol-cable-routing
description: Create or update Sol cable-kit routing procedures in the established PowerPoint/PDF format, including cable grouping and installation checklists; maintain the route workbook, route-length audits, tape marks and ICD traceback. Use for Sol cable routing and training packages, rather than harness drawings or cable-label exports alone.
---

# Sol Cable Routing

Use this skill for the Sol cable-routing workbook/training package. This is not the harness drawing workflow; it is a workbook + route-training + audit maintenance workflow.

## Before acting

Read the relevant reference before making changes:

- `references/routing-rules.md` for durable routing assumptions and tape-marker rules.
- `references/files-and-workflow.md` for paths, scripts, rebuild commands, and verification.
- `references/procedure-format.md` before creating or reformatting a cable-kit procedure.

Follow the established cable-routing procedure format unless the user explicitly requests a different format. **Network and Comm is the master for the TOC, slack-rules slide and route-block slides; use Core Control's grouping slide when grouping applies.** Inspect their rendered examples before building. Each route slide must show the large floor-plan route graphic with the endpoint marking bubbles on that same slide. Include the ICD acronym legend from the current Integration procedure on the cable-label slide. See `references/procedure-format.md` for the front matter, route layout and visual acceptance checks.

For component bundles, collect all signals between the same physical component pair before mapping route blocks; ports, signal names and worksheet-block boundaries do not define separate bundles. Verify route/part/length/datum compatibility and retain every cable's source traceback. The TOC has one entry per route section, naming both components and displaying its actual section-start slide number. See the grouping and navigation rules in `references/procedure-format.md`.

## Cable-kit procedure destination

Save cable-kit routing procedure deliverables in the applicable SharePoint-synced BOM cable-kit folder, beside its BOM and cable labels, unless the user specifies another destination. Put the PDF, PowerPoint, and installation checklist together and verify their links from that destination. The AI Workspace is a build/staging area; a workspace-only output does not complete delivery. See `references/files-and-workflow.md` for the BOM root and BD Beamplate destination.

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
