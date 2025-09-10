# FILE: evaluation/metrics/volatility.py
from typing import Sequence
import numpy as np

def jaccard_volatility(seq: Sequence[int], W: int = 200) -> float:
    """
    Volatility proxy on raw observations:
      V = 1 - Jaccard(S_{t-W}, S_t), where S_* are sets of symbols in W-sized windows.
    If insufficient length, returns 1.0 (max volatility).
    """
    if len(seq) < 2 * W:
        return 1.0
    A = set(seq[-2*W:-W])
    B = set(seq[-W:])
    if not A and not B:
        return 0.0
    inter = len(A & B)
    union = len(A | B)
    if union == 0:
        return 0.0
    return float(1.0 - inter / union)
