"""Invariants for first-pass quotient/equivalence derivation.

Run with: python -m agents.co.tests.quotient_equivalence_first_pass_invariants
"""
from __future__ import annotations

from pathlib import Path

from agents.co.runtime.surfaces.continuation_field import apply_continuation_field
from agents.co.runtime.surfaces.quotient_equivalence import derive_quotient_equivalence
from agents.co.runtime.surfaces.relation_surface import derive_relation_surface

CONTROLS = {
    "local_authority": 0.40,
    "nonlocal_authority": 0.70,
    "path_sensitivity": 0.70,
    "revision_permissibility": 0.70,
    "rival_breadth": 0.65,
    "collapse_admissibility": 0.45,
    "low_evidence_sampling": 0.60,
    "contradiction_sensitivity": 0.70,
    "coarseness_radius": 0.25,
}


def _effect(operation: str, burden_type: str = "generic_load", *, magnitude: float = 0.55, scope: str = "local_region", kind: str = "burden", leakage: str = "public", public_basis: str = "declared_transition_rule", coupling: str = "continuation_coupling", threshold_status: str = "", basin_status: str = "") -> dict:
    return {
        "operation": operation,
        "kind": kind,
        "burden_type": burden_type,
        "scope": scope,
        "magnitude": magnitude,
        "public_basis": public_basis,
        "leakage_status": leakage,
        "coupling": coupling,
        "threshold_status": threshold_status,
        "basin_status": basin_status,
    }


def _row(expr: str, *, public_effects: list[dict], support: float = 0.60, debt: float = 0.30) -> dict:
    return {
        "action": expr,
        "candidate_id": expr,
        "support_mass": support,
        "decision_state": support,
        "local_support": support,
        "continuation_viability": support,
        "burden_pressure": debt,
        "burden_accumulation": debt,
        "burden_trend": debt,
        "fracture_state": debt,
        "uncertainty": 0.20,
        "commitment_stability": 0.55,
        "public_effects": list(public_effects),
    }


def _types(result) -> list[str]:
    return [r.relation_type for r in result.relations]


def _field_rows_by_expr(rows: list[dict]) -> dict[str, dict]:
    return {str(r["action"]): r for r in rows}


def test_different_expressions_same_public_residual_profile_may_quotient() -> None:
    a = _row("expr_alpha", public_effects=[_effect("reduce", "generic_load", magnitude=0.55)])
    b = _row("expr_beta", public_effects=[_effect("relieve", "generic_load", magnitude=0.57)])
    result = derive_relation_surface([a, b], CONTROLS)
    assert "equivalence" in _types(result), result.telemetry
    field_rows = _field_rows_by_expr(apply_continuation_field(result.rows, CONTROLS, relations=result.relations))
    assert field_rows["expr_alpha"]["quotient_share_count"] == 2
    assert field_rows["expr_beta"]["quotient_share_count"] == 2
    assert field_rows["expr_alpha"].get("relation_surface_quotient_profile")


def test_same_expression_different_burden_regime_does_not_quotient() -> None:
    low = _row("same_interface_expr", public_effects=[_effect("carry", "generic_load", magnitude=0.20)], support=0.50, debt=0.20)
    high = _row("same_interface_expr", public_effects=[_effect("carry", "generic_load", magnitude=0.86)], support=0.50, debt=0.86)
    result = derive_relation_surface([low, high], CONTROLS)
    assert "equivalence" not in _types(result), result.telemetry


def test_weak_decision_slot_competition_is_not_quotient_basis() -> None:
    slot = {
        "operation": "decision_slot",
        "kind": "legal_constraint",
        "burden_type": "",
        "scope": "decision_slot",
        "relation_scope": "one_slot",
        "magnitude": 1.0,
        "public_basis": "legal_constraint",
        "leakage_status": "public",
    }
    a = _row("expr_alpha", public_effects=[slot])
    b = _row("expr_beta", public_effects=[dict(slot)])
    result = derive_relation_surface([a, b], CONTROLS)
    rels = result.telemetry.get("relations_by_type", {})
    assert rels.get("decision_slot_competition", 0) > 0
    assert rels.get("equivalence", 0) == 0
    assert result.telemetry.get("quotient_profiles_rejected", {}).get("procedural_only", 0) == 2


def test_same_scalar_score_different_hiddenness_profile_does_not_quotient() -> None:
    hidden = _row("expr_alpha", support=0.70, debt=0.40, public_effects=[_effect("carry", "hiddenness", magnitude=0.55, kind="uncertainty")])
    load = _row("expr_beta", support=0.70, debt=0.40, public_effects=[_effect("carry", "generic_load", magnitude=0.55, kind="burden")])
    result = derive_relation_surface([hidden, load], CONTROLS)
    assert "equivalence" not in _types(result), result.telemetry


def test_hidden_or_solver_like_effects_do_not_derive_quotient() -> None:
    direct = derive_quotient_equivalence(
        {
            "a": [_effect("reduce", "generic_load", leakage="hidden_policy")],
            "b": [_effect("relieve", "generic_load")],
        },
        controls=CONTROLS,
    )
    assert not direct.relations
    assert direct.telemetry["quotient_profiles_rejected"].get("nonpublic_or_solver_like_effect", 0) == 1


def test_exclusion_or_rivalry_facts_do_not_quotient_by_themselves() -> None:
    exclusion = {
        "operation": "exclude",
        "kind": "legal_constraint",
        "burden_type": "",
        "scope": "candidate",
        "relation_scope": "shared_resource",
        "magnitude": 1.0,
        "public_basis": "legal_constraint",
        "leakage_status": "public",
        "relation_strength": "strong",
    }
    a = _row("expr_alpha", public_effects=[exclusion])
    b = _row("expr_beta", public_effects=[dict(exclusion)])
    result = derive_relation_surface([a, b], CONTROLS)
    rels = result.telemetry.get("relations_by_type", {})
    assert rels.get("rivalry", 0) > 0
    assert rels.get("equivalence", 0) == 0


def test_quotient_helper_contains_no_problem_family_or_native_action_literals() -> None:
    source = Path(__file__).resolve().parents[1] / "runtime" / "surfaces" / "quotient_equivalence.py"
    import re
    text = source.read_text(encoding="utf-8").lower()
    forbidden = [
        "maintenance", "bandit", "renewal", "maze", "latent", "robot", "simulator",
        "repair", "replace", "inspect", "run", "wait", "left", "right", "up", "down",
        "reward", "dp_value", "shortest_path", "best_action",
    ]
    leaked = [token for token in forbidden if re.search(r"(?<![a-z0-9_])" + re.escape(token) + r"(?![a-z0-9_])", text)]
    assert not leaked, leaked


def main() -> None:
    test_different_expressions_same_public_residual_profile_may_quotient()
    test_same_expression_different_burden_regime_does_not_quotient()
    test_weak_decision_slot_competition_is_not_quotient_basis()
    test_same_scalar_score_different_hiddenness_profile_does_not_quotient()
    test_hidden_or_solver_like_effects_do_not_derive_quotient()
    test_exclusion_or_rivalry_facts_do_not_quotient_by_themselves()
    test_quotient_helper_contains_no_problem_family_or_native_action_literals()
    print("quotient_equivalence_first_pass_invariants passed")


if __name__ == "__main__":
    main()
