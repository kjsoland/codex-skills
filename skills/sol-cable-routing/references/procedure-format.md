# Cable-kit procedure format

Use the existing Sol procedure layout for new kits and revisions. This applies to the visual presentation and installation flow, not only the output file extensions. Change the format only when the user requests it.

## Inspect and reuse the existing layout

Find the current delivered kit procedures under the BOM root in `files-and-workflow.md`. Read their generation sources in the workspace's `Sol Cable Routing Procedure/Source` folder and visually inspect representative rendered slides before editing. **Network and Comm is the master format** for the table of contents, slack rules, and route-block slides. **Core Control is the grouping-slide template** when cable grouping applies. Other kits can illustrate the same conventions, but do not replace these templates merely because another kit is newer.

Existing implementations worth reusing:

- `build_network_comm_routing_deck.py`: `slide_index` and `slide_full_route_graphic` provide the master TOC and route-block formats.
- `build_core_control_procedure.py`: `bundle_preparation` provides the grouping-slide layout and three preparation steps.
- `kit_front_matter.py`: `label_slide` / `refresh_kit_label` provide the mandatory shared labeling slide; `slack_slide` provides the original mobility/slack-allocation slide.
- `Templates/Sol_Cable_Routing_Label_Slide_Template.pptx` under the cable-routing work area: reusable single-slide template, with matching PDF/PNG previews. Its design comes from training slide 1, `Slides/slide_01_cable_labeling.png`.

Keep these project drawings and generated artifacts in their existing local/SharePoint locations. They are examples to inspect, not assets to copy into a public skill repository.

## Front matter and installation flow

Keep the established 16:9 slides, white background, teal titles and rules, readable Arial text, and consistent kit/revision/page footer. Use the shared styling helpers instead of inventing a separate design.

Include the title/scope, linked released floor plan, six-step installation workflow, linked group/route index, direction-specific end-label instructions, and the original graphical mobility/slack-allocation slide before the routes. The workflow links to the applicable BOM, label files, ICD and companion checklist. Reuse the shared slack slide; update its displayed revision or audit counts only when supported by the selected workbook. A kit-specific exception must not overwrite the shared asset or other kits.

Preserve the Network and Comm TOC style: three columns of rounded route entries, alternating pale/white fills, circular page-number badges, and linked entries. Use **one entry per route section**; name both physical components (including rack/location), and show the actual section-start slide number in the badge. Link to the grouping/preparation slide when present, otherwise the route slide. Do not list grouping and marking as separate TOC entries or show separate preparation/marking page numbers in the TOC. The preparation slide can link forward to its marking slide. Derive numbers from the final slide order and verify both displayed numbers and PDF/PowerPoint link targets after reordering. Do not replace this with a source-family summary table.

Every cable routing procedure includes the shared **Cable Labeling, ICD Acronyms, and Tape Workflow** slide in its front matter, before routing begins. Retain the training slide's From-End and To-End examples on the left, the complete ICD acronym chart on the right, and the six-step tape workflow along the bottom. A label-only slide, a kit acronym alone, or a link to another procedure does not satisfy this requirement. Use `kit_front_matter.label_slide` or `refresh_kit_label` in the generator so rebuilding cannot omit the chart.

Obtain the code-to-document-name mappings from the current Integration procedure/Integration Plan To/From ICD list; use the current synced HTML/source, not a remembered or guessed list. Link or record that source, retain all listed codes, and emphasize the current kit's acronym. The established Integration Plan location is `Integration/Integration Plan/Sol_Integration_Plan_v3.html` under the synced project-team folder (also accessible through the workspace's `integration-plan-playground/v2` junction). Refresh the chart when this source changes; the shared helper reads it and records the source hash in the generated `.label.json` sidecar.

Adapt the examples and kit notes without dropping endpoint definitions, blank-designator rules, print instructions, source exceptions or missing-label warnings. `Source/kit_label_profiles.json` supplies local defaults; pass current source-derived examples and instructions when rebuilding a kit. Preserve the complete FROM/TO order on both examples. Use shorter example boxes when needed to retain detailed kit rules legibly. Keep the kit footer and correct page number. Use the selected route's marking rules rather than carrying the training deck's fixed slide-number references or workbook revision into another deck.

Keep the operational slides concise. Put detailed source reconciliation and audit tables after a backup divider or in the companion workbook; retain an applicable source note on the affected route slide.

## Route-and-marks slide

The map and marking bubbles belong together on the primary route slide:

- Center the actual route drawing from the selected route workbook, large and at its original aspect ratio. Keep the route visible and readable; do not replace it with a generic horizontal cable line or defer it to an appendix.
- Place the source marking bubble to the left and the destination marking bubble to the right. Name the physical endpoints and show each connector as its own `0 in` datum. Use prominent red rack-exit, gantry-entry or fixed-boundary distances as applicable. Keep mobility between the two rack-end marks.
- Put the cable coverage and selection under the source bubble: exact ICD row(s), connector pair(s), part, length and count. Use the preparation table/checklist for a long group rather than shrinking the text.
- Put worksheet Total, selected cable length, purchase excess, storage allocation and length reconciliation under the other bubble.
- Keep the workbook color legend along the bottom, with the selected route outlined. Resolve theme/tint colors and preserve multi-color or gradient routes where present; do not assign arbitrary colors. Preserve the established large centered map and left/right endpoint callouts; the CMOS power / Detection motor slide is the confirmed layout reference.
- Place source discrepancies in the established lower warning banner or sidebar without hiding the map. Keep unresolved dimensions visibly unresolved. An arithmetic reconciliation is not source approval.

Do not use a separate marks-only page plus route-table appendix as a substitute for this layout. Route-detail rows can remain in the checklist/audit workbook.

## Cable grouping

For component bundling, collect **all signals between the same two physical components**, regardless of electrical direction, signal/function name, connector number or whether the ICD rows are adjacent. Identify a component by location/rack plus component name; preserve every individual port pair as a bundle member. Normalize only proven naming aliases. A destination-only label such as `BOC` is insufficient when several drivers connect to it: show both components in the section title, TOC and grouping table.

Map those members to their route sources after identifying the component pair. Merge compatible members across separate worksheet blocks when the physical path, purchased part/length, connector datums, slack allocation and marks are verified equivalent; retain every original block reference and each cable's traceback. Do not split an otherwise compatible bundle merely because signal families or worksheet titles differ. If a component pair needs incompatible routes or marks, retain a common section and identify the necessary sub-bundles and reasons. A common rack, driver or route color alone does not establish equivalence: different destination components need identifiable bundles/fan-outs, and a shared route does not make their endpoint dimensions interchangeable.

Gates/LSC examples: `CE5 / AO_RFDriver_08` outputs 1-8 to `493 BS / BOC` S7-S14 form one eight-cable bundle. The current ICD places BOC at 493 BS; do not substitute 370 BS based on stale route-detail wording. `CE6 / EOM_RFCOMBINER` to `TR3 / TP3` includes all three cables even though Ba/Yb repump entries occupy two equivalent blocks. `AO_RFDriver_10` has six cables to BOA and two to BOB; keep those destination bundles identifiable. These examples do not authorize changing ICD endpoints or resolving open geometry warnings.

For a useful multi-cable group, insert a **Bundle Preparation** slide immediately before its route slide. Follow Core Control's `bundle_preparation` format: connector-pair table on the left; `1 GROUP`, `2 SECURE WITH TAPE`, and `3 MARK THE BUNDLE` instructions on the right; any relevant source note below. Keep individual end fan-outs free. Link preparation to the following route slide and keep the group IDs consistent in the index and checklist. Single cables can use the route slide directly.

## Format validation and delivery

Compare rendered output side by side with at least one current delivered procedure. Inspect the title, workflow, shared label/acronym slide, shared slack slide, a multi-cable preparation/route pair, a rack-to-rack route, and a rack-to-fixed route when those exist. Confirm both PDF and PowerPoint include every current acronym mapping, correct label direction and the kit-specific instructions. Check map size/aspect, endpoint bubbles, red dimensions, selected color key, warning placement, readable text and clipping. Verify page references and hyperlinks after reordering.

On a format-only correction, preserve cable scope, source data, dimensions, unresolved notes, and existing installer/checker entries. Back up replaced deliverables and remap only the necessary navigation fields. Recheck cable coverage and marking reconciliation, then deliver PDF, PowerPoint and checklist together beside the applicable BOM and labels, as specified in `files-and-workflow.md`.

For grouping changes, compare the full cable inventory against component-pair groups: every in-scope cable appears exactly once, all compatible members of each pair are present, and any split has an explicit route/marking reason. Verify complete output/channel sets where the ICD defines them, including nonadjacent rows. Confirm the TOC section-start numbers match the actual grouping slides and that the checklist's group/route references agree. Merge these fields into the current delivered checklist by source-record identity; preserve its current layout, formulas, recorded completion, measurements, notes and signoffs instead of replacing it with an older generator's blank workbook.
