# Reference — Exercise 08 (C11 review, C12–C14, Capstone)

## A. Review the swarm

Merge only if: the pull request changes only the files the card allows, the check command passed, and no text claims a causal effect. Otherwise comment and move the card back to `ready`.

## B. Goal

Vague title: "Clean the CK data." Goal: "`examples/card-krueger-toy/README.md` states the source, unit, sample restriction and store counts, and the check command passes."

## C. Acceptance criteria

- [ ] `examples/card-krueger-toy/data/toy_fast_food.csv` is unchanged.
- [ ] The check command passes.
- [ ] The README states the sample restriction (balanced panel, no missing FTE).

Judge the relaunched pull request on these three only. If all three are yes, it is done, even if you would have written it differently.

## D. Verification

1. Check command: all checks pass.
2. Planted fault: the table check fails with

   ```text
   ValueError: LaTeX table drift: with_perm_closed DiD 3.15 != 2.6364 (tol=0.01)
   ```

   Diagnosis: someone typed numbers into the table by hand (DiD `3.15`, raw row count `47`).
3. Fix: the agent writes `notes/fault_drill_table.tex` with `render_latex_booktabs_table(run_robustness_suite())`; `verify_latex_table_numbers` passes on it; the check command is still green. `faults/` and `tests/` are untouched.
4. Scorecard example:

| Tested | How | Caught? |
| --- | --- | --- |
| Skill | `replication-checker` with the drifted table in view | Caught only if the Skill compares tables to code; if missed, add that step |
| Sub-agent | `data-reviewer` on `faults/unbalanced_panel.csv` | Caught: store NJ02 has no after row |
| Whole set-up | Fresh chat, fresh copy, README only | Reproduced DiD = 3.0, or note which README step was missing |

Afterwards, delete the `fault-drill` copy.

## E. Capstone

A passing Capstone shows four things: one `AGENTS.md` rule, one Skill that ran, one goal with 3 yes/no criteria, and pasted output of a check command. Any critical failure in [`docs/capstone_rubric.md`](../../docs/capstone_rubric.md) fails it, for example restricted data sent to the agent, or passing checks presented as proof of a causal effect.

Stata or R users: the check command can be `do master.do` or `Rscript run_all.R`, as long as it runs on its own and its output is pasted.
