from __future__ import annotations
from typing import Any, Dict, Optional

class COAdapterRenewal:
    def __init__(self, core, name: str = "CO") -> None:
        self.core = core
        self.name = name
        self._pipe = core.combinators.get("pipeline")
        self._last_obs: Optional[Dict[str, Any]] = None

    def _ensure_bus(self) -> None:
        if "co_bus" not in self.core.primitives:
            try:
                from agents.co.core.primitives.co_bus import CoVoteBus
                self.core.primitives["co_bus"] = CoVoteBus()
            except Exception:
                pass

    def select(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        obs = dict(observation or {})
        obs.setdefault("family", "renewal")

        self._ensure_bus()

        out: Dict[str, Any] = {}
        try:
            out = self._pipe.run(self.core.elements, self.core.primitives, self.core.header, obs, feedback=None) or {}
        except Exception:
            out = {}

        if "action" not in out:
            out["action"] = int(obs.get("obs", 0))
            out.setdefault("co_policy", "renewal:safe_default")
            out.setdefault("co_bus_votes", 0)

        self._last_obs = dict(obs)
        return out

    def update(self, feedback: Dict[str, Any]) -> None:
        obs_like = {"family": "renewal"}
        if self._last_obs and "t" in self._last_obs:
            try:
                obs_like["t"] = int(self._last_obs["t"]) + 1
            except Exception:
                pass

        try:
            if hasattr(self._pipe, "run_update"):
                self._pipe.run_update(self.core.elements, self.core.primitives, self.core.header, obs_like, feedback or {})
            else:
                self._pipe.run(self.core.elements, self.core.primitives, self.core.header, obs_like, feedback or {})
        except Exception:
            pass