# [CK] Plot NJ and PA mean employment before and after

**Label:** `ready` · **Role:** writer · **Separate copy (branch):** `ck/parallel-trends-figure` · **Reviewer:** `pr-reviewer`

## Goal

`examples/card-krueger-goals/figures/parallel_trends.png` shows NJ and PA mean FTE
employment in both waves, and a script in the same folder recreates it.

Full brief: [`../../card-krueger-goals/goals/ck-parallel-trends-figure.md`](../../card-krueger-goals/goals/ck-parallel-trends-figure.md).

## Allowed files

- `examples/card-krueger-goals/figures/make_figure.py` (create)
- `examples/card-krueger-goals/figures/parallel_trends.png` (created by the script)
- `examples/card-krueger-goals/README.md` (add a short "Figure" section)

Read `examples/card-krueger-toy/data/toy_fast_food.csv`; do not edit anything in
`examples/card-krueger-toy/`. The card needs no other card: it reads the raw
synthetic panel directly. `matplotlib` is already in `requirements.txt`.

## Acceptance criteria (done when)

- [ ] `python3 examples/card-krueger-goals/figures/make_figure.py` runs from the
      project folder and creates `parallel_trends.png`.
- [ ] The figure has two labelled lines (NJ, PA) over two points (before, after),
      and its title or subtitle says "synthetic teaching data".
- [ ] The four plotted means equal the group means printed by `did_analysis.py`.
- [ ] The README section says that two waves cannot test parallel trends, and the
      check command passes.

## Check command

```bash
python3 examples/card-krueger-goals/figures/make_figure.py
python3 -m pytest examples/card-krueger-toy/tests examples/mini-economics/tests
```

## Not in this card

- Editing any file in `examples/card-krueger-toy/`.
- Any claim that the figure shows a causal effect.
