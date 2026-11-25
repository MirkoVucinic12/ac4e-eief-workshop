# Provenance manifest

Use one row per data input, cleaning or estimation step, and output. Never edit raw input files under `data/`.

| ID | What | Path or URL | Version / hash / date | Role | Produced by | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| S1 | Synthetic teaching CSV | `examples/card-krueger-toy/data/toy_fast_food.csv` | shipped with course files; do not modify | source input | human (shipped) | Not Card and Krueger microdata |
| T1 | | | | transformation | | |
| O1 | | | | output | | |

## Code-to-output map

| Exhibit / claim in the note | Code path | Command that produced it | Human reviewed? |
| --- | --- | --- | --- |
| Toy group means | `examples/card-krueger-toy/src/did_analysis.py` | `python3 examples/card-krueger-toy/src/did_analysis.py` | |
| Toy 2x2 contrast | same | same | |

## Unchanged raw inputs

- Were any raw or source files modified? Yes / No
- If yes, stop, restore the original file, and record the path:

## Environment

- Python / R / Stata version:
- Install command (`requirements-lock.txt`, `renv.lock`, or Stata `.ado` list):
- Operating system and machine (a brief description is fine):
- Date of the recorded run:
