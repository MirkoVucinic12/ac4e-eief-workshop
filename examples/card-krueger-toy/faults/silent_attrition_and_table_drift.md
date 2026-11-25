# Silent attrition and LaTeX table drift (planted)

Two common research-assistant mistakes paired with `examples/card-krueger-toy/src/panel_workflow.py`:

## Trap 1: Silent `dropna()` sample loss

A naive cleaning script calls `df.dropna()` on `data/messy_fast_food_extract.csv`,
dropping `47` raw store-wave rows to `36` balanced open rows without recording:

1. How many rows exited because of interview status (`refused`, `temp_closed`, `perm_closed`).
2. How many open interviews had item non-response (`pt_workers` missing in `NJ13` wave 2).
3. How many stores lost balance once incomplete second-wave rows were dropped.
4. Whether permanently closed stores (`NJ11`, `PA09`) belong in the estimand at `FTE = 0.0`.

Why this fails verification:

- Replication packages (such as the AEA format) require step-by-step sample counts
  (`raw_rows -> after_status_filter -> after_missing_filter -> balanced_panel_rows`).
- Treating permanent closures as missing at random changes the economic estimand.

## Trap 2: Manuscript `.tex` transcription drift (`drifted_table.tex`)

An assistant copies estimates into `faults/drifted_table.tex` by hand, changing the
column (3) DiD coefficient from `2.64` to `3.15` and reporting `47` raw rows instead of
`40` balanced observations.

Why this fails verification:

- `verify_latex_table_numbers()` compares every `booktabs` cell against `run_robustness_suite()`
  and raises `ValueError("LaTeX table drift...")` when any estimate, standard error,
  observation count, store count, or synthetic/$G=2$ caveat drifts.
