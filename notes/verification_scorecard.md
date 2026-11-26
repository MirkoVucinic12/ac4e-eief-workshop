# Verification scorecard

Fill this in Fri 14:50–15:50.

## Planted fault

- Check command before: pass / fail
- Table check on `faults/drifted_table.tex`: error message:
- Diagnosis (one line):
- Fix (on the `fault-drill` copy, in `notes/fault_drill_table.tex`):
- Check command after: pass / fail
- [ ] No file in `tests/` or `faults/` changed.

## Did the set-up catch a known mistake?

| Tested | How | Caught? | What to change |
| --- | --- | --- | --- |
| Skill | Run `replication-checker` with the drifted table in view | | |
| Sub-agent | Run `data-reviewer` on `faults/unbalanced_panel.csv` | | |
| Whole set-up | Fresh chat, fresh copy: reproduce DiD = 3.0 from the README alone | | |
