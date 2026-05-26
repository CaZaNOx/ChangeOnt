"""Active-path invariants for canonical six-question placement.

Run:
    python -m agents.co.tests.shape_prior6_active_path_invariants
"""
from __future__ import annotations

from agents.co.core.contracts.placement_contract import build_runtime_contract
from agents.co.placement.control import direct_kernel_controls_from_shape
from agents.co.placement.shape_prior6 import SHAPE_PRIOR6_AXES


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def _problem():
    return {
        "actions": {"count": 3, "labels": ["run", "inspect", "repair"]},
        "observation_channels": ["public_state", "public_reward", "legal_actions"],
        "task_anchor": {"kind": "cost_uptime_tradeoff", "provided_externally": True},
        "hard_constraints": ["legal_action_only"],
        "mutable_factors": ["health_state", "failure_risk"],
        "timescale_profile": {"horizon_fixity": "mixed", "drift": "slow"},
        "observability_profile": {"state": "partial", "outcome": "direct", "constraints": "direct"},
        "reversibility_profile": {"action_reversibility": "partly_reversible", "commitment_cost": "medium"},
    }


def main() -> None:
    contract = build_runtime_contract({"problem_contract": _problem()})
    _assert(set(contract["shape_prior6"]["axes"]) == set(SHAPE_PRIOR6_AXES), "shape_prior6 axes missing")
    _assert(contract["shape_prior6"]["source"] == "problem_contract_questionnaire", "shape must be derived from public problem contract")
    _assert(contract["direct_controls"]["source"] == "shape_prior6_direct_projection", "direct controls must be shape-driven")
    _assert("environment_basis" not in contract, "active runtime contract must not expose environment_basis")

    low = {k: 0.25 for k in SHAPE_PRIOR6_AXES}
    high = dict(low)
    high["consequence_span"] = 1.0
    high["hidden_decisiveness"] = 1.0
    c_low = direct_kernel_controls_from_shape(low)
    c_high = direct_kernel_controls_from_shape(high)
    _assert(c_high["nonlocal_authority"] > c_low["nonlocal_authority"], "higher hidden/consequence shape should raise nonlocal authority")
    _assert(c_high["collapse_admissibility"] < c_low["collapse_admissibility"], "higher hidden/consequence shape should reduce collapse admissibility")


if __name__ == "__main__":
    main()
