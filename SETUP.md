# Setup Guide

Complete as much as you can **before Thu 26 Nov 09:00 (Rome)**. If something fails,
still attend. The sessions are designed so you can follow the demos and fill
Markdown notes even with a partial install.

These notes were written in September 2026, and vendor installers change occasionally. If a command below disagrees with the official page, follow the official page. Most of these install steps run in a terminal, so open Terminal (macOS or Linux) or PowerShell (Windows) to run the commands.

## Quick checklist

- [ ] Git installed and configured (`user.name` and `user.email`).
- [ ] GitHub account available.
- [ ] Python 3.12 installed (3.11–3.14 also work; not 3.15).
- [ ] One coding assistant installed and signed in: **Claude Code** (preferred),
      Codex, or Cursor.
- [ ] The assistant’s command line prints a version (or you logged a blocker).
- [ ] Visual Studio Code installed (`code --version`), if you will use Claude Code
      or Codex in an editor.
- [ ] Claude Code and/or Codex extension installed **and signed in** in VS Code
      (publisher Anthropic / OpenAI).

Optional, not required to sit down on Thursday:

- [ ] Extra data tool (FRED) attempted. Optional; not used in the room.
- [ ] Cloud / background assistant account ready, if your tool has one.

## 1. Git

Confirm:

```bash
git --version
```

If not installed, follow the instructions below.

### macOS

Install the developer tools (includes Git), or install Git with Homebrew if
you already use it:

```bash
xcode-select --install
# or, if Homebrew is installed:
brew install git
```

### Windows

Install [Git for Windows](https://git-scm.com/download/win). During setup,
keep the option that adds Git to your `PATH`. A terminal with Git is what
the assistants use; GitHub Desktop is optional and does not replace this.

Claude Code on native Windows works more smoothly with Git for Windows
installed. WSL users can use the Linux Git from their distro.

### Linux (Debian / Ubuntu)

```bash
sudo apt update
sudo apt install git
```

Fedora / RHEL: `sudo dnf install git`.

### Identity (needed before you make a GitHub change)

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Use the email attached to your GitHub account.

## 2. GitHub account

Create an account at [https://github.com/signup](https://github.com/signup) if you do not have one.

Do **not** add student records, bank extracts, confidential manuscripts, or
secrets.

## 3. Python

The workshop runs on Python 3.12. CI installs 3.12, and `requirements-lock.txt` was built on CPython 3.12. Python 3.11, 3.13, and 3.14 are the rest of the supported range.

Do not install Python 3.15 for this workshop. The download page on [python.org](https://www.python.org/downloads/) currently offers 3.15 as the latest release. The locked builds of numpy, pandas, pydantic-core, and cryptography have no CPython 3.15 wheels, so `pip install -r requirements-lock.txt` fails on 3.15. Install 3.12 from the version list on that page, or with the commands below. Check:

```bash
python3 --version
```

On Windows, if `python3` is not found, try `py -3 --version`.

### macOS

- From [python.org](https://www.python.org/downloads/), or
- `brew install python@3.12` if you use Homebrew.

The `python3` that ships with some macOS developer tools can be older than
3.11. If `--version` is below 3.11, or if it is 3.15, install 3.12.

### Windows

Install from [python.org](https://www.python.org/downloads/). Tick **Add
python.exe to PATH**. Or:

```powershell
winget install Python.Python.3.12
```

### Linux (Debian / Ubuntu)

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

## 4. Choose one coding assistant

You do not need every product. Pick the one you will use in the room.
Install and sign in **here first**. Visual Studio Code comes after that, in
section 8, if you want the same assistant inside an editor.


| Lane     | Tool                                              | Use when                          |
| -------- | ------------------------------------------------- | --------------------------------- |
| Primary  | Claude Code (command line, app, or VS Code)       | Default live demos                |
| Parallel | Codex (command line, app, or VS Code)             | You already work in Codex         |
| Parallel | Cursor (app; optional command line)               | You want an editor-first workflow |


I recommend the Claude Code desktop app; that is what I will use in the live demos.

## 5. Claude Code (preferred)

Official overview: [https://code.claude.com/docs/en/overview](https://code.claude.com/docs/en/overview)

### Command line (recommended so Slot 1 can record a version)

macOS, Linux, or WSL:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Windows PowerShell:

```powershell
irm https://claude.ai/install.ps1 | iex
```

Homebrew (macOS):

```bash
brew install --cask claude-code
```

Windows WinGet:

```powershell
winget install Anthropic.ClaudeCode
```

Sign in when the installer or first `claude` run asks. Note the printed
version.

### Desktop app

Download from the Claude Code overview page (macOS, Windows, Linux beta).
Sign in, open a project folder, use the Code tab. The app includes Claude
Code; you can still use the command line after the native installer.

To use Claude Code inside VS Code as well, finish this section, then section 8.

## 6. Codex

Use this section if Codex is your tool in the room. Official docs:
[https://learn.chatgpt.com/docs](https://learn.chatgpt.com/docs)

### Command line

macOS / Linux:

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"
```

Homebrew:

```bash
brew install --cask codex
```

If you already have Node.js:

```bash
npm install -g @openai/codex
```

Then:

```bash
codex --version
codex
```

Sign in when prompted. Note the printed version.

### App

The ChatGPT desktop app includes Codex. Download it from the OpenAI website if you do not have it installed yet.

To use Codex inside VS Code as well, finish this section, then section 8.

## 7. Cursor

Use this section if Cursor is your tool in the room. Official docs:
[https://cursor.com/docs](https://cursor.com/docs)

### App

1. Download Cursor from [https://cursor.com/download](https://cursor.com/download).
2. Install, sign in, and open a project folder.
3. Let indexing finish.
4. Use Agent for edits, Plan when you want a reviewable plan before coding,
   and Ask for read-only exploration. The IDE and the CLI (`agent`) both have
   these three modes. In the CLI, Ask is `/ask` or `--mode=ask`, and Plan is
   `/plan`, Shift+Tab, or `--mode=plan`. Agent is the default.

Help → About (or the equivalent in your version) is enough to record that
the app is installed. Also try a command-line version if your install
provides one.

### Command line (optional; labels change by version)

Current Cursor docs install with:

```bash
# macOS, Linux, WSL
curl https://cursor.com/install -fsS | bash
```

Windows PowerShell:

```powershell
irm 'https://cursor.com/install?win32=true' | iex
```

Then try, in order, until one prints a version:

```bash
agent --version
cursor-agent --version
cursor --version
```

Cursor is a separate editor. Skip section 8 if Cursor is your only tool.

## 8. Visual Studio Code

Install [Visual Studio Code](https://code.visualstudio.com/download) if you
want Claude Code or Codex inside an editor. Do this **after** the command line
or app in sections 5–6 is installed and signed in.

Official download: [https://code.visualstudio.com/download](https://code.visualstudio.com/download)

### macOS

Download the installer from the page above. Open the `.dmg` and drag Visual
Studio Code into Applications.

If you use Homebrew:

```bash
brew install --cask visual-studio-code
```

Add the `code` command to your PATH: in VS Code, open the Command Palette
(`Cmd+Shift+P`), run **Shell Command: Install 'code' command in PATH**, then
open a new terminal.

### Windows

Download the **User** installer from the page above. Keep the option that adds
VS Code to your `PATH`.

Or:

```powershell
winget install Microsoft.VisualStudioCode
```

Restart the terminal after install.

### Linux (Debian / Ubuntu)

Download the `.deb` from the same page and install it, or:

```bash
sudo snap install --classic code
```

Fedora / RHEL: follow the Linux instructions on the download page, then
`sudo dnf install code`.

### Confirm

```bash
code --version
```

On macOS, if this fails, run the Shell Command PATH step above.

Open a project folder in VS Code (`code .` from that folder, or File → Open
Folder).

### Install the Claude Code and Codex extensions

Install the official add-on (extension) for the assistant you will use.
Search results include lookalikes; check the publisher. You do not need both.

**From the editor**

1. Open Extensions: `Cmd+Shift+X` (macOS) or `Ctrl+Shift+X` (Windows / Linux).
2. Search **Claude Code**. Install **Claude Code** by **Anthropic** (verified).
   [Marketplace listing](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code)
   (id `anthropic.claude-code`).
3. Search **Codex**. Install **Codex** by **OpenAI** (id `openai.chatgpt`).
   [Marketplace listing](https://marketplace.visualstudio.com/items?itemName=openai.chatgpt).
4. Reload the window if the icons do not appear (Command Palette →
   **Developer: Reload Window**).

**From the terminal** (after `code --version` works):

```bash
code --install-extension anthropic.claude-code
code --install-extension openai.chatgpt
```

Installing the extension does not sign you in. Sign in inside VS Code next, even
if the command line is already authenticated, because the editor keeps its own
session.

Docs: [Claude Code in VS Code](https://code.claude.com/docs/en/vscode);
[Codex in an editor](https://learn.chatgpt.com/docs/codex/ide).

### Sign in to Claude Code in VS Code

Use the same Claude account you used in section 5.

1. Keep a project folder open in VS Code.
2. Open the Claude Code panel. Click the **Spark** icon in the left Activity
   Bar. Or open the Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`), type
   **Claude Code**, and choose **Open in New Tab**.
3. The first time, a sign-in screen appears. Click **Sign in**.
4. Your browser opens. Log in to Claude (Pro, Max, Team, Enterprise, or a
   Claude Console account). Allow the connection when asked.
5. Return to VS Code. You are signed in when the prompt box is ready. A short
   “Learn Claude Code” checklist may appear; you can dismiss it.
6. If you see **Not logged in · Please run /login**, wait for the sign-in
   screen, or reload the window (Command Palette → **Developer: Reload
   Window**) and click **Sign in** again.

### Sign in to Codex in VS Code

Use the same ChatGPT account you used in section 6.

1. Keep a project folder open in VS Code.
2. Open the Codex sidebar. Click the **Codex** icon in the Activity Bar. If
   you do not see it, open the Command Palette and run **Codex: Open Codex
   Sidebar**.
3. Click **Sign in with ChatGPT** (prefer this over an API key for the
   workshop).
4. Your browser opens. Log in with ChatGPT. Codex is included on Free, Go,
   Plus, Pro, Business, Edu, and Enterprise
   ([pricing](https://learn.chatgpt.com/docs/pricing)): Free and Go cover the
   desktop app (GPT-6 Luna at Standard speed, subject to rollout), while Plus
   adds the web app, the CLI, the IDE extension, and iOS; Codex Cloud is not
   included with Free or Go. Click Continue or Allow when asked.
5. Return to VS Code. You are signed in when the Codex chat is ready to take a
   prompt.
6. To check or switch accounts, open the Codex sidebar, click the **gear**
   icon, and use **Log out**, then **Sign in with ChatGPT** again.

Cursor users who skipped the VS Code installer can add the same Anthropic and
OpenAI extensions from Cursor’s Extensions view and sign in the same way.

## If something will not install

1. Note the exact command and the error (no secrets). Send a message to [a.mele1@lse.ac.uk](mailto:a.mele1@lse.ac.uk) for help.
2. Come anyway. Pair with a neighbour or a shared machine at the Thursday pause (10:35).
3. You can still take notes in Markdown even if an installer failed.
