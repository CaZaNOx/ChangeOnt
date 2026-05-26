"""Invariants for domain-relative coarseness field.

Run with: python -m agents.co.tests.domain_relative_coarseness_field_invariants
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


def effect(operation: str, burden_type: str, magnitude: float) -> dict:
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


def row(name: str, effects: list[dict], *, uncertainty: float = 0.0, debt: float = 0.0) -> dict:
    return {
        "action": name,
        "candidate_id": name,
        "support_mass": 0.50,
        "local_support": 0.50,
        "decision_state": 0.50,
        "continuation_viability": 0.50,
        "stability_under_change": 0.50,
        "uncertainty": uncertainty,
        "field_debt": debt,
        "public_effects": effects,
    }


def test_domain_relative_coarseness_tracks_public_domains_without_global_collapse() -> None:
    rows = [
        row("hidden_carrier_a", [effect("carry", "hiddenness", 0.50)], uncertainty=0.80, debt=0.30),
        row("hidden_carrier_b", [effect("carry", "hiddenness", 0.50)], uncertainty=0.75, debt=0.35),
        row("degradation_resolver", [effect("relieve", "degradation", 0.92)], uncertainty=0.05, debt=0.05),
        row("degradation_minor", [effect("carry", "degradation", 0.08)], uncertainty=0.05, debt=0.05),
    ]
    rel = derive_relation_surface(rows, CONTROLS)
    field = DynamicShapeField(alpha=0.80)
    update = field.update(rows=rel.rows, relations=rel.relations)
    state = field.state_dict()
    domains = state["coarseness_by_domain"]
    assert update["applied"] is True
    assert "burden:hiddenness" in domains
    assert "burden:degradation" in domains
    # The hiddenness domain is ambiguous/high-burden, so it should retain finer
    # resolution than the concentrated degradation domain.
    assert domains["burden:hiddenness"] < domains["burden:degradation"]
    assert 0.0 <= state["coarseness_radius"] <= 1.0


def test_rows_receive_domain_coarseness_without_native_policy_labels() -> None:
    rows = [
        row("native_expr_a", [effect("carry", "hiddenness", 0.50)], uncertainty=0.80),
        row("native_expr_b", [effect("carry", "hiddenness", 0.50)], uncertainty=0.80),
    ]
    rel = derive_relation_surface(rows, CONTROLS)
    field = DynamicShapeField(alpha=0.75)
    field.update(rows=rel.rows, relations=rel.relations)
    assert field.domain_coarseness_for("burden:hiddenness") <= field.state.coarseness_radius + 0.15
    assert field.domain_coarseness_for("unknown") == field.state.coarseness_radius


def test_source_has_no_family_action_or_solver_literals_for_domain_coarseness() -> None:
    src = pathlib.Path(__file__).parents[1] / "runtime" / "surfaces" / "dynamic_shape_field.py"
    text = src.read_text()
    forbidden = ["best_action", "dp_value", "q_value", "shortest_path"]
    for token in forbidden:
        assert token not in text, token


if __name__ == "__main__":
    test_domain_relative_coarseness_tracks_public_domains_without_global_collapse()
    test_rows_receive_domain_coarseness_without_native_policy_labels()
    test_source_has_no_family_action_or_solver_literals_for_domain_coarseness()
    print("domain_relative_coarseness_field_invariants passed")
