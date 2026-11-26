# Issue-board swarm: cards and labels

Each job is an **issue**, a to-do card on GitHub. Agents pick up cards marked `ready`, work in their own separate copy, and return a **pull request** linked to the card. A human reviews every pull request before it is merged.

## Card flow

| Label | Meaning | Who moves it |
| --- | --- | --- |
| `ready` | Goal, allowed files and done-when checks are written; an agent may start | you |
| `in-progress` | An agent is working on it in its own separate copy | you, when you start the agent |
| `needs-review` | A pull request linked to the card is open | the agent, or you |
| `done` | You reviewed the pull request against the card's checks and merged it | you |

A card that fails review goes back to `ready` with a comment saying which check failed.

## What every card contains

1. **Goal**: one sentence describing the finished state.
2. **Allowed files**: the only files the agent may change.
3. **Acceptance criteria**: 3–4 yes/no checks.
4. **Check command**: `python3 -m pytest examples/card-krueger-toy/tests examples/mini-economics/tests`.

Template: [`templates/issue_card.md`](../templates/issue_card.md).

## Workshop cards

| Card | When | Note |
| --- | --- | --- |
| [`ck-data-cleaning`](../examples/card-krueger-swarm/issues/ck-data-cleaning.md) | Live: launched Fri 11:25, reviewed Fri 14:00 | Writer: documents the panel |
| [`ck-parallel-trends-figure`](../examples/card-krueger-swarm/issues/ck-parallel-trends-figure.md) | Live: launched Fri 11:25, reviewed Fri 14:00 | Before/after group-means figure |
| [`ck-literature`](../examples/card-krueger-swarm/issues/ck-literature.md) | Spare | Checker: literature claims |
| [`ck-estimation`](../examples/card-krueger-swarm/issues/ck-estimation.md) | Spare | Not run live |

## Rules

- No more than 2 cards live at once in the room.
- Two cards never share an allowed file.
- Fill [`agent-harness/autonomous_agent_risk_card.md`](../agent-harness/autonomous_agent_risk_card.md) before any cloud agent. No confidential data.
- Write "Related to #N" in a pull request. Use "Closes #N" only after a human accepts the work.
- Review each pull request with the `pr-reviewer` sub-agent and your own reading of the list of changes.
