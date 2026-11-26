# Privacy check

Fill this in Thu 09:55–10:35 for one real project of yours. Three questions; if any answer is "no" or "unclear", that project stays out of the agent.

## 1. How sensitive is the data?

Tick one. If a file mixes classes, use the strictest.

- [ ] **Public or synthetic** (the Card–Krueger panel)
- [ ] **Unpublished, not sensitive** (your own draft, public series)
- [ ] **Restricted** (administrative, bank, student, identifiable, or other limited-access data)
- [ ] **Contains secrets** (passwords, keys, tokens, `.env`)

Restricted files and files with secrets stay **out of the agent** in this workshop.

## 2. Who may see it?

Institutional or vendor rules can forbid a tool even for non-sensitive files.

- Tool:
- Am I allowed to put this material into **this** tool? Yes / No / Unclear (unclear = no)

## 3. Where does the agent run?

- [ ] On my laptop
- [ ] On a cloud machine (fill [`agent-harness/autonomous_agent_risk_card.md`](../agent-harness/autonomous_agent_risk_card.md) first)

| Check | What I found | OK today? |
| --- | --- | --- |
| Files the agent can read | | |
| Files the agent can change | | |
| Can data leave the machine? | | |
| Are chat records kept by the vendor? | | |
| How do I stop it and undo its changes? | | |

## Rule

**Anonymize, authorize, keep it on the machine.**

1. **Anonymize.** Remove identifiers, small cells and sensitive fields before any agent sees the file.
2. **Authorize.** Confirm your institution allows this tool for this file.
3. **Keep it on the machine.** No cloud agent or outside connection for sensitive files.

## Folder boundaries in this project

| Folder | Agent may | Agent must not |
| --- | --- | --- |
| `examples/card-krueger-toy/` | read; edit on a separate copy | claim causal results; change `data/toy_fast_food.csv` |
| `docs/`, `notes/`, `templates/` | read, edit | add secrets |
| `data/raw/`, `data/private/`, `.env` | nothing | read or save to GitHub |
| Confidential drives | nothing | be pasted into prompts |

## Sign-off

- Name / date / tool:
- Cloud agent allowed today? Yes / No / Risk card only
