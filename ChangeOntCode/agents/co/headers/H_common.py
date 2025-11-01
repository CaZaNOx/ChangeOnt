# agents/co/headers/H_common.py
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Optional

@dataclass
class MathContext:
    path_algebra: str = "classical"   # 'classical' | 'minplus'
    number_arith: str = "classic"     # 'classic' | 'spread'
    logic: str        = "boolean"     # 'boolean' | 'quantale'
    def to_dict(self) -> Dict: 
        return asdict(self)

@dataclass
class HeaderState:
    # dynamicity (0 classical .. 1 strongly CO)
    dyn: float = 0.0
    tag: str = "CS"  # 'CS'|'ID'|'SSI'
    # effective tolerances (derived)
    tau_eff: float = 0.0
    eps_eff: float = 0.0
    # caps and knobs derived by router + static ranges
    alpha_cap: float = 0.0
    gamma_eff: float = 0.03
    cooldown_eff: int = 10
    # scheduling
    p_breadth: float = 0.2
    # precision / density
    r_prime: int = 1

class BaseHeader:
    """
    Static ranges define min/max per family.
    Dynamic state is stored in .state and tweaked by router.
    """
    def __init__(self, family: str = "maze", overrides: Optional[Dict] = None):
        self.family = family
        self.st: Dict = dict(overrides or {})
        # family presets (you can tune later)
        if family == "maze":
            self.st.setdefault("tau_range", (0.0, 2.0))
            self.st.setdefault("eps_range", (0.0, 0.25))
        elif family == "bandit":
            self.st.setdefault("tau_range", (0.0, 1.0))
            self.st.setdefault("eps_range", (0.0, 0.15))
        elif family == "renewal":
            self.st.setdefault("tau_range", (0.0, 3.0))
            self.st.setdefault("eps_range", (0.0, 0.35))
        else:
            self.st.setdefault("tau_range", (0.0, 1.0))
            self.st.setdefault("eps_range", (0.0, 0.25))

        self.st.setdefault("alpha_cap_range", (0.0, 0.9))
        self.st.setdefault("gamma_range", (0.01, 0.10))
        self.st.setdefault("cooldown_range", (5, 30))
        self.st.setdefault("dyn_prior", 0.0)

        self.math = MathContext()
        self.state = HeaderState(dyn=float(self.st["dyn_prior"]))
        # tag default
        self.state.tag = "CS"

    def apply_static(self):
        """Hook for concrete headers."""
        pass

    def derive_effective(self):
        """
        Map dyn in [0,1] into effective tolerances and caps within static ranges.
          tau_eff = lerp(tau_min, tau_max, dyn)
          eps_eff = lerp(eps_min, eps_max, dyn)
          alpha_cap increases with dyn
          gamma_eff decreases slightly with dyn
        """
        tau_min, tau_max = self.st["tau_range"]
        eps_min, eps_max = self.st["eps_range"]
        d = float(self.state.dyn)
        self.state.tau_eff = tau_min + d * (tau_max - tau_min)
        self.state.eps_eff = eps_min + d * (eps_max - eps_min)

        a0, a1 = self.st["alpha_cap_range"]
        self.state.alpha_cap = a0 + d * (a1 - a0)

        g0, g1 = self.st["gamma_range"]
        # flip: more dynamic → allow easier births (smaller gamma)
        self.state.gamma_eff = g1 - d * (g1 - g0)

        c0, c1 = self.st["cooldown_range"]
        self.state.cooldown_eff = int(round(c1 - d * (c1 - c0)))

        # clamp p_breadth if it already exists
        self.state.p_breadth = max(0.1, min(0.9, self.state.p_breadth))

    def guards(self) -> Dict[str, bool]:
        """
        Simple guard flags for elements (runners may ignore).
        """
        tag = self.state.tag
        return {
            "skip_heavy_co": (tag == "CS"),
            "prefer_minplus": (tag != "CS"),
        }
