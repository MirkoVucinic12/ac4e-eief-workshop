# Exercise 04 — Agent vs chatbot, Version control

**When:** Thu 26 Nov 2026, 09:10–09:55 (Rome). **Example:** synthetic Card–Krueger panel.

## A. Agent vs chatbot (10 min, read-only)

1. In a plain browser chat, ask:

   ```text
   In the Card–Krueger fast-food example, what is the NJ–PA change in employment?
   ```

2. In your agent, opened on this project folder, ask:

   ```text
   Read examples/card-krueger-toy/README.md. Then run
   python3 examples/card-krueger-toy/src/did_analysis.py
   Do not edit any file. Quote the printed NJ change, PA change and DiD,
   and quote the line that says what this number is not.
   ```

3. In `notes/lane_choice.md`, write one line: what did the agent do that the chatbot could not?

## B. Your first pull request (15 min)

1. Make a separate copy called `slot1-first-pr`.
2. In `notes/lane_choice.md`, tick the tool you use. Change nothing else.
3. Look at the list of changes. Only that file should appear.
4. Save a version with the note "Add my tool choice" and publish it.
5. On GitHub, open a pull request, read the list of changes, and merge.

You can click through these steps in your editor's Source Control panel, or ask the agent to do steps 1–4 and wait for your OK before it publishes. The command-window version is in [`demos/slot1_workflows.md`](../demos/slot1_workflows.md).

**Stuck on GitHub sign-in?** Do steps 1–4 locally and show the list of changes to a neighbour. Fix sign-in at the 10:35 pause.

## Done when

- [ ] You can say in one sentence how the agent's answer differs from the chatbot's.
- [ ] One pull request touching only `notes/lane_choice.md` is merged (or reviewed locally).

Reference: [`solutions/04_slot1_workflows_solution.md`](solutions/04_slot1_workflows_solution.md).
