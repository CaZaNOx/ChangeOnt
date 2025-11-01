# agents/co/core/primitives/budget.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class BudgetLedger:
    """Tracks debits/credits and per-action cooldowns."""
    credits: float = 0.0
    debits: float = 0.0
    cooldowns: Dict[str, int] = field(default_factory=dict)
    cooldown_cfg: Dict[str, int] = field(default_factory=lambda:{
        "birth": 10, "flip": 15, "precision+": 8
    })
    costs: Dict[str, float] = field(default_factory=lambda:{
        "birth": 1.0, "flip": 0.6, "precision+": 0.4
    })
    min_margin: float = 0.0  # require credits - debits >= min_margin

    def tick(self):
        for k in list(self.cooldowns.keys()):
            if self.cooldowns[k] > 0:
                self.cooldowns[k] -= 1

    def credit(self, amt: float):
        self.credits += float(amt)

    def _apply(self, action: str) -> bool:
        self.debits += self.costs.get(action, 0.0)
        self.cooldowns[action] = self.cooldown_cfg.get(action, 0)
        return True

    def allow_move(self, action: str) -> bool:
        if self.cooldowns.get(action, 0) > 0:
            return False
        if (self.credits - self.debits) < self.min_margin:
            return False
        return True

    def commit(self, action: str) -> bool:
        if not self.allow_move(action):
            return False
        return self._apply(action)
