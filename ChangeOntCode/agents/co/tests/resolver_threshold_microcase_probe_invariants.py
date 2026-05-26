from __future__ import annotations

"""Invariant wrapper for resolver-threshold microcase probe v1."""

from experiments.studies.resolver_threshold_microcase_probe_v1 import main


def test_resolver_threshold_microcases_have_no_watchpoints() -> None:
    result = main()
    assert result["summary"]["watchpoint_count"] == 0
    inv = result["summary"]["invariants"]
    assert inv["resolver_requirement_scales_up_with_carrier_pressure"]
    assert inv["noise_floor_0_079_does_not_switch_high_carrier"]
    assert inv["bare_floor_0_08_does_not_switch_high_carrier"]
    assert inv["medium_resolver_switches_high_carrier"]
    assert inv["transform_transfer_do_not_count_as_resolvers"]
    assert inv["canonical_resolver_operations_can_switch"]
