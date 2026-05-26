"""Invariant/diagnostic module for recursive continuation field invariants.

Run with: python -m agents.co.tests.recursive_continuation_field_invariants
"""
from __future__ import annotations

from agents.co.runtime.surfaces.continuation_field import (
    BranchRelation,
    ContinuationBranch,
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

LOCAL_CONTROLS = {
    "local_authority": 0.90,
    "nonlocal_authority": 0.15,
    "path_sensitivity": 0.15,
    "revision_permissibility": 0.15,
    "rival_breadth": 0.15,
    "collapse_admissibility": 0.90,
    "low_evidence_sampling": 0.10,
    "contradiction_sensitivity": 0.10,
}


def _branch(branch_id: str, *, support: float, viability: float, debt: float, burden: float | None = None, relief: float = 0.0, uncertainty: float = 0.1) -> ContinuationBranch:
    return ContinuationBranch(
        branch_id=branch_id,
        support=support,
        local_support=support,
        viability=viability,
        burden=debt if burden is None else burden,
        debt=debt,
        instability=debt,
        uncertainty=uncertainty,
        relief_capacity=relief,
    )


def test_high_local_support_with_rising_debt_lowers_collapse_readiness() -> None:
    low_debt = [_branch("A", support=0.88, viability=0.82, debt=0.08)]
    high_debt = [_branch("A", support=0.88, viability=0.82, debt=0.78)]
    field = ContinuationField(CAUTIOUS_CONTROLS)
    low = field.update(low_debt)["A"]
    high = field.update(high_debt)["A"]
    assert high.field_debt > low.field_debt
    assert high.field_collapse_readiness < low.field_collapse_readiness
    assert high.field_viability < low.field_viability


def test_relief_branch_gains_viability_from_debtful_branch_without_action_names() -> None:
    branches = [
        _branch("A", support=0.86, viability=0.78, debt=0.76, relief=0.02),
        _branch("B", support=0.50, viability=0.55, debt=0.10, relief=0.92),
    ]
    field = ContinuationField(CAUTIOUS_CONTROLS)
    no_rel = field.update(branches)
    with_rel = field.update(branches, [BranchRelation(source="B", target="A", relation_type="relief", weight=1.0)])
    assert with_rel["B"].field_relief_support > no_rel["B"].field_relief_support
    assert with_rel["B"].field_viability > no_rel["B"].field_viability
    assert with_rel["A"].field_grey_pressure >= no_rel["A"].field_grey_pressure


def test_close_grey_rivals_preserve_nonclosure_under_cautious_shape() -> None:
    branches = [
        _branch("A", support=0.62, viability=0.58, debt=0.34, uncertainty=0.42),
        _branch("B", support=0.60, viability=0.57, debt=0.32, uncertainty=0.44),
    ]
    relation = BranchRelation(source="A", target="B", relation_type="competition", weight=1.0)
    cautious = ContinuationField(CAUTIOUS_CONTROLS).update(branches, [relation])
    local = ContinuationField(LOCAL_CONTROLS).update(branches, [relation])
    assert cautious["A"].field_grey_pressure > local["A"].field_grey_pressure
    assert cautious["B"].field_grey_pressure > local["B"].field_grey_pressure
    assert cautious["A"].field_recursion_budget > local["A"].field_recursion_budget
    assert cautious["B"].field_recursion_budget > local["B"].field_recursion_budget


def test_equivalent_branches_are_quotient_marked_and_do_not_double_count_debt() -> None:
    branches = [
        _branch("A", support=0.55, viability=0.58, debt=0.42),
        _branch("B", support=0.54, viability=0.57, debt=0.40),
    ]
    states = ContinuationField(CAUTIOUS_CONTROLS).update(branches, [BranchRelation(source="A", target="B", relation_type="equivalence", weight=1.0)])
    assert states["A"].quotient_id == states["B"].quotient_id
    assert states["A"].quotient_share_count == 2
    assert states["B"].quotient_share_count == 2
    assert states["A"].field_debt <= 0.42
    assert states["B"].field_debt <= 0.40


def test_compensating_branch_can_cancel_debt_generically() -> None:
    branches = [
        _branch("A", support=0.70, viability=0.62, debt=0.74),
        _branch("C", support=0.48, viability=0.62, debt=0.12, relief=0.95),
    ]
    no_cancel = ContinuationField(CAUTIOUS_CONTROLS).update(branches)
    with_cancel = ContinuationField(CAUTIOUS_CONTROLS).update(branches, [BranchRelation(source="C", target="A", relation_type="cancellation", weight=1.0)])
    assert with_cancel["A"].field_debt < no_cancel["A"].field_debt
    assert with_cancel["C"].field_collapse_readiness > no_cancel["C"].field_collapse_readiness


def test_candidate_row_application_adds_field_terms_without_family_policy() -> None:
    rows = [
        {"action": "A", "support_mass": 0.84, "local_support": 0.84, "continuation_viability": 0.78, "burden_accumulation": 0.72, "burden_trend": 0.50, "continuation_instability": 0.72, "uncertainty": 0.18, "burden_relief": 0.02, "preventive_support": 0.02, "fracture_state": 0.45, "decision_state": 0.78, "commitment_stability": 0.72},
        {"action": "B", "support_mass": 0.52, "local_support": 0.52, "continuation_viability": 0.55, "burden_accumulation": 0.12, "burden_trend": 0.02, "continuation_instability": 0.12, "uncertainty": 0.22, "burden_relief": 0.86, "preventive_support": 0.36, "fracture_state": 0.10, "decision_state": 0.48, "commitment_stability": 0.50},
    ]
    out = {r["action"]: r for r in apply_continuation_field(rows, CAUTIOUS_CONTROLS)}
    assert "field_debt" in out["A"]
    assert "field_relief_support" in out["B"]
    assert out["B"]["field_relief_support"] > out["A"]["field_relief_support"]
    assert out["A"]["field_collapse_readiness"] < rows[0]["decision_state"]


def test_continuation_field_source_has_no_family_or_action_policy_literals() -> None:
    import pathlib

    src = pathlib.Path(__file__).parents[1] / "runtime" / "surfaces" / "continuation_field.py"
    text = src.read_text()
    forbidden = ["maintenance", "bandit", "maze", "renewal", "RUN", "REPAIR", "REPLACE", "INSPECT", "WAIT"]
    for token in forbidden:
        assert token not in text, token


if __name__ == "__main__":
    test_high_local_support_with_rising_debt_lowers_collapse_readiness()
    test_relief_branch_gains_viability_from_debtful_branch_without_action_names()
    test_close_grey_rivals_preserve_nonclosure_under_cautious_shape()
    test_equivalent_branches_are_quotient_marked_and_do_not_double_count_debt()
    test_compensating_branch_can_cancel_debt_generically()
    test_candidate_row_application_adds_field_terms_without_family_policy()
    test_continuation_field_source_has_no_family_or_action_policy_literals()
