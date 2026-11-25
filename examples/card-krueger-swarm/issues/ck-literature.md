# [CK] Check the Card–Krueger references

**Label:** `ready` · **Role:** checker · **Separate copy (branch):** `ck/literature` · **Reviewer:** `literature-reviewer`

## Goal

`references/bibliography.bib` has correct entries for Card and Krueger (1994) and
their 1993 NBER working paper, and `notes/ck_literature_note.md` summarises the study.

## Allowed files

- `references/bibliography.bib` (read and fix)
- `notes/ck_literature_note.md` (create)

## Acceptance criteria (done when)

- [ ] The 1994 entry reads: *American Economic Review*, volume 84, number 4,
      pages 772–793, with both authors.
- [ ] The 1993 entry is NBER Working Paper 4509, with both authors and the year.
- [ ] The note states the question, the data (NJ and PA fast-food stores, two-wave
      phone survey, 1992), the main finding (no significant fall in NJ employment
      relative to PA), and that the toy data here cannot replicate it.
- [ ] No file in `examples/card-krueger-toy/` changed, and the check command passes.

## Check command

```bash
python3 -m pytest examples/card-krueger-toy/tests examples/mini-economics/tests
```

A human checks the 1994 entry against the article itself.

## Not in this card

- Editing anything in `examples/card-krueger-toy/`.
- Any claim that the toy estimate replicates the 1994 paper.
