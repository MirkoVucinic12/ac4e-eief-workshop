# Reference — Exercise 04

## A. Agent vs chatbot

**Chatbot:** answers from memory. It usually quotes the published Card and Krueger (1994) figures or makes up a number. It cannot see this folder.

**Agent:** runs the script and quotes it:

```text
NJ change: 2.0 FTE workers.
PA change: -1.0 FTE workers.
Toy DID estimate: 3.0 FTE workers.
Research caveat: this is not Card and Krueger's raw data and does not certify a causal claim.
```

Good one-line answer: "The agent ran the code on our file and showed me the output; the chatbot guessed."

## B. First pull request

The list of changes shows one file, `notes/lane_choice.md`, with one line changed (for example `- [x] Claude Code`). Anything else in the list means stop and discard the extra change.

Command-window equivalent:

```bash
git checkout -b slot1-first-pr
git diff
git add notes/lane_choice.md
git commit -m "Add my tool choice" && git push -u origin slot1-first-pr
```

Then open the pull request on GitHub, review and merge.

Common problems:

- **GitHub asks for a password and refuses it.** Sign in through the editor or the GitHub app; fix at the 10:35 pause.
- **The agent saved and published without asking.** Say "wait for my OK before publishing" in the prompt next time.
