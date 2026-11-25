from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import time

import numpy as np
import pytest

from structural_bellman import (
    DEFAULT_TRANSITION,
    MOMENT_COLUMNS,
    audit_calibration_moments,
    bellman_step,
    check_blackwell_conditions,
    render_structural_caveat,
    solve_consumption_saving,
    validate_grid_interiority,
    validate_structural_params,
)


FAULTS_DIR = Path(__file__).resolve().parents[1] / "faults"


def test_solve_consumption_saving_converges_fast_and_interior() -> None:
    t0 = time.perf_counter()
    result = solve_consumption_saving()
    elapsed = time.perf_counter() - t0

    assert elapsed < 0.15
    assert result.converged is True
    assert result.sup_norm < 1e-7
    assert result.iterations < 500
    assert result.stationary_dist.shape == (60, 2)
    assert float(result.stationary_dist.sum()) == pytest.approx(1.0, abs=1e-12)
    assert np.all(result.stationary_dist >= 0.0)
    assert result.share_at_grid_top <= 0.01
    assert result.grid_warning == ""
    validate_grid_interiority(result)


def test_policy_monotonicity_and_log_utility_case() -> None:
    result = solve_consumption_saving(gamma=1.0)

    assert result.converged is True
    assert np.all(np.diff(result.policy_assets[:, 0]) >= -1e-12)
    assert np.all(np.diff(result.policy_assets[:, 1]) >= -1e-12)


def test_blackwell_conditions_hold_for_valid_bellman_operator() -> None:
    asset_grid = np.linspace(0.0, 12.0, 60, dtype=float)
    income = np.array([0.7, 1.3], dtype=float)
    result = solve_consumption_saving()

    checks = check_blackwell_conditions(
        result.value,
        shift=1.5,
        beta=0.95,
        r=0.03,
        gamma=2.0,
        income=income,
        transition=DEFAULT_TRANSITION,
        asset_grid=asset_grid,
    )
    assert checks["monotonicity_holds"] is True
    assert checks["discounting_holds"] is True
    assert float(checks["max_discounting_gap"]) < 1e-11


def test_validate_structural_params_rejects_impatient_or_bad_inputs() -> None:
    grid = np.linspace(0.0, 5.0, 10)
    with pytest.raises(ValueError, match="Impatience"):
        validate_structural_params(
            beta=0.98,
            r=0.03,
            gamma=2.0,
            transition=DEFAULT_TRANSITION,
            asset_grid=grid,
        )

    with pytest.raises(ValueError, match="strictly increasing"):
        validate_structural_params(
            beta=0.95,
            r=0.03,
            gamma=2.0,
            transition=DEFAULT_TRANSITION,
            asset_grid=np.array([0.0, 2.0, 1.5]),
        )


def test_planted_non_stochastic_transition_fault_fails_validation() -> None:
    cfg = json.loads((FAULTS_DIR / "non_stochastic_transition.json").read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match="rows must sum to 1.0"):
        solve_consumption_saving(**cfg)


def test_planted_premature_stop_fault_raises_runtime_error() -> None:
    cfg = json.loads((FAULTS_DIR / "premature_stop_config.json").read_text(encoding="utf-8"))
    with pytest.raises(RuntimeError, match="Bellman VFI failed to converge"):
        solve_consumption_saving(**cfg)


def test_planted_clipped_asset_grid_fault_triggers_boundary_gate() -> None:
    cfg = json.loads((FAULTS_DIR / "clipped_asset_grid.json").read_text(encoding="utf-8"))
    clipped = solve_consumption_saving(**cfg)

    assert clipped.share_at_grid_top > 0.01
    assert clipped.grid_warning != ""
    with pytest.raises(ValueError, match="Asset grid upper bound binds"):
        validate_grid_interiority(clipped)


def test_audit_calibration_moments_includes_schema_and_identification_caveat() -> None:
    result = solve_consumption_saving()
    moments = audit_calibration_moments(result)
    caveat = render_structural_caveat(result)

    assert list(moments.columns) == MOMENT_COLUMNS
    assert len(moments) == 4
    assert "do not certify structural identification" in caveat
    assert "structural identification" in " ".join(moments["diagnostic_note"]).lower()
    assert bellman_step is not None


def test_non_finite_structural_inputs_and_top_share_are_rejected() -> None:
    grid = np.linspace(0.0, 5.0, 10)
    with pytest.raises(ValueError, match="beta"):
        validate_structural_params(
            beta=float("nan"),
            r=0.03,
            gamma=2.0,
            transition=DEFAULT_TRANSITION,
            asset_grid=grid,
        )

    nan_trans = np.array([[float("nan"), 0.15], [0.15, 0.85]])
    with pytest.raises(ValueError, match="non-finite"):
        validate_structural_params(
            beta=0.95,
            r=0.03,
            gamma=2.0,
            transition=nan_trans,
            asset_grid=grid,
        )

    result = solve_consumption_saving()
    nan_top = replace(result, share_at_grid_top=float("nan"))
    with pytest.raises(ValueError, match="Asset grid upper bound binds"):
        validate_grid_interiority(nan_top)
