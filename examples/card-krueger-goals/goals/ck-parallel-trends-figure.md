# Figure: NJ and PA mean employment before and after

**Goal:** `examples/card-krueger-goals/figures/parallel_trends.png` shows NJ and PA
mean FTE employment in both waves, and `figures/make_figure.py` recreates it.

## What to do

Write `examples/card-krueger-goals/figures/make_figure.py`. It should:

- read `examples/card-krueger-toy/data/toy_fast_food.csv` with a relative path;
- compute the four group means (NJ and PA, before and after);
- draw one line per state over the two waves, with the y-axis in FTE workers;
- add the subtitle "synthetic teaching data, not for research claims";
- save the figure as `figures/parallel_trends.png`.

Then add a short "Figure" section to `examples/card-krueger-goals/README.md` with
the run command. Say plainly that two waves show the means behind the 2x2
comparison; they cannot test parallel trends.

## Acceptance criteria (done when)

- [ ] The script runs from the project folder and creates the PNG.
- [ ] Two labelled lines (NJ, PA) over two points, with "synthetic teaching data"
      in the title or subtitle.
- [ ] The plotted means equal the group means printed by `did_analysis.py`
      (NJ 23.33 → 25.33, PA 24.00 → 23.00).
- [ ] No file in `examples/card-krueger-toy/` changed, and the check command passes.

## Check command

```bash
python3 examples/card-krueger-goals/figures/make_figure.py
python3 -m pytest examples/card-krueger-toy/tests examples/mini-economics/tests
```

Use `matplotlib`, which is already in `requirements.txt`. Add no other packages.
