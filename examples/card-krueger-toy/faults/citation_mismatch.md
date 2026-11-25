# Citation mismatch (planted)

False claim for the `literature-mapper` Skill (a written procedure) exercise:

> Card and Krueger (1994, table 3) report a +3.0 FTE difference-in-differences
> using `examples/card-krueger-toy/data/toy_fast_food.csv`.

Why this fails verification:

- Card and Krueger (1994) survey 410 fast-food restaurants rather than using this 24-row CSV.
- The +3.0 FTE figure comes from the synthetic teaching dataset, not the 1994 article.
- In `references/bibliography.bib`, `card1994minimum` cites the published article, not the toy file.

Ledger decision: rewrite or drop the claim.
