# agents/co/core/elements/EF_router_gil.py
from __future__ import annotations
from typing import Dict, Any
from dataclasses import dataclass

def _sigmoid(x: float) -> float:
    return 1.0 / (1.0 + (2.718281828)**(-x))

@dataclass
class EF_Router:
    wV: float = 1.0
    wCP: float = 1.2
    wH: float = 0.6
    wK: float = 0.8
    wR: float = -0.6
    wF: float = 0.4
    wM: float = 1.0
    enter_thr: float = 0.6
    exit_thr: float = 0.4
    dyn_min: float = 0.0
    dyn_max: float = 1.0

    def configure(self, params: Dict[str, Any], context: Dict[str, Any]):
        for k,v in params.items():
            if hasattr(self, k): setattr(self, k, v)
        return self

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        hdr = state["header_state"]
        probes = state.get("probes", {})
        budget = state.get("budget", None)

        V  = float(probes.get("volatility", 0.0))
        CP = float(probes.get("change_point", 0.0))
        H  = float(probes.get("holonomy", 0.0))
        K  = float(probes.get("compressibility", 0.0))
        R  = float(probes.get("repeat_ratio", 0.0))
        F  = float(probes.get("fano", 0.0))
        M  = float(probes.get("agreement", 0.0))

        score = (self.wV*V + self.wCP*CP + self.wH*H + self.wK*K +
                 self.wR*R + self.wF*F + self.wM*M)
        prop = _sigmoid(score)  # 0..1
        dyn_prev = float(getattr(hdr, "dyn", 0.0))
        dyn_target = self.dyn_min + prop * (self.dyn_max - self.dyn_min)

        # hysteresis: move only across thresholds
        dyn_new = dyn_prev
        if dyn_prev < self.exit_thr and dyn_target >= self.enter_thr:
            dyn_new = dyn_target
            # flipping regime costs budget "flip"
            if budget is not None and budget.allow_move("flip"):
                budget.commit("flip")
        elif dyn_prev > self.enter_thr and dyn_target <= self.exit_thr:
            dyn_new = dyn_target
            if budget is not None and budget.allow_move("flip"):
                budget.commit("flip")
        else:
            # small adjustment
            dyn_new = 0.9 * dyn_prev + 0.1 * dyn_target

        hdr.dyn = max(0.0, min(1.0, dyn_new))

        # math context selection
        mctx = state["math_context"]
        if hdr.dyn < 0.2:
            mctx.path_algebra = "classical"
            mctx.number_arith = "classic"
            mctx.logic = "boolean"
        elif hdr.dyn < 0.7:
            mctx.path_algebra = "minplus"
            mctx.number_arith = "classic"
            mctx.logic = "boolean"
        else:
            mctx.path_algebra = "minplus"
            mctx.number_arith = "spread"
            mctx.logic = "quantale"

        # derive tolerances from dyn (header will finish mapping ranges)
        # (caller typically calls header.derive_effective() after router)
        return {"dyn": hdr.dyn, "math_context": mctx.to_dict()}
