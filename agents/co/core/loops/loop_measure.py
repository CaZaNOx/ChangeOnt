from __future__ import annotations
from typing import Sequence, Iterable, Tuple
import math

def ema(prev: float, x: float, beta: float) -> float:
    return beta * prev + (1 - beta) * x

def normalize(x: float, eps: float = 1e-9) -> float:
    return max(0.0, min(1.0, x / (x + 1.0 + eps)))

def loopiness_from_costs(
    cycle_costs: Sequence[float],
    *,
    beta: float = 0.9,
) -> float:
    """
    Cheap loopiness surrogate from a stream of cycle-cost estimates.
    Lower costs over time increase 'loopiness'; smoothed via EMA; squashed to [0,1].
    """
    if not cycle_costs:
        return 0.0
    s = 0.0
    for c in cycle_costs:
        s = ema(s, -float(c), beta)  # cheaper cycles -> larger negative costs -> larger s
    return normalize(max(0.0, s))

def min_mean_cycle_karp(weights: Sequence[Sequence[float]]) -> Tuple[float, int]:
    """
    Karp's algorithm for minimum mean cycle in a weighted directed graph.
    weights[i][j] is cost of edge i->j (math.inf if absent).
    Returns (mu*, argmin_node). math.inf if no cycles.
    """
    n = len(weights)
    if n == 0:
        return math.inf, -1
    dp = [[math.inf] * n for _ in range(n + 1)]
    for v in range(n):
        dp[0][v] = 0.0
    for k in range(1, n + 1):
        for v in range(n):
            best = math.inf
            row = dp[k - 1]
            for u in range(n):
                w = weights[u][v]
                if math.isfinite(w) and math.isfinite(row[u]):
                    best = min(best, row[u] + w)
            dp[k][v] = best
    mu_best = math.inf
    arg = -1
    for v in range(n):
        numer = -math.inf
        for k in range(n):
            if math.isfinite(dp[n][v]) and math.isfinite(dp[k][v]):
                numer = max(numer, (dp[n][v] - dp[k][v]) / (n - k))
        if numer < mu_best:
            mu_best = numer
            arg = v
    return mu_best, arg
