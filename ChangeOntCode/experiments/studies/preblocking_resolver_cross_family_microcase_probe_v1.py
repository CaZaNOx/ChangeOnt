from __future__ import annotations

"""Cross-family pre-blocking resolver timing microcase probe v1.

This is a generic readout audit.  It constructs anonymous carrier/resolver rows
under different public shape profiles and asks whether CommitmentSurface bends
commitment before formal blockage.  The probe uses no family names, no native
solver labels, no rewards, no hidden state, and no topology edits.  It does not
set benchmark expectations; it exposes whether the generic timing gate is too
permissive, too strict, or correctly inert.
"""

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping, Tuple

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agents.co.runtime.surfaces.commitment_surface import CommitmentSurface

OUT_JSON = ROOT / "outputs" / "preblocking_resolver_cross_family_microcase_probe_v1.json"
REPORT_MD = ROOT.parent / "PREBLOCKING_RESOLVER_CROSS_FAMILY_MICROCASE_PROBE_REPORT_2026-05-22.md"

CLAIM_BOUNDARY = (
    "Cross-family pre-blocking resolver microcase audit only. It is not a benchmark, "
    "not maintenance tuning, not SOTA comparison, and not CO proof."
)


@dataclass
class HeaderState:
    collapse_admissibility: float = 0.45
    revision_permissibility: float = 0.65
    support_carry_forward: float = 0.45
    rival_breadth: float = 0.65
    nonlocal_authority: float = 0.70
    path_sensitivity: float = 0.70
    local_authority: float = 0.35
    evidence_gate: float = 0.55
    fracture_tolerance: float = 0.38


@dataclass
class Header:
    state: HeaderState


def _row(
    action: str,
    *,
    support: float,
    burden: float,
    stability: float,
    resolver_support: float = 0.0,
    carrier_pressure: float = 0.0,
    ready: bool = False,
    blocker: float = 0.08,
    recursion: float = 0.12,
) -> Dict[str, Any]:
    return {
        "action": action,
        "candidate_id": action,
        "support_mass": support,
        "decision_state": support,
        "local_support": support,
        "field_score": support,
        "contradiction_burden": burden,
        "burden_accumulation": burden,
        "continuation_instability": burden,
        "burden_trend": 0.04,
        "commitment_stability": stability,
        "continuation_viability": stability,
        "support_persistence": stability,
        "sampling_demand": 0.05,
        "uncertainty": 0.24,
        "branch_internal_resolver_support": resolver_support,
        "branch_internal_relief_support": resolver_support,
        "branch_internal_raw_carry_pressure": carrier_pressure,
        "collapse_certificate_ready": ready,
        "collapse_certificate_score": 0.56 if ready else 0.18,
        "collapse_certificate_blocker_pressure": blocker,
        "collapse_certificate_recursion_demand": recursion,
        "collapse_blockers": [],
    }


def _shape_axes(profile: str) -> Dict[str, float]:
    profiles = {
        "low_urgency_local": {
            "hidden_decisiveness": 0.25, "reshapeability": 0.25, "local_cue_reliability": 0.75,
            "revision_cost": 0.25, "consequence_span": 0.25, "topology_constraint": 0.25,
        },
        "medium_mixed": {
            "hidden_decisiveness": 0.50, "reshapeability": 0.50, "local_cue_reliability": 0.50,
            "revision_cost": 0.50, "consequence_span": 0.50, "topology_constraint": 0.50,
        },
        "high_hidden_consequence": {
            "hidden_decisiveness": 0.75, "reshapeability": 0.75, "local_cue_reliability": 0.25,
            "revision_cost": 0.75, "consequence_span": 0.75, "topology_constraint": 0.75,
        },
        "high_topology_revision": {
            "hidden_decisiveness": 0.50, "reshapeability": 0.75, "local_cue_reliability": 0.25,
            "revision_cost": 0.75, "consequence_span": 0.50, "topology_constraint": 0.75,
        },
    }
    return dict(profiles[profile])


def _dynamic_controls(profile: str, urgency: float | None = None) -> Dict[str, float]:
    axes = _shape_axes(profile)
    hidden = axes["hidden_decisiveness"]
    rev = axes["revision_cost"]
    cons = axes["consequence_span"]
    topo = axes["topology_constraint"]
    local_cue = axes["local_cue_reliability"]
    u = urgency if urgency is not None else max(0.05, min(0.95, 0.28 * hidden + 0.28 * rev + 0.28 * cons + 0.16 * topo))
    return {
        "local_authority": max(0.15, min(0.85, local_cue - 0.20 * u)),
        "nonlocal_authority": max(0.15, min(0.90, 0.35 + 0.45 * u)),
        "path_sensitivity": max(0.15, min(0.90, 0.35 + 0.42 * u)),
        "revision_permissibility": max(0.15, min(0.90, 0.35 + 0.38 * u)),
        "collapse_admissibility": max(0.20, min(0.85, 0.60 - 0.20 * u)),
        "rival_breadth": max(0.20, min(0.85, 0.35 + 0.35 * u)),
        "dynamic_shape_urgency": u,
    }


def _commit(case: Mapping[str, Any]) -> Tuple[str, Dict[str, Any]]:
    carrier_pressure = float(case.get("carrier_pressure", 0.45))
    resolver_support = float(case.get("resolver_support", 0.34))
    carrier_support = float(case.get("carrier_support", 0.70))
    resolver_base_support = float(case.get("resolver_base_support", 0.60))
    rows = [
        _row(
            "CARRY_CONTINUATION",
            support=carrier_support,
            burden=float(case.get("carrier_burden", 0.10)),
            stability=float(case.get("carrier_stability", 0.65)),
            resolver_support=0.0,
            carrier_pressure=carrier_pressure,
            ready=False,
            blocker=float(case.get("carrier_blocker", 0.10)),
            recursion=float(case.get("carrier_recursion", 0.18)),
        ),
        _row(
            "RESOLVE_CONTINUATION",
            support=resolver_base_support,
            burden=float(case.get("resolver_burden", 0.14)),
            stability=float(case.get("resolver_stability", 0.55)),
            resolver_support=resolver_support,
            carrier_pressure=0.0,
            ready=True,
            blocker=0.0,
            recursion=0.04,
        ),
    ]
    obs = {
        "action_space": ["CARRY_CONTINUATION", "RESOLVE_CONTINUATION"],
        "shape_prior6": {"axes": _shape_axes(str(case["shape_profile"]))},
    }
    prims = {
        "__candidate_publication_rows__": rows,
        "__dynamic_shape_effective_controls__": _dynamic_controls(str(case["shape_profile"]), case.get("urgency")),
    }
    scores = {r["action"]: float(r["field_score"]) for r in rows}
    choice, tel = CommitmentSurface()._canonical_commitment_choice(
        scores, obs, prims, Header(HeaderState()), set(), ["CARRY_CONTINUATION", "RESOLVE_CONTINUATION"]
    )
    return str(choice), tel


def _case_result(case: Mapping[str, Any]) -> Dict[str, Any]:
    choice, tel = _commit(case)
    applied = bool(tel.get("shape_gauged_resolver_timing_applied"))
    gauge = tel.get("local_shape_gauge", {}) if isinstance(tel.get("local_shape_gauge", {}), dict) else {}
    assessment = tel.get("canonical_commitment_assessment", {}) if isinstance(tel.get("canonical_commitment_assessment", {}), dict) else {}
    expected = case.get("expected")
    if expected == "trigger":
        status = "passed" if applied and choice == "RESOLVE_CONTINUATION" else "watchpoint"
    elif expected == "no_trigger":
        status = "passed" if not applied else "watchpoint"
    else:
        status = "observed"
    return {
        "id": case["id"],
        "description": case["description"],
        "shape_profile": case["shape_profile"],
        "expected": expected,
        "status": status,
        "selected": choice,
        "commitment_mode": tel.get("canonical_commitment_mode"),
        "commitment_reason": tel.get("canonical_commitment_reason"),
        "shape_gauged_resolver_timing_applied": applied,
        "local_shape_gauge": gauge,
        "assessment": assessment,
    }


def main() -> Dict[str, Any]:
    cases: List[Dict[str, Any]] = [
        {
            "id": "PB1_HIGH_URGENCY_HIGH_CARRIER_TRIGGERS",
            "description": "High hidden/consequence shape, explicit resolver, and carrier pressure above gate should bend to resolver.",
            "shape_profile": "high_hidden_consequence", "carrier_pressure": 0.50, "resolver_support": 0.35,
            "carrier_support": 0.70, "resolver_base_support": 0.60, "urgency": 0.82, "expected": "trigger",
        },
        {
            "id": "PB2_HIGH_URGENCY_BORDERLINE_CARRIER_AUDIT",
            "description": "High urgency with borderline carrier pressure tests whether the carrier gate is too strict.",
            "shape_profile": "high_hidden_consequence", "carrier_pressure": 0.46, "resolver_support": 0.35,
            "carrier_support": 0.70, "resolver_base_support": 0.60, "urgency": 0.82, "expected": "trigger",
        },
        {
            "id": "PB3_MEDIUM_MIXED_MODERATE_CARRIER_OBSERVE",
            "description": "Medium mixed shape with moderate carrier pressure and explicit resolver mirrors the unresolved first-pass calibration site without using family labels.",
            "shape_profile": "medium_mixed", "carrier_pressure": 0.36, "resolver_support": 0.22,
            "carrier_support": 0.70, "resolver_base_support": 0.60, "expected": "observe",
        },
        {
            "id": "PB4_LOW_URGENCY_NO_TRIGGER",
            "description": "Local/low-urgency shape should not pre-block a stronger carrier merely because a resolver exists.",
            "shape_profile": "low_urgency_local", "carrier_pressure": 0.50, "resolver_support": 0.35,
            "carrier_support": 0.70, "resolver_base_support": 0.60, "expected": "no_trigger",
        },
        {
            "id": "PB5_WEAK_RESOLVER_NO_TRIGGER",
            "description": "High urgency but weak resolver support should not displace the carrier.",
            "shape_profile": "high_hidden_consequence", "carrier_pressure": 0.52, "resolver_support": 0.08,
            "carrier_support": 0.70, "resolver_base_support": 0.60, "urgency": 0.82, "expected": "no_trigger",
        },
        {
            "id": "PB6_LARGE_CARRIER_ADVANTAGE_NO_TRIGGER",
            "description": "A large material carrier advantage should not be erased by moderate resolver timing pressure.",
            "shape_profile": "high_hidden_consequence", "carrier_pressure": 0.50, "resolver_support": 0.30,
            "carrier_support": 0.88, "resolver_base_support": 0.45, "urgency": 0.82, "expected": "no_trigger",
        },
    ]
    results = [_case_result(c) for c in cases]
    watchpoints = [r for r in results if r["status"] == "watchpoint"]
    out = {
        "study": "preblocking_resolver_cross_family_microcase_probe_v1",
        "claim_boundary": CLAIM_BOUNDARY,
        "cases": len(results),
        "passed": sum(1 for r in results if r["status"] == "passed"),
        "observed": sum(1 for r in results if r["status"] == "observed"),
        "watchpoints": len(watchpoints),
        "case_results": results,
        "audit_findings": [
            {
                "id": "PB_AUDIT_CARRIER_GATE_BORDERLINE",
                "severity": "medium" if any(r["id"] == "PB2_HIGH_URGENCY_BORDERLINE_CARRIER_AUDIT" and r["status"] == "watchpoint" for r in results) else "low",
                "finding": "The generic carrier-gate calibration is checked at a borderline high-urgency site where an explicit resolver should become eligible before score comparison.",
                "evidence": "See PB2 local_shape_gauge preblocking_min_carrier_pressure versus carrier_pressure_for_timing; after calibration PB2 should pass without using family-specific thresholds.",
                "next_action": "Keep the calibration generic and continue rejecting family-specific thresholds.",
            },
            {
                "id": "PB_AUDIT_LOW_URGENCY_PROTECTION",
                "severity": "low",
                "finding": "Low urgency and weak resolver cases remain protected from premature resolver displacement.",
                "evidence": "PB4/PB5/PB6 expected no-trigger cases should remain non-triggering.",
                "next_action": "Any future loosening must preserve these negative controls.",
            },
        ],
        "recommendation": "Do not tune per problem. The generic carrier-gate calibration must remain guarded by the low-urgency, weak-resolver, and large-carrier-advantage negative controls."
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
    _write_report(out)
    return out


def _fmt(x: Any) -> str:
    try:
        return f"{float(x):.3f}"
    except Exception:
        return str(x)


def _write_report(out: Mapping[str, Any]) -> None:
    lines: List[str] = []
    lines.append("# Pre-blocking Resolver Cross-Family Microcase Probe v1 — 2026-05-22")
    lines.append("")
    lines.append(f"Claim boundary: {CLAIM_BOUNDARY}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- cases: {out['cases']}")
    lines.append(f"- passed: {out['passed']}")
    lines.append(f"- observed-only: {out['observed']}")
    lines.append(f"- watchpoints: {out['watchpoints']}")
    lines.append("")
    lines.append("## Case table")
    lines.append("")
    lines.append("| case | profile | expected | status | selected | applied | gate | pressure | resolver_required |")
    lines.append("|---|---|---:|---:|---|---:|---:|---:|---:|")
    for r in out.get("case_results", []):
        g = r.get("local_shape_gauge", {}) if isinstance(r.get("local_shape_gauge", {}), dict) else {}
        lines.append(
            "| {id} | {profile} | {expected} | {status} | {selected} | {applied} | {gate} | {pressure} | {req} |".format(
                id=r.get("id"), profile=r.get("shape_profile"), expected=r.get("expected"), status=r.get("status"),
                selected=r.get("selected"), applied=r.get("shape_gauged_resolver_timing_applied"),
                gate=_fmt(g.get("preblocking_min_carrier_pressure")), pressure=_fmt(g.get("carrier_pressure_for_timing")),
                req=_fmt(g.get("preblocking_required_resolver_support")),
            )
        )
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("The probe uses anonymous `CARRY_CONTINUATION` / `RESOLVE_CONTINUATION` rows and public shape profiles only. It does not inspect family names, native action semantics, rewards, hidden state, baselines, or topology.")
    lines.append("")
    lines.append("A watchpoint here is not a license to tune maintenance or any other problem. After the generic carrier-gate calibration, the borderline high-urgency positive case should pass while the low-urgency, weak-resolver, and large-carrier-advantage negative controls remain protected.")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
