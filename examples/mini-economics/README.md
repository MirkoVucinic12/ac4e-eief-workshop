# Mini-economics examples (extra, not on the workshop path)

The workshop uses only [`../card-krueger-toy/`](../card-krueger-toy/). This folder
is kept for anyone who wants a structural or theory example after the workshop.
Its checks still run inside the check command, so leave the code and files as they are.

Three small Python scripts, using only `numpy` and `pandas` and no outside data:

1. **`src/analysis.py`:** a 40-draw synthetic regression styled after a Phillips
   curve. It is a setup check, not an empirical Phillips curve.
2. **`src/structural_bellman.py`:** a consumption-saving model with two income states,
   solved by value-function iteration, with checks on discounting, the stationary
   distribution and the top of the asset grid.
3. **`src/theory_conjecture.py`:** a two-type screening model with outside options
   $\bar{u}(\theta) = \kappa \theta$, an exact counterexample search and a check on
   the assumptions of a draft proposition.

Planted errors for these scripts are in [`faults/`](faults/).

## What passing checks do and do not show

- **Structural:** the solver converges and the moment table matches the code. This
  does not establish identification or the validity of a policy counterfactual.
- **Theory:** an exact counterexample disproves a false general claim. Passing on a
  finite grid never proves a general theorem.

## Which code makes which output

| Script | Output | Function |
| --- | --- | --- |
| `analysis.py` | Regression summary | `summarize_relationship` |
| `structural_bellman.py` | Parameter and transition-row check | `validate_structural_params` |
| `structural_bellman.py` | Monotonicity and discounting check | `check_blackwell_conditions` |
| `structural_bellman.py` | Policy, stationary distribution, convergence | `solve_consumption_saving` |
| `structural_bellman.py` | Top-of-grid check (`share_at_grid_top <= 0.01`) | `validate_grid_interiority` |
| `structural_bellman.py` | Moment-to-code table | `audit_calibration_moments` |
| `theory_conjecture.py` | Optimal screening menu in 4 regimes | `solve_optimal_screening_menu` |
| `theory_conjecture.py` | Exact incentive and participation slack | `verify_ic_ir_constraints` |
| `theory_conjecture.py` | Counterexample search | `search_conjecture_counterexample` |
| `theory_conjecture.py` | Draft-proposition assumption check | `audit_proof_assumptions` |

## Run

From the project folder:

```bash
python3 examples/mini-economics/src/analysis.py
python3 examples/mini-economics/src/structural_bellman.py
python3 examples/mini-economics/src/theory_conjecture.py
python3 -m pytest examples/card-krueger-toy/tests examples/mini-economics/tests
```
