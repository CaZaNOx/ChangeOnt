# agents/co/core/elements/EA_haq.py
from __future__ import annotations
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class EA_HAQ:
    alpha: float = 0.0
    kappa: float = 0.2  # learning stiffness

    def configure(self, params: Dict[str, Any], context: Dict[str, Any]):
        self.alpha = float(params.get("alpha0", 0.0))
        self.kappa = float(params.get("kappa", self.kappa))
        return self

    def _update_alpha(self, z_pe: float, z_gain: float, cap: float):
        target = max(0.0, min(cap, z_pe + z_gain))
        self.alpha += self.kappa * (target - self.alpha)
        self.alpha = max(0.0, min(cap, self.alpha))

    def _warp_classical(self, base_costs: Dict[Any, float]) -> Dict[Any, float]:
        # Simple affine warp by alpha
        return {k: v * (1.0 - self.alpha) for k, v in base_costs.items()}

    def _warp_minplus(self, base_costs: Dict[Any, float]) -> Dict[Any, float]:
        # In min-plus, lowering costs is also a linear shift; we keep it simple
        return {k: v - self.alpha for k, v in base_costs.items()}

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        hdr = state["header_state"]
        math_ctx = state["math_context"]
        signals = state.get("signals", {})
        z_pe = float(signals.get("z_PE", 0.0))
        z_gain = float(signals.get("z_gain", 0.0))
        cap = float(getattr(hdr, "alpha_cap", 0.0))
        self._update_alpha(z_pe, z_gain, cap)

        base_costs = state.get("base_costs", {})
        if math_ctx.path_algebra == "minplus":
            warped = self._warp_minplus(base_costs)
        else:
            warped = self._warp_classical(base_costs)

        return {"alpha": self.alpha, "warped_costs": warped}
