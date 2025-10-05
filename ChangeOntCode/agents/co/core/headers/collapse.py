# PATH: agents/co/core/headers/collapse.py
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class CollapseGuard:
    """Tracks smooth cadence; flips collapsed if sustained."""
    max_smooth: int = 200
    _smooth: int = 0
    collapsed: bool = False

    def reset(self) -> None:
        self._smooth = 0
        self.collapsed = False

    def note(self, step_ok: bool) -> None:
        if step_ok:
            self._smooth = 0
        else:
            self._smooth += 1
            if self._smooth >= self.max_smooth:
                self.collapsed = True
