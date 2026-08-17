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

## Cable identification labels

- Apply a direction-specific cable-identification label at each cable end.
- Put `FROM: [DESIGNATOR]    ICD: [ACRONYM]` on the From-end label's top row and `TO: [DESIGNATOR]    ICD: [ACRONYM]` on the To-end label's top row. The acronym comes from the current Integration Plan To/From ICD acronym list.
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
- For the rack mobility screen, exclude ground straps, then identify each rack's minimum remaining route margin as `Actual - Total`. Compare that limiting margin with the 24 in target one rack at a time; do not imply that mobility can be restored simultaneously at both ends of the same cable. Ground straps remain included in the overall route-length audit and ICD traceback.
