from __future__ import annotations

"""Invariant wrapper for shape-gauged resolver timing probe v1."""

from experiments.studies.shape_gauged_resolver_timing_probe_v1 import main


def test_shape_gauged_resolver_timing_is_shape_and_relation_dependent() -> None:
    result = main()
    inv = result["summary"]["invariants"]
    assert inv["low_urgency_does_not_force_resolver"]
    assert inv["high_urgency_allows_resolver_timing"]
    assert inv["transform_transfer_do_not_count_as_resolvers"]
