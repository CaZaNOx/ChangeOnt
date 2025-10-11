# P13_creative_option_birth.py
from dataclasses import dataclass
from typing import List, Any, Callable

@dataclass
class BirthDecision:
    born: bool
    reason: str
    prototype: Any | None

class CreativeOptionBirth:
    """
    CO P13: MDL-penalized variable birth (Gödel-like). Skeleton: propose split/new prototype
    if residual > threshold for cooldown window; accept only if MDL drops.
    """
    def __init__(self, mdl_lambda: float = 1.0, threshold: float = 1.0, cooldown: int = 5):
        self.mdl_lambda = max(0.0, float(mdl_lambda))
        self.threshold = max(0.0, float(threshold))
        self.cooldown = max(1, int(cooldown))
        self._cool = 0

    def step(self, residual: float,
             propose: Callable[[], Any],
             mdl_change: Callable[[Any], float]) -> BirthDecision:
        if self._cool > 0:
            self._cool -= 1
            return BirthDecision(False, "cooldown", None)
        if residual <= self.threshold:
            return BirthDecision(False, "residual_below_threshold", None)
        proto = None
        try:
            proto = propose()
            delta = mdl_change(proto) - self.mdl_lambda
        except Exception:
            return BirthDecision(False, "proposal_failed", None)
        if delta < 0:
            self._cool = self.cooldown
            return BirthDecision(True, "mdl_improved", proto)
        return BirthDecision(False, "mdl_not_improved", None)

__all__ = ["CreativeOptionBirth", "BirthDecision"]
