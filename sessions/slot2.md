# Slot 2 — Thu 26 Nov 2026, 11:00–12:00 and Fri 27 Nov 2026, 09:30–10:15 (Rome)

Concepts **C5–C8**: Skills, writing your own Skill, sub-agents, and when to use which. The slot spans the night: you draft a Skill on Thursday and finish it on Friday morning.

| Clock | Block | You do | You write |
| ---: | --- | --- | --- |
| Thu 11:00–11:25 | **C5** Skills: why | Read and run `replication-checker` | `notes/skills_log.md` |
| Thu 11:25–11:55 | **C6** Create a Skill | Fill the Skill template, run it, fix one step | your `SKILL.md` |
| Thu 11:55–12:00 | Wrap, overnight task | Note what to finish tonight | — |
| *Thu 12:00 → Fri 09:30* | *Overnight* | *Finish your Skill draft ([`docs/between_sessions.md`](../docs/between_sessions.md))* | |
| Fri 09:30–09:35 | Recap | One Skill from the room | — |
| Fri 09:35–09:55 | **C7** Sub-agent vs Skill | Read `data-reviewer.md` | `notes/skills_log.md` |
| Fri 09:55–10:15 | **C8** Rule of thumb | Sort six tasks into Skill or sub-agent | `notes/skills_log.md` |

## C5 Skills: repeatable prompts (Thu 11:00–11:25)

A **Skill** is a saved set of instructions for a task you do often. The agent follows it the same way every time, and you can share it with coauthors: a recipe card in place of explaining the dish from memory.

Example: [`replication-checker`](../.claude/skills/replication-checker/SKILL.md) checks whether the Card–Krueger folder reproduces its numbers from a fresh start. Exercise: [`06_slot2_sdd_skill_pr.md`](../exercises/06_slot2_sdd_skill_pr.md), part A.

## C6 Create a Skill (Thu 11:25–11:55)

Make a folder and write one short file in it: a name, a line saying when to use it, and numbered steps. Test it once and fix whatever was unclear. It is like writing down your referee-report checklist so a student can follow it.

Worked example: `sample-restrictions-note`, which lists every rule that drops stores, gives the count after each step and quotes the command. Template: [`templates/skill_template.md`](../templates/skill_template.md). Exercise: part B.

## C7 Sub-agent vs Skill (Fri 09:35–09:55)

A **sub-agent** is a separate helper agent with its own blank notebook and one narrow job. It reports back a summary. A Skill is instructions; a sub-agent is another worker: a recipe versus a sous-chef you send to taste the sauce.

Example: [`data-reviewer`](../.claude/agents/data-reviewer.md) looks only at panel balance and group coding, and never edits. Exercise: part C.

## C8 Rule of thumb (Fri 09:55–10:15)

- Same steps, done the same way each time: **Skill**.
- A fresh pair of eyes, a big messy job, or work that can run at the same time: **sub-agent**.

"Recompute the DiD the same way each time" is a Skill. "Independently check my data coding" is a sub-agent. Exercise: part D.

## Leave with

- One `replication-checker` result (GREEN, YELLOW or RED) with the command it ran.
- Your own Skill file, run once and fixed once.
- Six tasks sorted, with one disagreement you can explain.

Reference answers: [`exercises/solutions/06_slot2_sdd_skill_pr_solution.md`](../exercises/solutions/06_slot2_sdd_skill_pr_solution.md).
