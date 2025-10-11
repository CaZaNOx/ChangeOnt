# bandit_adapter.py
from typing import Any, Dict, Optional
from agents.co.core.pipeline import COAgentCore

class COAdapterBandit:
    def __init__(self, core: COAgentCore, name: str = "CO_full"):
        self.core = core
        self.name = name
        self._warned = False

    def select(self, observation: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if observation is None and not self._warned:
            self._warned = True
            observation = {}
        metrics = self.core.step(observation, feedback=None)
        metrics["action"] = 0  # pick arm 0 as safe default
        metrics["agent"] = self.name
        metrics["family"] = "bandit"
        return metrics

    def update(self, feedback: Dict[str, Any]) -> None:
        _ = feedback
