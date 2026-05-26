"""Invariants for first-pass recursion-demand scheduler.

Run with: python -m agents.co.tests.recursion_scheduler_first_pass_invariants
"""
from __future__ import annotations

from pathlib import Path
import re

from agents.co.runtime.surfaces.continuation_field import BranchRelation, apply_continuation_field
from agents.co.runtime.surfaces.collapse_certificate import apply_collapse_certificates
from agents.co.runtime.surfaces.recursion_scheduler import derive_recursion_schedule, apply_recursion_scheduler

CONTROLS = {
    "local_authority": 0.30,
    "nonlocal_authority": 0.78,
    "path_sensitivity": 0.78,
    "revision_permissibility": 0.70,
    "rival_breadth": 0.72,
    "collapse_admissibility": 0.35,
    "low_evidence_sampling": 0.72,
    "contradiction_sensitivity": 0.82,
}

LOW_CONTROLS = dict(CONTROLS, nonlocal_authority=0.25, path_sensitivity=0.25, revision_permissibility=0.25, rival_breadth=0.25, low_evidence_sampling=0.25, contradiction_sensitivity=0.25, collapse_admissibility=0.80)


def _row(name: str, *, support: float = 0.60, debt: float = 0.20, grey: float = 0.10, hidden: float = 0.0, threshold: float = 0.0, quotient_id: str | None = None) -> dict:
    return {
        "action": name,
        "candidate_id": name,
        "support_mass": support,
        "decision_state": support,
        "local_support": support,
        "continuation_viability": support,
        "field_viability": support,
        "burden_pressure": debt,
        "burden_accumulation": debt,
        "field_debt": debt,
        "field_grey_pressure": grey,
        "field_recursion_budget": 0.0,
        "branch_internal_hiddenness_pressure": hidden,
        "branch_internal_threshold_pressure": threshold,
        "branch_internal_exposure_support": 0.0,
        "uncertainty": hidden,
        "commitment_stability": support,
        "quotient_id": quotient_id or name,
    }


def _demand(rows, rels, controls=CONTROLS):
    return derive_recursion_schedule(rows, relations=rels, controls=controls)


def test_dense_equivalent_region_contracts_instead_of_inflating_recursion() -> None:
    rows = [_row("branch_a", debt=0.22, grey=0.08, quotient_id="q0"), _row("branch_b", debt=0.24, grey=0.08, quotient_id="q0"), _row("branch_c", debt=0.23, grey=0.08, quotient_id="q0")]
    rels = [BranchRelation("branch_a", "branch_b", "equivalence", 1.0), BranchRelation("branch_a", "branch_c", "quotient", 1.0), BranchRelation("branch_b", "branch_c", "merge", 1.0)]
    schedules = _demand(rows, rels)
    assert schedules["branch_a"].demand <= 0.40, schedules["branch_a"]
    assert schedules["branch_a"].mode == "quotient_contract", schedules["branch_a"]


def test_dense_non_equivalent_region_raises_structural_recursion() -> None:
    rows = [_row("branch_a", debt=0.48, grey=0.52), _row("branch_b", debt=0.46, grey=0.50), _row("branch_c", debt=0.44, grey=0.50)]
    rels = [BranchRelation("branch_a", "branch_b", "rivalry", 0.95), BranchRelation("branch_a", "branch_c", "dependency", 0.90), BranchRelation("branch_b", "branch_c", "similarity", 0.85)]
    schedules = _demand(rows, rels)
    assert schedules["branch_a"].demand >= 0.42, schedules["branch_a"]
    assert schedules["branch_a"].budget >= 1
    assert "dense_non_equivalent_region" in schedules["branch_a"].reasons


def test_sparse_high_consequence_unresolved_branch_can_request_unfolding() -> None:
    rows = [_row("branch_a", support=0.35, debt=0.78, grey=0.34, hidden=0.74, threshold=0.62)]
    schedules = _demand(rows, [])
    assert schedules["branch_a"].demand >= 0.42, schedules["branch_a"]
    assert "sparse_high_consequence_unresolved" in schedules["branch_a"].reasons


def test_many_irrelevant_rows_do_not_create_recursion_demand() -> None:
    rows = [_row(f"branch_{i}", support=0.70, debt=0.05, grey=0.04) for i in range(8)]
    schedules = _demand(rows, [], controls=LOW_CONTROLS)
    assert max(s.demand for s in schedules.values()) <= 0.20, schedules
    assert all(s.budget == 0 for s in schedules.values())


def test_same_scalar_rows_changed_relation_topology_changes_demand() -> None:
    rows = [_row("branch_a", support=0.55, debt=0.40, grey=0.38), _row("branch_b", support=0.55, debt=0.40, grey=0.38)]
    none = _demand(rows, [])
    topo = _demand(rows, [BranchRelation("branch_a", "branch_b", "burden_transform", 0.95)])
    assert topo["branch_a"].demand > none["branch_a"].demand + 0.04, (none["branch_a"], topo["branch_a"])
    assert "relation_may_change_next_layer_status" in topo["branch_a"].reasons


def test_weak_decision_slot_competition_only_is_not_recursion_trigger() -> None:
    rows = [_row("branch_a", support=0.65, debt=0.14, grey=0.08), _row("branch_b", support=0.65, debt=0.14, grey=0.08)]
    schedules = _demand(rows, [BranchRelation("branch_a", "branch_b", "decision_slot_competition", 1.0)])
    assert schedules["branch_a"].demand <= 0.24, schedules["branch_a"]
    assert schedules["branch_a"].budget == 0


def test_scheduler_feeds_certificate_without_deciding_expression() -> None:
    rows = [_row("branch_a", support=0.36, debt=0.80, grey=0.56, hidden=0.70, threshold=0.62), _row("branch_b", support=0.52, debt=0.35, grey=0.22)]
    rels = [BranchRelation("branch_a", "branch_b", "burden_transform", 0.90)]
    fielded = apply_continuation_field(rows, CONTROLS, relations=rels)
    scheduled = apply_recursion_scheduler(fielded, relations=rels, controls=CONTROLS)
    certified = apply_collapse_certificates(scheduled, relations=rels, controls=CONTROLS)
    by = {r["action"]: r for r in certified}
    assert by["branch_a"]["recursion_scheduler_demand"] >= 0.42
    assert "recursion_demand" in by["branch_a"].get("collapse_blockers", []), by["branch_a"].get("collapse_certificate")
    assert by["branch_a"].get("action") == "branch_a"


def test_scheduler_source_contains_no_problem_family_or_native_policy_literals() -> None:
    source = Path(__file__).resolve().parents[1] / "runtime" / "surfaces" / "recursion_scheduler.py"
    text = source.read_text(encoding="utf-8").lower()
    forbidden = [
        "maintenance", "bandit", "renewal", "maze", "latent", "robot", "simulator",
        "repair", "replace", "inspect", "run", "wait", "left", "right", "up", "down",
        "dp_value", "shortest_path", "best_action", "optimal_policy", "baseline_value",
    ]
    leaked = [token for token in forbidden if re.search(r"(?<![a-z0-9_])" + re.escape(token) + r"(?![a-z0-9_])", text)]
    assert not leaked, leaked


def main() -> None:
    test_dense_equivalent_region_contracts_instead_of_inflating_recursion()
    test_dense_non_equivalent_region_raises_structural_recursion()
    test_sparse_high_consequence_unresolved_branch_can_request_unfolding()
    test_many_irrelevant_rows_do_not_create_recursion_demand()
    test_same_scalar_rows_changed_relation_topology_changes_demand()
    test_weak_decision_slot_competition_only_is_not_recursion_trigger()
    test_scheduler_feeds_certificate_without_deciding_expression()
    test_scheduler_source_contains_no_problem_family_or_native_policy_literals()
    print("recursion_scheduler_first_pass_invariants passed")


if __name__ == "__main__":
    main()
