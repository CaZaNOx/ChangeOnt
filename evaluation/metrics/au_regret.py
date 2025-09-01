# FILE: evaluation/metrics/au_regret.py
from typing import List
import numpy as np

def au_regret_window(rewards_agent: List[float], rewards_base: List[float], win: int = 100) -> float:
    """
    Renewal-weighted AU-regret proxy:
    average per-window improvement (agent - base), clipped at 0.
    """
    n = min(len(rewards_agent), len(rewards_base))
    if n == 0:
        return 0.0
    diffs = []
    for i in range(0, n, win):
        a = rewards_agent[i:i+win]
        b = rewards_base[i:i+win]
        if not a or not b: break
        diffs.append(max(0.0, (sum(a) - sum(b)) / len(a)))
    if not diffs:
        return 0.0
    return float(sum(diffs) / len(diffs))
