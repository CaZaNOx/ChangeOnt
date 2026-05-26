"""Project public six-question shape priors into generic runtime controls.

The controls are regime-level biases, not action preferences or hidden problem
solutions.
"""
from __future__ import annotations

from typing import Any, Dict, Mapping

from .shape_prior6 import DIRECT_KERNEL_CONTROLS, SHAPE_PRIOR6_AXES, shape_prior6_to_direct_controls

POSTURE_AXES = (
    "hardening_bias",
    "reopen_bias",
    "persistence_depth",
    "contradiction_tolerance",
    "collapse_readiness",
)


def clamp01(x: Any) -> float:
    try:
        return max(0.0, min(1.0, float(x)))
    except Exception:
        return 0.5


def runtime_contract_from_owner(owner: Any) -> Dict[str, Any]:
    core = getattr(owner, "core", None)
    if core is not None and hasattr(core, "export_runtime_contract"):
        try:
            data = core.export_runtime_contract()
            if isinstance(data, dict):
                return data
        except Exception:
            pass
    prims = getattr(owner, "_primitives", None)
    if isinstance(prims, dict):
        data = prims.get("_runtime_contract")
        if isinstance(data, dict):
            return data
    return {}


def shape_prior6_axis_values_from_contract(contract: Mapping[str, Any]) -> Dict[str, float]:
    prior = contract.get("shape_prior6", {}) if isinstance(contract, Mapping) else {}
    axes = prior.get("axes", {}) if isinstance(prior.get("axes", {}), Mapping) else {}
    out: Dict[str, float] = {}
    for key in SHAPE_PRIOR6_AXES:
        out[key] = clamp01(axes.get(key, 0.5))
    return out


def direct_kernel_controls_from_shape(shape_axes: Mapping[str, Any]) -> Dict[str, float]:
    controls = shape_prior6_to_direct_controls({"axes": dict(shape_axes)})
    axes = controls.get("axes", {}) if isinstance(controls.get("axes", {}), Mapping) else {}
    return {k: clamp01(axes.get(k, 0.5)) for k in DIRECT_KERNEL_CONTROLS}


def direct_kernel_controls_from_contract(contract: Mapping[str, Any]) -> Dict[str, float]:
    if isinstance(contract, Mapping):
        explicit = contract.get("direct_controls", {})
        axes = explicit.get("axes", {}) if isinstance(explicit, Mapping) and isinstance(explicit.get("axes", {}), Mapping) else {}
        if axes:
            return {k: clamp01(axes.get(k, 0.5)) for k in DIRECT_KERNEL_CONTROLS}
    return direct_kernel_controls_from_shape(shape_prior6_axis_values_from_contract(contract))


def kernel_posture_axes_from_contract(contract: Mapping[str, Any]) -> Dict[str, Any]:
    """Legacy study override only; not canonical placement."""
    study = contract.get("study_overrides", {}) if isinstance(contract, Mapping) else {}
    posture = study.get("kernel_posture", {}) if isinstance(study, Mapping) else {}
    if not isinstance(posture, Mapping):
        return {"name": "", "applied": False, "axes": {}}
    enabled = bool(posture.get("enabled", False))
    authority = str(posture.get("authority", "study_override") or "study_override")
    if not enabled or authority not in {"study_override"}:
        return {"name": str(posture.get("name", "") or ""), "applied": False, "axes": {}}
    axes = posture.get("axes", {}) if isinstance(posture.get("axes", {}), Mapping) else {}
    out: Dict[str, float] = {}
    for key in POSTURE_AXES:
        if key in axes:
            out[key] = clamp01(axes.get(key))
    return {"name": str(posture.get("name", "") or ""), "applied": bool(out), "axes": out}


def apply_direct_controls(
    direct_controls: Mapping[str, float],
    *,
    identity_support_threshold: float,
    fracture_tolerance: float,
    retention_depth: float,
    collapse_permission: float,
    support_evidence: float,
) -> Dict[str, Any]:
    collapse = clamp01(direct_controls.get("collapse_admissibility", 0.5))
    revision = clamp01(direct_controls.get("revision_permissibility", 0.5))
    carry = clamp01(direct_controls.get("support_carry_forward", 0.5))
    breadth = clamp01(direct_controls.get("rival_breadth", 0.5))
    nonlocal_auth = clamp01(direct_controls.get("nonlocal_authority", 0.5))
    path = clamp01(direct_controls.get("path_sensitivity", 0.5))
    local_auth = clamp01(direct_controls.get("local_authority", 0.5))

    threshold = clamp01(identity_support_threshold - 0.20 * collapse + 0.18 * revision - 0.08 * local_auth + 0.06 * nonlocal_auth)
    fracture = clamp01(fracture_tolerance + 0.22 * revision + 0.10 * breadth + 0.08 * nonlocal_auth - 0.10 * carry)
    retention = clamp01(retention_depth + 0.24 * carry + 0.10 * path + 0.08 * local_auth - 0.12 * revision)
    collapse_permission = clamp01(collapse_permission + 0.24 * collapse + 0.10 * local_auth - 0.14 * revision - 0.10 * nonlocal_auth)
    support_evidence = clamp01(0.55 * support_evidence + 0.20 * local_auth + 0.15 * carry + 0.10 * collapse)
    denom = max(1e-6, 1.0 - threshold)
    evidence_gate = clamp01((support_evidence - threshold) / denom)

    return {
        "identity_support_threshold": threshold,
        "fracture_tolerance": fracture,
        "retention_depth": retention,
        "collapse_permission": collapse_permission,
        "evidence_gate": evidence_gate,
        "support_evidence": support_evidence,
        "direct_controls": dict(direct_controls),
    }

# Compatibility alias for existing header code/tests; do not use as placement doctrine.
apply_direct_environment_controls = apply_direct_controls


def apply_posture_controls(
    posture: Mapping[str, Any],
    *,
    identity_support_threshold: float,
    fracture_tolerance: float,
    retention_depth: float,
    collapse_permission: float,
    support_evidence: float,
) -> Dict[str, Any]:
    axes = posture.get("axes", {}) if isinstance(posture.get("axes", {}), Mapping) else {}
    if not axes:
        denom = max(1e-6, 1.0 - identity_support_threshold)
        return {
            "identity_support_threshold": clamp01(identity_support_threshold),
            "fracture_tolerance": clamp01(fracture_tolerance),
            "retention_depth": clamp01(retention_depth),
            "collapse_permission": clamp01(collapse_permission),
            "evidence_gate": clamp01((support_evidence - identity_support_threshold) / denom),
            "posture": dict(posture),
            "modulation": {},
        }

    def centered(key: str) -> float:
        return 2.0 * (clamp01(axes.get(key, 0.5)) - 0.5)

    hardening_delta = centered("hardening_bias")
    reopen_delta = centered("reopen_bias")
    persistence_delta = centered("persistence_depth")
    contradiction_delta = centered("contradiction_tolerance")
    collapse_delta = centered("collapse_readiness")

    threshold = clamp01(identity_support_threshold - 0.18 * hardening_delta + 0.04 * reopen_delta)
    fracture = clamp01(fracture_tolerance + 0.16 * contradiction_delta + 0.10 * reopen_delta)
    retention = clamp01(retention_depth + 0.18 * persistence_delta - 0.04 * reopen_delta)
    collapse = clamp01(collapse_permission + 0.18 * collapse_delta - 0.10 * reopen_delta - 0.04 * contradiction_delta)
    denom = max(1e-6, 1.0 - threshold)
    evidence_gate = clamp01((support_evidence - threshold) / denom)

    return {
        "identity_support_threshold": threshold,
        "fracture_tolerance": fracture,
        "retention_depth": retention,
        "collapse_permission": collapse,
        "evidence_gate": evidence_gate,
        "posture": dict(posture),
        "modulation": {
            "hardening_delta": hardening_delta,
            "reopen_delta": reopen_delta,
            "persistence_delta": persistence_delta,
            "contradiction_delta": contradiction_delta,
            "collapse_delta": collapse_delta,
        },
    }
