# Beam Delivery verification workflow

## Contents

1. Source and evidence rules
2. Verification columns
3. Common direct mappings
4. Limiting-value rules
5. Compliance and waiver states
6. Waiver content rules
7. Validation checklist

## 1. Source and evidence rules

- Treat the latest SharePoint-synced Beam Delivery requirements workbook as controlled source input.
- Perform drafting in a workspace copy. Report clearly that the SharePoint source was not modified.
- Treat `Sol BD Assembly - <port>.xlsx` as the summarized test-result record. Raw `.wcf`, `.m2_wcf`, and camera files are instrument data; do not copy or review them unless requested.
- Use the current Beam Spec Table when a Beam Delivery requirement refers to port-interface power, beam waist, polarization, PER, or another table-controlled value.
- Distinguish recorded measurements from setup values, requirements, commands, or planned ranges. A populated value is not automatically proof that a checklist step was executed.

## 2. Verification columns

| Column | Meaning | Rule |
|---|---|---|
| O | Test Procedure(s) | Identify the test workbook and precise tab/rows. Merge unique procedures when multiple ports contribute. |
| P | Compliance Statement | Use only `Compliant`, `Non-compliant`, or `Compliant with Waiver`. An unsigned waiver remains `Non-compliant`. |
| Q-V | Port verification values | Q=P45, R=P225, S=P135, T=P315, U=P90, V=P270. Record the limiting/worst-case port value. |
| W | Verification Artifact(s) | Identify the result workbook and every approved or draft waiver that covers the requirement. |
| X | Verification Summary | State method, complete population or useful range, limiting datum, failures, comparison, and caveats. Separate ports clearly. |
| Y | Verification Status | Keep `In Work` until evidence review and required dispositions are complete. |
| Z | Verified By | Leave blank until an authorized verifier signs. |

When one port fails, the overall compliance statement is `Non-compliant` even if other ports pass. When an approved port waiver resolves the only open noncompliance, use `Compliant with Waiver`.

## 3. Common direct mappings

Confirm workbook labels before using these locations; revisions may move rows.

| Requirement | Typical result evidence | Notes |
|---|---|---|
| `BRD_00108` axial waist position | `Compliance` axial-error u/v rows | Convert mm to um when comparing with +/-500 um. Use maximum absolute error while retaining its sign and collimator/axis. |
| `BRD_00112` 1762-nm waist radius | `Compliance` waist-radius u/v rows | Compare all axes with the Beam Spec range. For a symmetric waiver, retain the target and expand tolerance to the largest measured deviation. |
| `BRD_00116` pencil-beam M-squared | `Compliance` M-squared u/v rows | Use the maximum M-squared and list every value above the limit. |
| `BRD_00119` individual X/Y adjustment | `Lateral Range` individual negative/positive X/Y rows | Use the smallest recorded directional range. Confirm these are executed measurements when the checklist is incomplete. |
| `BRD_00121` global X/Y/Z adjustment | `Lateral Range` global negative/positive rows | Use the smallest axis range. Confirm execution provenance. |
| `BRD_00129` output power | `Data Input` laser-on/off/fiber power plus `Compliance` transmission | Use minimum transmission. If scaling to Beam Spec operating power, state the linear-scaling assumption and calculate predicted interface power. |
| `BRD_00135` 1762-nm polarization | `Data Input` ion-plane polarization table | Report state for every beam plus worst ellipticity and azimuth deviation. |
| `BRD_00142` PER | `Data Input` ion-plane polarization/PER table | Use the minimum reported PER or conservative lower bound. |

Output-angle, nominal-position, diagnostic-camera, pinhole, motor-model, and encoder fields may support inspections or analyses, but do not use them alone to close an inspection requirement unless the verification approach permits it.

## 4. Limiting-value rules

- Upper limit: choose the maximum result.
- Lower limit: choose the minimum result.
- Symmetric +/- limit: choose the result with maximum absolute deviation and retain its sign.
- Bounded range: report the limiting low or high result and summarize both extrema.
- Multiple axes: evaluate each axis separately before selecting the limiting datum.
- Inequality recorded as a lower bound, such as `>30 dB`: preserve the inequality; do not invent a numeric value.
- Include collimator, axis, units, and port in the verification value.
- List every failed member in the summary, not only the worst case.

## 5. Compliance and waiver states

| Evidence state | Compliance Statement | Status |
|---|---|---|
| Recorded values pass, review pending | `Compliant` | `In Work` |
| Recorded values fail, no waiver | `Non-compliant` | `In Work` |
| Waiver drafted or under review | `Non-compliant` | `In Work` |
| Waiver approved and all other evidence accepted | `Compliant with Waiver` | Set according to authorized review state |

Never treat waiver creation as approval. Never fill `Verified By` from an author name, workbook operator, or presumed responsible engineer.

## 6. Waiver content rules

- Use one waiver per port and include every noncompliant requirement for that port.
- Use `WAIVER_TBD` until an official number is assigned.
- In Section 4, show exact requirement ID and current requirement text.
- In proposed requirement text, show only the port-specific acceptance redline needed for the as-tested hardware:
  - existing value: red strikethrough;
  - proposed acceptance value: red underline.
- Set the proposed value to the minimum change that includes the limiting measured result unless engineering provides a different approved value.
- State explicitly that the redline is port/build specific and does not revise the controlled requirement for other ports or future builds.
- Put affected hardware, evidence record, and system/integration interfaces in Section 8. Do not repeat requirements there. Mark unused rows `N/A`.
- Do not fabricate engineering rationale. Label unprovided rationale or impact conclusions as pending responsible-engineer review.
- Add the draft waiver to column W for every requirement it covers and mention the proposed redline in each summary.

## 7. Validation checklist

1. Confirm the requirements workbook is a workspace copy.
2. Confirm requirement IDs and port applicability.
3. Recalculate extrema independently from the summary cells.
4. Confirm only intended verification cells changed.
5. Confirm noncompliant rows remain `Non-compliant / In Work` while a waiver is unsigned.
6. Confirm `Verified By` remains blank unless explicitly authorized.
7. Confirm every waiver-covered row references the same port waiver.
8. Confirm Section 4 contains all noncompliant requirements and Section 8 contains none.
9. Confirm redline deletion is red strikethrough and insertion is red underline.
10. Confirm `word/vbaProject.bin` is present and unchanged in the generated DOCM.
11. Confirm controlled SharePoint inputs are unchanged.
