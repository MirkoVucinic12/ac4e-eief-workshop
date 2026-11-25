# Codex set-up files

Copy into project-native Codex locations after reading each file.

| Asset | Path in this folder | Project path |
| --- | --- | --- |
| Skills | `skills/<name>/SKILL.md` | `.agents/skills/<name>/SKILL.md` |
| Sub-agents | `agents/<name>.toml` | `.codex/agents/<name>.toml` |
| Hooks | `hooks/economics-hooks-example.json` | `.codex/hooks.json` |
| Hook scripts | `hooks/post_edit_did_analysis.py` | `.codex/hooks/` |
| MCP (optional prework) | `mcp/config.toml.example` | `.codex/config.toml` |

In the Codex CLI, `/hooks` inspects hook sources and is where you review and trust a non-managed hook. Trust is stored against the hook's current hash. A new or changed hook is skipped until you trust it again. The example Stop hook appends a line to `notes/orchestration_log.md`.

Custom agents inherit the parent session's sandbox and approval mode. `sandbox_mode` and `approval_policy` in an agent file are ignored. Before you delegate a reviewer, set the parent mode (CLI: `/permissions`; app: the permission control under the composer). Instructions that say "do not edit files" do not create a separate read-only sandbox.

Invoke subagents by name in prompts, e.g. `Use data-reviewer to review the panel read-only.`

Official docs: [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Codex skills](https://learn.chatgpt.com/docs/build-skills), [Codex hooks](https://learn.chatgpt.com/docs/hooks).
