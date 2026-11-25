# Tool lane: Claude Code (app or command window)

The primary lane for the workshop. Install steps are in [`SETUP.md`](../SETUP.md).

1. Install Claude Code and sign in.
2. Open this project folder.
3. First instruction: "Read `AGENTS.md` and `CLAUDE.md`. Do not edit files. Summarise the rules."

## Where each concept lives

| Concept | In Claude Code |
| --- | --- |
| Rules file (C3) | `CLAUDE.md`, which points to `AGENTS.md` |
| To-do list (C4) | Plan mode (Shift+Tab); the agent shows its to-do list before acting |
| Skills (C5, C6) | `.claude/skills/<name>/SKILL.md`; call by name, e.g. "Use the `replication-checker` Skill" |
| Sub-agents (C7, C9) | `.claude/agents/<name>.md`; "Use the `data-reviewer` sub-agent on `examples/card-krueger-toy/`"; `/agents` lists them |
| Goal (C12) | `/goal <one sentence>`; `/goal clear` removes it |
| Cloud agents from issues (C11) | Claude Code on the web, or `@claude` in a GitHub issue if the Claude GitHub app is installed |
| Automatic check after each edit (C14, optional) | `.claude/settings.json`; example in `agent-harness/claude/hooks/` |

## Habits

- Start read-only. Allow edits only once the goal and allowed files are clear.
- Keep sub-agents read-only.
- Read a Skill before you run it.
- Read the list of changes and run the check command before you merge.

Menu names change between versions. Check them in your installed version.
