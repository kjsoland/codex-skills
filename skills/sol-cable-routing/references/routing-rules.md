# Sol cable routing rules

## Rack families and route-row naming

- CE racks, BD/DET Motor Rack, Chiller Racks (`CR1`/`CR2`), and L2 Compute Rack are Tripp Lite SR48UB-family racks.
- For Tripp Lite rack families, route rows should use `Top ... Rack to Waterfall entry`, not `Top ... Rack to Cable Gantry`.
- The base Tripp Lite top-of-rack-to-waterfall-entry value is `20.5 in`.
- If a route row formula includes additional rack/U offset, preserve that extra term and replace only the `19.8` base with `20.5`; for example `=19.8+6*$B$2` becomes `=20.5+6*$B$2`.
- Use the `Go over waterfall...` value in the selected route block. In v4p1, standard waterfall crossings are `9.5 in` and flat-waterfall crossings are `2 in`.
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

## v4p2 rack mobility allocations

- Treat rack mobility as a route-file cable allowance, distinct from purchase-excess slack storage. Read it from the selected route row and include it in worksheet `Total`; do not add it off-sheet.
- Use these uniform per-rack values in v4p2: CE1 `0.15 in`, CE2 `4.875 in`, CE3 `3.15 in`, CE4 `4.875 in`, CE5 `11.8 in`, CE6 `1.9 in`, BD/DET Motor Rack `5.65 in`, CR1 `0 in`, CR2 `1.4 in`, L2 Compute Rack `1.9 in`, and T-Rack 1-4 `24 in` each.
- The normal basis is the v4p1 minimum route margin minus a `1 in` reserve.
- CE2 and CE4 share the limiting CE4-to-CE2 cable. Split its available `9.75 in` equally: `4.875 in` at each rack.
- Preserve the T-rack `24 in` exception wherever possible. T-Rack 2 remains `24 in`; its limiting shared cable constrains CE6 to `1.9 in` so that route retains `1 in`.
- CR1 remains `0 in` because its v4p1 minimum margin is only `0.1 in`; no positive allocation can retain the full `1 in` reserve.
- Keep Menlo, 370/493 nm Bookshelf, Gates, QPA, and other fixed/non-rack endpoint mobility rows at `0` unless a route-specific instruction says otherwise. Preserve the three pre-existing `36 in` Antenna Driver endpoint rows.
- Ground-strap route blocks remain excluded from rack minimum-margin calculations. Preserve the generic T-rack ground-row mobility at `24 in`.

## Cable identification labels

- Apply a direction-specific cable-identification label at each cable end.
- Put `FROM SIDE [DESIGNATOR]    ICD: [ACRONYM]` on the From-end label's top row and `TO SIDE [DESIGNATOR]    ICD: [ACRONYM]` on the To-end label's top row. The acronym comes from the current Integration Plan To/From ICD acronym list.
- Use only the governing ICD's `Designator` field. If that field is absent or the row value is blank, leave the designator area blank; do not substitute a description, route-block title, or another identifier.
- Include the full From and To rack/device/port definitions in the same order on both end labels.

## Tape-marker interpretation

- Apply exactly two tape markers per routed cable: one at the source waterfall entry and one at the destination waterfall exit.
- Do not apply tape at rack-top, rack-exit, enclosure-entry, table, connector, or other strain-relief datums.
- The source tape datum is the end of the route row immediately before the first `Go over waterfall...` row. In Tripp Lite rack examples this is normally the highlighted `Top ... Rack to Waterfall entry` row.
- Calculate the source-entry tape from the From connector by summing the preceding route rows through that highlighted entry row and adding the source-side slack allocation.
- The destination tape datum is the end of the last `Go over waterfall...` row. Calculate it backward from the To connector by summing the route rows after that highlighted crossing row and adding any destination-side slack allocation.
- Use each cable connector as its own `0 in` measurement datum: measure Tape 1 forward from the From end and measure Tape 2 backward from the To end.
- Training diagrams should show every source-side route step from the cable beginning through the highlighted Tape 1 row, followed by the total From-end-to-Tape-1 measurement.
- Show every destination-side route step after the highlighted Tape 2 row through the cable end, followed by the total Tape-2-to-To-end measurement; note that this is measured backward from the To end.
- Summarize the route between Tape 1 and Tape 2 without providing a tape-to-tape distance.
- Do not place tape at the source waterfall exit or destination waterfall entry. The tape-to-tape span includes the first waterfall crossing, all route rows between waterfalls, and the destination waterfall crossing.
- Continue to allocate slack only at approved rack interiors: split between two slack-capable racks, keep CE/Chiller/L2/Motor-to-T/Menlo slack entirely at the slack-capable rack end, and keep rack-to-QPA/Gates slack at the rack end. Slack changes the connector-to-waterfall measurement but does not create an additional tape point.
- In graphics, place slack only at the physical cable ends: source slack first and rack-to-rack destination slack last.
- Negative offset rows are bookkeeping only; fold them into the applicable slack/storage allocation and do not create tape points for them.

## Audit rule

- The worksheet `Total` is authoritative.
- Do not apply post-processing subtractions or additions for waterfalls, rack-frame rows, QPA laterals, or endpoint allowances once those rows are present in the route block.
- Ground cables follow their route-file rows; do not apply off-sheet waterfall post-processing. Generic CE/CR and L2 ground rows still use the Tripp Lite naming/value rule when those rack families are present.
- For v4p2, calculate remaining route margin as `Actual - Total` after the route-file mobility rows are included. RED is negative, BLUE is non-negative but below the `1 in` reserve, and PASS is at least `1 in`.
- For the rack table, exclude ground straps and show the v4p1 minimum margin used as the allocation basis, the v4p2 assigned rack mobility, and the recalculated v4p2 minimum remaining margin. Ground straps remain included in the overall route-length audit and ICD traceback.
