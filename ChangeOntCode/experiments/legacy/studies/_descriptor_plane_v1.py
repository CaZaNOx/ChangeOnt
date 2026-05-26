from __future__ import annotations

from typing import Any, Dict, List, Tuple

AXES = (
    "evidence_discriminability",
    "persistence_reliability",
    "revision_cost",
    "deformation_rate",
)

POSTURES: Dict[str, Dict[str, float]] = {
    "sharp_commit": {
        "hardening_bias": 0.85,
        "reopen_bias": 0.20,
        "persistence_depth": 0.80,
        "contradiction_tolerance": 0.35,
        "collapse_readiness": 0.72,
    },
    "balanced": {
        "hardening_bias": 0.55,
        "reopen_bias": 0.50,
        "persistence_depth": 0.55,
        "contradiction_tolerance": 0.50,
        "collapse_readiness": 0.45,
    },
    "reopen_probe": {
        "hardening_bias": 0.25,
        "reopen_bias": 0.82,
        "persistence_depth": 0.35,
        "contradiction_tolerance": 0.68,
        "collapse_readiness": 0.18,
    },
}


def _clip01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def bandit_descriptor(probs: List[float]) -> Dict[str, float]:
    ordered = sorted(float(p) for p in probs)
    best = ordered[-1] if ordered else 0.0
    second = ordered[-2] if len(ordered) >= 2 else best
    gap = max(0.0, best - second)
    # 0.60 is the widest margin in the current task suite and keeps the scale human-readable.
    disc = _clip01(gap / 0.60)
    # For anchor-fixed bandits, persistence reliability should drop when evidence is weak,
    # because support over latent value hypotheses is not trustworthy yet even if arm identities are fixed.
    persistence = _clip01(0.35 + 0.60 * disc)
    # Wrong lock-in is more costly exactly when evidence is weak.
    revision_cost = _clip01(0.25 + 0.55 * (1.0 - disc))
    deformation = 0.05  # stationary horizon in this task track
    return {
        "evidence_discriminability": disc,
        "persistence_reliability": persistence,
        "revision_cost": revision_cost,
        "deformation_rate": deformation,
    }


def renewal_descriptor(*, p_ren: float, p_noise: float) -> Dict[str, float]:
    ren = max(0.0, float(p_ren))
    noise = max(0.0, float(p_noise))
    disc = _clip01(1.0 - (1.4 * ren + 2.0 * noise))
    persistence = _clip01(1.0 - (1.8 * ren + 1.3 * noise))
    deformation = _clip01(2.0 * ren + 1.5 * noise)
    revision_cost = _clip01(0.30 + 0.35 * deformation + 0.25 * (1.0 - disc))
    return {
        "evidence_discriminability": disc,
        "persistence_reliability": persistence,
        "revision_cost": revision_cost,
        "deformation_rate": deformation,
    }


def posture_scores(descriptor: Dict[str, float]) -> Dict[str, float]:
    disc = float(descriptor.get("evidence_discriminability", 0.5) or 0.5)
    persist = float(descriptor.get("persistence_reliability", 0.5) or 0.5)
    revision = float(descriptor.get("revision_cost", 0.5) or 0.5)
    deform = float(descriptor.get("deformation_rate", 0.5) or 0.5)

    # Positive pull favors earlier hardening; negative pull favors reopening.
    pull = 0.5 * ((disc + persist) - (revision + deform))
    pull = max(-1.0, min(1.0, pull))
    sharp = 0.5 + 0.5 * pull
    reopen = 0.5 - 0.5 * pull
    balanced = 1.0 - abs(pull)
    return {
        "sharp_commit": round(sharp, 6),
        "balanced": round(balanced, 6),
        "reopen_probe": round(reopen, 6),
    }


def predicted_order(descriptor: Dict[str, float]) -> List[str]:
    scores = posture_scores(descriptor)
    return [k for k, _ in sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))]


def deformation_summary(before: Dict[str, float], after: Dict[str, float]) -> Dict[str, float]:
    return {axis: round(float(after.get(axis, 0.0)) - float(before.get(axis, 0.0)), 6) for axis in AXES}


def target_scope_for_family(family: str) -> str:
    if family == "bandit":
        return "hypothesis_over_anchor"
    return "mixed"


def problem_contract_for_family(family: str, spec: Dict[str, Any]) -> Dict[str, Any]:
    if family == "bandit":
        probs = list(spec.get("probs") or [])
        return {
            "actions": {"count": len(probs), "native_type": "discrete", "labels": [f"arm_{i}" for i in range(len(probs))]},
            "observation_channels": ["reward_feedback", "trace_history"],
            "task_anchor": {"kind": "reward_maximization", "provided_externally": True, "notes": "maximize expected reward over fixed action anchors"},
            "hard_constraints": [],
            "soft_costs": ["regret"],
            "regime_anchors": ["action_identities", "arm_count"],
            "mutable_factors": ["latent_arm_value_relation"],
            "timescale_profile": {"horizon_fixity": "fixed", "drift": "fixed"},
            "observability_profile": {"state": "partial", "outcome": "direct", "constraints": "direct"},
            "reversibility_profile": {"action_reversibility": "reversible", "commitment_cost": "medium"},
            "notes": f"Bandit task {spec.get('name','')} expressed through the generic contract.",
            "source": "study_declared",
            "status": "investigatory",
        }
    A = int(spec.get("A", 0) or 0)
    labels = [f"sym_{i}" for i in range(A)]
    return {
        "actions": {"count": A, "native_type": "discrete", "labels": labels},
        "observation_channels": ["symbol_observation", "reward_feedback", "trace_history"],
        "task_anchor": {"kind": "predictive_reward_alignment", "provided_externally": True, "notes": "align predictions with shifting reward-bearing sequence structure"},
        "hard_constraints": [],
        "soft_costs": ["miss_rate"],
        "regime_anchors": ["alphabet_cardinality", "action_space_cardinality"],
        "mutable_factors": ["transition_relation", "codebook_relation", "noise_relation"],
        "timescale_profile": {"horizon_fixity": "mixed", "drift": "mixed"},
        "observability_profile": {"state": "direct", "outcome": "direct", "constraints": "unknown"},
        "reversibility_profile": {"action_reversibility": "reversible", "commitment_cost": "medium"},
        "notes": f"Renewal task {spec.get('name','')} expressed through the generic contract.",
        "source": "study_declared",
        "status": "investigatory",
    }
