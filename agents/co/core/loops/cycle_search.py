from __future__ import annotations
from typing import Sequence, Tuple
import math

def min_mean_cycle(weights: Sequence[Sequence[float]]) -> Tuple[float, int]:
    """
    Thin wrapper around Karp; kept in its own module for dependency hygiene.
    Returns (minimum_mean, node_index).
    """
    n = len(weights)
    if n == 0:
        return (math.inf, -1)
    # inline Karp (local copy to avoid import cycle)
    dp = [[math.inf] * n for _ in range(n + 1)]
    for v in range(n): dp[0][v] = 0.0
    for k in range(1, n + 1):
        for v in range(n):
            best = math.inf
            row = dp[k - 1]
            for u in range(n):
                w = weights[u][v]
                if math.isfinite(w) and math.isfinite(row[u]):
                    val = row[u] + w
                    if val < best:
                        best = val
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
