from __future__ import annotations
from typing import Any, Dict, Optional

class COAdapterMaze:
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
                # tiny inline bus fallback
                class _Bus:
                    def __init__(self): self._s = {}
                    def push(self,f,a,weight=1.0,**kw):
                        self._s.setdefault(f,[]).append({"action":a,"weight":float(weight),**kw})
                    def drain(self,f): lst=self._s.get(f,[]); self._s[f]=[]; return lst
                    def peek(self,f):  return list(self._s.get(f,[]))
                    def size(self,f):  return len(self._s.get(f,[]))
                self.core.primitives["co_bus"] = _Bus()

    def select(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        obs = dict(observation or {})
        obs.setdefault("family", "maze")

        # Ensure bus present (usually created by builder, but keep robust)
        self._ensure_bus()

        # DECISION PASS (header.update + elements.update/step + ActionHead.step exactly once)
        out: Dict[str, Any] = {}
        try:
            out = self._pipe.run(self.core.elements, self.core.primitives, self.core.header, obs, feedback=None) or {}
        except Exception:
            out = {}

        # Safety guard for action shape (maze)
        act = out.get("action")
        if act not in ("UP", "DOWN", "LEFT", "RIGHT"):
            out["action"] = "RIGHT"
            out.setdefault("co_policy", "maze:safe_default")
            out.setdefault("co_bus_votes", 0)

        # Keep last obs for update pass
        self._last_obs = dict(obs)
        return out

    def update(self, feedback: Dict[str, Any]) -> None:
        # LEARNING-ONLY PASS — must not call ActionHead again
        obs_like = {"family": "maze"}
        if self._last_obs and "t" in self._last_obs:
            try:
                obs_like["t"] = int(self._last_obs["t"]) + 1
            except Exception:
                pass

        try:
            # Prefer the dedicated learning pass
            if hasattr(self._pipe, "run_update"):
                self._pipe.run_update(self.core.elements, self.core.primitives, self.core.header, obs_like, feedback or {})
            else:
                # ultra-conservative fallback (shouldn’t be needed once pipeline has run_update)
                self._pipe.run(self.core.elements, self.core.primitives, self.core.header, obs_like, feedback or {})
        except Exception:
            pass