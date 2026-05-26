"""Translate public observation/candidate facts into thin CO evidence channels.

Implements the fail-closed boundary discipline: when no public candidate facts
exist, the mapper returns empty evidence rather than uniform or first-legal
proposal scores.
"""
from __future__ import annotations
from typing import Any, Dict, List, Set, Tuple

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

def _actions_from_observation(observation: Dict[str, Any]) -> List[Any]:
    actions = list(observation.get("action_space") or [])
    if actions:
        return actions
    out: List[Any] = []
    for cand in list(observation.get("candidates") or []):
        if isinstance(cand, dict) and cand.get("candidate_id") is not None:
            out.append(cand.get("candidate_id"))
    return out

def translate_observation(
    observation: Dict[str, Any],
    _header: Any,
    _primitives: Dict[str, Any],
    _signal_bus: Dict[str, Any],
    _cfg: Dict[str, Any],
) -> Tuple[Dict[Any, float], Set[Any], Dict[str, Any]]:
    actions = _actions_from_observation(observation)
    candidates = [c for c in list(observation.get("candidates") or []) if isinstance(c, dict)]
    if candidates:
        scores: Dict[Any, float] = {}
        mask: Set[Any] = set()
        for cand in candidates:
            cid = cand.get("candidate_id")
            if cid is None:
                continue
            if not bool(cand.get("legal", True)):
                mask.add(cid)
                continue
            goal = _clip01(cand.get("goal_relation", cand.get("visible_delta", 0.0)), 0.0)
            support = _clip01(cand.get("support_depth", 0.0), 0.0)
            continuity = _clip01(cand.get("continuity_support", 0.0), 0.0)
            uncertainty = _clip01(cand.get("uncertainty_hint", 0.5), 0.5)
            obstruction = _clip01(cand.get("obstruction_hint", cand.get("contradiction_hint", 0.0)), 0.0)
            scores[cid] = max(0.0, 0.42 * goal + 0.26 * support + 0.18 * continuity + 0.08 * (1.0 - uncertainty) - 0.14 * obstruction)
        return scores, mask, {"candidate_field_driven": bool(scores), "translator_mode": "thin_boundary_candidate_field"}
    # Fail closed instead of inventing a uniform candidate field.  A canonical
    # evidence-bearing route requires candidate/public-effect structure from the
    # boundary or adapter.  Returning empty scores lets the downstream kernel
    # raise/log a contract violation instead of silently rescuing with a
    # non-CO policy.
    mask: Set[Any] = set()
    return {}, mask, {
        "candidate_field_driven": False,
        "translator_mode": "thin_boundary_empty_fail_closed",
        "co_evidence_valid_for_step": False,
        "boundary_contract_violation": "no_public_candidate_field",
    }
