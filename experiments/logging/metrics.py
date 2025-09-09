from __future__ import annotations
from typing import Iterable, List, Sequence, Tuple
import math
import statistics

def theil_sen_slope(xs: Sequence[float], ys: Sequence[float], max_pairs: int = 400) -> float:
    n = len(xs)
    if n < 2:
        return 0.0
    pairs: List[float] = []
    # sample pairs up to max_pairs for speed
    step = max(1, int(math.sqrt(n)))
    count = 0
    for i in range(0, n, step):
        for j in range(i+1, n, step):
            dx = xs[j] - xs[i]
            if dx == 0:
                continue
            pairs.append((ys[j] - ys[i]) / dx)
            count += 1
            if count >= max_pairs:
                break
        if count >= max_pairs:
            break
    if not pairs:
        return 0.0
    return statistics.median(pairs)

def au_regret_window(truth: Sequence[int], preds: Sequence[int]) -> float:
    """Toy AU-Regret: 1 - accuracy over the sequence (placeholder)."""
    if not truth:
        return 0.0
    correct = sum(1 for t, p in zip(truth, preds) if t == p)
    acc = correct / len(truth)
    return 1.0 - acc

def fdr_windowed(decisions: Sequence[int], ground_truth: Sequence[int]) -> float:
    """False Discovery Rate over a window: FP / max(1, (FP + TP)). decisions=1 means 'positive'."""
    fp = 0
    tp = 0
    for d, g in zip(decisions, ground_truth):
        if d == 1 and g == 0:
            fp += 1
        elif d == 1 and g == 1:
            tp += 1
    denom = fp + tp
    if denom == 0:
        return 0.0
    return fp / denom
