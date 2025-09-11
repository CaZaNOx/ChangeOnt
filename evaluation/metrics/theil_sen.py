# FILE: evaluation/metrics/theil_sen.py
from typing import List
import numpy as np

def theil_sen_slope(xs: List[int], ys: List[float], max_pairs: int = 400) -> float:
    n = len(xs)
    if n < 2:
        return 0.0
    pairs = []
    step = max(1, n // int(np.sqrt(max_pairs)))
    idxs = list(range(0, n, step))
    for i in idxs:
        for j in idxs:
            if j > i and xs[j] != xs[i]:
                pairs.append((ys[j] - ys[i]) / (xs[j] - xs[i]))
                if len(pairs) >= max_pairs:
                    break
        if len(pairs) >= max_pairs:
            break
    if not pairs:
        return 0.0
    return float(np.median(np.array(pairs, dtype=np.float32)))
