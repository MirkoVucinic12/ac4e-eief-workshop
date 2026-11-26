# Capstone rubric

Fri 15:50–16:15. Apply a rules file, a Skill, a goal, and acceptance criteria to a **non-confidential** piece of your own work. If all your data are restricted, use the Card–Krueger panel (`examples/card-krueger-toy/`).

This is a workshop completion standard, not a judgement of research quality. Pass: at least 80 points and **no critical failure**.

| Part | Points | What counts |
| --- | ---: | --- |
| `AGENTS.md` rule | 20 | At least one rule specific to your project (a folder to avoid, a file to protect, or how to check work); privacy check answered |
| Skill | 25 | Name, when to use it, numbered steps; ran once; one step fixed after the run |
| Goal | 15 | One sentence describing the finished state that you can check |
| 3 acceptance criteria | 20 | Each answerable yes or no; at least one protects data or tests |
| Check-command evidence | 20 | A command that runs on its own (Python, `do master.do`, `Rscript run_all.R`…) and its pasted output from your machine |

## Critical failures (any one fails the Capstone)

- Restricted or private data reach an agent without authorization.
- Raw data are modified.
- A secret (password, key, token) is exposed.
- The agent changes the tests or the acceptance criteria to make them pass.
- Completion is claimed without a command that ran.
- Passing checks are presented as proof of identification or a causal effect.

Points elsewhere cannot offset a critical failure.

## Card–Krueger minimum

- Rule: for example, "Never edit `data/toy_fast_food.csv`."
- Skill: `sample-restrictions-note` or your own, run once.
- Goal and criteria: from your Slot 4 card.
- Evidence: the check command output.
