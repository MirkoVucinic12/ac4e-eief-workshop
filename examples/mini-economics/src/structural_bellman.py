"""Two-state consumption-saving Bellman solver and numerical checks.

Synthetic numerical illustration for the EIEF / Luiss workshop (Track S).
Passing numerical tests, Blackwell checks, and solver convergence (< tol) confirm
that the code and algorithm run as written; they do not establish structural
identification or policy counterfactual validity.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

import numpy as np
import pandas as pd


DEFAULT_TRANSITION = np.array([[0.85, 0.15], [0.15, 0.85]], dtype=float)
MOMENT_COLUMNS = ["moment", "model_value", "source_function", "diagnostic_note"]
STRUCTURAL_CAVEAT = (
    "Synthetic numerical illustration; solver convergence and moment fit do not "
    "certify structural identification."
)


@dataclass(frozen=True)
class BellmanResult:
    """Converged consumption-saving Bellman solution and ergodic diagnostics."""

    value: np.ndarray
    policy_idx: np.ndarray
    policy_assets: np.ndarray
    stationary_dist: np.ndarray
    iterations: int
    sup_norm: float
    converged: bool
    share_at_borrowing_limit: float
    share_at_grid_top: float
    mean_assets: float
    wealth_to_income_ratio: float
    grid_warning: str


def _crra_utility(consumption: np.ndarray, gamma: float) -> np.ndarray:
    util = np.full_like(consumption, -np.inf, dtype=float)
    pos = consumption > 0.0
    if abs(gamma - 1.0) < 1e-12:
        util[pos] = np.log(consumption[pos])
    else:
        util[pos] = (np.power(consumption[pos], 1.0 - gamma) - 1.0) / (1.0 - gamma)
    return util


def validate_structural_params(
    *,
    beta: float,
    r: float,
    gamma: float,
    transition: np.ndarray,
    asset_grid: np.ndarray,
) -> None:
    """Validate economic admissibility, impatience, grid order, and Markov matrix."""
    if not math.isfinite(beta) or beta <= 0.0 or beta >= 1.0:
        raise ValueError(f"Discount factor beta must lie in (0, 1), got {beta}")
    if not math.isfinite(gamma) or gamma <= 0.0:
        raise ValueError(f"Risk aversion gamma must be positive, got {gamma}")
    if not math.isfinite(r) or 1.0 + r <= 0.0:
        raise ValueError(f"Gross interest rate 1 + r must be positive, got r={r}")
    if not math.isfinite(beta * (1.0 + r)) or beta * (1.0 + r) >= 1.0:
        raise ValueError(
            f"Impatience condition beta * (1 + r) < 1 violated: {beta * (1.0 + r):.6f}"
        )

    grid = np.asarray(asset_grid, dtype=float)
    if grid.ndim != 1 or grid.size < 2 or not np.all(np.isfinite(grid)):
        raise ValueError("asset_grid must be a finite 1D array with at least 2 points")
    if not np.all(np.diff(grid) > 0.0):
        raise ValueError("asset_grid must be strictly increasing")

    trans = np.asarray(transition, dtype=float)
    if trans.ndim != 2 or trans.shape[0] != trans.shape[1] or trans.shape[0] < 2:
        raise ValueError("transition must be a square 2D Markov matrix")
    if not np.all(np.isfinite(trans)):
        raise ValueError("transition matrix contains non-finite probabilities")
    if np.any(trans < 0.0):
        raise ValueError("transition matrix contains negative probabilities")
    row_sums = trans.sum(axis=1)
    if not np.all(np.isfinite(row_sums)) or np.max(np.abs(row_sums - 1.0)) > 1e-9:
        raise ValueError(
            f"transition matrix rows must sum to 1.0 within 1e-9; got {row_sums.tolist()}"
        )


def _bellman_step_from_flow(
    value: np.ndarray,
    flow_utility: np.ndarray,
    beta: float,
    transition: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    expected_next = value @ transition.T
    rhs = flow_utility + beta * expected_next.T[None, :, :]
    policy_idx = np.argmax(rhs, axis=2)
    new_value = np.take_along_axis(rhs, policy_idx[:, :, None], axis=2)[:, :, 0]
    if not np.all(np.isfinite(new_value)):
        raise ValueError("Empty positive-consumption budget set at one or more states")
    return new_value, policy_idx


def bellman_step(
    value: np.ndarray,
    *,
    beta: float,
    r: float,
    gamma: float,
    income: np.ndarray,
    transition: np.ndarray,
    asset_grid: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Apply one Bellman operator step ``(T V)(a, y) = max_{a'} u(c) + beta E[V(a', y')]``."""
    grid = np.asarray(asset_grid, dtype=float)
    inc = np.asarray(income, dtype=float)
    trans = np.asarray(transition, dtype=float)
    val = np.asarray(value, dtype=float)

    if inc.ndim != 1 or inc.size != trans.shape[0]:
        raise ValueError("income must be 1D and match transition dimension")
    if not np.all(np.isfinite(inc)) or np.any(inc <= 0.0):
        raise ValueError("income states must be finite and strictly positive")
    if val.shape != (grid.size, inc.size) or not np.all(np.isfinite(val)):
        raise ValueError(
            f"value must be finite with shape {(grid.size, inc.size)}, got {val.shape}"
        )

    consumption = (1.0 + r) * grid[:, None, None] + inc[None, :, None] - grid[None, None, :]
    flow_utility = _crra_utility(consumption, gamma)
    return _bellman_step_from_flow(val, flow_utility, beta, trans)


def check_blackwell_conditions(
    value: np.ndarray,
    *,
    shift: float = 1.0,
    beta: float,
    r: float,
    gamma: float,
    income: np.ndarray,
    transition: np.ndarray,
    asset_grid: np.ndarray,
) -> dict[str, float | bool]:
    """Numerically verify Blackwell monotonicity and discounting on ``bellman_step``."""
    if not math.isfinite(shift) or shift < 0.0:
        raise ValueError("Blackwell shift c must be finite and non-negative")

    base_tv, _ = bellman_step(
        value,
        beta=beta,
        r=r,
        gamma=gamma,
        income=income,
        transition=transition,
        asset_grid=asset_grid,
    )
    shifted_tv, _ = bellman_step(
        value + shift,
        beta=beta,
        r=r,
        gamma=gamma,
        income=income,
        transition=transition,
        asset_grid=asset_grid,
    )

    weights = np.linspace(0.25, 1.0, value.shape[0])[:, None]
    monotone_tv, _ = bellman_step(
        value + shift * weights,
        beta=beta,
        r=r,
        gamma=gamma,
        income=income,
        transition=transition,
        asset_grid=asset_grid,
    )

    diff = shifted_tv - base_tv
    monotonicity_holds = bool(
        np.all(diff >= -1e-11) and np.all(monotone_tv - base_tv >= -1e-11)
    )
    discounting_holds = bool(np.all(diff <= beta * shift + 1e-10))
    max_discounting_gap = float(np.max(np.abs(diff - beta * shift)))

    return {
        "monotonicity_holds": monotonicity_holds,
        "discounting_holds": discounting_holds,
        "max_discounting_gap": max_discounting_gap,
    }


def _compute_stationary_distribution(
    policy_idx: np.ndarray,
    transition: np.ndarray,
) -> np.ndarray:
    n_grid, n_states = policy_idx.shape
    n_total = n_grid * n_states
    q_mat = np.zeros((n_total, n_total), dtype=float)

    for i_a in range(n_grid):
        for i_y in range(n_states):
            row = i_a * n_states + i_y
            next_a = int(policy_idx[i_a, i_y])
            for next_y in range(n_states):
                col = next_a * n_states + next_y
                q_mat[row, col] += transition[i_y, next_y]

    lhs = np.vstack([q_mat.T - np.eye(n_total), np.ones((1, n_total), dtype=float)])
    rhs = np.zeros(n_total + 1, dtype=float)
    rhs[-1] = 1.0
    mu, _, _, _ = np.linalg.lstsq(lhs, rhs, rcond=None)
    mu = np.maximum(mu, 0.0)
    total = float(mu.sum())
    if total <= 0.0:
        raise RuntimeError("Failed to compute positive stationary distribution")
    mu /= total

    for _ in range(50):
        mu = mu @ q_mat
    mu = np.maximum(mu, 0.0)
    mu /= float(mu.sum())

    l1_residual = float(np.sum(np.abs(mu @ q_mat - mu)))
    if (
        not np.all(np.isfinite(mu))
        or not math.isfinite(l1_residual)
        or abs(float(mu.sum()) - 1.0) > 1e-9
        or np.any(mu < 0.0)
        or l1_residual >= 1e-9
    ):
        raise RuntimeError(
            f"Stationary distribution failed invariant check: L1 residual={l1_residual:.3e}"
        )
    return mu.reshape(n_grid, n_states)


def solve_consumption_saving(
    *,
    beta: float = 0.95,
    r: float = 0.03,
    gamma: float = 2.0,
    income: tuple[float, float] | Sequence[float] = (0.7, 1.3),
    transition: np.ndarray | Sequence[Sequence[float]] | None = None,
    a_min: float = 0.0,
    a_max: float = 12.0,
    n_grid: int = 60,
    tol: float = 1e-7,
    max_iter: int = 500,
) -> BellmanResult:
    """Solve the consumption-saving problem by VFI and compute its ergodic distribution.

    Raises:
        ValueError: If structural parameters, asset grid, or Markov matrix are invalid.
        RuntimeError: If VFI fails to reach ``sup_norm < tol`` within ``max_iter``.
    """
    if n_grid < 2:
        raise ValueError(f"n_grid must be >= 2, got {n_grid}")
    if not (math.isfinite(a_min) and math.isfinite(a_max)) or a_max <= a_min:
        raise ValueError(f"a_max ({a_max}) must be finite and exceed a_min ({a_min})")
    if not math.isfinite(tol) or tol <= 0.0 or max_iter < 1:
        raise ValueError("tol must be finite and > 0 and max_iter >= 1")

    asset_grid = np.linspace(a_min, a_max, n_grid, dtype=float)
    income_arr = np.asarray(income, dtype=float)
    if (
        income_arr.shape != (2,)
        or not np.all(np.isfinite(income_arr))
        or np.any(income_arr <= 0.0)
    ):
        raise ValueError("income must contain two finite strictly positive state values")
    trans_arr = (
        DEFAULT_TRANSITION.copy()
        if transition is None
        else np.asarray(transition, dtype=float)
    )

    validate_structural_params(
        beta=beta,
        r=r,
        gamma=gamma,
        transition=trans_arr,
        asset_grid=asset_grid,
    )

    init_c = np.maximum(r * asset_grid[:, None] + income_arr[None, :], 1e-6)
    value = _crra_utility(init_c, gamma) / (1.0 - beta)

    policy_idx = np.zeros((n_grid, 2), dtype=int)
    sup_norm = float("inf")
    converged = False
    iterations = 0

    for step in range(1, max_iter + 1):
        next_value, policy_idx = bellman_step(
            value,
            beta=beta,
            r=r,
            gamma=gamma,
            income=income_arr,
            transition=trans_arr,
            asset_grid=asset_grid,
        )
        sup_norm = float(np.max(np.abs(next_value - value)))
        value = next_value
        iterations = step
        if not math.isfinite(sup_norm):
            break
        if sup_norm < tol:
            converged = True
            break

    if not converged:
        raise RuntimeError(
            f"Bellman VFI failed to converge after {max_iter} iterations "
            f"(sup_norm={sup_norm:.3e} >= tol={tol:.3e})"
        )

    policy_assets = asset_grid[policy_idx]
    stationary_dist = _compute_stationary_distribution(policy_idx, trans_arr)

    share_bottom = float(stationary_dist[0, :].sum())
    share_top = float(stationary_dist[-1, :].sum())
    mean_assets = float(np.sum(stationary_dist * asset_grid[:, None]))
    mean_income = float(np.sum(stationary_dist * income_arr[None, :]))
    wealth_to_income = mean_assets / mean_income

    grid_warning = ""
    if share_top > 0.01:
        grid_warning = (
            f"Upper asset grid boundary binds: stationary mass at a_max={a_max} is "
            f"{share_top:.4f} > 0.01. Increase a_max before interpreting moments."
        )

    return BellmanResult(
        value=value,
        policy_idx=policy_idx,
        policy_assets=policy_assets,
        stationary_dist=stationary_dist,
        iterations=iterations,
        sup_norm=sup_norm,
        converged=converged,
        share_at_borrowing_limit=share_bottom,
        share_at_grid_top=share_top,
        mean_assets=mean_assets,
        wealth_to_income_ratio=wealth_to_income,
        grid_warning=grid_warning,
    )


def validate_grid_interiority(
    result: BellmanResult,
    *,
    max_top_share: float = 0.01,
) -> None:
    """Require stationary mass at ``a_max`` to stay within ``max_top_share``."""
    if not math.isfinite(max_top_share) or max_top_share < 0.0:
        raise ValueError(f"max_top_share must be finite and >= 0, got {max_top_share}")
    if not math.isfinite(result.share_at_grid_top) or result.share_at_grid_top > max_top_share:
        raise ValueError(
            f"Asset grid upper bound binds: share_at_grid_top={result.share_at_grid_top:.4f} "
            f"> max_top_share={max_top_share:.4f}"
        )


def render_structural_caveat(result: BellmanResult) -> str:
    """Return a note separating numerical convergence from structural identification."""
    return (
        f"{STRUCTURAL_CAVEAT} "
        f"(iterations={result.iterations}, sup_norm={result.sup_norm:.2e}, "
        f"share_at_grid_top={result.share_at_grid_top:.4f})"
    )


def audit_calibration_moments(result: BellmanResult) -> pd.DataFrame:
    """Map stationary model moments to code functions with interpretation notes."""
    rows = [
        {
            "moment": "mean_assets",
            "model_value": result.mean_assets,
            "source_function": "solve_consumption_saving",
            "diagnostic_note": "Stationary E[a]; synthetic numerical illustration",
        },
        {
            "moment": "wealth_to_income_ratio",
            "model_value": result.wealth_to_income_ratio,
            "source_function": "solve_consumption_saving",
            "diagnostic_note": STRUCTURAL_CAVEAT,
        },
        {
            "moment": "share_at_borrowing_limit",
            "model_value": result.share_at_borrowing_limit,
            "source_function": "solve_consumption_saving",
            "diagnostic_note": "Stationary mass at borrowing limit a_min",
        },
        {
            "moment": "share_at_grid_top",
            "model_value": result.share_at_grid_top,
            "source_function": "validate_grid_interiority",
            "diagnostic_note": (
                result.grid_warning
                if result.grid_warning
                else "Interior upper bound (mass <= 0.01)"
            ),
        },
    ]
    return pd.DataFrame(rows, columns=MOMENT_COLUMNS)


def main() -> None:
    """Solve the baseline buffer-stock model and print numerical audit diagnostics."""
    asset_grid = np.linspace(0.0, 12.0, 60, dtype=float)
    income = np.array([0.7, 1.3], dtype=float)
    result = solve_consumption_saving()
    validate_grid_interiority(result)
    blackwell = check_blackwell_conditions(
        result.value,
        beta=0.95,
        r=0.03,
        gamma=2.0,
        income=income,
        transition=DEFAULT_TRANSITION,
        asset_grid=asset_grid,
    )
    moments = audit_calibration_moments(result)

    print("Consumption-saving Bellman solver (Track S)")
    print("===========================================")
    print(f"  converged: {result.converged} in {result.iterations} iterations")
    print(f"  sup_norm: {result.sup_norm:.3e}")
    print(
        f"  Blackwell: monotonicity={blackwell['monotonicity_holds']}, "
        f"discounting={blackwell['discounting_holds']} "
        f"(max_gap={blackwell['max_discounting_gap']:.2e})"
    )
    print()
    print("Stationary moment audit")
    print("=======================")
    print(moments.to_string(index=False, float_format=lambda val: f"{val:.4f}"))
    print()
    print(f"Caveat: {render_structural_caveat(result)}")


if __name__ == "__main__":
    main()
