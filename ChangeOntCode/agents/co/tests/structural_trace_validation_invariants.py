"""Invariants for structural trace validation summaries and watchpoint counts."""
from __future__ import annotations

"""Structural trace validation invariants.

These are diagnostic invariants, not reward benchmarks.  They ensure the
real-trace validation study can inspect the public-effect -> RelationSurface ->
RCF -> CollapseCertificate -> Commitment path and that weak decision-slot
competition remains separated from strong continuation rivalry.
"""

from experiments.studies.structural_trace_validation_v1 import _case_candidates, _case_trace, _formula_scan


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def test_structural_trace_cases_have_certificate_and_assessment() -> None:
    cases = _case_candidates()
    _assert(len(cases) >= 5, "expected representative adapter cases")
    for name, candidates in cases.items():
        trace = _case_trace(name, candidates)
        _assert(trace["candidate_rows"] > 0, f"{name}: missing candidate rows")
        selected = trace["commitment"]["selected_on"]
        _assert(bool(selected), f"{name}: missing selected-row structural trace")
        _assert("certificate" in selected, f"{name}: selected row missing collapse certificate")
        _assert("commitment_assessment" in selected, f"{name}: selected row missing commitment assessment")


def test_weak_decision_competition_is_not_strong_rivalry() -> None:
    cases = _case_candidates()
    traces = [_case_trace(name, candidates) for name, candidates in cases.items()]
    total_weak = sum(t["weak_decision_competition_relations"] for t in traces)
    total_strong = sum(int(t["relations_by_type"].get("rivalry", 0) or 0) for t in traces)
    _assert(total_weak > 0, "expected weak decision-slot competition to be logged")
    _assert(total_strong == 0, "weak decision-slot competition must not be counted as strong rivalry in sampled traces")
    for t in traces:
        selected = t["commitment"]["selected_on"]
        blockers = selected.get("certificate", {}).get("blockers", []) if selected else []
        if int(t["relations_by_type"].get("rivalry", 0) or 0) == 0:
            _assert("unresolved_non_equivalent_rival" not in blockers, f"{t['family']}: weak competition became unresolved-rival blocker")


def test_formula_scan_remains_explicitly_provisional() -> None:
    scan = _formula_scan()
    _assert(scan["formula_coefficient_lines"] > 0, "formula scan should detect active weighted formulas")
    _assert(scan["status"] in {"PASS_WITH_WATCHPOINTS", "NEEDS_LEDGER_EXPANSION"}, "formula scan status should be diagnostic")


def main() -> None:
    test_structural_trace_cases_have_certificate_and_assessment()
    test_weak_decision_competition_is_not_strong_rivalry()
    test_formula_scan_remains_explicitly_provisional()
    print("structural_trace_validation_invariants passed")


if __name__ == "__main__":
    main()
