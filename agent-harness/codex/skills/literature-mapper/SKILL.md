---
name: literature-mapper
description: Use when asked to map citations, claims, and bibliography gaps for an economics memo or PR without inventing sources.
---

# Literature Mapper

Source in this repo: `.claude/skills/literature-mapper/SKILL.md` (portable copies must match). Inspect this file before you trust it. Record source path and git revision. This Skill does not install packages from the network or write bibliographic entries it did not read.

Discovery and verification are separate steps. Discovery may list search queries. Verification requires a DOI or authoritative URL, a version or access date, a primary-text passage, and correction/retraction status.

When invoked:

1. Read the project brief / design memo / PR diff named by the human.
2. List claims that need citations.
3. If `references/bibliography.bib` is missing or empty, stop verification and report a **blocker**: create or fill that file from primary sources before mapping. Do not invent BibTeX.
4. Map existing keys to claims only when the metadata in the `.bib` file matches a source you can name (DOI, JSTOR URL, or publisher page).
5. For each mapped claim fill a ledger row (`templates/citation_verification_ledger.md`):
   - claim text
   - bib key
   - DOI or authoritative URL
   - version / date checked
   - primary-text passage (page or section)
   - supports the claim? yes / no / overclaim
   - correction / retraction status
6. Flag fabricated items, metadata mismatches, and claims the cited passage does not support.
7. Propose search queries for gaps. **Do not invent** bibliographic entries, DOIs, or page numbers.

Return blockers first, then a claim-to-source table, then suggested next reads.

## Rating

- **Green:** every research claim has a verified ledger row; toy/synthetic material is not cited as published evidence.
- **Yellow:** some claims are discovery-only and labelled as such.
- **Red:** a source was guessed, a DOI was fabricated, or a corrected/retracted item was accepted without notice.

Never mark the literature map complete if sources were guessed.

## Workshop fixture

`docs/research_design_memo.md` plus `references/bibliography.bib`. The Card–Krueger toy DID is **not** Card and Krueger (1994). Treat that mismatch as a catch if a draft claims otherwise.
