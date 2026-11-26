# Slot 1 — Thu 26 Nov 2026, 09:00–11:00 (Rome)

What an agent is, saved versions and pull requests, the rules file, and to-do lists. Slot 2 follows straight on at 11:00.

One example all day: the synthetic Card–Krueger panel in [`examples/card-krueger-toy/`](../examples/card-krueger-toy/). It is teaching data, not research evidence.

| Clock | Block | You do | You write |
| ---: | --- | --- | --- |
| 09:00–09:10 | Welcome, room rules | Run `python3 scripts/validate_setup.py` | — |
| 09:10–09:30 | Agent vs chatbot | Ask the same question in a chat and in the agent | `notes/lane_choice.md` |
| 09:30–09:55 | Version control | Your first pull request | one merged pull request |
| 09:55–10:35 | `AGENTS.md` + privacy | Read the rules file, watch a refusal, fill the privacy check | `notes/my_agents_md.md`, `docs/privacy_boundary.md` |
| 10:35–10:45 | Pause / setup rescue | Fix installs, GitHub sign-in | `notes/cli_lane.md` |
| 10:45–11:00 | To-do lists | Get a to-do list, edit it, run step 1 | `notes/modes_playbook.md` |

## Agent vs chatbot (09:10–09:30)

A **chatbot** only talks. An **agent** can also act: it opens your files, runs your code, reads the result and tries again. Think of phoning a friend for advice versus hiring an RA who sits at your desk.

Try it: ask "what is the NJ–PA change in employment?" in a plain chat, then ask the agent to run `examples/card-krueger-toy/src/did_analysis.py` and quote the printed note. Exercise: [`04_slot1_workflows.md`](../exercises/04_slot1_workflows.md), part A.

## Version control (09:30–09:55)

**Version control** keeps every **saved version** of the project, each with a short note, so you can see what changed and go back. GitHub keeps that record online and lets others review changes before they are accepted. It works like Track Changes plus dated "save as" copies, shared with coauthors.

Five words for today:

- **project folder**: all the files plus their history;
- **saved version**: a snapshot with a one-line note;
- **separate copy** (branch): where you or the agent edit without touching the main copy;
- **list of changes**: the lines added and removed, shown in green and red;
- **pull request**: a request to fold a separate copy into the main one, with a review page.

The steps are: make a separate copy, edit, save with a note, open a pull request, review the list of changes, then accept (merge). Exercise: [`04_slot1_workflows.md`](../exercises/04_slot1_workflows.md), part B.

## `AGENTS.md`: boundaries first (09:55–10:35)

[`AGENTS.md`](../AGENTS.md) is a plain-text **rules file** the agent reads before any task. It says what the agent may touch, what it must never do, and how to check its work: the house rules you give a new RA on day one.

Privacy comes down to three questions. How sensitive is the data? Who may see it? Where does the agent run? The short answer: **anonymize, authorize, keep it on the machine.** Exercise: [`05_slot1_governance.md`](../exercises/05_slot1_governance.md), parts A–B.

## To-do lists (10:45–11:00)

Before acting, the agent writes the steps it plans as a **to-do list**. You edit the list, then it works through it and ticks items off. It is the shopping list you check before anyone drives to the store. Exercise: [`05_slot1_governance.md`](../exercises/05_slot1_governance.md), part C.

## Leave with

- One merged pull request (or a reviewed separate copy if GitHub sign-in is pending).
- One rule of your own in `notes/my_agents_md.md` and a filled `docs/privacy_boundary.md`.
- One edited to-do list in `notes/modes_playbook.md`.

Reference answers: [`exercises/solutions/`](../exercises/solutions/README.md).
