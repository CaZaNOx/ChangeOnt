# agents/co/headers/H_ID_subject.py
from ..core.context.math_context import MathContext, HeaderState

_DEFAULT_RANGES = {
    "maze":    dict(tau=(0.00,0.25), eps=(0.00,0.15), alpha=(0.00,0.25), gamma=(0.05,0.02), cooldown=(20,10),
                    dyn_prior=0.2),
    "bandit":  dict(tau=(0.05,0.40), eps=(0.05,0.30), alpha=(0.10,0.60), gamma=(0.05,0.015), cooldown=(15,5),
                    dyn_prior=0.7),
    "renewal": dict(tau=(0.02,0.30), eps=(0.05,0.25), alpha=(0.00,0.35), gamma=(0.04,0.02), cooldown=(20,10),
                    dyn_prior=0.5),
}

class HeaderID:
    NAME = "ID"

    def configure(self, family: str = "generic", overrides: dict | None = None) -> tuple[MathContext, HeaderState]:
        cfg = _DEFAULT_RANGES.get(family, dict(
            tau=(0.00,0.30), eps=(0.00,0.30), alpha=(0.00,0.35), gamma=(0.05,0.02), cooldown=(20,10),
            dyn_prior=0.5))
        if overrides: cfg.update(overrides)
        mc = MathContext(path_algebra="minplus", number_arith="spread", logic="quantale")
        hs = HeaderState(tag="ID", dyn=float(cfg["dyn_prior"]))
        hs.tau_range = cfg["tau"]; hs.eps_range = cfg["eps"]; hs.alpha_cap_range = cfg["alpha"]
        hs.gamma_range = cfg["gamma"]; hs.cooldown_range = cfg["cooldown"]
        hs.derive_effective(r_prime_static=1)
        return mc, hs

    def guards(self) -> dict:
        return {
            "warp_off": False,
            "birth_off": False,
            "spread_off": False,
        }
