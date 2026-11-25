# Unstated outside-option assumption in screening proposition (planted)

Draft proposition note for Track T (`theory_conjecture.py`):

> **Proposition 1 (Faulty draft).** Consider a two-type buyer with valuations
> $0 < \theta_L < \theta_H$, high-type share $\mu \in (0, 1)$, quadratic cost
> $c(q) = \frac{1}{2} c q^2$, and any non-negative reservation utility
> $\bar{u}(\theta) = \kappa \theta$ with $\kappa \ge 0$. At the principal's
> optimal screening menu, $IR_L$ and $IC_H$ bind, $q_H^* = \theta_H / c$,
> $q_L^* = \max\{0, (\theta_L - \mu \theta_H)/((1-\mu)c)\}$, and high-type
> participation $IR_H$ is slack.

Why this fails verification:

1. **Refuted by exact counterexample (`search_conjecture_counterexample`):**
   At $\theta_L = 1.0$, $\theta_H = 1.5$, $\mu = 0.5$, $c = 1.0$, and
   $\kappa = 0.75$, the standard downward-distorted quantity is
   $q_L^{std} = 0.50 < \kappa = 0.75$. Evaluating the $(IR_L, IC_H)$-binding
   transfer gives indirect utility $u_H = 0.75 \times 1.0 + 0.5 \times 0.50 = 1.00$,
   which falls below $\bar{u}(\theta_H) = 0.75 \times 1.5 = 1.125$ by an exact
   deficit of $1/8 = 0.125$.
2. **Missing domain assumptions (`audit_proof_assumptions`):**
   The draft states $\kappa \ge 0$ rather than restricting to
   `outside_slope == 0` (or $q_L^{std} \ge \kappa$), and omits `interior_low_type`
   ($\theta_L > \mu \theta_H$) needed for strict slackness of $IR_H$ when $\kappa = 0$.
