"""Maze boundary adapter.

Publishes public movement legality, obstacle/transition facts, and candidate
action expressions for the CO kernel without route-planning or shortest-path
policy leakage.
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




def _maze_cell_kind(grid: Any, r: int, c: int) -> int:
    """Return 0=known-free, 1=known-wall, -1=unknown/other."""
    try:
        v = int(grid[r][c])
    except Exception:
        return -1
    if v == 0:
        return 0
    if v == 1:
        return 1
    return -1


def _maze_measurement_evidence(pos: Any, goal: Any, H: Any, W: Any, grid: Any, goal_field: Dict[str, Any]) -> Dict[str, Any]:
    legal_count = 0
    blocked_count = 0
    if isinstance(pos, (list, tuple)) and len(pos) == 2:
        try:
            pr, pc = int(pos[0]), int(pos[1])
            for dr, dc in ((-1,0),(1,0),(0,-1),(0,1)):
                nr, nc = pr + dr, pc + dc
                try:
                    in_bounds = H is None or W is None or (0 <= nr < int(H) and 0 <= nc < int(W))
                except Exception:
                    in_bounds = True
                if not in_bounds:
                    blocked_count += 1
                    continue
                if grid is None:
                    legal_count += 1
                    continue
                kind = _maze_cell_kind(grid, nr, nc)
                if kind == 0:
                    legal_count += 1
                elif kind == 1:
                    blocked_count += 1
        except Exception:
            pass
    exposed = max(1, legal_count + blocked_count)
    unknown_frac = 0.0
    try:
        if grid is not None:
            total = sum(len(row) for row in grid)
            unknown = sum(1 for row in grid for cell in row if int(cell) < 0)
            unknown_frac = float(unknown) / float(total or 1)
    except Exception:
        unknown_frac = 0.0
    return {
        "legal_count": float(legal_count),
        "blocked_count": float(blocked_count),
        "exposed_action_count": float(exposed),
        "legal_ratio": float(legal_count) / float(exposed),
        "blocked_ratio": float(blocked_count) / float(exposed),
        "branching_fraction": float(legal_count) / 4.0,
        "coverage_adequacy": float(max(0.0, min(1.0, 1.0 - unknown_frac))),
        "seen_ratio": float(max(0.0, min(1.0, 1.0 - unknown_frac))),
        "goal_observability": float(goal_field.get("goal_observability", 1.0) or 1.0),
        "goal_certainty": float(goal_field.get("goal_certainty", 0.5) or 0.5),
        "goal_stability": float(goal_field.get("goal_stability", 0.5) or 0.5),
        "constraint_exposure": float(blocked_count) / float(exposed),
    }


def _maze_public_effects(action: str, *, improve: float, reverse_risk: float, unknown_frac: float) -> List[Dict[str, Any]]:
    """Public burden/effect facts for maze candidates.

    These facts use visible local geometry only: a move may reduce or carry
    visible goal-distance burden, revisiting may carry path-commitment burden,
    and partial observability may expose topology hiddenness. No shortest-path
    route or hidden map fact is published.
    """
    effects: List[Dict[str, Any]] = [single_decision_slot_effect("maze_action_slot")]
    if improve > 0.0:
        effects.append(public_effect("reduce", "visible_goal_distance", magnitude=min(1.0, abs(float(improve))), scope="local_geometry", public_basis="visible_observation", direction="toward_visible_goal", coupling="goal_anchor"))
    elif improve < 0.0:
        effects.append(public_effect("carry", "visible_goal_distance", magnitude=min(1.0, abs(float(improve))), scope="local_geometry", public_basis="visible_observation", direction="away_from_visible_goal", coupling="goal_anchor"))
    else:
        effects.append(public_effect("carry", "path_commitment", magnitude=0.25, scope="local_geometry", public_basis="visible_observation", direction="lateral", coupling="goal_anchor"))
    if reverse_risk > 0.0:
        effects.append(public_effect("carry", "path_revisit", magnitude=min(1.0, float(reverse_risk)), scope="trace_history", public_basis="public_history", direction="backtrack", coupling="path_continuation"))
    if unknown_frac > 0.0:
        effects.append(public_effect("reveal", "topology_hiddenness", magnitude=min(1.0, float(unknown_frac)), scope="local_geometry", kind="evidence", public_basis="visible_observation", direction="expose", coupling="path_continuation"))
    return effects


class COAdapterMaze:
    def __init__(self, core, name: str = "CO") -> None:
        self.core = core
        self.name = name
        self._pipe = core.combinators.get("pipeline")
        self._last_obs: Optional[Dict[str, Any]] = None
        self._path: List[Tuple[int, int]] = []
        self._last_feedback: Optional[Dict[str, Any]] = None
        self._last_field_update: Dict[str, Any] = {}

    def _problem_contract(self, obs: Dict[str, Any]) -> Dict[str, Any]:
        labels = ["UP", "DOWN", "LEFT", "RIGHT"]
        return {
            "actions": {"count": 4, "native_type": "discrete", "labels": labels},
            "observation_channels": ["visible_position", "visible_goal", "legality_geometry", "trace_history"],
            "task_anchor": {"kind": "goal_reach", "provided_externally": True, "notes": "reach the externally supplied goal under visible legality constraints"},
            "hard_constraints": ["illegal_move_blocked"],
            "soft_costs": [],
            "regime_anchors": ["legal_move_system"],
            "mutable_factors": ["local_path_progress_relation"],
            "timescale_profile": {"horizon_fixity": "fixed", "drift": "slow", "notes": "geometry treated as fixed on the local decision horizon"},
            "observability_profile": {"state": "direct", "outcome": "direct", "constraints": "direct"},
            "reversibility_profile": {"action_reversibility": "partly_reversible", "commitment_cost": "medium", "notes": "wrong turns can often be undone but with path cost"},
            "notes": "Maze family emits visible legality and goal geometry, not search strategy.",
            "source": "adapter_visible_family_facts",
            "status": "adapter_emitted",
        }

    def _derive(self, obs: Dict[str, Any]) -> Dict[str, Any]:
        pos = obs.get("pos")
        goal = obs.get("goal")
        grid = obs.get("grid")
        H = obs.get("height")
        W = obs.get("width")
        residuals: Dict[str, float] = {}
        probes: Dict[str, float] = {}
        signals: Dict[str, float] = {}
        candidates: List[Dict[str, Any]] = []
        partial_obs = bool(obs.get("partial_observability", False))
        dynamic_walls = bool(obs.get("dynamic_walls", False))
        wall_flip_prob = float(obs.get("wall_flip_prob", 0.0) or 0.0)
        unknown_frac = 0.0
        try:
            if grid is not None:
                total = sum(len(row) for row in grid)
                unknown = sum(1 for row in grid for cell in row if int(cell) < 0)
                unknown_frac = float(unknown) / float(total or 1)
        except Exception:
            unknown_frac = 0.0
        goal_observability = max(0.10, min(1.0, 1.0 - 0.85 * unknown_frac)) if partial_obs else 1.0
        goal_certainty = max(0.20, min(1.0, goal_observability * (1.0 - 0.45 * (wall_flip_prob if dynamic_walls else 0.0))))
        goal_field = {
            "goal_mode": "fixed",
            "goal_sharpness": 1.0,
            "goal_stability": float(max(0.20, min(1.0, 1.0 - 0.60 * (wall_flip_prob if dynamic_walls else 0.0)))),
            "goal_certainty": float(goal_certainty),
            "goal_observability": float(goal_observability),
        }
        dyn_hint = 0.0
        co_conf_hint = 0.25
        if isinstance(pos, (list, tuple)) and isinstance(goal, (list, tuple)) and len(pos) == 2 and len(goal) == 2:
            pr, pc = int(pos[0]), int(pos[1])
            gr, gc = int(goal[0]), int(goal[1])
            d = abs(pr - gr) + abs(pc - gc)
            residuals["goal_distance"] = float(d)
            signals["z_PE"] = float(d)
            signals["z_gain"] = float(1.0 / (1.0 + d))
            signals["var_resid"] = float(d)
            deltas = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}
            def free(r: int, c: int) -> bool:
                try:
                    if H is not None and W is not None and not (0 <= r < int(H) and 0 <= c < int(W)):
                        return False
                    if grid is None:
                        return True
                    return int(grid[r][c]) == 0
                except Exception:
                    return True
            recent = list(self._path[-8:])
            prev = recent[-1] if recent else None
            visit_rate_here = float(sum(1 for p in recent if tuple(p) == (pr, pc)) / float(len(recent) or 1)) if recent else 0.0
            probes["revisit"] = float(tuple(pos) in self._path)
            for a, (dr, dc) in deltas.items():
                nr, nc = pr + dr, pc + dc
                if not free(nr, nc):
                    continue
                d1 = abs(nr - gr) + abs(nc - gc)
                improve = float(d - d1)
                recent_freq = float(sum(1 for p in recent if tuple(p) == (nr, nc)) / float(len(recent) or 1)) if recent else 0.0
                reverse_risk = 1.0 if prev is not None and tuple(prev) == (nr, nc) else 0.0
                goal_relation = float(max(-1.0, min(1.0, improve)))
                novelty_hint = float(max(0.0, 1.0 - recent_freq))
                continuity_support = float((1.0 - reverse_risk) * (0.20 + 0.50 * max(0.0, goal_relation) + 0.30 * novelty_hint))
                contradiction_hint = float(max(reverse_risk, max(0.0, -goal_relation)))
                coverage_adequacy = float(goal_observability)
                candidates.append({
                    "candidate_id": a,
                    "legal": True,
                    "visible_delta": float(improve),
                    "goal_relation": goal_relation,
                    "continuity_support": continuity_support,
                    "obstruction_hint": float(reverse_risk),
                    "novelty_hint": novelty_hint,
                    "uncertainty_hint": float(max(0.0, min(1.0, unknown_frac))),
                    "reversibility_hint": float(1.0 - reverse_risk),
                    "trace_relation": float(recent_freq),
                    "support_depth": 1.0,
                    "paired_depth": 1.0,
                    "line_support": float(max(0.0, 0.30 + 0.70 * max(0.0, goal_relation))),
                    "coverage_adequacy": coverage_adequacy,
                    "tested_hint": coverage_adequacy,
                    "contradiction_hint": contradiction_hint,
                    "revisit_hint": float(recent_freq),
                    "public_effects": _maze_public_effects(
                        a,
                        improve=improve,
                        reverse_risk=reverse_risk,
                        unknown_frac=unknown_frac,
                    ),
                })
            best_goal = max((float(c.get("goal_relation", 0.0) or 0.0) for c in candidates), default=0.0)
            dyn_hint = float(max(0.0, min(1.0, 0.45 * visit_rate_here + 0.20 * float(probes.get("revisit", 0.0)) + 0.35 * (wall_flip_prob if dynamic_walls else 0.0))))
            co_conf_hint = float(max(0.0, min(1.0, 0.20 + 0.40 * max(0.0, best_goal) + 0.40 * goal_observability)))
            support_evidence = float(max(0.0, min(1.0, 0.45 * goal_field["goal_certainty"] + 0.30 * goal_observability + 0.25 * (1.0 - visit_rate_here))))
        else:
            support_evidence = 0.0
        measurement_evidence = _maze_measurement_evidence(pos, goal, H, W, grid, goal_field)
        return {
            "residuals": residuals,
            "probes": probes,
            "signals": signals,
            "measurement_evidence": measurement_evidence,
            "candidates": candidates,
            "goal_field": goal_field,
            "dyn_hint": dyn_hint,
            "co_conf_hint": co_conf_hint,
            "support_evidence": support_evidence,
        }
    def select(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        obs = dict(observation or {})
        step_idx = int(obs.get("t", obs.get("step_idx", 0) or 0))
        visible = self._derive(obs)
        packet = make_problem_packet(
            family="maze",
            step_idx=step_idx,
            action_space=["UP", "DOWN", "LEFT", "RIGHT"],
            current_observation=obs,
            history=list(self._path[-128:]),
            trace=list(self._path[-128:]),
            feedback=dict(self._last_feedback or {}),
            residuals=visible["residuals"],
            probes=visible["probes"],
            signals=visible["signals"],
            constraints={},
            family_payload={"width": obs.get("width"), "height": obs.get("height")},
            measurement_evidence=visible.get("measurement_evidence"),
            candidates=visible["candidates"],
            goal_field=visible["goal_field"],
            problem_contract=self._problem_contract(obs),
            field_update=dict(self._last_field_update or {}),
            dyn_hint=visible["dyn_hint"],
            co_conf_hint=visible["co_conf_hint"],
            support_evidence=visible.get("support_evidence"),
        )
        warnings = validate_problem_packet(packet)
        ensure_signal_bus(self.core.primitives)
        out: Dict[str, Any] = {}
        try:
            out = self.core.step(packet, None) or {}
        except Exception:
            import os
            if os.environ.get("CO_STRICT_ERRORS", "") == "1":
                raise
            out = {}
        self._last_obs = dict(packet)
        out = require_kernel_action(out, legal_actions=["UP", "DOWN", "LEFT", "RIGHT"], family="maze")
        attach_contract_debug(out, packet, warnings)
        out.setdefault("field_update", dict(self._last_field_update or {}))
        out.setdefault("field_update_warnings", validate_problem_update(self._last_field_update or {}))
        self._last_obs = dict(packet)
        pos = obs.get("pos")
        if isinstance(pos, (list, tuple)) and len(pos) == 2:
            self._path.append((int(pos[0]), int(pos[1])))
        return out

    def update(self, feedback: Dict[str, Any]) -> None:
        if isinstance(feedback, dict):
            self._last_feedback = dict(feedback)
            try:
                sig_src = {}
                bus = self.core.primitives.get("signal_bus")
                if hasattr(bus, "signals"):
                    sig_src = dict(bus.signals())
                elif isinstance(bus, dict):
                    sig_src = dict(bus)
                self._last_field_update = dict(map_feedback_update(dict(self._last_obs or {}), dict(feedback), self.core.primitives, sig_src, {}) or {})
            except Exception:
                pass
        step_idx = int((self._last_obs or {}).get("step_idx", 0)) + 1
        cur_obs = (self._last_obs or {}).get("current_observation", {})
        visible = self._derive(cur_obs)
        packet = make_problem_packet(
            family="maze",
            step_idx=step_idx,
            action_space=["UP", "DOWN", "LEFT", "RIGHT"],
            current_observation=cur_obs,
            history=list(self._path[-128:]),
            trace=list(self._path[-128:]),
            feedback=dict(self._last_feedback or {}),
            residuals=visible["residuals"],
            probes=visible["probes"],
            signals=visible["signals"],
            constraints={},
            family_payload={},
            candidates=visible["candidates"],
            goal_field=visible["goal_field"],
            problem_contract=self._problem_contract(cur_obs),
            field_update=dict(self._last_field_update or {}),
            dyn_hint=visible["dyn_hint"],
            co_conf_hint=visible["co_conf_hint"],
            support_evidence=visible.get("support_evidence"),
        )
        try:
            if hasattr(self._pipe, "run_update"):
                self.core.step(packet, feedback or {})
            else:
                self.core.step(packet, feedback or {})
        except Exception:
            import os
            if os.environ.get("CO_STRICT_ERRORS", "") == "1":
                raise
            pass
