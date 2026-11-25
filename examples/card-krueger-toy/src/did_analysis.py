"""Synthetic difference-in-differences teaching example for EIEF / Luiss."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "toy_fast_food.csv"
REQUIRED_COLUMNS = {"store_id", "state", "wave", "fte_employment"}
EXPECTED_STATES = {"NJ", "PA"}
EXPECTED_WAVES = {"before", "after"}
NUMERICAL_TOLERANCE = 1e-9
GROUP_MEANS_COLUMNS = ("state", "wave", "mean_fte_employment")
CODE_TO_EXHIBIT = {
    "group_means_table": "make_group_means",
    "toy_2x2_contrast": "estimate_difference_in_differences",
    "replication_note": "render_replication_note",
}
TOY_ESTIMAND = {
    "name": "unweighted_2x2_mean_difference",
    "outcome": "fte_employment",
    "treated_group": "NJ",
    "comparison_group": "PA",
    "pre_wave": "before",
    "post_wave": "after",
    "weights": None,
    "variance_estimator": None,
    "clustering": None,
    "seed": None,
    "numerical_tolerance": NUMERICAL_TOLERANCE,
    "label": (
        "Descriptive teaching contrast of mean FTE changes. "
        "Not an ATT estimate, not causal, and not a statement of precision."
    ),
}


@dataclass(frozen=True)
class DidResult:
    """Compact difference-in-differences result for the toy example."""

    nj_change: float
    pa_change: float
    did: float
    observations: int
    treated_stores: int
    comparison_stores: int
    weights: None = None
    variance_estimator: None = None
    clustering: None = None
    seed: None = None


def load_fast_food_data(csv_path: str | Path = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """Load the synthetic fast-food panel and add teaching indicators."""

    data = pd.read_csv(csv_path)
    missing = REQUIRED_COLUMNS - set(data.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")

    if data[list(REQUIRED_COLUMNS)].isna().any().any():
        raise ValueError("Dataset contains missing values in required columns")

    invalid_states = set(data["state"]) - EXPECTED_STATES
    if invalid_states:
        raise ValueError(f"Unexpected states: {sorted(invalid_states)}")

    invalid_waves = set(data["wave"]) - EXPECTED_WAVES
    if invalid_waves:
        raise ValueError(f"Unexpected waves: {sorted(invalid_waves)}")

    cleaned = data.copy()
    cleaned["post"] = (cleaned["wave"] == "after").astype(int)
    cleaned["treated"] = (cleaned["state"] == "NJ").astype(int)
    validate_unique_identifiers(cleaned)
    validate_treatment_timing(cleaned)
    return cleaned.sort_values(["state", "store_id", "post"]).reset_index(drop=True)


def validate_unique_identifiers(data: pd.DataFrame) -> None:
    """Require unique store-wave rows."""

    duplicated_rows = data.duplicated(["store_id", "wave"])
    if duplicated_rows.any():
        duplicated = sorted(data.loc[duplicated_rows, "store_id"].unique())
        raise ValueError(f"Duplicate store-wave observations: {duplicated}")


def validate_balanced_panel(data: pd.DataFrame) -> None:
    """Check that each store has one before and one after observation."""

    validate_unique_identifiers(data)

    unbalanced = [
        store_id
        for store_id, waves in data.groupby("store_id")["wave"].agg(set).items()
        if waves != EXPECTED_WAVES
    ]
    if unbalanced:
        raise ValueError(f"Stores without a before/after pair: {sorted(unbalanced)}")

    changing_state = data.groupby("store_id")["state"].nunique()
    bad_state = sorted(changing_state[changing_state != 1].index)
    if bad_state:
        raise ValueError(f"Stores assigned to multiple states: {bad_state}")


def validate_treatment_timing(data: pd.DataFrame) -> None:
    """Treated means NJ; post means the after wave; assignment does not switch."""

    if not data["post"].eq(data["wave"].eq("after").astype(int)).all():
        raise ValueError("Treatment timing mismatch: post must equal the after wave")
    if not data["treated"].eq(data["state"].eq("NJ").astype(int)).all():
        raise ValueError("Treatment assignment mismatch: treated must equal NJ")
    changing_treated = data.groupby("store_id")["treated"].nunique()
    bad_treated = sorted(changing_treated[changing_treated != 1].index)
    if bad_treated:
        raise ValueError(f"Stores with changing treatment assignment: {bad_treated}")


def validate_sample_restriction(data: pd.DataFrame) -> None:
    """Stores in NJ or PA with exactly one before and one after observation."""

    validate_balanced_panel(data)
    extra_states = set(data["state"]) - EXPECTED_STATES
    if extra_states:
        raise ValueError(f"Sample restriction violated; unexpected states: {sorted(extra_states)}")


def validate_merge_cardinality(
    left: pd.DataFrame,
    right: pd.DataFrame,
    *,
    key: str,
    expected: str = "many_to_one",
) -> None:
    """Reject undeclared many-to-many merges on a store or chain key."""

    allowed = {"one_to_one", "many_to_one"}
    if expected not in allowed:
        raise ValueError(f"Unsupported merge cardinality: {expected}")
    if key not in left.columns or key not in right.columns:
        raise ValueError(f"Merge key missing: {key}")
    right_unique = not right.duplicated(key).any()
    left_unique = not left.duplicated(key).any()
    if expected == "many_to_one" and not right_unique:
        raise ValueError(f"Merge cardinality error: {key} is not unique on the right")
    if expected == "one_to_one" and not (left_unique and right_unique):
        raise ValueError(f"Merge cardinality error: {key} is not unique on both sides")


def validate_output_schema(result: DidResult, means: pd.DataFrame) -> None:
    """Check that the summary table and result match the documented columns and fields."""

    missing = [column for column in GROUP_MEANS_COLUMNS if column not in means.columns]
    if missing:
        raise ValueError(f"Group-means table missing columns: {missing}")
    if result.weights is not None or result.variance_estimator is not None:
        raise ValueError("Toy result must not report weights or a variance estimator")
    if result.clustering is not None or result.seed is not None:
        raise ValueError("Toy result must not report clustering or a seed")


def make_group_means(data: pd.DataFrame) -> pd.DataFrame:
    """Return mean full-time-equivalent employment by state and wave."""

    validate_sample_restriction(data)
    means = (
        data.groupby(["state", "wave"], as_index=False)["fte_employment"]
        .mean()
        .rename(columns={"fte_employment": "mean_fte_employment"})
    )
    means["wave_order"] = means["wave"].map({"before": 0, "after": 1})
    return means.sort_values(["state", "wave_order"]).drop(columns="wave_order")


def _mean_for(data: pd.DataFrame, state: str, wave: str) -> float:
    mask = (data["state"] == state) & (data["wave"] == wave)
    return float(data.loc[mask, "fte_employment"].mean())


def estimate_difference_in_differences(data: pd.DataFrame) -> DidResult:
    """Estimate the simple NJ-versus-PA before/after comparison."""

    validate_sample_restriction(data)

    nj_change = _mean_for(data, "NJ", "after") - _mean_for(data, "NJ", "before")
    pa_change = _mean_for(data, "PA", "after") - _mean_for(data, "PA", "before")

    return DidResult(
        nj_change=nj_change,
        pa_change=pa_change,
        did=nj_change - pa_change,
        observations=len(data),
        treated_stores=int(data.loc[data["state"] == "NJ", "store_id"].nunique()),
        comparison_stores=int(data.loc[data["state"] == "PA", "store_id"].nunique()),
    )


def sensitivity_drop_one_store(data: pd.DataFrame) -> dict[str, float]:
    """Descriptive range when dropping one store. Not a standard error."""

    validate_sample_restriction(data)
    estimates: list[float] = []
    for store_id in sorted(data["store_id"].unique()):
        subset = data.loc[data["store_id"] != store_id]
        estimates.append(estimate_difference_in_differences(subset).did)
    return {
        "min_did": min(estimates),
        "max_did": max(estimates),
        "n_stores_dropped": 1.0,
    }


def render_replication_note(result: DidResult) -> str:
    """Document source, transformations, units, restrictions, and caveats."""

    return "\n".join(
        [
            "# Card-Krueger Toy Example",
            "",
            "Data source: synthetic teaching CSV in examples/card-krueger-toy/data/toy_fast_food.csv.",
            "Unit: store-wave observation; employment is full-time-equivalent workers.",
            "Sample restriction: stores with one before and one after observation in NJ or PA.",
            "Estimand: unweighted 2x2 difference in mean FTE changes (NJ minus PA).",
            "Weights: none. Variance estimator: none. Clustering: none. Seed: none.",
            "Transformation: created treated and post indicators and compared mean changes.",
            f"NJ change: {result.nj_change:.1f} FTE workers.",
            f"PA change: {result.pa_change:.1f} FTE workers.",
            f"Toy DID estimate: {result.did:.1f} FTE workers.",
            "Research caveat: this is not Card and Krueger's raw data and does not certify a causal claim.",
            "Do not report precision or significance for this teaching contrast.",
        ]
    )


def main() -> None:
    """Run the toy analysis and print a compact replication note."""

    data = load_fast_food_data()
    means = make_group_means(data)
    result = estimate_difference_in_differences(data)
    validate_output_schema(result, means)

    print("Group means")
    print("===========")
    print(means.to_string(index=False))
    print()
    print(render_replication_note(result))


if __name__ == "__main__":
    main()
