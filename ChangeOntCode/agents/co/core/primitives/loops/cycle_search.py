# PATH: agents/co/core/loops/cycle_search.py
from __future__ import annotations
from typing import Sequence, Tuple
import math

def karp_min_mean_cycle(weights: Sequence[Sequence[float]]) -> Tuple[float, int]:
    """Karp’s min mean cycle value (mu) and arg node. Finite, no external deps."""
    n = len(weights)
    if n == 0:
        return math.inf, -1
    dp = [[math.inf]*n for _ in range(n+1)]
    for v in range(n):
        dp[0][v] = 0.0
    for k in range(1, n+1):
        prev = dp[k-1]; cur = dp[k]
        for v in range(n):
            best = math.inf
            for u in range(n):
                w = weights[u][v]
                if math.isfinite(w) and math.isfinite(prev[u]):
                    cand = prev[u] + w
                    if cand < best:
                        best = cand
            cur[v] = best
    mu_best = math.inf; arg = -1
    for v in range(n):
        numer = -math.inf
        for k in range(n):
            if math.isfinite(dp[n][v]) and math.isfinite(dp[k][v]) and n != k:
                numer = max(numer, (dp[n][v]-dp[k][v])/(n-k))
        if numer < mu_best:
            mu_best = numer; arg = v
    return mu_best, arg

def johnson_simple_cycles_limited(adj: Sequence[Sequence[int]], *, limit: int=1024) -> int:
    """Crude bounded simple-cycle count for pressure signal; safe and finite."""
    n = len(adj)
    seen = 0
    visited = [False]*n
    stack = []

    def dfs(u: int, start: int) -> None:
        nonlocal seen
        if seen >= limit:
            return
        visited[u] = True
        stack.append(u)
        for v in range(n):
            if adj[u][v]:
                if v == start and len(stack) > 1:
                    seen += 1
                    if seen >= limit:
                        break
                if not visited[v]:
                    dfs(v, start)
        stack.pop()
        visited[u] = False

    for s in range(n):
        dfs(s, s)
        if seen >= limit:
            break
    return seen
