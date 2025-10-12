from __future__ import annotations
from typing import Any, Dict, Optional

from agents.co.core.pipeline import COAgentCore

DIRS = ("UP", "DOWN", "LEFT", "RIGHT")

class COAdapterMaze:
    """
    Passes family='maze' + last feedback to core.
    Uses core-proposed 'action' if present; otherwise a minimal, deterministic fallback
    that cycles directions by core step (prevents hard-stall but is not a planner).
    """
    def __init__(self, core: COAgentCore, name: str = "CO_full"):
        self.core = core
        self.name = name
        self._last_feedback: Dict[str, Any] = {}

    def select(self, observation: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        obs: Dict[str, Any] = {"family": "maze"}
        if observation:
            obs.update(observation)

        metrics = self.core.step(obs, feedback=(self._last_feedback or None))

        # Prefer core's action if valid
        action = metrics.get("action")
        if action not in DIRS:
            # Minimal deterministic fallback: use the core step to cycle directions
            step = int(metrics.get("step", 1))
            action = DIRS[(step - 1) % len(DIRS)]

        metrics["action"] = action
        metrics["agent"] = self.name
        metrics["family"] = "maze"
        return metrics

    def update(self, feedback: Dict[str, Any]) -> None:
        self._last_feedback = dict(feedback or {})