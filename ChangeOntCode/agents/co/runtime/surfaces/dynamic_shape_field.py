"""Persistent dynamic shape/coarseness field.

Implements the first minimal runtime target described by
``103_DYNAMIC_SHAPE_FIELD_CONTRACT.md`` and the microcase expectations in
``104_DYNAMIC_SHAPE_UPDATE_MICROCASE_EXPECTATIONS.md``.

The field is deliberately conservative.  It records and updates a local shape
state from public retained trace only.  It does not choose an action, does not
read native action names, does not edit environment topology, and does not use
reward, DP values, baseline values, or hidden-state labels as update evidence.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Iterable, Mapping, Sequence

from agents.co.runtime.surfaces.continuation_field import BranchRelation, clamp01


RESOLVER_OPS = {"reduce", "relieve", "prevent", "reset", "cancel", "reveal", "expose", "buffer", "absorb"}
NONRESOLVER_REDIRECT_OPS = {"transform", "transfer"}


def _f(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return float(default)


def _avg(values: Iterable[Any], default: float = 0.0) -> float:
    vals = [_f(v, default) for v in values]
    if not vals:
        return float(default)
    return float(sum(vals) / len(vals))


def _ops(row: Mapping[str, Any]) -> Dict[str, int]:
    raw = row.get("branch_internal_operation_counts", {})
    if isinstance(raw, Mapping):
        out: Dict[str, int] = {}
        for k, v in raw.items():
            try:
                out[str(k).lower()] = int(v)
            except Exception:
                continue
        return out
    return {}


@dataclass
class DynamicShapeState:
    """Mutable local shape state.

    The original shape prior is intentionally not stored here as a mutable
    field.  Callers keep the base controls/shape prior separately and ask this
    state for a bounded *effective* control deformation.
    """

    coarseness_radius: float = 0.50
    projection_horizon: float = 0.50
    relation_density: float = 0.00
    burden_persistence: float = 0.00
    hiddenness_pressure: float = 0.00
    admissibility_pressure: float = 0.00
    gauge_confidence: float = 0.50
    # Domain-specific coarseness keeps the first-pass scalar coarseness as a
    # global fallback while allowing active public relation/burden domains to
    # retain different resolution.  Keys are generic public domains emitted by
    # RelationSurface/relation-field telemetry (for example ``burden:hiddenness``),
    # never native task or action names.
    coarseness_by_domain: Dict[str, float] = field(default_factory=dict)
    update_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DynamicShapeUpdateRecord:
    """Telemetry for one public-trace shape update."""

    applied: bool
    reason: str
    state_before: Dict[str, Any]
    public_evidence: Dict[str, Any]
    deltas: Dict[str, float]
    state_after: Dict[str, Any]
    skipped_fields: Sequence[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "applied": bool(self.applied),
            "reason": str(self.reason),
            "state_before": dict(self.state_before),
            "public_evidence": dict(self.public_evidence),
            "deltas": dict(self.deltas),
            "state_after": dict(self.state_after),
            "skipped_fields": list(self.skipped_fields),
        }


class DynamicShapeField:
    """Minimal persistent dynamic shape field.

    The update law is intentionally generic and bounded.  It consumes only
    candidate-row telemetry produced by CandidateSurface/RelationSurface/RCF/
    CollapseCertificate plus public observation/feedback annotations when
    present.  Reward values are logged as ignored evidence and never drive shape
    updates by themselves.
    """

    FORMULA_STATUS = "first_pass_contract_implementation"

    def __init__(self, alpha: float = 0.35, initial_state: Mapping[str, Any] | None = None) -> None:
        self.alpha = max(0.0, min(1.0, float(alpha)))
        self.state = DynamicShapeState()
        if initial_state:
            for k, v in initial_state.items():
                key = str(k)
                if key == "coarseness_by_domain" and isinstance(v, Mapping):
                    self.state.coarseness_by_domain = {
                        self._sanitize_domain_name(d): clamp01(val, self.state.coarseness_radius)
                        for d, val in v.items()
                        if self._sanitize_domain_name(d)
                    }
                    continue
                if hasattr(self.state, key) and key != "update_count":
                    setattr(self.state, key, clamp01(v, getattr(self.state, key)))
        self.last_update: Dict[str, Any] = {
            "applied": False,
            "reason": "not_updated_yet",
            "state_before": self.state.to_dict(),
            "public_evidence": {},
            "deltas": {},
            "state_after": self.state.to_dict(),
            "skipped_fields": [],
        }

    def state_dict(self) -> Dict[str, Any]:
        return self.state.to_dict()

    def _blend(self, old: float, target: float, *, rate: float | None = None) -> float:
        r = self.alpha if rate is None else max(0.0, min(1.0, float(rate)))
        return clamp01((1.0 - r) * float(old) + r * float(target))

    @staticmethod
    def _sanitize_domain_name(value: Any) -> str:
        text = str(value or "").strip().lower()
        # Keep only generic public domain labels.  The caller should pass domains
        # derived from burden/relation facts, not native task/action names.
        if not text or text in {"unknown", "none"}:
            return ""
        return text[:80]

    @classmethod
    def _row_domain(cls, row: Mapping[str, Any]) -> str:
        domain = cls._sanitize_domain_name(row.get("relation_field_domain", ""))
        if domain:
            return domain
        burden_types = row.get("branch_internal_burden_types", [])
        if isinstance(burden_types, Sequence) and not isinstance(burden_types, (str, bytes)) and burden_types:
            return cls._sanitize_domain_name(f"burden:{sorted(str(v).lower() for v in burden_types if str(v).strip())[0]}")
        return ""

    @classmethod
    def _domain_targets(cls, rows: Sequence[Mapping[str, Any]], global_target: float) -> Dict[str, float]:
        buckets: Dict[str, list[Mapping[str, Any]]] = {}
        for row in rows:
            domain = cls._row_domain(row)
            if domain:
                buckets.setdefault(domain, []).append(row)
        targets: Dict[str, float] = {}
        for domain, ds in buckets.items():
            ambiguity = max(
                _avg((r.get("relation_field_domain_ambiguity", 0.0) for r in ds), 0.0),
                _avg((r.get("relation_field_ambiguity", 0.0) for r in ds), 0.0) * 0.35,
            )
            concentration = _avg((r.get("relation_field_concentration", 0.0) for r in ds), 0.0)
            debt = max(
                _avg((r.get("field_debt", 0.0) for r in ds), 0.0),
                _avg((r.get("branch_internal_unresolved_pressure", 0.0) for r in ds), 0.0),
            )
            hidden = max(
                _avg((r.get("branch_internal_hiddenness_pressure", 0.0) for r in ds), 0.0),
                _avg((r.get("uncertainty", 0.0) for r in ds), 0.0) * 0.55,
            )
            resolver = max(
                _avg((r.get("branch_internal_resolver_support", 0.0) for r in ds), 0.0),
                _avg((r.get("field_relief_support", 0.0) for r in ds), 0.0),
            )
            function_like = _avg((1.0 if r.get("relation_field_function_like", False) else 0.0 for r in ds), 0.0)
            # Ambiguity/debt/hiddenness demand finer resolution.  Strong
            # function-like concentration and resolver/exposure support permit
            # coarser collapse.  Blend with the global target so sparse domains
            # cannot swing to extreme values from one row.
            raw = clamp01(
                0.45 * global_target
                + 0.23 * (1.0 - ambiguity)
                + 0.16 * function_like
                + 0.10 * resolver
                - 0.18 * debt
                - 0.13 * hidden
                - 0.11 * ambiguity
                + 0.06 * concentration
            )
            targets[domain] = raw
        return targets

    def domain_coarseness_for(self, domain: Any) -> float:
        key = self._sanitize_domain_name(domain)
        if not key:
            return clamp01(self.state.coarseness_radius)
        return clamp01(self.state.coarseness_by_domain.get(key, self.state.coarseness_radius), self.state.coarseness_radius)

    @staticmethod
    def _relation_density(rows: Sequence[Mapping[str, Any]], relations: Sequence[Any]) -> float:
        n = max(1, len(rows))
        explicit = float(len(relations)) / float(max(1, n * max(1, n - 1)))
        row_density = _avg((r.get("field_relation_count", r.get("relation_surface_relation_count", 0.0)) for r in rows), 0.0) / max(1.0, float(max(1, n - 1)))
        return clamp01(0.55 * explicit + 0.45 * row_density)

    @staticmethod
    def _public_admissibility_signal(observation: Mapping[str, Any] | None, feedback: Mapping[str, Any] | None) -> tuple[float, bool]:
        """Return public admissibility narrowing/widening pressure.

        The field accepts only explicit public annotations or legal candidate
        counts.  It does not infer environment topology beyond what is visible.
        """
        obs = observation or {}
        fb = feedback or {}
        candidates = [c for c in list(obs.get("candidates") or []) if isinstance(c, Mapping)]
        if candidates:
            legal = sum(1 for c in candidates if bool(c.get("legal", True)))
            total = len(candidates)
            if total > 0 and legal < total:
                return clamp01(1.0 - (float(legal) / float(total))), True
        for src in (fb, obs):
            for key in ("admissibility_pressure", "known_admissibility_pressure", "admissibility_delta", "public_admissibility_delta"):
                if key in src:
                    return clamp01(abs(_f(src.get(key), 0.0))), True
            if src.get("blocked_transition_discovered") is True or src.get("public_blocked_transition") is True:
                return 0.85, True
        return 0.0, False

    @staticmethod
    def _public_exposure_signal(rows: Sequence[Mapping[str, Any]], observation: Mapping[str, Any] | None, feedback: Mapping[str, Any] | None) -> tuple[float, float, bool]:
        obs = observation or {}
        fb = feedback or {}
        exposure_support = max(_avg((r.get("branch_internal_exposure_support", 0.0) for r in rows), 0.0), _avg((r.get("branch_internal_resolver_support", 0.0) for r in rows), 0.0) * 0.55)
        hiddenness = max(_avg((r.get("branch_internal_hiddenness_pressure", 0.0) for r in rows), 0.0), _avg((r.get("uncertainty", 0.0) for r in rows), 0.0) * 0.55)
        explicit_success = bool(obs.get("public_exposure_success") or fb.get("public_exposure_success") or obs.get("cue_reliability_improved") or fb.get("cue_reliability_improved"))
        explicit_failed = bool(obs.get("public_exposure_failed") or fb.get("public_exposure_failed") or obs.get("exposure_inconclusive") or fb.get("exposure_inconclusive"))
        if explicit_success:
            return clamp01(exposure_support + 0.35), hiddenness, True
        if explicit_failed:
            return 0.0, clamp01(hiddenness + 0.25), True
        return clamp01(exposure_support), clamp01(hiddenness), exposure_support > 0.0 or hiddenness > 0.0

    @staticmethod
    def _reward_only(observation: Mapping[str, Any] | None, feedback: Mapping[str, Any] | None, evidence: Mapping[str, Any]) -> bool:
        obs = observation or {}
        fb = feedback or {}
        has_reward = any(k in obs for k in ("reward", "outcome_reward", "score")) or any(k in fb for k in ("reward", "outcome_reward", "score"))
        if not has_reward:
            return False
        substantive = (
            _f(evidence.get("avg_field_debt", 0.0)) > 1e-9
            or _f(evidence.get("relation_density_observed", 0.0)) > 1e-9
            or _f(evidence.get("avg_hiddenness_pressure", 0.0)) > 1e-9
            or _f(evidence.get("admissibility_pressure_observed", 0.0)) > 1e-9
            or _f(evidence.get("resolver_support_observed", 0.0)) > 1e-9
            or _f(evidence.get("transform_redirect_observed", 0.0)) > 1e-9
        )
        return not substantive

    def update(
        self,
        *,
        rows: Sequence[Mapping[str, Any]],
        relations: Sequence[BranchRelation | Mapping[str, Any]] | None = None,
        observation: Mapping[str, Any] | None = None,
        feedback: Mapping[str, Any] | None = None,
    ) -> Dict[str, Any]:
        """Update local shape state from public retained trace.

        Returns a telemetry record with before/evidence/delta/after.  If no
        public shape evidence is present, the update fails closed and leaves the
        state unchanged.
        """
        before = self.state.to_dict()
        rows_list = [dict(r) for r in rows if isinstance(r, Mapping)]
        rels = list(relations or [])
        if not rows_list:
            rec = DynamicShapeUpdateRecord(False, "no_public_rows", before, {}, {}, before, ("all",)).to_dict()
            self.last_update = rec
            return rec

        op_counts: Dict[str, int] = {}
        for r in rows_list:
            for k, v in _ops(r).items():
                op_counts[k] = op_counts.get(k, 0) + int(v)
        resolver_ops = sum(op_counts.get(k, 0) for k in RESOLVER_OPS)
        redirect_ops = sum(op_counts.get(k, 0) for k in NONRESOLVER_REDIRECT_OPS)
        carry_ops = sum(op_counts.get(k, 0) for k in ("carry", "increase", "amplify", "mask", "postpone", "threshold", "phase_shift"))

        relation_density_observed = self._relation_density(rows_list, rels)
        avg_field_debt = max(
            _avg((r.get("field_debt", 0.0) for r in rows_list), 0.0),
            _avg((r.get("branch_internal_unresolved_pressure", 0.0) for r in rows_list), 0.0),
        )
        avg_grey = max(
            _avg((r.get("field_grey_pressure", 0.0) for r in rows_list), 0.0),
            _avg((r.get("collapse_certificate_blocker_pressure", 0.0) for r in rows_list), 0.0) * 0.55,
        )
        avg_recursion = max(
            _avg((r.get("field_recursion_budget", 0.0) for r in rows_list), 0.0),
            _avg((r.get("collapse_certificate_recursion_demand", 0.0) for r in rows_list), 0.0),
        )
        avg_burden_trend = _avg((r.get("burden_trend", 0.0) for r in rows_list), 0.0)
        relation_field_ambiguity = max(
            _avg((r.get("relation_field_domain_ambiguity", 0.0) for r in rows_list), 0.0),
            _avg((r.get("relation_field_ambiguity", 0.0) for r in rows_list), 0.0) * 0.35,
        )
        relation_field_concentration = _avg((r.get("relation_field_concentration", 0.0) for r in rows_list), 0.0)
        relation_field_function_like_ratio = _avg((1.0 if r.get("relation_field_function_like", False) else 0.0 for r in rows_list), 0.0)
        resolver_support_observed = max(
            _avg((r.get("branch_internal_resolver_support", 0.0) for r in rows_list), 0.0),
            _avg((r.get("field_relief_support", 0.0) for r in rows_list), 0.0),
        )
        exposure_support, hiddenness_observed, exposure_evidence = self._public_exposure_signal(rows_list, observation, feedback)
        admissibility_observed, admissibility_evidence = self._public_admissibility_signal(observation, feedback)
        transform_redirect_observed = clamp01(float(redirect_ops) / float(max(1, len(rows_list))))
        carry_pressure_observed = clamp01(float(carry_ops) / float(max(1, len(rows_list))))

        high_coupling = clamp01(0.32 * relation_density_observed + 0.24 * avg_field_debt + 0.16 * avg_grey + 0.11 * avg_recursion + 0.08 * admissibility_observed + 0.09 * relation_field_ambiguity)
        stable_low_coupling = clamp01((1.0 - high_coupling) * (1.0 - hiddenness_observed) * (1.0 - avg_field_debt) * (0.55 + 0.45 * self.state.gauge_confidence))
        burden_persistence_target = clamp01(0.38 * avg_field_debt + 0.20 * avg_burden_trend + 0.15 * carry_pressure_observed + 0.11 * avg_grey + 0.08 * transform_redirect_observed + 0.08 * relation_field_ambiguity)
        hiddenness_target = clamp01(0.58 * hiddenness_observed + 0.22 * avg_grey + 0.12 * relation_field_ambiguity + 0.08 * (1.0 - exposure_support if hiddenness_observed > 0.0 else 0.0))
        if exposure_support > 0.0 and exposure_support >= hiddenness_observed:
            hiddenness_target = clamp01(hiddenness_target * (1.0 - 0.45 * exposure_support))
        admissibility_target = clamp01(0.62 * admissibility_observed + 0.23 * avg_recursion + 0.15 * avg_field_debt)
        relation_density_target = relation_density_observed
        projection_target = clamp01(0.66 - 0.58 * high_coupling - 0.38 * burden_persistence_target - 0.20 * hiddenness_target - 0.15 * admissibility_target)
        coarseness_target = clamp01(0.52 * stable_low_coupling + 0.28 * self.state.coarseness_radius + 0.20 * (1.0 - relation_density_observed))
        if high_coupling > 0.45 or hiddenness_target > 0.45:
            coarseness_target = clamp01(coarseness_target * (1.0 - 0.35 * max(high_coupling, hiddenness_target)))
        gauge_conf_target = clamp01(
            0.38 * self.state.gauge_confidence
            + 0.20 * (1.0 - hiddenness_target)
            + 0.17 * (1.0 - admissibility_target)
            + 0.10 * (1.0 - relation_density_target)
            + 0.08 * exposure_support
            + 0.09 * relation_field_function_like_ratio
            - 0.09 * transform_redirect_observed
            - 0.08 * relation_field_ambiguity
        )

        evidence = {
            "candidate_rows": len(rows_list),
            "relations_total": len(rels),
            "operation_counts": dict(op_counts),
            "resolver_ops_count": int(resolver_ops),
            "transform_transfer_ops_count": int(redirect_ops),
            "carry_ops_count": int(carry_ops),
            "relation_density_observed": relation_density_observed,
            "avg_field_debt": avg_field_debt,
            "avg_grey_pressure": avg_grey,
            "avg_recursion_demand": avg_recursion,
            "avg_burden_trend": avg_burden_trend,
            "relation_field_ambiguity_observed": relation_field_ambiguity,
            "relation_field_concentration_observed": relation_field_concentration,
            "relation_field_function_like_ratio": relation_field_function_like_ratio,
            "resolver_support_observed": resolver_support_observed,
            "exposure_support_observed": exposure_support,
            "avg_hiddenness_pressure": hiddenness_observed,
            "admissibility_pressure_observed": admissibility_observed,
            "admissibility_evidence_present": bool(admissibility_evidence),
            "exposure_evidence_present": bool(exposure_evidence),
            "transform_redirect_observed": transform_redirect_observed,
            "reward_seen_but_ignored": bool(any(k in (observation or {}) for k in ("reward", "outcome_reward", "score")) or any(k in (feedback or {}) for k in ("reward", "outcome_reward", "score"))),
        }

        public_shape_signal = any(
            _f(evidence.get(k, 0.0)) > 1e-9
            for k in (
                "relation_density_observed",
                "avg_field_debt",
                "avg_grey_pressure",
                "avg_recursion_demand",
                "resolver_support_observed",
                "exposure_support_observed",
                "avg_hiddenness_pressure",
                "admissibility_pressure_observed",
                "relation_field_ambiguity_observed",
                "relation_field_concentration_observed",
                "transform_redirect_observed",
            )
        )
        if self._reward_only(observation, feedback, evidence):
            rec = DynamicShapeUpdateRecord(False, "reward_only_no_shape_update", before, evidence, {}, before, ("all",)).to_dict()
            self.last_update = rec
            return rec
        if not public_shape_signal:
            rec = DynamicShapeUpdateRecord(False, "no_public_shape_signal", before, evidence, {}, before, ("all",)).to_dict()
            self.last_update = rec
            return rec

        domain_targets = self._domain_targets(rows_list, coarseness_target)
        old_domain_coarseness = dict(self.state.coarseness_by_domain)
        after_values = {
            "relation_density": self._blend(self.state.relation_density, relation_density_target),
            "burden_persistence": self._blend(self.state.burden_persistence, burden_persistence_target),
            "hiddenness_pressure": self._blend(self.state.hiddenness_pressure, hiddenness_target),
            "admissibility_pressure": self._blend(self.state.admissibility_pressure, admissibility_target),
            "projection_horizon": self._blend(self.state.projection_horizon, projection_target),
            "coarseness_radius": self._blend(self.state.coarseness_radius, coarseness_target),
            "gauge_confidence": self._blend(self.state.gauge_confidence, gauge_conf_target),
        }
        deltas: Dict[str, float] = {}
        for k, v in after_values.items():
            old = _f(getattr(self.state, k), 0.0)
            new = clamp01(v)
            setattr(self.state, k, new)
            deltas[k] = float(new - old)
        if domain_targets:
            updated_domains: Dict[str, float] = {}
            for domain, target in domain_targets.items():
                old = self.domain_coarseness_for(domain)
                updated_domains[domain] = self._blend(old, target, rate=min(0.28, self.alpha))
            # Preserve only active or recently observed domains.  This avoids
            # accumulating arbitrary dimension names while still keeping a
            # bounded anisotropic coarseness profile.
            self.state.coarseness_by_domain = dict(sorted(updated_domains.items()))
            domain_deltas = {
                d: float(self.state.coarseness_by_domain[d] - old_domain_coarseness.get(d, self.state.coarseness_radius))
                for d in self.state.coarseness_by_domain
            }
            deltas["coarseness_by_domain_max_abs_delta"] = max((abs(v) for v in domain_deltas.values()), default=0.0)
            evidence["coarseness_by_domain_targets"] = dict(sorted(domain_targets.items()))
            evidence["coarseness_by_domain_deltas"] = domain_deltas
            evidence["coarseness_domain_count"] = len(self.state.coarseness_by_domain)
        else:
            self.state.coarseness_by_domain = {}
            evidence["coarseness_domain_count"] = 0
        self.state.update_count += 1
        after = self.state.to_dict()
        rec = DynamicShapeUpdateRecord(True, "public_trace_shape_update", before, evidence, deltas, after, ()).to_dict()
        self.last_update = rec
        return rec

    def effective_controls(self, controls: Mapping[str, Any]) -> Dict[str, float]:
        """Return next-cycle controls deformed by current shape-state.

        The deformation is bounded and generic.  It does not add/remove actions
        and cannot choose a native action; downstream surfaces still apply their
        own relation/certificate/readout logic.
        """
        c = {str(k): clamp01(v, 0.5) for k, v in dict(controls or {}).items()}
        s = self.state
        urgency = clamp01(0.34 * s.burden_persistence + 0.24 * s.hiddenness_pressure + 0.20 * s.admissibility_pressure + 0.14 * s.relation_density + 0.08 * (1.0 - s.projection_horizon))
        confidence = clamp01(s.gauge_confidence)
        domain_values = list((s.coarseness_by_domain or {}).values())
        domain_avg = clamp01(sum(domain_values) / len(domain_values), s.coarseness_radius) if domain_values else clamp01(s.coarseness_radius)
        domain_min = clamp01(min(domain_values), s.coarseness_radius) if domain_values else clamp01(s.coarseness_radius)
        # The global coarsening pressure remains scalar for existing readout
        # consumers, but it is now informed by the anisotropic coarseness field.
        coarsening = clamp01((0.62 * s.coarseness_radius + 0.38 * domain_avg) * confidence * (1.0 - max(s.relation_density, s.hiddenness_pressure)))

        def setc(name: str, value: float) -> None:
            c[name] = clamp01(value)

        setc("path_sensitivity", c.get("path_sensitivity", 0.5) + 0.20 * urgency - 0.06 * coarsening)
        setc("nonlocal_authority", c.get("nonlocal_authority", 0.5) + 0.18 * urgency + 0.08 * s.relation_density - 0.08 * confidence)
        setc("revision_permissibility", c.get("revision_permissibility", 0.5) + 0.16 * urgency - 0.05 * coarsening)
        setc("rival_breadth", c.get("rival_breadth", 0.5) + 0.16 * s.relation_density + 0.08 * s.hiddenness_pressure - 0.05 * coarsening)
        setc("collapse_admissibility", c.get("collapse_admissibility", c.get("collapse_permission", 0.5)) - 0.18 * urgency + 0.10 * coarsening + 0.06 * confidence)
        setc("collapse_permission", c.get("collapse_permission", c.get("collapse_admissibility", 0.5)) - 0.16 * urgency + 0.10 * coarsening + 0.05 * confidence)
        setc("local_authority", c.get("local_authority", 0.5) - 0.14 * urgency + 0.14 * coarsening + 0.06 * confidence)
        setc("support_carry_forward", c.get("support_carry_forward", 0.5) - 0.12 * s.burden_persistence + 0.12 * coarsening)
        setc("contradiction_sensitivity", c.get("contradiction_sensitivity", 0.5) + 0.18 * urgency + 0.08 * s.admissibility_pressure)
        setc("low_evidence_sampling", c.get("low_evidence_sampling", 0.5) + 0.16 * s.hiddenness_pressure + 0.08 * (1.0 - s.gauge_confidence))
        c["dynamic_shape_urgency"] = urgency
        c["dynamic_shape_coarsening"] = coarsening
        c["dynamic_shape_projection_horizon"] = clamp01(s.projection_horizon)
        c["dynamic_shape_gauge_confidence"] = confidence
        c["dynamic_shape_domain_coarseness_avg"] = domain_avg
        c["dynamic_shape_domain_coarseness_min"] = domain_min
        c["dynamic_shape_domain_coarseness_count"] = float(len(domain_values))
        return c
