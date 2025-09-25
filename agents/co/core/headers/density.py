# PATH: agents/co/core/headers/density.py
from __future__ import annotations
from typing import Sequence, Tuple
import math

def compute_density_signals(history: Sequence[int], A: int, L: int) -> Tuple[float, float]:
    """(entropy_norm ∈[0,1], max_bin_density ∈[0,1]) over tail of length L."""
    A = max(1, int(A)); L = max(1, int(L))
    tail = list(history[-L:])
    if not tail: return 0.0, 0.0
    counts = [0]*A
    for x in tail:
        if 0 <= x < A:
            counts[x] += 1
    total = len(tail)
    probs = [c/total for c in counts if c > 0]
    if not probs: return 0.0, 0.0
    H = -sum(p*math.log(p + 1e-12, 2) for p in probs)
    Hmax = math.log(min(A, total), 2) if A > 1 else 1.0
    entropy_norm = (H/Hmax) if Hmax > 0 else 0.0
    max_density = max(counts)/total
    return max(0.0, min(1.0, entropy_norm)), max(0.0, min(1.0, max_density))

def density_header_decision(entropy_norm: float, max_density: float, *, lo: float=0.3, hi: float=0.7) -> bool:
    """Gate example: low entropy & dominant bin -> exploit."""
    return (entropy_norm <= lo) and (max_density >= hi)
