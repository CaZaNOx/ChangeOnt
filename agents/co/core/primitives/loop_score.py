# PATH: agents/co/core/loops/loop_score.py
from __future__ import annotations
from typing import Sequence
import math

def ema(prev: float, x: float, beta: float) -> float:
    beta = float(max(0.0, min(1.0, beta)))
    return beta*float(prev) + (1.0 - beta)*float(x)

def _squash_pos(x: float) -> float:
    # map (0,∞) → (0,1); lower cost ⇒ higher score
    return 1.0/(1.0 + max(0.0, x))

def loopiness_from_costs(cycle_costs: Sequence[float], *, beta: float=0.9) -> float:
    vals = [float(c) for c in cycle_costs if math.isfinite(c)]
    if not vals:
        return 0.0
    mean = sum(vals)/len(vals)
    return _squash_pos(mean)
