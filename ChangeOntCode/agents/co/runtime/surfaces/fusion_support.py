"""Candidate evidence scoring helpers for CommitmentSurface.

These helpers implement provisional formula rows referenced by
``42_CANONICAL_READOUT_AND_ACTION_SELECTION_RULE.md`` and
``79_CANDIDATE_AND_COMMITMENT_FORMULA_GROUNDING_PROTOCOL.md``. They compress
published candidate-row fields into bounded generic support/readiness summaries.
They are not an independent policy layer and must not provide first-legal,
uniform, baseline, or family-specific rescue behavior.
"""

from __future__ import annotations
from typing import Any, Dict, List, Tuple


def clamp01(x: float) -> float:
    """Clamp a numeric helper value into 0..1 for provisional formula summaries."""
    try:
        return max(0.0, min(1.0, float(x)))
    except Exception:
        return 0.0


def _publication_rows(observation: Dict[str, Any], primitives: Dict[str, Any] | None) -> List[Dict[str, Any]]:
    """Return candidate-publication rows from canonical primitive or observation carriers."""
    if isinstance(primitives, dict):
        rows = primitives.get("__candidate_publication_rows__")
        if isinstance(rows, list):
            return [dict(r) for r in rows if isinstance(r, dict) and r.get("action") is not None]
    rows = observation.get("candidate_publication_rows") if isinstance(observation, dict) else None
    if isinstance(rows, list):
        return [dict(r) for r in rows if isinstance(r, dict) and r.get("action") is not None]
    return []


def publication_commitment_score(row: Dict[str, Any]) -> float:
    """Compress one published candidate row into a provisional bounded support score."""
    decision = clamp01(row.get("decision_state", row.get("base_state", row.get("support_conf", 0.0))))
    base = clamp01(row.get("base_state", row.get("support_conf", 0.0)))
    persistence = clamp01(row.get("persistence_state", 0.0))
    salience = clamp01(row.get("salience_state", 0.0))
    fracture = clamp01(row.get("fracture_state", row.get("contradiction", 0.0)))
    viability = clamp01(row.get("continuation_viability", persistence))
    instability = clamp01(row.get("continuation_instability", row.get("burden_accumulation", fracture)))
    raw = 0.58 * decision + 0.13 * base + 0.13 * persistence + 0.08 * salience + 0.08 * viability - 0.24 * fracture - 0.06 * instability
    return clamp01(raw)


def candidate_evidence_scores(observation: Dict[str, Any], primitives: Dict[str, Any] | None = None) -> Tuple[Dict[Any, float], Dict[str, float]]:
    """Summarize candidate-publication evidence for certificate-aware final readout."""
    rows = _publication_rows(observation, primitives)
    if not rows:
        return {}, {
            "readiness": 0.0,
            "top_margin": 0.0,
            "support_peak": 0.0,
            "tested_peak": 0.0,
            "goal_sharpness": 0.0,
            "goal_certainty": 0.0,
            "goal_stability": 0.0,
            "avg_uncertainty": 1.0,
            "avg_contradiction": 0.0,
        }
    scores = {row["action"]: publication_commitment_score(row) for row in rows}
    top2 = sorted(scores.values(), reverse=True)[:2]
    top = float(top2[0] if top2 else 0.0)
    second = float(top2[1] if len(top2) > 1 else 0.0)
    top_margin = clamp01(top - second)
    support_peak = max(clamp01(row.get("base_state", row.get("support_conf", 0.0))) for row in rows)
    decision_peak = max(clamp01(row.get("decision_state", row.get("base_state", row.get("support_conf", 0.0)))) for row in rows)
    persistence_peak = max(clamp01(row.get("persistence_state", 0.0)) for row in rows)
    salience_peak = max(clamp01(row.get("salience_state", 0.0)) for row in rows)
    avg_fracture = sum(clamp01(row.get("fracture_state", row.get("contradiction", 0.0))) for row in rows) / float(len(rows) or 1)
    viability_peak = max(clamp01(row.get("continuation_viability", row.get("persistence_state", 0.0))) for row in rows)
    avg_instability = sum(clamp01(row.get("continuation_instability", row.get("burden_accumulation", row.get("fracture_state", 0.0)))) for row in rows) / float(len(rows) or 1)
    readiness = clamp01(
        0.26 * top
        + 0.20 * top_margin
        + 0.16 * decision_peak
        + 0.12 * support_peak
        + 0.10 * persistence_peak
        + 0.06 * salience_peak
        + 0.08 * viability_peak
        - 0.14 * avg_fracture
        - 0.05 * avg_instability
    )
    max_abs = max(abs(v) for v in scores.values()) if scores else 0.0
    norm = {k: (float(v) / max_abs if max_abs > 1e-12 else float(v)) for k, v in scores.items()}
    return norm, {
        "readiness": readiness,
        "top_margin": top_margin,
        "support_peak": support_peak,
        "tested_peak": support_peak,
        "goal_sharpness": top_margin,
        "goal_certainty": top,
        "goal_stability": max(persistence_peak, viability_peak),
        "avg_uncertainty": 1.0 - support_peak,
        "avg_contradiction": avg_fracture,
        "viability_peak": viability_peak,
        "avg_instability": avg_instability,
    }
