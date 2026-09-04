# Sol cable routing rules

## Rack families and route-row naming

- CE racks, BD/DET Motor Rack, Chiller Racks (`CR1`/`CR2`), and L2 Compute Rack are Tripp Lite SR48UB-family racks.
- For Tripp Lite rack families, route rows should use `Top ... Rack to Waterfall entry`, not `Top ... Rack to Cable Gantry`.
- The base Tripp Lite top-of-rack-to-waterfall-entry value is `20.5 in`.
- If a route row formula includes additional rack/U offset, preserve that extra term and replace only the `19.8` base with `20.5`; for example `=19.8+6*$B$2` becomes `=20.5+6*$B$2`.
- Use the `Go over waterfall...` value in the selected route block. In the current v4p3 workbook, standard waterfall crossings are `9.5 in` and flat-waterfall crossings are `2 in`.
- CE rack ends also use `Rack Frame Thickness = 2 in` where present in the workbook.
- T-racks use top interface panels. Do not add T-rack frame-thickness rows, and do not apply the Tripp Lite 20.5-in rule to T-rack, Menlo, 370 bookshelf, Gates enclosure, or other non-Tripp-Lite rows unless the user explicitly asks.

## QPA and Gates endpoint rules

- QPA destination routes include `Cable Gantry Edge Lateral to QPA Feedthrough = 6 in` where applicable.
- QPA endpoints get no purchase-excess storage; strain relieve at the top/enclosure/table datum described by the route block.
- Gates endpoints get no purchase-excess storage; strain relieve at the enclosure entry where applicable.
- Gates rack mobility rows can be `0`; do not invent a rack-top service loop.

## Slack cable allocation

- Calculate route slack as `Actual - Total`.
- Do not modify `Actual` unless the user explicitly instructs it.
- Store slack only inside approved rack interiors.
- CE racks, Chiller Racks, and L2 Compute Rack are treated the same as slack-capable rack interiors; the BD/DET Motor Rack is also slack-capable.
- T-racks and Menlo / 1762 Rack cannot manage or store cable slack.
- Routes from a slack-capable CE/Chiller/L2/Motor rack to a T-rack or Menlo: store 100% of the slack inside the slack-capable rack and 0% at the T-rack or Menlo endpoint.
- Routes between two slack-capable racks: split slack equally between source and destination rack interiors. In route-order graphics, draw the source half as the first segment at the cable beginning and the destination half as the last segment at the cable end.
- Rack-to-QPA routes: all slack stays in the rack end; no slack in QPA. Draw the slack as the first route-bar segment at the source-rack cable beginning.
- Rack-to-Gates routes: all slack stays in the source rack; no slack in Gates. Draw the slack as the first route-bar segment at the source-rack cable beginning.
- If neither cable end is approved for slack storage, stop and obtain a route-specific disposition; do not create an unapproved loop.
- Negative offset rows are bookkeeping; do not show them as physical tape spans. If the graphic omits a negative offset, fold its effect into the rack-storage/slack bucket so tape marks still match worksheet math.

## Current v4p3 rack mobility allocations

- Treat rack mobility as a route-file cable allowance, distinct from purchase-excess slack storage. Read it from the selected route row and include it in worksheet `Total`; do not add it off-sheet.
- Use these uniform whole-inch values in v4p3: CE1 `0 in`, CE2 `5 in`, CE3 `3 in`, CE4 `5 in`, CE5 `12 in`, CE6 `2 in`, BD/DET Motor Rack `6 in`, CR1 `0 in`, CR2 `1 in`, L2 Compute Rack `2 in`, and T-Rack 1-4 `24 in` each.
- Derive the design value from the v4p1 minimum route margin minus a `1 in` reserve, then round to the nearest inch. Zero mobility is allowed.
- CE2 and CE4 share the limiting CE4-to-CE2 cable. Their unrounded values are `4.875 in` each; use `5 in` at each rack after rounding.
- Preserve the T-rack `24 in` exception. T-Rack 2 remains `24 in`; use the rounded `2 in` value at CE6 on their limiting shared route.
- CR1 remains `0 in`.
- Keep Menlo, 370/493 nm Bookshelf, Gates, QPA, and other fixed/non-rack endpoint mobility rows at `0` unless a route-specific instruction says otherwise. Preserve the three pre-existing `36 in` Antenna Driver endpoint rows.
- Ground-strap route blocks remain excluded from rack minimum-margin calculations. Preserve the generic T-rack ground-row mobility at `24 in`.

## Cooling ICD v2 route lengths

- Use `Sol_Cooling_ICD_v2.xlsx`, `Water Tubes`, as the current source for cooling-route Actual lengths.
- Relative to v1p2, update TR1 from `354` to `394 in`, TR3 from `394` to `433 in`, and Menlo from `433` to `354 in`; the other nine represented cooling route lengths are unchanged.
- Preserve the later user-added route-file allowances carried into v4p3: Gates Actual is `552 in` versus the `512 in` ICD value, and P135 Actual is `512 in` versus the `472 in` ICD value.
- Preserve the saved Cooling route-detail edits on the TR1/TR2/TR3 and Menlo blocks. The revised Menlo block ends at `Cooling_ICD_CR1!A85`; its Total is `306.55 in`, Actual is `354 in`, and remaining margin is `47.45 in`.
- Do not run a blind ICD-to-route synchronization over those two allowances. Use the current project helper, which validates all 12 ICD rows while retaining the Gates and P135 route-file values.

## Current TTL route edits

- Preserve the saved `CoreControlICD_TTL_Cables` revisions for the CE6-to-TR2 and CE6-to-Menlo blocks.
- CE6-to-TR2 ends at `A135` with Total `272 in`, Actual `314 in`, and margin `42 in`.
- CE6-to-Menlo ends at `A155` with Total `345.5 in`, Actual `394 in`, and margin `48.5 in`.

## Cable identification labels

- Apply a direction-specific cable-identification label at each cable end.
- Put `FROM SIDE [DESIGNATOR]    ICD: [ACRONYM]` on the From-end label's top row and `TO SIDE [DESIGNATOR]    ICD: [ACRONYM]` on the To-end label's top row. The acronym comes from the current Integration Plan To/From ICD acronym list.
- Use only the governing ICD's `Designator` field. If that field is absent or the row value is blank, leave the designator area blank; do not substitute a description, route-block title, or another identifier.
- Include the full From and To rack/device/port definitions in the same order on both end labels.

## Tape-marker interpretation

- For new rack-to-rack route-marking slides, use four physical marks per cable: rack exit and gantry entry at the source rack, plus gantry entry and rack exit at the destination rack. Match the presentation used by training Slides 5-6.
- Use each cable connector as its own `0 in` datum. Measure both source-end marks forward from the source connector and both destination-end marks backward from the destination connector.
- The rack-exit mark ends the rack-side route. Calculate it from the local connector using the applicable internal-rack route, rack-frame row, and purchase-slack allocation. Do not include the rack mobility allowance in the rack-exit distance.
- The gantry-entry mark equals the rack-exit distance plus the exit-to-gantry route and the local rack mobility allowance. When the route file uses waterfall wording, the gantry-entry boundary is the end of the applicable `Top ... Rack to Waterfall entry` row.
- Keep rack mobility between the rack-exit and gantry-entry marks so the marked span is the base exit-to-gantry route plus mobility.
- Reconcile the complete cable as source connector-to-gantry entry + gantry-to-gantry route + destination gantry entry-to-connector = route-file `Actual`.
- Do not add separate marks at waterfall crossings, rack tops, or connectors. Slack and mobility affect the four connector-referenced distances but do not create additional tape points.
- Continue to allocate slack only at approved rack interiors: split between two slack-capable racks, keep CE/Chiller/L2/Motor-to-T/Menlo slack entirely at the slack-capable rack end, and keep rack-to-QPA/Gates slack at the rack end.
- In graphics, place slack only at the physical cable ends: source slack first and rack-to-rack destination slack last.
- Routes between one rack and one fixed/non-rack endpoint use three physical marks: one route-boundary mark at the fixed endpoint and rack-exit plus gantry-entry marks at the rack end.
- Do not invent a rack exit or rack interior at QPA, Gates, Dewar, 370 Bookshelf, or another fixed/non-rack endpoint. Calculate the two rack-end marks with the same internal-route, exit-to-gantry, mobility, and approved slack-storage rules used for rack-to-rack routes.
- Negative offset rows are bookkeeping only; fold them into the applicable slack/storage allocation and do not create tape points for them.

## Network media-specific Actual lengths

- For Network and Comm ICD routes, use the purchased `Actual length` in column N for the route-block `Actual`; do not substitute the calculated `Length (in)` column.
- Convert meters to inches with `meters / 0.0254` and feet to inches with `feet * 12`; store route Actual values to three decimal places where needed.
- If Fiber and Copper share route geometry but column N specifies different purchased lengths, keep separate adjacent `- Fiber` and `- Copper` route blocks. Their detail rows and Total remain the same, while Actual, slack, and tape points are media-specific.
- A copied Actual cell must compare against its own block Total in both the slack equation and conditional formatting.
- When no route block exists for a populated ICD row, report it as missing route geometry. Do not map it to a superficially similar block or invent lengths without direction.

## Audit rule

- The worksheet `Total` is authoritative.
- Do not apply post-processing subtractions or additions for waterfalls, rack-frame rows, QPA laterals, or endpoint allowances once those rows are present in the route block.
- Ground cables follow their route-file rows; do not apply off-sheet waterfall post-processing. Generic CE/CR and L2 ground rows still use the Tripp Lite naming/value rule when those rack families are present.
- For v4p3, calculate remaining route margin as `Actual - Total` after the route-file mobility rows are included. RED is negative, BLUE is non-negative but below the `1 in` reserve, and PASS is at least `1 in`.
- Whole-inch rounding can reduce a previously exact `1 in` reserve below `1 in`; retain those results as BLUE rather than adjusting the rounded mobility off-sheet.
- For the rack table, exclude ground straps and show the v4p1 minimum margin used as the allocation basis, the v4p3 assigned rack mobility, and the recalculated v4p3 minimum remaining margin. Ground straps remain included in the overall route-length audit and ICD traceback.
