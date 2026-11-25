# Demo — C1 Agent vs chatbot, C2 Version control

**When:** Thu 26 Nov 2026, 09:10–09:55 (Rome). Live demo at most 10 minutes per concept.
**Example:** the synthetic Card–Krueger panel, [`examples/card-krueger-toy/`](../examples/card-krueger-toy/).

## C1 Agent vs chatbot (09:10–09:30)

**Say:** a chatbot only talks. An agent can also act: it opens your files, runs your code, reads the result and tries again. Phoning a friend versus an RA at your desk.

**1. Plain chat** (a browser chat window, no files attached):

```text
In the Card–Krueger fast-food example, what is the NJ–PA change in employment?
```

It answers from memory, often with the published figures, which are not what this folder computes.

**2. Agent** (opened on this project folder; read-only):

```text
Read examples/card-krueger-toy/README.md. Then run
python3 examples/card-krueger-toy/src/did_analysis.py
Do not edit any file. Quote the printed NJ change, PA change and DiD,
and quote the line that says what this number is not.
```

Expected: NJ change 2.0, PA change −1.0, toy DiD 3.0 FTE workers, and the caveat "this is not Card and Krueger's raw data and does not certify a causal claim".

**Point out:** the agent ran the code and quoted the output. You can see the command. The chatbot could not.

**Codex / Cursor:** same prompt. In Cursor, use Ask mode for read-only.

## C2 Version control: first pull request (09:30–09:55)

**Say:** a record of every saved version, each with a note, so you can see what changed and go back. GitHub keeps it online and lets coauthors review before accepting. Track Changes plus dated "save as" copies.

**Show** the agent's edit as a list of changes:

```text
In examples/card-krueger-toy/README.md, add one sentence under the title saying
the data are synthetic. Do not save a version yet. Show me the list of changes.
```

Then reject it (discard in the editor's Source Control panel) so the room sees that nothing is final until you accept.

**Live pull request** (instructor does it once; participants copy):

1. Make a separate copy called `slot1-first-pr` (editor: branch picker → "Create new branch").
2. Edit one line in `notes/lane_choice.md` (your tool name).
3. Save a version with the note "Add my tool choice" and publish it to GitHub.
4. On GitHub, open the pull request, read the list of changes, approve.
5. Merge.

Or ask the agent to do steps 1–3, and read the list of changes before it publishes:

```text
Make a separate copy called slot1-first-pr. Change only notes/lane_choice.md:
tick the tool I use. Show me the list of changes and wait for my OK before
saving a version and publishing it.
```

If you prefer the command window:

```bash
git checkout -b slot1-first-pr
git status
git diff
git add notes/lane_choice.md
git commit -m "Add my tool choice" && git push -u origin slot1-first-pr
```

**Say:** agents rewrite files in seconds. The list of changes is where you check them, history lets you undo, and the pull request is the human check before the main copy changes.
