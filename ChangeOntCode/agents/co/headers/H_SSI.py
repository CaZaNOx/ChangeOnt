# agents/co/headers/H_SSI.py
from .H_common import BaseHeader

class HeaderSSI(BaseHeader):
    """
    Strong subject-influence header: high dyn, permissive tolerances.
    """
    def apply_static(self):
        self.state.dyn = float(self.st.get("dyn_prior", 0.85))
        self.state.tag = "SSI"
        self.math.path_algebra = "minplus"
        self.math.number_arith = "spread"
        self.math.logic = "quantale"
