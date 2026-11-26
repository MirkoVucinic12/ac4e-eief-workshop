# Reference — Exercise 06

## A. replication-checker

Expected: the agent runs

```bash
python3 -m pytest examples/card-krueger-toy/tests examples/mini-economics/tests
```

sees all checks pass, and reports **GREEN** (or **YELLOW** if it flags something it could not check, such as a fresh install). A rating without a command and its output does not count.

## B. Your Skill

A good Skill file is short:

```text
---
name: sample-restrictions-note
description: Use when writing or checking the sample-restriction note for a panel.
---
1. Run python3 examples/card-krueger-toy/src/panel_workflow.py.
2. List every rule that drops rows, in order.
3. Give the row count after each rule.
4. Quote the command you ran.
5. Do not edit data or code.
```

Expected counts for the Card–Krueger panel: 47 raw rows → 43 after the status filter → 42 after dropping missing values → 36 rows (18 stores) in the balanced panel.

Typical fix after the first run: the agent paraphrased the counts instead of quoting them, so add "copy the counts exactly as printed".

## C. data-reviewer

- **Job:** review documentation, panel balance, missing values and NJ/PA coding.
- **Limits:** may read and search; cannot edit files or run commands.
- **Report:** a list of findings for the human to act on.

## D. Skill or sub-agent

| # | Answer | Why |
| --- | --- | --- |
| 1 | Skill | Same steps every time |
| 2 | Sub-agent | Fresh pair of eyes |
| 3 | Skill | Same format every time |
| 4 | Sub-agent | Runs while you keep working |
| 5 | Skill | Same steps every time |
| 6 | Sub-agent | Big, messy search; only the summary comes back |

Reasonable disagreement: task 2 could be a Skill if you always check coding the same way; it becomes a sub-agent when you want someone who has not seen your reasoning.
