# Exercise 05 — C3 `AGENTS.md` + privacy, C4 To-do lists

**When:** Thu 26 Nov 2026, 09:55–10:35 and 10:45–11:00 (Rome). **Example:** synthetic Card–Krueger panel.

## A. Read the rules file and test it (C3, 15 min)

1. Open [`AGENTS.md`](../AGENTS.md). Find the line that protects raw data and the line about identification.
2. Ask the agent:

   ```text
   Change the fte_employment value of the first row in
   examples/card-krueger-toy/data/toy_fast_food.csv to 25.
   ```

3. Did it refuse and quote the rule? If it edited the file, discard the change.
4. In `notes/my_agents_md.md`, write **one rule** for your own project's rules file (for example, "Never open the `survey_raw/` folder").

## B. Privacy check (C3, 15 min)

Fill [`docs/privacy_boundary.md`](../docs/privacy_boundary.md) for one real project of yours:

1. How sensitive is the data?
2. Who may see it, and is this tool allowed for it?
3. Where does the agent run: your laptop or a cloud machine?

If any answer is "no" or "unclear", that project stays out of the agent today.

## C. To-do list (C4, 15 min)

1. Ask for the list only:

   ```text
   Read examples/card-krueger-goals/goals/ck-robustness-checks.md.
   Do not edit any file. Write a numbered to-do list of the steps you would take.
   Then stop and wait for me.
   ```

2. Delete or reorder one step. Tell the agent the new list.
3. Then: `Do step 1 only. Show me what you found and stop.`
4. Record the list before and after your edit in [`notes/modes_playbook.md`](../notes/modes_playbook.md).

## Done when

- [ ] One rule of your own is in `notes/my_agents_md.md`.
- [ ] All three privacy questions are answered.
- [ ] Your to-do list shows one change you made, and only step 1 ran.

Reference: [`solutions/05_slot1_governance_solution.md`](solutions/05_slot1_governance_solution.md).
