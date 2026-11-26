# Issue card template

An issue is a to-do card on GitHub. Paste the block below into a new issue and give
it the label `ready`. Worked examples: [`examples/card-krueger-swarm/issues/`](../examples/card-krueger-swarm/issues/).

```markdown
# <Short title>

**Label:** `ready` · **Separate copy (branch):** `<branch-name>` · **Reviewer:** `<sub-agent name>`

## Goal

<One sentence describing the finished state, in a form you can check.>

## Allowed files

- `<path>` (create / edit / read only)

## Acceptance criteria (done when)

- [ ] <Yes/no check 1, e.g. "data/toy_fast_food.csv is unchanged">
- [ ] <Yes/no check 2, e.g. "the README states the sample restriction">
- [ ] <Yes/no check 3, e.g. "the DiD printed equals the DiD in the note">
- [ ] The check command passes.

## Check command

python3 -m pytest examples/card-krueger-toy/tests examples/mini-economics/tests

## Not in this card

- Editing raw data or tests.
- Any claim of identification or causality.
```

## Labels

`ready` → `in-progress` → `needs-review` → `done`. Only a human moves a card to `done`.

## Check before you mark it `ready`

- [ ] The goal is one sentence and someone else could check it.
- [ ] Each acceptance criterion can be answered yes or no in under a minute.
- [ ] The allowed files do not overlap with any other card that is running.
