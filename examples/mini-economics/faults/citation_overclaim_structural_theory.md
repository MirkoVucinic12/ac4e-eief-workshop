# Citation and synthetic-moment overclaim (planted)

False claims for the `literature-mapper` Skill (a written procedure) exercise on structural and theory drafts:

> 1. Myerson (1981), ``Optimal Auction Design,'' *Mathematics of Operations Research*
>    6(1): 58--73, `doi:10.1287/moor.1981.0058.fake`, proves that high-type
>    individual rationality is slack for every type-dependent outside option
>    $\bar{u}(\theta) = \kappa \theta$ ($\kappa \ge 0$).
> 2. Empirically, US liquid household wealth-to-income is `1.3492` with `20.0%`
>    hand-to-mouth households, as documented in `examples/mini-economics/src/structural_bellman.py`
>    (citing Card and Krueger 1994, `doi:10.1257/aer.84.4.772`).

Why this fails verification:

1. **Invented or unverified DOIs on pre-DOI papers:**
   - The string `10.1287/moor.1981.0058.fake` is invented, and `references/bibliography.bib`
     has no `myerson1981` entry. Finding a paper in search is not verification; never invent
     BibTeX entries or DOIs.
   - `10.1257/aer.84.4.772` is a common AI-invented Crossref DOI for `card1994minimum`. In
     `references/bibliography.bib`, `card1994minimum` points to JSTOR
     (`https://www.jstor.org/stable/2118030`) and RePEc, with **no** Crossref DOI.
2. **Proposition overclaim:** Under type-dependent reservation utilities, countervailing
   incentives make $IR_H$ bind whenever $\kappa > q_L^{std}$.
3. **Synthetic calibration cited as empirical data:** `structural_bellman.py` (`1.3492`
   and `0.2000`) is a synthetic 2-state numerical illustration, not survey microdata.

Ledger decision: record blockers, remove invented DOIs, and rewrite or drop unsupported claims.
