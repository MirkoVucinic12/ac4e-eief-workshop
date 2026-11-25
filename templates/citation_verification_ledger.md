# Citation verification ledger

> **Not on the workshop path.** Kept for longer projects after the workshop. For the workshop, use [`agent_task_contract.md`](agent_task_contract.md) (task card) and [`issue_card.md`](issue_card.md).

Use this ledger with the `literature-mapper` Skill (a written procedure). Finding a paper in search is not verification; check the primary text before adding a BibTeX entry, and never invent one.

| Claim (quote or paraphrase) | Source key in `references/bibliography.bib` | DOI or authoritative URL | Version / date checked | Primary-text passage (page or section) | Supports the claim? | Correction / retraction status | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | yes / no / overclaim | none / corrected / retracted / unknown | keep / rewrite / drop |

## Blockers (list first)

- Fabricated source:
- Metadata mismatch (wrong year, volume, DOI, or title):
- Claim not in the cited passage:
- Corrected or retracted item accepted without notice:

## Candidate papers from search (not yet verified)

Record search queries tried here, and add a bibliographic entry only after a human checks the primary text.

1.
2.

## Rule

If a Skill run guesses a citation, treat the check as incomplete and mark the map yellow or red until you fill the row from the primary text.
