# agents/co/core/elements/EB_ghvc.py
from __future__ import annotations
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class EB_GHVC:
    gamma: float = 0.05   # birth penalty
    lam_mdl: float = 0.01 # MDL weight
    last_birth_t: int = -10

    def configure(self, params: Dict[str, Any], context: Dict[str, Any]):
        self.gamma = float(params.get("gamma", self.gamma))
        self.lam_mdl = float(params.get("lambda", self.lam_mdl))
        return self

    def _mdl_gain(self, resid_mse: float, k_new: int) -> float:
        # crude MDL: error drop - λ * parameters
        return max(0.0, resid_mse) - self.lam_mdl * float(k_new)

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        t = len(state.get("history", ()))
        residuals = state.get("residuals", {})
        probes = state.get("probes", {})
        budget = state.get("budget", None)
        calibrators = state.get("calibrators", {})

        mse = float(residuals.get("mse", 0.0))
        cp = float(probes.get("change_point", 0.0))
        pressure = 0.5 * mse + 0.5 * cp

        # Robbins–Monro adapt gamma/lambda if provided
        rm_gamma = calibrators.get("gamma_rm")
        if rm_gamma is not None:
            self.gamma, calibrators["gamma_rm"] = rm_gamma(self.gamma, pressure)

        rm_lambda = calibrators.get("lambda_rm")
        if rm_lambda is not None:
            self.lam_mdl, calibrators["lambda_rm"] = rm_lambda(self.lam_mdl, pressure)

        # birth decision: pressure surpasses gamma and MDL is positive
        mdl_gain = self._mdl_gain(mse, k_new=1)
        want_birth = (pressure > self.gamma) and (mdl_gain > 0.0)

        born = False
        if want_birth and (budget is not None):
            if budget.allow_move("birth"):
                if budget.commit("birth"):
                    born = True
                    self.last_birth_t = t

        return {"born_variable": born, "pressure": pressure, "mdl_gain": mdl_gain}
