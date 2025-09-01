# FILE: evaluation/metrics/fdr_windowed.py
from typing import List

def fdr_windowed(flip_times: List[int], event_times: List[int], delta: int = 6) -> float:
    """
    Fraction of flips that lie within ±delta of any event time.
    (We often log the complement 'false discovery rate' in prose; here we return alignment rate.)
    """
    if not flip_times:
        return 0.0
    E = sorted(set(int(e) for e in event_times))
    hits = 0
    for f in flip_times:
        ok = any(abs(f - e) <= delta for e in E)
        if ok: hits += 1
    return float(hits / max(1, len(flip_times)))
