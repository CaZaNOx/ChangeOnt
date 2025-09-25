# PATH: agents/co/core/headers/loop_score.py
from __future__ import annotations
from typing import Sequence
from agents.co.core.loops.loop_measure import ema, loopiness_from_costs

def loop_score_ema(prev: float, costs: Sequence[float], *, beta: float=0.9) -> float:
    return ema(prev, loopiness_from_costs(costs, beta=beta), beta)
