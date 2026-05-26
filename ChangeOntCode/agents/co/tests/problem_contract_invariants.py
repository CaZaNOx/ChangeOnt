"""Smoke checks for the generic problem contract surface.

Run:
    python -m agents.co.tests.problem_contract_invariants
"""
from __future__ import annotations

from agents.co.integration.core_builder import build_co_core
from agents.co.adapters.bandit_adapter import COAdapterBandit
from agents.co.adapters.renewal_adapter import COAdapterRenewal
from agents.co.adapters.maze_adapter import COAdapterMaze


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def _core():
    return build_co_core({
        "header": {"type": "SSI"},
        "elements": {"candidate_surface": {"enabled": True}, "commitment_surface": {"enabled": True, "ngram_order": 0}}, "combinator": {"order": ["candidate_surface", "commitment_surface"]},
        "primitives": {"signal_bus": {}, "bandit_stats": {}, "ngram_model": {}},
    })


def _required_keys(contract):
    return {
        "schema", "actions", "observation_channels", "task_anchor", "hard_constraints",
        "soft_costs", "regime_anchors", "mutable_factors", "decision_scope", "timescale_profile",
        "observability_profile", "reversibility_profile", "notes", "source", "status",
    }


def main() -> None:
    # bandit with one arm-count variant
    bandit = COAdapterBandit(_core(), n_arms=5)
    bandit.select({"family": "bandit", "t": 0, "n_arms": 5})
    b_contract = dict((bandit._last_obs or {}).get("problem_contract", {}))

    renewal = COAdapterRenewal(_core())
    renewal.select({"family": "renewal", "t": 0, "A": 4, "obs": 1, "L_win": 2})
    r_contract = dict((renewal._last_obs or {}).get("problem_contract", {}))

    maze = COAdapterMaze(_core())
    maze.select({"family": "maze", "t": 0, "pos": [0, 0], "goal": [0, 1], "width": 2, "height": 1, "grid": [[0, 0]]})
    m_contract = dict((maze._last_obs or {}).get("problem_contract", {}))

    req = _required_keys(b_contract)
    _assert(set(b_contract.keys()) == req, "bandit problem contract keys mismatch")
    _assert(set(r_contract.keys()) == req, "renewal problem contract keys mismatch")
    _assert(set(m_contract.keys()) == req, "maze problem contract keys mismatch")

    _assert(b_contract["actions"]["count"] == 5, "bandit variant should preserve adapter plug-and-play over action count")
    _assert(r_contract["task_anchor"]["kind"] == "predictive_reward_alignment", "renewal task anchor missing")
    _assert("illegal_move_blocked" in m_contract["hard_constraints"], "maze hard constraint missing")


if __name__ == "__main__":
    main()
