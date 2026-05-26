"""Invariants for maintenance/replacement classical/STOA baselines.

Run:
    python -m agents.co.tests.maintenance_replacement_stoa_baseline_invariants
"""
from __future__ import annotations

from experiments.baselines.maintenance_replacement import (
    FiniteHorizonDPMaintenancePolicy,
    make_maintenance_policy,
)
from experiments.runners.maintenance_replacement_runner import run_episode, spec_from_name
from environments.maintenance_replacement.env import ACTIONS, MaintenanceReplacementEnv, MaintenanceSpec


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def _first_action(policy, spec):
    env = MaintenanceReplacementEnv(spec)
    obs, _, _, _ = env.reset(seed=spec.seed)
    return str(policy.select(obs))


def main() -> None:
    for regime in ("bandit_like", "middle", "renewal_like"):
        spec = spec_from_name(regime, 0)
        for kind in ("random", "threshold", "threshold_opt", "q_learning"):
            policy = make_maintenance_policy(kind, spec, seed=0)
            action = _first_action(policy, spec)
            _assert(action in ACTIONS, f"{kind}/{regime} produced illegal action {action}")
            result = run_episode(regime=regime, agent_kind=kind, seed=0)
            _assert(result["steps"] == spec.horizon, f"{kind}/{regime} did not run expected horizon")
            _assert(isinstance(result["total_reward"], float), f"{kind}/{regime} reward not numeric")

    direct_spec = MaintenanceSpec.bandit_like(seed=0)
    dp = FiniteHorizonDPMaintenancePolicy(direct_spec)
    _assert(_first_action(dp, direct_spec) in ACTIONS, "DP produced illegal action in direct regime")
    direct_result = run_episode(regime="bandit_like", agent_kind="finite_horizon_dp", seed=0)
    _assert(direct_result["observation_mode"] == "direct", "DP runner should only be direct-observed in this invariant")

    hidden_spec = MaintenanceSpec.renewal_like(seed=0)
    try:
        FiniteHorizonDPMaintenancePolicy(hidden_spec)
    except ValueError as exc:
        _assert("direct" in str(exc), "hidden-health DP refusal should explain direct-observation requirement")
    else:
        raise AssertionError("DP baseline must refuse hidden-health regime rather than becoming an oracle")

    env = MaintenanceReplacementEnv(hidden_spec)
    obs, _, _, info = env.reset(seed=0)
    _assert(obs.get("observed_health") is None, "hidden-health initial observation exposed health")
    _assert("health_true" in info, "env info may log hidden health after transition for diagnostics")


if __name__ == "__main__":
    main()
