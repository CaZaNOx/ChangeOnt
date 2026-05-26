"""Invariants for the current-kernel diagnostic map.

Run with: python -m agents.co.tests.current_kernel_diagnostic_map_invariants
"""

from __future__ import annotations

import json
from experiments.studies.current_kernel_diagnostic_map_v1 import SUMMARY_JSON, TASKS, VARIANTS, SEEDS, main


def test_current_kernel_diagnostic_map_completes_and_is_claim_bounded() -> None:
    if not SUMMARY_JSON.exists():
        main()
    data = json.loads(SUMMARY_JSON.read_text(encoding="utf-8"))
    expected = len(TASKS) * len(SEEDS) * len(VARIANTS)
    assert data.get("study") == "current_kernel_diagnostic_map_v1"
    assert data.get("runs_attempted") == expected
    assert data.get("runs_succeeded") == expected
    assert data.get("runs_failed") == 0
    boundary = str(data.get("claim_boundary", "")).lower()
    assert "not a benchmark" in boundary
    assert "not co proof" in boundary
    assert "not novelty evidence" in boundary
    assert "full_current" in data.get("variants", {})
    assert "static_shape" in data.get("variants", {})
    assert "no_quotient" in data.get("variants", {})
    assert "no_scheduler" in data.get("variants", {})
    assert "no_sequence" in data.get("variants", {})


def test_current_kernel_diagnostic_map_has_mechanism_visibility_comparisons() -> None:
    if not SUMMARY_JSON.exists():
        main()
    data = json.loads(SUMMARY_JSON.read_text(encoding="utf-8"))
    comparisons = list(data.get("comparisons", []) or [])
    assert comparisons
    assert any(str(c.get("ablation")) == "static_shape" and int(c.get("dynamic_shape_step_delta_vs_full", 0)) < 0 for c in comparisons)
    assert any(str(c.get("ablation")) == "no_scheduler" and float(c.get("avg_recursion_demand_delta_vs_full", 0.0)) < 0 for c in comparisons)
    assert any(str(c.get("ablation")) == "no_quotient" and float(c.get("avg_quotient_rows_delta_vs_full", 0.0)) < 0 for c in comparisons)
    assert any(str(c.get("ablation")) == "no_sequence" and float(c.get("avg_sequence_rows_delta_vs_full", 0.0)) < 0 for c in comparisons)


if __name__ == "__main__":
    test_current_kernel_diagnostic_map_completes_and_is_claim_bounded()
    test_current_kernel_diagnostic_map_has_mechanism_visibility_comparisons()
    print("current_kernel_diagnostic_map_invariants passed")
