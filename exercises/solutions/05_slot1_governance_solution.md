# Reference — Exercise 05

## A. Rules file

- Raw data line: "Do not modify raw data."
- Identification line: "Do not let agents certify identification, causality, or interpretation."
- Expected agent reply to the CSV edit: a refusal that quotes the raw-data rule and offers an alternative (for example, documenting the issue in a note).
- If the agent edited the file anyway: discard the change. Lesson: the rules file guides the agent; your review of the list of changes is what protects the data.

Good rules for your own project (one is enough):

- "Never open `data/confidential/`."
- "Do not change any file in `tables/final/` without asking."
- "After every edit, run `do master.do` and quote the last 20 lines of the log."

## B. Privacy check

For the Card–Krueger panel: public/synthetic; the tool is allowed; runs on the laptop. Everything passes.

For a project with administrative or bank data: restricted → stays out of the agent today, whatever the tool or location. Rule: **anonymize, authorize, keep it on the machine.**

## C. To-do list

A typical first list:

1. Load `toy_fast_food.csv`.
2. Check each store has one before and one after row.
3. Compute group means by state and wave.
4. Run the drop-one-store check.
5. Write a short note with the results.

A good edit: move step 2 first, or delete step 4 for now. Step 1 only should report the number of rows and stores without changing any file.

Record the list before and after in `notes/modes_playbook.md`.
