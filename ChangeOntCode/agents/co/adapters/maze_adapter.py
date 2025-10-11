# maze_adapter.py
from typing import Any, Dict, Optional
from agents.co.core.pipeline import COAgentCore

class COAdapterMaze:
    def __init__(self, core: COAgentCore, name: str = "CO_full"):
        self.core = core
        self.name = name
        self._warned = False

    def select(self, observation: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if observation is None and not self._warned:
            self._warned = True
            # synthesize minimal observation
            observation = {}
        metrics = self.core.step(observation, feedback=None)
        # trivial placeholder action; runner maps its own action protocol
        metrics["action"] = "UP"
        metrics["agent"] = self.name
        metrics["family"] = "maze"
        return metrics

    def update(self, feedback: Dict[str, Any]) -> None:
        # allow runners to pass reward/outcome; no crash if unused
        _ = feedback
