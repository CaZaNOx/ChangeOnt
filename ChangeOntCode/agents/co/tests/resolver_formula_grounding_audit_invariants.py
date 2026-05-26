from __future__ import annotations

"""Invariants for resolver formula grounding audit.

These checks protect the distinction between public resolver operations and
plain action names or transform pressure. They are structural diagnostics only,
not reward/performance tests.
"""

from experiments.studies.resolver_formula_grounding_audit_v1 import main


def test_resolver_audit_runs_without_resolver_watchpoints() -> None:
    result = main()
    summary = result["summary"]
    assert summary["cases"] >= 300, result
    assert summary["watchpoints_by_type"] == {}, result
    assert summary["resolver_rows_at_threshold"] > 0, result


def test_transform_is_not_counted_as_resolver_without_explicit_resolver_op() -> None:
    result = main()
    summary = result["summary"]
    assert summary["transform_pressure_rows"] > 0, result
    assert summary["transform_only_rows_counted_as_resolver"] == 0, result
    assert summary["selected_transform_only_rows_counted_as_resolver"] == 0, result
    checks = summary["microcase_checks"]
    assert checks["transform_only_not_resolver"] is True, result
    assert checks["transform_pressure_recorded"] is True, result


def test_resolver_recognition_follows_public_ops_not_action_names() -> None:
    result = main()
    checks = result["summary"]["microcase_checks"]
    assert checks["run_named_resolver_recognized"] is True, result
    assert checks["repair_named_carrier_not_resolver"] is True, result
    assert checks["repair_named_resolver_recognized"] is True, result
    assert checks["run_named_carrier_not_resolver"] is True, result
