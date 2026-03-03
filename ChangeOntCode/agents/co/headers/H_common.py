from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional


@dataclass
class MathContext:
    path_algebra: str = "classical"   # classical | minplus
    number_arith: str = "classic"     # classic | spread
    logic: str = "boolean"            # boolean | quantale

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class HeaderState:
    # regime / identity
    family: str = "maze"
    t: int = 0
    tag: str = "CS"                   # CS | ID | SSI
    regime: str = "stable"

    # dynamicity / classicality
    dyn: float = 0.0                  # 0 classical .. 1 strongly CO-relevant
    classicality: float = 1.0         # 1 highly classical .. 0 weakly classical
    co_weight: float = 0.0            # final local CO contribution weight

    # derived controls
    tau_eff: float = 0.0
    eps_eff: float = 0.0
    alpha_cap: float = 0.0
    gamma_eff: float = 0.03
    cooldown_eff: int = 10
    p_breadth: float = 0.2
    r_prime: int = 1

    # monitoring
    reeval_pressure: float = 0.0
    dyn_hint_last: float = 0.0
    update_count: int = 0
    last_feedback_reward: float = 0.0
    last_done: bool = False


class BaseHeader:
    """
    Target-state header base:
    - keeps prior/static family presets
    - updates live runtime regime
    - computes a local co_weight instead of leaving ActionHead stuck at 1.0
    - remains distinct from MetaHeader
    """

    def __init__(
        self,
        family: str = "maze",
        overrides: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        self.family = str(family or "maze")
        self.st: Dict[str, Any] = dict(overrides or {})
        self.st.update(kwargs)

        # family-local defaults
        if self.family == "maze":
            self.st.setdefault("tau_range", (0.0, 2.0))
            self.st.setdefault("eps_range", (0.0, 0.25))
        elif self.family == "bandit":
            self.st.setdefault("tau_range", (0.0, 1.0))
            self.st.setdefault("eps_range", (0.0, 0.15))
        elif self.family == "renewal":
            self.st.setdefault("tau_range", (0.0, 3.0))
            self.st.setdefault("eps_range", (0.0, 0.35))
        else:
            self.st.setdefault("tau_range", (0.0, 1.0))
            self.st.setdefault("eps_range", (0.0, 0.25))

        self.st.setdefault("alpha_cap_range", (0.0, 0.9))
        self.st.setdefault("gamma_range", (0.01, 0.10))
        self.st.setdefault("cooldown_range", (5, 30))

        # regime priors
        self.st.setdefault("dyn_prior", 0.0)
        self.st.setdefault("classicality_prior", 1.0)
        self.st.setdefault("co_base", 0.25)
        self.st.setdefault("anneal_beta", 0.005)
        self.st.setdefault("dyn_alpha", 0.25)
        self.st.setdefault("pressure_alpha", 0.20)

        self.math = MathContext()
        self.state = HeaderState(
            family=self.family,
            dyn=float(self.st["dyn_prior"]),
            classicality=float(self.st["classicality_prior"]),
        )

        self.apply_static()
        self.derive_effective()

    def apply_static(self) -> None:
        """
        Hook for subclasses to set:
        - state.tag
        - state.dyn
        - state.classicality
        - math mode defaults
        """
        pass

    def _clamp01(self, x: float) -> float:
        return max(0.0, min(1.0, float(x)))

    def derive_effective(self) -> None:
        tau_min, tau_max = self.st["tau_range"]
        eps_min, eps_max = self.st["eps_range"]
        d = self._clamp01(self.state.dyn)

        self.state.tau_eff = float(tau_min) + d * (float(tau_max) - float(tau_min))
        self.state.eps_eff = float(eps_min) + d * (float(eps_max) - float(eps_min))

        a0, a1 = self.st["alpha_cap_range"]
        self.state.alpha_cap = float(a0) + d * (float(a1) - float(a0))

        g0, g1 = self.st["gamma_range"]
        self.state.gamma_eff = float(g1) - d * (float(g1) - float(g0))

        c0, c1 = self.st["cooldown_range"]
        self.state.cooldown_eff = int(round(float(c1) - d * (float(c1) - float(c0))))

        self.state.p_breadth = max(0.1, min(0.9, float(self.state.p_breadth)))

    def guards(self) -> Dict[str, bool]:
        tag = self.state.tag
        return {
            "skip_heavy_co": (tag == "CS"),
            "prefer_minplus": (tag != "CS"),
        }

    def export_state(self) -> Dict[str, Any]:
        return {
            "family": self.state.family,
            "t": int(self.state.t),
            "tag": self.state.tag,
            "regime": self.state.regime,
            "dyn": float(self.state.dyn),
            "classicality": float(self.state.classicality),
            "co_weight": float(self.state.co_weight),
            "tau_eff": float(self.state.tau_eff),
            "eps_eff": float(self.state.eps_eff),
            "alpha_cap": float(self.state.alpha_cap),
            "gamma_eff": float(self.state.gamma_eff),
            "cooldown_eff": int(self.state.cooldown_eff),
            "p_breadth": float(self.state.p_breadth),
            "r_prime": int(self.state.r_prime),
            "reeval_pressure": float(self.state.reeval_pressure),
            "dyn_hint_last": float(self.state.dyn_hint_last),
            "update_count": int(self.state.update_count),
            "math": self.math.to_dict(),
        }

    def update(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        fam = str(observation.get("family", self.state.family or self.family))
        t_raw = observation.get("t", observation.get("step", self.state.t))
        try:
            t = int(t_raw)
        except Exception:
            t = int(self.state.t)

        # Optional explicit dynamic hint from env/adapter
        dyn_hint_raw = observation.get("dyn_hint", None)
        dyn_hint: Optional[float] = None
        if dyn_hint_raw is not None:
            try:
                dyn_hint = self._clamp01(float(dyn_hint_raw))
            except Exception:
                dyn_hint = None

        # Feedback-derived pressure (if available)
        reward = 0.0
        done = False
        fb = observation.get("feedback", None)
        if isinstance(fb, dict):
            try:
                reward = float(fb.get("reward", 0.0) or 0.0)
            except Exception:
                reward = 0.0
            done = bool(fb.get("done", False))

        # Re-evaluation pressure: explicit shift or local surprise proxy
        pressure = 0.0
        if dyn_hint is not None:
            pressure = abs(float(dyn_hint) - float(self.state.dyn))
        if fb is not None:
            pressure = max(pressure, min(1.0, abs(reward)))
        if bool(observation.get("shift_alert", False)):
            pressure = max(pressure, 1.0)

        pa = float(self.st.get("pressure_alpha", 0.20))
        self.state.reeval_pressure = (1.0 - pa) * float(self.state.reeval_pressure) + pa * float(pressure)

        # Dynamicity update
        prev_dyn = float(self.state.dyn)
        if dyn_hint is not None:
            alpha = float(self.st.get("dyn_alpha", 0.25))
            new_dyn = (1.0 - alpha) * prev_dyn + alpha * dyn_hint
        else:
            # without explicit hint, let pressure gently reopen
            new_dyn = prev_dyn * 0.98 + 0.15 * float(self.state.reeval_pressure)

        self.state.dyn = self._clamp01(new_dyn)
        self.state.dyn_hint_last = float(dyn_hint if dyn_hint is not None else self.state.dyn_hint_last)

        # Classicality is inverse-like but not simply 1-dyn:
        # high pressure reduces classical confidence
        classicality_prior = self._clamp01(float(self.st.get("classicality_prior", 1.0)))
        classicality = classicality_prior * (1.0 - 0.65 * self.state.dyn) * (1.0 - 0.50 * self.state.reeval_pressure)
        self.state.classicality = self._clamp01(classicality)

        # co_weight:
        # higher dyn and lower classicality -> more CO influence
        co_base = self._clamp01(float(self.st.get("co_base", 0.25)))
        anneal_beta = max(0.0, float(self.st.get("anneal_beta", 0.005)))
        anneal = 1.0 / (1.0 + anneal_beta * max(0, t))

        raw_weight = co_base * anneal * (0.35 + 0.65 * self.state.dyn) * (1.0 - 0.75 * self.state.classicality)

        # reopen slightly if pressure is high
        raw_weight += 0.30 * self.state.reeval_pressure

        self.state.co_weight = self._clamp01(raw_weight)

        # regime label
        if self.state.classicality >= 0.80 and self.state.reeval_pressure <= 0.10:
            self.state.regime = "high_classicality"
        elif self.state.reeval_pressure >= 0.45:
            self.state.regime = "reopening"
        elif self.state.dyn >= 0.60:
            self.state.regime = "dynamic"
        else:
            self.state.regime = "mixed"

        self.state.family = fam
        self.state.t = int(t)
        self.state.update_count += 1
        self.state.last_feedback_reward = float(reward)
        self.state.last_done = bool(done)

        self.derive_effective()

        return {
            "header_mode": self.state.tag,
            "family": fam,
            "t": int(t),
            "co_weight": float(self.state.co_weight),
            "dyn_est": float(self.state.dyn),
            "classicality_est": float(self.state.classicality),
            "reeval_pressure": float(self.state.reeval_pressure),
            "regime": self.state.regime,
        }