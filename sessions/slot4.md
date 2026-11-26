# Slot 4 — Fri 27 Nov 2026, 14:00–16:30 (Rome)

Review what the swarm returned, then goals, acceptance criteria, and verification. Then the Capstone on your own non-confidential project and a 7-day plan.

| Clock | Block | You do | You write |
| ---: | --- | --- | --- |
| 14:00–14:10 | Review the swarm | Review the two returned pull requests with `pr-reviewer` | review notes on each pull request |
| 14:10–14:25 | Goals | Rewrite one card title as a one-sentence goal | the card |
| 14:25–14:50 | Acceptance criteria | Add 3 yes/no checks, relaunch, judge the new pull request | the card + verdict |
| 14:50–15:50 | Verification and evaluation | Fix a planted fault, score your set-up | `notes/verification_scorecard.md` |
| 15:50–16:15 | Capstone | Apply a rules file, a Skill, a goal, and acceptance criteria to your own project | Capstone files |
| 16:15–16:30 | Close | Start the 7-day plan | `docs/adoption_plan_7d.md` |

## Review what the swarm returned (14:00–14:10)

Open each pull request linked to a card. Ask the [`pr-reviewer`](../.claude/agents/pr-reviewer.md) sub-agent for a read-only review, read the list of changes yourself, then move the card to `done` or back to `ready`. Exercise: [`08_slot4_verify_capstone.md`](../exercises/08_slot4_verify_capstone.md), part A.

## Goal (14:10–14:25)

A **goal** is one sentence describing the finished state, in a form you can check. It tells the agent where to stop, not how to get there: the destination in a satnav, not the turn-by-turn directions.

Example: "`notes/replication_audit_ck.md` exists and records GREEN, YELLOW or RED with the test output." Claude Code and Codex take it as `/goal …`; in Cursor, put it as the last line of the prompt. More: [`examples/card-krueger-goals/`](../examples/card-krueger-goals/README.md). Exercise: part B.

## Acceptance criterion (14:25–14:50)

An **acceptance criterion** is a yes/no check that says when a job counts as done, like a building inspector's checklist. In a swarm, each agent knows when to stop, and you can check many results quickly.

Example checks: `toy_fast_food.csv` is unchanged; the check command passes; the README states the sample restriction; the DiD printed equals the DiD in the note. Exercise: part C.

## Verification and evaluation (14:50–15:50)

Three parts:

1. **Need less checking**: small jobs, protected files, clear done-when checks.
2. **Automate the checking**: a **check command** that runs on its own: `python3 -m pytest examples/card-krueger-toy/tests examples/mini-economics/tests`.
3. **Test your set-up**: plant a known mistake and see whether your Skills, sub-agents and whole set-up catch it, as you might plant an error in a paper to test a referee.

Passing checks show the code does what it says. They never show identification or causality. Exercise: part D.

## Capstone (15:50–16:15)

On a **non-confidential** piece of your own work (or the Card–Krueger panel if all your data are restricted): one `AGENTS.md` rule, one Skill, one goal with 3 acceptance criteria, and the output of a check command. Rubric: [`docs/capstone_rubric.md`](../docs/capstone_rubric.md).

## Close (16:15–16:30)

Start [`docs/adoption_plan_7d.md`](../docs/adoption_plan_7d.md) for one project.

Reference answers: [`exercises/solutions/08_slot4_verify_capstone_solution.md`](../exercises/solutions/08_slot4_verify_capstone_solution.md).
