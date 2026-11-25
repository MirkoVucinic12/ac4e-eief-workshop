# Data notes: Card–Krueger toy panel

Where the data come from, what each column means, and every rule that drops stores.
The issue card `ck-data-cleaning` and the `data-reviewer` sub-agent check this file.

**All files in `data/` are synthetic teaching data.** They are hand-written, not
Card and Krueger's (1994) survey, and they support no research or causal claim.
Never edit them.

## Clean panel: `data/toy_fast_food.csv`

- **Source:** hand-written synthetic file, 24 rows.
- **Unit:** one store in one survey wave.
- **Columns:** `store_id`; `state` (`NJ` or `PA`); `wave` (`before` or `after`);
  `fte_employment` (full-time-equivalent workers).
- **Groups:** NJ stores are the treatment group (6 stores); eastern PA stores are
  the comparison group (6 stores).
- **Timing:** `before` and `after` New Jersey's April 1992 minimum wage increase.
- **Sample restriction:** keep stores with exactly one `before` and one `after` row
  and no missing employment. All 12 stores pass, so nothing is dropped.
- **Estimate:** NJ change in mean FTE minus PA change in mean FTE, unweighted, with
  no standard errors.
- **Script:** `src/did_analysis.py` prints NJ change 2.0, PA change −1.0, toy DiD 3.0.

## Messy extract: `data/messy_fast_food_extract.csv` and `data/chain_metadata.csv`

- **Source:** hand-written synthetic survey extract, 47 rows for 24 stores (14 NJ,
  10 PA), plus a lookup table of 4 chains.
- **Quirks on purpose:** mixed capitals and spaces in `state` and `status`; four
  interview outcomes (`open`, `temp_closed`, `perm_closed`, `refused`); one missing
  worker count; one store interviewed only once.
- **Employment:** `fte_employment = ft_workers + managers + 0.5 × pt_workers`.
  One version uses 0.25 on part-time workers. A permanently closed store counts as 0
  when it is kept.
- **Chain merge:** each store matches exactly one chain (many stores to one chain).
  The script stops if a store matches more than one.

### Rules that drop stores (`src/panel_workflow.py`)

| Step | Rule | Rows left | Rows dropped (stores) |
| --- | --- | --- | --- |
| Start | All rows | 47 | – |
| 1 | Keep interviews with status `open` | 43 | 4 after-wave rows: NJ11, PA09 (permanently closed), NJ12 (refused), PA10 (temporarily closed) |
| 2 | Keep rows with no missing worker count or starting wage | 42 | 1 after-wave row: NJ13 |
| 3 | Keep stores seen in both waves | 36 (18 stores) | 6 rows that lost their partner wave: NJ11, NJ12, NJ13, NJ14, PA09, PA10 |

The script prints these counts every time it runs. It never drops rows silently.

### Inference warning

Store-clustered standard errors allow for correlation within a store over time.
They do **not** allow for shocks common to a whole state, and there are only two
states. The choice of inference method stays with the researcher.

## Checks run

None recorded yet. The `ck-data-cleaning` card adds the counts it printed, the
command it used and the date here.
