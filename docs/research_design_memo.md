# Research design memo (v0)

Copy the structure from `templates/research_design_memo.md` and keep claims modest.

## Question

Teaching contrast on a synthetic fast-food panel (NJ vs PA, before and after).

## Literature

The running case is inspired by Card and Krueger (1994), key `card1994minimum` in `references/bibliography.bib`. The CSV in this repository (the project folder and its change history) is **not** that paper's data, so do not cite the toy DID of 3.0 FTE workers as a published result. Check every reference in `templates/citation_verification_ledger.md` before adding sources.

## Design

Descriptive two-by-two comparison of mean FTE employment, without standard errors, significance statements, or causal claims.

## Data

Synthetic CSV shipped in this repository: store-wave observations across treatment group `NJ` and comparison group `PA` in `before` and `after` waves, with no student, bank, or administrative microdata.

## Verification

```bash
python3 -m pytest examples/card-krueger-toy/tests examples/mini-economics/tests
```

Statistical approval stays with the researcher; passing tests check code mechanics rather than identification.

## Issue candidates (pick one for the classroom pull request, a proposed change on GitHub)

1. Document one sample restriction in the replication note (allowed: README or `src/did_analysis.py` docstring).
2. Add a provenance row mapping the printed group-means table to the function that produces it.
3. Map the claims in this memo against `references/bibliography.bib`, with no invented citations.
