# agents/co/headers/H_SSI_shared.py
from ..core.context.math_context import MathContext, HeaderState

class HeaderSSI:
    NAME = "SSI"

    def configure(self, family: str = "generic", overrides: dict | None = None) -> tuple[MathContext, HeaderState]:
        # Conservative version of ID: same dials but tighter caps
        mc = MathContext(path_algebra="minplus", number_arith="spread", logic="quantale")
        hs = HeaderState(tag="SSI", dyn=float(overrides.get("dyn_prior", 0.5) if overrides else 0.5))
        tau = overrides.get("tau", (0.00, 0.25)) if overrides else (0.00, 0.25)
        eps = overrides.get("eps", (0.00, 0.15)) if overrides else (0.00, 0.15)
        alpha = overrides.get("alpha", (0.00, 0.20)) if overrides else (0.00, 0.20)
        gamma = overrides.get("gamma", (0.05, 0.03)) if overrides else (0.05, 0.03)
        cooldown = overrides.get("cooldown", (20, 10)) if overrides else (20, 10)
        hs.tau_range, hs.eps_range, hs.alpha_cap_range = tau, eps, alpha
        hs.gamma_range, hs.cooldown_range = gamma, cooldown
        hs.derive_effective(r_prime_static=2)
        return mc, hs

    def guards(self) -> dict:
        return {
            "warp_off": False,          # allowed but capped
            "birth_off": False,         # allowed but stricter gamma
            "spread_off": False,
            "claim_gate": "shared_only" # reporting gate lives in adapters/plots
        }
