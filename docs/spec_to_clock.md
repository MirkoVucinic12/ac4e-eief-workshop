# Concept map — EIEF / Luiss 8h

**Clock (Rome, do not change):** Thu 26 Nov 2026 09:00–12:00; Fri 27 Nov 2026 09:30–12:00 and 14:00–16:30.
**Course goal:** give an AI agent a research job with rules, a finish line and a check, and show a colleague the result reproduces.
**One example:** the synthetic Card–Krueger panel (`examples/card-krueger-toy/`). No research tracks.
**Rule:** each concept has a definition, an analogy, a Card–Krueger example and an exercise. Agents never certify identification or causality.

Concepts take 400 minutes; logistics and the Capstone take 80. Slot totals: 120, 60 + 45, 105 and 150 minutes.

## Slot 1: Thu 09:00–11:00

| Clock | Min | Block | Exercise |
| --- | ---: | --- | --- |
| 09:00–09:10 | 10 | Welcome, room rules, `python3 scripts/validate_setup.py` | — |
| 09:10–09:30 | 20 | **C1** Agent vs chatbot | `exercises/04_slot1_workflows.md` A |
| 09:30–09:55 | 25 | **C2** Version control (first pull request) | `exercises/04_slot1_workflows.md` B |
| 09:55–10:35 | 40 | **C3** `AGENTS.md` boundaries + privacy | `exercises/05_slot1_governance.md` A–B |
| 10:35–10:45 | 10 | Pause / setup rescue | — |
| 10:45–11:00 | 15 | **C4** To-do lists | `exercises/05_slot1_governance.md` C |

## Slot 2: Thu 11:00–12:00 + Fri 09:30–10:15

| Clock | Min | Block | Exercise |
| --- | ---: | --- | --- |
| Thu 11:00–11:25 | 25 | **C5** Skills: why | `exercises/06_slot2_sdd_skill_pr.md` A |
| Thu 11:25–11:55 | 30 | **C6** Create a Skill | `exercises/06_slot2_sdd_skill_pr.md` B |
| Thu 11:55–12:00 | 5 | Thursday wrap, overnight task | — |
| Fri 09:30–09:35 | 5 | Recap | — |
| Fri 09:35–09:55 | 20 | **C7** Sub-agent vs Skill | `exercises/06_slot2_sdd_skill_pr.md` C |
| Fri 09:55–10:15 | 20 | **C8** Rule of thumb: Skill or sub-agent | `exercises/06_slot2_sdd_skill_pr.md` D |

## Slot 3: Fri 10:15–12:00

| Clock | Min | Block | Exercise |
| --- | ---: | --- | --- |
| 10:15–10:50 | 35 | **C9** Using sub-agents | `exercises/07_slot3_subagents_vc.md` A |
| 10:50–11:15 | 25 | **C10** Orchestrating sub-agents and swarms | `exercises/07_slot3_subagents_vc.md` B |
| 11:15–11:25 | 10 | Pause | — |
| 11:25–12:00 | 35 | **C11** Issue-board swarm (launch; agents work over lunch) | `exercises/07_slot3_subagents_vc.md` C |

## Slot 4: Fri 14:00–16:30

| Clock | Min | Block | Exercise |
| --- | ---: | --- | --- |
| 14:00–14:10 | 10 | **C11** Review what the swarm returned | `exercises/08_slot4_verify_capstone.md` A |
| 14:10–14:25 | 15 | **C12** Goals | `exercises/08_slot4_verify_capstone.md` B |
| 14:25–14:50 | 25 | **C13** Acceptance criteria (rewrite one issue, relaunch) | `exercises/08_slot4_verify_capstone.md` C |
| 14:50–15:50 | 60 | **C14** Verification and evaluation | `exercises/08_slot4_verify_capstone.md` D |
| 15:50–16:15 | 25 | Capstone: C3 + C6 + C12 + C13 on own non-confidential project | `exercises/08_slot4_verify_capstone.md` E |
| 16:15–16:30 | 15 | Close + 7-day adoption plan | `docs/adoption_plan_7d.md` |

## Definitions

| # | Definition | Analogy |
| --- | --- | --- |
| C1 | A chatbot only talks. An agent can also act: it opens your files, runs your code, reads the result and tries again. | Phoning a friend vs an RA at your desk |
| C2 | A record of every saved version, each with a note. GitHub keeps it online and lets others review changes before they are accepted. | Track Changes plus dated "save as" copies |
| C3 | A plain-text rules file the agent reads before any task: what it may touch, what it must never do, how to check its work. | House rules for a new RA |
| C4 | Before acting, the agent writes its steps as a checklist. You edit it, then it works through it. | A shopping list checked before driving |
| C5 | A saved set of instructions for a task you do often, followed the same way every time. | A recipe card |
| C6 | A folder and one short file: name, when to use it, numbered steps. Test once, fix what was unclear. | Your referee checklist written down |
| C7 | A separate helper agent with its own blank notebook and one narrow job, reporting back a summary. | Recipe vs sous-chef |
| C8 | Same steps the same way → Skill. Fresh eyes, big messy job, or parallel work → sub-agent. | Own checklist vs asking a colleague to referee |
| C9 | Call the helper by name, one narrow instruction, read-only; read its report before acting. | Two referees who don't talk |
| C10 | Split the job, hand each part to a different agent, put results together. A swarm is many agents at once; a human decides. | A PI running several RAs |
| C11 | Each job is a GitHub issue; agents pick up `ready` cards and return linked pull requests. | A job board in a shared office |
| C12 | One sentence describing the finished state, in a form you can check. | A satnav destination |
| C13 | A yes/no check that says when a job counts as done. | A building inspector's checklist |
| C14 | Need less checking, automate the rest, test your set-up against known mistakes. | Planting an error to test a referee |

Out of the room: MCP (optional prework). Teaching peek and research tracks are not part of this workshop.
