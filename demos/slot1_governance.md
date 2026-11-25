# Demo — C3 `AGENTS.md` + privacy, C4 To-do lists

**When:** Thu 26 Nov 2026, 09:55–10:35 and 10:45–11:00 (Rome).
**Example:** the synthetic Card–Krueger panel.

## C3 `AGENTS.md`: boundaries first (09:55–10:35)

**Say:** a plain-text rules file the agent reads before any task. What it may touch, what it must never do, how to check its work. House rules for a new RA.

**1. Walk the file (5 min).** Open [`AGENTS.md`](../AGENTS.md) and point to three lines:

- "Do not modify raw data."
- "Do not let agents certify identification, causality, or interpretation."
- "Do not ask agents to read `data/raw/`, `data/private/`, or `.env`."

Also show [`CLAUDE.md`](../CLAUDE.md) (Claude's pointer to the same rules) and `.gitignore` (files GitHub never receives).

**2. Watch a refusal.**

```text
Change the fte_employment value of the first row in
examples/card-krueger-toy/data/toy_fast_food.csv to 25.
```

Expected: the agent declines and quotes "Do not modify raw data". If it edits anyway, discard the change in Source Control and say: **the rules file is guidance; your review is the guard.**

**3. Privacy in three questions (10 min).** Walk [`docs/privacy_boundary.md`](../docs/privacy_boundary.md):

1. How sensitive is the data? (public / unpublished / restricted / contains secrets)
2. Who may see it? (is this tool allowed by your institution for this file?)
3. Where does the agent run? (your laptop or a cloud machine)

Rule: **anonymize, authorize, keep it on the machine.** In this room, only public or synthetic data.

**4. Participants** add one rule for their own project in `notes/my_agents_md.md` and fill the privacy check.

**Codex / Cursor:** both read `AGENTS.md` automatically.

## C4 To-do lists (10:45–11:00)

**Say:** before acting, the agent writes its steps as a checklist. You edit it, then it works through it. A shopping list you check before anyone drives to the store.

**1. Ask for the list only:**

```text
Read examples/card-krueger-goals/goals/ck-robustness-checks.md.
Do not edit any file. Write a numbered to-do list of the steps you would take.
Then stop and wait for me.
```

Expected steps, roughly: load the panel, check balance, compute group means, run the drop-one-store check, write a note.

**2. Edit it live:** delete one step or move "check balance" first. Then:

```text
Do step 1 only. Show me what you found and stop.
```

**Codex / Cursor:** Codex and Claude Code show the list in the chat. Cursor has Plan mode (`Shift+Tab`), which writes the list before any edit.

**Say:** the list is where you catch a bad plan for free. Fixing it after the edits costs more.
