from __future__ import annotations

"""Invariants for the real-adapter formula sensitivity probe.

The probe must remain diagnostic only: it should expose coefficient sensitivity
without changing defaults, adding performance claims, or treating any profile as
an optimized setting.
"""

from experiments.studies.real_adapter_formula_sensitivity_probe_v1 import main


def test_real_adapter_formula_sensitivity_probe_runs_and_keeps_boundary() -> None:
    result = main()
    assert result["summary"]["cases"] >= 300
    assert "not tuning" in result["claim_boundary"]
    assert "baseline" in result["summary"]["profiles"]
    assert "permissive_comparability_wide_margins" in result["summary"]["profiles"]


def test_formula_sensitivity_has_expected_profiles() -> None:
    result = main()
    profiles = result["summary"]["profiles"]
    for name in (
        "strict_comparability_narrow_margins",
        "permissive_comparability_wide_margins",
        "low_resolver_threshold",
        "high_resolver_threshold",
        "flat_blocker_terms",
    ):
        assert name in profiles
        assert "action_changes" in profiles[name]
