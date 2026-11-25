# Replication audit of the Card–Krueger toy example

**Goal:** `notes/replication_audit_ck.md` exists and records GREEN, YELLOW or RED
with the check-command output.

## What to do

Run the `replication-checker` Skill on `examples/card-krueger-toy/` and write the
result to `notes/replication_audit_ck.md`. Can someone starting from the README
alone reproduce the group means, the toy DiD and the passing check command?
Do not edit code or re-estimate anything.

## To-do list

1. Read `.claude/skills/replication-checker/SKILL.md` and follow its steps.
2. Run `python3 examples/card-krueger-toy/src/did_analysis.py` and compare its
   output with the numbers in the README.
3. Run the check command and paste the output word for word.
4. Look for file paths that only work on one machine.
5. Write the note: one row per check (passed, failed, could not check), the status,
   any blockers with the file name, the date and the tool used.

## Acceptance criteria (done when)

- [ ] The note exists, has one row per check, the pasted output and a status.
- [ ] GREEN only if the check command ran and passed.
- [ ] YELLOW or RED names at least one gap with its file.
- [ ] No file in `examples/card-krueger-toy/` changed.

## Check command

```bash
python3 -m pytest examples/card-krueger-toy/tests examples/mini-economics/tests
```

This audit checks only whether the code reproduces its numbers. Whether the DiD
design is convincing is a separate question for the researcher.
