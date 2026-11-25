# Prework — before Thu 26 Nov 09:00 (Rome)

Use a **personal laptop** with install rights if you can. Install steps for each system are in [`SETUP.md`](../SETUP.md); vendor links in [`docs/sources.md`](sources.md).

## Required

1. A **GitHub account**, and Git installed.
2. **Python 3.12** (3.11–3.14 also work; not 3.15).
3. **One agent**, installed and signed in: Claude Code (used in the demos), Codex or Cursor. If you use Claude Code or Codex inside VS Code, install the official extension ([`SETUP.md`](../SETUP.md) section 8).
4. Copy the workshop project folder to your laptop. Pick the folder first, then clone:

```bash
git clone https://github.com/meleantonio/ac4e-eief-workshop.git
cd ac4e-eief-workshop
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements-lock.txt
python3 -m pytest examples/card-krueger-toy/tests examples/mini-economics/tests
python3 scripts/validate_setup.py
```

If the pinned list fails, install from `requirements.txt` and note it. Windows: see the PowerShell block in [`SETUP.md`](../SETUP.md).

5. Paste your agent's version (`claude --version`, `codex --version` or `cursor-agent --version`) into `notes/cli_lane.md`.

## Helpful, not required

- **Cloud agents:** if your tool offers them (Claude Code on the web, Codex cloud, Cursor cloud agents), sign in once. On Friday you can otherwise use two local windows.
- **MCP (extra data connections):** optional, not used in the room. See [`docs/mcp_setup.md`](mcp_setup.md).

## Read ahead (optional, ≤15 min)

[`START_HERE.md`](../START_HERE.md) and [`GUIDE.md`](../GUIDE.md).
