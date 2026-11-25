from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from theory_conjecture import (
    THEOREM_EPISTEMIC_RULE,
    ScreeningMenu,
    audit_proof_assumptions,
    evaluate_naive_textbook_conjecture,
    search_conjecture_counterexample,
    solve_optimal_screening_menu,
    verify_ic_ir_constraints,
)


FAULTS_DIR = Path(__file__).resolve().parents[1] / "faults"
REPO_ROOT = Path(__file__).resolve().parents[3]


def _brute_force_max_profit(
    *,
    theta_low: float,
    theta_high: float,
    mu: float,
    cost: float,
    outside_slope: float,
) -> float:
    delta = theta_high - theta_low
    q_max = (theta_high - (1.0 - mu) * theta_low) / (mu * cost) + outside_slope + 1.0
    grid = np.linspace(0.0, q_max, 401)
    best = -np.inf
    for i, q_l in enumerate(grid):
        q_h_vec = grid[i:]
        u_l_case_a = outside_slope * theta_low
        u_h_case_a = np.maximum(outside_slope * theta_high, u_l_case_a + delta * q_l)
        valid_a = q_h_vec >= np.maximum(outside_slope, q_l) - 1e-12
        if np.any(valid_a):
            qh_a = q_h_vec[valid_a]
            uh_a = u_h_case_a[valid_a] if np.ndim(u_h_case_a) else u_h_case_a
            prof_a = (
                (1.0 - mu) * (theta_low * q_l - 0.5 * cost * q_l**2 - u_l_case_a)
                + mu * (theta_high * qh_a - 0.5 * cost * qh_a**2 - uh_a)
            )
            best = max(best, float(np.max(prof_a)))

        valid_b = q_h_vec < outside_slope
        if np.any(valid_b):
            qh_b = q_h_vec[valid_b]
            u_h_b = outside_slope * theta_high
            u_l_b = u_h_b - delta * qh_b
            prof_b = (
                (1.0 - mu) * (theta_low * q_l - 0.5 * cost * q_l**2 - u_l_b)
                + mu * (theta_high * qh_b - 0.5 * cost * qh_b**2 - u_h_b)
            )
            best = max(best, float(np.max(prof_b)))
    return best


def _menu_profit(
    menu: ScreeningMenu,
    *,
    mu: float,
    cost: float,
) -> float:
    return float(
        (1.0 - mu) * (menu.t_low - 0.5 * cost * menu.q_low**2)
        + mu * (menu.t_high - 0.5 * cost * menu.q_high**2)
    )


@pytest.mark.parametrize(
    ("params", "expected_regime"),
    [
        (
            {
                "theta_low": 1.0,
                "theta_high": 1.5,
                "mu": 0.5,
                "cost": 1.0,
                "outside_slope": 0.0,
            },
            "standard_downward_distortion",
        ),
        (
            {
                "theta_low": 1.0,
                "theta_high": 2.0,
                "mu": 0.6,
                "cost": 1.0,
                "outside_slope": 0.0,
            },
            "shutdown_low_type",
        ),
        (
            {
                "theta_low": 1.0,
                "theta_high": 1.5,
                "mu": 0.5,
                "cost": 1.0,
                "outside_slope": 0.75,
            },
            "both_ir_bind",
        ),
        (
            {
                "theta_low": 1.0,
                "theta_high": 1.5,
                "mu": 0.5,
                "cost": 1.0,
                "outside_slope": 2.5,
            },
            "countervailing_ir_high_binds",
        ),
    ],
)
def test_solve_optimal_screening_menu_covers_all_four_regimes(
    params: dict[str, float],
    expected_regime: str,
) -> None:
    menu = solve_optimal_screening_menu(**params)
    checks = verify_ic_ir_constraints(
        menu,
        theta_low=params["theta_low"],
        theta_high=params["theta_high"],
        outside_slope=params["outside_slope"],
    )

    assert menu.regime == expected_regime
    assert checks["all_constraints_hold"] is True

    analytic_profit = _menu_profit(menu, mu=params["mu"], cost=params["cost"])
    grid_profit = _brute_force_max_profit(**params)
    assert analytic_profit >= grid_profit - 1e-4


def test_default_conjecture_sweep_finds_exact_closed_form_counterexample() -> None:
    sweep = search_conjecture_counterexample()

    assert sweep["counterexample_found"] is True
    assert sweep["theorem_certified"] is False
    assert sweep["exact_ir_high_deficit_fraction"] == "1/8"
    assert float(sweep["exact_ir_high_deficit"]) == pytest.approx(0.125, abs=1e-15)
    assert isinstance(sweep["optimal_menu"], ScreeningMenu)
    assert sweep["optimal_menu"].ir_high_slack == pytest.approx(0.0, abs=1e-12)


def test_finite_grid_without_counterexample_never_certifies_theorem() -> None:
    kappa_zero_grid = [
        {
            "theta_low": 1.0,
            "theta_high": 1.5,
            "mu": mu,
            "cost": 1.0,
            "outside_slope": 0.0,
        }
        for mu in (0.2, 0.4, 0.6)
    ]
    sweep = search_conjecture_counterexample(kappa_zero_grid)

    assert sweep["counterexample_found"] is False
    assert sweep["theorem_certified"] is False
    assert "never proves a universal theorem" in str(sweep["conclusion"])
    assert "never proves a universal theorem" in THEOREM_EPISTEMIC_RULE


def test_evaluate_naive_conjecture_detects_ir_high_violation() -> None:
    ok = evaluate_naive_textbook_conjecture(
        theta_low=1.0,
        theta_high=1.5,
        mu=0.5,
        cost=1.0,
        outside_slope=0.25,
    )
    bad = evaluate_naive_textbook_conjecture(
        theta_low=1.0,
        theta_high=1.5,
        mu=0.5,
        cost=1.0,
        outside_slope=0.75,
    )

    assert ok["conjecture_holds"] is True
    assert float(ok["ir_high_slack"]) == pytest.approx(0.125, abs=1e-12)

    assert bad["conjecture_holds"] is False
    assert float(bad["exact_ir_high_deficit"]) == pytest.approx(0.125, abs=1e-12)


def test_planted_unstated_outside_option_claim_fails_assumption_audit() -> None:
    draft = (FAULTS_DIR / "unstated_outside_option_claim.md").read_text(encoding="utf-8")
    missing = audit_proof_assumptions(draft)

    assert missing == ["outside_slope == 0", "interior_low_type"]

    repaired = (
        "Proposition 1 (Repaired). Assume outside_slope == 0 and interior_low_type "
        "(theta_L > mu * theta_H). Then IR_L and IC_H bind and IR_H is strictly slack."
    )
    assert audit_proof_assumptions(repaired) == []


def test_planted_citation_overclaim_fixture_flags_pre_doi_and_synthetic_traps() -> None:
    planted = (FAULTS_DIR / "citation_overclaim_structural_theory.md").read_text(
        encoding="utf-8"
    )
    bib = (REPO_ROOT / "references" / "bibliography.bib").read_text(encoding="utf-8")

    assert "10.1257/aer.84.4.772" in planted
    assert "Crossref does not currently resolve a DOI for this 1994 article" in bib
    assert "structural_bellman.py" in planted


def test_non_finite_screening_inputs_are_rejected() -> None:
    with pytest.raises(ValueError, match="finite"):
        solve_optimal_screening_menu(
            theta_low=1.0,
            theta_high=1.5,
            mu=0.5,
            outside_slope=float("nan"),
        )

    menu = solve_optimal_screening_menu(theta_low=1.0, theta_high=1.5, mu=0.5)
    with pytest.raises(ValueError, match="Non-finite"):
        verify_ic_ir_constraints(
            menu,
            theta_low=1.0,
            theta_high=1.5,
            tol=float("nan"),
        )
