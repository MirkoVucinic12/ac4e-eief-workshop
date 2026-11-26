# Card–Krueger issue cards

Issue cards for orchestrating, the issue-board swarm, and acceptance criteria. Each card has a one-sentence goal, the files the agent may touch, 3–4
yes/no acceptance criteria and the check command. Copy a card into a GitHub issue
with [`../../templates/issue_card.md`](../../templates/issue_card.md).

## One writer, one checker

| Role | Card | May touch |
| --- | --- | --- |
| Writer | [`ck-data-cleaning`](issues/ck-data-cleaning.md) | `examples/card-krueger-toy/README.md`, `data_notes.md` |
| Checker | [`ck-literature`](issues/ck-literature.md) | `references/bibliography.bib`, `notes/ck_literature_note.md` |

The two cards share no files, so the agents cannot overwrite each other.

## The lunchtime swarm (two cards only)

| Card | Separate copy (branch) | Reviewer |
| --- | --- | --- |
| [`ck-data-cleaning`](issues/ck-data-cleaning.md) | `ck/data-cleaning` | `data-reviewer` |
| [`ck-parallel-trends-figure`](issues/ck-parallel-trends-figure.md) | `ck/parallel-trends-figure` | `pr-reviewer` |

Run no more than two cards live. Fill in
[`../../agent-harness/autonomous_agent_risk_card.md`](../../agent-harness/autonomous_agent_risk_card.md)
before you start a cloud agent.

Spare: [`ck-estimation`](issues/ck-estimation.md). Do not run it live.

## Labels

A card moves through four labels:

| Label | Meaning |
| --- | --- |
| `ready` | Goal, allowed files and acceptance criteria are written; an agent may pick it up |
| `in-progress` | An agent is working on its own separate copy |
| `needs-review` | A pull request is open and linked to the card |
| `done` | A human checked every acceptance criterion and merged |

## Before you merge

1. Judge the pull request only against the card's acceptance criteria.
2. If two agents edited the same lines, decide who fixes it before merging.
3. Run the check command after each merge:

   ```bash
   python3 -m pytest examples/card-krueger-toy/tests examples/mini-economics/tests
   ```

4. Log what you accepted and rejected in `notes/orchestration_log.md`.

One human makes the final merge. Agents do not certify identification or causality.
