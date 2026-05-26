"""Invariants for the real-adapter certificate-gating review diagnostic."""
from __future__ import annotations

from experiments.studies.real_adapter_certificate_gating_review_v1 import main


def test_real_adapter_certificate_gating_review_preserves_standard_samples() -> None:
    payload = main()
    standard = payload["standard_sample_summary"]
    assert standard["cases"] == 5
    assert standard["stable_selected_blocked_with_unblocked_alternative_without_switch"] == 0
    assert standard["reopen_or_sample_selected_blocked_despite_unblocked_resolver_watchpoints"] == 0
    assert not standard["watchpoints_by_type"]


def test_real_adapter_certificate_gating_review_exercises_resolver_aware_sampling_sweep() -> None:
    payload = main()
    summary = payload["summary"]
    assert summary["cases"] > 5
    assert summary["certificate_aware_reopen_or_sample_applied_cases"] > 0
    assert summary["stable_selected_blocked_with_unblocked_alternative_without_switch"] == 0
    assert summary["reopen_or_sample_selected_blocked_despite_unblocked_resolver_watchpoints"] == 0
    assert not summary["watchpoints_by_type"]


if __name__ == "__main__":
    test_real_adapter_certificate_gating_review_preserves_standard_samples()
    test_real_adapter_certificate_gating_review_exercises_resolver_aware_sampling_sweep()
