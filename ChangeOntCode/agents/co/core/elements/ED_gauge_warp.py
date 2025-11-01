# E_D_gauge_warp.py
from typing import Any, Dict, Callable, Iterable

class ED_GaugeWarp:
    """
    Element D: Gauge-only stabilization outside HAQ.
    Provides a salience-weighted warp for motif detection (no A* coupling).
    """
    def __init__(self, alpha: float = 0.0):
        self.alpha = max(0.0, float(alpha))

    def params(self) -> Dict[str, Any]:
        return {"alpha": self.alpha}

    def stabilize(self,
                  stream: Iterable[Any],
                  score: Callable[[Any], float],
                  gauge: Callable[[Any], float] | None = None) -> float:
        """
        Return a stabilization score: higher is 'more stabilized'. Safe default.
        """
        total = 0.0
        count = 0
        for x in stream:
            try:
                s = float(score(x))
            except Exception:
                s = 0.0
            g = 0.0
            if gauge is not None:
                try:
                    g = float(gauge(x))
                except Exception:
                    g = 0.0
            total += max(0.0, s - self.alpha * g)
            count += 1
        return (total / count) if count > 0 else 0.0
