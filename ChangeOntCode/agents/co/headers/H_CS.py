# agents/co/headers/H_CS.py
from .H_common import BaseHeader

class HeaderCS(BaseHeader):
    """
    Static classical header: dyn fixed near 0, small tolerances.
    """
    def apply_static(self):
        self.state.dyn = float(self.st.get("dyn_prior", 0.0))
        self.state.tag = "CS"
        # keep math classical
        self.math.path_algebra = "classical"
        self.math.number_arith = "classic"
        self.math.logic = "boolean"
