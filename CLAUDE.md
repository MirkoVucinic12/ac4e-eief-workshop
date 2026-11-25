# Claude Code Adapter — AC4E EIEF / Luiss

Claude Code is the **primary** demo lane for this faculty workshop.

## Use With

Read and follow [`AGENTS.md`](AGENTS.md). This file only adds Claude-specific path notes.

## Local Paths

| Piece | Where in this repo | Claude Code expectation |
| --- | --- | --- |
| Project rules | `AGENTS.md` + this file | Keep both at repo root |
| Skills | `.claude/skills/*/SKILL.md` (portable copies in `agent-harness/claude/skills/`) | Invoke by name or let Claude select |
| Subagents | `.claude/agents/*.md` (portable in `agent-harness/claude/agents/`) | Delegate reviewer roles explicitly |
| MCP | `agent-harness/claude/mcp/mcp.json.example` → project `.mcp.json` | Optional (not in the room) |
| Hooks | `.claude/hooks/` + `settings.example.json` | Optional |

## Workshop defaults

- Prefer **read-only** prompts until the issue acceptance criteria are clear.
- For the checkpoint PR, keep the branch scoped to one issue.
- Never mark replication green without a command run or equivalent evidence.
- Confidential data: refuse. Point the human to `docs/privacy_boundary.md`.

## CLI smoke check (Slot 1)

```bash
claude --version
# or the install's equivalent; record the exact command in notes/cli_lane.md
```
