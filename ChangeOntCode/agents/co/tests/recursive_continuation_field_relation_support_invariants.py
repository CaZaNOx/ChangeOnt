"""Invariant/diagnostic module for recursive continuation field relation support invariants.

Run with: python -m agents.co.tests.recursive_continuation_field_relation_support_invariants
"""
from __future__ import annotations

from agents.co.runtime.surfaces.continuation_field import (
    BranchRelation,
    ContinuationField,
    apply_continuation_field,
)


CAUTIOUS_CONTROLS = {
    "local_authority": 0.20,
    "nonlocal_authority": 0.90,
    "path_sensitivity": 0.90,
    "revision_permissibility": 0.85,
    "rival_breadth": 0.85,
    "collapse_admissibility": 0.25,
    "low_evidence_sampling": 0.80,
    "contradiction_sensitivity": 0.80,
}


def _row(
    action: str,
    *,
    support: float,
    viability: float,
    debt: float,
    burden_relief: float = 0.0,
    preventive_support: float = 0.0,
    uncertainty: float = 0.10,
) -> dict:
    return {
        "action": action,
        "support_mass": support,
        "local_support": support,
        "decision_state": support,
        "continuation_viability": viability,
        "stability_under_change": viability,
        "burden_pressure": debt,
        "burden_accumulation": debt,
        "burden_trend": debt,
        "continuation_instability": debt,
        "fracture_state": debt,
        "uncertainty": uncertainty,
        "burden_relief": burden_relief,
        "preventive_support": preventive_support,
        "commitment_stability": viability,
    }


def test_low_debt_stability_is_not_relief_without_explicit_relief_signal() -> None:
    rows = [
        _row("debtful", support=0.76, viability=0.70, debt=0.82),
        _row("stable", support=0.83, viability=0.88, debt=0.04),
    ]
    out = {r["action"]: r for r in apply_continuation_field(rows, CAUTIOUS_CONTROLS)}
    assert out["stable"]["field_relief_support"] <= 1e-9


def test_grey_pressure_requires_explicit_rivalry_similarity_or_equivalence() -> None:
    rows = [
        _row("left", support=0.62, viability=0.58, debt=0.36, uncertainty=0.46),
        _row("right", support=0.61, viability=0.57, debt=0.35, uncertainty=0.47),
    ]
    out = {r["action"]: r for r in apply_continuation_field(rows, CAUTIOUS_CONTROLS)}
    assert out["left"]["field_grey_pressure"] <= 1e-9
    assert out["right"]["field_grey_pressure"] <= 1e-9


def test_unrelated_high_debt_branch_does_not_grant_relief_to_all_stable_low_debt_branches() -> None:
    rows = [
        _row("unresolved", support=0.70, viability=0.65, debt=0.90),
        _row("stable_a", support=0.82, viability=0.86, debt=0.03),
        _row("stable_b", support=0.78, viability=0.84, debt=0.05),
    ]
    out = {r["action"]: r for r in apply_continuation_field(rows, CAUTIOUS_CONTROLS)}
    assert out["stable_a"]["field_relief_support"] <= 1e-9
    assert out["stable_b"]["field_relief_support"] <= 1e-9
    assert out["stable_a"]["quotient_share_count"] == 1
    assert out["stable_b"]["quotient_share_count"] == 1


def test_explicit_relief_relation_still_grants_relief_support() -> None:
    rows = [
        _row("debtful", support=0.76, viability=0.70, debt=0.82),
        _row("reliever", support=0.50, viability=0.54, debt=0.08, burden_relief=0.90),
    ]
    relations = [BranchRelation(source="reliever", target="debtful", relation_type="relief", weight=1.0)]
    out = {r["action"]: r for r in apply_continuation_field(rows, CAUTIOUS_CONTROLS, relations=relations)}
    assert out["reliever"]["field_relief_support"] > 0.10
    assert out["debtful"]["field_grey_pressure"] > 0.0


def test_explicit_competition_relation_still_preserves_grey() -> None:
    rows = [
        _row("left", support=0.62, viability=0.58, debt=0.36, uncertainty=0.46),
        _row("right", support=0.61, viability=0.57, debt=0.35, uncertainty=0.47),
    ]
    relations = [BranchRelation(source="left", target="right", relation_type="competition", weight=1.0)]
    out = {r["action"]: r for r in apply_continuation_field(rows, CAUTIOUS_CONTROLS, relations=relations)}
    assert out["left"]["field_grey_pressure"] > 0.0
    assert out["right"]["field_grey_pressure"] > 0.0


def test_row_embedded_relation_hints_are_honored_without_action_or_family_literals() -> None:
    rows = [
        _row("debtful", support=0.76, viability=0.70, debt=0.82),
        dict(
            _row("reliever", support=0.50, viability=0.54, debt=0.08, burden_relief=0.90),
            branch_relations=[{"target": "debtful", "relation_type": "relief", "weight": 1.0}],
        ),
    ]
    out = {r["action"]: r for r in apply_continuation_field(rows, CAUTIOUS_CONTROLS)}
    assert out["reliever"]["field_relation_count"] == 1
    assert out["debtful"]["field_relation_count"] == 1
    assert out["reliever"]["field_relief_support"] > 0.10
    assert out["debtful"]["field_grey_pressure"] > 0.0


if __name__ == "__main__":
    test_low_debt_stability_is_not_relief_without_explicit_relief_signal()
    test_grey_pressure_requires_explicit_rivalry_similarity_or_equivalence()
    test_unrelated_high_debt_branch_does_not_grant_relief_to_all_stable_low_debt_branches()
    test_explicit_relief_relation_still_grants_relief_support()
    test_explicit_competition_relation_still_preserves_grey()
    test_row_embedded_relation_hints_are_honored_without_action_or_family_literals()
