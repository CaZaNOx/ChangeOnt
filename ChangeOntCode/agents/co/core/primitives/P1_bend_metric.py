# agents/co/core/primitives/P1_bend_metric.py
from typing import Iterable, Sequence, Any, List

# Binding v1 constants
L = 12
PAD_TOKEN = -1
PAD_COST = 0.25
MISMATCH_COST = 1.0

def _normalize(trace: Sequence[Any]) -> List[Any]:
    t = list(trace)
    if len(t) > L:
        t = t[-L:]
    if len(t) < L:
        t = [PAD_TOKEN] * (L - len(t)) + t
    return t

def bend_distance(path, path_prime, metric: str = "edit", tau: float = 0.0) -> float:
    """
    Binding v1 bend distance: warped-Hamming with left padding.
    Metric/tau args are accepted for compatibility but ignored.
    """
    a = _normalize(path)
    b = _normalize(path_prime)
    cost = 0.0
    for x, y in zip(a, b):
        if x == PAD_TOKEN and y == PAD_TOKEN:
            cost += 0.0
        elif x == PAD_TOKEN or y == PAD_TOKEN:
            cost += PAD_COST
        elif x == y:
            cost += 0.0
        else:
            cost += MISMATCH_COST
    return cost / float(L)

def is_same(path, path_prime, tau: float) -> bool:
    """Within-tolerance identity."""
    return bend_distance(path, path_prime, "edit", tau) <= tau

def d_bend(trace_a: List[int], trace_b: List[int]) -> float:
    """Canonical P1 bend distance (alias of bend_distance v1)."""
    return float(bend_distance(trace_a, trace_b))

def closure(paths: Iterable[Sequence[Any]], eps: float) -> list[Sequence[Any]]:
    """Return a simple ε-closure by removing near-duplicates (greedy medoids)."""
    paths = list(paths)
    kept: list[Sequence[Any]] = []
    for p in paths:
        if not any(bend_distance(p, q, "edit") <= eps for q in kept):
            kept.append(p)
    return kept
