# agents/co/integration/translators/maze_translator.py
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
    Turn co_bus + observation into per-direction scores.
    Prefers moving closer to goal; penalizes revisits/density; tiny novelty bonus if present.
    translator_mask is a *blocklist* of invalid/blocked actions.
    """
    pos  = observation.get("pos")
    goal = observation.get("goal")
    H    = observation.get("height")
    W    = observation.get("width")
    grid = observation.get("grid")
    actions: List[str] = list(observation.get("action_space") or ["UP","DOWN","LEFT","RIGHT"])
    mask: set = set()

    if not (isinstance(pos,(list,tuple)) and isinstance(goal,(list,tuple))):
        return ({}, mask, {"reason":"missing_pos_or_goal"})

    pr, pc = int(pos[0]), int(pos[1])
    gr, gc = int(goal[0]), int(goal[1])

    deltas = {"UP":(-1,0),"DOWN":(1,0),"LEFT":(0,-1),"RIGHT":(0,1)}

    def in_bounds(r,c)->bool:
        if H is None or W is None: return True
        return 0 <= r < int(H) and 0 <= c < int(W)

    def free(r,c)->bool:
        if not in_bounds(r,c): return False
        if grid is None: return True
        try:
            return int(grid[r][c]) == 0
        except Exception:
            return True

    # pull optional signal hints
    # density / visited penalty (0..1), novelty (0..1)
    density_pen = float(co_bus.get("EG_DensityPrecision.visit_density", 0.0))
    novelty     = float(co_bus.get("EA_HAQ.novelty", 0.0))

    scores: Dict[str,float] = {}
    for a in actions:
        if a not in deltas: 
            continue
        dr, dc = deltas[a]
        nr, nc = pr + dr, pc + dc
        if not free(nr, nc):
            mask.add(a)
            continue
        # manhattan improvement (negative distance is better after normalization)
        dist_now  = abs(pr - gr) + abs(pc - gc)
        dist_next = abs(nr - gr) + abs(nc - gc)
        improve   = float(dist_now - dist_next)  # >0 is good
        # visiting penalty (prefer unseen cells slightly)
        vt = primitives.get("visit_tracker")
        visited_pen = 0.0
        if vt is not None and hasattr(vt, "score"):
            try:
                visited_pen = float(vt.score((nr,nc)))
            except Exception:
                visited_pen = 0.0
        # combine
        scores[a] = improve - 0.3 * density_pen - 0.2 * visited_pen + 0.05 * novelty

    return (normalize_scores(scores), mask, {"density_pen":density_pen, "novelty":novelty})



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
    t = int(obs.get("t", 0) or 0)
    pos = obs.get("pos")
    next_pos = fb.get("pos", pos)
    action = fb.get("action", obs.get("last_action"))
    reward = float(fb.get("reward", 0.0) or 0.0)
    done = bool(fb.get("done", False))
    truncated = bool(fb.get("truncated", False))
    action_space = list(obs.get("action_space") or ["UP","DOWN","LEFT","RIGHT"])
    blocked = set(fb.get("translator_mask") or [])
    branch_space = [
        {"candidate_ref": str(a), "parent_ref": f"maze:t{t}", "branch_weight": 1.0, "selection_bias": 1.0, "constraint_status": ("blocked" if a in blocked else "open")}
        for a in action_space
    ]
    return normalize_fragment({
        "family": "maze",
        "t": t + 1,
        "path_depth": t + 1,
        "prior_refs": [f"maze:t{t}"],
        "anchor_id": f"maze:{tuple(next_pos) if isinstance(next_pos,(list,tuple)) else next_pos}",
        "realized_segment": [{
            "from_ref": f"maze:{tuple(pos) if isinstance(pos,(list,tuple)) else pos}",
            "to_ref": f"maze:{tuple(next_pos) if isinstance(next_pos,(list,tuple)) else next_pos}",
            "action_ref": action,
            "order_rank": t + 1,
            "transition_weight": reward,
            "bend_local": 0.0 if pos == next_pos else 1.0,
            "delta_signature": {"reward": reward, "done": done, "truncated": truncated},
        }],
        "branch_space": branch_space,
        "feedback_fragment": {
            "action": action,
            "reward": reward,
            "done": done,
            "truncated": truncated,
            "next_pos": next_pos,
        },
        "structural_profiles": {"movement_changed": pos != next_pos},
        "regime_profiles": {"done": done, "truncated": truncated},
        "meta_priors": _meta_priors(primitives),
    }, family="maze")
