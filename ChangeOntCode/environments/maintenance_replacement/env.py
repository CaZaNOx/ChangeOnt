from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
import random

ACTIONS: List[str] = ["RUN", "INSPECT", "REPAIR", "REPLACE", "WAIT"]


@dataclass
class MaintenanceSpec:
    """Small controlled maintenance/replacement MDP.

    Health is 0..max_health. Running earns reward but may degrade health or fail.
    Repair/replacement restore health at cost. Observation may hide true health.
    """

    max_health: int = 4
    horizon: int = 80
    seed: int = 0
    degradation_prob: float = 0.20
    extra_degrade_when_low: float = 0.10
    failure_health: int = 0
    failure_penalty: float = 8.0
    run_reward: float = 1.0
    inspect_cost: float = 0.10
    repair_cost: float = 0.70
    replace_cost: float = 1.80
    wait_cost: float = 0.05
    repair_boost: int = 2
    wait_recovery_prob: float = 0.00
    observe_health: str = "partial"  # direct | partial | hidden
    observation_noise: float = 0.20
    reset_on_failure: bool = False
    start_health: Optional[int] = None

    @staticmethod
    def bandit_like(seed: int = 0) -> "MaintenanceSpec":
        return MaintenanceSpec(
            seed=seed,
            horizon=60,
            degradation_prob=0.02,
            extra_degrade_when_low=0.00,
            failure_penalty=2.0,
            repair_cost=1.5,
            replace_cost=3.0,
            wait_recovery_prob=0.00,
            observe_health="direct",
            observation_noise=0.0,
        )

    @staticmethod
    def middle(seed: int = 0) -> "MaintenanceSpec":
        return MaintenanceSpec(
            seed=seed,
            horizon=80,
            degradation_prob=0.18,
            extra_degrade_when_low=0.10,
            failure_penalty=7.0,
            repair_cost=0.8,
            replace_cost=2.0,
            wait_recovery_prob=0.08,
            observe_health="partial",
            observation_noise=0.20,
        )

    @staticmethod
    def renewal_like(seed: int = 0) -> "MaintenanceSpec":
        return MaintenanceSpec(
            seed=seed,
            horizon=100,
            degradation_prob=0.35,
            extra_degrade_when_low=0.20,
            failure_penalty=12.0,
            repair_cost=0.9,
            replace_cost=2.4,
            wait_recovery_prob=0.15,
            observe_health="hidden",
            observation_noise=0.35,
            reset_on_failure=True,
        )


class MaintenanceReplacementEnv:
    def __init__(self, spec: MaintenanceSpec):
        self.spec = spec
        self.rng = random.Random(spec.seed)
        self.reset(seed=spec.seed)

    def reset(self, seed: Optional[int] = None) -> Tuple[Dict[str, Any], float, bool, Dict[str, Any]]:
        if seed is not None:
            self.rng = random.Random(int(seed))
        self.t = 0
        self.done = False
        self.health = int(self.spec.start_health if self.spec.start_health is not None else self.spec.max_health)
        self.last_action: Optional[str] = None
        self.last_event = "start"
        self.last_reward = 0.0
        self.inspected_health: Optional[int] = None
        self.inspected_at: Optional[int] = None
        self.history: List[Dict[str, Any]] = []
        return self.get_observation(), 0.0, False, self._info()

    def legal_actions(self) -> List[str]:
        return list(ACTIONS)

    def _maybe_degrade(self) -> int:
        low_factor = max(0.0, 1.0 - float(self.health) / float(max(1, self.spec.max_health)))
        p = min(1.0, max(0.0, self.spec.degradation_prob + self.spec.extra_degrade_when_low * low_factor))
        if self.rng.random() < p:
            self.health = max(0, self.health - 1)
            return 1
        return 0

    def _maybe_recover_wait(self) -> int:
        if self.rng.random() < max(0.0, min(1.0, self.spec.wait_recovery_prob)):
            old = self.health
            self.health = min(self.spec.max_health, self.health + 1)
            return self.health - old
        return 0

    def step(self, action: str) -> Tuple[Dict[str, Any], float, bool, Dict[str, Any]]:
        if self.done:
            return self.get_observation(), 0.0, True, self._info()
        if action not in ACTIONS:
            action = "WAIT"
        self.t += 1
        self.last_action = action
        reward = 0.0
        event = "noop"

        if action == "RUN":
            reward += self.spec.run_reward * (float(self.health) / float(max(1, self.spec.max_health)))
            degraded = self._maybe_degrade()
            event = "run_degraded" if degraded else "run"
            if self.health <= self.spec.failure_health:
                reward -= self.spec.failure_penalty
                event = "failure"
                if self.spec.reset_on_failure:
                    self.health = self.spec.max_health
                    event = "failure_reset"
        elif action == "INSPECT":
            reward -= self.spec.inspect_cost
            self.inspected_health = self.health
            self.inspected_at = self.t
            event = "inspect"
        elif action == "REPAIR":
            reward -= self.spec.repair_cost
            old = self.health
            self.health = min(self.spec.max_health, self.health + max(1, int(self.spec.repair_boost)))
            event = "repair" if self.health > old else "repair_noop"
        elif action == "REPLACE":
            reward -= self.spec.replace_cost
            self.health = self.spec.max_health
            event = "replace"
        elif action == "WAIT":
            reward -= self.spec.wait_cost
            recovered = self._maybe_recover_wait()
            event = "wait_recovered" if recovered else "wait"

        self.last_reward = float(reward)
        self.last_event = event
        self.done = self.t >= self.spec.horizon
        row = {"t": self.t, "action": action, "reward": float(reward), "event": event, "health_true": int(self.health)}
        self.history.append(row)
        return self.get_observation(), float(reward), bool(self.done), self._info()

    def _observed_health(self) -> Optional[int]:
        mode = str(self.spec.observe_health)
        if mode == "direct":
            return int(self.health)
        if mode == "hidden":
            return self.inspected_health
        # partial: noisy bucket or inspected exact value if just inspected
        if self.inspected_health is not None and self.last_action == "INSPECT":
            return int(self.inspected_health)
        noisy = self.health
        if self.rng.random() < max(0.0, min(1.0, self.spec.observation_noise)):
            noisy += self.rng.choice([-1, 1])
        return int(max(0, min(self.spec.max_health, noisy)))

    def get_observation(self) -> Dict[str, Any]:
        obs_h = self._observed_health()
        known = obs_h is not None
        health_norm = None if obs_h is None else float(obs_h) / float(max(1, self.spec.max_health))
        if str(self.spec.observe_health) == "hidden" and self.inspected_at is not None and obs_h is not None:
            observed_health_age: Optional[int] = max(0, int(self.t) - int(self.inspected_at))
        elif known:
            observed_health_age = 0
        else:
            observed_health_age = None
        return {
            "family": "maintenance_replacement",
            "t": int(self.t),
            "actions": list(ACTIONS),
            "observed_health": obs_h,
            "health_observed": bool(known),
            "observed_health_norm": health_norm,
            "observed_health_age": observed_health_age,
            "observed_health_fresh": bool(known and (observed_health_age in (None, 0) or str(self.spec.observe_health) != "hidden")),
            "max_health": int(self.spec.max_health),
            "last_action": self.last_action,
            "last_event": self.last_event,
            "last_reward": float(self.last_reward),
            "degradation_prob_public": float(self.spec.degradation_prob),
            "wait_recovery_prob_public": float(self.spec.wait_recovery_prob),
            "repair_cost_public": float(self.spec.repair_cost),
            "replace_cost_public": float(self.spec.replace_cost),
            "failure_penalty_public": float(self.spec.failure_penalty),
            "observation_noise_public": float(self.spec.observation_noise),
            "observe_health_mode": str(self.spec.observe_health),
            "horizon": int(self.spec.horizon),
        }

    def _info(self) -> Dict[str, Any]:
        return {
            "health_true": int(self.health),
            "last_event": self.last_event,
            "last_reward": float(self.last_reward),
        }
