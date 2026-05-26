from __future__ import annotations

"""Invariant wrapper for DynamicShapeField real-trace ablation v1."""

from experiments.studies.dynamic_shape_real_trace_ablation_v1 import main


def test_dynamic_shape_real_trace_ablation_visible() -> None:
    result = main()
    inv = result["summary"]["invariants"]
    assert inv["dynamic_shape_state_updates_from_public_trace"]
    assert inv["dynamic_shape_ablation_is_visible"]
    assert inv["no_behavior_change_is_allowed_and_reported"]
