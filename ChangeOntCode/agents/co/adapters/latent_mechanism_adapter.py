"""Latent-mechanism boundary adapter.

Publishes visible/legal action facts and public hiddenness/deceptiveness effects
for structural diagnostics without giving the kernel hidden mechanism answers.
"""

from __future__ import annotations
from typing import Any, Dict, Optional, List, Tuple

from agents.co.boundary.problem_packet import (
    make_problem_packet,
    validate_problem_packet,
    validate_problem_update,
    attach_contract_debug,
    require_kernel_action,
)
from agents.co.adapters.common import ensure_signal_bus, public_effect, single_decision_slot_effect
from agents.co.boundary.update_mapper import map_feedback_update

ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT", "INTERACT"]
DELTAS = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}


def _mdist(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    return abs(int(a[0]) - int(b[0])) + abs(int(a[1]) - int(b[1]))


def _latent_measurement_evidence(obs: Dict[str, Any], candidates: List[Dict[str, Any]], goal_field: Dict[str, Any]) -> Dict[str, Any]:
    legal_count = float(sum(1 for c in candidates if bool(c.get("legal", True))))
    exposed = float(max(1, len(ACTIONS)))
    blocked_count = max(0.0, exposed - legal_count)
    hiddenness = float(max(0.0, min(1.0, obs.get("hiddenness", 0.0) or 0.0)))
    rewrite_harshness = float(max(0.0, min(1.0, obs.get("rewrite_harshness", 0.0) or 0.0)))
    local_deceptiveness = float(max(0.0, min(1.0, obs.get("local_deceptiveness", 0.0) or 0.0)))
    progress_known = 0.0 if obs.get("progress_obs", None) is None else 1.0
    recent = [float(max(0.0, min(1.0, c.get("revisit_hint", 0.0) or 0.0))) for c in candidates if isinstance(c, dict)]
    revisit_rate = sum(recent) / float(len(recent) or 1)
    return {
        "legal_count": legal_count,
        "blocked_count": blocked_count,
        "exposed_action_count": exposed,
        "legal_ratio": legal_count / exposed,
        "blocked_ratio": blocked_count / exposed,
        "branching_fraction": legal_count / exposed,
        "goal_observability": float(goal_field.get("goal_observability", 1.0) or 1.0),
        "goal_certainty": float(goal_field.get("goal_certainty", 0.5) or 0.5),
        "goal_stability": float(goal_field.get("goal_stability", 0.5) or 0.5),
        "goal_sharpness": float(goal_field.get("goal_sharpness", 0.5) or 0.5),
        "global_coverage": max(0.05, 1.0 - hiddenness),
        "hidden_decisiveness": max(hiddenness, rewrite_harshness),
        "cue_fidelity": max(0.0, min(1.0, progress_known * (1.0 - local_deceptiveness))),
        "correction_loss": max(rewrite_harshness, local_deceptiveness * 0.7),
        "carrier_break_rate": max(0.0, min(1.0, 0.5 * hiddenness + 0.5 * rewrite_harshness)),
        "payload_drift_rate": max(rewrite_harshness, local_deceptiveness),
        "reactive_divergence": max(0.0, min(1.0, 0.55 * hiddenness + 0.45 * local_deceptiveness)),
        "delayed_consequence_revelation": max(hiddenness, 1.0 - progress_known),
        "anchor_shift_rate": rewrite_harshness,
        "recent_revisit_rate": revisit_rate,
    }


def _latent_public_effects(
    action: str,
    *,
    movement_gain: float = 0.0,
    reverse_risk: float = 0.0,
    hiddenness: float = 0.0,
    rewrite_harshness: float = 0.0,
    on_surface: bool = False,
    door_open: bool = False,
    attempts: int = 0,
) -> List[Dict[str, Any]]:
    """Public burden/effect facts for latent-mechanism candidates.

    Facts express visible geometry and mechanism observability only.  They do
    not expose the true active switch or rank candidate interactions by hidden
    success.
    """
    effects: List[Dict[str, Any]] = [single_decision_slot_effect("latent_mechanism_action_slot")]
    hidden_mag = max(0.0, min(1.0, float(hiddenness)))
    rewrite_mag = max(0.0, min(1.0, float(rewrite_harshness)))
    if action == "INTERACT":
        if on_surface and not door_open:
            effects.append(public_effect("reveal", "mechanism_hiddenness", magnitude=max(0.05, hidden_mag), scope="visible_interactive", kind="evidence", public_basis="visible_observation", direction="expose", coupling="door_mechanism"))
            effects.append(public_effect("transform", "door_mechanism", magnitude=max(0.05, 1.0 - min(1.0, attempts / 3.0)), scope="visible_interactive", public_basis="declared_transition_rule", direction="mechanism_rewrite", coupling="door_mechanism"))
        else:
            effects.append(public_effect("carry", "mechanism_hiddenness", magnitude=max(0.05, hidden_mag), scope="visible_interactive", kind="uncertainty", public_basis="visible_observation", direction="unresolved", coupling="door_mechanism"))
    else:
        if movement_gain > 0.0:
            effects.append(public_effect("reduce", "visible_route_distance", magnitude=min(1.0, abs(float(movement_gain))), scope="local_geometry", public_basis="visible_observation", direction="toward_visible_anchor", coupling="goal_or_mechanism_anchor"))
        elif movement_gain < 0.0:
            effects.append(public_effect("carry", "visible_route_distance", magnitude=min(1.0, abs(float(movement_gain))), scope="local_geometry", public_basis="visible_observation", direction="away_from_visible_anchor", coupling="goal_or_mechanism_anchor"))
        else:
            effects.append(public_effect("carry", "path_commitment", magnitude=0.25, scope="local_geometry", public_basis="visible_observation", direction="lateral", coupling="goal_or_mechanism_anchor"))
        if hidden_mag > 0.0 or rewrite_mag > 0.0:
            effects.append(public_effect("carry", "mechanism_hiddenness", magnitude=max(hidden_mag, rewrite_mag), scope="mechanism_observability", kind="uncertainty", public_basis="visible_observation", direction="unresolved", coupling="door_mechanism"))
    if reverse_risk > 0.0:
        effects.append(public_effect("carry", "path_revisit", magnitude=min(1.0, float(reverse_risk)), scope="trace_history", public_basis="public_history", direction="backtrack", coupling="path_continuation"))
    return effects


class COAdapterLatentMechanism:
    def __init__(self, core, name: str = "CO_latent_mechanism") -> None:
        self.core = core
        self.name = name
        self._pipe = core.combinators.get("pipeline")
        self._last_obs: Optional[Dict[str, Any]] = None
        self._path: List[Tuple[int, int]] = []
        self._last_feedback: Optional[Dict[str, Any]] = None
        self._last_field_update: Dict[str, Any] = {}
        self._attempted: Dict[Tuple[int, int], int] = {}

    def _problem_contract(self, obs: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "actions": {"count": 5, "native_type": "discrete", "labels": ACTIONS},
            "observation_channels": ["visible_geometry", "door_state", "switch_locations", "recent_path", "mechanism_observables"],
            "task_anchor": {"kind": "goal_reach_under_latent_mechanism", "provided_externally": True, "notes": "reach the visible goal while latent mechanism state changes object meaning"},
            "hard_constraints": ["wall_blocked", "door_blocked_when_closed"],
            "soft_costs": ["step_cost", "wrong_interaction_cost"],
            "regime_anchors": ["door_mechanism", "interaction_history"],
            "mutable_factors": ["door_passability", "switch_relevance"],
            "timescale_profile": {"horizon_fixity": "fixed", "drift": "none", "notes": "semantic rewrite is endogenous, induced by interaction history"},
            "observability_profile": {"state": "partial", "outcome": "direct", "constraints": "direct"},
            "reversibility_profile": {"action_reversibility": "partly_reversible", "commitment_cost": "medium_to_high", "notes": "wrong interaction can reset or delay mechanism progress"},
            "notes": "Latent mechanism family: same visible object may lawfully change meaning after interaction history.",
            "source": "adapter_visible_family_facts",
            "status": "adapter_emitted",
        }


    def _derive(self, obs: Dict[str, Any]) -> Dict[str, Any]:
        pos = tuple(obs.get("pos") or (0, 0))
        goal = tuple(obs.get("goal") or (0, 0))
        door = tuple(obs.get("door") or (0, 0))
        switches = [tuple(s) for s in list(obs.get("switches") or [])]
        decoys = [tuple(s) for s in list(obs.get("decoys") or [])]
        legal = set(list(obs.get("legal_actions") or []))
        door_open = bool(obs.get("door_open", False))
        hiddenness = float(obs.get("hiddenness", 0.0) or 0.0)
        rewrite_harshness = float(obs.get("rewrite_harshness", 0.0) or 0.0)
        local_deceptiveness = float(obs.get("local_deceptiveness", 0.0) or 0.0)
        progress_obs = obs.get("progress_obs", None)
        residuals: Dict[str, float] = {"goal_distance": float(_mdist(pos, goal)), "door_distance": float(_mdist(pos, door))}
        probes: Dict[str, float] = {
            "door_open": 1.0 if door_open else 0.0,
            "hiddenness": hiddenness,
            "rewrite_harshness": rewrite_harshness,
            "progress_known": 0.0 if progress_obs is None else 1.0,
        }
        signals: Dict[str, float] = {
            "z_goal": float(1.0 / (1.0 + _mdist(pos, goal))),
            "z_door": float(1.0 / (1.0 + _mdist(pos, door))),
            "z_reframe_pressure": float(max(hiddenness, rewrite_harshness)),
            "z_deceptiveness": local_deceptiveness,
        }
        candidates: List[Dict[str, Any]] = []
        recent = list(self._path[-8:])
        prev = recent[-1] if recent else None
        visible_interactives = [tuple(s) for s in (switches + decoys)]
        guide_target = goal if door_open else (min(visible_interactives, key=lambda s: _mdist(pos, s)) if visible_interactives else door)
        for a in ACTIONS:
            if a == "INTERACT":
                if a not in legal:
                    continue
                tile = pos
                attempts = int(self._attempted.get(tile, 0) or 0)
                on_surface = tile in switches or tile in decoys
                novelty = float(max(0.0, 1.0 - min(1.0, attempts / 3.0)))
                goal_relation = float(0.45 * novelty if (on_surface and not door_open) else (0.10 * novelty if on_surface else 0.0))
                contradiction_hint = float(min(1.0, attempts / 3.0)) if on_surface else 0.25
                continuity_support = float(0.25 + 0.35 * novelty if on_surface else 0.05)
                candidates.append({
                    "candidate_id": a,
                    "legal": True,
                    "goal_relation": goal_relation,
                    "visible_delta": goal_relation,
                    "continuity_support": continuity_support,
                    "obstruction_hint": 0.0,
                    "novelty_hint": novelty,
                    "uncertainty_hint": hiddenness,
                    "reversibility_hint": 0.7,
                    "trace_relation": float(attempts / 3.0),
                    "support_depth": 1.0,
                    "paired_depth": 1.0,
                    "line_support": float(0.20 + 0.30 * novelty),
                    "coverage_adequacy": float(max(0.10, 1.0 - hiddenness)),
                    "tested_hint": float(max(0.10, 1.0 - hiddenness)),
                    "contradiction_hint": contradiction_hint,
                    "revisit_hint": float(attempts / 3.0),
                    "public_effects": _latent_public_effects(
                        a,
                        hiddenness=hiddenness,
                        rewrite_harshness=rewrite_harshness,
                        on_surface=on_surface,
                        door_open=door_open,
                        attempts=attempts,
                    ),
                })
                continue
            if a not in legal:
                continue
            dr, dc = DELTAS[a]
            nxt = (pos[0] + dr, pos[1] + dc)
            guide_gain = float(_mdist(pos, guide_target) - _mdist(nxt, guide_target))
            goal_gain = float(_mdist(pos, goal) - _mdist(nxt, goal))
            recent_freq = float(sum(1 for p in recent if tuple(p) == nxt) / float(len(recent) or 1)) if recent else 0.0
            reverse_risk = 1.0 if prev is not None and tuple(prev) == nxt else 0.0
            goal_relation = float(max(-1.0, min(1.0, (0.85 * guide_gain + 0.15 * goal_gain) if not door_open else goal_gain)))
            continuity_support = float((1.0 - reverse_risk) * (0.20 + 0.50 * max(0.0, goal_relation) + 0.30 * max(0.0, 1.0 - recent_freq)))
            candidates.append({
                "candidate_id": a,
                "legal": True,
                "goal_relation": goal_relation,
                "visible_delta": float(goal_relation),
                "continuity_support": continuity_support,
                "obstruction_hint": float(reverse_risk),
                "novelty_hint": float(max(0.0, 1.0 - recent_freq)),
                "uncertainty_hint": hiddenness,
                "reversibility_hint": float(1.0 - reverse_risk),
                "trace_relation": recent_freq,
                "support_depth": 1.0,
                "paired_depth": 1.0,
                "line_support": float(max(0.0, 0.25 + 0.5 * max(0.0, goal_relation))),
                "coverage_adequacy": float(max(0.10, 1.0 - hiddenness)),
                "tested_hint": float(max(0.10, 1.0 - 0.6 * hiddenness)),
                "contradiction_hint": float(max(reverse_risk, rewrite_harshness * recent_freq)),
                "revisit_hint": recent_freq,
                "public_effects": _latent_public_effects(
                    a,
                    movement_gain=goal_relation,
                    reverse_risk=reverse_risk,
                    hiddenness=hiddenness,
                    rewrite_harshness=rewrite_harshness,
                    door_open=door_open,
                ),
            })
        goal_field = {
            "goal_mode": "fixed",
            "goal_sharpness": 1.0,
            "goal_stability": 1.0,
            "goal_certainty": 1.0,
            "goal_observability": 1.0,
        }
        dyn_hint = 0.0
        co_conf_hint = max(0.10, 1.0 - hiddenness)
        memory_view = {
            "interaction_attempts": {f"{k[0]}_{k[1]}": int(v) for k, v in self._attempted.items()},
            "door_open": bool(door_open),
        }
        measurement_evidence = _latent_measurement_evidence(obs, candidates, goal_field)
        return {
            "residuals": residuals,
            "probes": probes,
            "signals": signals,
            "candidates": candidates,
            "goal_field": goal_field,
            "measurement_evidence": measurement_evidence,
            "dyn_hint": dyn_hint,
            "co_conf_hint": co_conf_hint,
            "memory_view": memory_view,
            "support_evidence": max(0.10, 1.0 - hiddenness),
        }
    def select(self, obs: Dict[str, Any]) -> Dict[str, Any]:
        obs = dict(obs or {})
        self._last_obs = obs
        if "pos" in obs:
            try:
                self._path.append(tuple(obs.get("pos")))
            except Exception:
                pass
        derived = self._derive(obs)
        payload = {
            "door": obs.get("door"),
            "mechanism_depth": obs.get("mechanism_depth"),
            "hiddenness": obs.get("hiddenness"),
            "rewrite_harshness": obs.get("rewrite_harshness"),
            "local_deceptiveness": obs.get("local_deceptiveness"),
        }
        packet = make_problem_packet(
            family="latent_mechanism",
            step_idx=int(obs.get("t", 0) or 0),
            action_space=list(ACTIONS),
            current_observation=obs,
            history=list(self._path[-128:]),
            trace=list(self._path[-128:]),
            feedback=dict(self._last_feedback or {}),
            residuals=derived["residuals"],
            probes=derived["probes"],
            signals=derived["signals"],
            constraints={},
            family_payload=payload,
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
        warnings = validate_problem_packet(packet)
        try:
            out = dict(self.core.step(packet, None) or {})
        except Exception:
            import os
            if os.environ.get("CO_STRICT_ERRORS", "") == "1":
                raise
            out = {}
        self._last_obs = dict(packet)
        out = require_kernel_action(out, legal_actions=list(ACTIONS), family="latent_mechanism")
        attach_contract_debug(out, packet, warnings)
        return out

    def update(self, feedback: Dict[str, Any]) -> None:
        self._last_feedback = dict(feedback or {})
        try:
            obs = dict(self._last_obs or {})
            if feedback.get("action") == "INTERACT" and "pos" in obs:
                tile = tuple(obs.get("pos"))
                self._attempted[tile] = self._attempted.get(tile, 0) + 1
            packet = make_problem_packet(
                family="latent_mechanism",
                step_idx=int(obs.get("t", 0) or 0),
                action_space=list(ACTIONS),
                current_observation=obs,
                history=list(self._path[-128:]),
                trace=list(self._path[-128:]),
                feedback=dict(feedback or {}),
                residuals={}, probes={}, signals={}, constraints={}, family_payload={}, measurement_evidence=obs.get("measurement_evidence"), candidates=[], goal_field=obs.get("goal_field"),
                problem_contract=self._problem_contract(obs), field_update=dict(self._last_field_update or {}),
            )
            update = map_feedback_update(packet, dict(feedback or {}), self.core.primitives, {}, {})
            if isinstance(update, dict):
                warnings = validate_problem_update(update)
                if not warnings:
                    self._last_field_update = dict(update)
        except Exception:
            pass
