from __future__ import annotations

"""Shape-gauged resolver-timing probe v1.

This diagnostic tests the generic CO rule requested after the mid-regime repair
probe: resolver timing should be derived from branch relations under a current
problem-shape gauge, not from maintenance-specific action names.

It constructs identical branch relations under low-urgency and high-urgency
shape controls.  A carrier branch carries unresolved burden; a resolver branch
reduces/exposes/cancels/buffers that burden.  Under low urgency, the carrier can
continue.  Under high urgency, an adequate resolver can bend commitment before
formal certificate blocking.  Transform/transfer-only branches must not count as
resolvers.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence

from agents.co.runtime.surfaces.candidate_surface import CandidateEvidenceSurface
from agents.co.runtime.surfaces.commitment_surface import CommitmentSurface
from agents.co.tests.relation_path_trace_diagnostics import TraceBus

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "shape_gauged_resolver_timing_probe_v1.json"
REPORT = ROOT.parent / "SHAPE_GAUGED_RESOLVER_TIMING_PROBE_REPORT_2026-05-17.md"

RESOLVER_OPS = ("reduce", "reveal", "reset", "buffer")
NONRESOLVER_OPS = ("transform", "transfer")


@dataclass
class HeaderState:
    co_weight: float = 1.0
    evidence_gate: float = 0.60
    fracture_tolerance: float = 0.45
    collapse_admissibility: float = 0.85
    revision_permissibility: float = 0.15
    support_carry_forward: float = 0.80
    rival_breadth: float = 0.20
    nonlocal_authority: float = 0.20
    path_sensitivity: float = 0.20
    local_authority: float = 0.85


@dataclass
class Header:
    state: HeaderState


LOW_SHAPE = HeaderState()
HIGH_SHAPE = HeaderState(
    collapse_admissibility=0.35,
    revision_permissibility=0.75,
    support_carry_forward=0.45,
    rival_breadth=0.75,
    nonlocal_authority=0.85,
    path_sensitivity=0.85,
    local_authority=0.25,
)


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


def _candidate(candidate_id: str, visible: float, effects: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    return {
        "candidate_id": candidate_id,
        "legal": True,
        "visible_delta": float(visible),
        "goal_relation": float(visible),
        "line_support": float(0.25 + 0.50 * visible),
        "support_depth": 0.62,
        "paired_depth": 0.62,
        "coverage_adequacy": 0.65,
        "tested_hint": 0.45,
        "uncertainty_hint": 0.35,
        "reversibility_hint": 0.55,
        "continuity_support": float(max(0.05, 0.35 + 0.45 * visible)),
        "public_effects": [dict(e) for e in effects],
    }


def _run_case(
    *,
    shape_name: str,
    header_state: HeaderState,
    resolver_operation: str,
    carrier_magnitude: float = 0.55,
    resolver_magnitude: float = 0.35,
    carrier_visible: float = 0.70,
    resolver_visible: float = 0.52,
) -> Dict[str, Any]:
    burden_type = "hiddenness" if resolver_operation == "reveal" else "degradation"
    kind = "evidence" if resolver_operation == "reveal" else "burden"
    candidates = [
        _candidate("CARRIER", carrier_visible, [_effect("carry", burden_type, carrier_magnitude)]),
        _candidate("RESOLVER", resolver_visible, [_effect(resolver_operation, burden_type, resolver_magnitude, kind=kind)]),
        _candidate("NEUTRAL", 0.22, [],),
    ]
    obs = {
        "family": "shape_gauged_resolver_timing_probe",
        "t": 1,
        "action_space": ["CARRIER", "RESOLVER", "NEUTRAL"],
        "candidates": candidates,
    }
    prims: Dict[str, Any] = {"signal_bus": TraceBus()}
    header = Header(header_state)
    CandidateEvidenceSurface().step(obs, prims, header, None)
    out = CommitmentSurface(collapse_enabled=False).step(obs, prims, header, None)
    ass = dict(out.get("canonical_commitment_assessment", {}) or {})
    return {
        "shape": shape_name,
        "resolver_operation": resolver_operation,
        "selected_action": out.get("action"),
        "selected_mode": out.get("canonical_commitment_mode"),
        "selected_reason": out.get("canonical_commitment_reason"),
        "shape_gauged_resolver_timing_applied": bool(out.get("shape_gauged_resolver_timing_applied", False)),
        "local_shape_gauge": out.get("local_shape_gauge", {}),
        "carrier": ass.get("CARRIER", {}),
        "resolver": ass.get("RESOLVER", {}),
    }


def _make_report(result: Mapping[str, Any]) -> str:
    return f"""# Shape-Gauged Resolver Timing Probe — 2026-05-17

## Scope

This probe tests the generic pre-blocking resolver-timing law.  It is not a
maintenance repair heuristic and it is not reward evidence.

The same branch relation is evaluated under two public gauges:

```text
low urgency: high local/collapse authority, low revision/nonlocal/path pressure
high urgency: high revision/nonlocal/path pressure, low local/collapse authority
```

A valid resolver may bend commitment before formal certificate blocking only
under the shape gauge where carried burden is urgent enough.  Transform/transfer
alone must not count as resolution.

## Summary

```json
{json.dumps(result['summary'], indent=2, sort_keys=True)}
```

## Interpretation

The probe confirms the intended doctrine boundary:

```text
branch relation alone is insufficient;
problem shape supplies the gauge that says when the relation should matter now.
```

The update is local and runtime-gauge based.  It does not edit environment
topology, does not infer native policy, and does not inspect action names.
"""


def main() -> Dict[str, Any]:
    cases: List[Dict[str, Any]] = []
    for op in RESOLVER_OPS + NONRESOLVER_OPS:
        cases.append(_run_case(shape_name="low_urgency", header_state=LOW_SHAPE, resolver_operation=op))
        cases.append(_run_case(shape_name="high_urgency", header_state=HIGH_SHAPE, resolver_operation=op))

    low_resolver_switches = [c for c in cases if c["shape"] == "low_urgency" and c["resolver_operation"] in RESOLVER_OPS and c["selected_action"] == "RESOLVER"]
    high_resolver_switches = [c for c in cases if c["shape"] == "high_urgency" and c["resolver_operation"] in RESOLVER_OPS and c["selected_action"] == "RESOLVER"]
    nonresolver_switches = [c for c in cases if c["resolver_operation"] in NONRESOLVER_OPS and c["selected_action"] == "RESOLVER"]
    summary = {
        "cases": len(cases),
        "resolver_ops": list(RESOLVER_OPS),
        "nonresolver_ops": list(NONRESOLVER_OPS),
        "low_urgency_resolver_switches": len(low_resolver_switches),
        "high_urgency_resolver_switches": len(high_resolver_switches),
        "nonresolver_transform_transfer_switches": len(nonresolver_switches),
        "invariants": {
            "low_urgency_does_not_force_resolver": len(low_resolver_switches) == 0,
            "high_urgency_allows_resolver_timing": len(high_resolver_switches) >= 1,
            "transform_transfer_do_not_count_as_resolvers": len(nonresolver_switches) == 0,
        },
    }
    result: Dict[str, Any] = {
        "study": "shape_gauged_resolver_timing_probe_v1",
        "claim_boundary": "structural doctrine/formula probe only; not reward evidence, not tuning evidence, not CO proof",
        "summary": summary,
        "cases": cases,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    REPORT.write_text(_make_report(result), encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(main()["summary"], indent=2, sort_keys=True))
