# agents/co/core/combinators/classic_ops.py
from __future__ import annotations
from typing import Dict, Sequence
import math

def op_classic_plus(a: float, b: float) -> float:
    return a + b

def op_min(a: float, b: float) -> float:
    return a if a <= b else b

def op_max(a: float, b: float) -> float:
    return a if a >= b else b

def op_weighted_sum(vals: Sequence[float], weights: Sequence[float]) -> float:
    z = sum(max(w, 0.0) for w in weights)
    if z <= 0: return sum(vals) / max(1, len(vals))
    return sum(v * max(w, 0.0) for v, w in zip(vals, weights)) / z

def op_softmax_mix(scores: Dict[str, float], temp: float = 1.0) -> Dict[str, float]:
    if len(scores) == 0: return {}
    m = min(scores.values())
    exps = {k: math.exp(-(v - m) / max(1e-6, temp)) for k, v in scores.items()}
    z = sum(exps.values())
    return {k: exps[k] / z for k in scores}
