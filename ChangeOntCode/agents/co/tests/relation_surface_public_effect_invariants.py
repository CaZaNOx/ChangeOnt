"""Invariants for deriving RelationSurface structure from public_effect facts."""
from __future__ import annotations

from agents.co.runtime.surfaces.continuation_field import apply_continuation_field, branch_key_from_row
from agents.co.runtime.surfaces.relation_surface import derive_relation_surface


CONTROLS = {
    "local_authority": 0.20,
    "nonlocal_authority": 0.90,
    "path_sensitivity": 0.90,
    "revision_permissibility": 0.85,
    "rival_breadth": 0.85,
    "collapse_admissibility": 0.25,
    "low_evidence_sampling": 0.80,
    "contradiction_sensitivity": 0.80,
}


def _effect(operation: str, burden_type: str = "degradation", *, magnitude: float = 1.0, basis: str = "declared_transition_rule", leakage: str = "public", kind: str = "burden", scope: str = "machine") -> dict:
    return {
        "effect_id": f"{operation}_{burden_type}",
        "kind": kind,
        "operation": operation,
        "burden_type": burden_type,
        "scope": scope,
        "magnitude": magnitude,
        "public_basis": basis,
        "leakage_status": leakage,
    }


def _row(action: str, *, debt: float = 0.30, public_effects: list[dict] | None = None) -> dict:
    return {
        "action": action,
        "candidate_id": action,
        "support_mass": 0.62,
        "local_support": 0.62,
        "decision_state": 0.62,
        "continuation_viability": 0.60,
        "stability_under_change": 0.60,
        "burden_pressure": debt,
        "burden_accumulation": debt,
        "burden_trend": debt,
        "continuation_instability": debt,
        "fracture_state": debt,
        "uncertainty": 0.20,
        "burden_relief": 0.0,
        "preventive_support": 0.0,
        "commitment_stability": 0.55,
        "public_effects": list(public_effects or []),
    }


def _by_action(rows: list[dict]) -> dict[str, dict]:
    return {str(r["action"]): r for r in rows}


def test_relation_surface_derives_relief_from_public_effects_without_action_literals() -> None:
    carrying = _row("native_expr_a", debt=0.78, public_effects=[_effect("carry", "degradation", magnitude=0.90)])
    relieving = _row("native_expr_b", debt=0.12, public_effects=[_effect("reduce", "degradation", magnitude=0.95)])

    result = derive_relation_surface([carrying, relieving], CONTROLS)
    types = [r.relation_type for r in result.relations]
    assert "relief" in types
    assert result.telemetry["relations_by_type"]["relief"] >= 1
    assert result.telemetry["rows_with_public_effects"] == 2
    assert result.telemetry["identity_source_counts"]["public_effects"] == 2

    field_rows = _by_action(apply_continuation_field(result.rows, CONTROLS, relations=result.relations))
    assert field_rows["native_expr_b"]["field_relation_count"] > 0
    assert field_rows["native_expr_b"]["field_relief_support"] > 0.10


def test_relation_surface_rejects_hidden_policy_effects() -> None:
    carrying = _row("native_expr_a", debt=0.78, public_effects=[_effect("carry", "degradation")])
    solver_hint = _row(
        "native_expr_b",
        debt=0.12,
        public_effects=[_effect("reduce", "degradation", leakage="forbidden", basis="declared_transition_rule")],
    )
    result = derive_relation_surface([carrying, solver_hint], CONTROLS)
    assert all(r.source != branch_key_from_row(result.rows[1]) for r in result.relations)
    assert result.telemetry.get("rejected_forbidden_leakage_status", 0) == 1
    assert result.telemetry["relations_total"] == 0


def test_relation_surface_requires_public_basis() -> None:
    carrying = _row("native_expr_a", debt=0.78, public_effects=[_effect("carry", "degradation")])
    no_basis = _row("native_expr_b", debt=0.12, public_effects=[_effect("reduce", "degradation", basis="")])
    result = derive_relation_surface([carrying, no_basis], CONTROLS)
    assert result.telemetry.get("rejected_missing_or_nonpublic_basis", 0) == 1
    assert result.telemetry["relations_total"] == 0


def test_relation_surface_derives_cancellation_distinct_from_relief() -> None:
    carrying = _row("native_expr_a", debt=0.82, public_effects=[_effect("carry", "degradation", magnitude=0.90)])
    relieving = _row("native_expr_b", debt=0.20, public_effects=[_effect("reduce", "degradation", magnitude=0.90)])
    canceling = _row("native_expr_c", debt=0.25, public_effects=[_effect("reset", "degradation", magnitude=0.90)])
    result = derive_relation_surface([carrying, relieving, canceling], CONTROLS)
    types = [r.relation_type for r in result.relations]
    assert "relief" in types
    assert "cancellation" in types

    field_rows = _by_action(apply_continuation_field(result.rows, CONTROLS, relations=result.relations))
    assert field_rows["native_expr_c"]["field_relation_count"] > 0
    assert field_rows["native_expr_a"]["field_debt"] < 0.82


def test_relation_surface_derives_shared_evidence_from_public_exposure() -> None:
    hidden = _row("native_expr_a", debt=0.48, public_effects=[_effect("carry", "hiddenness", magnitude=0.80, kind="uncertainty")])
    exposing = _row("native_expr_b", debt=0.20, public_effects=[_effect("reveal", "hiddenness", magnitude=0.90, kind="evidence")])
    result = derive_relation_surface([hidden, exposing], CONTROLS)
    assert "shared_evidence" in [r.relation_type for r in result.relations]
    field_rows = _by_action(apply_continuation_field(result.rows, CONTROLS, relations=result.relations))
    assert field_rows["native_expr_a"]["field_grey_pressure"] > 0.0


def test_relation_surface_derives_equivalence_from_same_public_pressure_signature() -> None:
    row_a = _row("native_expr_a", debt=0.32, public_effects=[_effect("carry", "path_commitment", magnitude=0.55, scope="frontier")])
    row_b = _row("native_expr_b", debt=0.31, public_effects=[_effect("carry", "path_commitment", magnitude=0.55, scope="frontier")])
    result = derive_relation_surface([row_a, row_b], CONTROLS)
    assert "equivalence" in [r.relation_type for r in result.relations]
    field_rows = _by_action(apply_continuation_field(result.rows, CONTROLS, relations=result.relations))
    assert field_rows["native_expr_a"]["quotient_share_count"] == 2
    assert field_rows["native_expr_b"]["quotient_share_count"] == 2


def test_branch_identity_precedence_prefers_branch_over_action() -> None:
    row = _row("native_action", public_effects=[])
    row["branch_id"] = "continuation_branch"
    result = derive_relation_surface([row], CONTROLS)
    assert branch_key_from_row(result.rows[0]) == "continuation_branch"
    out = apply_continuation_field(result.rows, CONTROLS)
    assert out[0]["branch_id"] == "continuation_branch"


def test_decision_slot_competition_is_not_strong_rivalry() -> None:
    slot = {
        "effect_id": "decision_slot",
        "kind": "legal_constraint",
        "operation": "decision_slot",
        "burden_type": "",
        "scope": "decision_slot",
        "magnitude": 1.0,
        "public_basis": "legal_constraint",
        "leakage_status": "public",
        "relation_scope": "one_slot",
    }
    row_a = _row("native_expr_a", public_effects=[slot])
    row_b = _row("native_expr_b", public_effects=[dict(slot)])
    result = derive_relation_surface([row_a, row_b], CONTROLS)
    rels = result.telemetry.get("relations_by_type", {})
    assert rels.get("decision_slot_competition", 0) > 0
    assert rels.get("rivalry", 0) == 0


def test_pressure_signature_uses_coarse_burden_regime_bands() -> None:
    low_a = _row("RUN", public_effects=[_effect("carry", "degradation", magnitude=0.20)])
    low_b = _row("RUN", public_effects=[_effect("carry", "degradation", magnitude=0.22)])
    high = _row("RUN", public_effects=[_effect("carry", "degradation", magnitude=0.84)])
    res_low = derive_relation_surface([low_a, low_b], CONTROLS)
    res_high = derive_relation_surface([low_a, high], CONTROLS)
    assert res_low.rows[0]["relation_surface_effect_signature"] == res_low.rows[1]["relation_surface_effect_signature"]
    assert res_high.rows[0]["relation_surface_effect_signature"] != res_high.rows[1]["relation_surface_effect_signature"]


if __name__ == "__main__":
    test_relation_surface_derives_relief_from_public_effects_without_action_literals()
    test_relation_surface_rejects_hidden_policy_effects()
    test_relation_surface_requires_public_basis()
    test_relation_surface_derives_cancellation_distinct_from_relief()
    test_relation_surface_derives_shared_evidence_from_public_exposure()
    test_relation_surface_derives_equivalence_from_same_public_pressure_signature()
    test_branch_identity_precedence_prefers_branch_over_action()
    test_decision_slot_competition_is_not_strong_rivalry()
    test_pressure_signature_uses_coarse_burden_regime_bands()
