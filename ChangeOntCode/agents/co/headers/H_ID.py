# agents/co/headers/H_ID.py
from .H_common import BaseHeader

class HeaderID(BaseHeader):
    """
    Intermediate dynamic header (router will move dyn across 0..1).
    """
    def apply_static(self):
        # dyn_prior might be >0 for semi-dynamic families (bandit/renewal)
        self.state.dyn = float(self.st.get("dyn_prior", 0.25))
        self.state.tag = "ID"
        # start hybrid math; router adjusts further
        self.math.path_algebra = "minplus"
        self.math.number_arith = "classic"
        self.math.logic = "boolean"
