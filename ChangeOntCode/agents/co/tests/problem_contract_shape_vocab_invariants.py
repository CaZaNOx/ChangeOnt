"""Invariants for public problem-contract vocabulary used by shape derivation.

The shape prior must not silently collapse legitimate public contract vocabulary
such as ``drift=none`` or ``commitment_cost=medium_to_high`` to ``unknown``.
That kind of vocabulary mismatch is not a family-specific policy issue; it
corrupts the public regime before the kernel receives it.
"""

from __future__ import annotations

from agents.co.core.contracts.problem_contract import normalize_problem_contract
from agents.co.placement.shape_prior6 import derive_shape_prior6


def test_extended_drift_and_commitment_cost_survive_normalization() -> None:
    problem = normalize_problem_contract({
        "actions": {"count": 2, "native_type": "discrete", "labels": ["a", "b"]},
        "timescale_profile": {"horizon_fixity": "fixed", "drift": "none"},
        "observability_profile": {"state": "partial", "outcome": "direct", "constraints": "direct"},
        "reversibility_profile": {"action_reversibility": "partly_reversible", "commitment_cost": "medium_to_high"},
        "mutable_factors": ["public_relation_change"],
    })
    assert problem["timescale_profile"]["drift"] == "none"
    assert problem["reversibility_profile"]["commitment_cost"] == "medium_to_high"


def test_extended_vocabulary_changes_shape_without_hidden_policy() -> None:
    base = {
        "actions": {"count": 2, "native_type": "discrete", "labels": ["a", "b"]},
        "timescale_profile": {"horizon_fixity": "fixed", "drift": "none"},
        "observability_profile": {"state": "partial", "outcome": "direct", "constraints": "direct"},
        "reversibility_profile": {"action_reversibility": "partly_reversible", "commitment_cost": "medium_to_high"},
        "mutable_factors": ["public_relation_change"],
    }
    shaped = derive_shape_prior6(base)
    axes = shaped["axes"]
    raw = shaped["raw_axes_before_quantization"]
    assert raw["reshapeability"] < 0.35, "drift=none should not behave like unknown/mixed drift"
    assert raw["revision_cost"] > 0.52, "medium_to_high should raise public revision-cost pressure"
    assert axes["reshapeability"] <= 0.25
    assert axes["consequence_span"] >= 0.5


if __name__ == "__main__":
    test_extended_drift_and_commitment_cost_survive_normalization()
    test_extended_vocabulary_changes_shape_without_hidden_policy()
    print("problem_contract_shape_vocab_invariants: PASS")
