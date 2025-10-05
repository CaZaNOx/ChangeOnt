# agents/co/core/primitives/loops/finite.py
from __future__ import annotations
from typing import List

def find_period(sequence: List[int], max_period: int | None = None) -> int:
    """
    Return the smallest period L ≥ 1 such that s[i] == s[i+L] for all valid i,
    if one exists; otherwise return 0 (no reliable period).
    """
    n = len(sequence)
    if n < 2:
        return 0
    if max_period is None:
        max_period = n // 2
    for L in range(1, max_period + 1):
        ok = True
        for i in range(n - L):
            if sequence[i] != sequence[i + L]:
                ok = False
                break
        if ok:
            return L
    return 0
