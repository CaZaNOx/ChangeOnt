# agents/co/core/elements/EB_ghvc.py
from __future__ import annotations
from typing import Dict, Any
from dataclasses import dataclass
from ._shared import publish_signal

@dataclass
class EB_GHVC:
    gamma: float = 0.05   # birth penalty
    lam_mdl: float = 0.01 # MDL weight
    last_birth_t: int = -10

    def configure(self, params: Dict[str, Any], context: Dict[str, Any]):
        self.gamma   = float(params.get("gamma",   params.get("birth_threshold", self.gamma)))
        self.lam_mdl = float(params.get("lambda",  params.get("mdl_lambda",      self.lam_mdl)))
        return self

    def _mdl_gain(self, resid_mse: float, k_new: int) -> float:
        return max(0.0, resid_mse) - self.lam_mdl * float(k_new)

    def _run_core(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any) -> Dict[str, Any]:
        t     = int(observation.get("t", 0))
        res   = observation.get("residuals", {}) or {}
        probes= observation.get("probes", {}) or {}
        budget= primitives.get("budget")
        cal   = primitives.get("calibrators", {}) or {}

        mse = float(res.get("mse", 0.0))
        cp  = float(probes.get("change_point", 0.0))
        pressure = 0.5 * mse + 0.5 * cp

        rm_gamma = cal.get("gamma_rm")
        if callable(rm_gamma):
            try:
                self.gamma, cal["gamma_rm"] = rm_gamma(self.gamma, pressure)
            except Exception:
                pass

        rm_lambda = cal.get("lambda_rm")
        if callable(rm_lambda):
            try:
                self.lam_mdl, cal["lambda_rm"] = rm_lambda(self.lam_mdl, pressure)
            except Exception:
                pass

        mdl_gain   = self._mdl_gain(mse, k_new=1)
        want_birth = (pressure > self.gamma) and (mdl_gain > 0.0)

        born = False
        if want_birth and (budget is not None):
            try:
                if budget.allow_move("birth") and budget.commit("birth"):
                    born = True
                    self.last_birth_t = t
            except Exception:
                pass

        return {"born_variable": born, "pressure": pressure, "mdl_gain": mdl_gain}

    def update(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None) -> Dict[str, Any]:
        out = self._run_core(observation, primitives, header)
        bus = primitives.get("co_bus")
        publish_signal(bus, "EB_GHVC.pressure",  out.get("pressure", 0.0))
        publish_signal(bus, "EB_GHVC.mdl_gain",  out.get("mdl_gain", 0.0))
        publish_signal(bus, "EB_GHVC.birth_suggest", 1.0 if out.get("born_variable") else 0.0)
        return out

    def step(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None) -> Dict[str, Any]:
        return self.update(observation, primitives, header, feedback)