# Concept → files

Each concept pairs a demo, an exercise and a file the participant keeps. All on the synthetic Card–Krueger panel.

| Concept | Clock (Rome) | Demo | Exercise | You keep | Example files used |
| --- | --- | --- | --- | --- | --- |
| C1 Agent vs chatbot | Thu 09:10–09:30 | `demos/slot1_workflows.md` | `exercises/04_slot1_workflows.md` | `notes/lane_choice.md` | `examples/card-krueger-toy/src/did_analysis.py` |
| C2 Version control | Thu 09:30–09:55 | `demos/slot1_workflows.md` | `exercises/04_slot1_workflows.md` | merged pull request | `notes/lane_choice.md` |
| C3 `AGENTS.md` + privacy | Thu 09:55–10:35 | `demos/slot1_governance.md` | `exercises/05_slot1_governance.md` | `notes/my_agents_md.md`, `docs/privacy_boundary.md` | `AGENTS.md`, `CLAUDE.md`, `.gitignore`, `data/toy_fast_food.csv` |
| C4 To-do lists | Thu 10:45–11:00 | `demos/slot1_governance.md` | `exercises/05_slot1_governance.md` | `notes/modes_playbook.md` | `examples/card-krueger-goals/goals/ck-robustness-checks.md`, `templates/agent_task_contract.md` |
| C5 Skills: why | Thu 11:00–11:25 | `demos/slot2_sdd_skill_pr.md` | `exercises/06_slot2_sdd_skill_pr.md` | `notes/skills_log.md` | `.claude/skills/replication-checker/SKILL.md` |
| C6 Create a Skill | Thu 11:25–11:55 | `demos/slot2_sdd_skill_pr.md` | `exercises/06_slot2_sdd_skill_pr.md` | your `SKILL.md` | `templates/skill_template.md`, `.claude/skills/sample-restrictions-note/`, `src/panel_workflow.py` |
| C7 Sub-agent vs Skill | Fri 09:35–09:55 | `demos/slot2_sdd_skill_pr.md` | `exercises/06_slot2_sdd_skill_pr.md` | `notes/skills_log.md` | `.claude/agents/data-reviewer.md` |
| C8 Rule of thumb | Fri 09:55–10:15 | `demos/slot2_sdd_skill_pr.md` | `exercises/06_slot2_sdd_skill_pr.md` | `notes/skills_log.md` | six-task sort |
| C9 Using sub-agents | Fri 10:15–10:50 | `demos/slot3_subagents_vc.md` | `exercises/07_slot3_subagents_vc.md` | `notes/orchestration_log.md` | `.claude/agents/data-reviewer.md`, `.claude/agents/literature-reviewer.md`, `faults/citation_mismatch.md` |
| C10 Orchestrating | Fri 10:50–11:15 | `demos/slot3_subagents_vc.md` | `exercises/07_slot3_subagents_vc.md` | `notes/orchestration_log.md` | `examples/card-krueger-swarm/README.md` |
| C11 Issue-board swarm | Fri 11:25–12:00, 14:00–14:10 | `demos/slot3_subagents_vc.md`, `demos/slot4_verify_capstone.md` | `exercises/07_…` C, `exercises/08_…` A | two issues + pull requests | `examples/card-krueger-swarm/issues/`, `docs/issues_tracking.md`, `agent-harness/autonomous_agent_risk_card.md`, `.claude/agents/pr-reviewer.md` |
| C12 Goals | Fri 14:10–14:25 | `demos/slot4_verify_capstone.md` | `exercises/08_slot4_verify_capstone.md` | a goal on a card | `examples/card-krueger-goals/` |
| C13 Acceptance criteria | Fri 14:25–14:50 | `demos/slot4_verify_capstone.md` | `exercises/08_slot4_verify_capstone.md` | 3 criteria + verdict | `templates/issue_card.md`, card "Acceptance Criteria" sections |
| C14 Verification | Fri 14:50–15:50 | `demos/slot4_verify_capstone.md` | `exercises/08_slot4_verify_capstone.md` | `notes/verification_scorecard.md` | `examples/card-krueger-toy/faults/`, `.claude/hooks/post_edit_did_analysis.py`, `replication/README.md` |
| Capstone | Fri 15:50–16:15 | `demos/slot4_verify_capstone.md` | `exercises/08_slot4_verify_capstone.md` | Capstone files | `docs/capstone_rubric.md`, `templates/agent_use_record.md` |
| Close | Fri 16:15–16:30 | — | — | `docs/adoption_plan_7d.md` | — |

## Off the teaching path (kept, not taught)

- `examples/mini-economics/` (its checks still run in the check command).
- MCP and the FRED connection: optional prework ([`docs/mcp_setup.md`](mcp_setup.md)).
- `literature-mapper`, `sdd` Skill, `sdd-orchestrator`, `loop-verifier` (optional mention only).
- `docs/project_brief.md`, `docs/research_design_memo.md`, `notes/context_patterns.md`: reference only.
- Research tracks, Teaching peek: dropped.
