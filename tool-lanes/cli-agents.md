# Tool lane: agents in a command window

For Claude Code, Codex or Cursor run from a command window instead of an app. The
concepts live in the same places as in each tool's app lane:
[`claude-app.md`](claude-app.md), [`codex-app.md`](codex-app.md), [`cursor.md`](cursor.md).

Install steps are in [`SETUP.md`](../SETUP.md). From the project folder, run the
check command once before you start the agent:

```bash
python3 -m pytest examples/card-krueger-toy/tests examples/mini-economics/tests
```

## Three instructions, in order

```text
Read AGENTS.md. Do not edit files. Summarise the rules and the check command.
```

```text
Plan issue #N only. Do not edit files yet. Give me the to-do list and the files you will touch.
```

```text
Do issue #N only. Stay within the allowed files. Run the check command and paste the output.
```

## Habits

- One command window per separate copy (branch).
- Save small versions, each with a clear note.
- Never give the agent access to confidential folders.
- Read a Skill before you run it.
