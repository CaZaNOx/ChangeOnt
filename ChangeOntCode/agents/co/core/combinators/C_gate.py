from typing import Any, Dict

class C_Gate:
    """Retired route gate retained only as a hard guard.

    Certified CO runtime does not switch between CO and non-CO routes. If
    constructed, this guard always reports `co`; any request for another route
    raises immediately instead of silently rescuing a run.
    """

    def __init__(self, prefer: str = "co", co_bias: float = 1.0):
        prefer = str(prefer or "co").lower()
        if prefer not in ("co", "canonical"):
            raise ValueError("C_Gate is retired: certified CO runtime permits only the canonical CO route")
        self.prefer = "co"
        self.co_bias = 1.0

    def route(self, header: Any, metrics: Dict[str, Any]) -> str:
        return "co"
