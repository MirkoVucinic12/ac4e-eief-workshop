# Planted errors (C14)

Each file here contains a **planted error**. The automatic checks load them and
confirm that each check catches its error. Never copy them over the files in
`data/`, and never leave a failing check on `main`.

| File | Planted error | Check that should catch it |
| --- | --- | --- |
| `drifted_table.tex` | Hand-copied DiD (`3.15`) and raw row count (`47`) in the LaTeX table | `verify_latex_table_numbers` (start here) |
| `unbalanced_panel.csv` | Store NJ02 has no after wave | `validate_balanced_panel` |
| `duplicate_store_wave.csv` | Two before rows for NJ01 | `validate_unique_identifiers` |
| `chain_many_to_many.csv` | A store matches more than one chain | `validate_merge_cardinality` |
| `silent_attrition_and_table_drift.md` | Rows dropped without a count, and a hand-copied table | Store counts per step + `verify_latex_table_numbers` |
| `citation_mismatch.md` | The toy DiD cited as Card and Krueger (1994) | `literature-reviewer`, citation ledger |
| `undocumented_restriction.md` | PA stores dropped without saying so | Sample restrictions in `data_notes.md` |

## Fail, diagnose, fix, rerun

On a separate copy (branch), point the code at one planted file and watch the
named check fail. Find the cause, fix it without editing `tests/`, and rerun:

```bash
python3 -m pytest examples/card-krueger-toy/tests examples/mini-economics/tests
```

Then score your set-up: did the `replication-checker` Skill and the `data-reviewer`
sub-agent catch the error or miss it? A reviewing agent must never edit `tests/`.
