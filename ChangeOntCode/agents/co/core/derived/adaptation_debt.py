from __future__ import annotations
from typing import Any, Dict, Mapping


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def derive_adaptation_debt(
    *,
    prev_debt: float,
    prev_misfit: float,
    continuity_conf: float,
    trajectory_stability: float,
    incumbent_stability: float,
    fracture_pressure: float,
    estimate_drift: float,
    field_update: Mapping[str, Any] | None = None,
) -> Dict[str, float]:
    """
    Derived quantity, not a primitive.

    Adaptation debt rises only when:
      1) a line is still being held together (continuity / stability remain non-trivial),
      2) fit to unfolding evidence worsens (fracture / drift / field-update break pressure), and
      3) that lag persists rather than resolving immediately.

    It is therefore the pressure produced by *preserved continuity outliving its warrant*.
    """
    fu = dict(field_update or {})
    fu_cont = _clamp01(float(fu.get("continuity_update", continuity_conf) or continuity_conf))
    fu_frac = _clamp01(float(fu.get("fracture_update", fracture_pressure) or fracture_pressure))
    branch_update = _clamp01(float(fu.get("branch_update", 0.0) or 0.0))
    confidence_update = _clamp01(float(fu.get("confidence_update", 0.0) or 0.0))

    stability = _clamp01(max(float(continuity_conf), 0.65 * float(trajectory_stability) + 0.35 * float(incumbent_stability)))
    commitment = _clamp01(max(0.0, stability - 0.40 * float(fracture_pressure)))

    # Misfit is not mere fracture; it is persistent evidence that the current stabilized line
    # is no longer earning itself under unfolding evidence.
    local_break = max(0.0, fu_frac - fu_cont)
    low_conf = max(0.0, 0.5 - confidence_update)
    misfit = _clamp01(max(float(fracture_pressure), float(estimate_drift), local_break, 0.60 * branch_update + 0.40 * low_conf))
    worsening = _clamp01(max(0.0, misfit - float(prev_misfit)))

    # Debt only rises when commitment remains non-trivial while misfit/worsening persist.
    debt_instant = _clamp01(commitment * (0.55 * misfit + 0.30 * worsening + 0.15 * branch_update))
    recovery = _clamp01(max(0.0, fu_cont - fu_frac) * (0.50 + 0.50 * confidence_update))

    if commitment < 0.35:
        decay = 0.72
    else:
        decay = 0.90
    debt = _clamp01(decay * float(prev_debt) + 0.40 * debt_instant - 0.30 * recovery)
    rigidity = _clamp01(debt * commitment)

    return {
        "adaptation_debt": float(debt),
        "adaptation_debt_instant": float(debt_instant),
        "adaptation_recovery": float(recovery),
        "fit_mismatch": float(misfit),
        "fit_worsening": float(worsening),
        "commitment_hold": float(commitment),
        "rigidity_pressure": float(rigidity),
        "field_continuity": float(fu_cont),
        "field_fracture": float(fu_frac),
        "field_branch_update": float(branch_update),
        "field_confidence_update": float(confidence_update),
    }
