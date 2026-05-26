"""Runtime placement contract for the canonical six-question path.

Active path:
    problem_contract -> shape_prior6 -> direct_controls

Only the canonical six-question path is active. Retired descriptor/axis/posture payloads are not accepted as runtime controls.
"""
from __future__ import annotations

from typing import Any, Dict, Mapping

from ._common import clean_list, clean_text, copy_mapping, deep_export_bundle
from .problem_contract import normalize_problem_contract
from agents.co.placement.shape_prior6 import normalize_shape_prior6, derive_shape_prior6, shape_prior6_to_direct_controls


def normalize_shape_prior(raw: Any) -> Dict[str, Any]:
    return normalize_shape_prior6(raw)


def normalize_kernel_posture(raw: Any) -> Dict[str, Any]:
    payload = copy_mapping(raw)
    axes = copy_mapping(payload.get("axes"))
    return {
        "schema": "co_kernel_posture_study_v1",
        "name": clean_text(payload.get("name", payload.get("label", ""))),
        "axes": {k: v for k, v in axes.items()},
        "enabled": bool(payload.get("enabled", False)),
        "authority": clean_text(payload.get("authority", "study_override")) or "study_override",
        "notes": clean_text(payload.get("notes")),
        "status": clean_text(payload.get("status", "study_only")) or "study_only",
    }


def normalize_study_overrides(raw: Any) -> Dict[str, Any]:
    payload = copy_mapping(raw)
    posture_raw = payload.get("kernel_posture", payload.get("posture", {}))
    return {"schema": "co_study_overrides_v2", "kernel_posture": normalize_kernel_posture(posture_raw)}


def normalize_retired_placement_payload(raw: Any) -> Dict[str, Any]:
    """Reject retired placement payloads by converting them to an inert audit record."""
    return {"schema": "co_no_retired_placement_payload_v1", "status": "not_accepted_in_certified_runtime", "payload": {}}

def build_runtime_contract(params: Any) -> Dict[str, Dict[str, Any]]:
    """Build problem contract, shape_prior6, and direct controls for certified runtime use."""
    payload = copy_mapping(params)
    problem_raw = copy_mapping(payload.get("problem_contract", payload.get("problem", {})))
    problem = normalize_problem_contract(problem_raw)
    shape_raw = payload.get("shape_prior6", payload.get("shape_prior", {}))
    shape = normalize_shape_prior(shape_raw) if shape_raw else derive_shape_prior6(problem)
    direct_controls = shape_prior6_to_direct_controls(shape)
    study_source = payload.get("study_overrides", {"kernel_posture": payload.get("kernel_posture", payload.get("posture", {}))})

    return {
        "problem_contract": problem,
        "shape_prior6": shape,
        "direct_controls": direct_controls,
        "study_overrides": normalize_study_overrides(study_source),
    }


def contract_is_declared(contract: Mapping[str, Any]) -> bool:
    if not isinstance(contract, Mapping):
        return False
    problem = copy_mapping(contract.get("problem_contract"))
    actions = copy_mapping(problem.get("actions"))
    shape_axes = copy_mapping(copy_mapping(contract.get("shape_prior6")).get("axes"))
    direct_axes = copy_mapping(copy_mapping(contract.get("direct_controls")).get("axes"))
    return any([
        int(actions.get("count", 0) or 0) > 0,
        bool(clean_list(problem.get("observation_channels"))),
        clean_text(problem.get("decision_scope")) != "",
        any((v or 0.0) != 0.5 for v in shape_axes.values()),
        any((v or 0.0) != 0.5 for v in direct_axes.values()),
    ])


def export_runtime_contract(contract: Any) -> Dict[str, Any]:
    if not isinstance(contract, Mapping):
        return build_runtime_contract({})
    return deep_export_bundle(contract, [
        "problem_contract",
        "shape_prior6",
        "direct_controls",
        "study_overrides",
    ])


__all__ = [
    "build_runtime_contract",
    "contract_is_declared",
    "export_runtime_contract",
    "normalize_shape_prior",
    "normalize_kernel_posture",
    "normalize_study_overrides",
]
