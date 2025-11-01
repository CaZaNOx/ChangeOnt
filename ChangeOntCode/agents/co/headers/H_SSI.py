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

    def update(self, observation: dict) -> dict:
        """
        Light-weight per-step header update:
        - surfaces family & t to downstream
        - computes a co_weight in [0,1] (how much we bias toward CO decisions)
        - optionally incorporates a dyn_hint from the observation
        Returns a small dict that the pipeline/elements can merge into their metrics.
        """
        # 1) Pull basics from observation
        fam = observation.get("family")
        t_raw = observation.get("t", 0)
        try:
            t = int(t_raw) if t_raw is not None else 0
        except Exception:
            t = 0

        # 2) Optional dynamic hint from the env/adapter (0..1: more dynamic => higher)
        dyn_hint = observation.get("dyn_hint", None)
        try:
            # keep an exponentially-smoothed dyn in the header state
            prev_dyn = float(getattr(self.state, "dyn", self.st.get("dyn_prior", 0.85)))
        except Exception:
            prev_dyn = float(self.st.get("dyn_prior", 0.85))

        if dyn_hint is not None:
            try:
                alpha = float(self.st.get("dyn_alpha", 0.3))  # smoothing for dyn
            except Exception:
                alpha = 0.3
            try:
                new_dyn = (1.0 - alpha) * prev_dyn + alpha * float(dyn_hint)
            except Exception:
                new_dyn = prev_dyn
        else:
            new_dyn = prev_dyn

        # 3) Make a co_weight schedule (higher early, anneal a bit with t, depend on dyn)
        #    co_base is an env prior; anneal_beta controls how fast it cools down with time.
        try:
            co_base = float(self.st.get("co_base", 0.7))
        except Exception:
            co_base = 0.7
        try:
            anneal_beta = float(self.st.get("anneal_beta", 0.01))
        except Exception:
            anneal_beta = 0.01

        anneal = 1.0 / (1.0 + anneal_beta * max(0, t))
        # blend base, anneal, and dynamic level; clamp to [0,1]
        co_weight = co_base * anneal * (0.5 + 0.5 * max(0.0, min(1.0, new_dyn)))
        co_weight = max(0.0, min(1.0, co_weight))

        # 4) Store into header.state (support both attr-style and dict-style state)
        #    (Your BaseHeader typically exposes an object; we also try mapping style for safety.)
        try:
            self.state.co_weight = float(co_weight)
            self.state.dyn = float(new_dyn)
            self.state.family = fam
            self.state.t = int(t)
        except Exception:
            try:
                self.state["co_weight"] = float(co_weight)
                self.state["dyn"] = float(new_dyn)
                self.state["family"] = fam
                self.state["t"] = int(t)
            except Exception:
                pass  # remain best-effort

        # 5) Return a compact record (pipeline/elements can merge/log this)
        return {
            "header_mode": "SSI",
            "t": t,
            "family": fam,
            "co_weight": float(co_weight),
            "dyn_est": float(new_dyn),
        }