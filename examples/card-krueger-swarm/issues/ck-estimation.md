# [CK] Add two robustness versions of the DiD (spare card)

**Label:** `ready` · **Role:** writer · **Separate copy (branch):** `ck/estimation` · **Reviewer:** `data-reviewer`

Spare card: do not run it live. Start it only after `ck-data-cleaning` is `done`.

## Goal

Running `examples/card-krueger-toy/src/did_analysis.py` prints the main estimate
and two labelled robustness versions, each with its sample count.

Full brief: [`../../card-krueger-goals/goals/ck-robustness-checks.md`](../../card-krueger-goals/goals/ck-robustness-checks.md).

## Allowed files

- `examples/card-krueger-toy/src/did_analysis.py` (extend)
- `examples/card-krueger-toy/README.md` (describe the two versions)
- `examples/card-krueger-toy/tests/test_did_analysis.py` (add new checks only; never change existing ones)

## Acceptance criteria (done when)

- [ ] The script prints three labelled panels: main, trim top 2% of FTE, and
      stores with positive employment in both waves.
- [ ] Each panel shows the NJ and PA means before and after, the DiD, the sample
      count and the words "synthetic teaching data".
- [ ] The main panel still prints a toy DiD of 3.0.
- [ ] `git diff --stat examples/card-krueger-toy/data/` shows no changes, and the
      check command passes.

## Check command

```bash
python3 examples/card-krueger-toy/src/did_analysis.py
python3 -m pytest examples/card-krueger-toy/tests examples/mini-economics/tests
```

## Not in this card

- Editing any file in `data/`.
- Any claim that a robustness version is more credible without an economic reason.
