from __future__ import annotations

"""Resolver-threshold microcase probe v1.

This diagnostic isolates the coefficient question exposed by resolver formula
sensitivity: when may an unblocked resolver branch displace a certificate-blocked
carrier-only branch during ``reopen_or_sample``?

The probe is structural, not a reward benchmark.  It sweeps public resolver
magnitudes against public carrier magnitudes and records the effective resolver
support required by CommitmentSurface.  The intended law is not "any resolver
label wins"; a resolver must be adequate to the unresolved burden it is being
used to reopen.
"""

import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence, Tuple

from experiments.studies.real_adapter_formula_sensitivity_probe_v1 import _run_candidate_commitment_with_params

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "resolver_threshold_microcase_probe_v1.json"

CARRIER_MAGNITUDES = [0.25, 0.45, 0.65, 0.85, 1.00]
RESOLVER_MAGNITUDES = [0.00, 0.02, 0.04, 0.06, 0.079, 0.08, 0.10, 0.12, 0.16, 0.20, 0.35, 0.60, 0.90]
RESOLVER_OPS = [
    # Use the same hiddenness burden for each operation here so the sampled
    # carrier branch is genuinely blocked and the only variable is resolver
    # operation semantics, not family-specific support differences.
    ("expose", "hiddenness", "hiddenness"),
    ("reduce", "hiddenness", "hiddenness"),
    ("cancel", "hiddenness", "hiddenness"),
    ("buffer", "hiddenness", "hiddenness"),
]
NONRESOLVER_OPS = [
    ("transform", "hiddenness", "hiddenness"),
    ("transfer", "hiddenness", "hiddenness"),
]


def _effect(
    operation: str,
    burden_type: str,
    magnitude: float,
    *,
    kind: str = "burden",
    relation_scope: str | None = None,
) -> Dict[str, Any]:
    return {
        "operation": operation,
        "kind": kind,
        "burden_type": burden_type,
        "scope": "candidate",
        "magnitude": float(magnitude),
        "relation_scope": relation_scope or burden_type,
        "public_basis": "visible_observation",
        "leakage_status": "public",
    }


def _candidate(
    candidate_id: str,
    visible: float,
    effects: Sequence[Mapping[str, Any]],
    *,
    uncertainty: float = 0.80,
    coverage: float = 0.70,
    tested: float = 0.60,
    reversibility: float = 0.70,
) -> Dict[str, Any]:
    return {
        "candidate_id": candidate_id,
        "legal": True,
        "visible_delta": float(visible),
        "line_support": float(visible),
        "coverage_adequacy": float(coverage),
        "tested_hint": float(tested),
        "uncertainty_hint": float(uncertainty),
        "reversibility_hint": float(reversibility),
        "public_effects": [dict(e) for e in effects],
    }


def _assessment(commit: Mapping[str, Any], action: str) -> Dict[str, float]:
    rec = dict(dict(commit.get("canonical_commitment_assessment", {}) or {}).get(action, {}) or {})
    out: Dict[str, float] = {}
    for key in (
        "support",
        "sampling_score",
        "continuation_score",
        "resolver_support",
        "carrier_only_pressure",
        "collapse_blocked",
        "collapse_certificate_blocker_pressure",
        "collapse_certificate_recursion_demand",
        "certificate_blocks_dominance",
    ):
        try:
            out[key] = round(float(rec.get(key, 0.0) or 0.0), 6)
        except Exception:
            out[key] = 0.0
    return out


def _run_case(
    *,
    carrier_mag: float,
    resolver_mag: float,
    resolver_op: str = "expose",
    burden_type: str = "hiddenness",
    kind: str = "hiddenness",
    carrier_visible: float = 0.70,
    resolver_visible: float = 0.66,
) -> Dict[str, Any]:
    candidates = [
        _candidate("carrier", carrier_visible, [_effect("carry", burden_type, carrier_mag, kind=kind)]),
        _candidate("resolver", resolver_visible, [_effect(resolver_op, burden_type, resolver_mag, kind=kind)]),
    ]
    rows, commit = _run_candidate_commitment_with_params(
        candidates,
        f"resolver_threshold:{resolver_op}:{carrier_mag:.2f}:{resolver_mag:.3f}",
        {},
    )
    carrier_ass = _assessment(commit, "carrier")
    resolver_ass = _assessment(commit, "resolver")
    return {
        "carrier_magnitude": float(carrier_mag),
        "resolver_magnitude": float(resolver_mag),
        "resolver_operation": resolver_op,
        "burden_type": burden_type,
        "selected_action": commit.get("action"),
        "selected_mode": commit.get("canonical_commitment_mode"),
        "selected_reason": commit.get("canonical_commitment_reason"),
        "certificate_aware_reopen_or_sample_applied": bool(commit.get("certificate_aware_reopen_or_sample_applied", False)),
        "required_resolver_support": round(float(commit.get("required_resolver_support", 0.0) or 0.0), 6),
        "sampling_gate_margin": round(float(commit.get("sampling_gate_margin", 0.0) or 0.0), 6),
        "sampling_support_advantage_limit": round(float(commit.get("sampling_support_advantage_limit", 0.0) or 0.0), 6),
        "selected_sampling_gap_before_certificate_gating": round(float(commit.get("selected_sampling_gap_before_certificate_gating", 0.0) or 0.0), 6),
        "selected_sampling_support_gap_before_certificate_gating": round(float(commit.get("selected_sampling_support_gap_before_certificate_gating", 0.0) or 0.0), 6),
        "carrier_assessment": carrier_ass,
        "resolver_assessment": resolver_ass,
        "rows": [
            {
                "action": r.get("action"),
                "branch_internal_operation_counts": dict(r.get("branch_internal_operation_counts", {}) or {}),
                "branch_internal_resolver_support": r.get("branch_internal_resolver_support"),
                "branch_internal_transform_pressure": r.get("branch_internal_transform_pressure"),
                "branch_internal_unresolved_pressure": r.get("branch_internal_unresolved_pressure"),
                "branch_internal_hiddenness_pressure": r.get("branch_internal_hiddenness_pressure"),
                "collapse_blockers": list(r.get("collapse_blockers", []) or []),
            }
            for r in rows
        ],
    }


def _first_switch(rows: Sequence[Mapping[str, Any]]) -> float | None:
    switched = [float(r["resolver_magnitude"]) for r in rows if r.get("certificate_aware_reopen_or_sample_applied")]
    return min(switched) if switched else None


def main() -> Dict[str, Any]:
    sweep_cases: List[Dict[str, Any]] = []
    for carrier_mag in CARRIER_MAGNITUDES:
        for resolver_mag in RESOLVER_MAGNITUDES:
            sweep_cases.append(_run_case(carrier_mag=carrier_mag, resolver_mag=resolver_mag))

    by_carrier: Dict[str, Dict[str, Any]] = {}
    for carrier_mag in CARRIER_MAGNITUDES:
        rows = [r for r in sweep_cases if abs(float(r["carrier_magnitude"]) - carrier_mag) < 1e-9]
        reqs = [float(r["required_resolver_support"]) for r in rows if float(r.get("required_resolver_support", 0.0) or 0.0) > 0.0]
        by_carrier[f"{carrier_mag:.2f}"] = {
            "required_resolver_support_min": min(reqs) if reqs else 0.0,
            "required_resolver_support_max": max(reqs) if reqs else 0.0,
            "first_switch_resolver_magnitude": _first_switch(rows),
            "switch_count": sum(1 for r in rows if r.get("certificate_aware_reopen_or_sample_applied")),
            "selected_actions": dict(Counter(str(r.get("selected_action")) for r in rows)),
        }

    operation_cases: List[Dict[str, Any]] = []
    for op, burden_type, kind in RESOLVER_OPS:
        operation_cases.append(_run_case(carrier_mag=0.85, resolver_mag=0.35, resolver_op=op, burden_type=burden_type, kind=kind))
    for op, burden_type, kind in NONRESOLVER_OPS:
        operation_cases.append(_run_case(carrier_mag=0.85, resolver_mag=0.90, resolver_op=op, burden_type=burden_type, kind=kind))

    weak_threshold_cases = [
        _run_case(carrier_mag=0.85, resolver_mag=0.079),
        _run_case(carrier_mag=0.85, resolver_mag=0.08),
        _run_case(carrier_mag=0.85, resolver_mag=0.20),
        _run_case(carrier_mag=0.85, resolver_mag=0.35),
    ]

    invariants = {
        "resolver_requirement_scales_up_with_carrier_pressure": by_carrier["1.00"]["required_resolver_support_max"] > by_carrier["0.45"]["required_resolver_support_max"],
        "noise_floor_0_079_does_not_switch_high_carrier": not weak_threshold_cases[0]["certificate_aware_reopen_or_sample_applied"],
        "bare_floor_0_08_does_not_switch_high_carrier": not weak_threshold_cases[1]["certificate_aware_reopen_or_sample_applied"],
        "medium_resolver_switches_high_carrier": bool(weak_threshold_cases[3]["certificate_aware_reopen_or_sample_applied"]),
        "transform_transfer_do_not_count_as_resolvers": all(
            not c["certificate_aware_reopen_or_sample_applied"]
            and c["resolver_assessment"].get("resolver_support", 0.0) <= 0.0
            for c in operation_cases
            if c["resolver_operation"] in {"transform", "transfer"}
        ),
        "canonical_resolver_operations_can_switch": all(
            c["certificate_aware_reopen_or_sample_applied"]
            for c in operation_cases
            if c["resolver_operation"] in {"expose", "reduce", "cancel", "buffer"}
        ),
    }
    watchpoints: List[Dict[str, Any]] = []
    for name, ok in invariants.items():
        if not ok:
            watchpoints.append({"type": name, "detail": "resolver threshold invariant failed"})

    result = {
        "study": "resolver_threshold_microcase_probe_v1",
        "claim_boundary": "structural resolver-threshold audit only; not reward evidence, tuning evidence, or novelty proof",
        "resolver_threshold_law": {
            "base_floor": "resolver_support_threshold default 0.08 rejects noise-level resolver facts",
            "scaled_adequacy": "effective required support scales with the selected blocked branch's carrier_only_pressure and blocker pressure",
            "nonresolver_transform": "transform/transfer pressure is not resolver support unless paired with explicit reduce/expose/cancel/buffer fact",
        },
        "summary": {
            "sweep_cases": len(sweep_cases),
            "operation_cases": len(operation_cases),
            "watchpoint_count": len(watchpoints),
            "by_carrier": by_carrier,
            "invariants": invariants,
        },
        "weak_threshold_cases": weak_threshold_cases,
        "operation_cases": operation_cases,
        "sweep_cases": sweep_cases,
        "watchpoints": watchpoints,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
