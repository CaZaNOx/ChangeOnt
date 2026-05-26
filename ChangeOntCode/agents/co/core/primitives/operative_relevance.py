from __future__ import annotations

from collections import deque
from agents.co.core.contracts.problem_contract import derive_goal_field
from dataclasses import asdict, dataclass
from typing import Any, Deque, Dict, Iterable, List, Optional, Tuple


def _clamp01(x: float) -> float:
    try:
        return max(0.0, min(1.0, float(x)))
    except Exception:
        return 0.0


@dataclass
class OperativeInvariant:
    name: str
    value: float
    anchor: float
    threat: float
    relevance: float
    scalarizable: float
    role: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class RegimeSignature:
    stability: float
    openness: float
    coherence: float
    burden_accumulation: float
    admissibility_decay: float
    invariant_stability: float
    history_dependence: float
    scalarizability: float
    thinness: float
    collapse_readiness: float
    representation_richness: float
    operative_difference: float
    mode: str
    collapse_reason: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class OperativeRelevanceController:
    """
    Runtime controller for operative relevance.

    This is the execution home of the doctrine family:
      operative difference -> operative invariant -> regime signature
      -> minimal adequate representation -> thin-collapse law.

    It never assumes hidden world access. It works only from the bounded local
    unfolding visible in packets/signals and keeps a small stateful ledger of
    anchors, burden accumulation, admissibility decay, and collapse readiness.
    """

    def __init__(self, history_len: int = 24, top_k: int = 4, anchor_alpha: float = 0.18) -> None:
        self.history_len = max(4, int(history_len))
        self.top_k = max(2, int(top_k))
        self.anchor_alpha = max(0.02, min(0.50, float(anchor_alpha)))
        self._anchors: Dict[str, float] = {}
        self._burden_hist: Deque[float] = deque(maxlen=self.history_len)
        self._adm_decay_hist: Deque[float] = deque(maxlen=self.history_len)
        self._history_dep_hist: Deque[float] = deque(maxlen=self.history_len)
        self._collapse_hist: Deque[float] = deque(maxlen=self.history_len)
        self._last: Dict[str, Any] = {}

    def _safe(self, src: Dict[str, Any], key: str, default: float = 0.0) -> float:
        try:
            return _clamp01(src.get(key, default))
        except Exception:
            return _clamp01(default)

    def _candidate_field(self, observation: Dict[str, Any]) -> Dict[str, float]:
        goal = derive_goal_field(observation) if isinstance(observation, dict) else {}
        mv = dict(observation.get('memory_view', {}) or {}) if isinstance(observation, dict) else {}
        signals = dict(observation.get('signals', {}) or {}) if isinstance(observation, dict) else {}
        candidates = list(observation.get('candidates', []) or []) if isinstance(observation, dict) else []
        legal = [c for c in candidates if isinstance(c, dict) and bool(c.get('legal', True))]
        top_goal = 0.0
        best_margin = _clamp01(goal.get('goal_sharpness', 0.0))
        avg_uncert = 0.0
        if legal:
            try:
                scores = sorted((_clamp01(float(c.get('goal_relation', 0.0) or 0.0)) for c in legal), reverse=True)
                top_goal = scores[0] if scores else 0.0
                best_margin = max(best_margin, (scores[0] - scores[1]) if len(scores) >= 2 else scores[0])
                avg_uncert = sum(_clamp01(float(c.get('uncertainty_hint', 0.0) or 0.0)) for c in legal) / float(len(legal))
            except Exception:
                top_goal = 0.0
                avg_uncert = 0.0
        miss_rate = _clamp01(mv.get('miss_rate', signals.get('miss_rate', 0.0)))
        pred_top = 0.0
        probs = dict(mv.get('ngram_proba', {}) or {})
        if probs:
            try:
                pred_top = _clamp01(max(float(v) for v in probs.values()))
            except Exception:
                pred_top = 0.0
        return {
            'goal_sharpness': _clamp01(goal.get('goal_sharpness', top_goal)),
            'goal_stability': _clamp01(goal.get('goal_stability', 0.5)),
            'goal_certainty': _clamp01(goal.get('goal_certainty', pred_top if pred_top > 0.0 else 0.5)),
            'best_margin': best_margin,
            'avg_uncertainty': avg_uncert,
            'miss_rate': miss_rate,
            'candidate_count': float(len(legal)),
        }

    def _feature_bundle(self, observation: Dict[str, Any], signals: Dict[str, float]) -> Dict[str, float]:
        obs_sig = self._candidate_field(observation)
        continuity = self._safe(signals, 'EC_Identity.continuity_conf', self._safe(signals, 'EC_Identity.same', 0.0))
        fracture = self._safe(signals, 'EC_Identity.fracture_pressure', 1.0 - continuity)
        admiss = self._safe(signals, 'Identity.admissibility', continuity * (1.0 - fracture))
        admissible_loss = self._safe(signals, 'EE_Compressibility.admissible_loss', 1.0 - admiss)
        closure = self._safe(signals, 'EE_Compressibility.closure_stability', 0.0)
        selective = self._safe(signals, 'EE_Compressibility.selective_retention', self._safe(signals, 'EE_Compressibility.score', 0.0))
        gauge = self._safe(signals, 'P2_Gauge.transport_coherence', 0.0)
        recurrence = self._safe(signals, 'EC_Identity.recurrence', 0.0)
        switch = self._safe(signals, 'EC_Identity.switch_pressure', 0.0)
        incumbent = self._safe(signals, 'EC_Identity.incumbent_stability', continuity)
        best_margin = max(obs_sig['best_margin'], self._safe(signals, 'EC_Identity.best_margin', 0.0))
        estimate_drift = self._safe(signals, 'EC_Identity.estimate_drift', 0.0)
        adaptation_debt = self._safe(signals, 'EC_Identity.adaptation_debt', 0.0)
        fit_mismatch = self._safe(signals, 'EC_Identity.fit_mismatch', 0.0)
        reeval = self._safe(signals, 'P16_RemainingBurden.reachability_deficit', 0.0)
        trans_burden = self._safe(signals, 'P16_RemainingBurden.transformation_burden', 0.0)
        field_update = dict(observation.get('field_update', {}) or {}) if isinstance(observation, dict) else {}
        field_frac = _clamp01(field_update.get('fracture_update', 0.0))
        field_cont = _clamp01(field_update.get('continuity_update', continuity))
        field_branch = _clamp01(field_update.get('branch_update', 0.0))

        burden_step = _clamp01(0.30 * trans_burden + 0.25 * adaptation_debt + 0.20 * fracture + 0.15 * fit_mismatch + 0.10 * field_frac)
        adm_decay_step = _clamp01(0.45 * (1.0 - admiss) + 0.20 * admissible_loss + 0.20 * max(0.0, field_frac - field_cont) + 0.15 * fracture)
        history_dep_step = _clamp01(
            0.35 * selective * (1.0 - obs_sig['goal_sharpness'])
            + 0.25 * recurrence * (1.0 - best_margin)
            + 0.20 * switch
            + 0.20 * field_branch
        )
        scalarizability = _clamp01(
            0.30 * obs_sig['goal_sharpness']
            + 0.20 * obs_sig['goal_stability']
            + 0.15 * obs_sig['goal_certainty']
            + 0.20 * best_margin
            + 0.15 * (1.0 - history_dep_step)
        )
        stability = _clamp01(0.35 * continuity + 0.25 * admiss + 0.20 * gauge + 0.20 * closure)
        openness = _clamp01(0.35 * burden_step + 0.20 * fracture + 0.20 * adm_decay_step + 0.15 * field_branch + 0.10 * reeval)
        coherence = _clamp01(0.45 * gauge + 0.30 * continuity + 0.25 * admiss)
        return {
            'continuity': continuity,
            'fracture': fracture,
            'admissibility': admiss,
            'admissible_loss': admissible_loss,
            'closure': closure,
            'selective_retention': selective,
            'gauge': gauge,
            'recurrence': recurrence,
            'switch': switch,
            'incumbent': incumbent,
            'best_margin': best_margin,
            'estimate_drift': estimate_drift,
            'adaptation_debt': adaptation_debt,
            'fit_mismatch': fit_mismatch,
            'field_frac': field_frac,
            'field_cont': field_cont,
            'field_branch': field_branch,
            'goal_sharpness': obs_sig['goal_sharpness'],
            'goal_stability': obs_sig['goal_stability'],
            'goal_certainty': obs_sig['goal_certainty'],
            'avg_uncertainty': obs_sig['avg_uncertainty'],
            'burden_step': burden_step,
            'admissibility_decay_step': adm_decay_step,
            'history_dependence_step': history_dep_step,
            'scalarizability': scalarizability,
            'stability': stability,
            'openness': openness,
            'coherence': coherence,
        }

    def _anchor(self, name: str, value: float) -> float:
        if name not in self._anchors:
            self._anchors[name] = float(value)
        return float(self._anchors[name])

    def _candidate_invariants(self, f: Dict[str, float]) -> List[OperativeInvariant]:
        cand: List[Tuple[str, float, float, float, str]] = [
            ('continuity_line', f['continuity'] * f['admissibility'], max(f['fracture'], f['burden_step']), f['goal_sharpness'], 'continuation'),
            ('admissible_core', f['admissibility'] * (1.0 - f['admissible_loss']), max(f['admissibility_decay_step'], f['fracture']), f['goal_sharpness'], 'admissibility'),
            ('gauge_lock', f['gauge'] * f['closure'], max(f['burden_step'], 1.0 - f['gauge']), 0.5 * f['goal_sharpness'] + 0.5 * f['best_margin'], 'coherence'),
            ('incumbent_ordering', f['incumbent'] * f['best_margin'] * (1.0 - f['estimate_drift']), max(f['adaptation_debt'], 1.0 - f['best_margin']), 0.65 * f['best_margin'] + 0.35 * f['goal_sharpness'], 'ordering'),
            ('motif_profile', f['selective_retention'] * (0.50 + 0.50 * f['recurrence']) * (1.0 - 0.50 * f['switch']), max(f['field_branch'], f['admissibility_decay_step']), 0.20 + 0.40 * (1.0 - f['history_dependence_step']), 'history'),
            ('goal_alignment', f['goal_sharpness'] * f['goal_stability'] * f['goal_certainty'], max(f['avg_uncertainty'], f['field_frac']), f['goal_sharpness'], 'goal'),
        ]
        out: List[OperativeInvariant] = []
        for name, value, threat, scalarizable, role in cand:
            value = _clamp01(value)
            threat = _clamp01(threat)
            scalarizable = _clamp01(scalarizable)
            anchor = self._anchor(name, value)
            drift = abs(value - anchor)
            relevance = _clamp01(value * (0.60 + 0.40 * max(threat, drift)))
            out.append(
                OperativeInvariant(
                    name=name,
                    value=value,
                    anchor=anchor,
                    threat=threat,
                    relevance=relevance,
                    scalarizable=scalarizable,
                    role=role,
                )
            )
        out.sort(key=lambda iv: (-iv.relevance, -iv.value, iv.name))
        return out[: self.top_k]

    def _operative_difference(self, invariants: List[OperativeInvariant]) -> float:
        if not invariants:
            return 0.0
        num = 0.0
        den = 0.0
        for iv in invariants:
            local = abs(float(iv.value) - float(iv.anchor)) + 0.50 * float(iv.threat)
            w = 0.25 + float(iv.relevance)
            num += w * local
            den += w
        return _clamp01(num / float(den or 1.0))

    def _commit_anchors(self, invariants: List[OperativeInvariant], signature: RegimeSignature) -> None:
        rate = self.anchor_alpha * max(0.10, signature.stability) * max(0.10, 1.0 - signature.burden_accumulation)
        for iv in invariants:
            prev = self._anchor(iv.name, iv.value)
            self._anchors[iv.name] = float((1.0 - rate) * prev + rate * iv.value)

    def _representation(self, signature: RegimeSignature, invariants: List[OperativeInvariant]) -> Dict[str, Any]:
        fields = ['goal_relation', 'continuity_support']
        if signature.mode != 'thin':
            fields.extend(['obstruction_hint', 'uncertainty_hint'])
        if signature.mode == 'rich':
            fields.extend(['novelty_hint', 'trace_relation', 'reversibility_hint'])
        weights = {
            'goal_relation': 0.55 if signature.mode == 'thin' else 0.35,
            'continuity_support': 0.25 if signature.mode == 'thin' else 0.20,
            'obstruction_hint': -0.20 if signature.mode == 'thin' else -0.15,
            'uncertainty_hint': 0.20 if signature.mode == 'thin' else 0.12,
            'novelty_hint': 0.04 if signature.mode == 'thin' else (0.12 if signature.mode == 'mixed' else 0.18),
            'trace_relation': 0.02 if signature.mode == 'thin' else (0.08 if signature.mode == 'mixed' else 0.14),
            'reversibility_hint': 0.04 if signature.mode == 'thin' else 0.08,
        }
        return {
            'mode': signature.mode,
            'richness': float(signature.representation_richness),
            'retained_fields': fields,
            'field_weights': weights,
            'top_invariants': [iv.name for iv in invariants],
        }

    def assess(self, observation: Optional[Dict[str, Any]], signals: Optional[Dict[str, float]] = None, advance: bool = False) -> Dict[str, Any]:
        obs = dict(observation or {})
        sig = {str(k): float(v) for k, v in dict(signals or {}).items() if isinstance(v, (int, float))}
        f = self._feature_bundle(obs, sig)

        burden_hist = list(self._burden_hist) + ([f['burden_step']] if advance else [])
        adm_hist = list(self._adm_decay_hist) + ([f['admissibility_decay_step']] if advance else [])
        hdep_hist = list(self._history_dep_hist) + ([f['history_dependence_step']] if advance else [])
        burden_acc = _clamp01(sum(burden_hist) / float(len(burden_hist) or 1))
        adm_decay = _clamp01(sum(adm_hist) / float(len(adm_hist) or 1))
        history_dep = _clamp01(sum(hdep_hist) / float(len(hdep_hist) or 1))

        invariants = self._candidate_invariants(f)
        invariant_stability = _clamp01(sum(iv.value for iv in invariants) / float(len(invariants) or 1))
        operative_difference = self._operative_difference(invariants)
        thinness = _clamp01(0.35 * f['stability'] + 0.25 * invariant_stability + 0.20 * f['scalarizability'] + 0.20 * (1.0 - f['openness']))
        collapse_readiness = _clamp01(
            0.35 * thinness + 0.25 * (1.0 - burden_acc) + 0.20 * (1.0 - adm_decay) + 0.10 * (1.0 - history_dep) + 0.10 * f['scalarizability']
        )
        representation_richness = _clamp01(0.45 * f['openness'] + 0.25 * burden_acc + 0.20 * history_dep + 0.10 * operative_difference)

        if collapse_readiness >= 0.70 and f['scalarizability'] >= 0.58 and history_dep <= 0.40:
            mode = 'thin'
            reason = 'stable sharp low-history regime'
        elif collapse_readiness >= 0.55:
            mode = 'mixed'
            reason = 'partially scalarizable regime'
        else:
            mode = 'rich'
            reason = 'history/burden keeps representation thick'

        signature = RegimeSignature(
            stability=float(f['stability']),
            openness=float(f['openness']),
            coherence=float(f['coherence']),
            burden_accumulation=float(burden_acc),
            admissibility_decay=float(adm_decay),
            invariant_stability=float(invariant_stability),
            history_dependence=float(history_dep),
            scalarizability=float(f['scalarizability']),
            thinness=float(thinness),
            collapse_readiness=float(collapse_readiness),
            representation_richness=float(representation_richness),
            operative_difference=float(operative_difference),
            mode=mode,
            collapse_reason=reason,
        )
        rep = self._representation(signature, invariants)
        out = {
            'operative_invariants': [iv.to_dict() for iv in invariants],
            'regime_signature': signature.to_dict(),
            'representation': rep,
            'operative_difference': float(operative_difference),
        }
        if advance:
            self._burden_hist.append(f['burden_step'])
            self._adm_decay_hist.append(f['admissibility_decay_step'])
            self._history_dep_hist.append(f['history_dependence_step'])
            self._collapse_hist.append(collapse_readiness)
            self._commit_anchors(invariants, signature)
            self._last = out
        return out

    def score_candidates(self, observation: Optional[Dict[str, Any]], signature: Optional[Dict[str, Any]] = None) -> Dict[Any, float]:
        """
        Non-canonical candidate scoring helper retained for legacy experiments.

        Evidence-bearing CO readout must use the documented CandidateSurface →
        RelationSurface → RCF → CollapseCertificate → CommitmentSurface path.
        This helper must not recover competence by branching on raw
        family-specific shortcut state such as bandit means/counts, and any use
        outside telemetry/investigatory contexts is paper-risky.
        """
        obs = dict(observation or {})
        sig = dict(signature or self._last.get('regime_signature', {}) or {})
        mode = str(sig.get('mode', 'mixed'))
        collapse = _clamp01(sig.get('collapse_readiness', 0.0))
        openness = _clamp01(sig.get('openness', 0.0))
        history_dep = _clamp01(sig.get('history_dependence', 0.0))
        burden = _clamp01(sig.get('burden_accumulation', 0.0))
        candidates = [c for c in list(obs.get('candidates', []) or []) if isinstance(c, dict) and bool(c.get('legal', True))]
        if not candidates:
            return {}
        weights = dict((self._last.get('representation') or {}).get('field_weights', {}))
        scores: Dict[Any, float] = {}
        exploit_pull = _clamp01(0.50 + 0.30 * collapse + 0.10 * (1.0 - history_dep))
        explore_pull = _clamp01(0.15 + 0.30 * (1.0 - collapse) + 0.15 * openness + 0.10 * burden)
        trace_pull = _clamp01(0.03 + 0.18 * history_dep + 0.06 * burden)
        reversibility_pull = _clamp01(0.05 + 0.18 * burden + 0.08 * openness)
        stale_pull = _clamp01(0.08 + 0.22 * history_dep + 0.18 * burden + 0.10 * openness)
        for c in candidates:
            a = c.get('candidate_id')
            if a is None:
                continue
            goal = _clamp01(c.get('goal_relation', 0.0))
            support = _clamp01(c.get('support_depth', 0.0))
            coverage = _clamp01(c.get('coverage_adequacy', support))
            cont = _clamp01(c.get('continuity_support', 0.0))
            cont = min(cont, _clamp01(0.25 + 0.75 * support))
            obst = _clamp01(c.get('obstruction_hint', 0.0))
            uncert = _clamp01(c.get('uncertainty_hint', 0.0))
            novelty = _clamp01(c.get('novelty_hint', 0.0))
            trace_rel = _clamp01(c.get('trace_relation', 0.0))
            rev = _clamp01(c.get('reversibility_hint', 0.0))
            # Continuity should help when it is still earning operative closure.
            # In burdened/history-thick regimes, continuity or trace that is not
            # improving the candidate toward closure should stop dominating.
            earned_cont = cont * _clamp01(0.30 + 0.35 * collapse + 0.35 * goal)
            earned_cont *= _clamp01(1.0 - 0.35 * history_dep - 0.30 * burden)
            stale_cont = cont * _clamp01(1.0 - goal) * stale_pull
            stale_trace = trace_rel * _clamp01(1.0 - goal) * stale_pull
            score = (
                weights.get('goal_relation', 0.35) * goal * exploit_pull
                + weights.get('continuity_support', 0.20) * earned_cont
                + 0.10 * support * exploit_pull
                + 0.05 * coverage * exploit_pull
                + weights.get('obstruction_hint', -0.15) * obst * (0.50 + 0.50 * burden)
                + weights.get('uncertainty_hint', 0.12) * uncert * explore_pull
                + weights.get('novelty_hint', 0.08) * novelty * (0.35 + 0.65 * (1.0 - collapse))
                + weights.get('trace_relation', 0.06) * trace_rel * trace_pull
                + weights.get('reversibility_hint', 0.06) * rev * reversibility_pull
                - 0.10 * stale_cont
                - 0.08 * stale_trace
            )
            if mode != 'thin':
                score += 0.04 * trace_rel * history_dep * goal
                score += 0.03 * novelty * openness
                score += 0.03 * rev * burden
            scores[a] = float(score)
        if scores:
            mx = max(scores.values())
            mn = min(scores.values())
            if mx > mn:
                scores = {k: (v - mn) / float(mx - mn) for k, v in scores.items()}
        return scores

    def report(self) -> Dict[str, Any]:
        return dict(self._last)
