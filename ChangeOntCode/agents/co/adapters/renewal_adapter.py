from __future__ import annotations
from typing import Any, Dict, Optional

from agents.co.core.pipeline import COAgentCore

class COAdapterRenewal:
    """
    Passes family='renewal' to core, forwards last feedback,
    and uses the core's proposed *integer* action when present.
    Minimal fallback is predict-last: action = observation['obs'] (type-correct).
    """
    def __init__(self, core: COAgentCore, name: str = "CO_full"):
        self.core = core
        self.name = name
        self._last_feedback: Dict[str, Any] = {}

    def select(self, observation: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        obs: Dict[str, Any] = {"family": "renewal"}
        if observation:
            obs.update(observation)

        metrics = self.core.step(obs, feedback=(self._last_feedback or None))

        action = metrics.get("action")
        if not isinstance(action, int):
            # Predict-last fallback (aligns with your baseline types):
            action = int(obs.get("obs", 0))

        metrics["action"] = int(action)
        metrics["agent"] = self.name
        metrics["family"] = "renewal"
        return metrics

    def update(self, feedback: Dict[str, Any]) -> None:
        self._last_feedback = dict(feedback or {})