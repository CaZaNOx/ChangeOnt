"""Invariant/diagnostic module for commitment surface relation awareness diagnostics.

Run with: python -m agents.co.tests.commitment_surface_relation_awareness_diagnostics
"""
from __future__ import annotations

"""CommitmentSurface relation-awareness diagnostics after certificate wiring.

The readout now consumes a first-class earned-collapse certificate.  Raw relation
metadata alone remains non-policy, but certificate fields derived upstream from
RelationSurface/RCF can change assessment and commitment for relation-traceable
reasons.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from agents.co.runtime.surfaces.commitment_surface import CommitmentSurface


@dataclass
class HeaderState:
    collapse_admissibility: float = 0.45
    revision_permissibility: float = 0.65
    support_carry_forward: float = 0.55
    rival_breadth: float = 0.65
    nonlocal_authority: float = 0.75
    path_sensitivity: float = 0.75
    local_authority: float = 0.35
    evidence_gate: float = 0.60
    fracture_tolerance: float = 0.45


@dataclass
class Header:
    state: HeaderState


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def _base_rows() -> List[Dict[str, Any]]:
    return [
        {
            "action": "A",
            "candidate_id": "A",
            "support_mass": 0.62,
            "decision_state": 0.58,
            "local_support": 0.60,
            "contradiction_burden": 0.24,
            "burden_accumulation": 0.24,
            "burden_trend": 0.02,
            "continuation_instability": 0.22,
            "commitment_stability": 0.58,
            "continuation_viability": 0.62,
            "support_persistence": 0.60,
            "sampling_demand": 0.02,
            "uncertainty": 0.22,
        },
        {
            "action": "B",
            "candidate_id": "B",
            "support_mass": 0.57,
            "decision_state": 0.55,
            "local_support": 0.56,
            "contradiction_burden": 0.27,
            "burden_accumulation": 0.27,
            "burden_trend": 0.02,
            "continuation_instability": 0.25,
            "commitment_stability": 0.55,
            "continuation_viability": 0.58,
            "support_persistence": 0.56,
            "sampling_demand": 0.02,
            "uncertainty": 0.24,
        },
    ]


def _commit(rows: List[Dict[str, Any]]) -> Tuple[Any, Dict[str, Any]]:
    obs = {"action_space": ["A", "B"]}
    prims = {"__candidate_publication_rows__": rows}
    scores = {"A": 0.60, "B": 0.57}
    return CommitmentSurface()._canonical_commitment_choice(scores, obs, prims, Header(HeaderState()), set(), ["A", "B"])


def test_raw_relation_metadata_alone_does_not_change_commitment_choice() -> None:
    plain_action, plain_tel = _commit(_base_rows())
    rows = _base_rows()
    rows[0].update({
        "field_relation_count": 9,
        "relation_surface_relation_count": 9,
        "relation_surface_telemetry": {"relations_by_type": {"relief": 4, "cancellation": 2, "rivalry": 3}},
        # No certificate fields: this metadata is telemetry, not a policy hint.
    })
    meta_action, meta_tel = _commit(rows)
    _assert(plain_action == meta_action, f"raw relation telemetry changed action: {plain_action} vs {meta_action}")
    _assert(plain_tel.get("canonical_commitment_mode") == meta_tel.get("canonical_commitment_mode"), "raw telemetry changed commitment mode")


def test_commitment_assessment_exposes_first_class_certificate_fields() -> None:
    rows = _base_rows()
    rows[0].update({
        "collapse_certificate_score": 0.12,
        "collapse_certificate_blocker_pressure": 0.92,
        "collapse_certificate_recursion_demand": 0.10,
        "unresolved_rival_count": 2,
        "quotient_resolved_rival_count": 0,
        "collapse_blockers": ["unresolved_non_equivalent_rival"],
    })
    _action, tel = _commit(rows)
    assessment = tel.get("canonical_commitment_assessment", {})
    _assert(assessment, "expected commitment assessment telemetry")
    for expected in (
        "collapse_certificate_score",
        "collapse_certificate_blocker_pressure",
        "collapse_certificate_recursion_demand",
        "collapse_blocked",
        "unresolved_rival_pressure",
        "quotient_resolved_pressure",
    ):
        _assert(expected in assessment["A"], f"first-class certificate field missing: {expected}")


def test_certificate_fields_can_change_commitment_assessment_without_scalar_row_mutation() -> None:
    base_rows = _base_rows()
    cert_rows = _base_rows()
    cert_rows[0].update({
        "collapse_certificate_ready": False,
        "collapse_certificate_score": 0.10,
        "collapse_certificate_blocker_pressure": 0.95,
        "collapse_certificate_recursion_demand": 0.10,
        "unresolved_rival_count": 2,
        "quotient_resolved_rival_count": 0,
        "collapse_blockers": ["unresolved_non_equivalent_rival"],
    })
    cert_rows[1].update({
        "collapse_certificate_ready": True,
        "collapse_certificate_score": 0.92,
        "collapse_certificate_blocker_pressure": 0.0,
        "collapse_certificate_recursion_demand": 0.0,
        "unresolved_rival_count": 0,
        "quotient_resolved_rival_count": 2,
        "collapse_blockers": [],
    })
    base_action, base_tel = _commit(base_rows)
    cert_action, cert_tel = _commit(cert_rows)
    _assert(base_tel.get("canonical_commitment_assessment") != cert_tel.get("canonical_commitment_assessment"), "certificate should alter assessment")
    _assert(cert_action == "B", f"certificate should select relation-ready B in this toy case, got {cert_action}; base was {base_action}")


if __name__ == "__main__":
    test_raw_relation_metadata_alone_does_not_change_commitment_choice()
    test_commitment_assessment_exposes_first_class_certificate_fields()
    test_certificate_fields_can_change_commitment_assessment_without_scalar_row_mutation()
