"""First-pass recursion scheduler microprobe.

Run with: python -m experiments.studies.recursion_scheduler_first_pass_probe_v1
"""
from __future__ import annotations

import json
from pathlib import Path

from agents.co.runtime.surfaces.continuation_field import BranchRelation
from agents.co.runtime.surfaces.recursion_scheduler import derive_recursion_schedule

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


def row(name: str, support: float = 0.60, debt: float = 0.20, grey: float = 0.10, hidden: float = 0.0, threshold: float = 0.0, quotient_id: str | None = None) -> dict:
    return {
        "action": name,
        "candidate_id": name,
        "support_mass": support,
        "decision_state": support,
        "field_viability": support,
        "continuation_viability": support,
        "field_debt": debt,
        "burden_accumulation": debt,
        "field_grey_pressure": grey,
        "field_recursion_budget": 0.0,
        "branch_internal_hiddenness_pressure": hidden,
        "branch_internal_threshold_pressure": threshold,
        "uncertainty": hidden,
        "quotient_id": quotient_id or name,
    }


def schedule_payload(rows, rels):
    schedules = derive_recursion_schedule(rows, relations=rels, controls=CONTROLS)
    return {str(k): v.to_dict() for k, v in schedules.items()}


def main() -> None:
    cases = []
    cases.append({
        "case": "dense_equivalent_contracts",
        "schedules": schedule_payload(
            [row("a", debt=0.22, grey=0.08, quotient_id="q"), row("b", debt=0.24, grey=0.08, quotient_id="q"), row("c", debt=0.23, grey=0.08, quotient_id="q")],
            [BranchRelation("a", "b", "equivalence", 1.0), BranchRelation("a", "c", "quotient", 1.0), BranchRelation("b", "c", "merge", 1.0)],
        ),
    })
    cases.append({
        "case": "dense_non_equivalent_requests",
        "schedules": schedule_payload(
            [row("a", debt=0.48, grey=0.52), row("b", debt=0.46, grey=0.50), row("c", debt=0.44, grey=0.50)],
            [BranchRelation("a", "b", "rivalry", 0.95), BranchRelation("a", "c", "dependency", 0.90), BranchRelation("b", "c", "similarity", 0.85)],
        ),
    })
    cases.append({
        "case": "sparse_high_consequence_requests",
        "schedules": schedule_payload([row("a", support=0.35, debt=0.78, grey=0.34, hidden=0.74, threshold=0.62)], []),
    })
    cases.append({
        "case": "weak_competition_only_low",
        "schedules": schedule_payload([row("a", support=0.65, debt=0.14, grey=0.08), row("b", support=0.65, debt=0.14, grey=0.08)], [BranchRelation("a", "b", "decision_slot_competition", 1.0)]),
    })

    summary = {
        "study": "recursion_scheduler_first_pass_probe_v1",
        "cases": len(cases),
        "max_demand_by_case": {c["case"]: max(v["demand"] for v in c["schedules"].values()) for c in cases},
        "cases_detail": cases,
        "claim_boundary": "first-pass structural microprobe only; not empirical proof and not algorithmic novelty evidence",
    }
    out = Path("outputs/studies/recursion_scheduler_first_pass_probe_v1.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
