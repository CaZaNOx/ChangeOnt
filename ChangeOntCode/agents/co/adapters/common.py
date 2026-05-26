"""Shared adapter helpers for public CO boundary facts.

Helpers here construct public burden/effect dictionaries and signal-bus support.
They are intentionally about public transformation grammar rather than action
optimality.
"""

from __future__ import annotations
from typing import Any, Dict


def ensure_signal_bus(primitives: Dict[str, Any]) -> None:
    """Attach the shared KernelSignalBus used by candidate publication when absent."""
    if "signal_bus" in primitives:
        return
    try:
        from agents.co.runtime.support.signal_bus import KernelSignalBus
        primitives["signal_bus"] = KernelSignalBus()
    except Exception:
        pass



def _clip01_value(x: Any, default: float = 0.0) -> float:
    try:
        v = float(x)
    except Exception:
        return float(default)
    if v < 0.0:
        return 0.0
    if v > 1.0:
        return 1.0
    return v


def public_effect(
    operation: str,
    burden_type: str = "",
    *,
    magnitude: float = 1.0,
    scope: str = "candidate",
    kind: str = "burden",
    public_basis: str = "declared_transition_rule",
    leakage_status: str = "public",
    relation_scope: str = "",
    effect_id: str | None = None,
    direction: str = "",
    coupling: str = "",
    barrier: str = "",
    threshold_status: str = "",
    basin_status: str = "",
    confidence: float = 1.0,
) -> Dict[str, Any]:
    """Create a public burden/effect fact for RelationSurface.

    This helper intentionally publishes transformation grammar, not policy.  It
    must not be used to encode optimality, baseline values, hidden state, or
    family-local best-action advice.  The kernel-side RelationSurface derives
    branch relations from these facts.
    """
    data: Dict[str, Any] = {
        "effect_id": effect_id or f"{str(operation)}_{str(burden_type or relation_scope or scope)}",
        "kind": str(kind),
        "operation": str(operation),
        "burden_type": str(burden_type or ""),
        "scope": str(scope),
        "magnitude": _clip01_value(magnitude, 1.0),
        "public_basis": str(public_basis),
        "leakage_status": str(leakage_status),
        "confidence": _clip01_value(confidence, 1.0),
    }
    if relation_scope:
        data["relation_scope"] = str(relation_scope)
    if direction:
        data["direction"] = str(direction)
    if coupling:
        data["coupling"] = str(coupling)
    if barrier:
        data["barrier"] = str(barrier)
    if threshold_status:
        data["threshold_status"] = str(threshold_status)
    if basin_status:
        data["basin_status"] = str(basin_status)
    return data


def single_decision_slot_effect(scope: str = "single_decision_slot", *, magnitude: float = 1.0) -> Dict[str, Any]:
    """Public fact: candidates in one decision publication compete for one slot.

    This is not a policy preference.  It only states the legal readout grammar
    that one immediate expression will be selected at this decision point.
    """
    return public_effect(
        "decision_slot",
        "",
        magnitude=magnitude,
        scope="decision_slot",
        kind="legal_constraint",
        public_basis="legal_constraint",
        leakage_status="public",
        relation_scope=scope,
        effect_id=f"decision_slot_{scope}",
    )
