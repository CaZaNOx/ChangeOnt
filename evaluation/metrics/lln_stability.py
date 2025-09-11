from __future__ import annotations
from typing import Iterable, Tuple

def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / float(len(a | b))

def lln_stability(windows: Iterable[Tuple[set, set]], threshold: float = 0.9) -> bool:
    """
    windows: iterable of pairs (S_t, S_{t+1}), sets of observed transitions in successive windows.
    Returns True if all successive Jaccard similarities >= threshold.
    """
    for (s1, s2) in windows:
        if jaccard(s1, s2) < threshold:
            return False
    return True
