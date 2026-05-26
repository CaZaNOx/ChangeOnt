"""Invariant/diagnostic module for burden relation microdiagnostics.

Run with: python -m agents.co.tests.burden_relation_microdiagnostics
"""
from __future__ import annotations

"""Microdiagnostics for the burden-operation / relation-to-collapse contract.

These are deliberately small diagnostics, not performance tests.  They hold
ordinary scalar candidate fields fixed where possible and change only explicit
relation topology or burden-operation cues.  The point is to detect whether the
recursive continuation field behaves as a relation-aware continuation field or
collapses back into scalar action scoring.
"""

from agents.co.runtime.surfaces.continuation_field import BranchRelation, apply_continuation_field


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


def _row(
    branch: str,
    *,
    support: float = 0.60,
    viability: float = 0.60,
    debt: float = 0.25,
    uncertainty: float = 0.20,
    burden_relief: float = 0.0,
    preventive_support: float = 0.0,
) -> dict:
    return {
        "action": branch,
        "support_mass": support,
        "local_support": support,
        "continuation_viability": viability,
        "stability_under_change": viability,
        "burden_pressure": debt,
        "burden_accumulation": debt,
        "burden_trend": debt,
        "continuation_instability": debt,
        "uncertainty": uncertainty,
        "burden_relief": burden_relief,
        "preventive_support": preventive_support,
        "decision_state": viability,
        "commitment_stability": viability,
        "fracture_state": min(1.0, debt * 0.5),
    }


def _by_action(rows: list[dict]) -> dict[str, dict]:
    return {str(r["action"]): r for r in rows}


def test_fixed_scalar_rows_change_under_explicit_relation_topology() -> None:
    """Same scalar rows, different explicit topology must change field behavior."""
    rows = [
        _row("a", support=0.62, viability=0.59, debt=0.36, uncertainty=0.42),
        _row("b", support=0.61, viability=0.58, debt=0.35, uncertainty=0.43),
    ]
    no_rel = _by_action(apply_continuation_field(rows, CAUTIOUS_CONTROLS))
    rivalry = _by_action(
        apply_continuation_field(
            rows,
            CAUTIOUS_CONTROLS,
            relations=[BranchRelation(source="a", target="b", relation_type="rivalry", weight=1.0)],
        )
    )
    equivalent = _by_action(
        apply_continuation_field(
            rows,
            CAUTIOUS_CONTROLS,
            relations=[BranchRelation(source="a", target="b", relation_type="equivalence", weight=1.0)],
        )
    )

    assert no_rel["a"]["field_relation_count"] == 0
    assert rivalry["a"]["field_relation_count"] == 1
    assert rivalry["a"]["field_grey_pressure"] > no_rel["a"]["field_grey_pressure"]
    assert rivalry["b"]["field_recursion_budget"] > no_rel["b"]["field_recursion_budget"]
    assert equivalent["a"]["quotient_share_count"] == 2
    assert equivalent["b"]["quotient_share_count"] == 2
    assert equivalent["a"]["field_grey_pressure"] <= rivalry["a"]["field_grey_pressure"]


def test_masking_is_not_buffering_or_relief() -> None:
    """High local support with high debt must not be mistaken for buffering/relief."""
    low_burden = _by_action(apply_continuation_field([_row("stable", support=0.86, viability=0.82, debt=0.05)], CAUTIOUS_CONTROLS))["stable"]
    masked = _by_action(apply_continuation_field([_row("masked", support=0.86, viability=0.82, debt=0.82)], CAUTIOUS_CONTROLS))["masked"]
    buffered = _by_action(
        apply_continuation_field(
            [_row("buffered", support=0.86, viability=0.82, debt=0.05, preventive_support=0.80)],
            CAUTIOUS_CONTROLS,
        )
    )["buffered"]

    assert masked["field_debt"] > low_burden["field_debt"]
    assert masked["field_collapse_readiness"] < low_burden["field_collapse_readiness"]
    assert masked["field_relief_support"] <= 1e-9
    assert buffered["field_debt"] <= low_burden["field_debt"] + 1e-9
    assert buffered["field_relief_support"] > low_burden["field_relief_support"]
    assert buffered["field_collapse_readiness"] > masked["field_collapse_readiness"]


def test_exposure_shared_evidence_is_not_relief() -> None:
    """Exposure/shared evidence may preserve grey without granting relief support."""
    rows = [
        _row("uncertain", support=0.66, viability=0.60, debt=0.32, uncertainty=0.78),
        _row("probe", support=0.46, viability=0.48, debt=0.12, uncertainty=0.76),
    ]
    exposure = _by_action(
        apply_continuation_field(
            rows,
            CAUTIOUS_CONTROLS,
            relations=[BranchRelation(source="probe", target="uncertain", relation_type="shared_evidence", weight=1.0)],
        )
    )
    relief = _by_action(
        apply_continuation_field(
            [dict(rows[0]), dict(rows[1], burden_relief=0.90)],
            CAUTIOUS_CONTROLS,
            relations=[BranchRelation(source="probe", target="uncertain", relation_type="relief", weight=1.0)],
        )
    )

    assert exposure["probe"]["field_relation_count"] == 1
    assert exposure["probe"]["field_grey_pressure"] > 0.0
    assert exposure["probe"]["field_relief_support"] <= 1e-9
    assert relief["probe"]["field_relief_support"] > exposure["probe"]["field_relief_support"]


def test_relief_and_cancellation_are_distinct_burden_operations() -> None:
    """Relief supports a relieving branch; cancellation reduces target debt."""
    rows = [
        _row("carrying", support=0.76, viability=0.68, debt=0.80, uncertainty=0.20),
        _row("operator", support=0.50, viability=0.55, debt=0.10, uncertainty=0.20, burden_relief=0.90),
    ]
    relief = _by_action(
        apply_continuation_field(
            rows,
            CAUTIOUS_CONTROLS,
            relations=[BranchRelation(source="operator", target="carrying", relation_type="relief", weight=1.0)],
        )
    )
    cancel = _by_action(
        apply_continuation_field(
            rows,
            CAUTIOUS_CONTROLS,
            relations=[BranchRelation(source="operator", target="carrying", relation_type="cancellation", weight=1.0)],
        )
    )

    assert relief["operator"]["field_relief_support"] > 0.10
    assert cancel["carrying"]["field_debt"] < relief["carrying"]["field_debt"]
    assert cancel["carrying"]["field_collapse_readiness"] > relief["carrying"]["field_collapse_readiness"]
    assert relief["operator"]["field_relief_support"] > cancel["operator"]["field_relief_support"]


def test_dense_equivalent_paths_quotient_instead_of_preserving_extra_grey() -> None:
    rows = [
        _row("p1", support=0.58, viability=0.56, debt=0.34, uncertainty=0.32),
        _row("p2", support=0.57, viability=0.55, debt=0.33, uncertainty=0.33),
        _row("p3", support=0.59, viability=0.56, debt=0.35, uncertainty=0.31),
    ]
    equivalences = [
        BranchRelation(source="p1", target="p2", relation_type="equivalence", weight=1.0),
        BranchRelation(source="p2", target="p3", relation_type="equivalence", weight=1.0),
    ]
    rivals = [
        BranchRelation(source="p1", target="p2", relation_type="rivalry", weight=1.0),
        BranchRelation(source="p2", target="p3", relation_type="rivalry", weight=1.0),
    ]
    q = _by_action(apply_continuation_field(rows, CAUTIOUS_CONTROLS, relations=equivalences))
    r = _by_action(apply_continuation_field(rows, CAUTIOUS_CONTROLS, relations=rivals))

    assert all(q[k]["quotient_share_count"] >= 2 for k in ("p1", "p2", "p3"))
    assert all(r[k]["quotient_share_count"] == 1 for k in ("p1", "p2", "p3"))
    assert sum(q[k]["field_grey_pressure"] for k in q) < sum(r[k]["field_grey_pressure"] for k in r)


def test_dense_non_equivalent_paths_preserve_grey_and_recursion() -> None:
    rows = [
        _row("p1", support=0.58, viability=0.56, debt=0.38, uncertainty=0.42),
        _row("p2", support=0.57, viability=0.55, debt=0.39, uncertainty=0.43),
        _row("p3", support=0.59, viability=0.56, debt=0.37, uncertainty=0.41),
    ]
    rivals = [
        BranchRelation(source="p1", target="p2", relation_type="rivalry", weight=1.0),
        BranchRelation(source="p2", target="p3", relation_type="rivalry", weight=1.0),
    ]
    cautious = _by_action(apply_continuation_field(rows, CAUTIOUS_CONTROLS, relations=rivals))
    local = _by_action(apply_continuation_field(rows, LOCAL_CONTROLS, relations=rivals))

    assert sum(cautious[k]["field_grey_pressure"] for k in cautious) > sum(local[k]["field_grey_pressure"] for k in local)
    assert sum(cautious[k]["field_recursion_budget"] for k in cautious) > sum(local[k]["field_recursion_budget"] for k in local)


def test_sparse_high_consequence_unresolved_relation_can_drive_recursion() -> None:
    rows = [
        _row("main", support=0.72, viability=0.68, debt=0.28, uncertainty=0.20),
        _row("risk", support=0.30, viability=0.34, debt=0.86, uncertainty=0.82),
    ]
    relation = [BranchRelation(source="main", target="risk", relation_type="rivalry", weight=1.0)]
    cautious = _by_action(apply_continuation_field(rows, CAUTIOUS_CONTROLS, relations=relation))
    local = _by_action(apply_continuation_field(rows, LOCAL_CONTROLS, relations=relation))

    assert cautious["risk"]["field_recursion_budget"] > local["risk"]["field_recursion_budget"]
    assert cautious["main"]["field_collapse_readiness"] < local["main"]["field_collapse_readiness"]


def test_collapse_certificate_distinguishes_quotient_from_unresolved_rivalry() -> None:
    """Same scores: equivalent rivals permit more collapse than unresolved rivals."""
    rows = [
        _row("a", support=0.72, viability=0.70, debt=0.22, uncertainty=0.20),
        _row("b", support=0.70, viability=0.69, debt=0.23, uncertainty=0.21),
    ]
    quotient = _by_action(
        apply_continuation_field(
            rows,
            CAUTIOUS_CONTROLS,
            relations=[BranchRelation(source="a", target="b", relation_type="equivalence", weight=1.0)],
        )
    )
    rival = _by_action(
        apply_continuation_field(
            rows,
            CAUTIOUS_CONTROLS,
            relations=[BranchRelation(source="a", target="b", relation_type="rivalry", weight=1.0)],
        )
    )

    assert quotient["a"]["quotient_share_count"] == 2
    assert rival["a"]["quotient_share_count"] == 1
    assert quotient["a"]["field_grey_pressure"] < rival["a"]["field_grey_pressure"]
    assert quotient["a"]["field_collapse_readiness"] > rival["a"]["field_collapse_readiness"]


if __name__ == "__main__":
    test_fixed_scalar_rows_change_under_explicit_relation_topology()
    test_masking_is_not_buffering_or_relief()
    test_exposure_shared_evidence_is_not_relief()
    test_relief_and_cancellation_are_distinct_burden_operations()
    test_dense_equivalent_paths_quotient_instead_of_preserving_extra_grey()
    test_dense_non_equivalent_paths_preserve_grey_and_recursion()
    test_sparse_high_consequence_unresolved_relation_can_drive_recursion()
    test_collapse_certificate_distinguishes_quotient_from_unresolved_rivalry()
