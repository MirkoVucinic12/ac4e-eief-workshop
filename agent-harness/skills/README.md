# Skills

A Skill is a saved set of instructions for a task you do often. The agent follows
it the same way every time, and you can share it with coauthors.

**Use a Skill** when the same steps should be done the same way each time. If you
need a fresh pair of eyes or a big separate job instead, use a sub-agent (see
[`../subagents/README.md`](../subagents/README.md)).

The Skills live in one folder per tool, with identical files:

- Claude Code: `.claude/skills/` (portable copy: `../claude/skills/`)
- Codex: `.agents/skills/` (portable copy: `../codex/skills/`)
- Cursor: copy `../cursor/skills/` into `.cursor/skills/` after reading it

Start with `replication-checker` (C5) and `sample-restrictions-note` (C6). To write
your own, use [`../../templates/skill_template.md`](../../templates/skill_template.md).
Read a Skill before you run it.
