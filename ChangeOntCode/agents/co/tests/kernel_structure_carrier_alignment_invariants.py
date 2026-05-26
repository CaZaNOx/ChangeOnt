"""Invariants for branch-internal burden carriers and relation/certificate alignment."""
from __future__ import annotations

"""Kernel structure carrier alignment invariants.

These tests protect the docs-first target in
`docs/kernel_spec/95_KERNEL_STRUCTURE_CARRIER_ALIGNMENT.md`: public effects must
survive in the correct runtime carrier even when they do not produce a
cross-branch relation.
"""

from agents.co.runtime.surfaces.relation_surface import derive_relation_surface
from agents.co.runtime.surfaces.continuation_field import apply_continuation_field
from agents.co.runtime.surfaces.collapse_certificate import apply_collapse_certificates

CONTROLS = {
    "collapse_admissibility": 0.30,
    "revision_permissibility": 0.75,
    "nonlocal_authority": 0.80,
    "path_sensitivity": 0.70,
    "rival_breadth": 0.55,
    "local_authority": 0.30,
}


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def _effect(operation: str, burden_type: str, *, magnitude: float = 0.75, kind: str = "burden", scope: str = "local", direction: str = "unresolved") -> dict:
    return {
        "effect_id": f"{operation}_{burden_type}",
        "kind": kind,
        "operation": operation,
        "burden_type": burden_type,
        "scope": scope,
        "magnitude": magnitude,
        "public_basis": "declared_transition_rule",
        "leakage_status": "public",
        "direction": direction,
        "coupling": "test_anchor",
    }


def _row(name: str, effects: list[dict], *, support: float = 0.62) -> dict:
    return {
        "action": name,
        "candidate_id": name,
        "support_mass": support,
        "local_support": support,
        "decision_state": support,
        "continuation_viability": 0.58,
        "stability_under_change": 0.58,
        "commitment_stability": 0.52,
        "uncertainty": 0.10,
        "public_effects": list(effects),
    }


def _certified(rows: list[dict]) -> list[dict]:
    rel = derive_relation_surface(rows, CONTROLS)
    field = apply_continuation_field(rel.rows, CONTROLS, relations=rel.relations)
    return apply_collapse_certificates(field, relations=rel.relations, controls=CONTROLS)


def test_branch_internal_hiddenness_survives_without_cross_branch_relation() -> None:
    row = _row("OBSERVELESS_RUN", [_effect("carry", "mechanism_hiddenness", magnitude=0.86, kind="uncertainty")])
    rel = derive_relation_surface([row], CONTROLS)
    _assert(rel.telemetry["relations_total"] == 0, "single branch should have no cross-branch relations")
    out = rel.rows[0]
    _assert(out["branch_internal_operation_count"] == 1, "public effect should survive as branch-internal operation")
    _assert(out["branch_internal_hiddenness_pressure"] > 0.80, "hiddenness should be carried internally")
    field = apply_continuation_field(rel.rows, CONTROLS, relations=rel.relations)[0]
    _assert(field["field_grey_pressure"] > 0.20, "internal hiddenness should affect field grey/uncertainty state")
    cert = apply_collapse_certificates([field], relations=rel.relations, controls=CONTROLS)[0]
    _assert("unresolved_hiddenness_burden" in cert["collapse_blockers"], f"hiddenness should reach certificate blockers: {cert}")


def test_buffering_and_masking_use_different_carriers() -> None:
    masked = _row("MASK", [_effect("mask", "degradation", magnitude=0.72, direction="appears_stable")])
    buffered = _row("BUFFER", [_effect("buffer", "degradation", magnitude=0.72, direction="absorb")])
    certs = {r["action"]: r for r in _certified([masked, buffered])}
    _assert(certs["MASK"]["branch_internal_masking_pressure"] > 0.65, "masking pressure should be explicit")
    _assert(certs["BUFFER"]["branch_internal_buffering_support"] > 0.65, "buffering support should be explicit")
    _assert("masked_unresolved_burden" in certs["MASK"]["collapse_blockers"], f"masking should block/caution collapse: {certs['MASK']}")
    _assert("masked_unresolved_burden" not in certs["BUFFER"]["collapse_blockers"], f"buffering should not be treated as masking: {certs['BUFFER']}")
    _assert(certs["BUFFER"]["collapse_certificate_blocker_pressure"] < certs["MASK"]["collapse_certificate_blocker_pressure"], "buffering should carry lower blocker pressure than masking")


def test_branch_internal_reducer_can_affect_field_without_relation() -> None:
    row = _row("SAMPLE_ARM", [
        _effect("carry", "reward_uncertainty_arm", magnitude=0.65, kind="uncertainty"),
        _effect("reduce", "reward_uncertainty_arm", magnitude=0.65, kind="evidence", direction="sample"),
    ])
    rel = derive_relation_surface([row], CONTROLS)
    _assert(rel.telemetry["relations_total"] == 0, "single sample branch should not need cross-branch relation")
    out = rel.rows[0]
    _assert(out["branch_internal_hiddenness_pressure"] > 0.0, "uncertainty carry should be internal hiddenness pressure")
    _assert(out["branch_internal_resolver_support"] > 0.0, "reduce effect should be internal resolver support")
    field = apply_continuation_field(rel.rows, CONTROLS, relations=rel.relations)[0]
    cert = apply_collapse_certificates([field], relations=rel.relations, controls=CONTROLS)[0]
    _assert("branch_internal_resolution_support" in cert["collapse_certificate_reason_flags"], "internal reducer should be preserved in certificate reasons")


def test_weak_decision_slot_competition_remains_telemetry_only() -> None:
    slot = {
        "effect_id": "slot",
        "kind": "legal_constraint",
        "operation": "decision_slot",
        "burden_type": "",
        "scope": "decision_slot",
        "relation_scope": "one_slot",
        "magnitude": 1.0,
        "public_basis": "legal_constraint",
        "leakage_status": "public",
    }
    rel = derive_relation_surface([_row("A", [slot]), _row("B", [dict(slot)])], CONTROLS)
    _assert(rel.telemetry["relations_by_type"].get("decision_slot_competition", 0) > 0, "weak competition should be logged")
    _assert(rel.telemetry["relations_by_type"].get("rivalry", 0) == 0, "weak competition must not become rivalry")
    _assert(rel.telemetry.get("branch_internal_operation_rows", 0) == 0, "weak competition alone must not count as branch-internal burden-carrier coverage")
    certs = _certified([_row("A", [slot]), _row("B", [dict(slot)])])
    for cert in certs:
        _assert("unresolved_non_equivalent_rival" not in cert["collapse_blockers"], f"weak competition should not block collapse: {cert}")


def main() -> None:
    test_branch_internal_hiddenness_survives_without_cross_branch_relation()
    test_buffering_and_masking_use_different_carriers()
    test_branch_internal_reducer_can_affect_field_without_relation()
    test_weak_decision_slot_competition_remains_telemetry_only()
    print("kernel_structure_carrier_alignment_invariants passed")


if __name__ == "__main__":
    main()
