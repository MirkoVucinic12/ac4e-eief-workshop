---
name: replication-checker
description: Use when asked to assess whether the repo can reproduce its documented outputs from a clean setup.
---

# Replication Checker

Source in this repo: `.claude/skills/replication-checker/SKILL.md` (portable copies must match). Inspect this file before you trust it. Record source path and git revision. This Skill does not request network or destructive git commands.

When invoked:

1. Read `AGENTS.md`, `replication/README.md`, `examples/card-krueger-toy/README.md`, and available tests.
2. Record the environment: Python version, install file used (`requirements-lock.txt` preferred; `requirements.txt` if the lock is absent), and working directory.
3. Identify the documented verification command. In this workshop it is:

   ```bash
   python3 -m pytest examples/card-krueger-toy/tests examples/mini-economics/tests
   ```

4. Check input immutability: source CSVs under `examples/card-krueger-toy/data/` must be unchanged; no writes to `data/raw/` or `data/private/`.
5. Check the data contract for the toy: unique `store_id`–`wave`, balanced before/after panel, NJ/PA only, no missing required fields, documented sample restriction, unweighted 2x2 mean contrast. No standard errors or causal language in outputs.
6. Check code-to-output coverage: the replication note and printed group means must map to functions in `examples/card-krueger-toy/src/did_analysis.py`.
7. Look for hardcoded absolute paths, secrets, private data, and undeclared dependencies.
8. Run the documented verification command if allowed. Paste the command and the result. Never mark green without a run or equivalent captured output.
9. Report **green / yellow / red** with evidence for each of: environment, input immutability, data contract, code-to-output, command execution.

## Rating

- **Green:** command ran and passed; inputs unchanged; no undeclared deps; outputs stay descriptive.
- **Yellow:** ran with documented gaps (missing optional lock file, skipped optional check, local-only fallback).
- **Red:** command failed, was not run, inputs were modified, secrets found, or the report claims causality from tests.

A failing command is yellow or red, never green.

## Do not

- Invent passing tests.
- Modify source data to make tests pass.
- Certify identification, causality, or statistical interpretation.
