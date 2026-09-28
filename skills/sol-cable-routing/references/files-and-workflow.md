# Files and workflow

## Cable-kit procedure delivery

Default delivery root for cable-kit routing procedures:

`C:\Users\Kyle.Solander\Quantinuum LLC\Sol Hardware Project Team - Sol Project Team Channel\BOMs\Sol Computer\System Interconnect`

Locate the applicable cable-kit folder under this root using its existing BOM and labels. Deliver the procedure PDF, PowerPoint, and installation checklist together there. Retain generation scripts, source snapshots, slide images, and build audits in the AI Workspace. Older procedure outputs in ICD folders or the workspace do not override this destination rule; an explicit user destination does.

BD Beamplate EICD destination:

`C:\Users\Kyle.Solander\Quantinuum LLC\Sol Hardware Project Team - Sol Project Team Channel\BOMs\Sol Computer\System Interconnect\BD Beamplate Cable Kit`

For the BD-E v7 package, deliver `BD_Beamplate_EICD_Cable_Routing_Procedure_v7_Draft.pdf`, the corresponding `.pptx`, and `BD_Beamplate_EICD_v7_Routing_Checklist.xlsx`. Keep the checklist beside the procedure for its relative workflow link. Verify copied file hashes and link targets, and report the BOM-folder paths to the user. Preserve existing deliverables before replacing differing files.

## Source files

Primary route workbook:

`C:\Users\Kyle.Solander\Quantinuum LLC\Sol Hardware Project Team - Sol Project Team Channel\Systems\ICDs\Sol Floor Plan ICD\Interconnect Routing\CE Cable Length Estimates_v4p3.xlsx`

Mobility allocation baseline (read-only):

`C:\Users\Kyle.Solander\Quantinuum LLC\Sol Hardware Project Team - Sol Project Team Channel\Systems\ICDs\Sol Floor Plan ICD\Interconnect Routing\CE Cable Length Estimates_v4p1.xlsx`

Current cooling-length source:

`C:\Users\Kyle.Solander\Quantinuum LLC\Sol Hardware Project Team - Sol Project Team Channel\Systems\ICDs\Cooling ICD\Sol_Cooling_ICD_v2.xlsx`

Local AI work area:

`C:\Users\Kyle.Solander\Documents\AI Workspace\Sol Cable Routing Procedure`

Current training outputs:

- `Sol_Cable_Routing_Training_Examples_Draft.pptx`
- `Sol_Cable_Routing_Training_Examples_Draft.pdf`
- `Slides\*.png`
- `Audit\current_length_audit.csv`
- `Audit\current_icd_traceback.csv`
- `Audit\current_rack_margin_audit.csv`
- `Audit\current_audit_summary.txt`
- `Audit\network_comm_column_n_vs_route_actual_v4p3.csv`

Generation scripts in the work area:

- `Source\build_training_slides.py`: regenerates slide images, exact route-block screenshots, length audit, and ICD traceback CSV/text.
- `Source\build_training_deck.ps1`: rebuilds the PowerPoint/PDF from generated slide images.
- `Source\network_comm_actual_length_audit.py`: compares Network and Comm ICD column N with the media-specific route Actual rows.
- `Source\create_v4p3_network_lengths.ps1`: creates v4p3 from v4p2 and performs the scoped Network media split.
- `Source\apply_v4p2_rack_mobility.py`: applies the approved whole-inch per-rack mobility values to v4p2 while preserving v4p1.
- `Source\update_v4p2_from_cooling_icd.py`: applies Cooling ICD v2 lengths to the 12 cooling route blocks while retaining the saved Gates `552 in` and P135 `512 in` route-file allowances.
- `README.md`: contains project-level persistent notes and current rebuild commands.

## Rebuild commands

Run from `C:\Users\Kyle.Solander\Documents\AI Workspace\Sol Cable Routing Procedure`:

```powershell
python ".\Source\build_training_slides.py"
powershell -NoProfile -ExecutionPolicy Bypass -File ".\Source\build_training_deck.ps1"
```

Use `python -m py_compile Source\build_training_slides.py` after editing the generator.

## Workbook edit pattern

1. Check for visible Excel instances:

   ```powershell
   Get-Process EXCEL -ErrorAction SilentlyContinue | Select-Object Id,MainWindowTitle,StartTime
   ```

2. Back up the workbook before editing, normally under `%TEMP%\SolCableRoutingBackups`.
3. Use `openpyxl` for straightforward label/value/formula edits. Use Excel automation for copied/inserted rows so formulas and formatting translate as Excel would.
4. Open/save with Excel COM afterward to refresh cached formula values:

   - `CalculateFullRebuild()`
   - `Save()`
   - `Close($true)`

5. Verify from a fresh copy, not an already-open workbook object.

## Verification checklist

After workbook changes, report:

- number of rows found/changed;
- number of targeted old labels remaining;
- value/formula counts for changed rows;
- current audited route-block count and non-compliant route-block count;
- regenerated output paths and timestamps.

For current v4p3 rack-mobility updates, also verify:

- all rack mobility rows use whole-inch values;
- the generated audit uses a `1 in` post-mobility reserve threshold;
- CE2 and CE4 are `5 in` each after rounding their shared `4.875 in` design values;
- T-Rack 1-4 remain `24 in`, CE6 is `2 in`, and CR1 is `0 in`;
- the procedure table shows v4p1 design-basis margin, rounded mobility, current minimum margin, and the current limiting route.

For Cooling ICD v2 synchronization, verify:

- 12 cooling route-block Actual cells are checked;
- TR1 is `394 in`, TR3 is `433 in`, and Menlo is `354 in`;
- Gates is retained at `552 in` versus the `512 in` ICD value, and P135 is retained at `512 in` versus the `472 in` ICD value;
- the revised Menlo route is `Cooling_ICD_CR1!A85` and remains PASS at `47.45 in` margin;
- current tracebacks use the shifted Menlo/Gates Actual-label cells `A85` and `A108`.

For the saved TTL route changes, verify:

- `CoreControlICD_TTL_Cables!A135` has Total `272 in`, Actual `314 in`, and margin `42 in`;
- `CoreControlICD_TTL_Cables!A155` has Total `345.5 in`, Actual `394 in`, and margin `48.5 in`.

For Tripp Lite waterfall-entry updates, useful checks include:

- no targeted `Top ... to Cable Gantry` rows remain for CE, Motor, CR, or L2 racks;
- updated rows use `Top ... to Waterfall entry`;
- flat base values are `20.5`;
- formula rows preserve added offsets, e.g. `=20.5+6*$B$2`;
- standard `Go over waterfall` rows are `9.5`, while current flat-waterfall rows are `2`.

For Network and Comm ICD column-N Actual synchronization, also verify:

- every represented populated column-N row matches its media-specific route-block `Actual` after unit conversion;
- meter values use `meters / 0.0254` inches and foot values use `feet * 12` inches, rounded to three decimals in the route file;
- a shared route block is split into adjacent `- Fiber` and `- Copper` blocks when the purchased lengths differ, with identical route geometry but separate Actual/slack calculations;
- copied formulas, styles, row dimensions, and blank separator rows match the source block;
- each Actual cell's conditional-format rules compare against that block's own Total cell;
- populated ICD rows with no route geometry are reported as `NO_ROUTE_BLOCK`; do not invent or borrow a route block merely to clear the audit;
- non-`Network_ICD` worksheets remain semantically and visually unchanged.

For rack-exit and gantry-entry marking slides, useful checks include:

- four physical marks appear per rack-to-rack route: rack exit and gantry entry at each end;
- each cable connector is a visible `0 in` datum;
- both source-end marks are measured forward from the source connector;
- both destination-end marks are measured backward from the destination connector;
- each rack-exit distance includes the local rack-side route and allocated purchase slack but excludes rack mobility;
- each gantry-entry distance adds the exit-to-gantry base route and local rack mobility to the rack-exit distance;
- rack mobility is shown between the rack-exit and gantry-entry marks;
- source gantry-entry distance + gantry-to-gantry route + destination gantry-entry distance reconciles to route-file `Actual`;
- rack-to-rack graphics split purchase slack equally, with one half at each physical cable end;
- no extra tape point is shown at a waterfall crossing, rack top, or connector;
- shared route blocks use one controlled set of marks only when that conservative treatment is explicit;
- rack-to-fixed routes use three physical marks: one route-boundary mark at the fixed endpoint and rack-exit plus gantry-entry marks at the rack end;
- fixed/non-rack endpoints such as QPA, Gates, Dewar, and 370 Bookshelf do not receive an invented rack exit;
- the 370 Bookshelf-to-L2 Fiber marks are `109.2 in` at 370BS and `192.902 / 237.902 in` for L2 rack exit / gantry entry; Copper uses `109.2 in` at 370BS and `305.5 / 350.5 in` at L2.

## ICD traceback notes

The appendix in `build_training_slides.py` is manually curated. If route edits change the non-compliant route list, compare `Audit\current_length_audit.csv` against `Audit\current_icd_traceback.csv` and update `ICD_APPENDIX_ROWS` / `ICD_APPENDIX_COUNTS` when new failures appear.

Current local ICD folders to search first:

- Core Control Signal Map ICD
- Frequency Reference ICD
- Network and Comm ICD
- QPA And Physics Package Control ICD
- System Monitor ICD
- BD Beamplate Assembly ICD
- Gates-LSC Electrical ICD
- Cooling ICD materials where present

Use local synced files before web lookup.
