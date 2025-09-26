# PATH: agents/co/core/headers/density.py
from __future__ import annotations
from typing import List, Tuple


def compute_density_signals(seq: List[int] | List[float], A: int, L: int) -> Tuple[List[float], List[int]]:
    """
    Compute simple categorical densities over the last L items of seq.

    Robustness:
      - Coerces items to int in [0, A-1] by clamping (so callers can pass raw signals).
      - O(A + L) time, small constants; safe for tight loops.

    Returns:
      (dens_smooth, counts)
        dens_smooth: normalized counts / L (length A, floats)
        counts:      raw counts per symbol (length A, ints)
    """
    if L <= 0:
        return [0.0] * A, [0] * A

    counts = [0] * A
    for x in seq[-L:]:
        try:
            xi = int(x)
        except Exception:
            xi = 0
        if xi < 0:
            xi = 0
        elif xi >= A:
            xi = A - 1
        counts[xi] += 1

    invL = 1.0 / float(L)
    dens = [c * invL for c in counts]
    return dens, counts
