"""Problem-contract normalization for public boundary inputs.

The contract describes action space, observability, constraints, reversibility,
and task-anchor facts without supplying hidden policy conclusions.
"""

from __future__ import annotations

from typing import Any, Dict, Mapping

from ._common import (
    ALLOWED_SCOPES,
    COMMITMENT_COST,
    HORIZON_FIXITY,
    DRIFT_PROFILE,
    OBSERVABILITY,
    REVERSIBILITY,
    bounded01,
    choice,
    clean_list,
    clean_text,
    copy_mapping,
)


def normalize_problem_contract(raw: Any) -> Dict[str, Any]:
    """Normalize public problem-contract data without adding solver knowledge."""
    payload = copy_mapping(raw)
    actions_raw = copy_mapping(payload.get("actions"))
    labels = clean_list(actions_raw.get("labels", payload.get("action_labels")))
    count = actions_raw.get("count", payload.get("action_count", len(labels)))
    try:
        action_count = int(count)
    except Exception:
        action_count = len(labels)
    if action_count < 0:
        action_count = 0
    task_raw = copy_mapping(payload.get("task_anchor"))
    time_raw = copy_mapping(payload.get("timescale_profile"))
    obs_raw = copy_mapping(payload.get("observability_profile"))
    rev_raw = copy_mapping(payload.get("reversibility_profile"))

    decision_scope = clean_text(payload.get("decision_scope", payload.get("problem_scope", payload.get("scope", "")))).lower()
    if decision_scope not in ALLOWED_SCOPES:
        decision_scope = ""
    return {
        "schema": "co_problem_contract_v1",
        "actions": {
            "count": action_count,
            "native_type": clean_text(actions_raw.get("native_type", payload.get("action_native_type", ""))) or "unknown",
            "labels": labels,
        },
        "observation_channels": clean_list(payload.get("observation_channels")),
        "decision_scope": decision_scope,
        "task_anchor": {
            "kind": clean_text(task_raw.get("kind", payload.get("task_kind", ""))) or "unknown",
            "provided_externally": bool(task_raw.get("provided_externally", payload.get("task_provided_externally", True))),
            "notes": clean_text(task_raw.get("notes", payload.get("task_notes"))),
        },
        "hard_constraints": clean_list(payload.get("hard_constraints")),
        "soft_costs": clean_list(payload.get("soft_costs")),
        "regime_anchors": clean_list(payload.get("regime_anchors")),
        "mutable_factors": clean_list(payload.get("mutable_factors")),
        "timescale_profile": {
            "horizon_fixity": choice(time_raw.get("horizon_fixity", payload.get("horizon_fixity", "unknown")), HORIZON_FIXITY, "unknown"),
            "drift": choice(time_raw.get("drift", payload.get("drift", "unknown")), DRIFT_PROFILE, "unknown"),
            "notes": clean_text(time_raw.get("notes", payload.get("timescale_notes"))),
        },
        "observability_profile": {
            "state": choice(obs_raw.get("state", payload.get("observability_state", "unknown")), OBSERVABILITY, "unknown"),
            "outcome": choice(obs_raw.get("outcome", payload.get("observability_outcome", "unknown")), OBSERVABILITY, "unknown"),
            "constraints": choice(obs_raw.get("constraints", payload.get("observability_constraints", "unknown")), OBSERVABILITY, "unknown"),
        },
        "reversibility_profile": {
            "action_reversibility": choice(rev_raw.get("action_reversibility", payload.get("action_reversibility", "unknown")), REVERSIBILITY, "unknown"),
            "commitment_cost": choice(rev_raw.get("commitment_cost", payload.get("commitment_cost", "unknown")), COMMITMENT_COST, "unknown"),
            "notes": clean_text(rev_raw.get("notes", payload.get("reversibility_notes"))),
        },
        "notes": clean_text(payload.get("notes")),
        "source": clean_text(payload.get("source", "declared")) or "declared",
        "status": clean_text(payload.get("status", "declared")) or "declared",
    }


def _goal_observability_from_problem(problem: Mapping[str, Any]) -> float:
    obs = copy_mapping(problem.get("observability_profile"))
    state = choice(obs.get("state", "unknown"), OBSERVABILITY, "unknown")
    outcome = choice(obs.get("outcome", "unknown"), OBSERVABILITY, "unknown")
    scale = {"direct": 1.0, "partial": 0.65, "indirect": 0.35, "mixed": 0.55, "unknown": 0.50}
    return max(0.0, min(1.0, 0.45 * scale.get(state, 0.5) + 0.55 * scale.get(outcome, 0.5)))


def action_count_from_observation(observation: Any, default: int = 0) -> int:
    obs = copy_mapping(observation)
    actions = obs.get("action_space")
    if isinstance(actions, list) and actions:
        return max(0, len(actions))
    problem = normalize_problem_contract(obs.get("problem_contract", {}))
    try:
        count = int(copy_mapping(problem.get("actions")).get("count", default) or default)
    except Exception:
        count = int(default)
    if count > 0:
        return count
    cur = copy_mapping(obs.get("current_observation"))
    fam = copy_mapping(obs.get("family_payload"))
    for key in ("n_arms", "A"):
        for src in (obs, cur, fam):
            try:
                val = int(src.get(key, 0) or 0)
            except Exception:
                val = 0
            if val > 0:
                return val
    return max(0, int(default))


def derive_goal_field(observation: Any) -> Dict[str, Any]:
    obs = copy_mapping(observation)
    goal = copy_mapping(obs.get("goal_field"))
    if goal:
        return {
            "goal_mode": clean_text(goal.get("goal_mode", "graded")) or "graded",
            "goal_sharpness": bounded01(goal.get("goal_sharpness", 0.5)) if bounded01(goal.get("goal_sharpness", 0.5)) is not None else 0.5,
            "goal_stability": bounded01(goal.get("goal_stability", 0.5)) if bounded01(goal.get("goal_stability", 0.5)) is not None else 0.5,
            "goal_certainty": bounded01(goal.get("goal_certainty", 0.5)) if bounded01(goal.get("goal_certainty", 0.5)) is not None else 0.5,
            "goal_observability": bounded01(goal.get("goal_observability", 1.0)) if bounded01(goal.get("goal_observability", 1.0)) is not None else 1.0,
            "source": clean_text(goal.get("source", "goal_field")) or "goal_field",
        }
    problem = normalize_problem_contract(obs.get("problem_contract", {}))
    task = copy_mapping(problem.get("task_anchor"))
    time = copy_mapping(problem.get("timescale_profile"))
    kind = clean_text(task.get("kind", "unknown")) or "unknown"
    fixity = choice(time.get("horizon_fixity", "unknown"), HORIZON_FIXITY, "unknown")
    stability_map = {"fixed": 0.90, "slow": 0.72, "mixed": 0.55, "active": 0.30, "unknown": 0.50}
    stability = stability_map.get(fixity, 0.50)
    candidates = [c for c in list(obs.get("candidates") or []) if isinstance(c, Mapping) and bool(c.get("legal", True))]
    top_goal = 0.0
    best_margin = 0.0
    avg_uncert = 0.5
    if candidates:
        try:
            scores = [max(0.0, min(1.0, float(c.get("goal_relation", c.get("visible_delta", 0.0)) or 0.0))) for c in candidates]
            ordered = sorted(scores, reverse=True)
            top_goal = ordered[0] if ordered else 0.0
            best_margin = max(0.0, ordered[0] - ordered[1]) if len(ordered) >= 2 else top_goal
        except Exception:
            top_goal = 0.0
            best_margin = 0.0
        try:
            uncerts = [max(0.0, min(1.0, float(c.get("uncertainty_hint", 0.5) or 0.5))) for c in candidates]
            avg_uncert = sum(uncerts) / float(len(uncerts) or 1)
        except Exception:
            avg_uncert = 0.5
    certainty = max(0.0, min(1.0, 0.55 * float(best_margin) + 0.45 * (1.0 - avg_uncert)))
    if kind in {"goal_reach", "constraint_satisfaction"}:
        mode = "targeted"
    elif kind in {"reward_maximization", "predictive_reward_alignment"}:
        mode = "graded"
    else:
        mode = "unknown"
    return {
        "goal_mode": mode,
        "goal_sharpness": max(0.0, min(1.0, float(best_margin))),
        "goal_stability": stability,
        "goal_certainty": certainty,
        "goal_observability": _goal_observability_from_problem(problem),
        "source": "problem_contract_derivation",
    }


__all__ = [
    "normalize_problem_contract",
    "action_count_from_observation",
    "derive_goal_field",
]
