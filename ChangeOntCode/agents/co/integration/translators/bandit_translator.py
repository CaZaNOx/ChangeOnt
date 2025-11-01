# agents/co/integration/translators/bandit_translator.py
from __future__ import annotations
from typing import Any, Dict, Tuple, List
import math
from agents.co.core.contracts.signals import normalize_scores

def translate(
    observation: Dict[str, Any],
    header: Any,
    primitives: Dict[str, Any],
    co_bus: Dict[str, Any],
    cfg: Dict[str, Any],
) -> Tuple[Dict[Any, float], set, Dict[str, Any]]:
    n_arms = int(observation.get("n_arms", 2))
    actions: List[int] = list(observation.get("action_space") or list(range(n_arms)))
    mask: set = set()
    if n_arms <= 0:
        return ({}, mask, {"reason":"no_arms"})

    eps = float(cfg.get("eps", 0.0))  # ActionHead may pass its eps here

    bs = primitives.get("bandit_stats")
    means = [0.0]*n_arms
    counts = [0]*n_arms
    if bs is not None and all(hasattr(bs,k) for k in ("means","counts","ensure")):
        try:
            bs.ensure(n_arms)
            means = list(bs.means[:n_arms])
            counts = list(bs.counts[:n_arms])
        except Exception:
            pass

    # UCB-style bonus; fall back to eps as a small explore bias via bonus
    t = int(observation.get("t", sum(counts)))
    t = max(1, t)
    scores: Dict[int,float] = {}
    for a in actions:
        n = max(1, counts[a])
        bonus = math.sqrt(2.0 * math.log(t+1) / n) + 0.1*eps
        scores[a] = float(means[a]) + bonus

    return (normalize_scores(scores), mask, {"t":t, "eps":eps})