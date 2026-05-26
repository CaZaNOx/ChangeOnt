from __future__ import annotations

"""Public, parity-auditable baselines for maintenance/replacement MDPs.

The baselines in this module deliberately operate through the public observation
surface. Finite-horizon DP is included only for the fully observed known-model
case; it refuses hidden/partial-health regimes unless a caller explicitly labels
a separate oracle experiment elsewhere.
"""

from dataclasses import replace
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple
import random

from environments.maintenance_replacement.env import ACTIONS, MaintenanceReplacementEnv, MaintenanceSpec


def _as_float(x: Any, default: float = 0.5) -> float:
    try:
        return float(x)
    except Exception:
        return float(default)


def _public_health_norm(obs: Mapping[str, Any], default: Optional[float] = None) -> Optional[float]:
    h = obs.get("observed_health_norm")
    if h is None:
        return default
    try:
        return max(0.0, min(1.0, float(h)))
    except Exception:
        return default


class RandomMaintenancePolicy:
    """Uniform legal-action baseline."""

    def __init__(self, seed: int = 0) -> None:
        self.rng = random.Random(int(seed))

    def select(self, obs: Mapping[str, Any]) -> str:
        return self.rng.choice(list(ACTIONS))

    def update(self, feedback: Mapping[str, Any]) -> None:
        pass


class ThresholdMaintenancePolicy:
    """Condition/control-limit baseline using only public observed health.

    If health is not currently public, the policy inspects periodically rather
    than reading the environment's hidden true health.
    """

    def __init__(
        self,
        repair_threshold: float = 0.50,
        replace_threshold: float = 0.20,
        inspect_period: int = 4,
    ) -> None:
        self.repair_threshold = float(max(0.0, min(1.0, repair_threshold)))
        self.replace_threshold = float(max(0.0, min(1.0, replace_threshold)))
        if self.replace_threshold > self.repair_threshold:
            self.replace_threshold = self.repair_threshold
        self.inspect_period = int(max(1, inspect_period))
        self.t = 0

    def select(self, obs: Mapping[str, Any]) -> str:
        self.t += 1
        h = _public_health_norm(obs, None)
        if h is None:
            return "INSPECT" if self.t % self.inspect_period == 1 else "RUN"
        if h <= self.replace_threshold:
            return "REPLACE"
        if h <= self.repair_threshold:
            return "REPAIR"
        return "RUN"

    def update(self, feedback: Mapping[str, Any]) -> None:
        pass


def evaluate_policy(policy: Any, spec: MaintenanceSpec, *, seed: int = 0) -> Dict[str, Any]:
    """Run one episode and return a compact summary.

    The policy receives only observations returned by the environment. The
    diagnostic ``info`` object is used for logging after the transition, not as
    policy input.
    """

    env = MaintenanceReplacementEnv(replace(spec, seed=int(seed)))
    obs, _, done, info = env.reset(seed=int(seed))
    total = 0.0
    steps = 0
    actions: List[str] = []
    while not done:
        action = str(policy.select(obs))
        if action not in ACTIONS:
            raise ValueError(
                f"maintenance baseline fail-closed: policy {policy.__class__.__name__} emitted invalid action {action!r}"
            )
        next_obs, reward, done, info = env.step(action)
        total += float(reward)
        steps += 1
        actions.append(action)
        if hasattr(policy, "update"):
            policy.update({"action": action, "reward": float(reward), "done": bool(done), "info": dict(info)})
        obs = next_obs
    return {
        "total_reward": float(total),
        "steps": int(steps),
        "final_health_true": int(info.get("health_true", -1)),
        "action_counts": {a: int(actions.count(a)) for a in ACTIONS},
    }


def _mean_reward_for_threshold(
    spec: MaintenanceSpec,
    *,
    repair_threshold: float,
    replace_threshold: float,
    inspect_period: int,
    seeds: Sequence[int],
) -> float:
    vals = []
    for s in seeds:
        pol = ThresholdMaintenancePolicy(repair_threshold, replace_threshold, inspect_period)
        vals.append(evaluate_policy(pol, spec, seed=int(s))["total_reward"])
    return float(sum(vals) / max(1, len(vals)))


class OptimizedThresholdMaintenancePolicy(ThresholdMaintenancePolicy):
    """Small public grid-search control-limit baseline.

    This is not a solver over hidden state. It selects thresholds using sampled
    public episodes from the same environment specification.
    """

    def __init__(
        self,
        spec: MaintenanceSpec,
        seed: int = 0,
        train_seeds: Optional[Sequence[int]] = None,
    ) -> None:
        if train_seeds is None:
            train_seeds = tuple(int(seed) * 100 + i for i in range(5))
        best: Tuple[float, float, int, float] | None = None
        for repair_threshold in (0.25, 0.50, 0.75):
            for replace_threshold in (0.00, 0.25, 0.50):
                if replace_threshold > repair_threshold:
                    continue
                for inspect_period in (1, 2, 4, 8):
                    score = _mean_reward_for_threshold(
                        spec,
                        repair_threshold=repair_threshold,
                        replace_threshold=replace_threshold,
                        inspect_period=inspect_period,
                        seeds=train_seeds,
                    )
                    if best is None or score > best[3]:
                        best = (repair_threshold, replace_threshold, inspect_period, score)
        assert best is not None
        self.training_score = float(best[3])
        super().__init__(repair_threshold=best[0], replace_threshold=best[1], inspect_period=best[2])


class FiniteHorizonDPMaintenancePolicy:
    """Known-model finite-horizon DP baseline for fully observed health only.

    This is a strong classical baseline, but only parity-valid when health is
    publicly observed. It refuses partial/hidden observation modes rather than
    silently becoming an oracle.
    """

    def __init__(self, spec: MaintenanceSpec) -> None:
        if str(spec.observe_health) != "direct":
            raise ValueError(
                "finite_horizon_dp baseline is parity-valid only when observe_health='direct'; "
                "use threshold/q_learning for partial/hidden regimes or label a separate oracle upper bound."
            )
        self.spec = spec
        self.max_h = int(spec.max_health)
        self.horizon = int(spec.horizon)
        self.V: List[List[float]] = [[0.0 for _ in range(self.max_h + 1)] for _ in range(self.horizon + 1)]
        self.policy: List[List[str]] = [["RUN" for _ in range(self.max_h + 1)] for _ in range(self.horizon)]
        self._solve()

    def _degrade_prob(self, h: int) -> float:
        low_factor = max(0.0, 1.0 - float(h) / float(max(1, self.spec.max_health)))
        return max(0.0, min(1.0, float(self.spec.degradation_prob) + float(self.spec.extra_degrade_when_low) * low_factor))

    def _q(self, t: int, h: int, action: str) -> float:
        s = self.spec
        max_h = self.max_h
        if action == "RUN":
            base = float(s.run_reward) * (float(h) / float(max(1, max_h)))
            p = self._degrade_prob(h)
            total = 0.0
            for prob, h1 in ((1.0 - p, h), (p, max(0, h - 1))):
                reward = base
                nh = h1
                if nh <= int(s.failure_health):
                    reward -= float(s.failure_penalty)
                    if bool(s.reset_on_failure):
                        nh = max_h
                total += prob * (reward + self.V[t + 1][nh])
            return float(total)
        if action == "INSPECT":
            return -float(s.inspect_cost) + self.V[t + 1][h]
        if action == "REPAIR":
            nh = min(max_h, h + max(1, int(s.repair_boost)))
            return -float(s.repair_cost) + self.V[t + 1][nh]
        if action == "REPLACE":
            return -float(s.replace_cost) + self.V[t + 1][max_h]
        if action == "WAIT":
            p = max(0.0, min(1.0, float(s.wait_recovery_prob)))
            nh_recover = min(max_h, h + 1)
            return -float(s.wait_cost) + (1.0 - p) * self.V[t + 1][h] + p * self.V[t + 1][nh_recover]
        return -float(s.wait_cost) + self.V[t + 1][h]

    def _solve(self) -> None:
        for t in reversed(range(self.horizon)):
            for h in range(self.max_h + 1):
                scored = [(self._q(t, h, a), a) for a in ACTIONS]
                scored.sort(key=lambda x: (x[0], -ACTIONS.index(x[1])), reverse=True)
                self.V[t][h] = float(scored[0][0])
                self.policy[t][h] = str(scored[0][1])

    def select(self, obs: Mapping[str, Any]) -> str:
        h_obs = obs.get("observed_health")
        if h_obs is None:
            raise RuntimeError("finite_horizon_dp did not receive public observed_health in a direct-observation regime")
        h = int(max(0, min(self.max_h, int(h_obs))))
        t = int(max(0, min(self.horizon - 1, int(obs.get("t", 0) or 0))))
        return self.policy[t][h]

    def update(self, feedback: Mapping[str, Any]) -> None:
        pass


class TabularQMaintenancePolicy:
    """Sampled model-free baseline over public observation states.

    The learner is allowed training episodes but its state encoder uses only the
    public observation object, never ``info['health_true']``.
    """

    def __init__(
        self,
        spec: MaintenanceSpec,
        seed: int = 0,
        train_episodes: int = 120,
        alpha: float = 0.25,
        gamma: float = 0.97,
        epsilon: float = 0.20,
    ) -> None:
        self.spec = spec
        self.seed = int(seed)
        self.alpha = float(alpha)
        self.gamma = float(gamma)
        self.epsilon = float(epsilon)
        self.rng = random.Random(self.seed)
        self.Q: Dict[Tuple[Any, ...], Dict[str, float]] = {}
        self._train(int(train_episodes))

    def _state(self, obs: Mapping[str, Any]) -> Tuple[Any, ...]:
        h = obs.get("observed_health")
        if h is None:
            h_key: Any = "unknown"
        else:
            try:
                h_key = int(h)
            except Exception:
                h_key = "unknown"
        t = int(obs.get("t", 0) or 0)
        horizon = int(obs.get("horizon", self.spec.horizon) or self.spec.horizon)
        t_bucket = int(4 * t / max(1, horizon))
        return (
            h_key,
            t_bucket,
            str(obs.get("last_action", "")),
            str(obs.get("last_event", "")),
            round(_as_float(obs.get("degradation_prob_public", self.spec.degradation_prob), self.spec.degradation_prob), 2),
        )

    def _ensure(self, st: Tuple[Any, ...]) -> Dict[str, float]:
        return self.Q.setdefault(st, {a: 0.0 for a in ACTIONS})

    def _choose_train(self, st: Tuple[Any, ...]) -> str:
        if self.rng.random() < self.epsilon:
            return self.rng.choice(list(ACTIONS))
        q = self._ensure(st)
        return max(ACTIONS, key=lambda a: (q.get(a, 0.0), -ACTIONS.index(a)))

    def _train(self, episodes: int) -> None:
        for ep in range(max(1, episodes)):
            env = MaintenanceReplacementEnv(replace(self.spec, seed=self.seed * 1000 + ep))
            obs, _, done, _ = env.reset(seed=self.seed * 1000 + ep)
            while not done:
                st = self._state(obs)
                action = self._choose_train(st)
                next_obs, reward, done, _ = env.step(action)
                nst = self._state(next_obs)
                q = self._ensure(st)
                nq = self._ensure(nst)
                target = float(reward) + (0.0 if done else self.gamma * max(nq.values()))
                q[action] = (1.0 - self.alpha) * q.get(action, 0.0) + self.alpha * target
                obs = next_obs

    def select(self, obs: Mapping[str, Any]) -> str:
        st = self._state(obs)
        q = self._ensure(st)
        return max(ACTIONS, key=lambda a: (q.get(a, 0.0), -ACTIONS.index(a)))

    def update(self, feedback: Mapping[str, Any]) -> None:
        pass


BASELINE_ALIASES = {
    "random": "random",
    "threshold": "threshold",
    "condition_based": "threshold",
    "threshold_opt": "threshold_opt",
    "optimized_threshold": "threshold_opt",
    "dp": "finite_horizon_dp",
    "finite_horizon_dp": "finite_horizon_dp",
    "q_learning": "q_learning",
    "tabular_q": "q_learning",
}


def canonical_baseline_name(kind: str) -> str:
    key = str(kind or "threshold").lower()
    return BASELINE_ALIASES.get(key, key)


def make_maintenance_policy(kind: str, spec: MaintenanceSpec, seed: int = 0) -> Any:
    name = canonical_baseline_name(kind)
    if name == "random":
        return RandomMaintenancePolicy(seed=seed)
    if name == "threshold":
        return ThresholdMaintenancePolicy()
    if name == "threshold_opt":
        return OptimizedThresholdMaintenancePolicy(spec, seed=seed)
    if name == "finite_horizon_dp":
        return FiniteHorizonDPMaintenancePolicy(spec)
    if name == "q_learning":
        return TabularQMaintenancePolicy(spec, seed=seed)
    raise ValueError(f"unknown maintenance baseline: {kind}")


__all__ = [
    "ACTIONS",
    "BASELINE_ALIASES",
    "RandomMaintenancePolicy",
    "ThresholdMaintenancePolicy",
    "OptimizedThresholdMaintenancePolicy",
    "FiniteHorizonDPMaintenancePolicy",
    "TabularQMaintenancePolicy",
    "canonical_baseline_name",
    "make_maintenance_policy",
    "evaluate_policy",
]
