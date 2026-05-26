"""Bandit boundary adapter.

Publishes public arm/action facts and sampling-related burden effects for the
CO kernel.  It must not publish best-arm labels, baseline values, or hidden
policy conclusions.
"""

from __future__ import annotations
from typing import Any, Dict, Optional, List
from agents.co.boundary.problem_packet import (
    make_problem_packet,
    validate_problem_packet,
    validate_problem_update,
    attach_contract_debug,
    require_kernel_action,
)
from agents.co.adapters.common import ensure_signal_bus, public_effect, single_decision_slot_effect
from agents.co.boundary.update_mapper import map_feedback_update

def _bandit_measurement_evidence(n_arms: int, counts: List[int], global_coverage: float, recent_reward_means: List[float], goal_field: Dict[str, Any]) -> Dict[str, Any]:
    legal_count = int(max(1, n_arms))
    seen_ratio = float(sum(1 for c in counts if int(c) > 0) / float(max(1, n_arms))) if n_arms > 0 else 0.0
    reward_span = 0.0
    if recent_reward_means:
        reward_span = float(max(recent_reward_means) - min(recent_reward_means))
    predictive_entropy = float(max(0.0, min(1.0, 1.0 - reward_span)))
    return {
        "legal_count": legal_count,
        "blocked_count": 0.0,
        "exposed_action_count": legal_count,
        "legal_ratio": 1.0,
        "blocked_ratio": 0.0,
        "branching_fraction": 1.0,
        "coverage_adequacy": float(global_coverage),
        "seen_ratio": float(seen_ratio),
        "goal_observability": float(goal_field.get("goal_observability", 1.0) or 1.0),
        "goal_certainty": float(goal_field.get("goal_certainty", 0.5) or 0.5),
        "goal_stability": float(goal_field.get("goal_stability", 0.5) or 0.5),
        "predictive_entropy": predictive_entropy,
        "constraint_exposure": 0.0,
    }


def _bandit_public_effects(arm: int, *, support_depth: float, uncertainty_hint: float, recent_freq: float) -> List[Dict[str, Any]]:
    """Public burden/effect facts for bandit candidates.

    Pulling an arm is repeatable public sampling grammar: it can expose/reduce
    uncertainty for that arm while also using the single immediate action slot.
    The burden type is arm-local because sampling arm i does not reveal arm j.
    """
    arm_scope = f"arm_{int(arm)}"
    magnitude = max(0.05, min(1.0, float(uncertainty_hint)))
    effects: List[Dict[str, Any]] = [single_decision_slot_effect("bandit_action_slot")]
    effects.append(public_effect("carry", f"reward_uncertainty_{arm_scope}", magnitude=magnitude, scope=arm_scope, kind="uncertainty", public_basis="public_history", direction="unresolved", coupling="reward_feedback"))
    effects.append(public_effect("reduce", f"reward_uncertainty_{arm_scope}", magnitude=magnitude, scope=arm_scope, kind="evidence", public_basis="declared_transition_rule", direction="sample", coupling="reward_feedback"))
    if recent_freq > 0.0:
        effects.append(public_effect("carry", "commitment_revisit", magnitude=min(1.0, float(recent_freq)), scope="action_trace", public_basis="public_history", direction="repeat", coupling="single_decision_history"))
    return effects


class COAdapterBandit:
    def __init__(self, core, name: str = "CO", n_arms: int = 2) -> None:
        self.core = core
        self.name = name
        self.n_arms = int(n_arms)
        self._pipe = core.combinators.get("pipeline")
        self._last_obs: Optional[Dict[str, Any]] = None
        self._last_feedback: Optional[Dict[str, Any]] = None
        self._last_field_update: Dict[str, Any] = {}
        self._history: List[Dict[str, Any]] = []
        self._trace: List[int] = []
        self._incumbent_id: Optional[int] = None
        self._incumbent_decay_accum: float = 0.0
        self._line_memory: List[Dict[str, float]] = [
            {'support': 0.0, 'recent': 0.0, 'probe_debt': 1.0, 'contradiction': 0.0, 'reward_ema': 0.0}
            for _ in range(self.n_arms)
        ]


    def _problem_contract(self, obs: Dict[str, Any]) -> Dict[str, Any]:
        action_labels = [f"arm_{i}" for i in range(self.n_arms)]
        return {
            "actions": {"count": self.n_arms, "native_type": "discrete", "labels": action_labels},
            "observation_channels": ["action_identity", "reward_feedback", "trace_history"],
            "task_anchor": {"kind": "reward_maximization", "provided_externally": True, "notes": "maximize externally returned reward"},
            "hard_constraints": [],
            "soft_costs": [],
            "regime_anchors": ["action_identities", "action_space_cardinality"],
            "mutable_factors": ["candidate_goal_relation"],
            "timescale_profile": {"horizon_fixity": "fixed", "drift": "unknown", "notes": "arm identities fixed on active horizon; latent reward relation may or may not drift"},
            "observability_profile": {"state": "partial", "outcome": "direct", "constraints": "unknown"},
            "reversibility_profile": {"action_reversibility": "reversible", "commitment_cost": "medium", "notes": "actions are repeatable but mistaken hardening can be costly in regret"},
            "notes": "Bandit family emits declarative action/reward structure only; strategy must remain kernel-side.",
            "source": "adapter_visible_family_facts",
            "status": "adapter_emitted",
        }

    def _derive_from_visible_history(self, obs: Dict[str, Any], step_idx: int) -> Dict[str, Any]:
        bs = self.core.primitives.get("bandit_stats")
        means = [0.0] * self.n_arms
        counts = [0] * self.n_arms
        if bs is not None:
            try:
                if hasattr(bs, "ensure"):
                    bs.ensure(self.n_arms)
                if hasattr(bs, "means"):
                    means = list(bs.means[: self.n_arms])
                if hasattr(bs, "counts"):
                    counts = list(bs.counts[: self.n_arms])
            except Exception:
                pass

        total = max(1, sum(int(c) for c in counts))
        nonzero = sum(1 for c in counts if int(c) > 0)
        recent = list(self._trace[-8:])
        recent_fb = list(self._history[-16:])
        recent_reward_means = [0.0] * self.n_arms
        recent_reward_counts = [0] * self.n_arms
        for fb in recent_fb:
            try:
                aa = int(fb.get("action"))
                rr = float(fb.get("reward", 0.0) or 0.0)
            except Exception:
                continue
            if 0 <= aa < self.n_arms:
                recent_reward_means[aa] += rr
                recent_reward_counts[aa] += 1
        for i in range(self.n_arms):
            c = int(recent_reward_counts[i])
            if c > 0:
                recent_reward_means[i] = float(recent_reward_means[i]) / float(c)
            else:
                recent_reward_means[i] = float(means[i]) if i < len(means) else 0.0

        global_coverage = float(nonzero) / float(max(1, self.n_arms))
        residuals = {f"arm_{i}_gap": float(max(means) - means[i]) for i in range(len(means))} if means else {}
        probes = {f"arm_{i}_under_sampled": float(max(0.0, 1.0 - (float(counts[i]) / float(max(counts) or 1)))) for i in range(len(counts))} if counts else {}
        candidates = []
        support_levels: List[float] = []
        goal_scores: List[float] = []
        for i in range(self.n_arms):
            count_i = int(counts[i]) if i < len(counts) else 0
            mean_i = max(0.0, min(1.0, float(means[i]) if i < len(means) else 0.0))
            recent_mean = max(0.0, min(1.0, float(recent_reward_means[i])))
            support_depth = float(count_i) / float(count_i + 4) if count_i > 0 else 0.0
            tested_hint = 1.0 if count_i > 0 else 0.0
            recent_freq = float(sum(1 for a in recent if int(a) == i) / float(len(recent) or 1)) if recent else 0.0
            novelty_hint = max(0.0, 1.0 - recent_freq)
            uncertainty_hint = max(0.0, 1.0 - support_depth)
            goal_relation = 0.5 if count_i <= 0 else mean_i
            continuity_support = max(0.0, min(1.0, 0.20 + 0.80 * support_depth))
            contradiction_hint = max(0.0, min(1.0, support_depth * max(0.0, 0.5 - goal_relation) * 2.0))
            revisit_hint = recent_freq
            coverage_adequacy = global_coverage
            candidates.append({
                "candidate_id": int(i),
                "legal": True,
                "visible_delta": float(mean_i),
                "goal_relation": float(goal_relation),
                "support_depth": float(support_depth),
                "paired_depth": float(support_depth),
                "line_support": float(support_depth),
                "continuity_support": float(continuity_support),
                "recent_reward_mean": float(recent_mean),
                "obstruction_hint": 0.0,
                "novelty_hint": float(novelty_hint),
                "uncertainty_hint": float(uncertainty_hint),
                "reversibility_hint": 1.0,
                "trace_relation": float(recent_freq),
                "coverage_adequacy": float(coverage_adequacy),
                "contradiction_hint": float(contradiction_hint),
                "revisit_hint": float(revisit_hint),
                "tested_hint": float(tested_hint),
                "public_effects": _bandit_public_effects(
                    int(i),
                    support_depth=support_depth,
                    uncertainty_hint=uncertainty_hint,
                    recent_freq=recent_freq,
                ),
            })
            support_levels.append(support_depth)
            goal_scores.append(goal_relation)

        ordered = sorted(goal_scores, reverse=True)
        top = float(ordered[0] if ordered else 0.0)
        second = float(ordered[1] if len(ordered) > 1 else top)
        best_margin = max(0.0, top - second)
        goal_certainty = max(0.0, min(1.0, 0.55 * best_margin + 0.45 * global_coverage))
        goal_field = {
            "goal_mode": "graded",
            "goal_sharpness": float(best_margin),
            "goal_stability": float(max(0.0, min(1.0, 0.25 + 0.75 * global_coverage))),
            "goal_certainty": float(goal_certainty),
            "goal_observability": 1.0,
        }
        signals = {
            "z_PE": 0.0,
            "z_gain": float(max((self._last_feedback or {}).get("reward", 0.0) or 0.0, 0.0) if self._last_feedback else 0.0),
            "var_resid": float(sum(abs(v) for v in residuals.values()) / float(len(residuals) or 1)),
            "coverage_adequacy": float(global_coverage),
        }
        memory_view = {
            "counts": list(int(c) for c in counts),
            "means": list(float(m) for m in means),
            "recent_reward_means": list(float(v) for v in recent_reward_means),
            "coverage_adequacy": float(global_coverage),
        }
        dyn_hint = float(max(0.0, min(1.0, 1.0 - goal_certainty)))
        co_conf_hint = float(max(support_levels) if support_levels else 0.0)
        support_evidence = float(max(support_levels) if support_levels else 0.0)
        measurement_evidence = _bandit_measurement_evidence(self.n_arms, counts, global_coverage, recent_reward_means, goal_field)
        return {
            'residuals': residuals,
            'probes': probes,
            'signals': signals,
            'memory_view': memory_view,
            'measurement_evidence': measurement_evidence,
            'candidates': candidates,
            'goal_field': goal_field,
            'dyn_hint': dyn_hint,
            'co_conf_hint': co_conf_hint,
            'support_evidence': support_evidence,
        }
    def select(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        obs = dict(observation or {})
        step_idx = int(obs.get("t", obs.get("step_idx", 0) or 0))
        visible = self._derive_from_visible_history(obs, step_idx)
        packet = make_problem_packet(
            family="bandit",
            step_idx=step_idx,
            action_space=list(range(self.n_arms)),
            current_observation={"n_arms": self.n_arms, **obs},
            history=list(self._history[-64:]),
            trace=list(self._trace[-64:]),
            feedback=dict(self._last_feedback or {}),
            residuals=visible["residuals"],
            probes=visible["probes"],
            signals=visible["signals"],
            constraints={},
            family_payload={},
            memory_view=visible["memory_view"],
            measurement_evidence=visible.get("measurement_evidence"),
            candidates=visible["candidates"],
            goal_field=visible.get("goal_field"),
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
        out = require_kernel_action(out, legal_actions=list(range(self.n_arms)), family="bandit")
        attach_contract_debug(out, packet, warnings)
        out.setdefault("field_update", dict(self._last_field_update or {}))
        out.setdefault("field_update_warnings", validate_problem_update(self._last_field_update or {}))
        self._last_obs = dict(packet)
        return out

    def update(self, feedback: Dict[str, Any]) -> None:
        if isinstance(feedback, dict):
            self._last_feedback = dict(feedback)
            self._history.append(dict(feedback))
            act = feedback.get("action")
            if act is not None:
                try:
                    self._trace.append(int(act))
                except Exception:
                    pass
            bs = self.core.primitives.get("bandit_stats")
            if bs is not None:
                try:
                    if hasattr(bs, "update"):
                        bs.update(action=feedback.get("action"), reward=feedback.get("reward"), n_arms=self.n_arms)
                    elif hasattr(bs, "update_from_feedback"):
                        bs.update_from_feedback(self.n_arms, feedback.get("action"), feedback.get("reward"))
                except Exception:
                    pass
            try:
                sig_src = {}
                bus = self.core.primitives.get("signal_bus")
                if hasattr(bus, "signals"):
                    sig_src = dict(bus.signals())
                elif isinstance(bus, dict):
                    sig_src = dict(bus)
                base_obs = dict(self._last_obs or {})
                self._last_field_update = dict(map_feedback_update(base_obs, dict(feedback), self.core.primitives, sig_src, {}) or {})
            except Exception:
                pass
        step_idx = int((self._last_obs or {}).get("step_idx", 0)) + 1
        obs = dict((self._last_obs or {}).get("current_observation", {}) or {})
        obs.setdefault("family", "bandit")
        obs.setdefault("n_arms", self.n_arms)
        visible = self._derive_from_visible_history(obs, step_idx)
        packet = make_problem_packet(
            family="bandit",
            step_idx=step_idx,
            action_space=list(range(self.n_arms)),
            current_observation={"n_arms": self.n_arms},
            history=list(self._history[-64:]),
            trace=list(self._trace[-64:]),
            feedback=dict(self._last_feedback or {}),
            residuals=visible["residuals"],
            probes=visible["probes"],
            signals=visible["signals"],
            constraints={},
            family_payload={},
            memory_view=visible["memory_view"],
            measurement_evidence=visible.get("measurement_evidence"),
            candidates=visible["candidates"],
            goal_field=visible.get("goal_field"),
            problem_contract=self._problem_contract(obs),
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
