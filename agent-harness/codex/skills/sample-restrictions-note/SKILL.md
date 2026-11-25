---
name: sample-restrictions-note
description: Use when asked to list every rule that drops stores or rows from the Card-Krueger panel, with the count left after each rule.
---

# Sample restrictions note

1. Read `examples/card-krueger-toy/data_notes.md` and `examples/card-krueger-toy/src/panel_workflow.py`.
2. Run `python3 examples/card-krueger-toy/src/panel_workflow.py` and keep the "Sample attrition counts" block.
3. For each rule that drops rows, write one table row: the rule in plain words, rows left, stores left.
4. Compare each count with the table in `data_notes.md`. Mark every mismatch.
5. Quote the command and its printed counts word for word under the table.
6. Write the note to `notes/sample_restrictions_ck.md`.

## Do not

- Edit anything in `examples/card-krueger-toy/` (data, code or tests).
- Say whether the restrictions are justified or causal; that is the researcher's call.
