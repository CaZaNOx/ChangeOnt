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
        for k, v in (params or {}).items():
            if hasattr(self, k):
                setattr(self, k, v)
        return self

    # original core logic (slightly generalized)
    def _run_core(self, hdr: Any, probes: Dict[str, Any], budget: Any, math_ctx: Any) -> Dict[str, Any]:
        V  = float(probes.get("volatility", 0.0))
        CP = float(probes.get("change_point", 0.0))
        H  = float(probes.get("holonomy", 0.0))
        K  = float(probes.get("compressibility", 0.0))
        R  = float(probes.get("repeat_ratio", 0.0))
        F  = float(probes.get("fano", 0.0))
        M  = float(probes.get("agreement", 0.0))

        score = (self.wV*V + self.wCP*CP + self.wH*H + self.wK*K +
                 self.wR*R + self.wF*F + self.wM*M)
        prop = _sigmoid(score)
        dyn_prev = float(getattr(hdr, "dyn", 0.0))
        dyn_target = self.dyn_min + prop * (self.dyn_max - self.dyn_min)

        dyn_new = dyn_prev
        if dyn_prev < self.exit_thr and dyn_target >= self.enter_thr:
            dyn_new = dyn_target
            if budget is not None and hasattr(budget, "allow_move") and budget.allow_move("flip"):
                try: budget.commit("flip")
                except Exception: pass
        elif dyn_prev > self.enter_thr and dyn_target <= self.exit_thr:
            dyn_new = dyn_target
            if budget is not None and hasattr(budget, "allow_move") and budget.allow_move("flip"):
                try: budget.commit("flip")
                except Exception: pass
        else:
            dyn_new = 0.9 * dyn_prev + 0.1 * dyn_target

        hdr.dyn = max(0.0, min(1.0, dyn_new))

        # math selection
        if math_ctx is not None:
            try:
                if hdr.dyn < 0.2:
                    math_ctx.path_algebra = "classical"
                    math_ctx.number_arith = "classic"
                    math_ctx.logic = "boolean"
                elif hdr.dyn < 0.7:
                    math_ctx.path_algebra = "minplus"
                    math_ctx.number_arith = "classic"
                    math_ctx.logic = "boolean"
                else:
                    math_ctx.path_algebra = "minplus"
                    math_ctx.number_arith = "spread"
                    math_ctx.logic = "quantale"
            except Exception:
                pass

        mctx_dict = {}
        if math_ctx is not None:
            to_dict = getattr(math_ctx, "to_dict", None)
            if callable(to_dict):
                try: mctx_dict = to_dict()
                except Exception: mctx_dict = {}
            else:
                mctx_dict = {
                    "path_algebra": getattr(math_ctx, "path_algebra", None),
                    "number_arith": getattr(math_ctx, "number_arith", None),
                    "logic": getattr(math_ctx, "logic", None),
                }
        return {"dyn": float(hdr.dyn), "math_context": mctx_dict}

    # pipeline hooks
    def update(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None):
        hdr = getattr(header, "state", header)  # accept either
        probes = observation.get("probes", {}) or {}
        budget = primitives.get("budget")
        math_ctx = getattr(header, "math", None)
        return self._run_core(hdr, probes, budget, math_ctx)

    def step(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None):
        return self.update(observation, primitives, header, feedback)