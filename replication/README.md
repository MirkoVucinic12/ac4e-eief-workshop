# Replication README

## Environment

Participant software install (Git, Python, Claude Code / Codex / Cursor):
[`SETUP.md`](../SETUP.md).

- Python 3.12 (what CI and `requirements-lock.txt` use). 3.11–3.14 are the rest of the range. Do not use 3.10 or 3.15. See [`SETUP.md`](../SETUP.md).
- Exact dependencies in `requirements-lock.txt`
- Range file `requirements.txt` is the human-editable source; regenerate the
  lock before delivery if the tree changes
- Live statistical track is Python. R (`renv.lock`) and Stata (`version` plus
  preserved ado files) are documented in `tool-lanes/research-languages.md`
  and are not required to complete this workshop

## Setup (clean clone)

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements-lock.txt
```

## Verify

This is the documented command. Keep it identical in `AGENTS.md`.

```bash
python3 -m pytest examples/card-krueger-toy/tests examples/mini-economics/tests
```

Optional printed exhibits:

```bash
python3 examples/card-krueger-toy/src/did_analysis.py
python3 examples/mini-economics/src/analysis.py
```

## Expected output

- pytest: all collected tests pass
- Card–Krueger script: group-means table and a replication note that labels the
  CSV as synthetic and refuses a causal claim
- Mini-economics script: a synthetic Phillips-curve summary

Generated output must not overwrite `examples/card-krueger-toy/data/toy_fast_food.csv`.

## Known limitations

Both bundled examples use synthetic data for teaching only. Do not interpret
them as empirical results. Passing tests do not certify identification,
precision, or causality. A qualified human owns statistical approval.
