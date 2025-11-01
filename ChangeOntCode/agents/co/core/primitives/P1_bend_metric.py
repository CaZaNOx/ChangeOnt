# agents/co/core/primitives/P1_bend_metric.py
from typing import Iterable, Sequence, Any

def _edit_distance(a: Sequence[Any], b: Sequence[Any], sub_cost=1, ins_cost=1, del_cost=1) -> int:
    """Classic Levenshtein (small, dependency-free)."""
    n, m = len(a), len(b)
    if n == 0: return m
    if m == 0: return n
    dp = list(range(m + 1))
    for i in range(1, n + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, m + 1):
            cur = dp[j]
            cost = 0 if a[i-1] == b[j-1] else sub_cost
            dp[j] = min(dp[j] + 1,         # deletion
                        dp[j-1] + 1,       # insertion
                        prev + cost)       # substitution
            prev = cur
    return dp[m]


def bend_distance(path, path_prime, metric: str = "edit", tau: float = 0.0) -> float:
    """
    Lawvere bend distance: inf bend budget to turn path->path'.
    Minimal implementation via edit distance (strings/sequences).
    """
    if metric == "edit":
        return float(_edit_distance(path, path_prime))
    elif metric == "hamming":
        assert len(path) == len(path_prime)
        return float(sum(int(x != y) for x, y in zip(path, path_prime)))
    else:
        # Placeholder for DTW or other metrics
        return float(_edit_distance(path, path_prime))

def is_same(path, path_prime, tau: float) -> bool:
    """Within-tolerance identity."""
    return bend_distance(path, path_prime, "edit", tau) <= tau

def closure(paths: Iterable[Sequence[Any]], eps: float) -> list[Sequence[Any]]:
    """Return a simple ε-closure by removing near-duplicates (greedy medoids)."""
    paths = list(paths)
    kept: list[Sequence[Any]] = []
    for p in paths:
        if not any(bend_distance(p, q, "edit") <= eps for q in kept):
            kept.append(p)
    return kept
