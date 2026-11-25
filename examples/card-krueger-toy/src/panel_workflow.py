"""Synthetic panel cleaning, store-clustered DiD, and LaTeX table checks.

The CSV inputs in ``examples/card-krueger-toy/data/`` are synthetic teaching data.
They are not Card and Krueger (1994) survey microdata, and passing checks here
confirms code-to-table reproduction only, never causal identification.
"""

from __future__ import annotations

import math
from pathlib import Path
import re

import numpy as np
import pandas as pd

from did_analysis import (
    EXPECTED_STATES,
    EXPECTED_WAVES,
    PROJECT_ROOT,
    validate_balanced_panel,
    validate_merge_cardinality,
    validate_unique_identifiers,
)


DEFAULT_EXTRACT_PATH = PROJECT_ROOT / "data" / "messy_fast_food_extract.csv"
DEFAULT_CHAIN_PATH = PROJECT_ROOT / "data" / "chain_metadata.csv"

EXTRACT_REQUIRED_COLUMNS = {
    "store_id",
    "state",
    "wave",
    "status",
    "ft_workers",
    "pt_workers",
    "managers",
    "starting_wage",
    "chain_id",
}
CHAIN_REQUIRED_COLUMNS = {"chain_id", "chain_name", "company_owned"}
ALLOWED_STATUSES = {"open", "temp_closed", "perm_closed", "refused"}
OPEN_REQUIRED_NUMERIC = ["ft_workers", "pt_workers", "managers", "starting_wage"]
ROBUSTNESS_COLUMNS = [
    "spec_id",
    "specification",
    "did_estimate",
    "se_store_cluster",
    "n_obs",
    "n_stores",
]


def clean_messy_extract(
    extract_path: str | Path = DEFAULT_EXTRACT_PATH,
    chain_path: str | Path = DEFAULT_CHAIN_PATH,
    *,
    fte_pt_weight: float = 0.5,
    include_perm_closed: bool = False,
) -> tuple[pd.DataFrame, dict[str, int]]:
    """Clean the synthetic two-wave fast-food extract and record sample counts at each step.

    Args:
        extract_path: Path to the store-wave extract CSV (never modified).
        chain_path: Path to the chain metadata CSV (never modified).
        fte_pt_weight: Weight placed on part-time workers in FTE employment.
        include_perm_closed: Whether permanently closed stores are kept at FTE = 0.0.

    Returns:
        Tuple ``(cleaned_df, waterfall)`` with standardized balanced panel rows and
        step-by-step row and store counts.
    """
    if not math.isfinite(fte_pt_weight) or fte_pt_weight < 0.0 or fte_pt_weight > 1.0:
        raise ValueError(f"fte_pt_weight must lie in [0, 1], got {fte_pt_weight}")

    raw_df = pd.read_csv(extract_path)
    chains = pd.read_csv(chain_path)

    missing_extract = EXTRACT_REQUIRED_COLUMNS - set(raw_df.columns)
    if missing_extract:
        raise ValueError(f"Extract missing required columns: {sorted(missing_extract)}")

    missing_chain = CHAIN_REQUIRED_COLUMNS - set(chains.columns)
    if missing_chain:
        raise ValueError(f"Chain metadata missing required columns: {sorted(missing_chain)}")

    raw_rows = int(len(raw_df))

    df = raw_df.copy()
    df["store_id"] = df["store_id"].astype(str).str.strip()
    df["state"] = df["state"].astype(str).str.strip().str.upper()
    df["wave"] = df["wave"].astype(str).str.strip().str.lower()
    df["status"] = df["status"].astype(str).str.strip().str.lower()

    invalid_states = set(df["state"]) - EXPECTED_STATES
    if invalid_states:
        raise ValueError(f"Unexpected states after standardization: {sorted(invalid_states)}")

    invalid_waves = set(df["wave"]) - EXPECTED_WAVES
    if invalid_waves:
        raise ValueError(f"Unexpected waves after standardization: {sorted(invalid_waves)}")

    invalid_statuses = set(df["status"]) - ALLOWED_STATUSES
    if invalid_statuses:
        raise ValueError(f"Unexpected interview statuses: {sorted(invalid_statuses)}")

    validate_unique_identifiers(df)
    validate_merge_cardinality(df, chains, key="chain_id", expected="many_to_one")

    unmatched_chains = set(df["chain_id"]) - set(chains["chain_id"])
    if unmatched_chains:
        raise ValueError(f"Unmatched chain_id values in extract: {sorted(unmatched_chains)}")

    merged = df.merge(chains, on="chain_id", how="left")

    kept_statuses = {"open", "perm_closed"} if include_perm_closed else {"open"}
    status_filtered = merged.loc[merged["status"].isin(kept_statuses)].copy()
    after_status_filter = int(len(status_filtered))

    is_perm_closed = status_filtered["status"] == "perm_closed"
    open_complete = ~status_filtered[OPEN_REQUIRED_NUMERIC].isna().any(axis=1)
    perm_closed_valid = is_perm_closed & (
        (status_filtered["wave"] == "after")
        | (~status_filtered["starting_wage"].isna())
    )
    missing_filtered = status_filtered.loc[open_complete | perm_closed_valid].copy()
    after_missing_filter = int(len(missing_filtered))

    open_fte = (
        missing_filtered["ft_workers"].fillna(0.0)
        + missing_filtered["managers"].fillna(0.0)
        + fte_pt_weight * missing_filtered["pt_workers"].fillna(0.0)
    )
    missing_filtered["fte_employment"] = np.where(
        missing_filtered["status"] == "perm_closed",
        0.0,
        open_fte,
    ).astype(float)

    waves_by_store = missing_filtered.groupby("store_id")["wave"].agg(set)
    balanced_ids = sorted(
        store_id for store_id, waves in waves_by_store.items() if waves == EXPECTED_WAVES
    )
    balanced = missing_filtered.loc[missing_filtered["store_id"].isin(balanced_ids)].copy()

    before_wages = balanced.loc[balanced["wave"] == "before"].set_index("store_id")[
        "starting_wage"
    ]
    if before_wages.isna().any():
        bad_stores = sorted(before_wages[before_wages.isna()].index)
        raise ValueError(f"Missing baseline starting_wage for stores: {bad_stores}")

    validate_balanced_panel(balanced)
    balanced["baseline_starting_wage"] = balanced["store_id"].map(before_wages).astype(float)
    balanced["treated"] = (balanced["state"] == "NJ").astype(int)
    balanced["post"] = (balanced["wave"] == "after").astype(int)
    balanced["treated_post"] = balanced["treated"] * balanced["post"]
    balanced["company_owned"] = balanced["company_owned"].astype(int)

    cleaned_df = balanced.sort_values(["state", "store_id", "post"]).reset_index(drop=True)
    waterfall = {
        "raw_rows": raw_rows,
        "after_status_filter": after_status_filter,
        "after_missing_filter": after_missing_filter,
        "balanced_panel_rows": int(len(cleaned_df)),
        "balanced_stores": int(cleaned_df["store_id"].nunique()),
    }
    return cleaned_df, waterfall


def estimate_panel_did(
    data: pd.DataFrame,
    *,
    add_controls: bool = False,
) -> dict[str, float | int | str]:
    """Estimate linear DiD with Liang-Zeger store-clustered HC1 standard errors.

    Args:
        data: Balanced two-wave store panel from ``clean_messy_extract``.
        add_controls: Include ``company_owned`` and baseline ``starting_wage`` controls.

    Returns:
        Dictionary with point estimate, store-clustered SE, sample counts, state
        cluster count, and few-cluster econometric warning.
    """
    validate_balanced_panel(data)

    work = data.copy()
    if "treated" not in work.columns:
        work["treated"] = (work["state"] == "NJ").astype(int)
    if "post" not in work.columns:
        work["post"] = (work["wave"] == "after").astype(int)
    if "treated_post" not in work.columns:
        work["treated_post"] = work["treated"] * work["post"]

    regressors = ["treated", "post", "treated_post"]
    if add_controls:
        if "company_owned" not in work.columns:
            raise ValueError("add_controls=True requires 'company_owned' in data")
        if "baseline_starting_wage" not in work.columns:
            if "starting_wage" not in work.columns:
                raise ValueError(
                    "add_controls=True requires 'baseline_starting_wage' or 'starting_wage'"
                )
            before_wages = work.loc[work["wave"] == "before"].set_index("store_id")[
                "starting_wage"
            ]
            work["baseline_starting_wage"] = work["store_id"].map(before_wages).astype(float)
        regressors.extend(["company_owned", "baseline_starting_wage"])

    n_obs = int(len(work))
    y = work["fte_employment"].to_numpy(dtype=float)
    x_cols = [np.ones(n_obs, dtype=float)] + [
        work[col].to_numpy(dtype=float) for col in regressors
    ]
    x_mat = np.column_stack(x_cols)
    if not np.all(np.isfinite(y)) or not np.all(np.isfinite(x_mat)):
        raise ValueError("Non-finite values in panel DiD regression inputs")
    n_params = int(x_mat.shape[1])

    store_codes, cluster_idx = np.unique(work["store_id"].to_numpy(), return_inverse=True)
    n_stores = int(len(store_codes))
    if n_stores <= 1 or n_obs <= n_params:
        raise ValueError("Insufficient degrees of freedom for store-clustered inference")

    beta_hat, _, rank, _ = np.linalg.lstsq(x_mat, y, rcond=None)
    if rank < n_params:
        raise ValueError("Design matrix is rank-deficient in estimate_panel_did")

    residuals = y - x_mat @ beta_hat

    meat = np.zeros((n_params, n_params), dtype=float)
    for g in range(n_stores):
        mask = cluster_idx == g
        score_g = x_mat[mask].T @ residuals[mask]
        meat += np.outer(score_g, score_g)

    xtx_inv = np.linalg.inv(x_mat.T @ x_mat)
    hc1_scale = (n_stores / (n_stores - 1.0)) * ((n_obs - 1.0) / (n_obs - n_params))
    vcov_cluster = hc1_scale * (xtx_inv @ meat @ xtx_inv)

    did_idx = 3
    did_estimate = float(beta_hat[did_idx])
    se_store_cluster = float(np.sqrt(max(0.0, vcov_cluster[did_idx, did_idx])))

    n_state_clusters = int(work["state"].nunique())
    inference_warning = ""
    if n_state_clusters < 10:
        inference_warning = (
            f"Caution: policy varies across G={n_state_clusters} state clusters; "
            "store-clustered SEs do not account for state-level common shocks. "
            "A researcher must choose the inference method; synthetic teaching data, not causal."
        )

    return {
        "did_estimate": did_estimate,
        "se_store_cluster": se_store_cluster,
        "n_obs": n_obs,
        "n_stores": n_stores,
        "n_state_clusters": n_state_clusters,
        "inference_warning": inference_warning,
    }


def run_robustness_suite(
    extract_path: str | Path = DEFAULT_EXTRACT_PATH,
    chain_path: str | Path = DEFAULT_CHAIN_PATH,
) -> pd.DataFrame:
    """Run four synthetic panel DiD specifications across cleaning and control choices."""
    configs = [
        (
            "baseline_open",
            "Balanced open stores (0.5 PT weight)",
            0.5,
            False,
            False,
        ),
        (
            "with_controls",
            "Balanced open + chain and baseline-wage controls",
            0.5,
            False,
            True,
        ),
        (
            "with_perm_closed",
            "Balanced open + permanently closed (FTE = 0)",
            0.5,
            True,
            False,
        ),
        (
            "pt_weight_025",
            "Alternative FTE formula (0.25 PT weight)",
            0.25,
            False,
            False,
        ),
    ]

    rows: list[dict[str, float | int | str]] = []
    for spec_id, label, pt_weight, include_closed, add_controls in configs:
        panel, _ = clean_messy_extract(
            extract_path,
            chain_path,
            fte_pt_weight=pt_weight,
            include_perm_closed=include_closed,
        )
        est = estimate_panel_did(panel, add_controls=add_controls)
        rows.append(
            {
                "spec_id": spec_id,
                "specification": label,
                "did_estimate": float(est["did_estimate"]),
                "se_store_cluster": float(est["se_store_cluster"]),
                "n_obs": int(est["n_obs"]),
                "n_stores": int(est["n_stores"]),
            }
        )

    return pd.DataFrame(rows, columns=ROBUSTNESS_COLUMNS)


def _short_column_header(spec_id: str, index: int) -> str:
    labels = {
        "baseline_open": "Baseline open",
        "with_controls": "With controls",
        "with_perm_closed": r"Perm.\ closed",
        "pt_weight_025": "PT wt 0.25",
    }
    if spec_id in labels:
        return labels[spec_id]
    escaped = (
        spec_id.replace("\\", r"\textbackslash{}")
        .replace("_", r"\_")
        .replace("&", r"\&")
        .replace("%", r"\%")
    )
    return f"Spec {index} ({escaped})"


def render_latex_booktabs_table(specs: pd.DataFrame) -> str:
    """Render a star-free LaTeX booktabs snippet from ``run_robustness_suite``."""
    missing = set(ROBUSTNESS_COLUMNS) - set(specs.columns)
    if missing:
        raise ValueError(f"Specs DataFrame missing required columns: {sorted(missing)}")
    if specs.empty:
        raise ValueError("Specs DataFrame must contain at least one specification")

    n_cols = len(specs)
    align = "l" + "c" * n_cols
    col_numbers = " & ".join(f"({idx})" for idx in range(1, n_cols + 1))
    col_titles = " & ".join(
        _short_column_header(str(row["spec_id"]), idx)
        for idx, (_, row) in enumerate(specs.iterrows(), start=1)
    )
    estimates = " & ".join(f"{float(val):.2f}" for val in specs["did_estimate"])
    ses = " & ".join(f"({float(val):.2f})" for val in specs["se_store_cluster"])
    obs = " & ".join(f"{int(val)}" for val in specs["n_obs"])
    stores = " & ".join(f"{int(val)}" for val in specs["n_stores"])

    total_cols = n_cols + 1
    note_text = (
        r"\footnotesize \textit{Notes:} Synthetic teaching data; not Card and Krueger "
        r"(1994) microdata and not a causal estimate. Store-clustered HC1 standard errors "
        r"in parentheses; policy varies across $G=2$ state clusters, so store clustering "
        r"does not address state-level shocks. No significance stars are reported."
    )

    lines = [
        rf"\begin{{tabular}}{{{align}}}",
        r"\toprule",
        rf" & {col_numbers} \\",
        rf" & {col_titles} \\",
        r"\midrule",
        rf"NJ $\times$ Post (DiD) & {estimates} \\",
        rf" & {ses} \\",
        r"\midrule",
        rf"Observations & {obs} \\",
        rf"Stores & {stores} \\",
        r"\bottomrule",
        rf"\multicolumn{{{total_cols}}}{{p{{0.94\linewidth}}}}{{{note_text}}} \\",
        r"\end{tabular}",
    ]
    return "\n".join(lines)


def _split_latex_cells(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.endswith(r"\\"):
        stripped = stripped[:-2]
    return [cell.strip() for cell in stripped.split("&")]


def verify_latex_table_numbers(
    latex_table: str,
    specs: pd.DataFrame,
    *,
    tol: float = 0.01,
) -> None:
    """Verify that a LaTeX booktabs table matches ``specs`` and preserves caveats.

    Raises:
        ValueError: With prefix ``"LaTeX table drift"`` on any numeric mismatch,
            star annotation, or missing synthetic/cluster caveat.
    """
    if not math.isfinite(tol) or tol < 0.0:
        raise ValueError(
            f"LaTeX table drift: tolerance tol must be finite and >= 0, got {tol}"
        )

    lowered = latex_table.lower()
    if "synthetic teaching data" not in lowered:
        raise ValueError("LaTeX table drift: missing 'synthetic teaching data' caveat")
    if "g=2" not in lowered and "state cluster" not in lowered:
        raise ValueError("LaTeX table drift: missing G=2 state-cluster caveat")

    lines = [line.strip() for line in latex_table.splitlines() if line.strip()]
    did_line: str | None = None
    se_line: str | None = None
    obs_line: str | None = None
    stores_line: str | None = None

    for idx, line in enumerate(lines):
        if "(DiD)" in line or line.startswith(r"NJ $\times$ Post"):
            did_line = line
            if idx + 1 < len(lines):
                se_line = lines[idx + 1]
        elif line.startswith("Observations"):
            obs_line = line
        elif line.startswith("Stores"):
            stores_line = line

    if did_line is None or se_line is None or obs_line is None or stores_line is None:
        raise ValueError(
            "LaTeX table drift: missing required DiD, SE, Observations, or Stores row"
        )

    if "*" in did_line or "*" in se_line:
        raise ValueError(
            "LaTeX table drift: significance stars are forbidden on synthetic data"
        )

    n_expected = len(specs)
    did_cells = _split_latex_cells(did_line)[1:]
    se_cells = _split_latex_cells(se_line)[1:]
    obs_cells = _split_latex_cells(obs_line)[1:]
    store_cells = _split_latex_cells(stores_line)[1:]

    for label, cells in (
        ("DiD estimates", did_cells),
        ("standard errors", se_cells),
        ("Observations", obs_cells),
        ("Stores", store_cells),
    ):
        if len(cells) != n_expected:
            raise ValueError(
                f"LaTeX table drift: expected {n_expected} {label} cells, found {len(cells)}"
            )

    for col_idx, (_, row) in enumerate(specs.iterrows()):
        spec_id = row["spec_id"]
        try:
            parsed_did = float(did_cells[col_idx])
        except ValueError as exc:
            raise ValueError(
                f"LaTeX table drift: unparseable DiD cell {did_cells[col_idx]!r} for {spec_id}"
            ) from exc

        if not math.isfinite(parsed_did):
            raise ValueError(
                f"LaTeX table drift: non-finite DiD cell {did_cells[col_idx]!r} for {spec_id}"
            )

        se_match = re.fullmatch(r"\(([+-]?\d+(?:\.\d+)?)\)", se_cells[col_idx])
        if se_match is None:
            raise ValueError(
                f"LaTeX table drift: malformed parenthesized SE {se_cells[col_idx]!r} "
                f"for {spec_id}"
            )
        parsed_se = float(se_match.group(1))
        if not math.isfinite(parsed_se):
            raise ValueError(
                f"LaTeX table drift: non-finite SE cell {se_cells[col_idx]!r} for {spec_id}"
            )

        try:
            parsed_obs = int(obs_cells[col_idx])
            parsed_stores = int(store_cells[col_idx])
        except ValueError as exc:
            raise ValueError(
                f"LaTeX table drift: non-integer count cell for {spec_id}"
            ) from exc

        expected_did = float(row["did_estimate"])
        expected_se = float(row["se_store_cluster"])
        expected_obs_raw = float(row["n_obs"])
        expected_stores_raw = float(row["n_stores"])
        if not (
            math.isfinite(expected_did)
            and math.isfinite(expected_se)
            and math.isfinite(expected_obs_raw)
            and math.isfinite(expected_stores_raw)
        ):
            raise ValueError(
                f"LaTeX table drift: non-finite expected spec value for {spec_id}"
            )
        expected_obs = int(row["n_obs"])
        expected_stores = int(row["n_stores"])

        if abs(parsed_did - expected_did) > tol:
            raise ValueError(
                f"LaTeX table drift: {spec_id} DiD {parsed_did:.2f} != "
                f"{expected_did:.4f} (tol={tol})"
            )
        if abs(parsed_se - expected_se) > tol:
            raise ValueError(
                f"LaTeX table drift: {spec_id} SE {parsed_se:.2f} != "
                f"{expected_se:.4f} (tol={tol})"
            )
        if abs(parsed_obs - expected_obs) > tol:
            raise ValueError(
                f"LaTeX table drift: {spec_id} Observations {parsed_obs} != {expected_obs}"
            )
        if abs(parsed_stores - expected_stores) > tol:
            raise ValueError(
                f"LaTeX table drift: {spec_id} Stores {parsed_stores} != {expected_stores}"
            )


def main() -> None:
    """Run panel cleaning, four DiD specifications, and the LaTeX table check."""
    cleaned, waterfall = clean_messy_extract()
    baseline = estimate_panel_did(cleaned, add_controls=False)
    specs = run_robustness_suite()
    latex_table = render_latex_booktabs_table(specs)
    verify_latex_table_numbers(latex_table, specs)

    print("Sample attrition counts (open balanced panel)")
    print("=============================================")
    for stage, count in waterfall.items():
        print(f"  {stage}: {count}")
    print()

    print("Four-specification robustness table (synthetic teaching data)")
    print("=============================================================")
    print(specs.to_string(index=False, float_format=lambda val: f"{val:.3f}"))
    print()

    print("Econometric inference check")
    print("===========================")
    print(f"  {baseline['inference_warning']}")
    print()

    print("Verified LaTeX booktabs table (code-to-table checked)")
    print("=====================================================")
    print(latex_table)


if __name__ == "__main__":
    main()
