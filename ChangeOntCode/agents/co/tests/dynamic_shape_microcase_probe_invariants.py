from __future__ import annotations

"""Invariant wrapper for DynamicShapeField microcase probe v1."""

from experiments.studies.dynamic_shape_microcase_probe_v1 import main


def test_dynamic_shape_microcases_pass() -> None:
    result = main()
    assert result["summary"]["all_passed"]
