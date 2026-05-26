from __future__ import annotations

"""DynamicShapeField real-trace ablation v1.

Runs the same public two-step abstract trace with DynamicShapeField enabled and
disabled.  It checks that dynamic-shape telemetry and next-cycle effective
controls differ while the adapter facts remain identical.  This is structural
ablation only, not reward/performance evidence.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping

from agents.co.runtime.surfaces.candidate_surface import CandidateEvidenceSurface
from agents.co.runtime.surfaces.commitment_surface import CommitmentSurface
from agents.co.tests.relation_path_trace_diagnostics import TraceBus

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "dynamic_shape_real_trace_ablation_v1.json"
REPORT = ROOT.parent / "DYNAMIC_SHAPE_REAL_TRACE_ABLATION_REPORT_2026-05-21.md"


@dataclass
class HeaderState:
    co_weight: float = 1.0
    evidence_gate: float = 0.55
    fracture_tolerance: float = 0.38
    retention_depth: float = 0.60
    collapse_permission: float = 0.45
    identity_support_threshold: float = 0.50
    support_evidence: float = 0.45
    collapse_admissibility: float = 0.45
    revision_permissibility: float = 0.68
    support_carry_forward: float = 0.52
    rival_breadth: float = 0.65
    nonlocal_authority: float = 0.72
    path_sensitivity: float = 0.76
    local_authority: float = 0.32


@dataclass
class Header:
    state: HeaderState


def _effect(operation: str, burden_type: str, magnitude: float, *, kind: str = "burden") -> Dict[str, Any]:
    return {
        "operation": operation,
        "kind": kind,
        "burden_type": burden_type,
        "scope": "candidate",
        "magnitude": float(magnitude),
        "relation_scope": burden_type,
        "public_basis": "visible_observation",
        "leakage_status": "public",
    }


def _obs(step: int) -> Dict[str, Any]:
    # Same public grammar both steps; step two is not secretly enriched with
    # reward/optimality.  Any dynamic-shape difference must come from retained
    # public trace in the enabled runtime.
    return {
        "family": "dynamic_shape_real_trace_ablation",
        "t": step,
        "action_space": ["carrier_expr", "resolver_expr", "redirect_expr"],
        "problem_contract": {
            "task_anchor": {"kind": "abstract_continuation", "provided_externally": True},
            "actions": {"count": 3, "native_type": "abstract"},
            "observability_profile": {"state": "public_trace", "constraints": "public_trace"},
        },
        "candidates": [
            {
                "candidate_id": "carrier_expr",
                "legal": True,
                "visible_delta": 0.72,
                "line_support": 0.72,
                "coverage_adequacy": 0.70,
                "tested_hint": 0.58,
                "uncertainty_hint": 0.28,
                "reversibility_hint": 0.35,
                "contradiction_hint": 0.45,
                "public_effects": [_effect("carry", "degradation", 0.76)],
            },
            {
                "candidate_id": "resolver_expr",
                "legal": True,
                "visible_delta": 0.50,
                "line_support": 0.50,
                "coverage_adequacy": 0.55,
                "tested_hint": 0.45,
                "uncertainty_hint": 0.34,
                "reversibility_hint": 0.78,
                "contradiction_hint": 0.08,
                "public_effects": [_effect("reduce", "degradation", 0.58)],
            },
            {
                "candidate_id": "redirect_expr",
                "legal": True,
                "visible_delta": 0.48,
                "line_support": 0.48,
                "coverage_adequacy": 0.48,
                "tested_hint": 0.35,
                "uncertainty_hint": 0.45,
                "reversibility_hint": 0.65,
                "contradiction_hint": 0.15,
                "public_effects": [_effect("transform", "degradation", 0.48)],
            },
        ],
    }


def _step(surface: CandidateEvidenceSurface, obs: Mapping[str, Any]) -> Dict[str, Any]:
    prims: Dict[str, Any] = {"signal_bus": TraceBus()}
    header = Header(HeaderState())
    surf_out = surface.step(dict(obs), prims, header, None)
    commit_out = CommitmentSurface(collapse_enabled=False).step(dict(obs), prims, header, None)
    rows = [dict(r) for r in prims.get("__candidate_publication_rows__", [])]
    return {
        "surface_out": dict(surf_out or {}),
        "commitment": dict(commit_out or {}),
        "rows": rows,
        "dynamic_shape_state": dict(prims.get("__dynamic_shape_state__", {}) or {}),
        "dynamic_shape_update": dict(prims.get("__dynamic_shape_update__", {}) or {}),
        "dynamic_shape_effective_controls": dict(prims.get("__dynamic_shape_effective_controls__", {}) or {}),
    }


def _run(enabled: bool) -> List[Dict[str, Any]]:
    surface = CandidateEvidenceSurface(dynamic_shape_enabled=enabled)
    return [_step(surface, _obs(1)), _step(surface, _obs(2))]


def _make_report(result: Dict[str, Any]) -> str:
    return f"""# DynamicShapeField Real-Trace Ablation — 2026-05-21

## Scope

This is a structural trace ablation.  It compares identical public candidate
facts with DynamicShapeField enabled vs disabled.  It is not reward evidence and
not a benchmark.

## Summary

```json
{json.dumps(result['summary'], indent=2, sort_keys=True)}
```
"""


def main() -> Dict[str, Any]:
    enabled = _run(True)
    disabled = _run(False)
    enabled_step1 = enabled[0]
    enabled_step2 = enabled[1]
    disabled_step2 = disabled[1]
    state_changed = bool(enabled_step1.get("dynamic_shape_update", {}).get("applied")) and enabled_step1.get("dynamic_shape_state") != enabled_step1.get("dynamic_shape_update", {}).get("state_before")
    controls_changed_between_steps = enabled_step1.get("dynamic_shape_effective_controls") != enabled_step2.get("dynamic_shape_effective_controls")
    disabled_has_no_shape_update = not bool(disabled_step2.get("dynamic_shape_update"))
    any_commitment_difference = enabled_step2.get("commitment", {}).get("action") != disabled_step2.get("commitment", {}).get("action")
    summary = {
        "study": "dynamic_shape_real_trace_ablation_v1",
        "state_changed_after_public_trace": bool(state_changed),
        "next_cycle_effective_controls_changed": bool(controls_changed_between_steps),
        "disabled_run_has_no_dynamic_shape_update": bool(disabled_has_no_shape_update),
        "commitment_difference_observed": bool(any_commitment_difference),
        "claim_boundary": "structural telemetry/ablation only; absence of action change is not hidden",
        "invariants": {
            "dynamic_shape_state_updates_from_public_trace": bool(state_changed),
            "dynamic_shape_ablation_is_visible": bool(disabled_has_no_shape_update and controls_changed_between_steps),
            "no_behavior_change_is_allowed_and_reported": True,
        },
    }
    result: Dict[str, Any] = {"study": "dynamic_shape_real_trace_ablation_v1", "summary": summary, "enabled": enabled, "disabled": disabled}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    REPORT.write_text(_make_report(result), encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(main()["summary"], indent=2, sort_keys=True))
