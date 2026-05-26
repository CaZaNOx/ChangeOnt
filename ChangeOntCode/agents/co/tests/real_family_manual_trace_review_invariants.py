"""Invariant wrapper for the real-family manual structural trace review."""
from __future__ import annotations

from experiments.studies.real_family_manual_trace_review_v1 import main


def test_real_family_manual_trace_review_has_no_hard_watchpoints() -> None:
    payload = main()
    summary = payload["summary"]
    assert summary["cases"] >= 15
    assert set(summary["cases_by_family"]) >= {"bandit", "renewal", "maze", "maintenance", "latent_mechanism"}
    assert summary["watchpoints_by_type"] == {}
    assert summary["families_with_relation_telemetry"].get("maintenance", 0) >= 1
    assert summary["families_with_relation_telemetry"].get("latent_mechanism", 0) >= 1
