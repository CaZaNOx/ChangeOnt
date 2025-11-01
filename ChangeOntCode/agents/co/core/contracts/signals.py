# agents/co/core/contracts/signals.py
from __future__ import annotations
from typing import Any, Dict, Mapping

SignalBus = Dict[str, Any]          # flat, namespaced keys: "EA_HAQ.novelty" -> 0.23
ActionScores = Dict[Any, float]     # {action -> score}
Mask = set                           # set of illegal/blocked actions

def merge_signals(bus: SignalBus, ns: str, payload: Mapping[str, Any]) -> None:
    """
    Copy 'payload' into 'bus' under the namespace 'ns'.
    """
    if not isinstance(payload, Mapping):
        return
    for k, v in payload.items():
        bus[f"{ns}.{k}"] = v

def normalize_scores(scores: ActionScores) -> ActionScores:
    """
    Affine-normalize scores into [0,1] when possible; otherwise return a shallow copy.
    """
    if not scores:
        return {}
    vals = list(scores.values())
    lo, hi = min(vals), max(vals)
    if hi <= lo:
        return dict((a, 0.5) for a in scores.keys())
    rng = hi - lo
    return {a: (s - lo) / rng for a, s in scores.items()}