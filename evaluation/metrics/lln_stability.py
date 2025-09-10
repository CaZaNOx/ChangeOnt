# FILE: evaluation/metrics/lln_stability.py
from typing import Sequence, Tuple
import numpy as np
from .volatility import jaccard_volatility

def lln_stable(seq: Sequence[int], W: int = 200, drift_thresh: float = 0.10, consecutive: int = 3, floor: int = 50) -> Tuple[bool, int]:
    """
    LLN-stability flag:
      - Volatility ≤ drift_thresh for 'consecutive' windows,
      - and each observed symbol appears at least 'floor' times overall.
    Returns (stable: bool, windows_checked: int).
    """
    n = len(seq)
    if n < W * (consecutive + 1):
        return (False, 0)

    # Sliding check of volatility
    ok_count = 0
    windows_checked = 0
    for i in range(consecutive):
        end = n - i * W
        start = end - 2 * W
        if start < 0: break
        v = jaccard_volatility(seq[start:end], W=W)
        windows_checked += 1
        if v <= drift_thresh:
            ok_count += 1

    # Sample floor
    counts = {}
    for s in seq:
        counts[s] = counts.get(s, 0) + 1
    floor_ok = all(c >= floor for c in counts.values()) if counts else False

    return (ok_count >= consecutive and floor_ok, windows_checked)
