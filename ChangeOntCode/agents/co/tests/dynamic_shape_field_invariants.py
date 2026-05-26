"""Invariants for first-pass DynamicShapeField implementation.

Run with: python -m agents.co.tests.dynamic_shape_field_invariants
"""
from __future__ import annotations

from typing import Any, Dict, List

from agents.co.runtime.surfaces.dynamic_shape_field import DynamicShapeField
from agents.co.runtime.surfaces.continuation_field import BranchRelation
from agents.co.runtime.surfaces.candidate_surface import CandidateEvidenceSurface
from agents.co.tests.relation_path_trace_diagnostics import TraceBus, TraceHeader, TraceHeaderState


def _row(**kw: Any) -> Dict[str, Any]:
    base: Dict[str, Any] = {
        "action": kw.pop("action", "branch"),
        "candidate_id": kw.pop("candidate_id", "branch"),
        "branch_id": kw.pop("branch_id", "branch"),
        "field_debt": 0.0,
        "field_grey_pressure": 0.0,
        "field_recursion_budget": 0.0,
        "field_relief_support": 0.0,
        "field_relation_count": 0,
        "uncertainty": 0.0,
        "burden_trend": 0.0,
        "branch_internal_operation_counts": {},
        "branch_internal_unresolved_pressure": 0.0,
        "branch_internal_resolver_support": 0.0,
        "branch_internal_exposure_support": 0.0,
        "branch_internal_hiddenness_pressure": 0.0,
        "branch_internal_transform_pressure": 0.0,
    }
    base.update(kw)
    return base


def _update(field: DynamicShapeField, rows: List[Dict[str, Any]], *, relations=None, observation=None, feedback=None) -> Dict[str, Any]:
    return field.update(rows=rows, relations=list(relations or []), observation=dict(observation or {}), feedback=dict(feedback or {}))


def test_repeated_carrier_burden_increases_persistence_and_shortens_projection() -> None:
    f = DynamicShapeField(alpha=0.60)
    rows = [
        _row(action="carrier", branch_id="c", field_debt=0.70, burden_trend=0.65, branch_internal_operation_counts={"carry": 1}, branch_internal_unresolved_pressure=0.70),
        _row(action="resolver", branch_id="r", field_relief_support=0.40, branch_internal_operation_counts={"reduce": 1}, branch_internal_resolver_support=0.50),
    ]
    rels = [BranchRelation(source="r", target="c", relation_type="relief", weight=0.75)]
    before = f.state_dict()
    rec = _update(f, rows, relations=rels)
    after = f.state_dict()
    assert rec["applied"] is True
    assert after["burden_persistence"] > before["burden_persistence"]
    assert after["projection_horizon"] < before["projection_horizon"]


def test_successful_exposure_reduces_hiddenness_and_can_raise_confidence() -> None:
    f = DynamicShapeField(alpha=0.65, initial_state={"hiddenness_pressure": 0.80, "gauge_confidence": 0.35})
    rows = [_row(action="exposer", branch_id="e", branch_internal_operation_counts={"reveal": 1}, branch_internal_exposure_support=0.90, branch_internal_resolver_support=0.90, branch_internal_hiddenness_pressure=0.35, uncertainty=0.30)]
    before = f.state_dict()
    _update(f, rows, observation={"public_exposure_success": True, "cue_reliability_improved": True})
    after = f.state_dict()
    assert after["hiddenness_pressure"] < before["hiddenness_pressure"]
    assert after["gauge_confidence"] >= before["gauge_confidence"] - 1e-9


def test_failed_exposure_does_not_invent_knowledge() -> None:
    f = DynamicShapeField(alpha=0.70, initial_state={"hiddenness_pressure": 0.35})
    rows = [_row(action="probe", branch_id="p", branch_internal_operation_counts={"reveal": 1}, branch_internal_exposure_support=0.10, uncertainty=0.70)]
    before = f.state_dict()
    rec = _update(f, rows, observation={"public_exposure_failed": True})
    after = f.state_dict()
    assert rec["applied"] is True
    assert after["hiddenness_pressure"] >= before["hiddenness_pressure"]
    assert "hidden_state" not in str(rec).lower()


def test_topology_discovery_updates_known_admissibility_not_topology() -> None:
    f = DynamicShapeField(alpha=0.60)
    rows = [_row(action="move", branch_id="m", field_debt=0.20)]
    rec = _update(f, rows, observation={"blocked_transition_discovered": True})
    after = f.state_dict()
    assert rec["applied"] is True
    assert after["admissibility_pressure"] > 0.0
    assert "topology" not in rec["deltas"]


def test_stable_low_coupling_permits_coarsening() -> None:
    f = DynamicShapeField(alpha=0.65, initial_state={"coarseness_radius": 0.35, "gauge_confidence": 0.70})
    rows = [_row(action="stable", branch_id="s", field_debt=0.02, field_grey_pressure=0.01, uncertainty=0.02)]
    before = f.state_dict()
    _update(f, rows)
    after = f.state_dict()
    assert after["coarseness_radius"] > before["coarseness_radius"]


def test_high_coupling_consumes_projection_and_narrows_coarseness() -> None:
    f = DynamicShapeField(alpha=0.70, initial_state={"coarseness_radius": 0.75, "projection_horizon": 0.75})
    rows = [
        _row(action="a", branch_id="a", field_debt=0.72, field_grey_pressure=0.60, field_recursion_budget=0.55, field_relation_count=2, uncertainty=0.55),
        _row(action="b", branch_id="b", field_debt=0.65, field_grey_pressure=0.58, field_recursion_budget=0.50, field_relation_count=2, uncertainty=0.60),
    ]
    rels = [BranchRelation(source="a", target="b", relation_type="rivalry", weight=0.8), BranchRelation(source="b", target="a", relation_type="rivalry", weight=0.8)]
    before = f.state_dict()
    _update(f, rows, relations=rels)
    after = f.state_dict()
    assert after["projection_horizon"] < before["projection_horizon"]
    assert after["coarseness_radius"] < before["coarseness_radius"]


def test_resolver_relation_requires_explicit_public_relation() -> None:
    f = DynamicShapeField(alpha=0.80)
    rows = [_row(action="repair_named_only", branch_id="n", branch_internal_operation_counts={}, branch_internal_resolver_support=0.0)]
    rec = _update(f, rows)
    assert rec["applied"] is False
    assert rec["reason"] == "no_public_shape_signal"


def test_transform_transfer_not_resolution_by_itself() -> None:
    f = DynamicShapeField(alpha=0.70)
    rows = [_row(action="transformer", branch_id="t", branch_internal_operation_counts={"transform": 1}, branch_internal_transform_pressure=0.80, field_debt=0.40)]
    rec = _update(f, rows)
    assert rec["applied"] is True
    assert rec["public_evidence"]["transform_transfer_ops_count"] == 1
    assert rec["public_evidence"]["resolver_ops_count"] == 0
    assert f.state_dict()["burden_persistence"] > 0.0


def test_revision_success_lowers_revision_pressure_via_public_feedback() -> None:
    f = DynamicShapeField(alpha=0.70, initial_state={"admissibility_pressure": 0.60})
    rows = [_row(action="revise", branch_id="r", field_debt=0.10)]
    before = f.state_dict()
    _update(f, rows, feedback={"admissibility_pressure": 0.0, "public_revision_success": True})
    after = f.state_dict()
    assert after["admissibility_pressure"] < before["admissibility_pressure"]


def test_failed_revision_raises_narrowing_pressure() -> None:
    f = DynamicShapeField(alpha=0.70)
    rows = [_row(action="revise", branch_id="r", field_debt=0.15)]
    _update(f, rows, feedback={"admissibility_pressure": 0.90, "public_revision_blocked": True})
    assert f.state_dict()["admissibility_pressure"] > 0.40


def test_reward_alone_does_not_update_shape() -> None:
    f = DynamicShapeField(alpha=0.80)
    rows = [_row(action="x", branch_id="x")]
    before = f.state_dict()
    rec = _update(f, rows, feedback={"reward": 1.0})
    assert rec["applied"] is False
    assert rec["reason"] == "reward_only_no_shape_update"
    assert f.state_dict() == before


def test_shape_update_ablation_visible_in_candidate_surface() -> None:
    obs = {
        "family": "dynamic_shape_ablation_probe",
        "t": 1,
        "action_space": ["C", "R"],
        "candidates": [
            {"candidate_id": "C", "legal": True, "visible_delta": 0.70, "line_support": 0.70, "coverage_adequacy": 0.65, "tested_hint": 0.55, "uncertainty_hint": 0.25, "reversibility_hint": 0.35, "public_effects": [{"operation": "carry", "kind": "burden", "burden_type": "degradation", "magnitude": 0.75, "relation_scope": "degradation", "public_basis": "visible_observation", "leakage_status": "public"}]},
            {"candidate_id": "R", "legal": True, "visible_delta": 0.50, "line_support": 0.50, "coverage_adequacy": 0.55, "tested_hint": 0.45, "uncertainty_hint": 0.35, "reversibility_hint": 0.75, "public_effects": [{"operation": "reduce", "kind": "burden", "burden_type": "degradation", "magnitude": 0.55, "relation_scope": "degradation", "public_basis": "visible_observation", "leakage_status": "public"}]},
        ],
    }
    header = TraceHeader(TraceHeaderState())
    prims_on = {"signal_bus": TraceBus()}
    prims_off = {"signal_bus": TraceBus()}
    CandidateEvidenceSurface(dynamic_shape_enabled=True).step(obs, prims_on, header, None)
    CandidateEvidenceSurface(dynamic_shape_enabled=False).step(obs, prims_off, header, None)
    assert prims_on.get("__dynamic_shape_enabled__") is True
    assert "__dynamic_shape_update__" in prims_on
    assert "__dynamic_shape_update__" not in prims_off
    assert prims_on["__dynamic_shape_update__"]["applied"] is True


def test_source_has_no_family_or_action_policy_literals() -> None:
    import pathlib
    src = pathlib.Path(__file__).parents[1] / "runtime" / "surfaces" / "dynamic_shape_field.py"
    text = src.read_text()
    forbidden = ["maintenance", "bandit", "maze", "renewal", "RUN", "REPAIR", "REPLACE", "INSPECT", "WAIT", "best_action", "dp_value", "q_value", "shortest_path"]
    for token in forbidden:
        assert token not in text, token


if __name__ == "__main__":
    test_repeated_carrier_burden_increases_persistence_and_shortens_projection()
    test_successful_exposure_reduces_hiddenness_and_can_raise_confidence()
    test_failed_exposure_does_not_invent_knowledge()
    test_topology_discovery_updates_known_admissibility_not_topology()
    test_stable_low_coupling_permits_coarsening()
    test_high_coupling_consumes_projection_and_narrows_coarseness()
    test_resolver_relation_requires_explicit_public_relation()
    test_transform_transfer_not_resolution_by_itself()
    test_revision_success_lowers_revision_pressure_via_public_feedback()
    test_failed_revision_raises_narrowing_pressure()
    test_reward_alone_does_not_update_shape()
    test_shape_update_ablation_visible_in_candidate_surface()
    test_source_has_no_family_or_action_policy_literals()
