"""Smoke invariants for the maintenance/replacement family.

Run:
    python -m agents.co.tests.maintenance_replacement_family_invariants
"""
from __future__ import annotations

from agents.co.integration.core_builder import build_co_core
from agents.co.adapters.maintenance_replacement_adapter import COAdapterMaintenanceReplacement
from agents.co.placement.shape_prior6 import derive_shape_prior6, SHAPE_SCORE_VALUES
from environments.maintenance_replacement.env import MaintenanceReplacementEnv, MaintenanceSpec, ACTIONS


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def _core():
    return build_co_core({
        "header": {"type": "SSI"},
        "elements": {
            "haq": {"enabled": True, "history_len": 8, "ema_alpha": 0.2},
            "candidate_surface": {"enabled": True},
            "router": {"enabled": True},
            "commitment_surface": {"enabled": True, "eps_on_cycle": 0.02, "ngram_order": 0},
        },
        "combinator": {"order": ["haq", "candidate_surface", "router", "commitment_surface"]},
        "primitives": {"signal_bus": {}, "P2": {}, "P4": {}, "P16": {}},
    })


def _contract_for(spec):
    env = MaintenanceReplacementEnv(spec)
    obs, _, _, _ = env.reset(seed=spec.seed)
    agent = COAdapterMaintenanceReplacement(_core())
    return agent._problem_contract(obs)  # explicit adapter contract audit


def main() -> None:
    contracts = {
        "bandit_like": _contract_for(MaintenanceSpec.bandit_like(seed=0)),
        "middle": _contract_for(MaintenanceSpec.middle(seed=0)),
        "renewal_like": _contract_for(MaintenanceSpec.renewal_like(seed=0)),
    }
    shapes = {k: derive_shape_prior6(v)["axes"] for k, v in contracts.items()}
    for name, axes in shapes.items():
        _assert(set(axes.values()).issubset(set(SHAPE_SCORE_VALUES)), f"{name} shape not quantized")
        _assert(set(axes) == {"hidden_decisiveness", "reshapeability", "local_cue_reliability", "revision_cost", "consequence_span", "topology_constraint"}, f"{name} shape axes mismatch")
    _assert(shapes["renewal_like"]["reshapeability"] >= shapes["bandit_like"]["reshapeability"], "renewal-like should not be less reshapeable than bandit-like")
    _assert(shapes["renewal_like"]["hidden_decisiveness"] >= shapes["bandit_like"]["hidden_decisiveness"], "renewal-like should not be less hidden-decisive than bandit-like")

    env = MaintenanceReplacementEnv(MaintenanceSpec.middle(seed=1))
    obs, _, done, _ = env.reset(seed=1)
    agent = COAdapterMaintenanceReplacement(_core())
    for _ in range(5):
        sel = agent.select(obs)
        action = str(sel.get("action"))
        _assert(action in ACTIONS, f"CO action outside maintenance action set: {action}")
        _assert(int(sel.get("signal_bus_votes", 0) or 0) > 0, "maintenance CO path must publish candidate-surface votes before commitment")
        obs, reward, done, info = env.step(action)
        agent.update({"action": action, "reward": float(reward), "done": bool(done), "info": dict(info)})
        controls = getattr(agent.core.header, "state", None)
        _assert(controls is not None, "core header state missing after maintenance update")
        _assert(float(getattr(controls, "local_authority", 0.5)) != 0.5 or float(getattr(controls, "nonlocal_authority", 0.5)) != 0.5, "packet problem_contract must drive non-default six-question controls")
        if done:
            break


if __name__ == "__main__":
    main()
