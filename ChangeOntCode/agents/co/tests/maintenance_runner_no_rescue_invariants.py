"""The maintenance runner must fail closed instead of coercing invalid actions."""
from __future__ import annotations

import pytest

import experiments.runners.maintenance_replacement_runner as runner


class BadAgent:
    def select(self, obs):
        return "INVALID_ACTION"
    def update(self, fb):
        pass


def test_maintenance_runner_rejects_invalid_agent_action_without_run_rescue(monkeypatch) -> None:
    monkeypatch.setattr(runner, "build_agent", lambda kind, seed, spec=None, co_params=None: BadAgent())
    with pytest.raises(ValueError, match="fail-closed"):
        runner.run_episode(regime="middle", agent_kind="co", seed=0)


def test_maintenance_public_baseline_evaluator_rejects_invalid_policy_without_run_rescue() -> None:
    from environments.maintenance_replacement.env import MaintenanceSpec
    from experiments.baselines.maintenance_replacement import evaluate_policy

    with pytest.raises(ValueError, match="fail-closed"):
        evaluate_policy(BadAgent(), MaintenanceSpec.middle(seed=0), seed=0)
