# Tool lane: other agents

For Antigravity, OpenClaw, Hermes, Eve, Windsurf, Cline or any other agent. The
workshop concepts have different names in each tool; look for these:

| Concept | Look for |
| --- | --- |
| Rules file (C3) | `AGENTS.md`, rules, memories, instruction files |
| To-do list (C4) | plan mode, task list, checklist |
| Skills (C5, C6) | skills, commands, routines, playbooks |
| Sub-agents (C7, C9) | sub-agents, custom agents, workers, roles |
| Goal (C12) | goals, finish conditions, task targets |
| Cloud agents from issues (C11) | background agents, scheduled tasks, issue triggers |
| Review (C14) | list of changes, logs, pull requests, run records |

## Before an agent runs on its own

Fill in [`agent-harness/autonomous_agent_risk_card.md`](../agent-harness/autonomous_agent_risk_card.md).
If the agent can act while you are not watching, give it narrower permissions, keep a
log, and review its pull request before anything is merged. The workshop does not run
unsupervised agents.

## Links

- OpenClaw: <https://github.com/openclaw/openclaw> ([skills](https://docs.openclaw.ai/tools/skills))
- Hermes Agent by Nous Research: <https://hermes-agent.nousresearch.com/>
- Eve by Vercel: <https://vercel.com/eve>
