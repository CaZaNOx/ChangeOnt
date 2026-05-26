from __future__ import annotations

from typing import Any, Dict, List

from agents.co.placement.measure import posture_scores_factorized, predicted_order_factorized, factorized_to_descriptor_axes

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


def bandit_factorized(probs: List[float], *, horizon: int = 80) -> Dict[str, float]:
    ordered = sorted(float(p) for p in probs)
    best = ordered[-1] if ordered else 0.0
    second = ordered[-2] if len(ordered) >= 2 else best
    gap = max(0.0, best - second)
    disc = min(1.0, gap / 0.60)
    ambiguity = 1.0 - disc
    cover = min(1.0, float(horizon) / (30.0 * max(1, len(probs)) * (1.0 + 1.8 * ambiguity)))
    return {
        "coverage_adequacy": cover,
        "revision_harshness": min(1.0, 0.30 + 0.45 * ambiguity + 0.15 * (1.0 - cover)),
        "local_progress_reliability": min(1.0, 0.25 + 0.55 * disc + 0.20 * cover),
        "scaffold_stability": 0.95,
        "payload_rewrite_intensity": 0.05,
        "strategic_coupling": 0.0,
        "consequence_depth": min(1.0, 0.12 + 0.20 * ambiguity),
    }


def renewal_factorized(*, p_ren: float, p_noise: float, horizon: int = 120, action_count: int = 8) -> Dict[str, float]:
    ren = max(0.0, float(p_ren))
    noise = max(0.0, float(p_noise))
    cover = min(1.0, float(horizon) / (18.0 * max(1, int(action_count)) * (1.0 + 1.2 * (2.0 * ren + 1.5 * noise))))
    payload = min(1.0, 2.2 * ren + 1.7 * noise)
    scaff = max(0.0, min(1.0, 0.92 - 0.25 * ren))
    local = max(0.0, min(1.0, 0.85 - 1.4 * ren - 1.8 * noise))
    revision = max(0.0, min(1.0, 0.22 + 0.45 * payload + 0.18 * (1.0 - local) + 0.15 * (1.0 - cover)))
    depth = max(0.0, min(1.0, 0.22 + 0.45 * payload + 0.10 * (1.0 - cover)))
    return {
        "coverage_adequacy": cover,
        "revision_harshness": revision,
        "local_progress_reliability": local,
        "scaffold_stability": scaff,
        "payload_rewrite_intensity": payload,
        "strategic_coupling": 0.0,
        "consequence_depth": depth,
    }


def descriptor_axes_from_factorized(f: Dict[str, float]) -> Dict[str, float]:
    return factorized_to_descriptor_axes(f)


def posture_scores(factorized: Dict[str, float]) -> Dict[str, float]:
    return posture_scores_factorized(factorized)


def predicted_order(factorized: Dict[str, float]) -> List[str]:
    return predicted_order_factorized(factorized)


def target_scope_for_family(family: str) -> str:
    if family == "bandit":
        return "hypothesis_over_anchor"
    return "mixed"
