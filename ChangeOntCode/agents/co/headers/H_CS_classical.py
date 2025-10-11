# agents/co/headers/H_CS_classical.py
from ..core.context.math_context import MathContext, HeaderState

class HeaderCS:
    NAME = "CS"

    def configure(self, family: str = "generic") -> tuple[MathContext, HeaderState]:
        mc = MathContext(path_algebra="classical", number_arith="classic", logic="boolean")
        hs = HeaderState(tag="CS", dyn=0.0)
        # Strict classical caps
        hs.tau_range = (0.0, 0.0)
        hs.eps_range = (0.0, 0.0)
        hs.alpha_cap_range = (0.0, 0.0)
        hs.gamma_range = (0.05, 0.05)  # irrelevant (birth disabled)
        hs.cooldown_range = (20, 20)
        hs.derive_effective(r_prime_static=3)
        return mc, hs

    def guards(self) -> dict:
        return {
            "warp_off": True,
            "birth_off": True,
            "spread_off": True,  # enforce classic numbers
        }
