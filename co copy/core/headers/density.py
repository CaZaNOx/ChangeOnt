# agents/co/core/headers/density.py
from __future__ import annotations

from collections import Counter
from typing import Iterable, List, Optional, Tuple


def _last_window(history: Iterable[int], L: int) -> List[int]:
    """
    Return the last L items of history as a list.
    Works even if history is a deque, generator, etc. (which don't support slicing).
    """
    if L <= 0:
        return []
    # Convert once, then slice
    h = list(history)
    return h[-L:]


def density_rho(history: Iterable[int], L: int, A: Optional[int] = None) -> Tuple[float, float]:
    """
    Simple density signal over a sliding window of length L.

    Returns:
      rho    : max empirical probability (mode frequency / window size)
      rho_ex : 'excess' density above uniform baseline (max(p) - 1/A, lower-bounded at 0)
    """
    window = _last_window(history, L)
    n = len(window)
    if n == 0:
        return 0.0, 0.0

    counts = Counter(window)
    p_max = max(counts.values()) / float(n)

    if A is None:
        # If alphabet size not provided, infer from window (fallback to 1 to avoid div-by-zero)
        A = max(1, len(counts))

    uniform = 1.0 / float(A)
    rho = p_max
    rho_ex = max(0.0, p_max - uniform)
    return rho, rho_ex


def compute_density_signals(history: Iterable[int], A: int, L: int) -> Tuple[float, float]:
    """
    Thin wrapper used by agents: consistent call surface.
    """
    return density_rho(history, L=L, A=A)
