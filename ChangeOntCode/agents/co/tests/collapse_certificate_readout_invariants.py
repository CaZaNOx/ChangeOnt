"""Invariants proving CommitmentSurface consumes CollapseCertificate gates."""
from __future__ import annotations

"""Earned-collapse certificate invariants.

These diagnostics verify the new architecture boundary: relation topology is
summarized as a first-class collapse certificate before readout, and
CommitmentSurface consumes the certificate as relation/collapse evidence rather
than receiving only scalar field perturbations.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from agents.co.runtime.surfaces.collapse_certificate import apply_collapse_certificates
from agents.co.runtime.surfaces.commitment_surface import CommitmentSurface
from agents.co.runtime.surfaces.continuation_field import BranchRelation


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


def _commit(rows: List[Dict[str, Any]]) -> Tuple[Any, Dict[str, Any]]:
    obs = {"action_space": [r["action"] for r in rows]}
    prims = {"__candidate_publication_rows__": rows}
    scores = {r["action"]: float(r.get("field_score", r.get("decision_state", 0.55))) for r in rows}
    return CommitmentSurface()._canonical_commitment_choice(scores, obs, prims, Header(HeaderState()), set(), [r["action"] for r in rows])


def _row(name: str, support: float = 0.60, ready: float = 0.55, debt: float = 0.20, grey: float = 0.10, rec: float = 0.10) -> Dict[str, Any]:
    return {
        "action": name,
        "candidate_id": name,
        "branch_id": name,
        "field_score": support,
        "support_mass": support,
        "decision_state": support,
        "local_support": support,
        "contradiction_burden": debt,
        "burden_accumulation": debt,
        "burden_trend": 0.0,
        "continuation_instability": debt,
        "commitment_stability": ready,
        "continuation_viability": ready,
        "support_persistence": ready,
        "sampling_demand": 0.10,
        "uncertainty": 0.20,
        "field_debt": debt,
        "field_grey_pressure": grey,
        "field_recursion_budget": rec,
        "field_collapse_readiness": ready,
        "quotient_share_count": 1,
        "field_relation_count": 0,
    }


def test_certificate_blocks_unresolved_rival_and_allows_quotient_ready_branch() -> None:
    rows = [_row("A", support=0.64, ready=0.55, debt=0.18, grey=0.32, rec=0.35), _row("B", support=0.60, ready=0.78, debt=0.18, grey=0.08, rec=0.10)]
    rows[0]["field_relation_count"] = 1
    rows[1]["field_relation_count"] = 1
    rows[1]["quotient_share_count"] = 2
    rels = [BranchRelation(source="A", target="B", relation_type="rivalry", weight=1.0), BranchRelation(source="B", target="A", relation_type="equivalence", weight=1.0)]
    certified = apply_collapse_certificates(rows, relations=rels, controls={"collapse_admissibility": 0.45, "revision_permissibility": 0.65, "rival_breadth": 0.65, "path_sensitivity": 0.75, "nonlocal_authority": 0.75})
    by = {r["action"]: r for r in certified}
    _assert("unresolved_non_equivalent_rival" in by["A"]["collapse_blockers"] or by["A"]["collapse_certificate_blocker_pressure"] > 0.0, "A should carry relation blocker")
    _assert(by["B"]["quotient_resolved_rival_count"] > 0, "B should carry quotient support")
    chosen, tel = _commit(certified)
    _assert(chosen == "B", f"certificate should let quotient-ready branch beat blocked rival, got {chosen} {tel}")
    assessment = tel.get("canonical_commitment_assessment", {})
    _assert("collapse_certificate_score" in assessment["A"], "assessment should expose first-class certificate score")
    _assert("collapse_blocked" in assessment["A"], "assessment should expose first-class blocker pressure")


def test_relation_metadata_without_certificate_does_not_drive_policy() -> None:
    rows = [_row("A", support=0.62), _row("B", support=0.60)]
    rows[0]["relation_surface_telemetry"] = {"relations_by_type": {"rivalry": 5}}
    rows[0]["collapse_blockers"] = ["unresolved_non_equivalent_rival"]
    plain_choice, _plain = _commit([_row("A", support=0.62), _row("B", support=0.60)])
    meta_choice, _meta = _commit(rows)
    _assert(plain_choice == meta_choice, "raw relation metadata without certificate should not be policy")


def test_certificate_recursion_pressure_reopens_sampling_when_no_collapse_is_earned() -> None:
    rows = [
        _row("A", support=0.58, ready=0.30, debt=0.32, grey=0.60, rec=0.80),
        _row("B", support=0.57, ready=0.28, debt=0.30, grey=0.58, rec=0.78),
        _row("S", support=0.46, ready=0.20, debt=0.10, grey=0.20, rec=0.20),
    ]
    rows[0].update({"collapse_certificate_score": 0.12, "collapse_certificate_blocker_pressure": 0.80, "collapse_certificate_recursion_demand": 0.92, "unresolved_rival_count": 2, "collapse_blockers": ["recursion_demand"]})
    rows[1].update({"collapse_certificate_score": 0.12, "collapse_certificate_blocker_pressure": 0.75, "collapse_certificate_recursion_demand": 0.90, "unresolved_rival_count": 2, "collapse_blockers": ["recursion_demand"]})
    rows[2].update({"sampling_demand": 0.92, "uncertainty": 0.90, "collapse_certificate_score": 0.20, "collapse_certificate_blocker_pressure": 0.05, "collapse_certificate_recursion_demand": 0.15})
    chosen, tel = _commit(rows)
    _assert(tel.get("canonical_commitment_mode") in {"reopen_or_sample", "stable_continuation"}, f"expected non-dominance under recursion pressure: {tel}")
    _assert(chosen in {"S", "B", "A"}, "sanity: admissible choice")
    assessment = tel.get("canonical_commitment_assessment", {})
    _assert(assessment["A"]["collapse_certificate_recursion_demand"] > 0.0, "recursion demand should reach readout")


def test_non_ready_certificate_blocks_dominance_even_when_local_support_is_high() -> None:
    rows = [
        _row("A", support=0.74, ready=0.62, debt=0.18, grey=0.08, rec=0.62),
        _row("B", support=0.60, ready=0.55, debt=0.16, grey=0.05, rec=0.08),
    ]
    rows[0].update({
        "field_relation_count": 2,
        "collapse_certificate_ready": False,
        "collapse_certificate_score": 0.46,
        "collapse_certificate_blocker_pressure": 0.16,
        "collapse_certificate_recursion_demand": 0.62,
        "collapse_blockers": [],
    })
    rows[1].update({
        "collapse_certificate_ready": True,
        "collapse_certificate_score": 0.72,
        "collapse_certificate_blocker_pressure": 0.0,
        "collapse_certificate_recursion_demand": 0.04,
        "collapse_blockers": [],
    })
    chosen, tel = _commit(rows)
    assessment = tel.get("canonical_commitment_assessment", {})
    _assert(assessment["A"].get("certificate_blocks_dominance", 0.0) >= 0.5, f"A should be dominance-blocked by non-ready certificate: {assessment['A']}")
    _assert(tel.get("canonical_commitment_mode") != "dominance" or chosen != "A", f"non-ready certificate must not permit dominance collapse into A: {chosen} {tel}")

if __name__ == "__main__":
    test_certificate_blocks_unresolved_rival_and_allows_quotient_ready_branch()
    test_relation_metadata_without_certificate_does_not_drive_policy()
    test_certificate_recursion_pressure_reopens_sampling_when_no_collapse_is_earned()
    test_non_ready_certificate_blocks_dominance_even_when_local_support_is_high()
