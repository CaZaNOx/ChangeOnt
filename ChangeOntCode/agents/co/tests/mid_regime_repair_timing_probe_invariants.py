from __future__ import annotations

"""Invariant wrapper for the mid-regime repair-timing probe."""

from experiments.studies.mid_regime_repair_timing_probe_v1 import main


def test_mid_regime_repair_timing_probe_runs_after_shape_gauged_law() -> None:
    result = main()
    adapter = result["summary"]["adapter_sweep"]
    synth = result["summary"]["synthetic_pressure_matrix"]
    assert adapter["cases"] > 0
    assert synth["cases"] > 0
    # After the shape-gauged pre-blocking resolver timing update, the previously
    # exposed high-risk RUN-through-carrier-burden cases should be eliminated in
    # this structural probe.  This is not reward evidence; it only guards the
    # generic relation/shape law that replaced the earlier open boundary.
    assert adapter["high_risk_run_case_count"] == 0
    # The synthetic matrix must still contain both resolver and carrier choices;
    # otherwise the update would have become a universal resolver bonus.
    selected = synth["selected_actions"]
    assert selected.get("REPAIR", 0) > 0
    assert selected.get("RUN", 0) > 0
