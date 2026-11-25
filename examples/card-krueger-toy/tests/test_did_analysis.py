from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from did_analysis import (
    CODE_TO_EXHIBIT,
    DEFAULT_DATA_PATH,
    NUMERICAL_TOLERANCE,
    TOY_ESTIMAND,
    estimate_difference_in_differences,
    load_fast_food_data,
    make_group_means,
    render_replication_note,
    sensitivity_drop_one_store,
    validate_balanced_panel,
    validate_merge_cardinality,
    validate_output_schema,
    validate_sample_restriction,
    validate_unique_identifiers,
)


FAULTS = Path(__file__).resolve().parents[1] / "faults"
REPO_ROOT = Path(__file__).resolve().parents[3]


def test_load_fast_food_data_adds_teaching_indicators() -> None:
    data = load_fast_food_data(DEFAULT_DATA_PATH)

    assert len(data) == 24
    assert {"post", "treated"}.issubset(data.columns)
    assert set(data["state"]) == {"NJ", "PA"}
    assert set(data["wave"]) == {"before", "after"}


def test_validate_balanced_panel_rejects_missing_wave() -> None:
    data = load_fast_food_data(DEFAULT_DATA_PATH)
    incomplete = data.loc[~((data["store_id"] == "NJ01") & (data["wave"] == "after"))]

    with pytest.raises(ValueError, match="before/after pair"):
        validate_balanced_panel(incomplete)


def test_make_group_means_reports_expected_cells() -> None:
    data = load_fast_food_data(DEFAULT_DATA_PATH)
    means = make_group_means(data)

    assert len(means) == 4
    nj_before = means.loc[
        (means["state"] == "NJ") & (means["wave"] == "before"), "mean_fte_employment"
    ].iloc[0]
    pa_after = means.loc[
        (means["state"] == "PA") & (means["wave"] == "after"), "mean_fte_employment"
    ].iloc[0]

    assert nj_before == pytest.approx(23.3333333333, abs=NUMERICAL_TOLERANCE)
    assert pa_after == pytest.approx(23.0, abs=NUMERICAL_TOLERANCE)


def test_estimate_difference_in_differences_returns_known_toy_result() -> None:
    data = load_fast_food_data(DEFAULT_DATA_PATH)
    result = estimate_difference_in_differences(data)

    assert result.observations == 24
    assert result.treated_stores == 6
    assert result.comparison_stores == 6
    assert result.nj_change == pytest.approx(2.0, abs=NUMERICAL_TOLERANCE)
    assert result.pa_change == pytest.approx(-1.0, abs=NUMERICAL_TOLERANCE)
    assert result.did == pytest.approx(3.0, abs=NUMERICAL_TOLERANCE)
    assert result.weights is None
    assert result.variance_estimator is None
    assert result.clustering is None
    assert result.seed is None


def test_render_replication_note_keeps_research_caveat_visible() -> None:
    result = estimate_difference_in_differences(load_fast_food_data(DEFAULT_DATA_PATH))
    note = render_replication_note(result)

    assert "synthetic teaching CSV" in note
    assert "full-time-equivalent workers" in note
    assert "does not certify a causal claim" in note
    assert "Weights: none" in note
    assert "Do not report precision or significance" in note


def test_loader_rejects_unexpected_state(tmp_path: Path) -> None:
    bad_data = pd.DataFrame(
        {
            "store_id": ["X01", "X01"],
            "state": ["XX", "XX"],
            "wave": ["before", "after"],
            "fte_employment": [10, 11],
        }
    )
    csv_path = tmp_path / "bad.csv"
    bad_data.to_csv(csv_path, index=False)

    with pytest.raises(ValueError, match="Unexpected states"):
        load_fast_food_data(csv_path)


def test_duplicate_store_wave_fault_fails_unique_id_check() -> None:
    with pytest.raises(ValueError, match="Duplicate store-wave"):
        load_fast_food_data(FAULTS / "duplicate_store_wave.csv")


def test_unbalanced_panel_fault_fails_sample_restriction() -> None:
    data = pd.read_csv(FAULTS / "unbalanced_panel.csv")
    data["post"] = (data["wave"] == "after").astype(int)
    data["treated"] = (data["state"] == "NJ").astype(int)

    with pytest.raises(ValueError, match="before/after pair"):
        validate_sample_restriction(data)


def test_chain_table_fault_fails_merge_cardinality() -> None:
    left = pd.DataFrame({"store_id": ["NJ01", "PA01"]})
    right = pd.read_csv(FAULTS / "chain_many_to_many.csv")

    with pytest.raises(ValueError, match="Merge cardinality error"):
        validate_merge_cardinality(left, right, key="store_id", expected="many_to_one")


def test_citation_mismatch_fixture_is_not_a_research_claim() -> None:
    planted = (FAULTS / "citation_mismatch.md").read_text(encoding="utf-8")
    bibliography = (REPO_ROOT / "references" / "bibliography.bib").read_text(encoding="utf-8")

    assert "False claim" in planted
    assert "toy CSV in this repository is not this paper's data" in bibliography


def test_undocumented_restriction_fixture_names_the_missing_pa_group() -> None:
    planted = (FAULTS / "undocumented_restriction.md").read_text(encoding="utf-8")

    assert "Pennsylvania" in planted
    assert "provenance" in planted.lower()


def test_estimand_and_code_map_are_documented() -> None:
    assert TOY_ESTIMAND["weights"] is None
    assert TOY_ESTIMAND["variance_estimator"] is None
    assert "Not an ATT" in TOY_ESTIMAND["label"]
    assert CODE_TO_EXHIBIT["group_means_table"] == "make_group_means"


def test_output_schema_and_descriptive_sensitivity() -> None:
    data = load_fast_food_data(DEFAULT_DATA_PATH)
    means = make_group_means(data)
    result = estimate_difference_in_differences(data)
    validate_output_schema(result, means)
    validate_unique_identifiers(data)

    sensitivity = sensitivity_drop_one_store(data)
    assert sensitivity["min_did"] == pytest.approx(3.0, abs=NUMERICAL_TOLERANCE)
    assert sensitivity["max_did"] == pytest.approx(3.0, abs=NUMERICAL_TOLERANCE)
