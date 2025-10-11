# agents/co/core/primitives/identity.py
from __future__ import annotations
from typing import Iterable, List, Tuple

def _lev(a: List, b: List) -> int:
    n, m = len(a), len(b)
    if n == 0: return m
    if m == 0: return n
    dp = list(range(m+1))
    for i in range(1, n+1):
        prev, dp[0] = dp[0], i
        for j in range(1, m+1):
            ins = dp[j-1] + 1
            dele = dp[j] + 1
            sub = prev + (0 if a[i-1] == b[j-1] else 1)
            prev, dp[j] = dp[j], min(ins, dele, sub)
    return dp[m]

def bend_distance(path: Iterable, other: Iterable) -> float:
    """Simple edit distance as a bend-cost proxy."""
    a, b = list(path), list(other)
    return float(_lev(a, b))

def same(path: Iterable, other: Iterable, eps: float) -> bool:
    return bend_distance(path, other) <= eps

def closure(paths: List[Tuple], eps: float) -> List[List[Tuple]]:
    """Cluster by same(.,.,eps) via greedy pass."""
    clusters: List[List[Tuple]] = []
    for p in paths:
        placed = False
        for C in clusters:
            if any(same(p, q, eps) for q in C):
                C.append(p); placed = True; break
        if not placed:
            clusters.append([p])
    return clusters
