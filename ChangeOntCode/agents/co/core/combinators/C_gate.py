# C_gate.py
from typing import Any, Dict

class C_Gate:
    """
    Chooses between classical and CO routes based on header/router signals.
    Non-throwing; returns "co" by default.
    """
    def __init__(self, prefer: str = "auto", co_bias: float = 0.5):
        self.prefer = prefer  # "auto"|"co"|"classical"
        self.co_bias = max(0.0, min(1.0, float(co_bias)))

    def route(self, header: Any, metrics: Dict[str, Any]) -> str:
        if self.prefer in ("co", "classical"):
            return self.prefer
        # auto mode: use router metric if present
        r = metrics.get("router_score")
        if isinstance(r, (int, float)):
            return "co" if r >= 0.5 else "classical"
        return "co" if self.co_bias >= 0.5 else "classical"
