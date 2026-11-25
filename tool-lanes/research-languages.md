# Research languages

> **Reference only, not on the workshop path.** The workshop runs on the Python
> Card–Krueger example, and you do not need to know Python: you direct the agent,
> it runs the code. In the capstone you may point the same steps at your own
> non-confidential Stata, R or MATLAB files. The notes below help with that.

Only Python is required in the workshop room.

Install Python (`3.12` recommended; `3.11`–`3.14` supported; avoid `3.15` where
locked binary wheels are unavailable) and the locked packages with [`SETUP.md`](../SETUP.md).
For copy-pasteable side-by-side code blocks across panel cleaning, clustered
DiD, `booktabs` tables, and MATLAB/Python Bellman solver assertions, see
[`examples/r_stata_equivalence.md`](../examples/r_stata_equivalence.md).

## Python (live)

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements-lock.txt
python3 -m pytest examples/card-krueger-toy/tests examples/mini-economics/tests
```

Pin exact versions in `requirements-lock.txt`. Edit ranges in `requirements.txt`
only when you intend to regenerate the lock.

## Stata (equivalence notes & Slot 4 Capstone target)

- Current Stata is release 19. StataNow uses `version 19.5` ([`version`](https://www.stata.com/manuals/pversion.pdf)).
- A `version` line is a reproducibility pin. Stata 19 accepts `version 18` and then interprets the do-file with Stata 18 syntax where the two differ. Keep `version 18` on a do-file that was written and checked under 18.
- A new do-file you write on Stata 19 should start with `version 19`, or `version 19.5` if you have StataNow, so a later Stata keeps today's behavior. `version` cannot make an older Stata understand newer syntax.
- Pin project ado dependencies with `adopath ++ "code/ado"` inside the repository; do not rely on an undocumented `ssc install`.
- Guard panel keys and merges with `isid store_id wave` and
  `merge m:1 chain_id using ..., assert(match master) nogen`.
- Export tables from code (`reghdfe ..., vce(cluster store_id)` and
  `esttab using "table.tex", booktabs nostar`) and flag few-cluster limits when
  policy varies across $G=2$ states.
- Record `creturn list` in batch execution logs (`stata-mp -b do ...`).
- The baseline `did_analysis.py` contrast has no weights, no variance estimator, and
  no clustering; `panel_workflow.py` adds store-clustered HC1 SEs with an explicit
  $G=2$ state-cluster warning. Name your exact estimator in the task contract.

## R (equivalence notes & Slot 4 Capstone target)

- Restore with `renv::restore()` from an `renv.lock` committed in the project.
- Guard panel keys and merges explicitly:
  `stopifnot(!anyDuplicated(df[c("store_id", "wave")]))` and
  `dplyr::left_join(..., by = "chain_id", relationship = "many-to-one")`.
- Export regression tables directly from code (`fixest::feols(..., cluster = ~store_id)`
  and `modelsummary::modelsummary(..., stars = FALSE, output = "table.tex")`) instead
  of copying numbers into `.tex` drafts by hand.
- Keep raw data out of the write path and record `sessionInfo()` next to the
  verification output.
- Do not treat a green `testthat` run as a causal claim or structural identification.

## MATLAB (equivalence notes & Slot 4 Capstone target)

- Pin the random-number generator at script entry (`rng(42, 'twister')`), use
  repo-relative paths (`addpath('code/functions')`), and record `version` / `ver`
  from `matlab -batch` verification runs.
- Assert Markov row-stochasticity (`assert(all(P(:) >= 0) && max(abs(sum(P, 2) - 1)) <= 1e-9)`)
  and finite arrays (`assert(all(isfinite(V(:))))`) before and during iteration.
- Fail explicitly when value-function or equilibrium iteration reaches `max_iter`
  unconverged (`if sup_norm >= tol, error('Bellman VFI failed to converge'); end`);
  never return the `max_iter` iterate silently.
- Verify stationary distribution residuals (`assert(norm(mu' * Q - mu', 1) < 1e-9)`)
  and upper-grid interiority (`assert(share_at_grid_top <= 0.01)`), and never treat
  solver convergence or moment fit as certifying structural identification.
- *Julia note:* Use committed `Project.toml` + `Manifest.toml` and explicit `@assert`
  solver gates when porting numerical models to Julia.

## Shared rules

- Relative paths.
- Do not modify raw data.
- Human owns identification, statistical approval, theorem proofs, and interpretation.
