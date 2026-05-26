# agents/co/integration/translators/renewal_translator.py
from __future__ import annotations
from typing import Any, Dict, Tuple, List
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
    """
    Score symbols using n-gram model when available; fallback predict-last.
    translator_mask is a *blocklist* of invalid/blocked actions.
    """
    A = int(observation.get("A", 0))
    actions: List[int] = list(observation.get("action_space") or list(range(A)))
    mask: set = set()
    if A <= 0:
        return ({}, mask, {"reason":"no_alphabet"})

    obs_sym = int(observation.get("obs", 0))
    # Prefer primitive model
    ng = primitives.get("ngram_model")
    scores: Dict[int, float] = {}
    if ng is not None and all(hasattr(ng, k) for k in ("predict_proba","ensure")):
        try:
            ng.ensure(A)
            proba = ng.predict_proba()  # should return length-A probabilities or dict
            if isinstance(proba, dict):
                for a in actions:
                    scores[a] = float(proba.get(a, 0.0))
            else:
                for a in actions:
                    scores[a] = float(proba[a]) if a < len(proba) else 0.0
        except Exception:
            pass

    if not scores:
        # fallback: predict-last heuristic
        scores = {a: (1.0 if a == obs_sym else 0.0) for a in actions}

    return (normalize_scores(scores), mask, {"fallback": not bool(scores)})



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
    A = int(obs.get("A", 0) or 0)
    t = int(obs.get("t", 0) or 0)
    next_obs = int(fb.get("observation", obs.get("obs", 0)) or 0)
    action = int(fb.get("action", 0) or 0)
    reward = float(fb.get("reward", 0.0) or 0.0)
    done = bool(fb.get("done", False))
    branch_space = [
        {"candidate_ref": f"sym:{a}", "parent_ref": f"renewal:t{t}", "branch_weight": 1.0 if a == next_obs else 0.0, "selection_bias": 1.0, "constraint_status": "open"}
        for a in range(A)
    ]
    return normalize_fragment({
        "family": "renewal",
        "t": t + 1,
        "path_depth": t + 1,
        "prior_refs": [f"renewal:t{t}"],
        "anchor_id": f"renewal:sym:{next_obs}",
        "realized_segment": [{
            "from_ref": f"renewal:sym:{int(obs.get('obs',0) or 0)}",
            "to_ref": f"renewal:sym:{next_obs}",
            "action_ref": action,
            "order_rank": t + 1,
            "transition_weight": reward,
            "bend_local": 0.0 if next_obs == int(obs.get('obs',0) or 0) else 1.0,
            "delta_signature": {"reward": reward, "done": done},
        }],
        "branch_space": branch_space,
        "feedback_fragment": {
            "action": action,
            "reward": reward,
            "done": done,
            "next_obs": next_obs,
        },
        "regime_profiles": {"done": done},
        "meta_priors": _meta_priors(primitives),
    }, family="renewal")
