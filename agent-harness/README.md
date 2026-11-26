# Agent set-up: Skills, sub-agents and checks

This folder holds the workshop set-up for **Claude Code**, **Codex** and **Cursor**:
the same Skills and sub-agents, saved in each tool's own format. The set-up is the
rules file (`AGENTS.md`) plus Skills, sub-agents and checks.

## Skill or sub-agent?

- **Skill** = saved instructions. Use one when the same steps should be done the
  same way every time. Example: "Recompute the DiD the same way each time."
- **Sub-agent** = a separate helper agent with its own blank notebook and one narrow
  job. Use one when you need a fresh pair of eyes, a big messy job, or work that can
  run at the same time. Example: "Independently check my data coding."

A Skill is instructions; a sub-agent is another worker. Either way, you read the
result and you decide.

## Skills on the workshop path

| Skill | Use when | Concept |
| --- | --- | --- |
| `replication-checker` | Checking whether the example reproduces its numbers from a fresh start | Skills, verification |
| `sample-restrictions-note` | Listing every rule that drops stores, with the count after each | Create a Skill (worked example) |
| `hooks` | Setting up the optional automatic check after each edit | Verification (optional) |
| `loop-on-verification` | Letting the agent check its own work before you review | Verification (optional) |

Off the path: `literature-mapper` (optional mention only) and `sdd`.

## Sub-agents on the workshop path

All are read-only: they report, they never edit.

| Sub-agent | One narrow job | Concept |
| --- | --- | --- |
| `data-reviewer` | Panel balance, missing values, NJ/PA coding | Sub-agents, verification |
| `literature-reviewer` | References and literature claims | Using sub-agents |
| `pr-reviewer` | Reviews a returned pull request against its card | Issue-board swarm |
| `loop-verifier` | One check-and-revise round (optional) | Verification |

Off the path: `sdd-orchestrator`.

## Where each tool keeps them

| Tool | Skills | Sub-agents | Copies in this folder |
| --- | --- | --- | --- |
| **Claude Code** | `.claude/skills/<name>/SKILL.md` | `.claude/agents/<name>.md` | `claude/` |
| **Codex** | `.agents/skills/<name>/SKILL.md` | `.codex/agents/<name>.toml` | `codex/` |
| **Cursor** | `.cursor/skills/<name>/SKILL.md` | `.cursor/agents/<name>.md` | `cursor/` |

The project folder already has working copies in `.claude/` and `.agents/skills/`.
For Cursor or Codex sub-agents, copy the files from `cursor/` or `codex/` after
reading them. Skill copies must stay identical in every location.

Each tool folder also holds an optional automatic check after each edit (`hooks/`)
and an optional data connection example (`mcp/`, prework only).

## Other files

- [`autonomous_agent_risk_card.md`](autonomous_agent_risk_card.md): fill in before
  any cloud agent works on the project.
- [`mcp/fred/`](mcp/fred/): optional FRED data connection, not used in the room.

Menu names change between versions. Check them in your installed tool.
