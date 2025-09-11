from __future__ import annotations
from typing import Sequence, Optional

def warped_bend_distance(
    a: Sequence[int],
    b: Sequence[int],
    *,
    pad_weight: float = 0.25,
    gauge_weights: Optional[Sequence[float]] = None,
) -> float:
    """
    Lightweight warped Hamming distance between two recent token traces (equal length not required).
    - pad_weight penalizes ⌀ padding when aligning different lengths.
    - gauge_weights (optional) down-weights positions.
    """
    la, lb = len(a), len(b)
    L = max(la, lb)
    if L == 0:
        return 0.0
    score = 0.0
    for i in range(L):
        wa = a[i] if i < la else None
        wb = b[i] if i < lb else None
        w = 1.0
        if gauge_weights is not None and i < len(gauge_weights):
            w = max(0.0, float(gauge_weights[i]))
        if wa is None or wb is None:
            score += w * pad_weight
        else:
            score += w * (0.0 if wa == wb else 1.0)
    return score / float(L)

def header_agreement(h1: dict, h2: dict) -> bool:
    """Two simple headers must match to allow merge."""
    return (h1.get("collapse") == h2.get("collapse")) and (h1.get("density") == h2.get("density"))
