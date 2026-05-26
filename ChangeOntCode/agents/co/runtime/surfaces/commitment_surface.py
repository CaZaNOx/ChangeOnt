"""Canonical final readout surface.

Implements ``43_CANONICAL_COMMITMENT_RULE.md`` and
``42_CANONICAL_READOUT_AND_ACTION_SELECTION_RULE.md``.  CommitmentSurface emits
the native action only after consuming CO candidate rows, field/certificate
telemetry, and direct controls.  It must respect certificate gates and fail
closed instead of rescuing missing evidence with a non-CO selection path.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple
from collections import defaultdict
import random
from agents.co.runtime.support.scope_keys import resolve_decision_scope
from agents.co.runtime.surfaces.fusion_support import candidate_evidence_scores

try:
    from agents.co.core.combinators.C_fuse import C_Fuse
except Exception:
    class C_Fuse:  # type: ignore
        def __init__(self, method: str = "add", tau: float = 1.0):
            self.method = method; self.tau = tau
        def fuse(self, scores_list):
            out: Dict[Any, float] = {}
            for item in scores_list:
                if isinstance(item, tuple) and len(item) == 2:
                    d, w = item
                    for k, v in d.items():
                        out[k] = out.get(k, 0.0) + float(v) * float(w)
                else:
                    for k, v in item.items():
                        out[k] = out.get(k, 0.0) + float(v)
            return out

try:
    from agents.co.core.contracts.signals import normalize_scores
except Exception:
    def normalize_scores(scores: Dict[Any, float]) -> Dict[Any, float]:
        if not scores:
            return {}
        m = max(abs(float(v)) for v in scores.values())
        if m <= 1e-12:
            return dict(scores)
        return {k: float(v) / m for k, v in scores.items()}

class CommitmentSurface:
    """Final CO readout surface that converts certificate-aware candidate state into a native action."""
    PRIMITIVE_DEPS = ("signal_bus (optional)",)
    COMBINATOR_DEPS = ()
    FORMULA_STATUS = "working"

    def __init__(
        self,
        seed: int = 0,
        fuse_method: str = "add",
        fuse_tau: float = 1.0,
        prefer_bus_if_present: bool = True,
        co_weight_override: Optional[float] = None,
        commitment_formula_params: Optional[Dict[str, float]] = None,
        **compat_aliases: Any,
    ) -> None:
        self.rng = random.Random(int(seed))
        # Backward-compatible constructor aliases are accepted only so old
        # configs can instantiate the canonical surface.  They are not readout
        # policy knobs and do not enable a non-canonical candidate-scoring path.
        self.compat_param_aliases_ignored = dict(compat_aliases or {})
        self._fuser = C_Fuse(method=fuse_method, tau=fuse_tau)
        self.prefer_bus = bool(prefer_bus_if_present)
        self.co_weight_override = co_weight_override
        self.commitment_formula_params = dict(commitment_formula_params or {})
        self.no_fallback_path = True

    def _formula_param(self, name: str, default: float) -> float:
        """Return a diagnostic formula parameter override or the certified default.

        Runtime configs normally use the defaults documented in the formula
        ledger.  Structural sensitivity studies may supply explicit overrides to
        test whether a coefficient is stable, brittle, or over-authoritative.
        Overrides are not performance-tuning evidence.
        """
        try:
            return float(self.commitment_formula_params.get(name, default))
        except Exception:
            return float(default)

    def _decision_scope(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any) -> str:
        return resolve_decision_scope(observation, primitives, header)

    def _bus_scores(self, primitives: Dict[str, Any], observation: Dict[str, Any]) -> tuple[Dict[Any, float], int]:
        """Drain scoped candidate votes from the signal bus without creating uniform rescue votes."""
        bus = primitives.get("signal_bus", None)
        if bus is None or not hasattr(bus, "drain"):
            return {}, 0
        scope_key = self._decision_scope(observation, primitives, None)
        try:
            votes = bus.drain(scope_key=scope_key)
        except TypeError:
            votes = bus.drain(scope_key)
        except Exception:
            votes = []
        agg_by_scope: Dict[str, Dict[Any, float]] = defaultdict(lambda: defaultdict(float))
        for v in votes:
            a = v.get("action", None)
            w = float(v.get("weight", 0.0) or 0.0)
            scope = str(v.get("scope") or "base")
            if a is not None and w > 0.0:
                agg_by_scope[scope][a] += w
        if set(agg_by_scope.keys()) <= {"base"}:
            return dict(agg_by_scope.get("base", {})), len(votes)
        return {"__scoped__": {s: dict(d) for s, d in agg_by_scope.items()}}, len(votes)

    def _typed_fuse_scoped(self, scoped: Dict[str, Dict[Any, float]], signals: Dict[str, float]) -> Dict[Any, float]:
        base = scoped.get("base", {})
        sal = scoped.get("salience", {})
        pers = scoped.get("persistence", {})
        fract = scoped.get("fracture", {})

        def _bounded(d: Dict[Any, float]) -> Dict[Any, float]:
            """Return 0..1 support magnitudes without erasing absolute weakness.

            CandidateEvidenceSurface already publishes bounded state magnitudes.
            Re-normalizing every scope to max=1 made weak salience/fracture
            channels as strong as genuine base support and caused probe actions to
            override well-supported local commitments.  Only scale if an upstream
            publisher emits values above 1.0.
            """
            if not d:
                return {}
            vals = [abs(float(v)) for v in d.values()]
            denom = max(1.0, max(vals) if vals else 1.0)
            return {k: max(0.0, min(1.0, float(v) / denom)) for k, v in d.items()}

        bN, sN, pN, fN = map(_bounded, (base, sal, pers, fract))
        g_fract = float(signals.get("EC_Identity.fracture_pressure", 0.0) or 0.0)
        g_cont = float(signals.get("EC_Identity.continuity_conf", signals.get("EC_Identity.same", 0.0)) or 0.0)
        g_debt = float(signals.get("EC_Identity.adaptation_debt", 0.0) or 0.0)
        out: Dict[Any, float] = {}
        domain = set(bN.keys()) | set(sN.keys()) | set(pN.keys()) | set(fN.keys())
        for a in domain:
            base_mass = float(bN.get(a, 0.0))
            salience = float(sN.get(a, 0.0))
            persistence = float(pN.get(a, 0.0))
            fracture = float(fN.get(a, 0.0))
            persist_gate = max(0.0, min(1.0, g_cont)) * max(0.0, 1.0 - max(0.0, min(1.0, g_debt)))
            fracture_gate = max(max(0.0, min(1.0, g_fract)), 0.75 * max(0.0, min(1.0, g_debt)))
            support = base_mass * (1.0 + 0.55 * persistence * persist_gate)
            # Probe/salience may reopen weakly supported choices, but should not
            # dominate a candidate that already has materially stronger base
            # support.  This is generic readout discipline, not a maintenance
            # threshold rule.
            explore_gate = max(0.0, 1.0 - persist_gate) * (0.35 + 0.65 * max(0.0, 1.0 - base_mass))
            explore = 0.10 * salience * explore_gate
            burden = 0.45 * fracture * fracture_gate
            out[a] = float(max(0.0, support + explore - burden))
        return out

    def _signal_snapshot(self, primitives: Dict[str, Any]) -> Dict[str, float]:
        bus = primitives.get("signal_bus", None)
        if bus is None:
            return {}
        if hasattr(bus, "signals"):
            try:
                return dict(bus.signals())
            except Exception:
                return {}
        if isinstance(bus, dict):
            try:
                return {k: float(v) for k, v in bus.items() if isinstance(v, (int, float))}
            except Exception:
                return {}
        return {}

    def _operative_assessment(self, observation: Dict[str, Any], primitives: Dict[str, Any], signals: Dict[str, float]) -> Dict[str, Any]:
        controller = primitives.get("operative_relevance") if isinstance(primitives, dict) else None
        if controller is None or not hasattr(controller, "assess"):
            return {}
        try:
            return dict(controller.assess(observation, signals, advance=False) or {})
        except Exception:
            return {}


    def _attach_telemetry(self, out: Dict[str, Any], primitives: Dict[str, Any], header: Any, translator_mask: set, actions: list) -> Dict[str, Any]:
        signals = self._signal_snapshot(primitives)
        out.setdefault("signals", dict(signals))
        meta = primitives.get("_meta_header")
        if meta is not None:
            try:
                out.setdefault("meta_header", meta.to_dict())
            except Exception:
                try:
                    out.setdefault("meta_header", dict(meta))
                except Exception:
                    out.setdefault("meta_header", {})
        out.setdefault("translator_mask", sorted(list(translator_mask)))
        out.setdefault("mask_mode", "blocklist")
        ass = primitives.get("_operative_relevance_assessment", {}) if isinstance(primitives, dict) else {}
        if isinstance(ass, dict) and ass:
            rs = ass.get("regime_signature", {}) if isinstance(ass.get("regime_signature", {}), dict) else {}
            out.setdefault("regime_signature", dict(rs))
            out.setdefault("representation", dict(ass.get("representation", {}) or {}))
            out.setdefault("operative_invariants", list(ass.get("operative_invariants", []) or []))
            out.setdefault("collapse_readiness", float(rs.get("collapse_readiness", 0.0)))
            out.setdefault("representation_mode", str(rs.get("mode", "mixed")))
        out.setdefault("no_fallback_path", True)
        return out

    def _fuse_safe(self, parts: List[Any]) -> Dict[Any, float]:
        """Fuse CO score parts; this is arithmetic fallback for fuser failure, not action-policy fallback."""
        try:
            return self._fuser.fuse(parts)
        except Exception:
            out: Dict[Any, float] = {}
            for item in parts:
                if isinstance(item, tuple) and len(item) == 2:
                    d, w = item
                    for k, v in d.items():
                        out[k] = out.get(k, 0.0) + float(v) * float(w)
                elif isinstance(item, dict):
                    for k, v in item.items():
                        out[k] = out.get(k, 0.0) + float(v)
            return out

    def run_update(self, elements: list, primitives: dict, header: Any, observation: dict, feedback: dict | None) -> dict:
        """CommitmentSurface is not a pipeline orchestrator.

        The certified runtime owns update sequencing in C_Pipeline.  This method
        is retained only to fail closed if an old caller treats the readout
        surface as an orchestration layer.
        """
        raise RuntimeError(
            "CommitmentSurface.run_update is not part of the canonical runtime; "
            "use C_Pipeline.run_update and keep CommitmentSurface as final readout only."
        )


    def _clamp01(self, x: Any, default: float = 0.0) -> float:
        try:
            v = float(x)
        except Exception:
            v = float(default)
        if v < 0.0:
            return 0.0
        if v > 1.0:
            return 1.0
        return v

    def _candidate_rows(self, observation: Dict[str, Any], primitives: Dict[str, Any], translator_mask: set) -> List[Dict[str, Any]]:
        """Read evidence-bearing candidate rows while excluding masked or inadmissible actions."""
        rows = []
        if isinstance(primitives, dict) and isinstance(primitives.get("__candidate_publication_rows__"), list):
            rows = [dict(r) for r in primitives.get("__candidate_publication_rows__", []) if isinstance(r, dict)]
        elif isinstance(observation, dict) and isinstance(observation.get("candidate_publication_rows"), list):
            rows = [dict(r) for r in observation.get("candidate_publication_rows", []) if isinstance(r, dict)]
        out: List[Dict[str, Any]] = []
        for row in rows:
            a = row.get("action")
            if a is None or a in translator_mask:
                continue
            if row.get("admissible", True) is False or row.get("legal", True) is False:
                continue
            out.append(row)
        return out

    def _direct_control_snapshot(
        self,
        header: Any,
        observation: Optional[Dict[str, Any]] = None,
        primitives: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, float]:
        """Read generic shape/direct controls for the current commitment step.

        The certified public shape path is still the six-question problem shape
        prior projected into direct controls.  This helper also exposes any
        current packet-level shape axes for telemetry/formula grounding.  It
        does **not** infer a native policy or inspect action names.
        """
        hs = getattr(header, "state", header)

        def g(name: str, default: float = 0.5) -> float:
            return self._clamp01(getattr(hs, name, default), default)

        out = {
            "collapse_admissibility": g("collapse_admissibility", 0.5),
            "revision_permissibility": g("revision_permissibility", 0.5),
            "support_carry_forward": g("support_carry_forward", 0.5),
            "rival_breadth": g("rival_breadth", 0.5),
            "nonlocal_authority": g("nonlocal_authority", 0.5),
            "path_sensitivity": g("path_sensitivity", 0.5),
            "local_authority": g("local_authority", 0.5),
            "evidence_gate": g("evidence_gate", 0.5),
            "fracture_tolerance": g("fracture_tolerance", 0.5),
        }

        def _axes_from(src: Any) -> Dict[str, float]:
            if not isinstance(src, dict):
                return {}
            axes = src.get("axes", src)
            if not isinstance(axes, dict):
                return {}
            keys = (
                "hidden_decisiveness",
                "reshapeability",
                "local_cue_reliability",
                "revision_cost",
                "consequence_span",
                "topology_constraint",
            )
            return {k: self._clamp01(axes.get(k, 0.5), 0.5) for k in keys if k in axes}

        obs = observation if isinstance(observation, dict) else {}
        prims = primitives if isinstance(primitives, dict) else {}
        axes = _axes_from(obs.get("shape_prior6"))
        if not axes:
            contract = prims.get("_runtime_contract", {}) if isinstance(prims.get("_runtime_contract", {}), dict) else {}
            axes = _axes_from(contract.get("shape_prior6", {}))
        if axes:
            for key, val in axes.items():
                out[f"shape_{key}"] = float(val)

        # First-pass DynamicShapeField integration: CandidateSurface may publish
        # public-trace-derived effective controls for the next commitment step.
        # These controls are generic gauge/control deformations only.  They do
        # not contain action labels, family names, rewards, hidden state, or
        # external values.  CommitmentSurface consumes them so dynamic shape is
        # readout-visible instead of remaining candidate-side telemetry.
        dyn = prims.get("__dynamic_shape_effective_controls__") if isinstance(prims, dict) else None
        if isinstance(dyn, dict):
            applied = False
            for key in (
                "collapse_admissibility",
                "revision_permissibility",
                "support_carry_forward",
                "rival_breadth",
                "nonlocal_authority",
                "path_sensitivity",
                "local_authority",
                "evidence_gate",
                "fracture_tolerance",
                "candidate_sharpness",
                "persistence_allowance",
                "reopen_pressure",
                "low_evidence_sampling",
                "contradiction_sensitivity",
            ):
                if key in dyn:
                    if key in out:
                        out[f"static_{key}"] = float(out[key])
                    out[key] = self._clamp01(dyn.get(key, out.get(key, 0.5)), out.get(key, 0.5))
                    applied = True
            # Preserve DynamicShapeField-specific public state for telemetry and
            # formula audits.  These are not used as native policy labels.
            for key in (
                "dynamic_shape_urgency",
                "dynamic_shape_coarsening",
                "dynamic_shape_projection_horizon",
                "dynamic_shape_gauge_confidence",
            ):
                if key in dyn:
                    out[key] = self._clamp01(dyn.get(key, 0.0), 0.0)
            out["dynamic_shape_controls_applied"] = 1.0 if applied else 0.0
        else:
            out["dynamic_shape_controls_applied"] = 0.0
        return out

    def _canonical_commitment_choice(
        self,
        final_scores: Dict[Any, float],
        observation: Dict[str, Any],
        primitives: Dict[str, Any],
        header: Any,
        translator_mask: set,
        actions: List[Any],
    ) -> tuple[Any, Dict[str, Any]]:
        """Return the generic CO commitment decision and audit telemetry.

        This is the implementation-side form of the documented readout rule:
        admissibility -> dominance -> reopen/sampling -> stable continuation.

        It deliberately consumes only:
        - admissible candidate identities,
        - candidate-publication state,
        - direct controls projected from shape_prior6/header state,
        - and, when present, DynamicShapeField effective controls derived from
          public retained trace.

        It must not inspect family names or action labels.
        """
        controls = self._direct_control_snapshot(header, observation, primitives)
        rows = self._candidate_rows(observation, primitives, translator_mask)
        legal_domain = [a for a in (actions or []) if a not in translator_mask]
        if not rows and not final_scores:
            raise RuntimeError(
                "CommitmentSurface fail-closed: no candidate rows or CO scores; "
                "canonical CO path forbids empty/first-legal fallback."
            )

        row_by_action: Dict[Any, Dict[str, Any]] = {r.get("action"): r for r in rows if r.get("action") is not None}
        # Evidence-bearing domain only.  Legal action space alone is not a
        # candidate proposal and must not be used as a first-legal/uniform
        # rescue.  Candidate rows or CO scores must supply the action.
        domain = list(dict.fromkeys(list(row_by_action.keys()) + list(final_scores.keys())))
        domain = [a for a in domain if a not in translator_mask]
        if not domain:
            raise RuntimeError(
                "CommitmentSurface fail-closed: no admissible evidence-bearing candidate; "
                "canonical CO path forbids legal-action-space fallback."
            )

        # Direct-control interpretation.  These are regime-conditioned weights,
        # not action presets.
        local_auth = controls["local_authority"]
        nonlocal_auth = controls["nonlocal_authority"]
        path_sens = controls["path_sensitivity"]
        revision = controls["revision_permissibility"]
        collapse = controls["collapse_admissibility"]
        carry = controls["support_carry_forward"]
        rival = controls["rival_breadth"]
        fracture_tol = controls["fracture_tolerance"]

        local_weight = self._clamp01(0.32 + 0.42 * local_auth + 0.18 * collapse + 0.08 * controls["evidence_gate"])
        stability_weight = self._clamp01(0.16 + 0.42 * carry + 0.12 * collapse - 0.10 * revision)
        burden_weight = self._clamp01(0.18 + 0.34 * nonlocal_auth + 0.26 * path_sens + 0.18 * revision + 0.12 * (1.0 - fracture_tol))
        sampling_weight = self._clamp01(0.10 + 0.30 * rival + 0.26 * nonlocal_auth + 0.22 * revision + 0.12 * (1.0 - local_auth))
        dominance_margin = self._clamp01(
            0.05 + 0.12 * rival + 0.10 * revision + 0.08 * nonlocal_auth + 0.06 * path_sens
            - 0.08 * collapse - 0.05 * local_auth,
            0.10,
        )
        dominance_margin = max(0.04, min(0.32, dominance_margin))
        burden_alarm = self._clamp01(0.32 + 0.26 * nonlocal_auth + 0.22 * path_sens + 0.16 * revision + 0.10 * rival - 0.12 * local_auth)

        assessments: Dict[Any, Dict[str, float]] = {}
        for a in domain:
            row = row_by_action.get(a, {})
            field_score = self._clamp01(final_scores.get(a, 0.0), 0.0)
            support_mass = self._clamp01(row.get("support_mass", row.get("base_state", row.get("support_conf", field_score))), field_score)
            decision_state = self._clamp01(row.get("decision_state", row.get("base_state", field_score)), field_score)
            local_support = self._clamp01(row.get("local_support", support_mass), support_mass)
            raw_burden = self._clamp01(row.get("contradiction_burden", row.get("fracture_state", row.get("contradiction", 0.0))), 0.0)
            burden_accumulation = self._clamp01(row.get("burden_accumulation", raw_burden), raw_burden)
            continuation_instability = self._clamp01(row.get("continuation_instability", burden_accumulation), burden_accumulation)
            burden_trend = self._clamp01(row.get("burden_trend", 0.0), 0.0)
            burden = self._clamp01(0.70 * raw_burden + 0.15 * burden_accumulation + 0.10 * continuation_instability + 0.05 * burden_trend)
            raw_stability = self._clamp01(row.get("commitment_stability", row.get("persistence_state", row.get("continuity", 0.0))), 0.0)
            continuation_viability = self._clamp01(row.get("continuation_viability", raw_stability), raw_stability)
            support_persistence = self._clamp01(row.get("support_persistence", raw_stability), raw_stability)
            stability = self._clamp01(0.42 * raw_stability + 0.36 * continuation_viability + 0.22 * support_persistence)
            sampling = self._clamp01(row.get("sampling_demand", row.get("salience_state", 0.0)), 0.0)
            sampling = self._clamp01(sampling + 0.06 * continuation_instability * (0.40 + 0.60 * (rival + nonlocal_auth) / 2.0))
            uncertainty = self._clamp01(row.get("uncertainty", 1.0 - support_mass), 1.0 - support_mass)

            # Structured earned-collapse certificate.  This is first-class
            # relation/collapse evidence produced upstream by RelationSurface +
            # RCF + collapse_certificate.  Defaults are neutral so older rows do
            # not acquire implicit policy.
            cert_ready = 1.0 if bool(row.get("collapse_certificate_ready", False)) else 0.0
            cert_score = self._clamp01(row.get("collapse_certificate_score", row.get("field_collapse_readiness", 0.0)), 0.0)
            cert_blocker_pressure = self._clamp01(row.get("collapse_certificate_blocker_pressure", 0.0), 0.0)
            cert_recursion = self._clamp01(row.get("collapse_certificate_recursion_demand", 0.0), 0.0)
            unresolved_rivals = self._clamp01(float(row.get("unresolved_rival_count", row.get("relation_unresolved_rival_count", 0)) or 0.0) / 3.0)
            quotient_resolved = self._clamp01(float(row.get("quotient_resolved_rival_count", 0) or 0.0) / 2.0)
            collapse_blocked = self._clamp01(max(cert_blocker_pressure, unresolved_rivals * (1.0 - 0.50 * quotient_resolved)))
            relation_ready_bonus = self._clamp01(0.55 * cert_score + 0.25 * cert_ready + 0.20 * quotient_resolved)
            has_certificate = bool(
                row.get("collapse_certificate_status") is not None
                or row.get("collapse_certificate")
                or row.get("relation_surface_public_effect_count", 0)
                or row.get("field_relation_count", 0)
            )
            # Certified docs require CommitmentSurface to respect certificate
            # gates.  A non-ready certificate is not automatically a hard veto
            # for all readout modes, but it must block dominance-style earned
            # collapse when relation/burden structure says another layer may
            # still matter.  This keeps high local support from overriding
            # unresolved hiddenness, grey, recursion, or blocker pressure.
            certificate_gate_open = self._clamp01(
                max(
                    cert_ready,
                    1.0 - max(
                        cert_recursion / max(0.22, 0.44 + 0.18 * collapse - 0.16 * revision),
                        cert_blocker_pressure / max(0.10, 0.26 + 0.18 * collapse),
                    ),
                )
            ) if has_certificate else 1.0
            certificate_blocks_dominance = bool(
                has_certificate
                and cert_ready <= 0.0
                and (
                    cert_recursion >= max(0.24, 0.38 + 0.12 * collapse - 0.12 * revision)
                    or cert_blocker_pressure >= max(0.12, 0.24 - 0.08 * collapse + 0.08 * revision)
                    or bool(row.get("collapse_blockers"))
                )
            )

            # Resolver support is restricted to operations that reduce, expose,
            # cancel, or buffer an active burden.  Plain transform is not a
            # resolver here: a transformation may reopen or redirect burden,
            # but without an explicit reduce/reveal/reset/buffer fact it must
            # remain recursion/transform pressure rather than a certificate
            # clearance signal.
            resolver_support = self._clamp01(max(
                row.get("branch_internal_resolver_support", 0.0),
                row.get("branch_internal_exposure_support", 0.0),
                row.get("branch_internal_relief_support", 0.0),
                row.get("branch_internal_cancellation_support", 0.0),
                row.get("branch_internal_buffering_support", 0.0),
            ))
            carrier_only_pressure = self._clamp01(max(
                row.get("branch_internal_unresolved_pressure", 0.0),
                row.get("branch_internal_hiddenness_pressure", 0.0),
                row.get("branch_internal_masking_pressure", 0.0),
                row.get("branch_internal_raw_carry_pressure", 0.0),
            ))

            support = self._clamp01(0.32 * support_mass + 0.26 * decision_state + 0.18 * local_support + 0.16 * field_score + 0.08 * continuation_viability)
            dominance_support_component = local_weight * support
            dominance_stability_component = stability_weight * stability
            dominance_field_component = 0.08 * field_score
            dominance_relation_component = 0.12 * relation_ready_bonus * (0.35 + 0.65 * collapse)
            dominance_burden_penalty = burden_weight * burden
            dominance_trend_penalty = 0.04 * burden_trend * (path_sens + nonlocal_auth)
            dominance_blocker_penalty = 0.18 * collapse_blocked * (0.45 + 0.55 * (revision + rival) / 2.0)
            dominance_positive_mass = (
                dominance_support_component
                + dominance_stability_component
                + dominance_field_component
                + dominance_relation_component
            )
            dominance_negative_mass = (
                dominance_burden_penalty
                + dominance_trend_penalty
                + dominance_blocker_penalty
            )
            dominance_score = dominance_positive_mass - dominance_negative_mass

            sampling_sampling_component = sampling_weight * sampling
            sampling_uncertainty_component = 0.18 * uncertainty * (rival + nonlocal_auth)
            sampling_burden_component = 0.12 * burden * burden_alarm
            sampling_instability_component = 0.08 * continuation_instability * revision
            sampling_recursion_component = 0.16 * cert_recursion * (0.35 + 0.65 * (revision + nonlocal_auth) / 2.0)
            sampling_blocker_component = 0.10 * collapse_blocked * (0.35 + 0.65 * revision)
            sampling_support_penalty = 0.10 * support * collapse
            sampling_score = (
                sampling_sampling_component
                + sampling_uncertainty_component
                + sampling_burden_component
                + sampling_instability_component
                + sampling_recursion_component
                + sampling_blocker_component
                - sampling_support_penalty
            )

            continuation_support_component = 0.28 * support
            continuation_stability_component = 0.30 * stability * (0.55 + 0.45 * carry)
            continuation_field_component = 0.12 * field_score
            continuation_viability_component = 0.10 * continuation_viability
            continuation_relation_component = 0.10 * relation_ready_bonus
            continuation_low_burden_component = 0.12 * (1.0 - burden) * (0.45 + 0.55 * nonlocal_auth)
            continuation_burden_penalty = burden_weight * burden
            continuation_blocker_penalty = 0.10 * collapse_blocked * (0.40 + 0.60 * revision)
            continuation_sampling_penalty = 0.08 * sampling * (1.0 - revision)
            continuation_score = (
                continuation_support_component
                + continuation_stability_component
                + continuation_field_component
                + continuation_viability_component
                + continuation_relation_component
                + continuation_low_burden_component
                - continuation_burden_penalty
                - continuation_blocker_penalty
                - continuation_sampling_penalty
            )
            assessments[a] = {
                "support": float(support),
                "field_score": float(field_score),
                "burden": float(burden),
                "raw_burden": float(raw_burden),
                "burden_accumulation": float(burden_accumulation),
                "burden_trend": float(burden_trend),
                "continuation_instability": float(continuation_instability),
                "continuation_viability": float(continuation_viability),
                "stability": float(stability),
                "sampling": float(sampling),
                "uncertainty": float(uncertainty),
                "collapse_certificate_ready": float(cert_ready),
                "collapse_certificate_score": float(cert_score),
                "collapse_certificate_blocker_pressure": float(cert_blocker_pressure),
                "collapse_certificate_recursion_demand": float(cert_recursion),
                "collapse_blocked": float(collapse_blocked),
                "certificate_gate_open": float(certificate_gate_open),
                "certificate_blocks_dominance": float(1.0 if certificate_blocks_dominance else 0.0),
                "resolver_support": float(resolver_support),
                "carrier_only_pressure": float(carrier_only_pressure),
                "unresolved_rival_pressure": float(unresolved_rivals),
                "quotient_resolved_pressure": float(quotient_resolved),
                "dominance_score": float(dominance_score),
                "dominance_positive_mass": float(dominance_positive_mass),
                "dominance_negative_mass": float(dominance_negative_mass),
                "dominance_support_component": float(dominance_support_component),
                "dominance_stability_component": float(dominance_stability_component),
                "dominance_field_component": float(dominance_field_component),
                "dominance_relation_component": float(dominance_relation_component),
                "dominance_burden_penalty": float(dominance_burden_penalty),
                "dominance_trend_penalty": float(dominance_trend_penalty),
                "dominance_blocker_penalty": float(dominance_blocker_penalty),
                "sampling_score": float(sampling_score),
                "sampling_sampling_component": float(sampling_sampling_component),
                "sampling_uncertainty_component": float(sampling_uncertainty_component),
                "sampling_burden_component": float(sampling_burden_component),
                "sampling_instability_component": float(sampling_instability_component),
                "sampling_recursion_component": float(sampling_recursion_component),
                "sampling_blocker_component": float(sampling_blocker_component),
                "sampling_support_penalty": float(sampling_support_penalty),
                "continuation_score": float(continuation_score),
                "continuation_support_component": float(continuation_support_component),
                "continuation_stability_component": float(continuation_stability_component),
                "continuation_field_component": float(continuation_field_component),
                "continuation_viability_component": float(continuation_viability_component),
                "continuation_relation_component": float(continuation_relation_component),
                "continuation_low_burden_component": float(continuation_low_burden_component),
                "continuation_burden_penalty": float(continuation_burden_penalty),
                "continuation_blocker_penalty": float(continuation_blocker_penalty),
                "continuation_sampling_penalty": float(continuation_sampling_penalty),
            }

        def _shape_gauge_for_carrier(carrier: Any) -> Dict[str, float]:
            """Return the local problem-shape gauge for resolver timing.

            Base problem shape/direct controls set the prior gauge.  Current
            public branch pressure then updates that gauge locally for this
            commitment only.  This is not a topology edit and not a learned
            policy: it says how strongly the current public relations should
            count under the declared problem shape.
            """
            ass = assessments[carrier]
            hidden_axis = controls.get("shape_hidden_decisiveness", nonlocal_auth)
            reshape_axis = controls.get("shape_reshapeability", revision)
            local_axis = controls.get("shape_local_cue_reliability", local_auth)
            revision_axis = controls.get("shape_revision_cost", revision)
            consequence_axis = controls.get("shape_consequence_span", nonlocal_auth)
            topology_axis = controls.get("shape_topology_constraint", rival)
            base_shape_urgency = self._clamp01(
                0.24 * consequence_axis
                + 0.20 * revision_axis
                + 0.18 * hidden_axis
                + 0.14 * topology_axis
                + 0.12 * reshape_axis
                + 0.12 * (1.0 - local_axis)
            )
            direct_shape_urgency = self._clamp01(
                0.26 * nonlocal_auth
                + 0.24 * path_sens
                + 0.18 * revision
                + 0.14 * rival
                + 0.10 * (1.0 - local_auth)
                + 0.08 * (1.0 - collapse)
            )
            carrier_pressure = self._clamp01(max(
                ass.get("carrier_only_pressure", 0.0),
                ass.get("collapse_blocked", 0.0),
                0.75 * ass.get("collapse_certificate_blocker_pressure", 0.0),
                0.55 * ass.get("collapse_certificate_recursion_demand", 0.0),
            ))
            local_shape_urgency = self._clamp01(
                0.42 * base_shape_urgency
                + 0.34 * direct_shape_urgency
                + 0.24 * carrier_pressure
            )
            min_carrier_pressure = max(
                self._formula_param("preblocking_carrier_pressure_floor", 0.42),
                min(
                    self._formula_param("preblocking_carrier_pressure_cap", 0.72),
                    self._formula_param("preblocking_carrier_pressure_base", 0.70)
                    - self._formula_param("preblocking_carrier_shape_urgency_weight", 0.37) * local_shape_urgency,
                ),
            )
            return {
                "base_shape_urgency": float(base_shape_urgency),
                "direct_shape_urgency": float(direct_shape_urgency),
                "local_shape_urgency": float(local_shape_urgency),
                "carrier_pressure_for_timing": float(carrier_pressure),
                "preblocking_min_carrier_pressure": float(min_carrier_pressure),
            }

        def _commitment_blocked(a: Any) -> bool:
            ass = assessments[a]
            return bool(
                ass.get("certificate_blocks_dominance", 0.0) >= 0.5
                or (ass.get("collapse_blocked", 0.0) >= 0.55 and collapse < 0.75)
            )

        def _shape_gauged_resolver_alt(
            carrier: Any,
            ordered: List[Any],
            *,
            score_key: str,
        ) -> tuple[Optional[Any], Dict[str, float]]:
            """Find a generic resolver alternative before formal blockage.

            This implements the CO-derived timing idea: under a problem shape
            where delay/consequence/revision/hiddenness make carried burden
            urgent, a relation-mediated resolver may bend commitment before the
            carrier branch becomes certificate-blocked.  The test is relational
            and shape-gauged; it never mentions native action labels.
            """
            carrier_ass = assessments[carrier]
            gauge = _shape_gauge_for_carrier(carrier)
            carrier_pressure = gauge["carrier_pressure_for_timing"]
            local_urgency = gauge["local_shape_urgency"]
            required_resolver_support = max(
                self._formula_param("preblocking_resolver_support_floor", 0.10),
                min(
                    self._formula_param("preblocking_resolver_support_cap", 0.46),
                    self._formula_param("preblocking_resolver_support_base", 0.12)
                    + self._formula_param("preblocking_resolver_carrier_weight", 0.18) * carrier_pressure
                    + self._formula_param("preblocking_resolver_shape_weight", 0.10) * local_urgency,
                ),
            )
            telemetry = dict(gauge)
            telemetry.update({
                "preblocking_required_resolver_support": float(required_resolver_support),
                "preblocking_score_gap": 0.0,
                "preblocking_support_gap": 0.0,
                "preblocking_score_margin": 0.0,
                "preblocking_support_margin": 0.0,
            })
            if carrier_pressure < gauge["preblocking_min_carrier_pressure"]:
                return None, telemetry
            if carrier_ass.get("resolver_support", 0.0) >= required_resolver_support:
                return None, telemetry

            resolver_candidates = [
                a for a in ordered
                if a != carrier
                and not _commitment_blocked(a)
                and assessments[a].get("resolver_support", 0.0) >= required_resolver_support
            ]
            if not resolver_candidates:
                return None, telemetry
            alt = resolver_candidates[0]
            alt_ass = assessments[alt]
            score_gap = float(carrier_ass[score_key] - alt_ass[score_key])
            support_gap = float(carrier_ass["support"] - alt_ass["support"])
            score_margin = max(
                self._formula_param("preblocking_score_margin_floor", 0.05),
                min(
                    self._formula_param("preblocking_score_margin_cap", 0.22),
                    self._formula_param("preblocking_score_margin_base", 0.055)
                    + self._formula_param("preblocking_score_margin_pressure_weight", 0.08) * carrier_pressure
                    + self._formula_param("preblocking_score_margin_shape_weight", 0.07) * local_urgency
                    + self._formula_param("preblocking_score_margin_revision_weight", 0.03) * revision
                    - self._formula_param("preblocking_score_margin_collapse_narrowing", 0.02) * collapse
                    - self._formula_param("preblocking_score_margin_local_narrowing", 0.02) * local_auth,
                ),
            )
            support_margin = max(
                self._formula_param("preblocking_support_margin_floor", 0.08),
                min(
                    self._formula_param("preblocking_support_margin_cap", 0.26),
                    self._formula_param("preblocking_support_margin_base", 0.11)
                    + self._formula_param("preblocking_support_margin_pressure_weight", 0.07) * carrier_pressure
                    + self._formula_param("preblocking_support_margin_shape_weight", 0.06) * local_urgency
                    + self._formula_param("preblocking_support_margin_nonlocal_weight", 0.02) * nonlocal_auth
                    - self._formula_param("preblocking_support_margin_local_narrowing", 0.02) * local_auth,
                ),
            )
            resolver_timing_pressure = self._clamp01(
                alt_ass.get("resolver_support", 0.0)
                * (0.48 + 0.32 * local_urgency + 0.20 * carrier_pressure)
            )
            continuation_advantage = self._clamp01(
                max(0.0, support_gap) * 0.55
                + max(0.0, score_gap) * 0.45
            )
            telemetry.update({
                "preblocking_score_gap": float(score_gap),
                "preblocking_support_gap": float(support_gap),
                "preblocking_score_margin": float(score_margin),
                "preblocking_support_margin": float(support_margin),
                "preblocking_resolver_timing_pressure": float(resolver_timing_pressure),
                "preblocking_continuation_advantage": float(continuation_advantage),
            })
            comparable = score_gap <= score_margin and support_gap <= support_margin
            pressure_exceeds_advantage = resolver_timing_pressure >= (
                continuation_advantage
                + self._formula_param("preblocking_resolver_advantage_margin", 0.03)
            )
            if comparable or pressure_exceeds_advantage or alt_ass["continuation_score"] > carrier_ass["continuation_score"]:
                return alt, telemetry
            return None, telemetry

        ordered_dom = sorted(domain, key=lambda a: assessments[a]["dominance_score"], reverse=True)
        top = ordered_dom[0]
        second = ordered_dom[1] if len(ordered_dom) > 1 else None
        top_dom = assessments[top]["dominance_score"]
        second_dom = assessments[second]["dominance_score"] if second is not None else -1.0
        top_support = assessments[top]["support"]
        top_burden = assessments[top]["burden"]
        top_stability = assessments[top]["stability"]
        top_relation_blocked = (
            (assessments[top].get("collapse_blocked", 0.0) >= 0.55 and collapse < 0.75)
            or bool(assessments[top].get("certificate_blocks_dominance", 0.0) >= 0.5)
        )
        dominance_ready = (
            second is None
            or (
                (top_dom - second_dom) >= dominance_margin
                and top_support >= 0.22
                and top_burden <= max(0.72, 0.42 + 0.45 * fracture_tol)
                and (top_stability >= 0.12 or collapse >= 0.55 or top_support >= 0.62)
                and not top_relation_blocked
                and not (
                    assessments[top]["sampling"] >= 0.65
                    and sampling_weight >= 0.35
                    and collapse < 0.50
                )
            )
        )
        if dominance_ready:
            preblocking_alt, preblocking_tel = _shape_gauged_resolver_alt(
                top, ordered_dom, score_key="dominance_score"
            )
            if preblocking_alt is not None:
                return preblocking_alt, {
                    "canonical_commitment_mode": "reopen_or_sample",
                    "canonical_commitment_reason": "shape_gauged_preblocking_resolver_timing_before_dominance",
                    "dominance_margin": float(dominance_margin),
                    "shape_gauged_resolver_timing_applied": True,
                    "shape_gauged_resolver_timing_original": str(top),
                    "shape_gauged_resolver_timing_alternative": str(preblocking_alt),
                    "local_shape_gauge": dict(preblocking_tel),
                    "canonical_commitment_assessment": {str(k): dict(v) for k, v in assessments.items()},
                    "direct_controls_used": controls,
                }
            return top, {
                "canonical_commitment_mode": "dominance",
                "canonical_commitment_reason": "one_candidate_dominates_support_burden_stability",
                "dominance_margin": float(dominance_margin),
                "shape_gauged_resolver_timing_applied": False,
                "local_shape_gauge": dict(preblocking_tel),
                "canonical_commitment_assessment": {str(k): dict(v) for k, v in assessments.items()},
                "direct_controls_used": controls,
            }

        ordered_sample = sorted(domain, key=lambda a: assessments[a]["sampling_score"], reverse=True)
        sample = ordered_sample[0]
        sample_score = assessments[sample]["sampling_score"]
        continuation_best = max(assessments[a]["continuation_score"] for a in domain)
        avg_burden = sum(assessments[a]["burden"] for a in domain) / float(len(domain) or 1)
        avg_uncertainty = sum(assessments[a]["uncertainty"] for a in domain) / float(len(domain) or 1)
        unresolved = self._clamp01(0.42 * avg_burden + 0.34 * avg_uncertainty + 0.24 * (1.0 - (top_dom - second_dom + 1.0) / 2.0))
        if (
            sample_score >= max(0.18, continuation_best - 0.04)
            and (sample_score >= 0.20 + 0.10 * collapse or unresolved >= 0.42)
            and sampling_weight >= 0.22
        ):
            # Certificate-aware reopen/sample.  Sampling should reopen or expose
            # unresolved structure; it should not select a blocked branch merely
            # because that branch carries burden.  A blocked sample can still be
            # selected when it has its own resolver operation (e.g. sampling an
            # uncertain arm reduces that arm's uncertainty) or no comparable
            # unblocked resolver exists.
            original_sample = sample
            resolver_alt = None
            sampling_gate_margin = 0.0
            sampling_support_advantage_limit = 0.0
            selected_sampling_gap = 0.0
            selected_sampling_support_gap = 0.0
            required_resolver_support = self._formula_param("resolver_support_threshold", 0.08)
            sample_ass = assessments[sample]
            sample_blocker_pressure = self._clamp01(max(
                sample_ass.get("collapse_blocked", 0.0),
                sample_ass.get("collapse_certificate_blocker_pressure", 0.0),
                sample_ass.get("collapse_certificate_recursion_demand", 0.0),
                sample_ass.get("carrier_only_pressure", 0.0),
                1.0 - sample_ass.get("certificate_gate_open", 1.0),
            ))
            # A resolver must be adequate to the unresolved burden it is being
            # used to reopen.  The base threshold rejects noise-level resolver
            # facts; carrier/blocker scaling prevents a tiny reducer/exposer
            # from displacing a heavily burdened branch merely because it passed
            # the floor.  This remains structural: it reads public burden
            # pressure, not action names or rewards.
            if _commitment_blocked(sample):
                required_resolver_support = max(
                    self._formula_param("resolver_support_threshold", 0.08),
                    min(
                        self._formula_param("resolver_support_scaled_cap", 0.32),
                        self._formula_param("resolver_support_scaled_base", 0.08)
                        + self._formula_param("resolver_support_carrier_weight", 0.12) * sample_ass.get("carrier_only_pressure", 0.0)
                        + self._formula_param("resolver_support_blocker_weight", 0.05) * sample_blocker_pressure,
                    ),
                )
            shape_resolver_alt, shape_resolver_tel = _shape_gauged_resolver_alt(
                sample, ordered_sample, score_key="sampling_score"
            )
            if shape_resolver_alt is not None:
                resolver_alt = shape_resolver_alt
                sample = shape_resolver_alt
                sample_score = assessments[sample]["sampling_score"]
                selected_sampling_gap = float(shape_resolver_tel.get("preblocking_score_gap", 0.0))
                selected_sampling_support_gap = float(shape_resolver_tel.get("preblocking_support_gap", 0.0))
                sampling_gate_margin = float(shape_resolver_tel.get("preblocking_score_margin", 0.0))
                sampling_support_advantage_limit = float(shape_resolver_tel.get("preblocking_support_margin", 0.0))
                required_resolver_support = float(shape_resolver_tel.get("preblocking_required_resolver_support", required_resolver_support))
            elif _commitment_blocked(sample) and sample_ass.get("resolver_support", 0.0) < required_resolver_support:
                resolver_candidates = [
                    a for a in ordered_sample
                    if a != sample
                    and not _commitment_blocked(a)
                    and assessments[a].get("resolver_support", 0.0) >= required_resolver_support
                ]
                if resolver_candidates:
                    alt = resolver_candidates[0]
                    alt_ass = assessments[alt]
                    blocker_pressure = sample_blocker_pressure
                    sampling_gate_margin = max(
                        self._formula_param("sampling_gate_margin_floor", 0.05),
                        min(
                            self._formula_param("sampling_gate_margin_cap", 0.18),
                            self._formula_param("sampling_gate_margin_base", 0.055)
                            + self._formula_param("sampling_gate_margin_blocker_weight", 0.070) * blocker_pressure
                            + self._formula_param("sampling_gate_margin_revision_weight", 0.030) * revision
                            + self._formula_param("sampling_gate_margin_nonlocal_weight", 0.025) * nonlocal_auth
                            + self._formula_param("sampling_gate_margin_rival_weight", 0.020) * rival
                            - self._formula_param("sampling_gate_margin_collapse_narrowing", 0.020) * collapse
                            - self._formula_param("sampling_gate_margin_local_narrowing", 0.015) * local_auth,
                        ),
                    )
                    sampling_support_advantage_limit = max(
                        self._formula_param("sampling_support_advantage_floor", 0.10),
                        min(
                            self._formula_param("sampling_support_advantage_cap", 0.30),
                            self._formula_param("sampling_support_advantage_base", 0.13)
                            + self._formula_param("sampling_support_advantage_blocker_weight", 0.070) * blocker_pressure
                            + self._formula_param("sampling_support_advantage_revision_weight", 0.030) * revision
                            + self._formula_param("sampling_support_advantage_nonlocal_weight", 0.020) * nonlocal_auth
                            - self._formula_param("sampling_support_advantage_collapse_narrowing", 0.020) * collapse
                            - self._formula_param("sampling_support_advantage_local_narrowing", 0.015) * local_auth,
                        ),
                    )
                    selected_sampling_gap = float(sample_ass["sampling_score"] - alt_ass["sampling_score"])
                    selected_sampling_support_gap = float(sample_ass["support"] - alt_ass["support"])
                    if (
                        selected_sampling_gap <= sampling_gate_margin
                        and selected_sampling_support_gap <= sampling_support_advantage_limit
                    ) or alt_ass["continuation_score"] > sample_ass["continuation_score"]:
                        resolver_alt = alt
                        sample = alt
                        sample_score = assessments[sample]["sampling_score"]

            return sample, {
                "canonical_commitment_mode": "reopen_or_sample",
                "canonical_commitment_reason": (
                    "shape_gauged_preblocking_resolver_timing_during_reopen_sample"
                    if shape_resolver_alt is not None
                    else (
                        "certificate_aware_resolver_reopen_or_sample_after_non_dominance"
                        if resolver_alt is not None
                        else "no_dominance_and_unresolved_sampling_or_revision_pressure"
                    )
                ),
                "dominance_margin": float(dominance_margin),
                "unresolved_pressure": float(unresolved),
                "certificate_aware_reopen_or_sample_applied": bool(resolver_alt is not None),
                "certificate_aware_reopen_or_sample_original": str(original_sample) if resolver_alt is not None else None,
                "certificate_aware_reopen_or_sample_alternative": str(resolver_alt) if resolver_alt is not None else None,
                "shape_gauged_resolver_timing_applied": bool(shape_resolver_alt is not None),
                "shape_gauged_resolver_timing_original": str(original_sample) if shape_resolver_alt is not None else None,
                "shape_gauged_resolver_timing_alternative": str(shape_resolver_alt) if shape_resolver_alt is not None else None,
                "local_shape_gauge": dict(shape_resolver_tel),
                "sampling_gate_margin": float(sampling_gate_margin),
                "sampling_support_advantage_limit": float(sampling_support_advantage_limit),
                "required_resolver_support": float(required_resolver_support),
                "selected_sampling_gap_before_certificate_gating": float(selected_sampling_gap),
                "selected_sampling_support_gap_before_certificate_gating": float(selected_sampling_support_gap),
                "canonical_commitment_assessment": {str(k): dict(v) for k, v in assessments.items()},
                "direct_controls_used": controls,
            }

        ordered_cont = sorted(domain, key=lambda a: assessments[a]["continuation_score"], reverse=True)
        cont = ordered_cont[0]

        # Certificate-aware stable continuation.  Dominance gating already
        # prevents a non-ready/blocked certificate from being treated as earned
        # collapse.  Stable continuation is more permissive: a live branch may
        # continue under unresolved burden.  But it must not reduce to
        # "highest continuation score after dominance failed" when a comparable
        # unblocked alternative exists.  This post-dominance check therefore
        # prefers the best unblocked continuation unless the blocked branch is
        # materially and structurally ahead.
        def _cont_blocked(a: Any) -> bool:
            return _commitment_blocked(a)

        unblocked_continuations = [a for a in ordered_cont if not _cont_blocked(a)]
        certificate_aware_alt = None
        shape_stable_alt, shape_stable_tel = _shape_gauged_resolver_alt(
            cont, ordered_cont, score_key="continuation_score"
        )
        if shape_stable_alt is not None:
            cont = shape_stable_alt
        continuation_gate_margin = 0.0
        support_advantage_limit = 0.0
        selected_continuation_gap = 0.0
        selected_support_gap = 0.0
        if shape_stable_alt is None and _cont_blocked(cont) and unblocked_continuations:
            alt = unblocked_continuations[0]
            cont_ass = assessments[cont]
            alt_ass = assessments[alt]
            blocker_pressure = self._clamp01(max(
                cont_ass.get("collapse_blocked", 0.0),
                cont_ass.get("collapse_certificate_blocker_pressure", 0.0),
                cont_ass.get("collapse_certificate_recursion_demand", 0.0),
                1.0 - cont_ass.get("certificate_gate_open", 1.0),
            ))
            # The margin is generic and structural: stronger unresolved blocker
            # pressure, wider rivalry, nonlocal authority, and revision
            # permissibility make unblocked alternatives more authoritative.
            # Collapse/local authority narrow the margin so a branch can still
            # continue under burden when it is materially stronger.
            continuation_gate_margin = max(
                self._formula_param("continuation_gate_margin_floor", 0.04),
                min(
                    self._formula_param("continuation_gate_margin_cap", 0.16),
                    self._formula_param("continuation_gate_margin_base", 0.045)
                    + self._formula_param("continuation_gate_margin_blocker_weight", 0.065) * blocker_pressure
                    + self._formula_param("continuation_gate_margin_revision_weight", 0.030) * revision
                    + self._formula_param("continuation_gate_margin_rival_weight", 0.020) * rival
                    + self._formula_param("continuation_gate_margin_nonlocal_weight", 0.020) * nonlocal_auth
                    - self._formula_param("continuation_gate_margin_collapse_narrowing", 0.025) * collapse
                    - self._formula_param("continuation_gate_margin_local_narrowing", 0.020) * local_auth,
                ),
            )
            support_advantage_limit = max(
                self._formula_param("support_advantage_limit_floor", 0.12),
                min(
                    self._formula_param("support_advantage_limit_cap", 0.28),
                    self._formula_param("support_advantage_limit_base", 0.16)
                    + self._formula_param("support_advantage_limit_blocker_weight", 0.08) * blocker_pressure
                    + self._formula_param("support_advantage_limit_revision_weight", 0.03) * revision
                    + self._formula_param("support_advantage_limit_nonlocal_weight", 0.02) * nonlocal_auth
                    - self._formula_param("support_advantage_limit_collapse_narrowing", 0.03) * collapse
                    - self._formula_param("support_advantage_limit_local_narrowing", 0.02) * local_auth,
                ),
            )
            selected_continuation_gap = float(cont_ass["continuation_score"] - alt_ass["continuation_score"])
            selected_support_gap = float(cont_ass["support"] - alt_ass["support"])
            comparable_unblocked_alt = (
                selected_continuation_gap <= continuation_gate_margin
                and selected_support_gap <= support_advantage_limit
            )
            if comparable_unblocked_alt:
                certificate_aware_alt = alt
                cont = alt

        return cont, {
            "canonical_commitment_mode": "stable_continuation",
            "canonical_commitment_reason": (
                "shape_gauged_preblocking_resolver_timing_during_stable_continuation"
                if shape_stable_alt is not None
                else (
                    "certificate_aware_unblocked_stable_continuation_after_non_dominance"
                    if certificate_aware_alt is not None
                    else "least_burden_stable_continuation_after_non_dominance"
                )
            ),
            "dominance_margin": float(dominance_margin),
            "unresolved_pressure": float(unresolved),
            "continuation_gate_margin": float(continuation_gate_margin),
            "support_advantage_limit": float(support_advantage_limit),
            "selected_continuation_gap_before_certificate_gating": float(selected_continuation_gap),
            "selected_support_gap_before_certificate_gating": float(selected_support_gap),
            "certificate_aware_stable_continuation_applied": bool(certificate_aware_alt is not None),
            "certificate_aware_stable_continuation_alternative": str(certificate_aware_alt) if certificate_aware_alt is not None else None,
            "shape_gauged_resolver_timing_applied": bool(shape_stable_alt is not None),
            "shape_gauged_resolver_timing_alternative": str(shape_stable_alt) if shape_stable_alt is not None else None,
            "local_shape_gauge": dict(shape_stable_tel),
            "canonical_commitment_assessment": {str(k): dict(v) for k, v in assessments.items()},
            "direct_controls_used": controls,
        }

    def step(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Run the final readout step and return action, mode, and audit telemetry."""
        try:
            hs = getattr(header, "state", header)
            co_w = float(getattr(hs, "co_weight", 1.0)) if self.co_weight_override is None else float(self.co_weight_override)
            non_co_weight = 0.0
            actions = list(observation.get("action_space") or [])
            bus_scores, n_votes = self._bus_scores(primitives, observation)
            translator_mask = {c.get("candidate_id") for c in (observation.get("candidates") or []) if isinstance(c, dict) and not bool(c.get("legal", True))}
            translator_mask = set(a for a in translator_mask if a is not None)
            co_scores: Dict[Any, float] = {}
            sig_src = self._signal_snapshot(primitives)
            assessment = self._operative_assessment(observation, primitives, sig_src)
            if isinstance(primitives, dict):
                primitives["_operative_relevance_assessment"] = dict(assessment or {})
            if isinstance(bus_scores, dict) and "__scoped__" in bus_scores:
                scoped = bus_scores.get("__scoped__")
                if isinstance(scoped, dict):
                    co_scores = normalize_scores(self._typed_fuse_scoped(scoped, sig_src))
            elif bus_scores:
                co_scores = normalize_scores(dict(bus_scores))

            ei_ann = primitives.get("_ei_candidate_annotations") or {}
            if isinstance(ei_ann, dict) and ei_ann:
                try:
                    ei_norm = normalize_scores({k: float(v) for k, v in ei_ann.items() if isinstance(v, (int, float))})
                except Exception:
                    ei_norm = {}
                if ei_norm:
                    co_scores = normalize_scores(self._fuse_safe([(co_scores, 1.0), (ei_norm, 0.75)])) if co_scores else dict(ei_norm)

            obs_scores, obs_meta = candidate_evidence_scores(observation, primitives)
            if translator_mask and obs_scores:
                obs_scores = {a: v for a, v in obs_scores.items() if a not in translator_mask}
            if obs_scores:
                bus_live = 1.0 if n_votes > 0 else 0.0
                readiness = float(obs_meta.get("readiness", 0.0) or 0.0)
                goal_sharp = float(obs_meta.get("goal_sharpness", 0.0) or 0.0)
                support_peak = float(obs_meta.get("support_peak", 0.0) or 0.0)
                tested_peak = float(obs_meta.get("tested_peak", 0.0) or 0.0)
                obs_w = max(0.12, min(0.58, 0.14 + 0.18 * readiness + 0.10 * goal_sharp + 0.08 * support_peak + 0.06 * tested_peak + 0.08 * (1.0 - bus_live)))
                co_scores = normalize_scores(self._fuse_safe([(co_scores, 1.0), (obs_scores, obs_w)])) if co_scores else normalize_scores(dict(obs_scores))
            else:
                obs_meta = {"readiness": 0.0, "top_margin": 0.0, "support_peak": 0.0, "tested_peak": 0.0, "goal_sharpness": 0.0, "goal_certainty": 0.0, "goal_stability": 0.0, "avg_uncertainty": 1.0, "avg_contradiction": 0.0}

            evidence_domain = list(dict.fromkeys(list(co_scores.keys()) + list((ei_ann or {}).keys()) + list((obs_scores or {}).keys())))
            final_scores: Dict[Any, float] = {}
            if evidence_domain:
                for a in evidence_domain:
                    final_scores[a] = float(co_scores.get(a, 0.0))
            if translator_mask:
                for a in list(final_scores.keys()):
                    if a in translator_mask:
                        final_scores.pop(a, None)

            commit_readiness = float(obs_meta.get("readiness", 0.0) or 0.0)
            evidence_margin = float(obs_meta.get("top_margin", 0.0) or 0.0)
            evidence_support = max(float(obs_meta.get("support_peak", 0.0) or 0.0), float(obs_meta.get("tested_peak", 0.0) or 0.0))

            def _finalize_action(chosen: Any, out: Dict[str, Any]) -> Dict[str, Any]:
                if chosen in translator_mask:
                    raise RuntimeError(
                        "CommitmentSurface fail-closed: selected action is translator-masked; "
                        "canonical CO path forbids masked-action rescue."
                    )
                out["action"] = chosen
                out.setdefault("engineering_safety_triggered", False)
                out.setdefault("co_evidence_valid_for_step", True)
                return self._attach_telemetry(out, primitives, header, translator_mask, list(actions or []))


            if final_scores:
                best, canonical_telemetry = self._canonical_commitment_choice(
                    final_scores,
                    observation,
                    primitives,
                    header,
                    translator_mask,
                    list(actions or []),
                )
                co_sources = ["canonical_commitment_rule"]
                out = {
                    "co_policy": "kernel:commit",
                    "signal_bus_votes": int(n_votes),
                    "co_weight": float(co_w),
                    "non_co_weight": float(non_co_weight),
                    "co_sources": co_sources,
                    "commitment_compat_param_aliases_ignored": bool(self.compat_param_aliases_ignored),
                    "commit_readiness": float(commit_readiness),
                    "evidence_margin": float(evidence_margin),
                    "evidence_support": float(evidence_support),
                    "candidate_final_scores": {str(k): float(v) for k, v in final_scores.items()},
                    "candidate_obs_scores": {str(k): float(v) for k, v in (obs_scores or {}).items()},
                }
                out.update(canonical_telemetry)
                return _finalize_action(best, out)
            return {}
        except Exception as e:
            raise RuntimeError(f"CommitmentSurface failed without fallback: {e}") from e

    def metrics(self) -> Dict[str, Any]:
        return {"no_fallback_path": True, "commitment_compat_param_aliases_ignored": bool(self.compat_param_aliases_ignored)}
