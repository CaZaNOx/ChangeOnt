"""Regime helpers for interpreting the six-question public shape basis.

This module keeps placement language generic so adapters do not become hidden
solvers.
"""
from __future__ import annotations

from typing import Any, Dict, Mapping

from .control import clamp01, apply_direct_controls, direct_kernel_controls_from_contract, shape_prior6_axis_values_from_contract
from agents.co.core.contracts.problem_contract import derive_goal_field


def _safe_sig(src: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    try:
        return clamp01(float(src.get(key, default) or default))
    except Exception:
        return clamp01(default)


def _math_context_for_regime(regime: str) -> Dict[str, str]:
    if regime == "discrete_stable":
        return {"path_algebra": "thin", "number_arith": "standard", "logic": "boolean"}
    if regime == "dynamic":
        return {"path_algebra": "minplus", "number_arith": "spread", "logic": "quantale"}
    if regime == "reopening":
        return {"path_algebra": "minplus", "number_arith": "spread", "logic": "boolean"}
    return {"path_algebra": "minplus", "number_arith": "standard", "logic": "boolean"}


def evaluate_regime_state(
    observation: Mapping[str, Any],
    *,
    previous_dyn: float,
    previous_reeval_pressure: float,
    previous_thinness: float,
    previous_regime: str,
    config: Mapping[str, Any],
    contract: Mapping[str, Any] | None = None,
    study_posture: Mapping[str, Any] | None = None,
) -> Dict[str, Any]:
    contract = contract if isinstance(contract, Mapping) else {}
    shape_axes = shape_prior6_axis_values_from_contract(contract)
    hidden = clamp01(shape_axes.get("hidden_decisiveness", 0.5))
    reshape = clamp01(shape_axes.get("reshapeability", 0.5))
    local_reliability = clamp01(shape_axes.get("local_cue_reliability", 0.5))
    revision_cost = clamp01(shape_axes.get("revision_cost", 0.5))
    consequence_span = clamp01(shape_axes.get("consequence_span", 0.5))
    topology_constraint = clamp01(shape_axes.get("topology_constraint", 0.5))
    direct_controls = direct_kernel_controls_from_contract(contract)

    dyn_hint_raw = observation.get("dyn_hint", None)
    dyn_hint = None
    if dyn_hint_raw is not None:
        try: dyn_hint = clamp01(float(dyn_hint_raw))
        except Exception: dyn_hint = None
    co_conf_raw = observation.get("co_conf_hint", None)
    co_conf_hint = None
    if co_conf_raw is not None:
        try: co_conf_hint = clamp01(float(co_conf_raw))
        except Exception: co_conf_hint = None

    goal_field = derive_goal_field(observation)
    goal_sharp = _safe_sig(goal_field, "goal_sharpness", 0.5)
    goal_stab = _safe_sig(goal_field, "goal_stability", 0.5)
    goal_cert = _safe_sig(goal_field, "goal_certainty", 0.5)

    reward = 0.0
    done = False
    fb = observation.get("feedback", None)
    if isinstance(fb, Mapping):
        try: reward = float(fb.get("reward", 0.0) or 0.0)
        except Exception: reward = 0.0
        done = bool(fb.get("done", False))

    ks = observation.get("_kernel_substrate", {}) if isinstance(observation, Mapping) else {}
    cmpf = ks.get("comparison", {}) if isinstance(ks.get("comparison", {}), Mapping) else {}
    admf = ks.get("admissibility", {}) if isinstance(ks.get("admissibility", {}), Mapping) else {}
    regf = ks.get("regime", {}) if isinstance(ks.get("regime", {}), Mapping) else {}
    regsig = ks.get("regime_signature", {}) if isinstance(ks.get("regime_signature", {}), Mapping) else {}
    conf = ks.get("continuation", {}) if isinstance(ks.get("continuation", {}), Mapping) else {}

    continuity = _safe_sig(cmpf, "continuity_conf", 0.0)
    fracture = _safe_sig(cmpf, "fracture_pressure", 0.0)
    admiss = _safe_sig(admf, "identity_admissibility", 0.0)
    closure = _safe_sig(admf, "closure_stability", 0.0)
    admiss_loss = _safe_sig(admf, "admissible_loss", 0.0)
    gauge = _safe_sig(regf, "gauge_coherence", 0.0)
    substrate_dyn = _safe_sig(regf, "router_dyn", 0.0)
    substrate_reeval = _safe_sig(regf, "reeval_pressure", 0.0)
    burden = _safe_sig(conf, "remaining_transformation_burden", 0.0)
    frame_shift = _safe_sig(regf, "frame_shift", substrate_dyn)

    if dyn_hint is None and substrate_dyn > 0.0:
        dyn_hint = substrate_dyn
    if co_conf_hint is None and admiss > 0.0:
        co_conf_hint = admiss

    stability = clamp01(0.35 * continuity + 0.25 * admiss + 0.20 * gauge + 0.20 * closure)
    openness = clamp01(0.35 * burden + 0.25 * fracture + 0.15 * frame_shift + 0.15 * admiss_loss + 0.10 * substrate_reeval)
    coherence = clamp01(0.50 * gauge + 0.25 * continuity + 0.25 * admiss)
    burden_acc = clamp01(regsig.get("burden_accumulation", burden))
    adm_decay = clamp01(regsig.get("admissibility_decay", admiss_loss))
    inv_stability = clamp01(regsig.get("invariant_stability", stability))
    history_dep = clamp01(regsig.get("history_dependence", substrate_dyn * 0.5))
    scalarizability = clamp01(regsig.get("scalarizability", goal_sharp * goal_stab * goal_cert))
    collapse_readiness = clamp01(regsig.get("collapse_readiness", 0.0))
    if regsig:
        stability = clamp01(0.55 * stability + 0.45 * clamp01(regsig.get("stability", stability)))
        openness = clamp01(0.55 * openness + 0.45 * clamp01(regsig.get("openness", openness)))
        coherence = clamp01(0.55 * coherence + 0.45 * clamp01(regsig.get("coherence", coherence)))

    c_collapse = clamp01(direct_controls.get("collapse_admissibility", 0.5))
    c_revision = clamp01(direct_controls.get("revision_permissibility", 0.5))
    c_carry = clamp01(direct_controls.get("support_carry_forward", 0.5))
    c_breadth = clamp01(direct_controls.get("rival_breadth", 0.5))
    c_nonlocal = clamp01(direct_controls.get("nonlocal_authority", 0.5))
    c_path = clamp01(direct_controls.get("path_sensitivity", 0.5))
    c_local = clamp01(direct_controls.get("local_authority", 0.5))

    # Apply direct controls derived from the canonical six-question runtime basis.
    stability = clamp01((1.0 - 0.16 * c_carry) * stability + 0.16 * c_carry * (0.45 * local_reliability + 0.35 * (1.0 - reshape) + 0.20 * (1.0 - hidden)))
    openness = clamp01((1.0 - 0.16 * c_revision) * openness + 0.16 * c_revision * (0.35 * revision_cost + 0.30 * reshape + 0.20 * hidden + 0.15 * consequence_span))
    coherence = clamp01((1.0 - 0.12 * c_local) * coherence + 0.12 * c_local * (0.55 * local_reliability + 0.25 * (1.0 - hidden) + 0.20 * (1.0 - reshape)))
    burden_acc = clamp01((1.0 - 0.12 * c_nonlocal) * burden_acc + 0.12 * c_nonlocal * (0.55 * consequence_span + 0.25 * reshape + 0.20 * hidden))
    history_dep = clamp01((1.0 - 0.12 * c_path) * history_dep + 0.12 * c_path * (0.40 * consequence_span + 0.25 * topology_constraint + 0.20 * revision_cost + 0.15 * reshape))

    meta = observation.get("meta_header", {}) if isinstance(observation.get("meta_header", {}), Mapping) else {}
    profile = dict(meta.get("regime_shape", {}) or {})
    rigidity = clamp01(profile.get("rigidity", 0.5))
    volatility_prior = clamp01(profile.get("volatility", 0.5))
    reversibility = clamp01(profile.get("reversibility", 0.5))
    commitment_cost = clamp01(profile.get("commitment_cost", 0.5))
    observability = clamp01(profile.get("observability", 0.5))
    deformation_bandwidth = clamp01(profile.get("deformation_bandwidth", 0.5))
    stability_horizon = clamp01(profile.get("stability_horizon", 0.5))

    shock = 0.0
    if dyn_hint is not None:
        shock = max(shock, abs(float(dyn_hint) - float(previous_dyn)))
    if fb is not None:
        shock = max(shock, min(1.0, abs(reward)))
    fu = observation.get("field_update", {}) if isinstance(observation.get("field_update", {}), Mapping) else {}
    if fu:
        try:
            shock = max(shock, clamp01(float(fu.get("fracture_update", 0.0) or 0.0)))
            shock = max(shock, 0.5 * clamp01(float(fu.get("branch_update", 0.0) or 0.0)))
        except Exception:
            pass
    if bool(observation.get("shift_alert", False)):
        shock = max(shock, 1.0)

    pressure = clamp01(0.45 * openness + 0.35 * (1.0 - stability) + 0.20 * shock)
    pa = float(config.get("pressure_alpha", 0.20))
    reeval_pressure = (1.0 - pa) * float(previous_reeval_pressure) + pa * pressure

    dyn_target = clamp01(0.34 * openness + 0.18 * reeval_pressure + 0.12 * (1.0 - stability) + 0.10 * history_dep + 0.08 * c_revision + 0.08 * c_nonlocal + 0.06 * (1.0 - collapse_readiness) + 0.04 * reshape)
    if dyn_hint is not None:
        dyn_target = clamp01(0.7 * dyn_target + 0.3 * float(dyn_hint))
    alpha = float(config.get("dyn_alpha", 0.25))
    dyn = clamp01((1.0 - alpha) * previous_dyn + alpha * dyn_target)

    thinness_prior = clamp01(float(config.get("thinness_prior", 1.0)))
    static_pull = goal_sharp * goal_stab * goal_cert
    thinness_target = clamp01(thinness_prior * static_pull * stability * (1.0 - 0.45 * openness) * (0.65 + 0.35 * scalarizability) * (0.70 + 0.30 * collapse_readiness))
    thinness = clamp01(0.75 * float(previous_thinness) + 0.25 * thinness_target)

    rigidity_eff = clamp01(0.65 * rigidity + 0.35 * stability)
    volatility_eff = clamp01(0.60 * volatility_prior + 0.40 * openness)
    deformation_eff = clamp01(0.60 * deformation_bandwidth + 0.40 * openness)
    support_evidence = observation.get("support_evidence", None)
    if support_evidence is None:
        support_evidence = 0.32 * goal_cert + 0.20 * stability + 0.16 * coherence + 0.12 * c_local + 0.10 * c_carry + 0.10 * max(0.0, min(1.0, float(co_conf_hint if co_conf_hint is not None else admiss)))
    support_evidence = clamp01(support_evidence)
    identity_hardness = clamp01(0.18 * rigidity_eff + 0.14 * observability + 0.08 * stability_horizon + 0.08 * (1.0 - volatility_eff) + 0.08 * c_carry + 0.08 * c_local + 0.08 * (1.0 - hidden) + 0.06 * (1.0 - reversibility))
    identity_support_threshold = clamp01(0.28 + 0.18 * volatility_eff + 0.14 * commitment_cost + 0.12 * c_revision + 0.10 * c_nonlocal - 0.10 * c_collapse - 0.08 * c_local - 0.08 * (1.0 - hidden) - 0.06 * observability)
    fracture_tolerance = clamp01(0.18 + 0.18 * volatility_eff + 0.18 * c_revision + 0.10 * c_breadth + 0.06 * c_nonlocal - 0.08 * c_carry - 0.06 * rigidity_eff)
    retention_depth = clamp01(0.18 + 0.16 * stability_horizon + 0.12 * rigidity_eff + 0.12 * c_carry + 0.08 * c_path + 0.06 * c_local - 0.10 * c_revision)
    collapse_permission = clamp01(0.18 * rigidity_eff + 0.14 * stability + 0.10 * thinness + 0.16 * c_collapse + 0.10 * c_local - 0.12 * c_revision - 0.10 * c_nonlocal - 0.06 * commitment_cost)

    axis_controls = apply_direct_controls(direct_controls, identity_support_threshold=identity_support_threshold, fracture_tolerance=fracture_tolerance, retention_depth=retention_depth, collapse_permission=collapse_permission, support_evidence=support_evidence)
    identity_support_threshold = float(axis_controls["identity_support_threshold"])
    fracture_tolerance = float(axis_controls["fracture_tolerance"])
    retention_depth = float(axis_controls["retention_depth"])
    collapse_permission = float(axis_controls["collapse_permission"])
    support_evidence = float(axis_controls["support_evidence"])
    evidence_gate = float(axis_controls["evidence_gate"])

    posture_controls: Dict[str, Any] = {}
    if isinstance(study_posture, Mapping) and study_posture.get("axes"):
        from .control import apply_posture_controls
        posture_controls = apply_posture_controls(study_posture, identity_support_threshold=identity_support_threshold, fracture_tolerance=fracture_tolerance, retention_depth=retention_depth, collapse_permission=collapse_permission, support_evidence=support_evidence)
        identity_support_threshold = float(posture_controls["identity_support_threshold"])
        fracture_tolerance = float(posture_controls["fracture_tolerance"])
        retention_depth = float(posture_controls["retention_depth"])
        collapse_permission = float(posture_controls["collapse_permission"])
        evidence_gate = float(posture_controls["evidence_gate"])

    co_base = clamp01(float(config.get("co_base", 0.25)))
    anneal_beta = max(0.0, float(config.get("anneal_beta", 0.005)))
    step_idx = int(observation.get("t", observation.get("step", 0)) or 0)
    anneal = 1.0 / (1.0 + anneal_beta * max(0, step_idx))
    raw_weight = co_base * anneal
    raw_weight += 0.35 * dyn + 0.20 * reeval_pressure + 0.12 * openness + 0.08 * (1.0 - stability) + 0.08 * (1.0 - coherence) + 0.08 * history_dep + 0.08 * burden_acc + 0.08 * adm_decay + 0.10 * float(co_conf_hint if co_conf_hint is not None else admiss)
    raw_weight -= 0.28 * thinness + 0.12 * collapse_permission
    co_weight = clamp01(raw_weight)

    if collapse_permission >= 0.70 and history_dep <= 0.40 and burden_acc <= 0.25 and adm_decay <= 0.25 and stability >= 0.62:
        regime = "discrete_stable"
    elif thinness >= 0.78 and reeval_pressure <= 0.12 and stability >= 0.65:
        regime = "discrete_stable"
    elif previous_regime == "reopening" and reeval_pressure >= 0.25:
        regime = "reopening"
    elif reeval_pressure >= 0.45 or shock >= 0.55:
        regime = "reopening"
    elif dyn >= 0.62 or openness >= 0.58:
        regime = "dynamic"
    elif stability >= 0.58 and coherence >= 0.55:
        regime = "stable"
    else:
        regime = "mixed"

    shape_bundle = {
        "schema": "co_shape_prior6_runtime_bundle_v1",
        "axes": dict(shape_axes),
        "direct_controls": dict(direct_controls),
        "source": "shape_prior6",
    }

    return {
        "goal_field": goal_field,
        "shape_prior6_bundle": shape_bundle,
        "direct_controls": dict(direct_controls),
        # Backward-compatible telemetry names; not an environment-basis path.
        "direct_environment_controls": dict(direct_controls),
        "reward": reward,
        "done": done,
        "dyn": dyn,
        "dyn_hint": dyn_hint,
        "thinness": thinness,
        "co_weight": co_weight,
        "regime": regime,
        "regime_stability": stability,
        "regime_openness": openness,
        "regime_coherence": coherence,
        "burden_accumulation": burden_acc,
        "admissibility_decay": adm_decay,
        "invariant_stability": inv_stability,
        "history_dependence": history_dep,
        "scalarizability": scalarizability,
        "collapse_readiness": collapse_readiness,
        "representation_mode": str(regsig.get("mode", "mixed" if collapse_readiness < 0.70 else "thin")),
        "reeval_pressure": reeval_pressure,
        "rigidity": rigidity_eff,
        "volatility": volatility_eff,
        "reversibility": reversibility,
        "commitment_cost": commitment_cost,
        "observability": observability,
        "deformation_bandwidth": deformation_eff,
        "stability_horizon": stability_horizon,
        "identity_hardness": identity_hardness,
        "fracture_tolerance": fracture_tolerance,
        "retention_depth": retention_depth,
        "collapse_permission": collapse_permission,
        "identity_support_threshold": identity_support_threshold,
        "evidence_gate": evidence_gate,
        "support_evidence": support_evidence,
        "study_override_controls": posture_controls,
        "math_context": _math_context_for_regime(regime),
        "p_breadth": max(0.1, min(0.9, 0.15 + 0.55 * openness + 0.10 * reeval_pressure)),
        "r_prime": 1 + int(round(2.0 * openness + 1.0 * reeval_pressure)),
    }
