# agents/co/integration/translators/bandit_translator.py
from __future__ import annotations
from typing import Any, Dict, Tuple, List
import math
from agents.co.core.contracts.signals import normalize_scores
from agents.co.core.contracts.path_space import normalize_fragment

def _meta_priors(primitives: Dict[str, Any]) -> Dict[str, Any]:
    mh = primitives.get("_meta_header")
    try:
        return mh.to_dict() if mh is not None and hasattr(mh, "to_dict") else {}
    except Exception:
        return {}

def translate(
    observation: Dict[str, Any],
    header: Any,
    primitives: Dict[str, Any],
    co_bus: Dict[str, Any],
    cfg: Dict[str, Any],
) -> Tuple[Dict[Any, float], set, Dict[str, Any]]:
    """translator_mask is a *blocklist* of invalid/blocked actions."""
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



def translate_feedback(
    last_observation: Dict[str, Any],
    feedback: Dict[str, Any],
    header: Any,
    primitives: Dict[str, Any],
    co_bus: Dict[str, Any],
    cfg: Dict[str, Any],
) -> Dict[str, Any]:
    obs = dict(last_observation or {})
    fb = dict(feedback or {})
    n_arms = int(obs.get("n_arms", 0) or 0)
    action = int(fb.get("action", obs.get("last_action", 0) or 0)) if n_arms else int(fb.get("action", 0) or 0)
    reward = float(fb.get("reward", 0.0) or 0.0)
    done = bool(fb.get("done", False))
    t = int(obs.get("t", 0) or 0)
    branch_space = []
    bs = primitives.get("bandit_stats")
    if bs is not None and all(hasattr(bs, k) for k in ("ensure", "means", "counts")):
        try:
            bs.ensure(max(n_arms, action + 1))
            for a in range(max(n_arms, action + 1)):
                mean = float(bs.means[a]) if a < len(bs.means) else 0.0
                count = int(bs.counts[a]) if a < len(bs.counts) else 0
                branch_space.append({
                    "candidate_ref": f"arm:{a}",
                    "parent_ref": f"bandit:t{t}",
                    "branch_weight": mean,
                    "selection_bias": 1.0 / max(1, count),
                    "constraint_status": "open",
                })
        except Exception:
            pass
    return normalize_fragment({
        "family": "bandit",
        "t": t + 1,
        "path_depth": t + 1,
        "prior_refs": [f"bandit:t{t}"],
        "anchor_id": f"bandit:arm:{action}",
        "realized_segment": [{
            "from_ref": f"bandit:t{t}",
            "to_ref": f"bandit:t{t+1}",
            "action_ref": f"arm:{action}",
            "order_rank": t + 1,
            "transition_weight": reward,
            "bend_local": abs(reward),
            "delta_signature": {"reward": reward, "done": done},
        }],
        "branch_space": branch_space,
        "feedback_fragment": {
            "action": action,
            "reward": reward,
            "done": done,
        },
        "structural_profiles": {"reward_magnitude": abs(reward)},
        "regime_profiles": {"done": done},
        "meta_priors": _meta_priors(primitives),
    }, family="bandit")
