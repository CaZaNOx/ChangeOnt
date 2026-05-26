from __future__ import annotations

"""Targeted structural microcase probe v1.

This diagnostic is not a reward benchmark.  It builds synthetic candidate rows
with controlled public effects so the current kernel can be checked against
small, known structural expectations:

- weak decision-slot competition should be logged but should not count as a
  branch-internal burden operation or structural blocker;
- hiddenness carried without exposure should block dominance-style collapse;
- explicit exposure/relief/cancellation should be recognized as resolver
  support and, under otherwise equal local evidence, should outrank the branch
  that merely carries the burden;
- equivalent pressure signatures should produce quotient/equivalence support
  without creating false rivalry;
- equal local scores with no public effects should remain a neutral baseline.

The probe records both pass/fail assertions and interpretive watchpoints.  A
watchpoint is a real limitation to review, not a test failure.
"""

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence

from agents.co.tests.relation_path_trace_diagnostics import _run_candidate_commitment, _strip_public_effects

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "structural_microcase_probe_v1.json"


def _effect(
    operation: str,
    burden_type: str = "",
    *,
    kind: str = "burden",
    magnitude: float = 0.8,
    relation_scope: str = "micro_scope",
    public_basis: str = "visible_observation",
    leakage_status: str = "public",
    scope: str = "candidate",
    **extra: Any,
) -> Dict[str, Any]:
    fact: Dict[str, Any] = {
        "operation": operation,
        "kind": kind,
        "scope": scope,
        "magnitude": float(magnitude),
        "relation_scope": relation_scope,
        "public_basis": public_basis,
        "leakage_status": leakage_status,
    }
    if burden_type:
        fact["burden_type"] = burden_type
    fact.update(extra)
    return fact


def _candidate(
    candidate_id: str,
    *,
    visible: float = 0.60,
    uncertainty: float = 0.30,
    coverage: float = 0.60,
    tested: float = 0.50,
    reversibility: float = 0.70,
    public_effects: Sequence[Mapping[str, Any]] = (),
) -> Dict[str, Any]:
    return {
        "candidate_id": candidate_id,
        "legal": True,
        "visible_delta": float(visible),
        "line_support": float(visible),
        "coverage_adequacy": float(coverage),
        "tested_hint": float(tested),
        "uncertainty_hint": float(uncertainty),
        "reversibility_hint": float(reversibility),
        "public_effects": [dict(e) for e in public_effects],
    }


def _cases() -> Dict[str, Dict[str, Any]]:
    return {
        "neutral_no_effects_equal": {
            "expect": ["no_relations", "no_branch_internal_operations"],
            "candidates": [
                _candidate("A", visible=0.60),
                _candidate("B", visible=0.60),
            ],
        },
        "weak_decision_slot_only": {
            "expect": ["weak_competition_only", "no_branch_internal_operations", "no_false_blocker"],
            "candidates": [
                _candidate("A", visible=0.60, public_effects=[_effect("decision_slot", kind="legal_constraint", relation_scope="slot")]),
                _candidate("B", visible=0.60, public_effects=[_effect("decision_slot", kind="legal_constraint", relation_scope="slot")]),
            ],
        },
        "hiddenness_without_exposure": {
            "expect": ["hiddenness_blocker", "dominance_blocked"],
            "candidates": [
                _candidate("continue", visible=0.72, coverage=0.70, tested=0.60, uncertainty=0.20, public_effects=[
                    _effect("carry", "hiddenness", kind="hiddenness", magnitude=0.90, relation_scope="hidden")
                ]),
                _candidate("neutral_probe", visible=0.62, coverage=0.70, tested=0.60, uncertainty=0.20),
            ],
        },
        "exposure_resolves_hiddenness_equal_evidence": {
            "expect": ["shared_evidence_relation", "exposure_support", "resolver_outranks_carrier"],
            "candidates": [
                _candidate("continue", visible=0.60, public_effects=[
                    _effect("carry", "hiddenness", kind="hiddenness", magnitude=0.90, relation_scope="hidden")
                ]),
                _candidate("inspect", visible=0.60, public_effects=[
                    _effect("expose", "hiddenness", kind="hiddenness", magnitude=0.90, relation_scope="hidden")
                ]),
            ],
        },
        "relief_resolves_burden_equal_evidence": {
            "expect": ["relief_relation", "relief_support", "resolver_outranks_carrier"],
            "candidates": [
                _candidate("carry_load", visible=0.60, public_effects=[
                    _effect("carry", "degradation", magnitude=0.85, relation_scope="degradation")
                ]),
                _candidate("repair", visible=0.60, public_effects=[
                    _effect("relieve", "degradation", magnitude=0.85, relation_scope="degradation")
                ]),
            ],
        },
        "cancellation_resolves_burden_equal_evidence": {
            "expect": ["cancellation_relation", "cancellation_support", "resolver_outranks_carrier"],
            "candidates": [
                _candidate("risk_carry", visible=0.60, public_effects=[
                    _effect("carry", "failure_risk", magnitude=0.85, relation_scope="failure_risk")
                ]),
                _candidate("replace", visible=0.60, public_effects=[
                    _effect("cancel", "failure_risk", magnitude=0.85, relation_scope="failure_risk")
                ]),
            ],
        },
        "quotient_equivalent_pressure_equal_evidence": {
            "expect": ["equivalence_relation", "quotient_support", "no_unresolved_rivalry"],
            "candidates": [
                _candidate("left", visible=0.60, public_effects=[
                    _effect("carry", "same_pressure", magnitude=0.30, relation_scope="same_pressure")
                ]),
                _candidate("right", visible=0.60, public_effects=[
                    _effect("carry", "same_pressure", magnitude=0.30, relation_scope="same_pressure")
                ]),
            ],
        },
    }


def _relations_by_type(rows: Sequence[Mapping[str, Any]]) -> Dict[str, int]:
    if not rows:
        return {}
    tel = rows[0].get("relation_surface_telemetry", {})
    if isinstance(tel, Mapping):
        return {str(k): int(v) for k, v in dict(tel.get("relations_by_type", {}) or {}).items()}
    return {}


def _telemetry(rows: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    if not rows:
        return {}
    tel = rows[0].get("relation_surface_telemetry", {})
    return dict(tel) if isinstance(tel, Mapping) else {}


def _by_action(rows: Iterable[Mapping[str, Any]]) -> Dict[str, Mapping[str, Any]]:
    return {str(r.get("action")): r for r in rows if r.get("action") is not None}


def _assessment(commit: Mapping[str, Any], action: str) -> Dict[str, Any]:
    ass = commit.get("canonical_commitment_assessment", {})
    if isinstance(ass, Mapping):
        return dict(ass.get(action, {}) or {})
    return {}


def _rounded_assessment(commit: Mapping[str, Any]) -> Dict[str, Dict[str, float]]:
    out: Dict[str, Dict[str, float]] = {}
    ass = commit.get("canonical_commitment_assessment", {})
    if not isinstance(ass, Mapping):
        return out
    keys = (
        "dominance_score",
        "sampling_score",
        "continuation_score",
        "collapse_certificate_blocker_pressure",
        "collapse_certificate_recursion_demand",
        "certificate_gate_open",
        "certificate_blocks_dominance",
        "collapse_blocked",
    )
    for action, rec in ass.items():
        if not isinstance(rec, Mapping):
            continue
        out[str(action)] = {}
        for key in keys:
            try:
                out[str(action)][key] = round(float(rec.get(key, 0.0)), 6)
            except Exception:
                out[str(action)][key] = 0.0
    return out


def _summarize_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    summary: List[Dict[str, Any]] = []
    for row in rows:
        summary.append({
            "action": row.get("action"),
            "branch_id": str(row.get("branch_id", ""))[:220],
            "identity_source": row.get("relation_surface_identity_source"),
            "branch_internal_operation_counts": dict(row.get("branch_internal_operation_counts", {}) or {}),
            "branch_internal_hiddenness_pressure": row.get("branch_internal_hiddenness_pressure"),
            "branch_internal_exposure_support": row.get("branch_internal_exposure_support"),
            "branch_internal_relief_support": row.get("branch_internal_relief_support"),
            "branch_internal_cancellation_support": row.get("branch_internal_cancellation_support"),
            "field_debt": row.get("field_debt"),
            "field_viability": row.get("field_viability"),
            "field_grey_pressure": row.get("field_grey_pressure"),
            "field_recursion_budget": row.get("field_recursion_budget"),
            "field_collapse_readiness": row.get("field_collapse_readiness"),
            "collapse_certificate_ready": row.get("collapse_certificate_ready"),
            "collapse_certificate_status": row.get("collapse_certificate_status"),
            "collapse_blockers": list(row.get("collapse_blockers", []) or []),
            "collapse_certificate_reason_flags": list(row.get("collapse_certificate_reason_flags", []) or []),
            "collapse_certificate_relations_by_type": dict(row.get("collapse_certificate_relations_by_type", {}) or {}),
            "quotient_share_count": row.get("quotient_share_count"),
            "unresolved_rival_count": row.get("unresolved_rival_count"),
            "quotient_resolved_rival_count": row.get("quotient_resolved_rival_count"),
        })
    return summary


def _field_delta(rows: Sequence[Mapping[str, Any]], stripped_rows: Sequence[Mapping[str, Any]]) -> float:
    by_a = _by_action(rows)
    off = _by_action(stripped_rows)
    keys = (
        "field_debt",
        "field_viability",
        "field_grey_pressure",
        "field_recursion_budget",
        "field_collapse_readiness",
        "collapse_certificate_blocker_pressure",
        "collapse_certificate_recursion_demand",
    )
    total = 0.0
    for action, row in by_a.items():
        other = off.get(action, {})
        for key in keys:
            try:
                total += abs(float(row.get(key, 0.0)) - float(other.get(key, 0.0)))
            except Exception:
                pass
    return round(total, 6)


def _check_expectations(
    case_name: str,
    expectations: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    stripped_rows: Sequence[Mapping[str, Any]],
    commit: Mapping[str, Any],
) -> List[Dict[str, Any]]:
    rels = _relations_by_type(rows)
    tel = _telemetry(rows)
    by_action = _by_action(rows)
    failures: List[Dict[str, Any]] = []

    def fail(expectation: str, detail: str) -> None:
        failures.append({"expectation": expectation, "detail": detail})

    if "no_relations" in expectations and sum(rels.values()) != 0:
        fail("no_relations", f"expected no relations, got {rels}")
    if "no_branch_internal_operations" in expectations and int(tel.get("branch_internal_operation_rows", 0) or 0) != 0:
        fail("no_branch_internal_operations", f"expected zero branch-internal rows, got {tel.get('branch_internal_operation_rows')}")
    if "weak_competition_only" in expectations:
        if set(rels.keys()) - {"decision_slot_competition"}:
            fail("weak_competition_only", f"unexpected non-weak relation types: {rels}")
        if int(rels.get("decision_slot_competition", 0) or 0) <= 0:
            fail("weak_competition_only", f"expected weak competition relations, got {rels}")
    if "no_false_blocker" in expectations:
        blockers = {str(r.get("action")): list(r.get("collapse_blockers", []) or []) for r in rows}
        if any(blockers.values()):
            fail("no_false_blocker", f"weak/procedural case should not create blockers: {blockers}")
    if "hiddenness_blocker" in expectations:
        hidden_rows = [r for r in rows if float(r.get("branch_internal_hiddenness_pressure", 0.0) or 0.0) > 0.50]
        if not hidden_rows:
            fail("hiddenness_blocker", "expected at least one branch carrying hiddenness pressure")
        elif not any("unresolved_hiddenness_burden" in list(r.get("collapse_blockers", []) or []) for r in hidden_rows):
            fail("hiddenness_blocker", f"hiddenness rows lacked unresolved_hiddenness_burden blocker: {_summarize_rows(hidden_rows)}")
    if "dominance_blocked" in expectations:
        blocked = []
        for row in rows:
            action = str(row.get("action"))
            ass = _assessment(commit, action)
            if float(ass.get("certificate_blocks_dominance", 0.0) or 0.0) >= 0.5:
                blocked.append(action)
        if not blocked:
            fail("dominance_blocked", f"expected at least one certificate_blocks_dominance assessment: {_rounded_assessment(commit)}")
    if "shared_evidence_relation" in expectations and int(rels.get("shared_evidence", 0) or 0) <= 0:
        fail("shared_evidence_relation", f"expected shared_evidence relation, got {rels}")
    if "relief_relation" in expectations and int(rels.get("relief", 0) or 0) <= 0:
        fail("relief_relation", f"expected relief relation, got {rels}")
    if "cancellation_relation" in expectations and int(rels.get("cancellation", 0) or 0) <= 0:
        fail("cancellation_relation", f"expected cancellation relation, got {rels}")
    if "equivalence_relation" in expectations and int(rels.get("equivalence", 0) or 0) <= 0:
        fail("equivalence_relation", f"expected equivalence relation, got {rels}")
    if "exposure_support" in expectations:
        if not any(float(r.get("branch_internal_exposure_support", 0.0) or 0.0) > 0.50 for r in rows):
            fail("exposure_support", f"expected exposure support in a branch: {_summarize_rows(rows)}")
    if "relief_support" in expectations:
        if not any(float(r.get("branch_internal_relief_support", 0.0) or 0.0) > 0.50 for r in rows):
            fail("relief_support", f"expected relief support in a branch: {_summarize_rows(rows)}")
    if "cancellation_support" in expectations:
        if not any(float(r.get("branch_internal_cancellation_support", 0.0) or 0.0) > 0.50 for r in rows):
            fail("cancellation_support", f"expected cancellation support in a branch: {_summarize_rows(rows)}")
    if "quotient_support" in expectations:
        if not any(int(r.get("quotient_resolved_rival_count", 0) or 0) > 0 or int(r.get("quotient_share_count", 1) or 1) > 1 for r in rows):
            fail("quotient_support", f"expected quotient support in rows: {_summarize_rows(rows)}")
    if "no_unresolved_rivalry" in expectations:
        if any(int(r.get("unresolved_rival_count", 0) or 0) > 0 for r in rows):
            fail("no_unresolved_rivalry", f"equivalence should not create unresolved rivalry: {_summarize_rows(rows)}")
    if "resolver_outranks_carrier" in expectations:
        resolver = None
        carrier = None
        for row in rows:
            if any(float(row.get(k, 0.0) or 0.0) > 0.50 for k in ("branch_internal_exposure_support", "branch_internal_relief_support", "branch_internal_cancellation_support")):
                resolver = str(row.get("action"))
            if float(row.get("branch_internal_raw_carry_pressure", 0.0) or 0.0) > 0.50:
                carrier = str(row.get("action"))
        if not resolver or not carrier:
            fail("resolver_outranks_carrier", f"could not identify resolver/carrier: {_summarize_rows(rows)}")
        elif str(commit.get("action")) != resolver:
            fail("resolver_outranks_carrier", f"expected resolver {resolver} to be selected over carrier {carrier}, got {commit.get('action')}")
        else:
            resolver_dom = float(_assessment(commit, resolver).get("dominance_score", 0.0) or 0.0)
            carrier_dom = float(_assessment(commit, carrier).get("dominance_score", 0.0) or 0.0)
            if resolver_dom <= carrier_dom:
                fail("resolver_outranks_carrier", f"resolver selected but dominance score did not exceed carrier: {resolver_dom} <= {carrier_dom}")
    return failures


def _watchpoints(case_name: str, rows: Sequence[Mapping[str, Any]], commit: Mapping[str, Any], declared: Sequence[str]) -> List[str]:
    out = list(declared)
    selected = str(commit.get("action"))
    row = _by_action(rows).get(selected, {})
    ass = _assessment(commit, selected)
    if (
        selected
        and float(ass.get("certificate_blocks_dominance", 0.0) or 0.0) >= 0.5
        and commit.get("canonical_commitment_mode") == "stable_continuation"
    ):
        out.append("selected_branch_has_dominance_blocked_certificate_but_still_wins_stable_continuation")
    if row and list(row.get("collapse_blockers", []) or []) and commit.get("canonical_commitment_mode") == "stable_continuation":
        out.append("stable_continuation_can_select_branch_with_active_certificate_blockers")
    return list(dict.fromkeys(out))


def _run_case(name: str, spec: Mapping[str, Any]) -> Dict[str, Any]:
    candidates = [dict(c) for c in spec["candidates"]]
    rows, commit = _run_candidate_commitment(candidates, f"microcase:{name}")
    stripped_rows, stripped_commit = _run_candidate_commitment(_strip_public_effects(candidates), f"microcase:{name}:stripped")
    failures = _check_expectations(name, spec.get("expect", []), rows, stripped_rows, commit)
    watchpoints = _watchpoints(name, rows, commit, spec.get("watchpoints", []))
    tel = _telemetry(rows)
    return {
        "case": name,
        "status": "FAIL" if failures else ("PASS_WITH_WATCHPOINTS" if watchpoints else "PASS"),
        "expectations": list(spec.get("expect", [])),
        "failures": failures,
        "watchpoints": watchpoints,
        "relations_by_type": _relations_by_type(rows),
        "telemetry": {
            "relations_total": int(tel.get("relations_total", 0) or 0),
            "branch_internal_operation_rows": int(tel.get("branch_internal_operation_rows", 0) or 0),
            "branch_internal_hiddenness_pressure_total": float(tel.get("branch_internal_hiddenness_pressure_total", 0.0) or 0.0),
            "branch_internal_resolver_support_total": float(tel.get("branch_internal_resolver_support_total", 0.0) or 0.0),
        },
        "commitment": {
            "action": commit.get("action"),
            "mode": commit.get("canonical_commitment_mode"),
            "reason": commit.get("canonical_commitment_reason"),
            "assessment": _rounded_assessment(commit),
        },
        "stripped_commitment": {
            "action": stripped_commit.get("action"),
            "mode": stripped_commit.get("canonical_commitment_mode"),
        },
        "field_delta_l1_vs_stripped": _field_delta(rows, stripped_rows),
        "rows": _summarize_rows(rows),
    }


def main() -> Dict[str, Any]:
    cases = [_run_case(name, spec) for name, spec in _cases().items()]
    aggregate = {
        "cases": len(cases),
        "passed": sum(1 for c in cases if c["status"] == "PASS"),
        "passed_with_watchpoints": sum(1 for c in cases if c["status"] == "PASS_WITH_WATCHPOINTS"),
        "failed": sum(1 for c in cases if c["status"] == "FAIL"),
        "cases_with_field_delta": sum(1 for c in cases if float(c.get("field_delta_l1_vs_stripped", 0.0) or 0.0) > 0.01),
        "selected_blocked_stable_continuation_watchpoints": sum(
            1 for c in cases for w in c.get("watchpoints", []) if w == "selected_branch_has_dominance_blocked_certificate_but_still_wins_stable_continuation"
        ),
    }
    result = {
        "study": "structural_microcase_probe_v1",
        "claim_boundary": "synthetic structural microcases only; not reward evidence, not generality evidence, not novelty proof",
        "aggregate": aggregate,
        "cases": cases,
        "interpretation": {
            "positive": [
                "weak decision-slot competition is separated from branch-internal burden carriers",
                "hiddenness without exposure blocks dominance-style collapse",
                "exposure, relief, cancellation, and equivalence are recognized as structural relations/carriers",
                "under equal local evidence, resolver branches outrank burden-carrying branches in the tested microcases",
            ],
            "watchpoint": [
                "certificate-aware stable_continuation now redirects comparable blocked branches to unblocked alternatives; overwhelming-support controls are covered by structural_continuation_gating_probe_v1",
            ],
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    return result


if __name__ == "__main__":
    data = main()
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "aggregate": data["aggregate"]}, indent=2, sort_keys=True))
