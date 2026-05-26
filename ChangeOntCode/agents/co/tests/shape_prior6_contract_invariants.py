"""Basic invariants for the 6-question shape prior contract.

Run:
    python -m agents.co.tests.shape_prior6_contract_invariants
"""
from __future__ import annotations

from agents.co.core.contracts.placement_contract import build_runtime_contract
from agents.co.placement.shape_prior6 import derive_shape_prior6, SHAPE_PRIOR6_AXES, SHAPE_SCORE_VALUES


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def main() -> None:
    problem = {
        "actions": {"count": 4, "labels": ["UP", "DOWN", "LEFT", "RIGHT"]},
        "observation_channels": ["visible_position", "visible_goal", "legality_geometry"],
        "task_anchor": {"kind": "goal_reach", "provided_externally": True},
        "hard_constraints": ["wall_blockage", "bounds"],
        "timescale_profile": {"horizon_fixity": "fixed", "drift": "fixed"},
        "observability_profile": {"state": "direct", "outcome": "direct", "constraints": "direct"},
        "reversibility_profile": {"action_reversibility": "partly_reversible", "commitment_cost": "medium"},
    }
    prior = derive_shape_prior6(problem)
    _assert(set(prior["axes"].keys()) == set(SHAPE_PRIOR6_AXES), "shape prior axes mismatch")
    _assert(set(prior["axes"].values()).issubset(set(SHAPE_SCORE_VALUES)), "shape scores must use canonical five-point values")
    contract = build_runtime_contract({"problem_contract": problem, "shape_prior6": prior})
    _assert("shape_prior6" in contract, "runtime contract lost shape_prior6")
    _assert("environment_basis" not in contract, "environment_basis must not be an active runtime-contract key")
    _assert(contract["direct_controls"]["source"] == "shape_prior6_direct_projection", "direct controls must be projected directly from shape_prior6")
    _assert("legacy_placement" not in contract, "retired placement payloads must not be exposed in certified runtime contract")

    derived_contract = build_runtime_contract({"problem_contract": problem})
    _assert(derived_contract["shape_prior6"]["source"] == "problem_contract_questionnaire", "runtime contract should derive shape_prior6 from problem_contract when absent")
    _assert(derived_contract["direct_controls"]["source"] == "shape_prior6_direct_projection", "derived shape must drive direct controls")


if __name__ == "__main__":
    main()
