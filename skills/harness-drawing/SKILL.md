---
name: harness-drawing
description: Create or update professional cable harness drawings and cable assembly drawing packages. Use when Codex is asked for cable assembly drawings, harness-style system diagrams, wiring diagrams, connector pinouts, cable BOMs, flag notes, label notes, mechanical cable dimensions, twisted-pair notation, or 11x17 Quantinuum-style PDF drawing outputs.
---

# Harness Drawing

## Overview

Use this skill to create cable/harness drawing packages in the established Quantinuum cable assembly format. The expected package is usually a two-sheet PDF per cable plus optional individual Excel BOMs.

Before creating or editing a harness drawing, read `references/drawing-standard.md`.

## Workflow

1. Identify whether the request is drawing-only or changes electrical design inputs.
   - If only notes, labels, dimensions, layout, or BOM exports change, do not regenerate voltage-drop analysis workbooks.
   - Regenerate voltage/electrical analysis only when length, AWG, pair count, current/load, resistance, connector selection, or workbook content changes.
2. Use the bundled Quantinuum drawing template for new drawing packages.
   - For new drawings, load or copy `assets/quantinuum_schematic_assembly_template.tex` so sheets use the Quantinuum border, zone grid, revision block, lower notes, and title block.
   - When updating an existing project, prefer patching the existing script over hand-editing generated `.tex` or `.pdf` outputs.
   - Preserve the bundled Quantinuum title block and 11x17 landscape output unless the user asks otherwise.
3. Keep cable assembly PDFs in the established two-sheet format.
   - Sheet 1: assembly/harness view with mechanical dimensions, vertical notes, flag-note markers, and PDF BOM.
   - Sheet 2: wiring diagram with straight schematic conductors, connector pin numbers, splices, and twisted-pair symbols.
4. For BOM exports, keep the PDF BOM format unchanged unless requested.
   - When the user asks for easier ordering, generate individual cable BOM Excel files with website/order links, stock, lead time, unit cost, and known subtotal.
5. Validate visually.
   - Compile PDFs.
   - Render page previews with PyMuPDF/fitz or equivalent.
   - Inspect for note overlap, dimension overlap, illegible text, off-page content, and BOM collisions.
   - Remove temporary preview images after validation.

## Resources

- `references/drawing-standard.md`: required drawing conventions and output rules.
- `assets/quantinuum_schematic_assembly_template.tex`: primary LaTeX 11x17 Quantinuum sheet template for new drawing packages.
- `assets/harness_tikz_macros.tex`: optional TikZ snippets for flag-note markers, dimensions, and twisted-pair notation.
