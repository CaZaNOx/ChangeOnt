"""Renewal boundary adapter.

Publishes public renewal/task facts and burden-effect carriers for the CO kernel
without exposing hidden renewal counters as policy advice.
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



def _clip01(x: float) -> float:
    try:
        return max(0.0, min(1.0, float(x)))
    except Exception:
        return 0.0


def _ablation_set(obs: Dict[str, Any], key: str) -> set[str]:
    try:
        raw = obs.get(key, ())
        if raw is None:
            return set()
        if isinstance(raw, str):
            return {str(raw)} if str(raw).strip() else set()
        return {str(x) for x in list(raw) if str(x).strip()}
    except Exception:
        return set()


def _apply_candidate_field_controls(candidates: List[Dict[str, Any]], obs: Dict[str, Any]) -> List[Dict[str, Any]]:
    drop = _ablation_set(obs, "field_ablation")
    keep_only = _ablation_set(obs, "field_keep_only")
    if not drop and not keep_only:
        return candidates
    controlled: List[Dict[str, Any]] = []
    target_fields = {"goal_relation", "context_relation", "reward_relation", "tested_hint", "continuity_support"}
    protected = {
        "candidate_id", "legal", "visible_delta", "support_depth", "paired_depth", "line_support",
        "coverage_adequacy", "contradiction_hint", "obstruction_hint", "uncertainty_hint", "novelty_hint",
        "trace_relation", "revisit_hint", "recent_reward_mean", "line_recent", "line_probe_debt",
        "reversibility_hint",
    }
    for cand in candidates:
        c = dict(cand)
        if keep_only:
            for f in target_fields:
                if f not in keep_only and f in c:
                    c[f] = 0.0
        if drop:
            for f in drop:
                if f in c:
                    c[f] = 0.0
        controlled.append(c)
    return controlled

def _renewal_measurement_evidence(A: int, coverage_adequacy: float, miss_rate: float, context_entropy_norm: float, predictive_certainty: float, row_support: float, context_support: float, goal_field: Dict[str, Any]) -> Dict[str, Any]:
    legal_count = int(max(1, A))
    return {
        "legal_count": legal_count,
        "blocked_count": 0.0,
        "exposed_action_count": legal_count,
        "legal_ratio": 1.0,
        "blocked_ratio": 0.0,
        "branching_fraction": 1.0,
        "coverage_adequacy": float(coverage_adequacy),
        "seen_ratio": float(coverage_adequacy),
        "miss_rate": float(miss_rate),
        "predictive_entropy": float(context_entropy_norm),
        "goal_observability": float(goal_field.get("goal_observability", 1.0) or 1.0),
        "goal_certainty": float(goal_field.get("goal_certainty", predictive_certainty) or predictive_certainty),
        "goal_stability": float(goal_field.get("goal_stability", 0.5) or 0.5),
        "constraint_exposure": 0.0,
        "support_alignment": float(max(0.0, min(1.0, 0.55 * context_support + 0.45 * row_support))),
    }


def _renewal_public_effects(
    symbol: int,
    *,
    uncertainty_hint: float,
    contradiction_hint: float,
    line_probe_debt: float,
    context_entropy: float,
) -> List[Dict[str, Any]]:
    """Public burden/effect facts for renewal/sequence candidates.

    Choosing a symbol is a public repeatable expression that can test/reduce
    symbol-local predictive uncertainty while all candidates compete for one
    immediate sequence-action slot.  These facts do not encode the true renewal
    phase or hidden generator.
    """
    sym_scope = f"sym_{int(symbol)}"
    uncertainty = max(0.0, min(1.0, float(uncertainty_hint)))
    effects: List[Dict[str, Any]] = [single_decision_slot_effect("renewal_action_slot")]
    effects.append(public_effect("carry", f"predictive_uncertainty_{sym_scope}", magnitude=max(0.05, uncertainty), scope=sym_scope, kind="uncertainty", public_basis="public_history", direction="unresolved", coupling="sequence_prediction"))
    effects.append(public_effect("reduce", f"predictive_uncertainty_{sym_scope}", magnitude=max(0.05, min(1.0, float(line_probe_debt))), scope=sym_scope, kind="evidence", public_basis="declared_transition_rule", direction="sample_or_test", coupling="sequence_prediction"))
    if contradiction_hint > 0.0:
        effects.append(public_effect("carry", "prediction_miss_burden", magnitude=min(1.0, float(contradiction_hint)), scope="sequence_history", public_basis="public_history", direction="misalignment", coupling="task_anchor"))
    if context_entropy > 0.0:
        effects.append(public_effect("carry", "context_entropy", magnitude=min(1.0, float(context_entropy)), scope="sequence_context", kind="uncertainty", public_basis="public_history", direction="diffuse", coupling="sequence_prediction"))
    return effects


class COAdapterRenewal:
    def __init__(self, core, name: str = "CO") -> None:
        self.core = core
        self.name = name
        self._pipe = core.combinators.get("pipeline")
        self._last_obs: Optional[Dict[str, Any]] = None
        self._history: List[int] = []
        self._action_history: List[int] = []
        self._reward_history: List[float] = []
        self._last_feedback: Optional[Dict[str, Any]] = None
        self._last_field_update: Dict[str, Any] = {}

    def _problem_contract(self, obs: Dict[str, Any]) -> Dict[str, Any]:
        A = int(obs.get("A", 0) or 0)
        labels = [f"sym_{i}" for i in range(A)]
        return {
            "actions": {"count": A, "native_type": "discrete", "labels": labels},
            "observation_channels": ["symbol_observation", "reward_feedback", "trace_history"],
            "task_anchor": {"kind": "predictive_reward_alignment", "provided_externally": True, "notes": "align actions with reward-bearing sequence structure"},
            "hard_constraints": [],
            "soft_costs": [],
            "regime_anchors": ["alphabet_cardinality", "action_space_cardinality"],
            "mutable_factors": ["symbol_transition_relation", "reward_alignment_relation"],
            "timescale_profile": {"horizon_fixity": "mixed", "drift": "unknown", "notes": "alphabet is fixed; useful transition relations may vary over the active horizon"},
            "observability_profile": {"state": "direct", "outcome": "direct", "constraints": "unknown"},
            "reversibility_profile": {"action_reversibility": "reversible", "commitment_cost": "medium", "notes": "wrong local hardening can be revised but incurs miss cost"},
            "notes": "Renewal family emits visible sequence and reward history only; no family-local periodicity or policy labels.",
            "source": "adapter_visible_family_facts",
            "status": "adapter_emitted",
        }


    def _derive_from_visible_history(self, obs: Dict[str, Any]) -> Dict[str, Any]:
        import math

        A = int(obs.get("A", 0) or 0)
        hist = [int(x) for x in list(self._history[-128:]) if 0 <= int(x) < max(1, A)]
        reward_hist = [float(r) for r in list(self._reward_history[-64:])]
        action_hist = [int(a) for a in list(self._action_history[-64:]) if 0 <= int(a) < max(1, A)]
        prior = 1.0 / float(max(1, A)) if A > 0 else 0.0

        def _entropy_norm(dist: Dict[int, float]) -> float:
            if A <= 1:
                return 0.0
            vals = [max(0.0, float(dist.get(i, 0.0))) for i in range(A)]
            total = sum(vals)
            if total <= 0.0:
                return 1.0
            vals = [v / total for v in vals]
            ent = -sum(v * math.log(max(v, 1e-12)) for v in vals if v > 0.0)
            return float(max(0.0, min(1.0, ent / math.log(float(A)))))

        current_obs = int(obs.get("obs", hist[-1] if hist else 0) or 0) if A > 0 else 0

        symbol_counts = {i: 0 for i in range(A)}
        for x in hist:
            symbol_counts[int(x)] += 1
        hist_len = float(len(hist) or 1)
        symbol_freq = {i: (float(symbol_counts.get(i, 0)) / hist_len if hist else prior) for i in range(A)}

        transition_counts = {i: {j: 0 for j in range(A)} for i in range(A)}
        antecedent_counts = {i: 0 for i in range(A)}
        for a, b in zip(hist[:-1], hist[1:]):
            if 0 <= int(a) < A and 0 <= int(b) < A:
                transition_counts[int(a)][int(b)] += 1
                antecedent_counts[int(a)] += 1
        row_total = int(antecedent_counts.get(current_obs, 0) or 0)
        row_support = float(row_total) / float(row_total + max(4, A or 1)) if A > 0 else 0.0
        transition_freq = {
            i: (float(transition_counts[current_obs].get(i, 0)) / float(row_total) if row_total > 0 else prior)
            for i in range(A)
        }

        max_ctx = min(4, max(0, len(hist) - 1))
        context_mix = {i: 0.0 for i in range(A)}
        context_weight_sum = 0.0
        context_support = 0.0
        if A > 0 and hist:
            for k in range(1, max_ctx + 1):
                ctx = tuple(hist[-k:])
                counts = {i: 0 for i in range(A)}
                total = 0
                for idx in range(0, max(0, len(hist) - k)):
                    if tuple(hist[idx:idx + k]) == ctx:
                        nxt = int(hist[idx + k])
                        if 0 <= nxt < A:
                            counts[nxt] += 1
                            total += 1
                if total <= 0:
                    continue
                support = float(total) / float(total + max(2, A))
                depth_weight = float(k) / float(max_ctx or 1)
                weight = support * (0.30 + 0.70 * depth_weight)
                context_weight_sum += weight
                context_support = max(context_support, support * depth_weight)
                for i in range(A):
                    context_mix[i] += weight * (float(counts.get(i, 0)) / float(total))
        if context_weight_sum > 0.0:
            context_freq = {i: float(context_mix.get(i, 0.0)) / float(context_weight_sum) for i in range(A)}
        else:
            context_freq = {i: float(transition_freq.get(i, prior)) for i in range(A)}

        ngram_freq = {i: prior for i in range(A)}
        ng_support = 0.0
        ng = self.core.primitives.get("ngram_model") if hasattr(self.core, 'primitives') else None
        if ng is not None and hasattr(ng, 'predict_proba'):
            try:
                probs = dict(ng.predict_proba() or {})
                if probs:
                    ngram_freq = {i: float(probs.get(i, prior)) for i in range(A)}
                    ng_support = float(max(ngram_freq.values()) if ngram_freq else 0.0)
            except Exception:
                pass

        action_counts = {i: 0 for i in range(A)}
        action_hits = {i: 0.0 for i in range(A)}
        action_recent_hits = {i: [] for i in range(A)}
        for a, r in zip(action_hist, reward_hist[-len(action_hist):]):
            if 0 <= int(a) < A:
                ai = int(a)
                action_counts[ai] += 1
                action_hits[ai] += float(r)
                action_recent_hits[ai].append(float(r))
                if len(action_recent_hits[ai]) > 8:
                    action_recent_hits[ai] = action_recent_hits[ai][-8:]
        action_freq = {i: float(action_counts.get(i, 0)) / float(len(action_hist) or 1) for i in range(A)} if A > 0 else {}
        action_success = {
            i: (float(action_hits.get(i, 0.0)) / float(action_counts.get(i, 0) or 1) if action_counts.get(i, 0) > 0 else prior)
            for i in range(A)
        }
        action_recent_success = {
            i: (float(sum(action_recent_hits.get(i, []))) / float(len(action_recent_hits.get(i, [])) or 1) if action_recent_hits.get(i) else action_success.get(i, prior))
            for i in range(A)
        }
        action_support = {i: float(action_counts.get(i, 0)) / float(action_counts.get(i, 0) + max(3, A)) for i in range(A)} if A > 0 else {}

        miss_streak = 0
        for r in reversed(reward_hist):
            if float(r) < 0.5:
                miss_streak += 1
            else:
                break
        miss_rate = float(sum(1 for r in reward_hist if float(r) < 0.5)) / float(len(reward_hist) or 1)
        avg_reward = float(sum(float(r) for r in reward_hist) / float(len(reward_hist) or 1)) if reward_hist else 0.0

        global_entropy_norm = _entropy_norm(symbol_freq)
        row_entropy_norm = _entropy_norm(transition_freq) if row_total > 0 else 1.0
        context_entropy_norm = _entropy_norm(context_freq) if context_weight_sum > 0.0 else row_entropy_norm
        ngram_entropy_norm = _entropy_norm(ngram_freq) if ng_support > 0.0 else context_entropy_norm
        coverage_adequacy = float(len(set(hist)) / float(max(1, A))) if hist and A > 0 else 0.0

        candidates = []
        goal_scores = []
        tested_levels = []
        for i in range(A):
            trans = float(transition_freq.get(i, prior))
            ctx = float(context_freq.get(i, trans))
            ngf = float(ngram_freq.get(i, ctx))
            global_f = float(symbol_freq.get(i, prior))
            act_freq = float(action_freq.get(i, 0.0))
            act_success = float(action_success.get(i, prior))
            act_recent = float(action_recent_success.get(i, act_success))
            act_support = float(action_support.get(i, 0.0))
            sequence_relation = float(max(0.0, min(1.0, 0.55 * ctx + 0.25 * ngf + 0.20 * trans)))
            reward_relation = float(max(0.0, min(1.0, 0.60 * act_recent + 0.40 * act_success)))
            goal_relation = float(max(0.0, min(1.0, 0.68 * sequence_relation + 0.22 * reward_relation + 0.10 * global_f)))
            support_depth = float(max(0.0, min(1.0, 0.45 * context_support + 0.30 * row_support + 0.15 * ng_support + 0.10 * act_support)))
            paired_depth = float(max(0.0, min(1.0, 0.55 * support_depth + 0.45 * act_support)))
            line_support = float(max(0.0, min(1.0, 0.60 * context_support + 0.40 * row_support)))
            tested_hint = float(max(0.0, min(1.0, 0.45 * support_depth + 0.35 * act_support + 0.20 * goal_relation)))
            continuity_support = float(max(0.0, min(1.0, (0.35 + 0.65 * goal_relation) * max(support_depth, 0.15 * act_support + 0.85 * line_support))))
            contradiction_hint = float(max(0.0, min(1.0, 0.55 * miss_rate * (1.0 - goal_relation) + 0.25 * act_support * (1.0 - act_recent) + 0.20 * max(0.0, context_entropy_norm - support_depth))))
            uncertainty_hint = float(max(0.0, min(1.0, 0.45 * context_entropy_norm + 0.25 * ngram_entropy_norm + 0.20 * (1.0 - support_depth) + 0.10 * (1.0 - act_support))))
            novelty_hint = float(max(0.0, min(1.0, 1.0 - global_f)))
            trace_relation = float(max(0.0, min(1.0, 0.60 * sequence_relation + 0.40 * trans)))
            revisit_hint = float(max(0.0, min(1.0, act_freq * (1.0 - act_recent) * (0.35 + 0.65 * (1.0 - support_depth)))))
            line_probe_debt = float(max(0.0, min(1.0, 1.0 - tested_hint)))
            candidates.append({
                "candidate_id": int(i),
                "legal": True,
                "visible_delta": float(global_f),
                "goal_relation": float(goal_relation),
                "continuity_support": float(continuity_support),
                "obstruction_hint": float(contradiction_hint),
                "novelty_hint": float(novelty_hint),
                "uncertainty_hint": float(uncertainty_hint),
                "reversibility_hint": 1.0,
                "trace_relation": float(trace_relation),
                "support_depth": float(support_depth),
                "paired_depth": float(paired_depth),
                "line_support": float(line_support),
                "coverage_adequacy": float(coverage_adequacy),
                "contradiction_hint": float(contradiction_hint),
                "revisit_hint": float(revisit_hint),
                "tested_hint": float(tested_hint),
                "recent_reward_mean": float(act_recent),
                "line_recent": float(act_recent),
                "line_probe_debt": float(line_probe_debt),
                "context_relation": float(ctx),
                "reward_relation": float(reward_relation),
                "sequence_relation": float(sequence_relation),
                "action_support_hint": float(act_support),
                "context_support_hint": float(context_support),
                "row_support_hint": float(row_support),
                "ngram_support_hint": float(ng_support),
                "context_entropy_hint": float(context_entropy_norm),
                "row_entropy_hint": float(row_entropy_norm),
                "public_effects": _renewal_public_effects(
                    int(i),
                    uncertainty_hint=uncertainty_hint,
                    contradiction_hint=contradiction_hint,
                    line_probe_debt=line_probe_debt,
                    context_entropy=context_entropy_norm,
                ),
            })
            goal_scores.append(goal_relation)
            tested_levels.append(tested_hint)

        candidates = _apply_candidate_field_controls(candidates, obs)
        goal_scores = [float(c.get("goal_relation", 0.0) or 0.0) for c in candidates]
        tested_levels = [float(c.get("tested_hint", 0.0) or 0.0) for c in candidates]

        ordered = sorted(goal_scores, reverse=True)
        top = float(ordered[0] if ordered else 0.0)
        second = float(ordered[1] if len(ordered) > 1 else top)
        best_margin = float(max(0.0, top - second))
        certainty_support = float(max(0.0, min(1.0, 0.45 * context_support + 0.25 * row_support + 0.15 * ng_support + 0.15 * coverage_adequacy)))
        predictive_certainty = float(max(0.0, min(1.0, top * (1.0 - context_entropy_norm) * (0.30 + 0.70 * certainty_support))))
        goal_field = {
            "goal_mode": "graded",
            "goal_sharpness": float(best_margin),
            "goal_stability": float(max(0.0, min(1.0, 0.30 * (1.0 - miss_rate) + 0.20 * (1.0 - context_entropy_norm) + 0.15 * (1.0 - row_entropy_norm) + 0.20 * coverage_adequacy + 0.15 * certainty_support))),
            "goal_certainty": float(predictive_certainty),
            "goal_observability": 1.0,
        }
        residuals = {f"sym_{k}": float(max(0.0, 1.0 - context_freq.get(k, prior))) for k in range(A)} if A > 0 else {}
        probes = {f"next_ctx_{current_obs}_{i}": float(context_freq.get(i, prior)) for i in range(A)} if A > 0 else {}
        signals = {
            "z_PE": float(1.0 - top if goal_scores else 0.0),
            "z_gain": float(top if goal_scores else 0.0),
            "var_resid": float(sum(residuals.values()) / float(len(residuals) or 1)),
            "miss_streak": float(miss_streak),
            "miss_rate": float(miss_rate),
            "avg_reward": float(avg_reward),
            "coverage_adequacy": float(coverage_adequacy),
            "predictive_entropy": float(context_entropy_norm),
            "predictive_certainty": float(predictive_certainty),
            "transition_row_support": float(row_support),
            "context_support": float(context_support),
            "ngram_support": float(ng_support),
        }
        memory_view = {
            "observation_history": hist,
            "action_history": action_hist,
            "reward_history": reward_hist,
            "symbol_freq": dict(symbol_freq),
            "transition_row": dict(transition_freq),
            "context_row": dict(context_freq),
            "current_symbol": int(current_obs) if A > 0 else None,
            "transition_row_support": float(row_support),
            "context_support": float(context_support),
            "ngram_support": float(ng_support),
            "miss_streak": miss_streak,
            "miss_rate": miss_rate,
            "avg_reward": avg_reward,
            "coverage_adequacy": coverage_adequacy,
            "predictive_entropy": context_entropy_norm,
            "predictive_certainty": predictive_certainty,
        }
        dyn_hint = float(max(0.0, min(1.0, 0.35 * miss_rate + 0.25 * context_entropy_norm + 0.20 * ngram_entropy_norm + 0.20 * (1.0 - certainty_support))))
        co_conf_hint = float(max(tested_levels) if tested_levels else 0.0)
        support_evidence = float(max(tested_levels) if tested_levels else 0.0)
        measurement_evidence = _renewal_measurement_evidence(A, coverage_adequacy, miss_rate, context_entropy_norm, predictive_certainty, row_support, context_support, goal_field)
        return {
            "residuals": residuals,
            "probes": probes,
            "signals": signals,
            "memory_view": memory_view,
            "measurement_evidence": measurement_evidence,
            "candidates": candidates,
            "goal_field": goal_field,
            "dyn_hint": dyn_hint,
            "co_conf_hint": co_conf_hint,
            "support_evidence": support_evidence,
        }

    def _packet(self, observation: Dict[str, Any], step_idx: int) -> Dict[str, Any]:
        obs = dict(observation or {})
        A = int(obs.get("A", 0) or 0)
        visible = self._derive_from_visible_history(obs)
        runtime_contract = {}
        try:
            if hasattr(self.core, "export_runtime_contract"):
                runtime_contract = dict(self.core.export_runtime_contract() or {})
        except Exception:
            runtime_contract = {}
        problem_contract = runtime_contract.get("problem_contract", {}) if isinstance(runtime_contract, dict) else {}
        target_scope = str(problem_contract.get("decision_scope", "") or "").strip().lower()
        packet = make_problem_packet(
            family="renewal",
            step_idx=step_idx,
            action_space=list(range(A)) if A > 0 else list(obs.get("action_space") or []),
            current_observation=obs,
            history=list(self._history[-128:]),
            trace=list(self._history[-128:]),
            feedback=dict(self._last_feedback or {}),
            residuals=visible["residuals"],
            probes=visible["probes"],
            signals=visible["signals"],
            constraints={},
            family_payload={"A": A},
            memory_view=visible["memory_view"],
            measurement_evidence=visible.get("measurement_evidence"),
            candidates=visible["candidates"],
            goal_field=visible["goal_field"],
            problem_contract=self._problem_contract(obs),
            field_update=dict(self._last_field_update or {}),
            dyn_hint=visible["dyn_hint"],
            co_conf_hint=visible["co_conf_hint"],
            support_evidence=visible["support_evidence"],
        )
        if target_scope:
            packet["_decision_scope"] = target_scope
            packet["problem_scope"] = target_scope
        if obs.get("field_ablation") is not None:
            packet["field_ablation"] = list(obs.get("field_ablation") or [])
        if obs.get("field_keep_only") is not None:
            packet["field_keep_only"] = list(obs.get("field_keep_only") or [])
        return packet

    def select(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        obs = dict(observation or {})
        step_idx = int(obs.get("t", obs.get("step_idx", 0) or 0))
        packet = self._packet(obs, step_idx)
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
        out = require_kernel_action(out, legal_actions=list(packet.get("action_space") or []), family="renewal")
        attach_contract_debug(out, packet, warnings)
        out.setdefault("field_update", dict(self._last_field_update or {}))
        out.setdefault("field_update_warnings", validate_problem_update(self._last_field_update or {}))
        self._last_obs = dict(packet)
        return out

    def update(self, feedback: Dict[str, Any]) -> None:
        if isinstance(feedback, dict):
            self._last_feedback = dict(feedback)
            nxt = feedback.get("observation")
            if isinstance(nxt, int):
                self._history.append(int(nxt))
            act = feedback.get("action")
            rew = feedback.get("reward")
            if isinstance(act, int):
                self._action_history.append(int(act))
                if len(self._action_history) > 256:
                    self._action_history = self._action_history[-256:]
            if isinstance(rew, (int, float)):
                self._reward_history.append(float(rew))
                if len(self._reward_history) > 256:
                    self._reward_history = self._reward_history[-256:]
            ng = self.core.primitives.get("ngram_model")
            if ng is not None and isinstance(nxt, int):
                try:
                    if hasattr(ng, "ensure"):
                        ng.ensure(A=(self._last_obs or {}).get("family_payload", {}).get("A"), order=getattr(ng, "k", None))
                    if hasattr(ng, "on_feedback"):
                        ng.on_feedback(int(nxt))
                except Exception:
                    pass
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
        packet = self._packet((self._last_obs or {}).get("current_observation", {}), step_idx)
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
