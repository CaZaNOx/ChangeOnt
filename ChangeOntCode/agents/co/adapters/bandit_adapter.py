from __future__ import annotations
from typing import Any, Dict, Optional

from agents.co.core.pipeline import COAgentCore

class COAdapterBandit:
    """
    Passes family='bandit' (+ n_arms if known) to core, forwards last feedback,
    and uses the core-proposed action when present. Minimal deterministic fallback
    is round-robin by core step.
    """
    def __init__(self, core: COAgentCore, name: str = "CO_full", n_arms: Optional[int] = None):
        self.core = core
        self.name = name
        self.n_arms = int(n_arms) if n_arms is not None else None
        self._last_feedback: Dict[str, Any] = {}

    def select(self, observation: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        obs: Dict[str, Any] = {"family": "bandit"}
        if self.n_arms is not None:
            obs["n_arms"] = int(self.n_arms)
        if observation:
            obs.update(observation)

        metrics = self.core.step(obs, feedback=(self._last_feedback or None))

        action = metrics.get("action")
        if not isinstance(action, int) or (self.n_arms is not None and not (0 <= action < self.n_arms)):
            step = int(metrics.get("step", 1))
            n = int(obs.get("n_arms", self.n_arms or 2))
            action = (step - 1) % max(1, n)

        metrics["action"] = int(action)
        metrics["agent"] = self.name
        metrics["family"] = "bandit"
        return metrics

    def update(self, feedback: Dict[str, Any]) -> None:
        self._last_feedback = dict(feedback or {})