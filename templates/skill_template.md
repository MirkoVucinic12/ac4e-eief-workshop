# Skill template

A Skill is a saved set of instructions for a task you do often. Copy the block
below into `.claude/skills/<skill-name>/SKILL.md` on your own separate copy (branch).
For Codex, save the same file under `.agents/skills/<skill-name>/SKILL.md`.

Worked example: [`.claude/skills/sample-restrictions-note/SKILL.md`](../.claude/skills/sample-restrictions-note/SKILL.md).

```markdown
---
name: <skill-name, lowercase-with-dashes, same as the folder>
description: Use when <the situation in which the agent should pick this Skill>.
---

# <Skill title>

1. Read <the files the agent needs>.
2. Run <the exact command> and keep its output.
3. <The next step, one action per line.>
4. Write <what, where> and quote the command output.

## Do not

- Edit raw data, tests or files outside <folder>.
- Claim identification or causality.
```

## Check before you share it

- [ ] The two header lines (`name`, `description`) are filled in, and `name` matches the folder.
- [ ] Each step is one action that a new RA could follow without asking you.
- [ ] At least one step runs a command and quotes its output.
- [ ] You ran it once, found one unclear step and rewrote it.
