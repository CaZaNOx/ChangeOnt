from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional

from agents.co.placement.control_defaults import apply_runtime_control_defaults
from agents.co.placement.regime import evaluate_regime_state
from agents.co.placement.control import runtime_contract_from_owner


@dataclass
class MathContext:
    path_algebra: str = "thin"
    number_arith: str = "standard"
    logic: str = "boolean"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class HeaderState:
    family: str = "maze"
    t: int = 0
    tag: str = "CS"
    regime: str = "stable"

    dyn: float = 0.0
    thinness: float = 1.0
    co_weight: float = 0.0

    tau_eff: float = 0.0
    eps_eff: float = 0.0
    alpha_cap: float = 0.0
    gamma_eff: float = 0.03
    cooldown_eff: int = 10
    p_breadth: float = 0.2
    r_prime: int = 1

    reeval_pressure: float = 0.0
    dyn_hint_last: float = 0.0
    regime_stability: float = 0.0
    regime_openness: float = 0.0
    regime_coherence: float = 0.0
    burden_accumulation: float = 0.0
    admissibility_decay: float = 0.0
    invariant_stability: float = 0.0
    history_dependence: float = 0.0
    scalarizability: float = 0.0
    collapse_readiness: float = 0.0
    representation_mode: str = "mixed"
    rigidity: float = 0.5
    volatility: float = 0.5
    reversibility: float = 0.5
    commitment_cost: float = 0.5
    observability: float = 0.5
    deformation_bandwidth: float = 0.5
    stability_horizon: float = 0.5
    identity_hardness: float = 0.5
    fracture_tolerance: float = 0.5
    retention_depth: float = 0.5
    collapse_permission: float = 0.5
    identity_support_threshold: float = 0.5
    evidence_gate: float = 0.5
    support_evidence: float = 0.0
    rival_breadth: float = 0.5
    nonlocal_authority: float = 0.5
    path_sensitivity: float = 0.5
    local_authority: float = 0.5
    support_carry_forward: float = 0.5
    revision_permissibility: float = 0.5
    collapse_admissibility: float = 0.5
    update_count: int = 0
    last_feedback_reward: float = 0.0
    last_done: bool = False


class BaseHeader:
    """
    Runtime header wrapper.

    Canonical responsibilities:
    - hold header-local state
    - expose static prior hooks for subclasses (CS/ID/SSI)
    - apply placement/regime evaluation results to state

    Non-canonical responsibilities such as placement estimation, posture control,
    and regime-shape evaluation live in agents.co.placement.
    """

    def __init__(
        self,
        family: str = "maze",
        overrides: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        self.family = str(family or "maze")
        self.st = apply_runtime_control_defaults(dict(overrides or {}), **kwargs)
        self.math = MathContext()
        self.state = HeaderState(
            family=self.family,
            dyn=float(self.st["dyn_prior"]),
            thinness=float(self.st.get("thinness_prior", self.st.get("classicality_prior", 1.0))),
        )
        self.apply_static()
        self.derive_effective()

    def apply_static(self) -> None:
        """Subclass hook for static prior mode selection."""
        raise NotImplementedError

    def _clamp01(self, x: float) -> float:
        return max(0.0, min(1.0, float(x)))

    def _runtime_contract(self) -> Dict[str, Any]:
        return runtime_contract_from_owner(self)

    def _runtime_contract_for_observation(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        """Return the active placement contract for the current public packet.

        Canonical placement is packet driven:
            public problem_contract -> shape_prior6 -> direct_controls

        The core-level runtime contract is only a construction-time default.
        Adapters normally provide ``problem_contract`` on each public packet; that
        packet contract must drive header controls or the six-question bridge is
        inert.
        """
        base = self._runtime_contract()
        if not isinstance(observation, dict):
            return base
        packet_problem = observation.get("problem_contract")
        if isinstance(packet_problem, dict) and packet_problem:
            try:
                from agents.co.core.contracts.placement_contract import build_runtime_contract

                payload: Dict[str, Any] = {"problem_contract": packet_problem}
                if isinstance(observation.get("shape_prior6"), dict):
                    payload["shape_prior6"] = observation.get("shape_prior6")
                if isinstance(observation.get("study_overrides"), dict):
                    payload["study_overrides"] = observation.get("study_overrides")
                return build_runtime_contract(payload)
            except Exception:
                return base
        return base

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
            "thinness": float(getattr(self.state, "thinness", 0.0)),
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
            "regime_stability": float(self.state.regime_stability),
            "regime_openness": float(self.state.regime_openness),
            "regime_coherence": float(self.state.regime_coherence),
            "burden_accumulation": float(self.state.burden_accumulation),
            "admissibility_decay": float(self.state.admissibility_decay),
            "invariant_stability": float(self.state.invariant_stability),
            "history_dependence": float(self.state.history_dependence),
            "scalarizability": float(self.state.scalarizability),
            "collapse_readiness": float(self.state.collapse_readiness),
            "representation_mode": str(self.state.representation_mode),
            "rigidity": float(self.state.rigidity),
            "volatility": float(self.state.volatility),
            "reversibility": float(self.state.reversibility),
            "commitment_cost": float(self.state.commitment_cost),
            "observability": float(self.state.observability),
            "deformation_bandwidth": float(self.state.deformation_bandwidth),
            "stability_horizon": float(self.state.stability_horizon),
            "identity_hardness": float(self.state.identity_hardness),
            "fracture_tolerance": float(self.state.fracture_tolerance),
            "retention_depth": float(self.state.retention_depth),
            "collapse_permission": float(self.state.collapse_permission),
            "identity_support_threshold": float(self.state.identity_support_threshold),
            "evidence_gate": float(self.state.evidence_gate),
            "support_evidence": float(self.state.support_evidence),
            "rival_breadth": float(self.state.rival_breadth),
            "nonlocal_authority": float(self.state.nonlocal_authority),
            "path_sensitivity": float(self.state.path_sensitivity),
            "local_authority": float(self.state.local_authority),
            "support_carry_forward": float(self.state.support_carry_forward),
            "revision_permissibility": float(self.state.revision_permissibility),
            "collapse_admissibility": float(self.state.collapse_admissibility),
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

        contract = self._runtime_contract_for_observation(observation)
        regime = evaluate_regime_state(
            observation,
            previous_dyn=float(self.state.dyn),
            previous_reeval_pressure=float(self.state.reeval_pressure),
            previous_thinness=float(getattr(self.state, "thinness", 0.0)),
            previous_regime=str(self.state.regime),
            config=self.st,
            contract=contract,
        )

        self.state.family = fam
        self.state.t = int(t)
        self.state.update_count += 1
        self.state.dyn = float(regime["dyn"])
        if regime.get("dyn_hint") is not None:
            self.state.dyn_hint_last = float(regime["dyn_hint"])
        self.state.thinness = float(regime.get("thinness", 0.0))
        self.state.co_weight = float(regime["co_weight"])
        self.state.regime = str(regime["regime"])
        self.state.regime_stability = float(regime["regime_stability"])
        self.state.regime_openness = float(regime["regime_openness"])
        self.state.regime_coherence = float(regime["regime_coherence"])
        self.state.burden_accumulation = float(regime["burden_accumulation"])
        self.state.admissibility_decay = float(regime["admissibility_decay"])
        self.state.invariant_stability = float(regime["invariant_stability"])
        self.state.history_dependence = float(regime["history_dependence"])
        self.state.scalarizability = float(regime["scalarizability"])
        self.state.collapse_readiness = float(regime["collapse_readiness"])
        self.state.representation_mode = str(regime["representation_mode"])
        self.state.last_feedback_reward = float(regime["reward"])
        self.state.last_done = bool(regime["done"])
        self.state.reeval_pressure = float(regime["reeval_pressure"])
        self.state.p_breadth = float(regime["p_breadth"])
        self.state.r_prime = int(regime["r_prime"])
        self.state.rigidity = float(regime["rigidity"])
        self.state.volatility = float(regime["volatility"])
        self.state.reversibility = float(regime["reversibility"])
        self.state.commitment_cost = float(regime["commitment_cost"])
        self.state.observability = float(regime["observability"])
        self.state.deformation_bandwidth = float(regime["deformation_bandwidth"])
        self.state.stability_horizon = float(regime["stability_horizon"])
        self.state.identity_hardness = float(regime["identity_hardness"])
        self.state.fracture_tolerance = float(regime["fracture_tolerance"])
        self.state.retention_depth = float(regime["retention_depth"])
        self.state.collapse_permission = float(regime["collapse_permission"])
        self.state.identity_support_threshold = float(regime["identity_support_threshold"])
        self.state.evidence_gate = float(regime["evidence_gate"])
        self.state.support_evidence = float(regime["support_evidence"])
        direct_controls = regime.get("direct_controls", regime.get("direct_environment_controls", {})) if isinstance(regime.get("direct_controls", regime.get("direct_environment_controls", {})), dict) else {}
        self.state.rival_breadth = float(direct_controls.get("rival_breadth", self.state.rival_breadth))
        self.state.nonlocal_authority = float(direct_controls.get("nonlocal_authority", self.state.nonlocal_authority))
        self.state.path_sensitivity = float(direct_controls.get("path_sensitivity", self.state.path_sensitivity))
        self.state.local_authority = float(direct_controls.get("local_authority", self.state.local_authority))
        self.state.support_carry_forward = float(direct_controls.get("support_carry_forward", self.state.support_carry_forward))
        self.state.revision_permissibility = float(direct_controls.get("revision_permissibility", self.state.revision_permissibility))
        self.state.collapse_admissibility = float(direct_controls.get("collapse_admissibility", self.state.collapse_admissibility))

        math_ctx = regime.get("math_context", {}) if isinstance(regime.get("math_context", {}), dict) else {}
        self.math.path_algebra = str(math_ctx.get("path_algebra", self.math.path_algebra))
        self.math.number_arith = str(math_ctx.get("number_arith", self.math.number_arith))
        self.math.logic = str(math_ctx.get("logic", self.math.logic))
        self.derive_effective()

        return {
            "header_mode": self.state.tag,
            "family": fam,
            "t": int(t),
            "co_weight": float(self.state.co_weight),
            "dyn_est": float(self.state.dyn),
            "thinness_est": float(getattr(self.state, "thinness", 0.0)),
            "collapse_readiness": float(self.state.collapse_readiness),
            "collapse_permission": float(self.state.collapse_permission),
            "history_dependence": float(self.state.history_dependence),
            "representation_mode": str(self.state.representation_mode),
            "reeval_pressure": float(self.state.reeval_pressure),
            "identity_hardness": float(self.state.identity_hardness),
            "fracture_tolerance": float(self.state.fracture_tolerance),
            "retention_depth": float(self.state.retention_depth),
            "identity_support_threshold": float(self.state.identity_support_threshold),
            "evidence_gate": float(self.state.evidence_gate),
            "support_evidence": float(self.state.support_evidence),
            "rival_breadth": float(self.state.rival_breadth),
            "nonlocal_authority": float(self.state.nonlocal_authority),
            "path_sensitivity": float(self.state.path_sensitivity),
            "local_authority": float(self.state.local_authority),
            "support_carry_forward": float(self.state.support_carry_forward),
            "revision_permissibility": float(self.state.revision_permissibility),
            "collapse_admissibility": float(self.state.collapse_admissibility),
            "shape_prior6_bundle": regime.get("shape_prior6_bundle", {}),
            "direct_controls": regime.get("direct_controls", {}),
            "direct_environment_controls": regime.get("direct_environment_controls", {}),
            "regime": self.state.regime,
            "regime_stability": float(self.state.regime_stability),
            "regime_openness": float(self.state.regime_openness),
            "regime_coherence": float(self.state.regime_coherence),
        }
