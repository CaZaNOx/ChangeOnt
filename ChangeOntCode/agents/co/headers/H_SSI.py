from __future__ import annotations

from .H_common import BaseHeader


class HeaderSSI(BaseHeader):
    """
    Stronger CO-sensitive regime header.

    Starts from a more dynamic prior and allows broader CO influence,
    but still does not force co_weight=1.0.
    """

    def apply_static(self) -> None:
        self.state.tag = "SSI"
        self.state.dyn = float(self.st.get("dyn_prior", 0.80))
        self.state.classicality = float(self.st.get("classicality_prior", 0.25))

        self.st.setdefault("co_base", 0.70)
        self.st.setdefault("anneal_beta", 0.010)

        self.math.path_algebra = "minplus"
        self.math.number_arith = "spread"
        self.math.logic = "quantale"