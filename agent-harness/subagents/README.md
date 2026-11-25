# Sub-agents

A sub-agent is a separate helper agent with its own blank notebook and one narrow
job. It reports back a summary; you decide what to do with it.

**Use a sub-agent** for a fresh pair of eyes, a big messy job, or work that can run
at the same time. If the same steps just need doing the same way each time, write a
Skill instead (see [`../skills/README.md`](../skills/README.md)).

## How to use one (C9)

1. Call it by name: "Use `data-reviewer` to review `examples/card-krueger-toy/`."
2. Give it one narrow instruction.
3. Keep it read-only.
4. Read its report before you act.

## Where they live

- Claude Code: `.claude/agents/` (portable copy: `../claude/agents/`)
- Cursor: copy `../cursor/subagents/` into `.cursor/agents/`
- Codex: copy `../codex/agents/` into `.codex/agents/`

## Keeping them read-only

Each tool does this differently:

- **Claude Code:** the files allow only reading tools (`Read`, `Grep`, `Glob`) and
  block editing and running commands.
- **Cursor:** the files set `readonly: true`, which blocks edits and commands.
- **Codex:** a sub-agent follows the permissions of the chat that calls it. Set the
  chat to read-only before you call a reviewer; see `../codex/README.md`.
