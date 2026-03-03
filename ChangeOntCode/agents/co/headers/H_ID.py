from __future__ import annotations

from .H_common import BaseHeader


class HeaderID(BaseHeader):
    """
    Intermediate regime header.

    This is the "bridge" regime:
    - not strongly classical
    - not strongly CO-dominant
    - can move either way based on runtime evidence
    """

    def apply_static(self) -> None:
        self.state.tag = "ID"
        self.state.dyn = float(self.st.get("dyn_prior", 0.35))
        self.state.classicality = float(self.st.get("classicality_prior", 0.65))

        self.st.setdefault("co_base", 0.35)
        self.st.setdefault("anneal_beta", 0.006)

        self.math.path_algebra = "minplus"
        self.math.number_arith = "classic"
        self.math.logic = "boolean"