"""Maintenance/replacement boundary adapter.

Publishes public effects for run/inspect/repair/replace style actions so the
kernel can derive relation and burden structure without using oracle health or
baseline-policy conclusions.
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional

from agents.co.adapters.common import ensure_signal_bus, public_effect, single_decision_slot_effect
from agents.co.boundary.problem_packet import (
    make_problem_packet,
    validate_problem_packet,
    validate_problem_update,
    attach_contract_debug,
    require_kernel_action,
)
from agents.co.boundary.update_mapper import map_feedback_update
from agents.co.placement.shape_prior6 import normalize_shape_prior6
from environments.maintenance_replacement.env import ACTIONS


def _clip01(x: Any, default: float = 0.5) -> float:
    try:
        return max(0.0, min(1.0, float(x)))
    except Exception:
        return float(default)


def _maintenance_public_effects(
    action: str,
    *,
    degradation: float,
    recovery: float,
    maintenance_need: float,
    uncertainty: float,
    health_known: bool,
    failure_penalty: float,
) -> List[Dict[str, Any]]:
    """Public burden/effect facts for maintenance.

    These facts describe public transition grammar only: degradation can be
    carried, inspection can expose hiddenness, repair can reduce degradation,
    replacement can reset degradation-state burden, and the immediate action
    candidates compete for one decision slot.  They are not value estimates or
    optimality hints.
    """
    effects: List[Dict[str, Any]] = [single_decision_slot_effect("maintenance_action_slot")]
    deg_pressure = _clip01(0.45 * degradation + 0.45 * maintenance_need + 0.10 * min(1.0, failure_penalty / 12.0))
    hidden_pressure = _clip01(uncertainty)
    if action == "RUN":
        effects.append(public_effect("carry", "degradation", magnitude=max(0.05, deg_pressure), scope="machine_health", public_basis="declared_transition_rule", direction="postpone_or_amplify", coupling="health_continuation"))
        if hidden_pressure > 0.20:
            effects.append(public_effect("carry", "hiddenness", magnitude=hidden_pressure, scope="health_observability", kind="uncertainty", public_basis="visible_observation", direction="mask_or_postpone", coupling="health_continuation"))
    elif action == "INSPECT":
        effects.append(public_effect("reveal", "hiddenness", magnitude=max(0.05, hidden_pressure), scope="health_observability", kind="evidence", public_basis="declared_transition_rule", direction="expose", coupling="health_continuation"))
    elif action == "REPAIR":
        effects.append(public_effect("reduce", "degradation", magnitude=max(0.05, maintenance_need), scope="machine_health", public_basis="declared_transition_rule", direction="relieve", coupling="health_continuation"))
    elif action == "REPLACE":
        effects.append(public_effect("reset", "degradation", magnitude=max(0.05, _clip01(0.70 * maintenance_need + 0.30 * degradation)), scope="machine_health", public_basis="declared_transition_rule", direction="cancel_or_reset", coupling="machine_identity"))
    elif action == "WAIT":
        if recovery > 0.0:
            effects.append(public_effect("buffer", "degradation", magnitude=max(0.05, _clip01(recovery * max(0.10, maintenance_need))), scope="machine_health", public_basis="declared_transition_rule", direction="absorb", coupling="health_continuation"))
        else:
            effects.append(public_effect("carry", "degradation", magnitude=max(0.05, deg_pressure * 0.65), scope="machine_health", public_basis="declared_transition_rule", direction="postpone", coupling="health_continuation"))
    return effects


class COAdapterMaintenanceReplacement:
    """CO adapter for the maintenance/replacement MDP.

    Boundary rule: this adapter may expose public action legality, observed health,
    public costs/probabilities, and local feedback. It must not expose true hidden
    health when the environment did not reveal it, value-iteration scores, optimal
    thresholds, or a best-action ranking.
    """

    def __init__(self, core: Any, name: str = "CO_MAINT", shape_prior6_override: Optional[Mapping[str, Any]] = None) -> None:
        self.core = core
        self.name = str(name)
        # Study-only override used by validation scripts to test wrong-shape
        # sensitivity. Normal production/runtime path leaves this as None so
        # placement is derived from the public problem_contract.
        self.shape_prior6_override = normalize_shape_prior6(shape_prior6_override) if shape_prior6_override is not None else None
        self._last_feedback: Dict[str, Any] = {}
        self._last_field_update: Dict[str, Any] = {}
        self._history: List[Dict[str, Any]] = []
        self._trace: List[str] = []
        self._last_obs: Dict[str, Any] = {}

    def _problem_contract(self, obs: Mapping[str, Any]) -> Dict[str, Any]:
        mode = str(obs.get("observe_health_mode", "partial"))
        state_obs = "direct" if mode == "direct" else ("partial" if mode == "partial" else "indirect")
        degradation = _clip01(obs.get("degradation_prob_public", 0.2), 0.2)
        recovery = _clip01(obs.get("wait_recovery_prob_public", 0.0), 0.0)
        drift = "fixed" if degradation <= 0.05 and recovery <= 0.02 else ("slow" if degradation <= 0.18 else "active")
        commitment_cost = "low" if float(obs.get("failure_penalty_public", 5.0) or 5.0) <= 3.0 else ("medium" if float(obs.get("failure_penalty_public", 5.0) or 5.0) <= 8.0 else "high")
        return {
            "actions": {"count": len(ACTIONS), "native_type": "discrete_control", "labels": list(ACTIONS)},
            "decision_scope": "anchor",
            "observation_channels": ["observed_health", "public_costs", "action_feedback", "history"],
            "task_anchor": {"kind": "reward_maximization", "provided_externally": True, "notes": "maximize uptime/reward net of maintenance and failure costs"},
            "hard_constraints": ["finite_health_state", "legal_action_set"],
            "soft_costs": ["repair_cost", "replace_cost", "inspect_cost", "failure_penalty"],
            "regime_anchors": ["machine_identity", "health_state", "maintenance_action_identities"],
            "mutable_factors": ["health_degradation", "repair_or_replacement_resets_state", "inspection_changes_information"] if degradation > 0.05 else ["low_rate_health_degradation"],
            "timescale_profile": {"horizon_fixity": "fixed", "drift": drift, "notes": "health evolves under public degradation/repair dynamics"},
            "observability_profile": {"state": state_obs, "outcome": "direct", "constraints": "direct"},
            "reversibility_profile": {"action_reversibility": "partly_reversible", "commitment_cost": commitment_cost, "notes": "running can create deferred repair/failure burden; repair/replacement can partially reset"},
            "notes": "maintenance/replacement MDP public contract; no true hidden health or optimal policy exposed",
            "source": "maintenance_replacement_adapter",
            "status": "declared",
        }

    def _derive(self, obs: Mapping[str, Any]) -> Dict[str, Any]:
        obs_h = obs.get("observed_health")
        max_h = max(1, int(obs.get("max_health", 4) or 4))
        health_known = bool(obs.get("health_observed", obs_h is not None))
        health_norm = _clip01((float(obs_h) / float(max_h)) if obs_h is not None else obs.get("observed_health_norm", 0.5), 0.5)
        degradation = _clip01(obs.get("degradation_prob_public", 0.2), 0.2)
        recovery = _clip01(obs.get("wait_recovery_prob_public", 0.0), 0.0)
        repair_cost = max(0.0, float(obs.get("repair_cost_public", 0.8) or 0.8))
        replace_cost = max(0.0, float(obs.get("replace_cost_public", 2.0) or 2.0))
        failure_penalty = max(0.0, float(obs.get("failure_penalty_public", 8.0) or 8.0))
        mode = str(obs.get("observe_health_mode", "partial"))
        obs_age_raw = obs.get("observed_health_age", 0 if health_known else None)
        try:
            obs_age = 0 if obs_age_raw is None else max(0, int(obs_age_raw))
        except Exception:
            obs_age = 0
        noise = _clip01(obs.get("observation_noise_public", 0.20), 0.20)
        if not health_known:
            uncertainty = 0.85 if mode == "hidden" else 0.75
        elif mode == "direct":
            uncertainty = 0.05
        elif mode == "hidden":
            # Hidden-mode health observations are public but can be stale after an
            # inspection.  Treat inspected health as decaying evidence, not as a
            # persistent oracle read of the true state.
            low_health_pressure = max(0.0, 1.0 - health_norm)
            uncertainty = min(0.95, 0.10 + 0.08 * float(obs_age > 0) + 0.32 * degradation * float(obs_age) + 0.12 * low_health_pressure)
        else:
            # Partial observations are current public cues but noisy, not direct
            # state knowledge.  The adapter may expose the cue, but must mark its
            # uncertainty so generic readout does not over-collapse on it.
            uncertainty = min(0.80, max(0.20, noise + 0.10 * degradation))
        recent = list(self._trace[-8:])

        # Public, non-solver local cues. These are not optimal-policy values.
        run_local = health_norm * (1.0 - 0.55 * degradation)
        maintenance_need = max(0.0, 1.0 - health_norm)
        if mode == "direct":
            inspect_need = 0.02 * degradation
        elif mode == "hidden":
            inspect_need = max(0.20 * degradation, uncertainty * (0.70 + 0.20 * degradation))
        else:
            inspect_need = max(0.05, 0.45 * uncertainty + 0.25 * degradation)
        repair_support = max(0.0, maintenance_need - min(0.5, repair_cost / 4.0))
        replace_support = max(0.0, maintenance_need * 0.85 + 0.25 * degradation - min(0.7, replace_cost / 5.0))
        wait_support = max(0.0, recovery * maintenance_need - 0.05)

        raw_scores = {
            "RUN": run_local,
            "INSPECT": inspect_need,
            "REPAIR": repair_support,
            "REPLACE": replace_support,
            "WAIT": wait_support,
        }
        candidates: List[Dict[str, Any]] = []
        for a in ACTIONS:
            recent_freq = float(sum(1 for x in recent if x == a) / float(len(recent) or 1)) if recent else 0.0
            ever_tested = any(x == a for x in self._trace)
            local = _clip01(raw_scores.get(a, 0.0), 0.0)
            if a == "RUN":
                reversibility = max(0.0, 1.0 - degradation - 0.2 * maintenance_need)
                failure_burden = min(1.0, failure_penalty / 12.0)
                # Public one-step burden cue: running when health is degraded has
                # future consequence that is not captured by immediate visible
                # reward alone.  This is not an optimal threshold or value score;
                # it is bounded evidence from public degradation/penalty/observed
                # health used by the generic candidate surface.
                contradiction = max(0.0, degradation * (0.20 + 1.70 * (maintenance_need ** 1.2) + failure_burden * maintenance_need) + (0.25 if not health_known else 0.0))
                support_depth = 0.45 + 0.40 * (1.0 - uncertainty)
            elif a == "INSPECT":
                reversibility = 1.0
                contradiction = 0.15 if health_known else 0.55
                support_depth = 0.30 + 0.50 * uncertainty
            elif a in {"REPAIR", "REPLACE"}:
                reversibility = 0.55 if a == "REPAIR" else 0.35
                contradiction = max(0.0, health_norm - 0.65)
                support_depth = 0.35 + 0.45 * maintenance_need
            else:  # WAIT
                reversibility = 0.85
                contradiction = max(0.0, degradation - recovery)
                support_depth = 0.25 + 0.40 * recovery
            candidates.append({
                "candidate_id": a,
                "legal": True,
                "visible_delta": float(local),
                "goal_relation": float(local),
                "support_depth": float(_clip01(support_depth)),
                "paired_depth": float(_clip01(support_depth)),
                "line_support": float(_clip01(0.25 + 0.50 * local)),
                "continuity_support": float(_clip01((1.0 - contradiction) * (0.30 + 0.50 * local))),
                "obstruction_hint": 0.0,
                "novelty_hint": float(max(0.0, 1.0 - recent_freq)),
                "uncertainty_hint": float(uncertainty),
                "reversibility_hint": float(_clip01(reversibility)),
                "trace_relation": float(recent_freq),
                "coverage_adequacy": float(1.0 - uncertainty),
                "contradiction_hint": float(_clip01(contradiction)),
                "revisit_hint": float(recent_freq),
                "tested_hint": float(max(0.25, min(0.75, 0.25 + 0.50 * recent_freq))) if ever_tested else 0.25,
                "public_effects": _maintenance_public_effects(
                    a,
                    degradation=degradation,
                    recovery=recovery,
                    maintenance_need=maintenance_need,
                    uncertainty=uncertainty,
                    health_known=health_known,
                    failure_penalty=failure_penalty,
                ),
            })
        ordered = sorted([float(c["goal_relation"]) for c in candidates], reverse=True)
        best_margin = max(0.0, ordered[0] - ordered[1]) if len(ordered) > 1 else (ordered[0] if ordered else 0.0)
        goal_field = {
            "goal_mode": "graded",
            "goal_sharpness": float(best_margin),
            "goal_stability": float(max(0.1, 1.0 - degradation)),
            "goal_certainty": float(max(0.0, min(1.0, 0.55 * best_margin + 0.45 * (1.0 - uncertainty)))),
            "goal_observability": float(1.0 - 0.65 * uncertainty),
        }
        signals = {
            "z_health_visible": float(health_norm if health_known else 0.5),
            "z_degradation": float(degradation),
            "z_recovery": float(recovery),
            "z_failure_burden": float(min(1.0, failure_penalty / 12.0) * maintenance_need),
        }
        memory_view = {
            "recent_actions": list(recent),
            "last_feedback": dict(self._last_feedback or {}),
            "health_known": bool(health_known),
            "observed_health_norm": float(health_norm),
            "observed_health_age": int(obs_age),
            "observation_uncertainty": float(uncertainty),
        }
        support_evidence = float(max(0.10, min(1.0, 0.55 * (1.0 - uncertainty) + 0.25 * max(ordered or [0.0]) + 0.20 * len(self._history) / max(1, len(self._history) + 8))))
        dyn_hint = float(max(degradation, 0.5 * uncertainty, recovery))
        return {
            "residuals": {"maintenance_need": float(maintenance_need), "uncertainty": float(uncertainty)},
            "probes": {"inspect_pressure": float(inspect_need), "repair_pressure": float(repair_support), "replace_pressure": float(replace_support)},
            "signals": signals,
            "memory_view": memory_view,
            "measurement_evidence": {"health_known": float(1.0 - uncertainty), "health_observation_age": float(obs_age), "public_degradation": float(degradation), "history_coverage": float(min(1.0, len(self._history) / 8.0))},
            "candidates": candidates,
            "goal_field": goal_field,
            "dyn_hint": dyn_hint,
            "co_conf_hint": support_evidence,
            "support_evidence": support_evidence,
        }

    def select(self, obs: Dict[str, Any]) -> Dict[str, Any]:
        obs = dict(obs or {})
        self._last_obs = obs
        derived = self._derive(obs)
        packet = make_problem_packet(
            family="maintenance_replacement",
            step_idx=int(obs.get("t", 0) or 0),
            action_space=list(ACTIONS),
            current_observation=obs,
            history=list(self._history[-128:]),
            trace=list(self._trace[-128:]),
            feedback=dict(self._last_feedback or {}),
            residuals=derived["residuals"],
            probes=derived["probes"],
            signals=derived["signals"],
            constraints={"legal_actions": list(ACTIONS)},
            family_payload={"max_health": obs.get("max_health"), "observe_health_mode": obs.get("observe_health_mode")},
            memory_view=derived["memory_view"],
            measurement_evidence=derived.get("measurement_evidence"),
            candidates=derived["candidates"],
            goal_field=derived["goal_field"],
            problem_contract=self._problem_contract(obs),
            field_update=dict(self._last_field_update or {}),
            dyn_hint=derived["dyn_hint"],
            co_conf_hint=derived["co_conf_hint"],
            support_evidence=derived["support_evidence"],
        )
        if self.shape_prior6_override is not None:
            packet["shape_prior6"] = dict(self.shape_prior6_override)
        warnings = validate_problem_packet(packet)
        ensure_signal_bus(self.core.primitives)
        try:
            out = dict(self.core.step(packet, None) or {})
        except Exception:
            import os
            if os.environ.get("CO_STRICT_ERRORS", "") == "1":
                raise
            out = {}
        self._last_obs = dict(packet)
        out = require_kernel_action(out, legal_actions=list(ACTIONS), family="maintenance")
        attach_contract_debug(out, packet, warnings)
        return out

    def update(self, feedback: Dict[str, Any]) -> None:
        fb = dict(feedback or {})
        self._last_feedback = fb
        self._history.append(fb)
        if fb.get("action") is not None:
            self._trace.append(str(fb.get("action")))

        # ``select`` stores the public packet. Rebuild an update packet from its
        # public current_observation, not from the packet wrapper itself; otherwise
        # the adapter silently loses observation-mode/cost fields and emits a
        # default partial contract during learning.
        last_packet = dict(self._last_obs or {})
        cur_obs = dict(last_packet.get("current_observation", {}) or {})
        try:
            visible = self._derive(cur_obs)
            sig_src = {}
            bus = self.core.primitives.get("signal_bus")
            if hasattr(bus, "signals"):
                sig_src = dict(bus.signals())
            elif isinstance(bus, dict):
                sig_src = dict(bus)
            packet = make_problem_packet(
                family="maintenance_replacement",
                step_idx=int(last_packet.get("step_idx", cur_obs.get("t", 0)) or 0) + 1,
                action_space=list(ACTIONS),
                current_observation=cur_obs,
                history=list(self._history[-128:]),
                trace=list(self._trace[-128:]),
                feedback=fb,
                residuals=visible["residuals"],
                probes=visible["probes"],
                signals=visible["signals"],
                constraints={"legal_actions": list(ACTIONS)},
                family_payload={"max_health": cur_obs.get("max_health"), "observe_health_mode": cur_obs.get("observe_health_mode")},
                memory_view=visible["memory_view"],
                measurement_evidence=visible.get("measurement_evidence"),
                candidates=visible["candidates"],
                goal_field=visible["goal_field"],
                problem_contract=self._problem_contract(cur_obs),
                field_update=dict(self._last_field_update or {}),
                dyn_hint=visible["dyn_hint"],
                co_conf_hint=visible["co_conf_hint"],
                support_evidence=visible["support_evidence"],
            )
            if self.shape_prior6_override is not None:
                packet["shape_prior6"] = dict(self.shape_prior6_override)
            update = map_feedback_update(packet, fb, self.core.primitives, sig_src, {})
            if isinstance(update, dict):
                warnings = validate_problem_update(update)
                if not warnings:
                    self._last_field_update = dict(update)
                    packet["field_update"] = dict(update)
            # Drive the core update/learning pass so header placement, substrate,
            # and learning elements see feedback. This mirrors the mature bandit
            # and maze adapters and is required for shape_prior6 to affect runtime.
            self.core.step(packet, fb)
        except Exception:
            import os
            if os.environ.get("CO_STRICT_ERRORS", "") == "1":
                raise
            pass
