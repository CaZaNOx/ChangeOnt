"""Canonical six-question public shape prior.

Only this shape-prior path is active for certified CO runtime.
"""

from __future__ import annotations

from typing import Any, Dict, Mapping

SHAPE_SCORE_VALUES = (0.0, 0.25, 0.5, 0.75, 1.0)

SHAPE_PRIOR6_AXES = (
    "hidden_decisiveness",
    "reshapeability",
    "local_cue_reliability",
    "revision_cost",
    "consequence_span",
    "topology_constraint",
)

DIRECT_KERNEL_CONTROLS = (
    "collapse_admissibility",
    "revision_permissibility",
    "support_carry_forward",
    "rival_breadth",
    "nonlocal_authority",
    "path_sensitivity",
    "local_authority",
)


def _clip01(x: Any, default: float = 0.5) -> float:
    try:
        v = float(x)
    except Exception:
        return float(default)
    return max(0.0, min(1.0, v))


def quantize_shape_score(x: Any, default: float = 0.5) -> float:
    """Return the nearest canonical five-point shape score."""
    v = _clip01(x, default)
    return min(SHAPE_SCORE_VALUES, key=lambda s: abs(float(s) - v))


OBS_SCALE = {"direct": 1.0, "partial": 0.65, "indirect": 0.30, "mixed": 0.55, "unknown": 0.50}
FIXITY_SCALE = {"fixed": 0.95, "slow": 0.75, "mixed": 0.50, "active": 0.20, "unknown": 0.50}
DRIFT_SCALE = {"none": 0.00, "fixed": 0.05, "slow": 0.25, "mixed": 0.50, "active": 0.85, "unknown": 0.50}
REV_SCALE = {"reversible": 0.05, "partly_reversible": 0.50, "irreversible": 0.95, "unknown": 0.50}
COMMIT_SCALE = {"low": 0.15, "low_to_medium": 0.32, "medium": 0.50, "medium_to_high": 0.68, "high": 0.85, "unknown": 0.50}


def normalize_shape_prior6(raw: Any, *, quantize: bool = True) -> Dict[str, Any]:
    payload = raw if isinstance(raw, Mapping) else {}
    axes_raw = payload.get("axes", payload) if isinstance(payload, Mapping) else {}
    scorer = quantize_shape_score if quantize else _clip01
    axes = {k: scorer(axes_raw.get(k, 0.5), 0.5) for k in SHAPE_PRIOR6_AXES}
    return {
        "schema": "co_shape_prior6_v2",
        "axes": axes,
        "score_values": list(SHAPE_SCORE_VALUES),
        "notes": str(payload.get("notes", "") if isinstance(payload, Mapping) else ""),
        "source": str(payload.get("source", "declared") if isinstance(payload, Mapping) else "declared"),
        "status": str(payload.get("status", "declared") if isinstance(payload, Mapping) else "declared"),
    }


def derive_shape_prior6(problem_contract: Mapping[str, Any]) -> Dict[str, Any]:
    """Derive the canonical six-question prior from public problem-contract fields.

    This is still a working placement law, not a proven final derivation. It must
    remain auditable: no family-private labels, no solver output, and no hidden
    state may enter this function.
    """
    from agents.co.core.contracts.problem_contract import normalize_problem_contract

    problem = normalize_problem_contract(problem_contract)
    obs = problem.get("observability_profile", {}) if isinstance(problem.get("observability_profile", {}), Mapping) else {}
    time = problem.get("timescale_profile", {}) if isinstance(problem.get("timescale_profile", {}), Mapping) else {}
    rev = problem.get("reversibility_profile", {}) if isinstance(problem.get("reversibility_profile", {}), Mapping) else {}
    task = problem.get("task_anchor", {}) if isinstance(problem.get("task_anchor", {}), Mapping) else {}
    actions = problem.get("actions", {}) if isinstance(problem.get("actions", {}), Mapping) else {}
    hard_constraints = list(problem.get("hard_constraints") or [])
    mutable_factors = list(problem.get("mutable_factors") or [])
    soft_costs = list(problem.get("soft_costs") or [])
    anchors = list(problem.get("regime_anchors") or [])

    state_obs = OBS_SCALE.get(str(obs.get("state", "unknown")), 0.50)
    outcome_obs = OBS_SCALE.get(str(obs.get("outcome", "unknown")), 0.50)
    constraint_obs = OBS_SCALE.get(str(obs.get("constraints", "unknown")), 0.50)
    fixity = FIXITY_SCALE.get(str(time.get("horizon_fixity", "unknown")), 0.50)
    drift = DRIFT_SCALE.get(str(time.get("drift", "unknown")), 0.50)
    act_rev = REV_SCALE.get(str(rev.get("action_reversibility", "unknown")), 0.50)
    commit_cost = COMMIT_SCALE.get(str(rev.get("commitment_cost", "unknown")), 0.50)
    try:
        action_count = max(0, int(actions.get("count", 0) or 0))
    except Exception:
        action_count = 0

    action_open = _clip01(action_count / 8.0, 0.0)
    hard_density = _clip01(len(hard_constraints) / 4.0, 0.0)
    mutable_density = _clip01(len(mutable_factors) / 4.0, 0.0)
    soft_density = _clip01(len(soft_costs) / 4.0, 0.0)
    anchor_density = _clip01(len(anchors) / 4.0, 0.0)
    goal_explicit = 1.0 if bool(task.get("provided_externally", False)) and str(task.get("kind", "unknown")) != "unknown" else 0.35

    raw_axes = {
        "hidden_decisiveness": _clip01(0.50 * (1.0 - outcome_obs) + 0.30 * (1.0 - state_obs) + 0.20 * (1.0 - constraint_obs), 0.5),
        "reshapeability": _clip01(0.45 * drift + 0.35 * mutable_density + 0.20 * (1.0 - fixity), 0.5),
        "local_cue_reliability": _clip01(0.40 * outcome_obs + 0.25 * state_obs + 0.15 * goal_explicit + 0.10 * anchor_density + 0.10 * (1.0 - mutable_density), 0.5),
        "revision_cost": _clip01(0.55 * commit_cost + 0.35 * act_rev + 0.10 * soft_density, 0.5),
        "consequence_span": _clip01(0.32 * fixity + 0.28 * commit_cost + 0.18 * hard_density + 0.12 * mutable_density + 0.10 * (1.0 - outcome_obs), 0.5),
        "topology_constraint": _clip01(0.60 * hard_density + 0.25 * (1.0 - action_open) + 0.15 * constraint_obs, 0.5),
    }
    axes = {k: quantize_shape_score(v) for k, v in raw_axes.items()}
    return {
        "schema": "co_shape_prior6_v2",
        "axes": axes,
        "raw_axes_before_quantization": raw_axes,
        "score_values": list(SHAPE_SCORE_VALUES),
        "source": "problem_contract_questionnaire",
        "status": "derived_from_public_problem_contract",
        "notes": "Derived from the six canonical generic regime questions using public problem specification fields only.",
    }


def shape_prior6_to_direct_controls(shape_prior: Mapping[str, Any]) -> Dict[str, Any]:
    """Project six canonical questions directly into runtime controls."""
    prior = normalize_shape_prior6(shape_prior)
    s = prior["axes"]
    hidden = float(s["hidden_decisiveness"])
    reshape = float(s["reshapeability"])
    local = float(s["local_cue_reliability"])
    revision = float(s["revision_cost"])
    consequence = float(s["consequence_span"])
    topology = float(s["topology_constraint"])

    axes = {
        "collapse_admissibility": _clip01(0.08 + 0.28 * local + 0.18 * (1.0 - hidden) + 0.16 * (1.0 - reshape) + 0.12 * (1.0 - revision) + 0.10 * (1.0 - consequence) + 0.08 * (1.0 - topology)),
        "revision_permissibility": _clip01(0.34 * revision + 0.24 * reshape + 0.18 * hidden + 0.14 * consequence + 0.10 * (1.0 - local)),
        "support_carry_forward": _clip01(0.30 * (1.0 - reshape) + 0.24 * local + 0.18 * (1.0 - hidden) + 0.14 * (1.0 - revision) + 0.14 * (1.0 - consequence)),
        "rival_breadth": _clip01(0.28 * topology + 0.22 * hidden + 0.20 * reshape + 0.18 * consequence + 0.12 * (1.0 - local)),
        "nonlocal_authority": _clip01(0.42 * consequence + 0.24 * hidden + 0.20 * reshape + 0.14 * topology),
        "path_sensitivity": _clip01(0.36 * consequence + 0.24 * topology + 0.20 * revision + 0.12 * reshape + 0.08 * hidden),
        "local_authority": _clip01(0.38 * local + 0.20 * (1.0 - hidden) + 0.18 * (1.0 - consequence) + 0.14 * (1.0 - reshape) + 0.10 * (1.0 - topology)),
    }
    return {
        "schema": "co_direct_controls_v2",
        "axes": axes,
        "source": "shape_prior6_direct_projection",
        "status": "active_canonical_projection",
        "notes": "Direct runtime controls projected from the 6-question canonical shape prior.",
    }


__all__ = [
    "SHAPE_SCORE_VALUES",
    "SHAPE_PRIOR6_AXES",
    "DIRECT_KERNEL_CONTROLS",
    "quantize_shape_score",
    "normalize_shape_prior6",
    "derive_shape_prior6",
    "shape_prior6_to_direct_controls",
]
