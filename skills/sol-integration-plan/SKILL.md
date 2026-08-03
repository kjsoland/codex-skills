---
name: sol-integration-plan
description: Maintain, audit, and regenerate the Sol Integration Plan from its SharePoint-synced Markdown source, ICD-derived cable data, and authoritative Smartsheet schedules. Use for editing integration sequences or task status, refreshing the team-facing HTML, updating hardware receive/readiness dates, regenerating ICD cable subtasks, syncing Gates/LSC RF checkout status, or tracing a plan date or cable entry back to its source.
---

# Sol Integration Plan

Maintain the shared plan without creating a competing local baseline.

## Locate the plan

Resolve the plan directory in this order:

1. Use the SharePoint-synced path beneath the current user's profile:
   `Quantinuum LLC/Sol Hardware Project Team - Sol Project Team Channel/Integration/Integration Plan`.
2. If available, accept an AI Workspace junction such as
   `Documents/AI Workspace/integration-plan-playground/v2`.
3. If neither exists, search the user's locally synced Quantinuum/OneDrive folders for
   `Integration/Integration Plan`.
4. Stop before editing if multiple candidates exist and the SharePoint-backed source cannot be identified confidently.

Treat the SharePoint-synced directory as the source of truth. Do not package or maintain a separate working copy of the controlled plan.

## Understand the file roles

- Edit `_source/Sol_Integration_Plan_v2.md` for plan content, sequence, dates, and status.
- Treat `Sol_Integration_Plan_v2.html` as generated output; never hand-edit it.
- Treat `_generated/` as derived data and audit output.
- Use `_source/build_cable_subtasks.py` to refresh ICD-derived cable subtasks and audits.
- Use `_source/render_integration_flow_v2.py` to rebuild the team-facing HTML.
- Use `_source/sync_cable_status_smartsheet.py` for the Gates/LSC RF-status sheet.
- Use `_source/update_integration_plan_from_smartsheet.py` or
  `Update_Integration_Plan_From_Smartsheet.bat` for the full cable-status refresh.

Read [references/project-sources.md](references/project-sources.md) before changing schedule dates, rack or beam-delivery readiness, cable assignments, or Smartsheet data.

## Choose the correct workflow

### Edit plan content or sequence

1. Inspect the relevant source Markdown block and its predecessor/dependency context.
2. Edit only the source Markdown.
3. Preserve generated-section markers and table schemas used by the scripts.
4. Rebuild with `python _source/render_integration_flow_v2.py`.
5. Inspect the regenerated HTML and any affected tables or flow cards.

### Refresh ICD-derived cable subtasks

1. Confirm the local SharePoint ICD sync is current.
2. Inspect the ICD source basis and generator constants before changing mappings.
3. Run `python _source/build_cable_subtasks.py`.
4. Review cable-assignment and unmatched-item audits under `_generated/cables/`.
5. Run `python _source/render_integration_flow_v2.py`.
6. Do not silently discard unmatched cables; leave them in the audit for review.

### Pull or sync cable status

`Update_Integration_Plan_From_Smartsheet.bat` performs an end-to-end refresh. Its `ensure` step may add missing rows to the Gates/LSC Smartsheet, so run it only when the user's request authorizes that external write.

For a read-only status pull, run:

```powershell
python _source/sync_cable_status_smartsheet.py pull
python _source/build_cable_subtasks.py
python _source/render_integration_flow_v2.py
```

For an authorized full refresh, run:

```powershell
.\Update_Integration_Plan_From_Smartsheet.bat
```

Never print, save, or package `SMARTSHEET_ACCESS_TOKEN`.

## Apply plan rules

- Use authoritative schedule rows rather than dates copied from chat, screenshots, or old exports.
- Use `Receive Date` for a clear equipment delivery/ready milestone.
- Use `TBD` when no confident schedule match exists.
- Use `N/A` when a row is not a received equipment item.
- Preserve predecessor logic. Do not convert contextual arrows into hard constraints unless the plan explicitly defines them that way.
- Place generated cable subtasks at the first matching cable-install step that begins after all known endpoint equipment is installed.
- Keep cables without a valid execution point in the cable-assignment audit.
- Limit Gates/LSC RF checkout status to `G-LSC` cable rows.

## Validate

After a change:

1. Confirm the script exits successfully without a traceback.
2. Confirm `Sol_Integration_Plan_v2.html` was regenerated from the intended source.
3. Inspect every affected task, date, cable table, and flow card.
4. Check that `TBD` and `N/A` semantics remain correct.
5. Review generated audits for new unmatched or duplicate cable records.
6. Report the source files changed, schedule data's as-of date, unresolved assumptions, and whether any Smartsheet rows were created or updated.

## Required local environment

- Synced access to the Sol Project Team SharePoint folders.
- Python 3 with `openpyxl`.
- Windows PowerShell.
- Microsoft Excel desktop automation for conversion of the System Monitor `.xlsb` source.
- `SMARTSHEET_ACCESS_TOKEN` in the environment for Smartsheet cable-status operations.

If a required source or credential is missing, continue with read-only inspection when useful and state exactly what could not be refreshed.
