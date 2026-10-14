"""Part C: estimate a rare probability honestly. TODO 4, 6 and 7."""
from __future__ import annotations

import math

import numpy as np

from avsim import space
from .search import proposal_logpdf


def wilson_ci(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """TODO 4. Wilson score interval for k successes in n trials. Must behave at k = 0 (lower bound 0,
    upper bound > 0) where the plain normal interval collapses to [0, 0]. Return (0, 1) for n = 0."""
    if n <= 0:
        return 0.0, 1.0
    if k <= 0:
        return 0.0, (z * z) / (n + z * z)
    if k >= n:
        return n / (n + z * z), 1.0
    p = k / n
    z2 = z * z
    denom = 1.0 + z2 / n
    center = (p + z2 / (2.0 * n)) / denom
    half = z * math.sqrt(p * (1.0 - p) / n + z2 / (4.0 * n * n)) / denom
    return max(0.0, center - half), min(1.0, center + half)


def log_weights(Z, Bn, nat: space.Natural, prop: dict, beta: float = 0.2) -> np.ndarray:
    """TODO 6. log p(u) - log q(u) for each row, where q is the DEFENSIVE MIXTURE
    q = (1 - beta) * proposal + beta * natural.

    nat.logpdf(Z, Bn) gives log p; proposal_logpdf(prop, Z, Bn) gives log of the CEM proposal.
    Use np.logaddexp so a weight of 1e-30 does not underflow to 0."""
    logp = nat.logpdf(Z, Bn)
    logq_cem = proposal_logpdf(prop, Z, Bn)
    with np.errstate(divide="ignore", invalid="ignore"):
        logq = np.logaddexp(np.log1p(-beta) + logq_cem, np.log(beta) + logp)
    return logp - logq


def is_estimate(logw: np.ndarray, y: np.ndarray, z: float = 1.96) -> dict:
    """TODO 7. Importance-sampling estimate of P(y = 1) under the natural distribution.

    w = exp(logw); p = mean(w * y)  (NOT normalised by sum(w): that version is biased for small n);
    se = std(w * y, ddof=1) / sqrt(n); CI = [max(0, p - z se), p + z se];
    Kish effective sample size ess = (sum w)^2 / sum(w^2).
    Return dict(p=, lo=, hi=, se=, ess=, n=)."""
    logw = np.asarray(logw, dtype=float)
    y = np.asarray(y, dtype=float)
    n = int(y.size)
    if logw.size != n:
        raise ValueError("logw and y must have the same number of samples")
    if n == 0:
        return dict(p=0.0, lo=0.0, hi=0.0, se=0.0, ess=0.0, n=0)
    with np.errstate(over="ignore", under="ignore", invalid="ignore"):
        w = np.exp(logw)
        weighted = w * y
        p = float(np.mean(weighted))
        se = float(np.std(weighted, ddof=1) / math.sqrt(n)) if n > 1 else 0.0
        sum_w = float(np.sum(w))
        sum_w2 = float(np.sum(w * w))
    ess = sum_w * sum_w / sum_w2 if sum_w2 > 0 else 0.0
    return dict(p=p, lo=max(0.0, p - z * se), hi=p + z * se, se=se, ess=ess, n=n)


def rule_of_three(n_eff: float) -> float:
    """Given: 95% upper bound on a probability when 0 events were seen in n_eff independent tries."""
    return 3.0 / max(n_eff, 1.0)
