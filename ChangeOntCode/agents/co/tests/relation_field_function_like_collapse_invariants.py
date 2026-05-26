"""Invariants for relation-field concentration / function-like collapse telemetry.

Run with: python -m agents.co.tests.relation_field_function_like_collapse_invariants
"""
from __future__ import annotations

import pathlib

from agents.co.runtime.surfaces.dynamic_shape_field import DynamicShapeField
from agents.co.runtime.surfaces.relation_surface import derive_relation_surface


CONTROLS = {
    "local_authority": 0.50,
    "path_sensitivity": 0.50,
    "contradiction_sensitivity": 0.50,
    "collapse_admissibility": 0.50,
    "dynamic_shape_coarsening": 0.20,
    "dynamic_shape_urgency": 0.15,
}


def _effect(operation: str, burden_type: str = "target", *, magnitude: float = 1.0) -> dict:
    return {
        "effect_id": f"{operation}_{burden_type}_{magnitude}",
        "kind": "burden",
        "operation": operation,
        "burden_type": burden_type,
        "scope": "public_domain",
        "magnitude": magnitude,
        "public_basis": "visible_observation",
        "leakage_status": "public",
    }


def _row(name: str, effects: list[dict]) -> dict:
    return {
        "action": name,
        "candidate_id": name,
        "support_mass": 0.50,
        "local_support": 0.50,
        "decision_state": 0.50,
        "continuation_viability": 0.50,
        "stability_under_change": 0.50,
        "public_effects": effects,
    }


def test_highly_concentrated_public_relation_is_function_like_under_gauge() -> None:
    dominant = _row("native_expr_dominant", [_effect("carry", magnitude=0.999)])
    tiny = _row("native_expr_tiny", [_effect("carry", magnitude=0.001)])
    result = derive_relation_surface([dominant, tiny], CONTROLS)
    by_action = {r["action"]: r for r in result.rows}
    assert by_action["native_expr_dominant"]["relation_field_concentration"] > 0.95
    assert by_action["native_expr_dominant"]["relation_field_function_like"] is True
    assert by_action["native_expr_tiny"]["relation_field_function_like"] is False
    assert result.telemetry["relation_field_function_like_count"] >= 1


def test_flat_relation_is_not_function_like_and_preserves_ambiguity() -> None:
    a = _row("native_expr_a", [_effect("carry", magnitude=0.50)])
    b = _row("native_expr_b", [_effect("carry", magnitude=0.50)])
    result = derive_relation_surface([a, b], CONTROLS)
    for row in result.rows:
        assert row["relation_field_concentration"] <= 0.51
        assert row["relation_field_function_like"] is False
        assert row["relation_field_ambiguity"] >= 0.49
    assert result.telemetry["relation_field_ambiguous_count"] >= 2


def test_shape_coarsening_lowers_function_like_threshold_without_action_policy() -> None:
    row_a = _row("native_expr_a", [_effect("carry", magnitude=0.78)])
    row_b = _row("native_expr_b", [_effect("carry", magnitude=0.22)])
    fine = derive_relation_surface([row_a, row_b], {**CONTROLS, "dynamic_shape_coarsening": 0.0, "dynamic_shape_urgency": 0.8})
    coarse = derive_relation_surface([row_a, row_b], {**CONTROLS, "dynamic_shape_coarsening": 0.9, "dynamic_shape_urgency": 0.0, "collapse_admissibility": 0.8})
    fine_dom = max(fine.rows, key=lambda r: r["relation_field_concentration"])
    coarse_dom = max(coarse.rows, key=lambda r: r["relation_field_concentration"])
    assert fine_dom["relation_field_function_like_threshold"] > coarse_dom["relation_field_function_like_threshold"]
    assert coarse_dom["relation_field_function_like"] is True


def test_dynamic_shape_consumes_relation_ambiguity_as_shape_evidence() -> None:
    a = _row("native_expr_a", [_effect("carry", magnitude=0.50)])
    b = _row("native_expr_b", [_effect("carry", magnitude=0.50)])
    result = derive_relation_surface([a, b], CONTROLS)
    field = DynamicShapeField(alpha=0.75)
    before = field.state_dict()
    rec = field.update(rows=result.rows, relations=result.relations)
    after = field.state_dict()
    assert rec["applied"] is True
    assert rec["public_evidence"]["relation_field_ambiguity_observed"] > 0.0
    assert after["burden_persistence"] >= before["burden_persistence"]
    assert after["gauge_confidence"] <= before["gauge_confidence"] + 0.15


def test_source_has_no_family_or_action_policy_literals() -> None:
    src = pathlib.Path(__file__).parents[1] / "runtime" / "surfaces" / "relation_field_concentration.py"
    text = src.read_text()
    forbidden = ["maintenance", "bandit", "maze", "renewal", "RUN", "REPAIR", "INSPECT", "WAIT", "best_action", "dp_value", "q_value", "shortest_path"]
    for token in forbidden:
        assert token not in text, token


if __name__ == "__main__":
    test_highly_concentrated_public_relation_is_function_like_under_gauge()
    test_flat_relation_is_not_function_like_and_preserves_ambiguity()
    test_shape_coarsening_lowers_function_like_threshold_without_action_policy()
    test_dynamic_shape_consumes_relation_ambiguity_as_shape_evidence()
    test_source_has_no_family_or_action_policy_literals()
    print("relation_field_function_like_collapse_invariants passed")
