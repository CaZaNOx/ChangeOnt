# agents/co/core/elements/EC_identity.py
from __future__ import annotations
from typing import Dict, Any, Iterable, List, Tuple
from dataclasses import dataclass
from statistics import mean
from ..primitives.identity import TraceMemory
from ..derived.adaptation_debt import derive_adaptation_debt
from ._shared import publish_signal, get_semantic

@dataclass
class EC_Identity:
    """
    EC_Identity (v1): local identity judgment under bend distance.
    Primitive deps (intended): P1_BendMetric, canonical identity memory; optional P12_ClosureQuotient later.
    Combinator form (intended): SC_GatedThreshold (primary).
    Formula status: provisional (threshold structure binding).
    """
    PRIMITIVE_DEPS = ("P1_BendMetric", "identity memory", "P12_ClosureQuotient (optional)")
    COMBINATOR_FORM = "SC_GatedThreshold"
    COMBINATOR_DEPS = ("SC_GatedThreshold",)
    FORMULA_STATUS = "provisional"

    mem_len: int = 64
    trace_len: int = 0

    def configure(self, params, context):
        try:
            self.mem_len = int(params.get("mem_len", self.mem_len))
            self.trace_len = int(params.get("trace_len", self.trace_len))
        except Exception:
            pass
        return self

    def _normalize_trace(self, trace: Iterable[Any], trace_len: int, pad_token: Any) -> List[Any]:
        t = list(trace)
        if trace_len > 0 and len(t) > trace_len:
            t = t[-trace_len:]
        if trace_len > 0 and len(t) < trace_len:
            t = [pad_token] * (trace_len - len(t)) + t
        return t

    def _get_eps(self, header: Any) -> float:
        eps_id = getattr(getattr(header, "state", object()), "eps_id", None)
        if eps_id is None:
            return 0.20
        try:
            return float(eps_id)
        except Exception:
            return 0.20

    def _candidate_support_mass(self, cand: Dict[str, Any]) -> float:
        try:
            depth = float(cand.get("support_depth", 0.0) or 0.0)
        except Exception:
            depth = 0.0
        try:
            line_support = float(cand.get("line_support", depth) or depth)
        except Exception:
            line_support = depth
        try:
            pair_depth = float(cand.get("paired_depth", depth) or depth)
        except Exception:
            pair_depth = depth
        mass = 0.45 * depth + 0.35 * line_support + 0.20 * pair_depth
        return max(0.0, min(1.0, mass))

    def _candidate_priority(self, cand: Dict[str, Any]) -> float:
        support_mass = self._candidate_support_mass(cand)
        goal_relation = max(0.0, min(1.0, float(cand.get("goal_relation", cand.get("visible_delta", 0.0)) or 0.0)))
        recent_mean = max(0.0, min(1.0, float(cand.get("recent_reward_mean", cand.get("line_recent", 0.0)) or 0.0)))
        uncertainty = max(0.0, min(1.0, float(cand.get("uncertainty_hint", 0.0) or 0.0)))
        return 0.45 * goal_relation + 0.25 * recent_mean + 0.20 * support_mass + 0.10 * uncertainty

    def _history_metrics(self, trace: List[Any], prev: List[Tuple[Any, ...]], last_d: float, identity_ok: bool, observation: Dict[str, Any], header: Any) -> Dict[str, float]:
        continuity_conf = max(0.0, min(1.0, 1.0 - float(last_d)))
        fracture_pressure = max(0.0, min(1.0, float(last_d)))
        switch_rate = 0.0
        if len(trace) >= 2:
            switches = sum(1 for a, b in zip(trace[:-1], trace[1:]) if a != b)
            switch_rate = float(switches) / float(max(1, len(trace) - 1))
        recurrence = 0.0
        if trace:
            recurrence = 1.0 - (len(set(trace)) / float(len(trace)))
            recurrence = max(0.0, min(1.0, recurrence))
        trajectory_stability = max(0.0, min(1.0, continuity_conf * (1.0 - 0.5 * switch_rate)))

        incumbent_stability = trajectory_stability
        best_margin = 0.0
        estimate_drift = 0.0
        contradiction = 0.0
        takeover_potential = 0.0

        cands = [dict(c) for c in list(observation.get("candidates") or []) if isinstance(c, dict) and bool(c.get("legal", True))]
        if cands:
            ranked = sorted(cands, key=self._candidate_priority, reverse=True)
            incumbent = ranked[0] if ranked else None
            challenger = ranked[1] if len(ranked) > 1 else incumbent
            inc_support = self._candidate_support_mass(incumbent or {})
            chal_support = self._candidate_support_mass(challenger or {})
            inc_priority = self._candidate_priority(incumbent or {})
            chal_priority = self._candidate_priority(challenger or {})
            best_margin = max(0.0, inc_priority - chal_priority)
            evidence = float(observation.get("support_evidence", 0.0) or 0.0)
            support_conf = max(inc_support, evidence)
            contradiction = max(
                float((incumbent or {}).get("contradiction_hint", 0.0) or 0.0),
                float((challenger or {}).get("contradiction_hint", 0.0) or 0.0),
                max(0.0, chal_support - inc_support),
            )
            takeover_potential = max(
                0.0,
                max(0.0, chal_priority - inc_priority) + 0.35 * max(0.0, chal_support - inc_support) + 0.20 * float((challenger or {}).get("novelty_hint", 0.0) or 0.0),
            )
            estimate_drift = max(0.0, 0.55 * (1.0 - min(1.0, best_margin)) + 0.45 * contradiction)
            incumbent_stability = max(0.0, min(1.0, 0.65 * support_conf + 0.35 * best_margin))
            trajectory_stability = max(0.0, min(1.0, 0.55 * incumbent_stability + 0.25 * continuity_conf + 0.20 * (1.0 - contradiction)))
            continuity_conf = max(0.0, min(1.0,
                0.25 * continuity_conf + 0.35 * support_conf + 0.20 * best_margin + 0.10 * trajectory_stability - 0.25 * contradiction - 0.15 * takeover_potential
            ))
            fracture_pressure = max(0.0, min(1.0,
                1.0 - continuity_conf + 0.25 * estimate_drift + 0.20 * contradiction + 0.15 * takeover_potential
            ))
        else:
            mem = dict(observation.get("memory_view", {}) or {})
            top = 0.0
            second = 0.0
            if isinstance(mem.get("blended_proba"), dict) and mem.get("blended_proba"):
                vals = sorted([float(v) for v in mem.get("blended_proba", {}).values()])
                top = vals[-1]
                second = vals[-2] if len(vals) >= 2 else 0.0
            elif isinstance(mem.get("ngram_proba"), dict) and mem.get("ngram_proba"):
                vals = sorted([float(v) for v in mem.get("ngram_proba", {}).values()])
                top = vals[-1]
                second = vals[-2] if len(vals) >= 2 else 0.0
            if top > 0.0:
                best_margin = max(0.0, top - second)
                miss_rate = max(0.0, min(1.0, float(mem.get("miss_rate", 0.0) or 0.0)))
                continuity_conf = max(0.0, min(1.0, 0.30 * continuity_conf + 0.35 * top + 0.15 * max(0.0, 1.0 - switch_rate) + 0.20 * (1.0 - miss_rate)))
                fracture_pressure = max(0.0, min(1.0, 1.0 - continuity_conf + 0.20 * miss_rate + 0.15 * (1.0 - top)))
                incumbent_stability = max(0.0, min(1.0, 0.70 * top + 0.30 * best_margin))
                estimate_drift = max(0.0, min(1.0, 0.60 * miss_rate + 0.40 * (1.0 - top)))

        hs = getattr(header, "state", header)
        try:
            evidence_gate = max(0.0, min(1.0, float(getattr(hs, "evidence_gate", 1.0))))
        except Exception:
            evidence_gate = 1.0
        try:
            identity_hardness = max(0.0, min(1.0, float(getattr(hs, "identity_hardness", 0.5))))
        except Exception:
            identity_hardness = 0.5
        try:
            fracture_tolerance = max(0.0, min(1.0, float(getattr(hs, "fracture_tolerance", 0.5))))
        except Exception:
            fracture_tolerance = 0.5
        precommit_cap = max(0.03, min(0.85, 0.03 + 0.08 * identity_hardness + 0.35 * evidence_gate))
        continuity_conf = min(float(continuity_conf), precommit_cap)
        incumbent_stability = float(incumbent_stability) * (0.10 + 0.90 * evidence_gate)
        trajectory_stability = float(trajectory_stability) * (0.15 + 0.85 * evidence_gate)
        best_margin = float(best_margin) * (0.10 + 0.90 * evidence_gate)
        fracture_floor = max(0.0, min(1.0, 0.10 + 0.45 * (1.0 - evidence_gate) + 0.20 * fracture_tolerance))
        fracture_pressure = max(float(fracture_pressure), fracture_floor)

        return {
            "continuity_conf": float(max(0.0, min(1.0, continuity_conf))),
            "fracture_pressure": float(max(0.0, min(1.0, fracture_pressure))),
            "switch_pressure": float(max(0.0, min(1.0, switch_rate))),
            "trajectory_stability": float(max(0.0, min(1.0, trajectory_stability))),
            "incumbent_stability": float(max(0.0, min(1.0, incumbent_stability))),
            "best_margin": float(max(0.0, best_margin)),
            "estimate_drift": float(max(0.0, estimate_drift)),
            "recurrence": float(max(0.0, min(1.0, recurrence))),
            "evidence_gate": float(max(0.0, min(1.0, evidence_gate))),
            "incumbent_contradiction": float(max(0.0, min(1.0, contradiction))),
            "takeover_potential": float(max(0.0, min(1.0, takeover_potential))),
            "identity_ok": 1.0 if identity_ok else 0.0,
        }

    def _run_core(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any) -> Dict[str, Any]:
        eps = self._get_eps(header)
        P1 = primitives.get("P1")
        if P1 is None:
            raise RuntimeError("EC_Identity requires primitives['P1'] (P1_BendMetric) but it is missing.")
        trace_len = self.trace_len if self.trace_len > 0 else int(getattr(P1, "L", 0) or 0)
        pad_token = getattr(P1, "PAD_TOKEN", None)
        hist = list(observation.get("history", ()))
        trace = observation.get("trace", hist)
        if isinstance(trace, (list, tuple)):
            trace = self._normalize_trace(trace, trace_len, pad_token)
        else:
            trace = self._normalize_trace(hist, trace_len, pad_token)

        mem = primitives.get("id_mem")
        if mem is None:
            mem = TraceMemory(maxlen=self.mem_len)
            primitives["id_mem"] = mem

        prev = mem.traces()
        last_d = 1.0
        identity_ok = False
        bend_trigger = 0
        reid_summary = None
        if prev and trace:
            if hasattr(P1, "directional_bend"):
                last_d = min(float(P1.directional_bend(p, trace)) for p in prev)
            elif hasattr(P1, "bend_distance"):
                last_d = min(float(P1.bend_distance(trace, p)) for p in prev)
            elif hasattr(P1, "d_bend"):
                last_d = min(float(P1.d_bend(trace, p)) for p in prev)
            else:
                raise RuntimeError("P1_BendMetric has no supported API (directional_bend/bend_distance/d_bend).")
            P4 = primitives.get("P4")
            if P4 is not None:
                try:
                    if hasattr(P4, "compare_memory"):
                        reid_summary = P4.compare_memory(
                            trace,
                            prev,
                            lambda a, b: float(P1.bend_distance(a, b)),
                            bend_components=getattr(P1, "bend_components", None),
                        )
                    elif hasattr(P4, "compare_pair"):
                        reid_summary = P4.compare_pair(
                            trace,
                            prev[-1],
                            lambda a, b: float(P1.bend_distance(a, b)),
                            bend_components=getattr(P1, "bend_components", None),
                        )
                except Exception:
                    reid_summary = None
            sem = get_semantic(primitives)
            sc_gate = sem.get("SC_GatedThreshold")
            if sc_gate is None:
                raise RuntimeError("EC_Identity requires semantic combinator SC_GatedThreshold.")
            gate_distance = float(reid_summary.get("fracture_pressure", last_d)) if isinstance(reid_summary, dict) else float(last_d)
            identity_ok = bool(sc_gate.activate(gate_distance, eps, gate_ok=True, direction="lte"))
            bend_trigger = 1 if (gate_distance > eps) else 0

        # compute class count from closure over recent traces
        if hasattr(P1, "closure"):
            classes = P1.closure(prev + ([tuple(trace)] if trace else []), eps) if (prev or trace) else []
        else:
            classes = prev + ([tuple(trace)] if trace else [])
        class_count = len(classes)

        # update memory after computing distance
        if trace:
            mem.push(tuple(trace))

        metrics = self._history_metrics(trace, prev, last_d, identity_ok, observation, header)
        if isinstance(reid_summary, dict):
            metrics["continuity_conf"] = 0.65 * float(metrics.get("continuity_conf", 0.0)) + 0.35 * float(reid_summary.get("continuity_conf", 0.0))
            metrics["fracture_pressure"] = 0.65 * float(metrics.get("fracture_pressure", 0.0)) + 0.35 * float(reid_summary.get("fracture_pressure", 0.0))
            metrics["reid_frequency"] = float(reid_summary.get("reid_frequency", 0.0))
        else:
            metrics["reid_frequency"] = 0.0

        debt_state = primitives.setdefault("_adaptation_debt_state", {"debt": 0.0, "prev_misfit": 0.0})
        debt_terms = derive_adaptation_debt(
            prev_debt=float(debt_state.get("debt", 0.0) or 0.0),
            prev_misfit=float(debt_state.get("prev_misfit", 0.0) or 0.0),
            continuity_conf=float(metrics.get("continuity_conf", 0.0)),
            trajectory_stability=float(metrics.get("trajectory_stability", 0.0)),
            incumbent_stability=float(metrics.get("incumbent_stability", 0.0)),
            fracture_pressure=float(metrics.get("fracture_pressure", 0.0)),
            estimate_drift=float(metrics.get("estimate_drift", 0.0)),
            field_update=observation.get("field_update", {}) or {},
        )
        debt_state["debt"] = float(debt_terms["adaptation_debt"])
        debt_state["prev_misfit"] = float(debt_terms["fit_mismatch"])

        return {
            "eps": eps,
            "identity_ok": identity_ok,
            "last_d": float(last_d),
            "bend_trigger": int(bend_trigger),
            "class_count": int(class_count),
            **metrics,
            **debt_terms,
        }

    def update(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None) -> Dict[str, Any]:
        # Update pass only records the last action for trace construction.
        if feedback:
            try:
                act = feedback.get("action", None)
            except Exception:
                act = None
            if act is not None:
                mem = primitives.get("id_mem")
                if mem is None:
                    mem = TraceMemory(maxlen=self.mem_len)
                    primitives["id_mem"] = mem
                mem.last_action = act
        return {}

    def step(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None) -> Dict[str, Any]:
        obs = dict(observation or {})
        # If no explicit history/trace provided, use last action from id_mem (if any).
        if "history" not in obs and "trace" not in obs:
            mem = primitives.get("id_mem")
            act = getattr(mem, "last_action", None) if mem is not None else None
            obs["history"] = [] if act is None else [act]

        out = self._run_core(obs, primitives, header)
        bus = primitives.get("signal_bus")
        publish_signal(bus, "EC_Identity.same",   1.0 if out["identity_ok"] else 0.0)
        publish_signal(bus, "EC_Identity.last_d", out["last_d"])
        publish_signal(bus, "EC_Identity.continuity_conf", out.get("continuity_conf", 0.0))
        publish_signal(bus, "EC_Identity.fracture_pressure", out.get("fracture_pressure", 0.0))
        publish_signal(bus, "Identity.admissibility", max(0.0, min(1.0, float(out.get("continuity_conf", 0.0)) * (1.0 - float(out.get("fracture_pressure", 0.0))))))
        publish_signal(bus, "P1_Bend.directional_burden", out.get("last_d", 0.0))
        publish_signal(bus, "EC_Identity.switch_pressure", out.get("switch_pressure", 0.0))
        publish_signal(bus, "EC_Identity.trajectory_stability", out.get("trajectory_stability", 0.0))
        publish_signal(bus, "EC_Identity.incumbent_stability", out.get("incumbent_stability", 0.0))
        publish_signal(bus, "EC_Identity.best_margin", out.get("best_margin", 0.0))
        publish_signal(bus, "EC_Identity.estimate_drift", out.get("estimate_drift", 0.0))
        publish_signal(bus, "EC_Identity.recurrence", out.get("recurrence", 0.0))
        publish_signal(bus, "EC_Identity.adaptation_debt", out.get("adaptation_debt", 0.0))
        publish_signal(bus, "EC_Identity.adaptation_debt_instant", out.get("adaptation_debt_instant", 0.0))
        publish_signal(bus, "EC_Identity.adaptation_recovery", out.get("adaptation_recovery", 0.0))
        publish_signal(bus, "EC_Identity.fit_mismatch", out.get("fit_mismatch", 0.0))
        publish_signal(bus, "EC_Identity.fit_worsening", out.get("fit_worsening", 0.0))
        publish_signal(bus, "EC_Identity.commitment_hold", out.get("commitment_hold", 0.0))
        publish_signal(bus, "EC_Identity.rigidity_pressure", out.get("rigidity_pressure", 0.0))
        publish_signal(bus, "bend_triggers", float(out.get("bend_trigger", 0)))
        return out
