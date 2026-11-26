# Task card

Fill this in before you hand one job to an agent. It reuses four concepts:
goal, to-do list, acceptance criteria and allowed files.

## Goal

One sentence describing the finished state, in a form you can check:

-

## To-do list

Ask the agent for its plan first. Edit it here before it starts.

1.
2.
3.

## Acceptance criteria (done when)

Yes/no checks, not slogans.

- [ ]
- [ ]
- [ ] The check command passes:

  ```bash
  python3 -m pytest examples/card-krueger-toy/tests examples/mini-economics/tests
  ```

## Allowed files

- May read:
- May edit (at most three for a workshop pull request):
- Never touch: `data/raw/`, `data/private/`, `.env`, the tests, this card

## The human decides

- [ ] Identification and causal interpretation
- [ ] Privacy and permission to use the data
- [ ] Whether to merge

If the agent edits a file not listed above, stop and reject the change.
