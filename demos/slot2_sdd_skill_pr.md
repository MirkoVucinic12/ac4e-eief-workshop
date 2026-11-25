# Demo — C5–C8 Skills and sub-agents

**When:** Thu 26 Nov 2026, 11:00–12:00 and Fri 27 Nov 2026, 09:30–10:15 (Rome).
**Example:** the synthetic Card–Krueger panel.

## C5 Skills: why (Thu 11:00–11:25)

**Say:** a Skill is a saved set of instructions for a task you do often. The agent follows it the same way every time, and coauthors can reuse it. A recipe card.

**1. Read it first (3 min).** Open [`.claude/skills/replication-checker/SKILL.md`](../.claude/skills/replication-checker/SKILL.md). Point to: the header lines (name, when to use it), the numbered steps, and the GREEN / YELLOW / RED rule.

**2. Run it:**

```text
Use the replication-checker Skill on examples/card-krueger-toy/.
Do not edit any file. Report GREEN, YELLOW or RED, the exact command you ran,
and its output. Do not claim a check passed unless you ran it.
```

Expected: the check command runs and passes; rating GREEN or YELLOW with reasons.

**Codex / Cursor:** the same Skill is at `.agents/skills/replication-checker/SKILL.md` (copies in `agent-harness/codex/` and `agent-harness/cursor/`). See [`tool-lanes/`](../tool-lanes/).

## C6 Create a Skill (Thu 11:25–11:55)

**Say:** a folder, one short file: a name, a line saying when to use it, numbered steps. Test once, fix what was unclear. Your referee checklist written down for a student.

**1. Show the worked example** `.claude/skills/sample-restrictions-note/SKILL.md`: it lists every rule that drops stores, gives the count after each step, and quotes the command.

**2. Run it:**

```text
Use the sample-restrictions-note Skill on examples/card-krueger-toy/.
Do not edit data or code.
```

Expected counts (from `panel_workflow.py`): 47 raw rows → 43 after the status filter → 42 after dropping missing values → 36 rows, 18 stores in the balanced panel.

**3. Participants** copy [`templates/skill_template.md`](../templates/skill_template.md) to `.claude/skills/<your-skill>/SKILL.md` on their separate copy, run it once, fix one step.

## Thu 11:55–12:00 Wrap

Overnight: finish your Skill draft. No confidential data. See [`docs/between_sessions.md`](../docs/between_sessions.md).

## Fri 09:30–09:35 Recap

One participant reads their Skill aloud. The room names one unclear step.

## C7 Sub-agent vs Skill (Fri 09:35–09:55)

**Say:** a sub-agent is a separate helper with its own blank notebook and one narrow job. It reports back a summary. A Skill is instructions; a sub-agent is another worker. Recipe versus sous-chef.

Open [`.claude/agents/data-reviewer.md`](../.claude/agents/data-reviewer.md) and mark three things:

- **Job:** panel balance, missing values, NJ/PA group coding, documentation.
- **Limits:** it can read and search; it cannot edit files or run commands.
- **Report:** a short list of findings for you to act on.

## C8 Rule of thumb (Fri 09:55–10:15)

**Say:** same steps done the same way → Skill. A fresh pair of eyes, a big messy job, or work that can run at the same time → sub-agent.

Show the six tasks from [`exercises/06_slot2_sdd_skill_pr.md`](../exercises/06_slot2_sdd_skill_pr.md) part D. Participants sort them, then compare with a neighbour. Take one disagreement from the room.
