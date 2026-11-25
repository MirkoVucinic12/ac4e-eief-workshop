from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from panel_workflow import (
    DEFAULT_CHAIN_PATH,
    DEFAULT_EXTRACT_PATH,
    ROBUSTNESS_COLUMNS,
    clean_messy_extract,
    estimate_panel_did,
    render_latex_booktabs_table,
    run_robustness_suite,
    verify_latex_table_numbers,
)


FAULTS_DIR = Path(__file__).resolve().parents[1] / "faults"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_clean_messy_extract_waterfall_and_immutability() -> None:
    extract_before = _sha256(DEFAULT_EXTRACT_PATH)
    chain_before = _sha256(DEFAULT_CHAIN_PATH)

    cleaned_open, waterfall_open = clean_messy_extract()
    cleaned_closed, waterfall_closed = clean_messy_extract(include_perm_closed=True)

    assert _sha256(DEFAULT_EXTRACT_PATH) == extract_before
    assert _sha256(DEFAULT_CHAIN_PATH) == chain_before

    assert waterfall_open == {
        "raw_rows": 47,
        "after_status_filter": 43,
        "after_missing_filter": 42,
        "balanced_panel_rows": 36,
        "balanced_stores": 18,
    }
    assert set(cleaned_open["state"]) == {"NJ", "PA"}
    assert set(cleaned_open["wave"]) == {"before", "after"}
    assert set(cleaned_open["status"]) == {"open"}

    assert waterfall_closed == {
        "raw_rows": 47,
        "after_status_filter": 45,
        "after_missing_filter": 44,
        "balanced_panel_rows": 40,
        "balanced_stores": 20,
    }
    perm_rows = cleaned_closed.loc[cleaned_closed["status"] == "perm_closed"]
    assert len(perm_rows) == 2
    assert (perm_rows["fte_employment"] == 0.0).all()


def test_perm_closed_forces_zero_fte_even_with_nonzero_raw_cells(tmp_path: Path) -> None:
    extract = pd.DataFrame(
        {
            "store_id": ["NJ01", "NJ01", "PA01", "PA01"],
            "state": [" nj ", "NJ", "PA", " pa "],
            "wave": ["Before", "AFTER", "before", "after"],
            "status": ["open", "PERM_CLOSED", "open", "open"],
            "ft_workers": [10, 9, 10, 10],
            "pt_workers": [8, 6, 8, 8],
            "managers": [2, 2, 2, 2],
            "starting_wage": [4.25, np.nan, 4.25, 4.25],
            "chain_id": [1, 1, 1, 1],
        }
    )
    extract_csv = tmp_path / "extract.csv"
    extract.to_csv(extract_csv, index=False)

    cleaned, waterfall = clean_messy_extract(
        extract_csv,
        DEFAULT_CHAIN_PATH,
        include_perm_closed=True,
    )
    assert waterfall["balanced_stores"] == 2
    nj_after_fte = cleaned.loc[
        (cleaned["store_id"] == "NJ01") & (cleaned["wave"] == "after"),
        "fte_employment",
    ].iloc[0]
    assert nj_after_fte == 0.0


def test_clean_messy_extract_rejects_duplicate_chain_key(tmp_path: Path) -> None:
    bad_chains = pd.DataFrame(
        {
            "chain_id": [1, 1, 2, 3, 4],
            "chain_name": ["A", "A_dup", "B", "C", "D"],
            "company_owned": [0, 1, 1, 0, 1],
        }
    )
    chain_csv = tmp_path / "bad_chains.csv"
    bad_chains.to_csv(chain_csv, index=False)

    with pytest.raises(ValueError, match="Merge cardinality error"):
        clean_messy_extract(DEFAULT_EXTRACT_PATH, chain_csv)


def test_estimate_panel_did_reports_clustered_se_and_few_cluster_warning() -> None:
    cleaned, _ = clean_messy_extract()
    base = estimate_panel_did(cleaned, add_controls=False)
    ctrl = estimate_panel_did(cleaned, add_controls=True)

    expected_se = float(np.sqrt((18.0 / 100.0 + 12.875 / 64.0) * (18.0 / 17.0) * (35.0 / 32.0)))
    assert base["did_estimate"] == pytest.approx(2.875, abs=1e-9)
    assert base["se_store_cluster"] == pytest.approx(expected_se, abs=1e-12)
    assert base["n_obs"] == 36
    assert base["n_stores"] == 18
    assert base["n_state_clusters"] == 2
    assert "G=2" in str(base["inference_warning"])
    assert "synthetic teaching data" in str(base["inference_warning"]).lower()

    assert ctrl["se_store_cluster"] > 0.0
    assert ctrl["se_store_cluster"] != pytest.approx(base["se_store_cluster"], abs=1e-4)


def test_run_robustness_suite_returns_expected_four_specifications() -> None:
    specs = run_robustness_suite()

    assert list(specs.columns) == ROBUSTNESS_COLUMNS
    assert list(specs["spec_id"]) == [
        "baseline_open",
        "with_controls",
        "with_perm_closed",
        "pt_weight_025",
    ]
    assert list(specs["n_obs"]) == [36, 36, 40, 36]
    assert list(specs["n_stores"]) == [18, 18, 20, 18]
    assert (specs["se_store_cluster"] > 0.0).all()


def test_latex_booktabs_table_passes_verification_and_omits_stars() -> None:
    specs = run_robustness_suite()
    latex = render_latex_booktabs_table(specs)

    assert r"\toprule" in latex
    assert r"\midrule" in latex
    assert r"\bottomrule" in latex
    assert "Synthetic teaching data" in latex
    assert "$G=2$" in latex
    verify_latex_table_numbers(latex, specs)


def test_planted_drifted_table_fault_raises_value_error() -> None:
    specs = run_robustness_suite()
    drifted_tex = (FAULTS_DIR / "drifted_table.tex").read_text(encoding="utf-8")

    with pytest.raises(ValueError, match="LaTeX table drift"):
        verify_latex_table_numbers(drifted_tex, specs)


def test_verify_latex_table_rejects_stars_and_missing_caveat() -> None:
    specs = run_robustness_suite()
    latex = render_latex_booktabs_table(specs)

    starred = latex.replace("2.88", "2.88***", 1)
    with pytest.raises(ValueError, match="LaTeX table drift"):
        verify_latex_table_numbers(starred, specs)

    stripped_caveat = latex.replace("Synthetic teaching data;", "Empirical microdata;")
    with pytest.raises(ValueError, match="LaTeX table drift"):
        verify_latex_table_numbers(stripped_caveat, specs)


def test_verify_latex_table_rejects_nan_and_inf_values() -> None:
    specs = run_robustness_suite()
    latex = render_latex_booktabs_table(specs)

    for bad_token in ("nan", "NaN", "inf", "-inf"):
        corrupted = latex.replace("2.88", bad_token, 1)
        with pytest.raises(ValueError, match="LaTeX table drift"):
            verify_latex_table_numbers(corrupted, specs)

    for bad_se in ("(nan)", "(inf)"):
        corrupted_se = latex.replace("(0.66)", bad_se, 1)
        with pytest.raises(ValueError, match="LaTeX table drift"):
            verify_latex_table_numbers(corrupted_se, specs)

    nan_specs = specs.copy()
    nan_specs.loc[0, "did_estimate"] = float("nan")
    with pytest.raises(ValueError, match="LaTeX table drift"):
        verify_latex_table_numbers(latex, nan_specs)

    for bad_tol in (float("nan"), float("inf"), -0.01):
        with pytest.raises(ValueError, match="LaTeX table drift"):
            verify_latex_table_numbers(latex, specs, tol=bad_tol)


def test_silent_attrition_and_table_drift_brief_documents_both_traps() -> None:
    brief = (FAULTS_DIR / "silent_attrition_and_table_drift.md").read_text(encoding="utf-8")
    assert "dropna()" in brief
    assert "drifted_table.tex" in brief
