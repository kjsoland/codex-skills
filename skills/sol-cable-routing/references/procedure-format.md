# Cable-kit procedure format

Use the existing Sol procedure layout for new kits and revisions. This applies to the visual presentation and installation flow, not only the output file extensions. Change the format only when the user requests it.

## Inspect and reuse the existing layout

Find the current delivered kit procedures under the BOM root in `files-and-workflow.md`. Read their generation sources in the workspace's `Sol Cable Routing Procedure/Source` folder and visually inspect representative rendered slides before editing. **Network and Comm is the master format** for the table of contents, slack rules, and route-block slides. **Core Control is the grouping-slide template** when cable grouping applies. Other kits can illustrate the same conventions, but do not replace these templates merely because another kit is newer.

Existing implementations worth reusing:

- `build_network_comm_routing_deck.py`: `slide_index` and `slide_full_route_graphic` provide the master TOC and route-block formats.
- `build_core_control_procedure.py`: `bundle_preparation` provides the grouping-slide layout and three preparation steps.
- `kit_front_matter.py`: original mobility/slack-allocation slide used across the kits.

Keep these project drawings and generated artifacts in their existing local/SharePoint locations. They are examples to inspect, not assets to copy into a public skill repository.

## Front matter and installation flow

Keep the established 16:9 slides, white background, teal titles and rules, readable Arial text, and consistent kit/revision/page footer. Use the shared styling helpers instead of inventing a separate design.

Include the title/scope, linked released floor plan, six-step installation workflow, linked group/route index, direction-specific end-label instructions, and the original graphical mobility/slack-allocation slide before the routes. The workflow links to the applicable BOM, label files, ICD and companion checklist. Reuse the shared slack slide; update its displayed revision or audit counts only when supported by the selected workbook. A kit-specific exception must not overwrite the shared asset or other kits.

Preserve the Network and Comm TOC style: three columns of rounded route entries, alternating pale/white fills, circular page-number badges, and linked entries. Include the grouping-preparation pages in navigation while keeping the following route-slide number clear. Do not replace this with a source-family summary table.

On the cable-label slide, show the ICD acronym legend beside the From/To label examples. Obtain the code-to-document-name mappings from the current Integration procedure/Integration Plan To/From ICD list; use the current synced HTML/source, not a remembered or guessed list. Link or record that source, retain all listed codes, and emphasize the current kit's acronym. Refresh the chart when the Integration procedure changes. The established Integration Plan location is `Integration/Integration Plan/Sol_Integration_Plan_v3.html` under the synced project-team folder (also accessible through the workspace's `integration-plan-playground/v2` junction).

Keep the operational slides concise. Put detailed source reconciliation and audit tables after a backup divider or in the companion workbook; retain an applicable source note on the affected route slide.

## Route-and-marks slide

The map and marking bubbles belong together on the primary route slide:

- Center the actual route drawing from the selected route workbook, large and at its original aspect ratio. Keep the route visible and readable; do not replace it with a generic horizontal cable line or defer it to an appendix.
- Place the source marking bubble to the left and the destination marking bubble to the right. Name the physical endpoints and show each connector as its own `0 in` datum. Use prominent red rack-exit, gantry-entry or fixed-boundary distances as applicable. Keep mobility between the two rack-end marks.
- Put the cable coverage and selection under the source bubble: exact ICD row(s), connector pair(s), part, length and count. Use the preparation table/checklist for a long group rather than shrinking the text.
- Put worksheet Total, selected cable length, purchase excess, storage allocation and length reconciliation under the other bubble.
- Include the workbook color legend, identifying the selected route color. Resolve theme/tint colors and preserve multi-color or gradient routes where present; do not assign arbitrary colors.
- Place source discrepancies in the established lower warning banner or sidebar without hiding the map. Keep unresolved dimensions visibly unresolved. An arithmetic reconciliation is not source approval.

Do not use a separate marks-only page plus route-table appendix as a substitute for this layout. Route-detail rows can remain in the checklist/audit workbook.

## Cable grouping

Group by the user's requested source component or destination, then separate by compatible route, part/length and connector datum. A common component alone does not make branches or marking distances interchangeable.

For a useful multi-cable group, insert a **Bundle Preparation** slide immediately before its route slide. Follow Core Control's `bundle_preparation` format: connector-pair table on the left; `1 GROUP`, `2 SECURE WITH TAPE`, and `3 MARK THE BUNDLE` instructions on the right; any relevant source note below. Keep individual end fan-outs free. Link preparation to the following route slide and keep the group IDs consistent in the index and checklist. Single cables can use the route slide directly.

## Format validation and delivery

Compare rendered output side by side with at least one current delivered procedure. Inspect the title, workflow, shared slack slide, a multi-cable preparation/route pair, a rack-to-rack route, and a rack-to-fixed route when those exist. Check map size/aspect, endpoint bubbles, red dimensions, selected color key, warning placement, readable text and clipping. Verify page references and hyperlinks after reordering.

On a format-only correction, preserve cable scope, source data, dimensions, unresolved notes, and existing installer/checker entries. Back up replaced deliverables and remap only the necessary navigation fields. Recheck cable coverage and marking reconciliation, then deliver PDF, PowerPoint and checklist together beside the applicable BOM and labels, as specified in `files-and-workflow.md`.
