# agents/co/core/elements/EG_density_precision.py
from typing import Any, Dict
from ..primitives.P7_precision import precision_schedule

class EG_Density:
    """
    Precision / density control.
    Inputs:
      - signals: {'surprise': float} (optional)
      - header_state: used to write r_prime and keep effective ranges coherent
    Params:
      - mode: 'fixed' | 'coarse' | 'adaptive'
      - r_static: default starting precision (int)
    """
    def __init__(self):
        self.params: Dict[str, Any] = {}
        self.last_r: int = 1

    def configure(self, params: Dict, context: Dict):
        self.params = params or {}
        self.params.setdefault("mode", "adaptive")
        self.params.setdefault("r_static", 1)
        return self

    def fit(self, stream_or_env_view=None):
        return self

    def step(self, inputs: Dict) -> Dict:
        signals = inputs.get("signals", {})
        hs = inputs.get("header_state")
        mode = self.params["mode"]
        r_static = int(self.params["r_static"])

        stats = {"surprise": float(signals.get("z_PE", 0.0))}
        r_p = precision_schedule(stats, mode)
        # Let header derive r' baseline; we lightly override for adaptive
        if r_p != getattr(hs, "r_prime", r_static):
            hs.r_prime = r_p
        self.last_r = hs.r_prime

        return {"r_prime": int(self.last_r)}

    def report(self) -> Dict:
        return {"r_prime": int(self.last_r)}
