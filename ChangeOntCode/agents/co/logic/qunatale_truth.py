# agents/co/logic/quantale_truth.py
from typing import Iterable

INF = float("inf")

def q_and(a: float, b: float) -> float:
    """Conjunction in Lawvere quantale (max)."""
    return max(a, b)

def q_or(a: float, b: float) -> float:
    """Disjunction (min)."""
    return min(a, b)

def q_then(a: float, b: float) -> float:
    """Sequential composition (min-plus 'tensor')."""
    return a + b

def q_imp(a: float, b: float) -> float:
    """Implication via residuation (truncated subtraction)."""
    return max(0.0, b - a)

def q_big_and(vals: Iterable[float]) -> float:
    m = 0.0
    for v in vals: m = q_and(m, v)
    return m

def q_big_or(vals: Iterable[float]) -> float:
    m = INF
    for v in vals: m = q_or(m, v)
    return m
