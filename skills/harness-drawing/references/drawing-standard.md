# Harness Drawing Standard

Use these conventions for cable assembly drawings unless the user explicitly overrides them.

## Drawing Package

- Use 11x17 landscape PDF sheets with the bundled Quantinuum drawing template/title block.
- Create one PDF per cable assembly.
- Use two sheets per cable:
  - `SH1`: assembly view in harness-diagram style plus complete PDF BOM.
  - `SH2`: wiring diagram / schematic view.
- Use a separate system diagram PDF only when the user asks for a system-level view.
- Save/update the generating script with the drawings.
- When the assembly part number has a dash suffix such as `20009097-101`, use the base number without the dash suffix as the drawing number unless the user specifies a different drawing number. In that example, drawing number `20009097`, part number `20009097-101`.
- Name generated drawing files with the drawing number first, then an underscore, then the title with spaces replaced by underscores. Example: `20009097_SPAD_Cable_1_Assembly_Drawing.pdf`.

## Bundled LaTeX Template

- Use `assets/quantinuum_schematic_assembly_template.tex` as the default sheet template for new drawing generators.
- Load the template after LaTeX packages such as `tikz`, `xcolor`, and `helvet`.
- Start each sheet with `\quantinuumsheet{title}{drawing_no}{rev}{size}{sheet}{project}{engineer}{part_number}{drawing_type}`.
- Put drawing content inside `\begin{quantinuumcontent}` and `\end{quantinuumcontent}`.
- Set optional revision row values before calling `\quantinuumsheet` when needed:

```tex
\renewcommand{\qtrevdescription}{Initial release}
\renewcommand{\qtrevdate}{2026-07-07}
\renewcommand{\qtrevname}{AB}
```

## Sheet 1 Assembly View

- Draw the cable as a smooth harness diagram, not a block diagram.
- Use black harness lines with small connector blocks.
- Keep the assembly graphic centered horizontally in the drawing field and vertically balanced between the notes and the BOM.
- Move the graphic down when notes grow. Do not let notes collide with dimensions or harness geometry.
- Keep connector part numbers out of the graphic; show reference designators in the graphic and detailed part numbers in the BOM.
- Add connector or component pictures near their components only when they help assembly or identification and do not crowd the drawing.

## Mechanical Dimensions

- Place mechanical dimensions above the harness graphic.
- Dimension cable length connector-face to connector-face unless the user specifies another datum.
- Use the outward/mating connector faces as dimension datums for end-to-end dimensions. Do not dimension to the wire-exit/backside edge unless explicitly requested.
- Put tolerance directly in the dimension callout, for example `31 ft +/- 1 in`.
- Add branch/Y dimensions when specified, for example `8 in TYP +/- 1 in`.
- Make the drawn proportions communicate the dimension intent. Example: an 8 in Y branch on a 2 ft cable should look about one-third of the overall length.

## Notes And Flag Notes

- Put drawing notes in the upper-left corner.
- Notes must be one vertical, left-aligned stack. Do not expand notes horizontally into side-by-side columns.
- Continue note numbering for flag notes.
- For flag notes, put the full note text only in the notes stack.
- On the graphic, place only a small square-boxed note number at the approximate location.
- Do not use leader arrows for flag notes unless the user specifically requests arrows.
- Preserve user-provided label text and line breaks. Label flag notes should show the label rows exactly as intended, for example:

```text
[3] Create From End label:
SPAD_Power_Cable_1 (From End)
From: Motor Rack, M15, 9V_Out_5V_Out
To: QPA, JUNCTION_BOX, SPAD_Power
```

- If the user gives exact spelling, preserve it, even if it contains a typo such as `Create lable:`.

## Sheet 2 Wiring Diagram

- Use straight schematic conductors and standard electrical drafting style.
- Keep lines horizontal/vertical where possible.
- Do not place net names directly on top of conductors. Put net names in a clear label column beside the connector, above/below the wire with visible clearance, or in a wire-list/table if space is tight.
- Put connector pin numbers inside connector bodies.
- Show connector terminals in the order useful for assembly.
- Show local-sense jumpers or other terminal jumpers explicitly when relevant.
- Show splice IDs and net-level joining clearly.
- Show twisted power/return pairs with a compact TP marker on the relevant pair. A vertical marker with two dots and a `TP#` label is acceptable unless a project-specific symbol is required.

## BOM Rules

- The PDF BOM on `SH1` should use reference designators to call out parts.
- Include manufacturer, part number/material, quantity, distributor/PN, unit cost, extended cost, and notes when known.
- Keep PDF BOMs compact and assembly-focused.
- When asked for individual Excel BOMs, create one workbook per cable with:
  - Reference designator
  - Manufacturer
  - Part number/material
  - Description
  - Quantity
  - Distributor and distributor PN
  - Unit USD and extended USD
  - Stock/availability
  - Lead time/status
  - Clickable order/source website
  - Date checked
  - Notes
- Add formulas for known subtotal and leave TBD items as TBD.

## Validation Checklist

- PDF compiles without LaTeX errors.
- Sheet 1 notes are vertical and left aligned.
- Flag-note markers are only boxed numbers on the graphic.
- Mechanical dimensions sit above the graphic and include tolerances.
- Assembly graphic does not overlap notes, BOM, title block, or border zones.
- Sheet 2 wiring lines are readable and not kinked unnecessarily.
- BOM rows fit and remain legible.
- Excel BOM hyperlinks are clickable.
- Voltage-drop workbook timestamp is unchanged for drawing-only changes.
