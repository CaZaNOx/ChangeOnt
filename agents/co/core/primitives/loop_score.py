# agents/co/core/primitives/loop_score.py
from __future__ import annotations
from typing import List
from .loops.finite import find_period

def loop_score(sequence: List[int]) -> float:
    """
    Heuristic: score ∈ [0,1] measuring how 'loop-like' a sequence is.
      - Find a candidate period L (if any).
      - Compare sequence against its L-shifted self; fraction of matches is the score.
    """
    if not sequence:
        return 0.0
    L = find_period(sequence)
    if L <= 0 or L >= len(sequence):
        return 0.0
    matches = 0
    total = len(sequence) - L
    if total <= 0:
        return 0.0
    for i in range(total):
        if sequence[i] == sequence[i + L]:
            matches += 1
    return matches / float(total)
