---
name: hooks
description: Use when you want to configure a lifecycle hook that runs a verification command automatically after the agent edits a file or completes a session. Works with Cursor, Claude Code, and Codex.
---

# Hooks

A hook is a postcondition listener: the agent tool fires a command when a specified
event occurs, without you having to ask. For economists, the most useful hook is one
that runs the documented verification command automatically after every edit to an
analysis script — so a broken estimation step surfaces immediately rather than
after several downstream changes.

## When to use a hook

Use a hook when:

- You want every edit to `did_analysis.py` (or equivalent) to trigger `pytest`
  automatically.
- You want the agent to log its stopping state to a file at the end of a session.
- You want a data-map check to run whenever a data file changes.

Do not use a hook to replace human review of a diff or to auto-approve a result.

## Cross-tool hook configuration

| Tool | Hook config location | Event types |
| --- | --- | --- |
| Cursor | `.cursor/hooks.json` | `afterFileEdit`, `afterShellExecution`, `stop` (wrapper `version` + `hooks`; see below) |
| Claude Code | `~/.claude/settings.json` under `"hooks"` | `PreToolUse`, `PostToolUse`, `Stop`, `Notification` |
| Codex | Codex app Hooks section (verify in your version) | Varies by release; confirm in-app |

## Card-Krueger worked example

### Cursor — run the verification suite after editing the DiD script

Create or update `.cursor/hooks.json` in this repository. The file must be an object with `version` and `hooks`. The filter field is `matcher`, not `match`. For `afterFileEdit`, that matcher is tested against the tool name `Write`, not against a path. Read `file_path` from the JSON on stdin if the command should run only for the DiD script. For `afterShellExecution`, the matcher is tested against the shell command. For `stop`, it is tested against `Stop`.

The `stop` command below appends one line to `notes/orchestration_log.md`. A hook does not replace human review of the diff. The fuller example, including the raw-data warning, is `agent-harness/cursor/hooks/economics-hooks-example.json`.

```json
{
  "version": 1,
  "hooks": {
    "afterFileEdit": [
      {
        "matcher": "Write",
        "command": "python3 -c \"import json,sys,subprocess; p=json.load(sys.stdin).get('file_path',''); target='examples/card-krueger-toy/src/did_analysis.py'; sys.exit(0 if not p.endswith(target) else subprocess.call([sys.executable,'-m','pytest','examples/card-krueger-toy/tests','-q']))\""
      }
    ],
    "stop": [
      {
        "matcher": "Stop",
        "command": "python3 -c \"import datetime; open('notes/orchestration_log.md','a').write('| '+datetime.datetime.now().strftime('%Y-%m-%d %H:%M')+' | Agent stopped | — | Review diff before merge |\\n')\""
      }
    ]
  }
}
```

### Claude Code — postcondition hook after writing to analysis files

Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 -m pytest examples/card-krueger-toy/tests -q 2>&1 | tail -10"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo '[Hook] Agent stopped. Check notes/orchestration_log.md.' "
          }
        ]
      }
    ]
  }
}
```

## How to verify the hook fires

When invoked, do the following:

1. Identify the tool the participant is using (Cursor, Claude Code, or Codex).
2. Locate the hook configuration path for that tool (see table above).
3. Read the current hook configuration file if it exists.
4. Draft the hook entry appropriate for the tool — postcondition on the DiD script,
   stop-session log entry.
5. Ask the participant to make a small, safe edit (e.g., add a comment to
   `did_analysis.py`) and confirm the hook command fires and its output appears.
6. Report: which event triggered the hook, what command ran, what the output was,
   and whether the verification command returned zero failures.

## Constraints

- Do not commit hook config to a shared branch without noting it in the PR description.
- Hooks run agent-side; they do not replace the human diff review before merge.
- If a hook command writes to a file, document the output location in `AGENTS.md`
  or the PR body. The Cursor `stop` example and the Claude Code `Stop` example
  append a line to `notes/orchestration_log.md`.
- Verify current hook feature names in your installed tool version before a live demo.
