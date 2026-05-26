"""Minimal coherence tests for the canonical runtime contract surface.

Run:
    python -m agents.co.tests.runtime_contract_invariants
"""
from __future__ import annotations

from agents.co.core.contracts.placement_contract import build_runtime_contract, contract_is_declared
from agents.co.integration.core_builder import build_co_core
from agents.co.placement.shape_prior6 import SHAPE_PRIOR6_AXES, SHAPE_SCORE_VALUES


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def _problem():
    return {
        "actions": {"count": 3, "native_type": "discrete", "labels": ["a0", "a1", "a2"]},
        "observation_channels": ["reward_feedback", "trace_history"],
        "task_anchor": {"kind": "reward_maximization", "provided_externally": True},
        "regime_anchors": ["action_identities"],
        "mutable_factors": ["candidate_goal_relation"],
        "timescale_profile": {"horizon_fixity": "fixed"},
        "observability_profile": {"state": "partial", "outcome": "direct"},
        "reversibility_profile": {"action_reversibility": "reversible", "commitment_cost": "medium"},
    }


def main() -> None:
    problem = dict(_problem())
    problem["decision_scope"] = "hypothesis_over_anchor"
    contract = build_runtime_contract({
        "kernel_posture": {"name": "late_hardening", "enabled": True, "authority": "study_override", "axes": {"hardening_bias": 0.2}},
        "problem_contract": problem,
    })
    _assert(contract["problem_contract"]["decision_scope"] == "hypothesis_over_anchor", "explicit problem scope should be retained")
    _assert(set(contract["shape_prior6"]["axes"]) == set(SHAPE_PRIOR6_AXES), "shape axes missing")
    _assert(set(contract["shape_prior6"]["axes"].values()).issubset(set(SHAPE_SCORE_VALUES)), "shape scores not quantized")
    _assert(contract["direct_controls"]["source"] == "shape_prior6_direct_projection", "direct controls should be shape-derived")
    _assert(contract["study_overrides"]["kernel_posture"]["name"] == "late_hardening", "study override posture lost")
    _assert("legacy_placement" not in contract, "retired placement payloads must not be exposed in certified runtime contract")
    _assert("environment_basis" not in contract, "environment_basis must not be an active runtime-contract key")
    _assert("primitive_closure_fields" not in contract, "primitive closure fields must not be an active runtime-contract key")
    _assert(contract_is_declared(contract), "declared contract should count as declared")

    core = build_co_core({
        "header": {"type": "SSI"},
        "elements": {"commitment_surface": {"enabled": True, "ngram_order": 0}},
        "primitives": {"signal_bus": {}},
        "problem_contract": {**_problem(), "actions": {"count": 2, "native_type": "discrete", "labels": ["left", "right"]}},
    })
    exported = core.export_runtime_contract()
    _assert(exported["problem_contract"]["actions"]["count"] == 2, "core export lost problem contract")
    _assert(set(exported["shape_prior6"]["axes"]) == set(SHAPE_PRIOR6_AXES), "core export lost shape prior")
    _assert(exported["direct_controls"]["source"] == "shape_prior6_direct_projection", "core export lost direct controls")
    _assert("environment_basis" not in exported, "core export must not expose active environment_basis")


if __name__ == "__main__":
    main()
