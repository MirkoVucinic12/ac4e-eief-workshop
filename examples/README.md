# Examples

The workshop uses **one shared example**: the synthetic Card–Krueger minimum-wage
panel in [`card-krueger-toy/`](card-krueger-toy/). Every concept, from the first
read-only question to the planted-error check, works on this one folder.

| Path | Role | What is inside |
| --- | --- | --- |
| [`card-krueger-toy/`](card-krueger-toy/) | **The workshop example** | Data, two scripts, planted errors, and the 14-concept [workshop path](card-krueger-toy/README.md#workshop-path) |
| [`card-krueger-swarm/`](card-krueger-swarm/) | Issue cards (C10, C11, C13) | Two live cards for the lunchtime swarm, two spares |
| [`card-krueger-goals/`](card-krueger-goals/) | Goal briefs (C4, C12) | Three short briefs, each opening with a one-sentence goal |
| [`mini-economics/`](mini-economics/) | Extra, not on the workshop path | Structural and theory scripts; their checks still run |
| [`r_stata_equivalence.md`](r_stata_equivalence.md) | Reference only | Python, R, Stata and MATLAB side by side |

The check command, run from the project folder:

```bash
python3 -m pytest examples/card-krueger-toy/tests examples/mini-economics/tests
```

All data and numbers under `examples/` are **synthetic teaching material**, not
research findings.
