from __future__ import annotations

from typing import Any, Dict, List

AXES = (
    "evidence_discriminability",
    "persistence_reliability",
    "revision_cost",
    "deformation_rate",
    "coverage_adequacy",
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


def bandit_descriptor(probs: List[float], *, horizon: int = 80) -> Dict[str, float]:
    ordered = sorted(float(p) for p in probs)
    best = ordered[-1] if ordered else 0.0
    second = ordered[-2] if len(ordered) >= 2 else best
    gap = max(0.0, best - second)
    disc = _clip01(gap / 0.60)
    persistence = _clip01(0.35 + 0.60 * disc)
    revision_cost = _clip01(0.25 + 0.55 * (1.0 - disc))
    deformation = 0.05
    # Generic notion: how adequate the available decision budget is for rival testing
    # relative to branching factor and ambiguity burden.
    ambiguity_burden = 1.0 + 1.8 * (1.0 - disc)
    coverage = _clip01(float(horizon) / (30.0 * max(1, len(probs)) * ambiguity_burden))
    return {
        "evidence_discriminability": disc,
        "persistence_reliability": persistence,
        "revision_cost": revision_cost,
        "deformation_rate": deformation,
        "coverage_adequacy": coverage,
    }


def renewal_descriptor(*, p_ren: float, p_noise: float, horizon: int = 120, action_count: int = 8) -> Dict[str, float]:
    ren = max(0.0, float(p_ren))
    noise = max(0.0, float(p_noise))
    disc = _clip01(1.0 - (1.4 * ren + 2.0 * noise))
    persistence = _clip01(1.0 - (1.8 * ren + 1.3 * noise))
    deformation = _clip01(2.0 * ren + 1.5 * noise)
    revision_cost = _clip01(0.30 + 0.35 * deformation + 0.25 * (1.0 - disc))
    ambiguity_burden = 1.0 + 1.2 * deformation + 0.6 * (1.0 - disc)
    coverage = _clip01(float(horizon) / (18.0 * max(1, int(action_count)) * ambiguity_burden))
    return {
        "evidence_discriminability": disc,
        "persistence_reliability": persistence,
        "revision_cost": revision_cost,
        "deformation_rate": deformation,
        "coverage_adequacy": coverage,
    }


def target_scope_for_family(family: str) -> str:
    if family == "bandit":
        return "hypothesis_over_anchor"
    return "mixed"


def posture_scores(descriptor: Dict[str, float], *, target_scope: str = "mixed") -> Dict[str, float]:
    disc = float(descriptor.get("evidence_discriminability", 0.5) or 0.5)
    persist = float(descriptor.get("persistence_reliability", 0.5) or 0.5)
    revision = float(descriptor.get("revision_cost", 0.5) or 0.5)
    deform = float(descriptor.get("deformation_rate", 0.5) or 0.5)
    coverage = float(descriptor.get("coverage_adequacy", 0.5) or 0.5)

    if target_scope == "hypothesis_over_anchor" and deform <= 0.15:
        # V3 generic static-hypothesis regime law:
        # - balanced wins only when ambiguity remains genuinely high under weak coverage
        # - once commitment readiness becomes substantial, sharp commitment should lead
        # - reopen becomes the secondary hedge in static regimes when commitment is plausible
        commitment_readiness = disc * (0.55 + 0.45 * coverage) * (1.0 - 0.45 * revision)
        ambiguity_pressure = (1.0 - disc) ** 3 * (1.0 - coverage)
        sharp = (
            0.75 * commitment_readiness
            + 0.15 * disc
            + 0.10 * coverage
            + 0.08 * persist
            + 0.05 * (1.0 - revision)
        )
        balanced = (
            0.70 * ambiguity_pressure
            + 0.10 * revision
            + 0.10 * (1.0 - disc)
            + 0.05 * (1.0 - deform)
        )
        reopen = (
            0.55 * commitment_readiness * (1.0 - coverage)
            + 0.10 * (1.0 - revision)
            + 0.08 * (1.0 - deform) * (1.0 - coverage)
            + 0.05 * disc
            + 0.03 * coverage
        )
        return {
            "sharp_commit": round(_clip01(sharp), 6),
            "balanced": round(_clip01(balanced), 6),
            "reopen_probe": round(_clip01(reopen), 6),
        }

    # V4 generic fallback for mixed/emergent regimes.
    # Commitment should remain strong in highly stable, well-covered regimes,
    # but under partial deformation with only moderate coverage the law should
    # prefer a balanced posture before sharp commitment. At higher deformation,
    # reopen pressure can overtake sharp commitment without displacing balanced.
    commitment_readiness = (
        disc
        * persist
        * (0.40 + 0.60 * coverage)
        * (1.0 - 1.05 * deform)
        * (1.0 - 0.35 * revision)
    )
    ambiguity_pressure = (
        0.28 * (1.0 - disc)
        + 0.52 * deform
        + 0.20 * (1.0 - coverage)
        + 0.12 * revision
    )
    sharp_pull = 0.82 * commitment_readiness + 0.08 * disc + 0.05 * coverage
    balanced_pull = (
        0.62 * ambiguity_pressure
        + 0.20 * (1.0 - abs(commitment_readiness - ambiguity_pressure))
        + 0.08 * (1.0 - deform)
        + 0.10 * coverage
    )
    reopen_pull = (
        0.60 * deform * (1.0 - coverage)
        + 0.18 * revision
        + 0.17 * (1.0 - persist)
        + 0.12 * (1.0 - disc)
    )
    return {
        "sharp_commit": round(_clip01(sharp_pull), 6),
        "balanced": round(_clip01(balanced_pull), 6),
        "reopen_probe": round(_clip01(reopen_pull), 6),
    }


def predicted_order(descriptor: Dict[str, float], *, target_scope: str = "mixed") -> List[str]:
    scores = posture_scores(descriptor, target_scope=target_scope)
    return [k for k, _ in sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))]


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
