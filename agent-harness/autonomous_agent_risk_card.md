# Cloud-agent risk card

Fill this in before a cloud or background agent works on the project, for example
when it picks up an issue card over lunch. Five minutes. This is your own check, not
a vendor certificate.

## The agent

- Name and link:
- Date checked:
- Fallback if it is unavailable (e.g. a second local window):

## Six questions

Rate each Green, Yellow or Red.

| Question | Your answer | Rating |
| --- | --- | --- |
| **Read:** what may it read? It must never read `data/raw/`, `data/private/`, `.env`, secrets, student records, confidential drafts or institutional data. | | |
| **Write:** which separate copy (branch) may it change? It may open a pull request; merging stays human. | | |
| **Memory:** what stays after the run (branch, logs, the vendor's records)? | | |
| **Where it runs:** whose machine or cloud, and does it hold any passwords or confidential data? | | |
| **Review:** who checks the pull request against the card's acceptance criteria before merging? | | |
| **Record:** where do you log start, progress, stop and the final list of changes? | | |

Agents do not certify identification, causality or interpretation.

## Decision

- [ ] Safe for read-only use
- [ ] Safe to work on its own separate copy and open a pull request
- [ ] Not safe for this project
- [ ] Need more information first

---

## Worked example (this project folder, 22 Aug 2026)

Kept as a record. Fill in the blanks above for **your** tool; do not copy these.

- Agent: Cursor Cloud Agent (`https://cursor.com/agents/`).
- Read: public workshop files and public web; confidential paths denied. Yellow.
- Write: its own branch `cursor/post-march-course-reevaluation-d5f9`; draft pull request; no merge. Yellow.
- Memory: branch, saved versions, chat record, vendor records. Yellow.
- Where it runs: separate cloud copy of the public project. Yellow.
- Review: a human checks citations, changes and check-command output before merging. Green.
- Record: version history, pull request, check command. Green.
- Decision: safe to work on its own branch and open a pull request.
