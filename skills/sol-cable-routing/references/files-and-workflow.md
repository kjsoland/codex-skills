# Files and workflow

## Source files

Primary route workbook:

`C:\Users\Kyle.Solander\Quantinuum LLC\Sol Hardware Project Team - Sol Project Team Channel\Systems\ICDs\Sol Floor Plan ICD\Interconnect Routing\CE Cable Length Estimates_v4p2.xlsx`

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

Generation scripts in the work area:

- `Source\build_training_slides.py`: regenerates slide images, exact route-block screenshots, length audit, and ICD traceback CSV/text.
- `Source\build_training_deck.ps1`: rebuilds the PowerPoint/PDF from generated slide images.
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
3. Use `openpyxl` for straightforward label/value/formula edits.
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

For v4p2 rack-mobility updates, also verify:

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
- standard `Go over waterfall` rows are `9.5`, while v4p2 flat-waterfall rows are `2`.

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
- non-rack endpoints retain their route-specific treatment rather than receiving an invented rack exit.

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
