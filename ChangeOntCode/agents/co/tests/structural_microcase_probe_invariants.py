"""Invariants for targeted structural microcases.

These are structural checks only.  They protect the current relation/certificate
semantics from drifting back into weak-competition telemetry or scalar-only
collapse, but they do not assert reward performance.
"""

from __future__ import annotations

from experiments.studies.structural_microcase_probe_v1 import main


def test_targeted_structural_microcases_pass_or_watchpoint_only() -> None:
    result = main()
    aggregate = result["aggregate"]
    assert aggregate["failed"] == 0, result
    assert aggregate["cases"] >= 7, result
    assert aggregate["cases_with_field_delta"] >= 4, result


def test_microcases_do_not_select_comparable_blocked_branch_under_stable_continuation() -> None:
    result = main()
    aggregate = result["aggregate"]
    assert aggregate["selected_blocked_stable_continuation_watchpoints"] == 0, result
