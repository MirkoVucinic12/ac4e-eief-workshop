# R, Stata, and MATLAB Equivalence Notes

> **Reference only, not on the workshop path.** The workshop runs on the Python
> Card–Krueger example. Use these notes afterwards if you want to bring the same
> checks to your own R, Stata or MATLAB code.

The live workshop checks run in **Python 3.12** (`numpy==2.4.4`, `pandas==3.0.5`,
`pytest==9.1.1`). You do not need prior Python fluency in Slots 1–3: you manage the
assistant on the Python scripts in this repository (the project folder). In the Slot 4
Capstone, you can apply the same checks to your own non-confidential **Stata (`.do`)**,
**R (`.R`)**, or **MATLAB (`.m`)** code.

See also [`tool-lanes/research-languages.md`](../tool-lanes/research-languages.md).

---

## 1. Environment Lock and Runtime Record

| Check | Python (live workshop) | R | Stata | MATLAB |
| --- | --- | --- | --- | --- |
| Dependency / syntax pin | `requirements-lock.txt` on Python `3.12` (`3.11`–`3.14`; avoid `3.15` when binary wheels are missing) | `renv.lock` saved in a commit (a recorded snapshot in Git) and restored with `renv::restore()` | `version 19` (or `version 19.5` on StataNow; keep `version 18` on do-files written and checked under 18) | Release + toolbox check (`ver`) and `rng(42, 'twister')` at script entry |
| Local packages / path | `.venv/` (`python3 -m venv .venv`) | Project `renv/` library | `adopath ++ "code/ado"` saved with the replication package (do not rely on undocumented `ssc install`) | `addpath('code/functions')` using project-relative paths only (no personal machine paths) |
| Recorded environment | `python3 --version` + `pip freeze` | `sessionInfo()` | `creturn list` in batch verification log | `version` + `ver` recorded in `-batch` log |

Note on Stata `version`: `version #` pins command interpretation on newer Stata
releases so future versions preserve today's behavior; it cannot make an older
Stata release understand newer syntax.

---

## 2. Panel Keys, Sample Attrition Counts, and Merge Checks

These checks match `did_analysis.py` (`validate_unique_identifiers`,
`validate_merge_cardinality`) and `panel_workflow.py` (`clean_messy_extract`).

### Python

```python
validate_unique_identifiers(df)
validate_merge_cardinality(df, chains, key="chain_id", expected="many_to_one")
merged = df.merge(chains, on="chain_id", how="left")
```

### R (`base` + `dplyr`)

```r
stopifnot(!anyDuplicated(df[c("store_id", "wave")]))
stopifnot(!anyDuplicated(chains[["chain_id"]]))
merged <- dplyr::left_join(
  df,
  chains,
  by = "chain_id",
  relationship = "many-to-one"
)
```

### Stata 19

```stata
version 19
use "data/derived/clean_extract.dta", clear
isid store_id wave
merge m:1 chain_id using "data/chain_metadata.dta", assert(match master) nogen
```

**Attrition rule (all languages):** Record row counts at each sample restriction
(`raw_rows -> after_status_filter -> after_missing_filter -> balanced_panel_rows`)
instead of calling `dropna()`, `na.omit()`, or unlogged `drop if missing(...)`.

---

## 3. Store-Clustered DiD, Few-Cluster ($G=2$) Caution, and `booktabs` Tables

These scripts match `panel_workflow.py` (`estimate_panel_did`, `run_robustness_suite`,
`render_latex_booktabs_table`, `verify_latex_table_numbers`).

### Python

```bash
python3 examples/card-krueger-toy/src/panel_workflow.py
```

### R (`fixest` + `modelsummary`)

```r
m1 <- fixest::feols(
  fte_employment ~ treated + post + treated_post,
  data = panel_open,
  cluster = ~store_id
)
m2 <- fixest::feols(
  fte_employment ~ treated + post + treated_post + company_owned + baseline_starting_wage,
  data = panel_open,
  cluster = ~store_id
)
modelsummary::modelsummary(
  list("(1)" = m1, "(2)" = m2),
  stars = FALSE,
  output = "table.tex"
)
```

### Stata 19 (`reghdfe` + `esttab`)

```stata
version 19
adopath ++ "code/ado"

eststo clear
eststo m1: reghdfe fte_employment treated post treated_post, noabsorb vce(cluster store_id)
eststo m2: reghdfe fte_employment treated post treated_post company_owned baseline_starting_wage, ///
    noabsorb vce(cluster store_id)

esttab m1 m2 using "table.tex", booktabs nostar b(%9.2f) se(%9.2f) ///
    stats(N N_clust, labels("Observations" "Stores")) replace
```

**Econometric caution ($G=2$ states):** Store-level clustering (`cluster = ~store_id`
or `vce(cluster store_id)`) accounts for within-store serial correlation across
waves, not common state-level shocks across `NJ` and `PA` ($G=2$). Keep significance
stars off synthetic tables (`stars = FALSE`, `nostar`), generate `.tex` tables from
code rather than copying numbers by hand, and leave inference decisions to the
researcher.

---

## 4. Numerical Solver and Theory Checks (Python and MATLAB)

These checks match `structural_bellman.py` and `theory_conjecture.py` in
[`examples/mini-economics/`](mini-economics/).

### Python

```bash
python3 examples/mini-economics/src/structural_bellman.py
python3 examples/mini-economics/src/theory_conjecture.py
```

### MATLAB (`.m`: VFI, Markov, and grid-boundary checks)

Run non-interactively via `matlab -batch "run('code/verify_bellman.m')"` so any
failed assertion exits with a non-zero status code:

```matlab
% 1. Pin deterministic RNG and check parameter + Markov admissibility
rng(42, 'twister');
assert(isfinite(beta) && beta > 0 && beta < 1 && beta * (1 + r) < 1, ...
    'Impatience condition beta * (1 + r) < 1 violated');
assert(all(isfinite(a_grid)) && all(diff(a_grid(:)) > 0), ...
    'Asset grid must be finite and strictly increasing');
assert(all(isfinite(P(:))) && all(P(:) >= 0) && max(abs(sum(P, 2) - 1)) <= 1e-9, ...
    'Transition matrix P must be row-stochastic within 1e-9');

% 2. Value-function iteration with finite guard and hard non-convergence failure
sup_norm = inf;
for it = 1:max_iter
    [V_next, policy_idx] = bellman_step(V, beta, r, gamma, y_grid, P, a_grid);
    assert(all(isfinite(V_next(:))), 'Non-finite value array in Bellman step');
    sup_norm = max(abs(V_next(:) - V(:)));
    V = V_next;
    if sup_norm < tol
        break;
    end
end
assert(all(isfinite(V(:))), 'Converged value array must be finite');
if sup_norm >= tol
    error('Bellman VFI failed to converge');
end

% 3. Ergodic distribution invariant check (mu is (n_grid * n_states) x 1)
assert(all(isfinite(mu)) && all(mu >= 0) && abs(sum(mu) - 1) < 1e-9, ...
    'Stationary distribution mu must be a valid probability vector');
assert(norm(mu' * Q - mu', 1) < 1e-9, ...
    'Stationary distribution failed invariant residual check');

% 4. Upper asset-grid interiority gate (reshape mu to n_grid x n_states)
mu_grid = reshape(mu, numel(a_grid), numel(y_grid));
share_at_grid_top = sum(mu_grid(end, :));
assert(share_at_grid_top <= 0.01, ...
    'Asset grid upper bound binds: increase a_max before reading moments');
```

### Summary of Numerical and Theory Checks

| Check | What fails silently without it | Assertion pattern |
| --- | --- | --- |
| Stochastic transition rows | Typo in Markov matrix breaks discounting ($P \mathbf{1} \neq \mathbf{1}$) | Assert `all(P(:) >= 0)` and `max(abs(sum(P, 2) - 1)) <= 1e-9` before VFI (`validate_structural_params`). |
| Finite-value & convergence check | `NaN` comparisons pass `<` / `>` checks, or `1:max_iter` exits silently at `max_iter` | Assert `all(isfinite(V(:)))` and raise / `error('Bellman VFI failed to converge')` whenever `sup_norm >= tol` (`solve_consumption_saving`). |
| Stationary distribution residual | Indexing bug in induced transition matrix $Q$ | Assert `abs(sum(mu) - 1) < 1e-9`, `all(mu >= 0)`, and `norm(mu' * Q - mu', 1) < 1e-9`. |
| Upper-grid interiority | Truncated `a_max` clips precautionary savings and biases moments | Assert stationary mass at `a_max` satisfies `share_at_grid_top <= 0.01` (`validate_grid_interiority`). |
| Conjecture grid vs. proof | Finite grid check mistaken for universal proof, or solver noise mistaken for counterexample | Verify any grid counterexample in exact closed form (`exact_ir_high_deficit > 0`); never mark a universal theorem proved from a finite grid. |

*Julia note:* Apply the same checks with tracked `Project.toml` + `Manifest.toml`
files and `@assert` statements before returning solver structs.
