from __future__ import annotations

from .H_common import BaseHeader


class HeaderCS(BaseHeader):
    """
    Classical-stable prior header.

    Strong prior toward:
    - fixed-rule handling
    - low CO influence
    - strong classical collapse unless runtime pressure reopens it
    """

    def apply_static(self) -> None:
        self.state.tag = "CS"
        self.state.dyn = float(self.st.get("dyn_prior", 0.05))
        self.state.classicality = float(self.st.get("classicality_prior", 0.95))

        # conservative CO bias
        self.st.setdefault("co_base", 0.12)
        self.st.setdefault("anneal_beta", 0.003)

        self.math.path_algebra = "classical"
        self.math.number_arith = "classic"
        self.math.logic = "boolean"