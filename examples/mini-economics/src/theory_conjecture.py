"""Two-type principal-agent screening, counterexample checks, and assumption checks.

Synthetic analytical illustration for the EIEF / Luiss workshop (Track T).
Closed-form counterexamples refute false universal claims without floating-point
error; passing on a finite parameter grid never proves a universal theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math
import re


THEOREM_EPISTEMIC_RULE = (
    "A verified closed-form counterexample refutes a false claim; "
    "passing on a finite grid never proves a universal theorem."
)


@dataclass(frozen=True)
class ScreeningMenu:
    """Optimal two-type screening contract and exact IC/IR constraint slacks."""

    q_low: float
    t_low: float
    q_high: float
    t_high: float
    ir_low_slack: float
    ir_high_slack: float
    ic_low_slack: float
    ic_high_slack: float
    regime: str


def _validate_screening_params(
    *,
    theta_low: float,
    theta_high: float,
    mu: float,
    cost: float,
    outside_slope: float,
) -> None:
    for name, val in (
        ("theta_low", theta_low),
        ("theta_high", theta_high),
        ("mu", mu),
        ("cost", cost),
        ("outside_slope", outside_slope),
    ):
        if not math.isfinite(val):
            raise ValueError(f"{name} must be finite, got {val}")
    if theta_low <= 0.0:
        raise ValueError(f"theta_low must be > 0, got {theta_low}")
    if theta_high <= theta_low:
        raise ValueError(
            f"theta_high ({theta_high}) must exceed theta_low ({theta_low})"
        )
    if mu <= 0.0 or mu >= 1.0:
        raise ValueError(f"High-type share mu must lie in (0, 1), got {mu}")
    if cost <= 0.0:
        raise ValueError(f"Quadratic cost parameter must be > 0, got {cost}")
    if outside_slope < 0.0:
        raise ValueError(f"outside_slope kappa must be >= 0, got {outside_slope}")


def verify_ic_ir_constraints(
    menu: ScreeningMenu,
    *,
    theta_low: float,
    theta_high: float,
    outside_slope: float = 0.0,
    tol: float = 1e-10,
) -> dict[str, float | bool]:
    """Verify exact participation, incentive-compatibility, and monotonicity slacks."""
    if not (
        math.isfinite(theta_low)
        and math.isfinite(theta_high)
        and math.isfinite(outside_slope)
        and math.isfinite(tol)
    ):
        raise ValueError("Non-finite parameter or tolerance in verify_ic_ir_constraints")
    if theta_low <= 0.0 or theta_high <= theta_low or outside_slope < 0.0 or tol < 0.0:
        raise ValueError("Invalid type, outside-option, or tolerance for IC/IR check")
    if not all(
        math.isfinite(val)
        for val in (menu.q_low, menu.t_low, menu.q_high, menu.t_high)
    ):
        raise ValueError("Non-finite contract quantity or transfer in ScreeningMenu")

    u_low = theta_low * menu.q_low - menu.t_low
    u_high = theta_high * menu.q_high - menu.t_high
    u_low_mimic = theta_low * menu.q_high - menu.t_high
    u_high_mimic = theta_high * menu.q_low - menu.t_low

    ir_low_slack = float(u_low - outside_slope * theta_low)
    ir_high_slack = float(u_high - outside_slope * theta_high)
    ic_low_slack = float(u_low - u_low_mimic)
    ic_high_slack = float(u_high - u_high_mimic)

    ir_low_holds = bool(ir_low_slack >= -tol)
    ir_high_holds = bool(ir_high_slack >= -tol)
    ic_low_holds = bool(ic_low_slack >= -tol)
    ic_high_holds = bool(ic_high_slack >= -tol)
    monotonicity_holds = bool(
        menu.q_low >= -tol and menu.q_high >= menu.q_low - tol
    )

    return {
        "ir_low_slack": ir_low_slack,
        "ir_high_slack": ir_high_slack,
        "ic_low_slack": ic_low_slack,
        "ic_high_slack": ic_high_slack,
        "ir_low_holds": ir_low_holds,
        "ir_high_holds": ir_high_holds,
        "ic_low_holds": ic_low_holds,
        "ic_high_holds": ic_high_holds,
        "monotonicity_holds": monotonicity_holds,
        "all_constraints_hold": bool(
            ir_low_holds
            and ir_high_holds
            and ic_low_holds
            and ic_high_holds
            and monotonicity_holds
        ),
    }


def solve_optimal_screening_menu(
    *,
    theta_low: float,
    theta_high: float,
    mu: float,
    cost: float = 1.0,
    outside_slope: float = 0.0,
) -> ScreeningMenu:
    """Compute the exact closed-form optimal menu with type-dependent outside options."""
    _validate_screening_params(
        theta_low=theta_low,
        theta_high=theta_high,
        mu=mu,
        cost=cost,
        outside_slope=outside_slope,
    )

    delta_theta = theta_high - theta_low
    q_l_std = max(0.0, (theta_low - mu * theta_high) / ((1.0 - mu) * cost))
    q_l_fb = theta_low / cost
    q_h_fb = theta_high / cost
    q_h_up = (theta_high - (1.0 - mu) * theta_low) / (mu * cost)

    if outside_slope == 0.0 and q_l_std == 0.0:
        q_low = 0.0
        q_high = q_h_fb
        u_low = 0.0
        u_high = 0.0
        regime = "shutdown_low_type"
    elif outside_slope < q_l_std:
        q_low = q_l_std
        q_high = q_h_fb
        u_low = outside_slope * theta_low
        u_high = u_low + delta_theta * q_low
        regime = "standard_downward_distortion"
    elif outside_slope <= q_h_up:
        q_low = min(q_l_fb, outside_slope)
        q_high = max(q_h_fb, outside_slope)
        u_low = outside_slope * theta_low
        u_high = outside_slope * theta_high
        regime = "both_ir_bind"
    else:
        q_low = q_l_fb
        q_high = q_h_up
        u_high = outside_slope * theta_high
        u_low = u_high - delta_theta * q_high
        regime = "countervailing_ir_high_binds"

    t_low = float(theta_low * q_low - u_low)
    t_high = float(theta_high * q_high - u_high)

    ir_low_slack = float(u_low - outside_slope * theta_low)
    ir_high_slack = float(u_high - outside_slope * theta_high)
    ic_low_slack = float(u_low - (theta_low * q_high - t_high))
    ic_high_slack = float(u_high - (theta_high * q_low - t_low))

    return ScreeningMenu(
        q_low=float(q_low),
        t_low=t_low,
        q_high=float(q_high),
        t_high=t_high,
        ir_low_slack=ir_low_slack,
        ir_high_slack=ir_high_slack,
        ic_low_slack=ic_low_slack,
        ic_high_slack=ic_high_slack,
        regime=regime,
    )


def evaluate_naive_textbook_conjecture(
    *,
    theta_low: float,
    theta_high: float,
    mu: float,
    cost: float = 1.0,
    outside_slope: float = 0.0,
) -> dict[str, float | bool | str]:
    """Evaluate the naive conjecture that (IR_L, IC_H) bind with IR_H >= 0 for all kappa >= 0."""
    _validate_screening_params(
        theta_low=theta_low,
        theta_high=theta_high,
        mu=mu,
        cost=cost,
        outside_slope=outside_slope,
    )

    delta_theta = theta_high - theta_low
    q_l_std = max(0.0, (theta_low - mu * theta_high) / ((1.0 - mu) * cost))
    q_h_fb = theta_high / cost

    t_l_naive = theta_low * q_l_std - outside_slope * theta_low
    t_h_naive = theta_high * q_h_fb - (
        outside_slope * theta_low + delta_theta * q_l_std
    )

    ir_high_slack = float(delta_theta * (q_l_std - outside_slope))
    exact_deficit = float(max(0.0, delta_theta * (outside_slope - q_l_std)))
    conjecture_holds = bool(q_l_std >= outside_slope)
    ir_high_strictly_slack = bool(q_l_std > outside_slope)

    return {
        "q_low_std": float(q_l_std),
        "t_low_std": float(t_l_naive),
        "q_high_fb": float(q_h_fb),
        "t_high_std": float(t_h_naive),
        "ir_high_slack": ir_high_slack,
        "exact_ir_high_deficit": exact_deficit,
        "conjecture_holds": conjecture_holds,
        "ir_high_strictly_slack": ir_high_strictly_slack,
        "epistemic_note": THEOREM_EPISTEMIC_RULE,
    }


def _default_conjecture_grid() -> list[dict[str, float]]:
    grid: list[dict[str, float]] = []
    for mu in (0.2, 0.5, 0.7):
        for outside_slope in (0.0, 0.25, 0.75):
            grid.append(
                {
                    "theta_low": 1.0,
                    "theta_high": 1.5,
                    "mu": mu,
                    "cost": 1.0,
                    "outside_slope": outside_slope,
                }
            )
    return grid


def _exact_rational_ir_high_deficit(params: dict[str, float]) -> Fraction:
    theta_l = Fraction(str(params["theta_low"]))
    theta_h = Fraction(str(params["theta_high"]))
    mu = Fraction(str(params["mu"]))
    cost = Fraction(str(params.get("cost", 1.0)))
    kappa = Fraction(str(params.get("outside_slope", 0.0)))

    raw_q_l = (theta_l - mu * theta_h) / ((Fraction(1) - mu) * cost)
    q_l_std = raw_q_l if raw_q_l > 0 else Fraction(0)
    deficit = (theta_h - theta_l) * (kappa - q_l_std)
    return deficit if deficit > 0 else Fraction(0)


def search_conjecture_counterexample(
    grid: list[dict[str, float]] | None = None,
) -> dict[str, object]:
    """Sweep a parameter grid and verify the first counterexample in exact arithmetic."""
    candidates = _default_conjecture_grid() if grid is None else grid
    points_checked = 0

    for raw_point in candidates:
        point = {
            "theta_low": float(raw_point["theta_low"]),
            "theta_high": float(raw_point["theta_high"]),
            "mu": float(raw_point["mu"]),
            "cost": float(raw_point.get("cost", 1.0)),
            "outside_slope": float(raw_point.get("outside_slope", 0.0)),
        }
        points_checked += 1
        eval_res = evaluate_naive_textbook_conjecture(**point)
        exact_frac = _exact_rational_ir_high_deficit(point)

        if exact_frac > 0:
            optimal = solve_optimal_screening_menu(**point)
            return {
                "counterexample_found": True,
                "points_checked": points_checked,
                "counterexample_params": point,
                "naive_evaluation": eval_res,
                "optimal_menu": optimal,
                "exact_ir_high_deficit": float(exact_frac),
                "exact_ir_high_deficit_fraction": str(exact_frac),
                "theorem_certified": False,
                "conclusion": (
                    f"Refuted at point {points_checked}: naive (IR_L, IC_H) menu "
                    f"violates IR_H by exact deficit {exact_frac} "
                    f"({float(exact_frac):.6f}). {THEOREM_EPISTEMIC_RULE}"
                ),
            }

    return {
        "counterexample_found": False,
        "points_checked": points_checked,
        "counterexample_params": None,
        "naive_evaluation": None,
        "optimal_menu": None,
        "exact_ir_high_deficit": 0.0,
        "exact_ir_high_deficit_fraction": "0",
        "theorem_certified": False,
        "conclusion": (
            f"No counterexample on {points_checked} grid points. "
            f"{THEOREM_EPISTEMIC_RULE}"
        ),
    }


def _tag_is_stated(text: str, tag: str) -> bool:
    lowered = text.lower()
    if tag.lower() in lowered:
        return True
    if tag == "outside_slope == 0":
        return bool(
            re.search(r"(\\kappa|kappa|outside_slope)\s*(==|=)\s*0(?![.\d])", text)
            or "type-independent outside option" in lowered
        )
    if tag == "interior_low_type":
        return bool(
            re.search(r"theta_l(?:ow)?\s*>\s*\\?mu\s*\*?\s*\\?theta_h", lowered)
            or "q_l^* > 0" in lowered
            or "strictly positive low-type quantity" in lowered
        )
    return False


def _extract_proposition_body(markdown: str) -> str:
    split_match = re.split(r"(?im)^why this fails\b", markdown, maxsplit=1)
    return split_match[0]


def audit_proof_assumptions(
    proposition_markdown: str,
    *,
    required_tags: tuple[str, ...] = ("outside_slope == 0", "interior_low_type"),
) -> list[str]:
    """Return required domain-assumption tags missing from a draft proposition."""
    if not proposition_markdown.strip():
        raise ValueError("proposition_markdown must be non-empty")

    body = _extract_proposition_body(proposition_markdown)
    missing: list[str] = []
    for tag in required_tags:
        if not _tag_is_stated(body, tag):
            missing.append(tag)
    return missing


def main() -> None:
    """Print the kappa=0 textbook baseline, the kappa>0 counterexample, and the proof note."""
    baseline = solve_optimal_screening_menu(
        theta_low=1.0,
        theta_high=1.5,
        mu=0.5,
        cost=1.0,
        outside_slope=0.0,
    )
    sweep = search_conjecture_counterexample()

    print("Two-type screening and conjecture check (Track T)")
    print("=================================================")
    print(
        f"  Textbook baseline (kappa=0, mu=0.5): regime={baseline.regime}, "
        f"q_low={baseline.q_low:.3f}, q_high={baseline.q_high:.3f}, "
        f"ir_high_slack={baseline.ir_high_slack:.3f}"
    )
    print()

    print("Grid counterexample search")
    print("==========================")
    print(f"  counterexample_found: {sweep['counterexample_found']}")
    print(f"  points_checked: {sweep['points_checked']}")
    print(f"  counterexample_params: {sweep['counterexample_params']}")
    print(
        f"  exact_ir_high_deficit: {sweep['exact_ir_high_deficit_fraction']} "
        f"({float(sweep['exact_ir_high_deficit']):.4f})"
    )
    opt = sweep["optimal_menu"]
    if isinstance(opt, ScreeningMenu):
        print(
            f"  repaired optimal regime: {opt.regime} "
            f"(q_low={opt.q_low:.3f}, q_high={opt.q_high:.3f}, "
            f"ir_high_slack={opt.ir_high_slack:.3f})"
        )
    print()
    print(f"Note: {THEOREM_EPISTEMIC_RULE}")


if __name__ == "__main__":
    main()
