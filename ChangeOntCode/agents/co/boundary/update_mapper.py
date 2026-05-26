"""Map environment feedback into bounded public update fields for the kernel.

The mapper converts realized/unrealized candidate feedback into public update
structure without creating hidden policy rankings.
"""
from __future__ import annotations
from typing import Any, Dict

def _clip01(value: Any, default: float = 0.0) -> float:
    try:
        v = float(value)
    except Exception:
        return float(default)
    if v < 0.0:
        return 0.0
    if v > 1.0:
        return 1.0
    return v

def _actions_from_observation(observation: Dict[str, Any]):
    actions = list(observation.get("action_space") or [])
    if actions:
        return actions
    out = []
    for cand in list(observation.get("candidates") or []):
        if isinstance(cand, dict) and cand.get("candidate_id") is not None:
            out.append(cand.get("candidate_id"))
    return out

def map_feedback_update(observation: Dict[str, Any], feedback: Dict[str, Any], _primitives: Dict[str, Any], signal_bus: Dict[str, Any], _cfg: Dict[str, Any]) -> Dict[str, Any]:
    actions = _actions_from_observation(observation)
    realized = feedback.get("action", None)
    reward = float(feedback.get("reward", 0.0) or 0.0)
    signals = dict(signal_bus or {})
    continuity = _clip01(signals.get("EC_Identity.continuity_conf", signals.get("EC_Identity.same", 0.5)), 0.5)
    fracture = _clip01(signals.get("EC_Identity.fracture_pressure", 1.0 - continuity), 1.0 - continuity)
    outcome = "positive" if reward > 0.0 else ("negative" if reward < 0.0 else "neutral")
    return {
        "realized_candidate": realized,
        "unrealized_candidates": [a for a in actions if a != realized],
        "reward": reward,
        "outcome": outcome,
        "continuity_update": _clip01(continuity + (0.05 if reward >= 0.0 else -0.08), continuity),
        "fracture_update": _clip01(fracture + (0.10 if reward < 0.0 else -0.04), fracture),
        "branch_update": float(1.0 if reward < 0.0 else 0.0),
        "confidence_update": _clip01(0.50 + 0.35 * max(0.0, reward), 0.5),
        "notes": {"translator_mode": "thin_boundary_update"},
    }
