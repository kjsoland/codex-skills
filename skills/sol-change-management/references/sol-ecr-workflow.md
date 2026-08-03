# Sol ECR Workflow Reference

## Sources

Workspace root:

`$env:USERPROFILE\Documents\AI Workspace`

Sol Change and Decision Log:

`https://app.smartsheet.com/sheets/4mJF93pjGwJv96c5hcHVXfFc3CPwq4JHFjphfV21`

Sheet ID:

`7435158395244420`

Configuration Management Plan local synced source:

`$env:USERPROFILE\Quantinuum LLC\Sol Hardware Project Team - Sol Project Team Channel\Systems\Configuration Management\20260423_Release_v1\Sol_Configuration_Management_Plan_v1.docx`

SEMP local synced source:

`$env:USERPROFILE\Quantinuum LLC\Sol Hardware Project Team - Sol Project Team Channel\Systems\SEMP\Sol_SEMP_v3.docx`

Search SharePoint links locally first under synced Quantinuum or OneDrive folders. Use web access only when the synced local copy cannot be found or is stale. For impact assessment, inspect only the released baseline controlled document and the current/proposed working controlled document; do not search supplemental folders or side files as evidence sources unless Kyle explicitly asks for a separate supplemental review.

## User-Facing Link Hygiene

Use local synced paths internally for file operations, but avoid printing full `C:\Users\<name>\...` paths in user-facing summaries, Smartsheet drafts, and change-summary source tables unless Kyle explicitly asks for the local path.

For controlled documents under the synced Sol SharePoint tree:

`C:\Users\<name>\Quantinuum LLC\Sol Hardware Project Team - Sol Project Team Channel\<relative path>`

Use a known-good SharePoint web URL only when it was copied from SharePoint, Smartsheet, OneDrive metadata, or another authoritative source. Do not invent SharePoint URLs by string-converting a local sync path; those links can be tenant/library/channel-specific and may not open.

If no known-good URL is available, use a SharePoint-relative label such as `Sol Project Team Channel/Systems/ICDs/...` instead of the full local path. In tables, put the relative label in code formatting rather than markdown link syntax.

For local generated package artifacts under the AI Workspace, use workspace-relative labels such as `Change Management/<package>/<file>` in user-facing text. Once the artifact is attached to Smartsheet, prefer the Smartsheet row/attachment reference over a local absolute path.

## Package Layout

Use this layout under `Change Management/<slug>-change-package`:

```text
<slug>_change_summary.md
<slug>_change_summary.pdf
<slug>_impacted_docs_assessment.md (optional workup only; fold final contents into change_summary.md)
<slug>_smartsheet_draft.md
<slug>_smartsheet_record.md
assets/
smartsheet-dry-run/
```

Use `change_summary.md` as the editable source artifact and generate `change_summary.pdf` as the WAS/IS Change Artifact for review and Smartsheet attachment. Attach the PDF to the official Smartsheet row after row creation or update. Do not attach the markdown instead of the PDF unless Kyle explicitly requests it. The markdown remains the authoritative editable source; do not rely on a separate impacted-docs markdown file unless Kyle explicitly requests one.

## Change Summary Contents

Every change summary should include:

- `Compared Source Artifacts` section with the standard table format below.
- Executive summary.
- Change item list with WAS, IS, rationale when known, and technical impact for actual changes only. Do not create `CR-#` sections for unchanged tabs, figures, tables, document areas, or verification checks.
- On reruns after source updates or corrections, replace stale assessment language with the current release-to-proposed deltas. Do not include process history such as previous inspections, removed temporary content, false starts, or statements that earlier findings are no longer true unless Kyle explicitly requests that audit trail.
- Graphics/figure impact findings when the changed data appears in diagrams, screenshots, embedded images, layout views, or figure captions inside the actual released/current controlled document.
- Complete material deltas for each changed/impacted controlled document, including concurrent changes found in the same working revision. Attribute each delta to the active CDL, another known CDL, concurrent/unattributed content, or a release check; do not silently omit changes merely because they are outside the active CDL.
- Review checks or open questions.
- `Impacted Docs Assessment` section.
- `Generated Visual Assets` section when screenshots, crops, extracted figures, or annotated graphics are produced; treat it as an index only, not the primary evidence location.
- SharePoint URLs or privacy-safe path labels for source evidence; avoid full local user-profile paths in user-facing artifacts.

When the user has not yet provided rationale, identify changes first and prompt for change rationale one item at a time or in a compact list.

## Compared Source Artifacts

Use this section title and table format in every change summary. Do not use a loose `Source Files` bullet list.

```markdown
## Compared Source Artifacts

| Role | Released/Baseline | Current/Proposed | Evidence Used |
|---|---|---|---|
| <changed subject document> | `<SharePoint-relative released baseline label>` | `<SharePoint-relative current/proposed label>` | <comparison basis: workbook diff, DOCX text/table diff, figure audit, requirements diff, etc.> |
```

Only include controlled documents that are the changed subject documents or likely impacted controlled documents being directly compared for a required update. Do not include downstream documents inspected only to determine that there is no impact; put those review findings in `Reviewed But Not Directly Impacted`. Do not include Smartsheet/CDL row reads, changelogs, raw notes, generated package artifacts, temporary exports, local analysis files, or other context/supporting sources. If those sources are needed for rationale or workflow traceability, mention them elsewhere such as `Smartsheet Notes`, reviewer notes, or dry-run records. Use SharePoint-relative labels for controlled Sol documents unless a known-good SharePoint URL is available, and never use local absolute user-profile paths in this table.

## PDF Generation

Regenerate the PDF after every change-summary or visual-asset update and before any Smartsheet write. Use the bundled renderer by default:

```powershell
python "$env:USERPROFILE\.codex\skills\sol-change-management\scripts\render_change_summary_pdf.py" "<package>\<slug>_change_summary.md" --pdf "<package>\<slug>_change_summary.pdf"
```

The renderer writes a print HTML copy under `smartsheet-dry-run/` and prints the PDF with local Chrome or Edge. It applies the Quantinuum template-style footer by default: plain text, no colored footer background, `Quantinuum Internal Only` centered, and generated date plus page count on the right. If the package has a more descriptive final PDF filename, pass that path with `--pdf` and update the Smartsheet draft/payload to match. Verify that the PDF exists, is non-empty, that embedded graphics render, and that the footer marking appears. If Chrome/Edge is unavailable, use another local Markdown-to-PDF route, but still produce a PDF with the same footer marking and record the chosen path.

## Visual Evidence

When the change is graphical, layout-based, diagram-heavy, figure-driven, or Kyle asks for graphics:

- Proactively inspect embedded media, figure captions, diagrams, screenshots, and layout views in the released/current controlled documents.
- Run a whole-document embedded-figure diff before finalizing the package. For DOCX/PPTX/XLSX-style sources, inventory every figure caption and embedded media object in both the released baseline and current/proposed document, including media target, hash, file format, dimensions, and nearby caption text. Classify figures as unchanged/renumbered, changed, added, removed, or ambiguous. Visually inspect every changed, added, removed, and ambiguous candidate; do not stop after the expected figure or the first obvious delta. Record materially useful review evidence in the package or dry-run folder.
- Treat image re-encoding or format conversion alone as review evidence, not a change item, when the visual content is unchanged after inspection. Treat connector orientation, pin-number orientation, callout/label changes, added interface views, replaced CAD/drawing views, dimensional changes, and changed layout views as actual figure changes.
- For likely downstream docs, inspect whether controlled graphics repeat changed beam allocations, interfaces, labels, component placement, rack layouts, requirement applicability, or other visualized baseline content.
- Treat controlled documents that require graphics updates as impacted docs in `Related Docs?`; generated comparison images are evidence attachments, not controlled Systems documents.
- Base graphics impact recommendations on the actual released/current controlled document. Do not search or use supplemental graphics, exported art files, adjacent graphics folders, extracted media work folders, or other side material as impacted-doc drivers. If Kyle explicitly requests supplemental review, document it separately from the controlled-document impact assessment.
- Create reviewer-friendly images such as before/after screenshot crops, annotated current-state context views, or extracted DOCX/Visio/PowerPoint figure comparisons.
- Put a visible box, arrow, highlight, or callout around each changed figure/diagram region. If the same figure contains multiple CDL scopes, use distinct scope-coded colors and label each annotation. Do not rely on prose alone to tell the reviewer where to look.
- Store generated images under `<package>/assets/`.
- Embed each image directly in the applicable `CR-#` or change item section of `<slug>_change_summary.md`, adjacent to the WAS/IS/impact text it supports.
- For before/after graphics, label the baseline image as `WAS - old baseline picture` and the current image as `IS - new current picture`. Prefer side-by-side, equal-width WAS/IS pairs, such as a two-column markdown table. If the images become unreadable or do not fit cleanly, stack them vertically, but preserve the explicit WAS/IS labels immediately with each image.
- When a designed PNG/SVG already contains the detailed WAS/IS rows, use that visual as the sole table-level evidence in the change item. Do not place a Markdown table containing the same rows immediately before or after it. A one- or two-sentence lead-in is sufficient. This non-duplication rule does not replace the required source-artifact or impacted-docs Markdown tables.
- Regenerate `<slug>_change_summary.pdf` after updating images or image references so the review artifact shows the latest graphics.
- When a current/proposed document adds a new figure, table, diagram, screenshot, or embedded graphic with no released-baseline counterpart, document the item as `WAS = none` and `IS = new figure` (or `new table` / `new graphic` as applicable), including the new figure/table number and caption.
- Do not group visual evidence only near the top of the summary. A top-level `Generated Visual Assets` table is an index; the actual evidence embed belongs with its associated change item.
- Add a `Generated Visual Assets` table near the top of the change summary with asset path and purpose when useful.
- List generated images as embedded visual evidence/package assets in `<slug>_smartsheet_draft.md` and the payload preview. Do not list them as separate Smartsheet attachments unless Kyle explicitly requests separate image files.
- Do not include generated image assets in `Related Docs?`; they are evidence attachments, not controlled Systems documents.

## Complete Impacted-Document Comparison

For each changed subject or impacted controlled document included in the package:

1. Inventory every worksheet/section and review values, formulas, tables, added/removed logical records, freeze panes, hidden/visible content, validations, charts, embedded figures, and release-relevant layout settings.
2. Use stable logical identifiers when inserted/deleted rows make a coordinate diff noisy. For formulas that refer to shifted rows, resolve references back to logical records before classifying a material change.
3. Separate the active-CDL delta from other known-CDL and concurrent/unattributed deltas. Show concurrent changes when a complete revision audit is requested or necessary for release review, but state that they do not expand the active CDL scope without owner confirmation.
4. Record no-change worksheet/figure results only in concise audit evidence; do not create change items for them.
5. Preserve machine-readable comparison evidence under `smartsheet-dry-run/` when practical.

## Impacted Docs Assessment

Interpret `Related Docs?` as `Impacted Docs`: the changed subject document plus released Systems documentation expected to require updates because of the proposed source change. List the subject document first, followed by downstream impacted docs.

Every change summary must include this table pattern:

```markdown
### Likely Impacted Released Docs

| Document | Released file inspected | Impact driver | Assessment |
|---|---|---|---|
| <subject or downstream doc> | `<released baseline path>`; current `<current/proposed path>` | <changed value, interface, figure, requirement, or duplicated data driving impact> | <Changed subject document or Impacted. State the required review/update.> |
```

Use that four-column table as the primary impacted-docs display. Include changed subject documents first, then downstream impacted docs, matching the `Related Docs?` order. The PDF renderer converts the impacted-docs tables below into print-friendly field cards, so keep the markdown table structure for review/editing. Escape literal pipe characters inside cell text as `\|` when practical; the renderer also recovers the standard impacted-doc table shape if an interface string contains unescaped pipes.

```markdown
### Possible Follow-Up Impact

| Document | Evidence checked | Why it is not in the proposed field yet |
|---|---|---|

### Reviewed But Not Directly Impacted

| Document | Evidence checked | Assessment |
|---|---|---|
```

Use reviewed-but-not-directly-impacted evidence only when it materially de-risks the review. Do not list routine unchanged tabs or sections just to prove they were checked, and never turn no-change findings into numbered change items.

Candidate Systems-document families come from the SEMP Technical Baseline, but evidence must come from released or working controlled documents only:

- Requirements.
- Architecture documents.
- ICDs.
- Design drawings and models.
- Assembly instructions.
- Test procedures.
- Calibration, CONOPS, diagrams, and spec tree material when controlled or release-relevant.

Check local Systems folders first for controlled released/current documents:

- `Systems\Requirements`
- `Systems\ICDs`
- `Systems\Spec Tree`
- `Systems\Systems Diagrams`
- `Systems\Calibration Plan`
- `Systems\CONOPS`
- `Systems\Configuration Management`
- `Systems\SEMP`

Do not list:

- Generated change summaries, generated PDFs, slide packages, or local render artifacts.
- Raw change notes.
- Non-Systems reference files.
- Documents that merely consume/reference the changed data unless they are expected to require updates.
- Supplemental folders/files such as loose `Graphics`, `Worksheets`, `Old`, CDR delivery snapshots, exports, extracted media, or local analysis artifacts unless Kyle explicitly asks for a separate supplemental review.

## Classification

Use the CM plan definitions as initial drafting guidance:

| Class | Drafting rule |
|---|---|
| `1` | Change affects multiple subsystems, multiple ICDs, external/system interfaces, cost/schedule, or system-level integration. |
| `2` | Change is localized design maturity, a single-subsystem correction, or a documentation clarification with limited downstream effect. |
| `N/A - no risk, decision only` | Use only for decisions that do not alter controlled baseline content or risk posture. |

When uncertain, use `Flag for Discussion = true` and state the uncertainty in `Technical Impact?`.

## Draft Row Mapping

Prepare a local draft before writing the live row.

For long narrative draft fields such as `Change or Decision Description` and `Technical Impact?`, prefer a readable title-plus-bullets shape instead of dense paragraphs:

```text
Title:
- bullet 1
- bullet 2
- bullet 3
```

In local markdown tables, use `<br>-` line breaks inside the cell. In Smartsheet JSON payloads, use newline bullets (`\n- ...`) so the live row preserves the structure.

| CM plan need | Smartsheet field |
|---|---|
| Unique ECR number | `Row ID`; omit on create, Smartsheet auto-populates. |
| Date initiated | `Date Added`; omit on create, Smartsheet auto-populates. |
| Change owner/originator | `Originator`; default Kyle Solander unless user specifies otherwise. |
| Change description and rationale | `Change or Decision Description`. |
| Classification | `ERB Class?`; use `Flag for Discussion` when needed. |
| Documentation impact | `Related Docs?`; include the changed subject document first, then downstream impacted docs. |
| Technical/performance impact | `Technical Impact?`. |
| Cost impact | `Financial Impact (nearest $10k)`. |
| Schedule impact | `Schedule Impact (Days)`. |
| Risk impact | `Related Risk Item?`. |
| Impacted parties | `Assessors`; optionally summarize teams in `Technical Impact?`. |
| ERB decision | `Disposition`, `Disposition Date`, approval fields. |
| Implementation complete | `Implemented?`; one row-level status for all impacted docs. |
| Released document completion log | `Decision or Change Output`; leave blank until impacted documents are actually released. Each listed document means that document is released/done for the change. |
| WAS/IS artifact | Smartsheet row attachment, normally the generated `<slug>_change_summary.pdf`. |

Default new proposed row values after Kyle approval:

- `Flag for Discussion = true` if discussion is expected or any uncertainty remains.
- `Disposition = New`.
- `Implemented? = No`.
- `Decision or Change Output` blank unless one or more impacted documents have already been released. Do not populate proposed approvals, intended outcomes, or release plans in this field.
- `Schedule Impact (Days) = 0` only when no schedule impact is expected or user confirms zero.
- `Financial Impact (nearest $10k) = $0` only when no cost impact is expected or user confirms zero.

Leave lifecycle fields blank until ERB or workflow action:

- `Decision need-by date?`
- `Related Risk Item?`
- `Disposition Date`
- `Assessors approval`
- `Final Approver`
- `Final Approval`
- `Final Approver approval`

For implementation tracking:

- Use `Decision or Change Output` as a concise release ledger, for example `Released Network and Comm ICD v2p0 on 2026-07-01`.
- Add impacted documents to `Decision or Change Output` only after they are released. Listing a document there means it is done for that change.
- Keep `Implemented? = No` before release work starts, `In Process` while only some impacted documents are released, and `Yes` only when all impacted documents in `Related Docs?` are released.

## Current Smartsheet Columns

Verify schema before writing, but these columns were observed on 2026-07-01:

| Column | ID | Type |
|---|---:|---|
| `Row ID` | `6996395309617028` | auto/system text-number |
| `Flag for Discussion` | `5886485312786308` | checkbox |
| `Date Added` | `4293246749724548` | created date |
| `Originator` | `8796846377095044` | contact list |
| `Change or Decision Description` | `211859587420036` | text-number |
| `Decision need-by date?` | verify | date |
| `ERB Class?` | `5662887266439044` | picklist |
| `Schedule Impact (Days)` | `2463659401105284` | text-number |
| `Financial Impact (nearest $10k)` | `4715459214790532` | text-number |
| `Technical Impact?` | `3027396549365636` | text-number |
| `Related Docs?` | `4504787989778308` | text-number |
| `Related Risk Item?` | verify | text-number |
| `Disposition` | `6967259028475780` | picklist |
| `Assessors` | `1337759494262660` | multi-contact list |
| `Decision or Change Output` | `5841359121633156` | text-number |
| `Implemented?` | `6720257744654212` | picklist |

Known picklist values:

- `ERB Class?`: `1`, `2`, `N/A - no risk, decision only`.
- `Disposition`: `New`, `Approved`, `Approved+WIP`, `Approved+DONE`, `Cancelled`, `Rejected`, `Wait`.
- `Implemented?`: `No`, `In Process`, `Yes`.

## Smartsheet API Guardrails

Use `SMARTSHEET_ACCESS_TOKEN` from the environment. Never echo or write the token.

Before create/update:

1. Read schema with `level=1` when contacts are involved.
2. Search for duplicates by source document name, revision, and description text.
3. Save a local payload preview under `smartsheet-dry-run`.
4. Confirm with Kyle before the live write unless he has already explicitly approved.

Important implementation details:

- Row-add and row-update payloads must be JSON arrays of row objects. In PowerShell, single-item arrays are easily unwrapped during `ConvertTo-Json`; force an array wrapper when updating exactly one row.
- Omit `Row ID` and `Date Added`; Smartsheet auto-populates them.
- In PowerShell strings, use `"https://api.smartsheet.com/2.0/sheets/${sheetId}?level=1"` so the query string does not get parsed as part of the variable name.
- `Originator` is a `CONTACT_LIST`; use `objectValue` with `objectType = CONTACT`, `name`, and `email` when updating. Smartsheet can reject plain `value` writes with error `1235`, `Use objectValue instead`.
- `Assessors` is `MULTI_CONTACT_LIST`; use `objectValue` with `objectType = MULTI_CONTACT` and contact values.
- If row creation succeeds but attachment fails, retry the attachment to the created row object ID. Do not create a second row.
- For PDF attachment upload, use raw file upload with `Content-Type: application/pdf` and `Content-Disposition: attachment; filename="<file>.pdf"`. Multipart upload can fail with Smartsheet error `1011` about missing or invalid `Content-Disposition`.

Known contact values from the sheet:

```json
[
  {"objectType":"CONTACT","name":"Kyle Solander","email":"kyle.solander@quantinuum.com"},
  {"objectType":"CONTACT","name":"Kyle McKay","email":"kyle.mckay@quantinuum.com"},
  {"objectType":"CONTACT","name":"Justin Gerber","email":"justin.gerber@quantinuum.com"},
  {"objectType":"CONTACT","name":"Loren Jones","email":"loren.jones@quantinuum.com"},
  {"objectType":"CONTACT","name":"Jenny Wu","email":"jenny.wu@quantinuum.com"}
]
```

Example assessor object:

```json
{
  "columnId": 1337759494262660,
  "objectValue": {
    "objectType": "MULTI_CONTACT",
    "values": [
      {"objectType": "CONTACT", "name": "Kyle Solander", "email": "kyle.solander@quantinuum.com"},
      {"objectType": "CONTACT", "name": "Kyle McKay", "email": "kyle.mckay@quantinuum.com"},
      {"objectType": "CONTACT", "name": "Justin Gerber", "email": "justin.gerber@quantinuum.com"},
      {"objectType": "CONTACT", "name": "Loren Jones", "email": "loren.jones@quantinuum.com"},
      {"objectType": "CONTACT", "name": "Jenny Wu", "email": "jenny.wu@quantinuum.com"}
    ]
  }
}
```

## Live Row Completion

After creating or updating a live row:

1. Regenerate and attach the change summary PDF as the WAS/IS Change Artifact.
2. Read the row back with attachments included.
3. Save API payloads and responses in `smartsheet-dry-run/`.
4. Create or update `<slug>_smartsheet_record.md` with:
   - Sheet URL.
   - Row ID.
   - Row object ID.
   - Row number at creation if available.
   - Date Added.
   - Attachment ID and PDF name.
   - Entered field values.
   - Local API record paths.
5. Update `<slug>_smartsheet_draft.md` status from draft to official row created.
6. Scan local files for accidental token strings before final response.

## Proven Example

Earlier completed packages may have attached markdown before the PDF-first convention. Do not copy that older attachment behavior. Use this package only as a general row/payload pattern:

`Change Management\network-comm-icd-v2p0-change-package`

Official result:

- Row ID: `SOL-052-CDL`
- Row object ID: `1303949780647812`
- Attachment in that older example: `network_comm_icd_v2p0_change_summary.md`
- Attachment ID: `403962762530692`

Use this package as a pattern for future Sol change entries, but do not copy row IDs or assume new auto-number values.
