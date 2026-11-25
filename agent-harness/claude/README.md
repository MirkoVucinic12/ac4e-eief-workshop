# Claude Code set-up files

Copy into `.claude/` at the repository root (this repo already includes live
examples in `.claude/`).

| Asset | Path in this folder | Project path |
| --- | --- | --- |
| Skills | `skills/<name>/SKILL.md` | `.claude/skills/<name>/SKILL.md` |
| Sub-agents | `agents/<name>.md` | `.claude/agents/<name>.md` |
| Hooks | `hooks/settings.example.json` | `.claude/settings.json` |
| Hook scripts | `hooks/post_edit_did_analysis.py` | `.claude/hooks/` |
| MCP (optional prework) | `mcp/mcp.json.example` | `.mcp.json` at repo root |

In an interactive session, accept the workspace trust dialog before project hooks run. `/hooks` lists loaded hooks and their commands. It does not trust or edit them. The example Stop hook appends a line to `notes/orchestration_log.md`.

Official docs: [Claude Code skills](https://code.claude.com/docs/en/skills), [Claude Code hooks](https://code.claude.com/docs/en/hooks).
