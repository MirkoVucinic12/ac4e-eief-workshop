# Planted structural and theory errors (extra, not on the workshop path)

The workshop's planted errors are in
[`../../card-krueger-toy/faults/`](../../card-krueger-toy/faults/). These files are
kept for self-study. The automatic checks load them and confirm that each check
catches its error, so leave them unchanged.

| File | Model | Planted error | Check that catches it |
| --- | --- | --- | --- |
| `non_stochastic_transition.json` | Structural | Transition row sums to `1.05`, not `1.0` | `validate_structural_params` |
| `premature_stop_config.json` | Structural | `max_iter = 3` at `tol = 1e-8`: the solver stops before converging | `solve_consumption_saving` |
| `clipped_asset_grid.json` | Structural | `a_max = 1.2` cuts off wealth at the top of the grid | `validate_grid_interiority` |
| `unstated_outside_option_claim.md` | Theory | Claims a participation constraint is slack for all $\kappa \ge 0$ | `search_conjecture_counterexample`, `audit_proof_assumptions` |
| `citation_overclaim_structural_theory.md` | Both | Invented references, and model moments cited as US data | `literature-mapper` Skill, citation ledger |

To practise: on a separate copy (branch), feed one file to a scratch script, watch
the check fail, fix the parameter or assumption without editing `tests/`, and rerun:

```bash
python3 -m pytest examples/card-krueger-toy/tests examples/mini-economics/tests
```
