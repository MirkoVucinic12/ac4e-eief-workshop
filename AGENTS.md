# Agent Instructions — AC4E EIEF / Luiss (8h faculty pack)

## Project

Participant repository for **Agentic Coding for Economists** at EIEF / Luiss
(26–27 Nov 2026, eight hours, four slots). Public instructional materials, a synthetic
Card–Krueger teaching example, templates, and participant work products.

**Primary demo lane:** Claude Code. Codex and Cursor are fully supported parallel lanes.

## Workflow

- Use issue → branch → pull request for non-trivial changes.
- Plan before editing multiple files.
- Keep edits scoped to the active session artifact.
- Run the documented verification command before claiming work is complete.
- Treat agent output as a proposal until a human reviews the diff and evidence.

## Economics Standards

- Document data sources, transformations, units, and sample restrictions.
- Use relative paths.
- Do not modify raw data.
- Separate research claims from code mechanics.
- Do not let agents certify identification, causality, or interpretation.
- The Card–Krueger files under `examples/card-krueger-toy/` are **synthetic teaching data**, not research claims.

## Privacy / Confidential Data

- Do not commit secrets, API keys, private data, confidential manuscripts, bank extracts, or student records.
- Do not ask agents to read `data/raw/`, `data/private/`, or `.env`.
- Do not paste confidential/institutional data into prompts or cloud agents.
- If using a cloud or autonomous agent, complete `agent-harness/autonomous_agent_risk_card.md` first.
- Faculty default: anonymize, authorize, don’t send it off the machine (see `docs/privacy_boundary.md`).

## Verification

```bash
python3 -m pytest examples/card-krueger-toy/tests examples/mini-economics/tests
```

For packaging, follow `replication/README.md`. Prefer `requirements-lock.txt` for a clean clone.
