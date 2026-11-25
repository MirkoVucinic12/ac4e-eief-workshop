# Start here

Over two mornings and one afternoon you learn 14 concepts for supervising an AI agent the way you supervise an RA: give it rules, a to-do list, a finish line and a check.

Everything uses **one example**: the synthetic Card–Krueger minimum-wage panel in [`examples/card-krueger-toy/`](examples/card-krueger-toy/). You do not need to write code.

## Before Thursday

1. Complete [`docs/prework.md`](docs/prework.md).
2. Follow [`SETUP.md`](SETUP.md) (printable [`SETUP.pdf`](SETUP.pdf)) for Git, Python and your agent (Claude Code, Codex or Cursor).
3. Run `python3 scripts/validate_setup.py`.

## In the room

| Open this | For |
| --- | --- |
| [`SCHEDULE.md`](SCHEDULE.md) | The clock |
| [`sessions/slot1.md`](sessions/slot1.md) … [`slot4.md`](sessions/slot4.md) | What each block covers |
| [`exercises/`](exercises/) | What you do (answers in [`exercises/solutions/`](exercises/solutions/README.md)) |
| [`GUIDE.md`](GUIDE.md) | One-page summary and word list |
| [`AGENTS.md`](AGENTS.md) | The rules file the agent reads |

## The two days

- **Thursday 09:00–12:00.** What an agent is, your first pull request, the rules file and privacy, to-do lists, then Skills. Overnight: finish your own Skill.
- **Friday 09:30–12:00.** Sub-agents, when to use a Skill or a sub-agent, then two agents start work on GitHub cards before lunch.
- **Friday 14:00–16:30.** Review what the agents returned, write goals and done-when checks, catch a planted mistake, then apply it all to your own non-confidential project.

## After Friday

Follow [`docs/adoption_plan_7d.md`](docs/adoption_plan_7d.md) on one non-confidential project.

## First prompt (read-only)

```text
Read START_HERE.md, AGENTS.md and SCHEDULE.md. Do not edit any file.
Tell me what to do first, which folders you must never open,
and which command checks my setup.
```
