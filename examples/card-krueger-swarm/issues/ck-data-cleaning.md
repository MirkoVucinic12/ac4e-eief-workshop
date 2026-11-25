# [CK] Check and document the Card–Krueger panel

**Label:** `ready` · **Role:** writer · **Separate copy (branch):** `ck/data-cleaning` · **Reviewer:** `data-reviewer`

## Goal

`examples/card-krueger-toy/data_notes.md` records the panel checks you ran, with
store counts that match the printed output, and the CSV files are unchanged.

## Allowed files

- `examples/card-krueger-toy/data_notes.md` (edit the "Checks run" section)
- `examples/card-krueger-toy/README.md` (edit only if a fact is wrong)
- `examples/card-krueger-toy/src/` (read only)

## Acceptance criteria (done when)

- [ ] "Checks run" lists total, NJ and PA stores, stores with both waves, and stores
      dropped, each matching the output of `did_analysis.py` and `panel_workflow.py`.
- [ ] It confirms that `state` is only `NJ`/`PA`, `wave` is only `before`/`after`,
      and `fte_employment` is a non-negative number, and quotes the command used.
- [ ] The README states the sample restriction, and the toy DiD it reports (3.0)
      equals the one printed by `did_analysis.py`.
- [ ] `git diff --stat examples/card-krueger-toy/data/` shows no changes, and the
      check command passes.

## Check command

```bash
python3 -m pytest examples/card-krueger-toy/tests examples/mini-economics/tests
```

## Not in this card

- Editing any file in `data/` or `tests/`.
- Changing or extending the estimate.
- Any claim that the synthetic panel identifies a causal effect.
