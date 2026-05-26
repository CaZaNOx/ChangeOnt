"""Canonical candidate-publication surface.

Implements the intake side of the active docs loop described in
``44_CANONICAL_CANDIDATE_SURFACE.md`` and
``76_CONTINUATION_IDENTITY_AND_RELATION_PUBLICATION_CONTRACT.md``.

This module turns public adapter facts into candidate rows, continuation
identity hints, branch-internal burden-operation carriers, relation-surface
inputs, field updates, and certificate-ready row telemetry.  It is not a final
action selector and must not consume hidden policy conclusions.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from agents.co.runtime.support.scope_keys import resolve_decision_scope
from agents.co.runtime.surfaces.continuation_state import ContinuationStateTracker, derive_continuation_memory_id
from agents.co.runtime.surfaces.continuation_field import apply_continuation_field
from agents.co.runtime.surfaces.relation_surface import apply_relation_surface
from agents.co.runtime.surfaces.collapse_certificate import apply_collapse_certificates
from agents.co.runtime.surfaces.dynamic_shape_field import DynamicShapeField
from agents.co.runtime.surfaces.recursion_scheduler import apply_recursion_scheduler
from agents.co.runtime.surfaces.sequence_composition import SequenceContinuationComposer


def _signal_snapshot(prims: Dict[str, Any]) -> Dict[str, float]:
    """Return public signal-bus values for candidate telemetry; fail closed on malformed buses."""
    bus = prims.get("signal_bus")
    if bus is not None and hasattr(bus, "signals"):
        try:
            return {str(k): float(v) for k, v in (bus.signals() or {}).items()}
        except Exception as e:
            raise RuntimeError(f"CandidateEvidenceSurface failed without fallback: {e}") from e
    return {}


def _normalize01(x: Any, default: float = 0.0) -> float:
    try:
        v = float(x)
    except Exception:
        return float(default)
    if v < 0.0:
        return 0.0
    if v > 1.0:
        return 1.0
    return v


def _header_state(header: Any) -> Any:
    return getattr(header, "state", header)


def _candidate_visible_cue(cand: Dict[str, Any]) -> float:
    raw = cand.get("visible_delta", None)
    if raw is None:
        return 0.5
    try:
        v = float(raw)
    except Exception:
        return 0.5
    # Negative deltas are interpreted as below-neutral local support, not as a
    # separate family-specific cost signal.
    if v < 0.0:
        return _normalize01(0.5 + 0.5 * v)
    return _normalize01(v)




def _public_effects_from_candidate(cand: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract adapter-published public effects without interpreting them as policy."""
    value = cand.get("public_effects", cand.get("burden_effects", cand.get("effect_facts", [])))
    if isinstance(value, dict):
        return [dict(value)]
    if isinstance(value, list):
        return [dict(v) for v in value if isinstance(v, dict)]
    if isinstance(value, tuple):
        return [dict(v) for v in value if isinstance(v, dict)]
    return []


def _candidate_goal_cue(cand: Dict[str, Any]) -> float:
    # Canonical candidate publication must not consume adapter-authored
    # bestness/priority relations such as goal_relation/reward_relation/
    # context_relation.  Those may remain in older adapter packets for audit
    # compatibility, but this surface uses only thin public evidence and generic
    # burden/continuation fields.
    return 0.5


def _geometry_controls(header: Any, goal: Dict[str, Any]) -> Dict[str, float]:
    """Project header/goal state into generic controls used by candidate publication formulas."""
    hs = _header_state(header)
    gate = _normalize01(getattr(hs, "evidence_gate", 0.0))
    frac_tol = _normalize01(getattr(hs, "fracture_tolerance", 0.5))
    retain = _normalize01(getattr(hs, "retention_depth", 0.5))
    collapse = _normalize01(getattr(hs, "collapse_permission", 0.5))
    threshold = _normalize01(getattr(hs, "identity_support_threshold", 0.5))
    support_evidence = _normalize01(getattr(hs, "support_evidence", 0.0))
    rival_breadth = _normalize01(getattr(hs, "rival_breadth", 0.5))
    nonlocal_auth = _normalize01(getattr(hs, "nonlocal_authority", 0.5))
    path_sens = _normalize01(getattr(hs, "path_sensitivity", 0.5))
    local_auth = _normalize01(getattr(hs, "local_authority", 0.5))
    carry = _normalize01(getattr(hs, "support_carry_forward", 0.5))
    revision = _normalize01(getattr(hs, "revision_permissibility", 0.5))
    collapse_adm = _normalize01(getattr(hs, "collapse_admissibility", 0.5))
    goal_sharp = _normalize01(goal.get("goal_sharpness", 0.5))
    goal_stab = _normalize01(goal.get("goal_stability", 0.5))
    goal_cert = _normalize01(goal.get("goal_certainty", 0.5))
    evidence_conf = _normalize01(
        0.28 * gate
        + 0.14 * goal_cert
        + 0.10 * goal_stab
        + 0.10 * support_evidence
        + 0.12 * local_auth
        + 0.10 * carry
        - 0.08 * revision
        - 0.06 * nonlocal_auth
        + 0.06 * (1.0 - threshold)
    )
    candidate_sharpness = _normalize01(0.08 + 0.58 * evidence_conf + 0.12 * carry + 0.10 * local_auth - 0.12 * (1.0 - frac_tol))
    persistence_allowance = _normalize01(0.04 + 0.48 * gate * retain + 0.16 * goal_stab + 0.16 * carry + 0.08 * local_auth - 0.10 * revision)
    reopen_pressure = _normalize01(0.08 + 0.36 * (1.0 - gate) + 0.14 * (1.0 - frac_tol) + 0.10 * (1.0 - collapse) + 0.18 * revision + 0.14 * nonlocal_auth)
    low_evidence_sampling = _normalize01(0.05 + 0.30 * (1.0 - evidence_conf) + 0.12 * (1.0 - retain) + 0.20 * rival_breadth + 0.18 * nonlocal_auth + 0.10 * revision)
    contradiction_sensitivity = _normalize01(0.10 + 0.38 * (1.0 - frac_tol) + 0.16 * (1.0 - gate) + 0.18 * path_sens + 0.10 * revision + 0.08 * (1.0 - collapse_adm))
    return {
        "evidence_conf": evidence_conf,
        "candidate_sharpness": candidate_sharpness,
        "persistence_allowance": persistence_allowance,
        "reopen_pressure": reopen_pressure,
        "low_evidence_sampling": low_evidence_sampling,
        "contradiction_sensitivity": contradiction_sensitivity,
        "rival_breadth": rival_breadth,
        "nonlocal_authority": nonlocal_auth,
        "path_sensitivity": path_sens,
        "local_authority": local_auth,
        "support_carry_forward": carry,
        "revision_permissibility": revision,
        "collapse_admissibility": collapse_adm,
        "goal_sharp": goal_sharp,
        "goal_stab": goal_stab,
        "goal_cert": goal_cert,
    }


def _first_pass_candidate_features(cand: Dict[str, Any], ctrls: Dict[str, float]) -> Dict[str, Any]:
    """Compute first-pass public candidate features before relation/field/certificate enrichment."""
    visible_cue = _candidate_visible_cue(cand)
    line_support = _normalize01(cand.get("line_support", visible_cue))
    uncertainty = _normalize01(cand.get("uncertainty_hint", 0.0))
    novelty = _normalize01(cand.get("novelty_hint", 0.0))
    reversibility = _normalize01(cand.get("reversibility_hint", 1.0))
    coverage = _normalize01(cand.get("coverage_adequacy", 0.0))
    revisit_hint = _normalize01(cand.get("revisit_hint", 0.0))
    tested_hint = _normalize01(cand.get("tested_hint", coverage))
    obstruction = _normalize01(cand.get("obstruction_hint", 0.0))
    contradiction_hint = _normalize01(cand.get("contradiction_hint", 0.0))

    # Local support is intentionally thin: public visible cue, line/local action
    # support, and evidence quality.  It does not consume mature relation verdicts.
    local_support = _normalize01(
        0.54 * visible_cue
        + 0.20 * line_support
        + 0.14 * (1.0 - uncertainty)
        + 0.12 * tested_hint
    )
    cue_gap = _normalize01(abs(local_support - 0.5) * 2.0)
    evidence_quality = _normalize01(0.34 * coverage + 0.30 * tested_hint + 0.24 * (1.0 - uncertainty) + 0.12 * cue_gap)
    support_mass = _normalize01(0.52 * local_support + 0.24 * evidence_quality + 0.14 * tested_hint + 0.10 * cue_gap)

    burden_pressure = _normalize01(
        0.50 * contradiction_hint
        + 0.16 * obstruction
        + 0.14 * (1.0 - reversibility)
        + 0.10 * (1.0 - coverage)
        + 0.10 * max(0.0, 0.55 - local_support)
    )
    revisit_penalty = _normalize01(revisit_hint * (0.72 - 0.42 * support_mass - 0.16 * ctrls["local_authority"] + 0.24 * ctrls["rival_breadth"]))
    path_cost = _normalize01(
        0.30 * obstruction
        + 0.30 * burden_pressure
        + 0.14 * revisit_penalty
        + 0.12 * (1.0 - reversibility)
        + 0.08 * (1.0 - coverage)
        + 0.06 * max(0.0, 0.55 - local_support)
    )
    return {
        "action": cand.get("candidate_id"),
        "candidate_id": cand.get("candidate_id"),
        "continuation_id": cand.get("continuation_id"),
        "branch_id": cand.get("branch_id"),
        "continuation_memory_id": cand.get("continuation_memory_id"),
        "public_effects": _public_effects_from_candidate(cand),
        "visible_cue": visible_cue,
        "line_support": line_support,
        "uncertainty": uncertainty,
        "novelty": novelty,
        "reversibility": reversibility,
        "coverage": coverage,
        "revisit_hint": revisit_hint,
        "tested_hint": tested_hint,
        "obstruction": obstruction,
        "contradiction_hint": contradiction_hint,
        "local_support": local_support,
        "cue_gap": cue_gap,
        "evidence_quality": evidence_quality,
        "support_mass": support_mass,
        "burden_pressure": burden_pressure,
        "revisit_penalty": revisit_penalty,
        "path_cost": path_cost,
    }


def _candidate_state_rows(
    obs: Dict[str, Any],
    prims: Dict[str, Any],
    header: Any,
    tracker: ContinuationStateTracker | None = None,
    shape_field: DynamicShapeField | None = None,
    feedback: Dict[str, Any] | None = None,
    *,
    quotient_enabled: bool = True,
    recursion_scheduler_enabled: bool = True,
    sequence_composer: SequenceContinuationComposer | None = None,
    sequence_composition_enabled: bool = True,
) -> List[Dict[str, Any]]:
    """Build canonical candidate rows and carry branch-internal operation telemetry into RCF."""
    candidates = [dict(c) for c in list(obs.get("candidates") or []) if isinstance(c, dict)]
    if not candidates:
        return []
    goal = {}
    if isinstance(obs.get("goal_field"), dict):
        goal = dict(obs.get("goal_field") or {})
    base_ctrls = _geometry_controls(header, goal)
    ctrls = shape_field.effective_controls(base_ctrls) if shape_field is not None else dict(base_ctrls)
    if shape_field is not None and isinstance(prims, dict):
        prims["__dynamic_shape_state_before__"] = shape_field.state_dict()
        prims["__dynamic_shape_effective_controls__"] = dict(ctrls)
    runtime_feedback = feedback if isinstance(feedback, dict) else (dict(obs.get("feedback") or {}) if isinstance(obs.get("feedback"), dict) else None)
    scope = resolve_decision_scope(obs, prims, header)

    first: List[Dict[str, Any]] = []
    for cand in candidates:
        a = cand.get("candidate_id")
        if a is None or not bool(cand.get("legal", True)):
            continue
        first.append(_first_pass_candidate_features(cand, ctrls))
    if not first:
        return []

    avg_burden = sum(f["burden_pressure"] for f in first) / float(len(first))
    max_burden = max(f["burden_pressure"] for f in first)
    min_burden = min(f["burden_pressure"] for f in first)
    burden_spread = max(0.0, max_burden - min_burden)
    avg_uncertainty = sum(f["uncertainty"] for f in first) / float(len(first))
    burden_context = _normalize01(0.50 * max_burden + 0.30 * avg_burden + 0.20 * burden_spread)

    continuation_updates: List[Dict[str, float]] = []
    continuation_memory_meta: List[Tuple[Any, str]] = []
    if tracker is not None:
        batch_items = []
        for f in first:
            mem_id, mem_source = derive_continuation_memory_id(f)
            fracture_for_memory = _normalize01(
                (0.54 * f["path_cost"] + 0.34 * f["burden_pressure"] + 0.12 * max(0.0, f["burden_pressure"] - avg_burden))
                * (0.45 + 0.55 * ctrls["contradiction_sensitivity"])
            )
            continuation_memory_meta.append((mem_id, mem_source))
            batch_items.append((mem_id, {"support": f["support_mass"], "burden": f["burden_pressure"], "fracture": fracture_for_memory, "uncertainty": f["uncertainty"]}))
        continuation_updates = tracker.update_candidate_batch(batch_items)

    rows: List[Dict[str, Any]] = []
    for idx, f in enumerate(first):
        visible_cue = f["visible_cue"]
        uncertainty = f["uncertainty"]
        novelty = f["novelty"]
        reversibility = f["reversibility"]
        coverage = f["coverage"]
        tested_hint = f["tested_hint"]
        revisit_hint = f["revisit_hint"]
        local_support = f["local_support"]
        support_mass = f["support_mass"]
        cue_gap = f["cue_gap"]
        burden_pressure = f["burden_pressure"]
        path_cost = f["path_cost"]

        cue_trust = _normalize01(
            0.14
            + 0.34 * ctrls["local_authority"]
            + 0.16 * ctrls["evidence_conf"]
            + 0.12 * tested_hint
            + 0.10 * coverage
            - 0.18 * ctrls["nonlocal_authority"]
            - 0.10 * ctrls["rival_breadth"]
        )
        hidden_probe = _normalize01(
            (1.0 - cue_gap)
            * (0.40 * ctrls["nonlocal_authority"] + 0.30 * ctrls["rival_breadth"] + 0.20 * uncertainty + 0.10 * (1.0 - tested_hint))
        )

        exploit_pref = _normalize01(0.10 + 0.42 * ctrls["evidence_conf"] + 0.30 * ctrls["local_authority"] + 0.24 * ctrls["support_carry_forward"])
        probe_pref = _normalize01(0.04 + 0.38 * ctrls["low_evidence_sampling"] + 0.30 * ctrls["rival_breadth"] + 0.24 * ctrls["nonlocal_authority"] + 0.12 * ctrls["revision_permissibility"])
        caution_pref = _normalize01(0.08 + 0.42 * ctrls["path_sensitivity"] + 0.24 * ctrls["contradiction_sensitivity"] + 0.10 * ctrls["support_carry_forward"] + 0.10 * ctrls["evidence_conf"])

        # Generic preventive support: when the candidate set contains active
        # burden, a lower-burden candidate with enough evidence quality gains
        # continuation support.  This is relative to the candidate set and does
        # not know action labels, family names, thresholds, or optimal policies.
        burden_relief = _normalize01(max(0.0, burden_context - burden_pressure))
        relief_gate = _normalize01(
            (0.30 + 0.70 * ctrls["path_sensitivity"])
            * (0.35 + 0.65 * ctrls["nonlocal_authority"])
            * (0.40 + 0.60 * f["evidence_quality"])
            * (0.40 + 0.35 * reversibility + 0.25 * support_mass)
        )
        preventive_support = _normalize01(burden_relief * relief_gate)

        exploit_component = _normalize01(
            0.38 * local_support * cue_trust
            + 0.24 * support_mass
            + 0.14 * tested_hint
            + 0.10 * coverage
            + 0.08 * (1.0 - uncertainty)
            + 0.06 * visible_cue
        )
        probe_component = _normalize01(
            0.28 * uncertainty
            + 0.20 * novelty
            + 0.18 * reversibility
            + 0.14 * (1.0 - tested_hint)
            + 0.12 * hidden_probe
            + 0.08 * (1.0 - local_support)
        )
        if scope == "hypothesis_over_anchor":
            probe_component = _normalize01(0.32 * uncertainty + 0.24 * novelty + 0.20 * reversibility + 0.10 * (1.0 - coverage) + 0.14 * hidden_probe)
            caution_pref = _normalize01(0.10 + 0.32 * ctrls["path_sensitivity"] + 0.20 * ctrls["contradiction_sensitivity"] + 0.18 * ctrls["support_carry_forward"])

        nonlocal_bonus = _normalize01(ctrls["nonlocal_authority"] * reversibility * (0.45 * uncertainty + 0.30 * novelty + 0.25 * (1.0 - cue_gap)) * (0.60 + 0.40 * (1.0 - support_mass)))
        local_bonus = _normalize01(ctrls["local_authority"] * exploit_component * (0.50 + 0.30 * tested_hint + 0.20 * visible_cue))
        support_bonus = _normalize01(ctrls["support_carry_forward"] * support_mass * (0.50 + 0.50 * tested_hint))

        fracture_state = _normalize01((0.54 * path_cost + 0.34 * burden_pressure + 0.12 * max(0.0, burden_pressure - avg_burden)) * (0.45 + 0.55 * ctrls["contradiction_sensitivity"]))
        if tracker is not None:
            continuation = dict(continuation_updates[idx])
            continuation_memory_id, continuation_memory_source = continuation_memory_meta[idx]
        else:
            continuation_memory_id, continuation_memory_source = derive_continuation_memory_id(f)
            continuation = {
                "continuation_age": 1.0,
                "support_persistence": support_mass,
                "burden_accumulation": burden_pressure,
                "burden_trend": 0.0,
                "fracture_trend": 0.0,
                "support_decay": 0.0,
                "continuation_instability": _normalize01(0.50 * burden_pressure + 0.30 * fracture_state + 0.20 * uncertainty),
                "continuation_viability": _normalize01(0.48 * support_mass + 0.24 * (1.0 - burden_pressure) + 0.18 * (1.0 - fracture_state) + 0.10 * (1.0 - uncertainty)),
                "support_ema": support_mass,
                "burden_ema": burden_pressure,
                "fracture_ema": fracture_state,
            }
        continuation_viability = _normalize01(continuation.get("continuation_viability", support_mass))
        continuation_instability = _normalize01(continuation.get("continuation_instability", burden_pressure))
        burden_accumulation = _normalize01(continuation.get("burden_accumulation", burden_pressure))
        burden_trend = _normalize01(continuation.get("burden_trend", 0.0))
        support_persistence = _normalize01(continuation.get("support_persistence", support_mass))

        stability_under_change = _normalize01(
            0.24 * support_mass
            + 0.22 * (1.0 - burden_pressure) * (0.45 + 0.55 * ctrls["path_sensitivity"])
            + 0.16 * reversibility
            + 0.10 * coverage
            + 0.08 * preventive_support
            + 0.22 * continuation_viability
            - 0.12 * continuation_instability
        )

        base_state = _normalize01(
            0.44 * exploit_pref * exploit_component
            + 0.22 * probe_pref * probe_component
            + 0.16 * nonlocal_bonus
            + 0.14 * local_bonus
            + 0.12 * support_bonus
            + 0.18 * preventive_support
            + 0.10 * visible_cue * cue_trust
            + 0.10 * continuation_viability
            - 0.25 * caution_pref * path_cost
            - 0.05 * ctrls["path_sensitivity"] * burden_accumulation
        )
        persistence_state = _normalize01(
            (0.30 * exploit_component + 0.24 * stability_under_change + 0.18 * support_persistence + 0.14 * continuation_viability + 0.08 * reversibility + 0.06 * preventive_support)
            * ctrls["persistence_allowance"]
        )
        salience_state = _normalize01(
            (0.34 * probe_component + 0.20 * novelty + 0.14 * uncertainty + 0.14 * hidden_probe + 0.08 * avg_uncertainty + 0.10 * continuation_instability)
            * ctrls["low_evidence_sampling"]
        )
        decision_state = _normalize01(
            0.42 * base_state
            + 0.18 * persistence_state
            + 0.14 * salience_state
            + 0.14 * preventive_support
            + 0.14 * stability_under_change
            + 0.08 * continuation_viability
            - 0.30 * fracture_state
            - 0.06 * ctrls["path_sensitivity"] * burden_accumulation
            - 0.03 * ctrls["nonlocal_authority"] * burden_trend
        )

        rows.append({
            "action": f["action"],
            "candidate_id": f["action"],
            "continuation_memory_id": continuation_memory_id,
            "continuation_memory_source": continuation_memory_source,
            "continuation_memory_shared_count": _normalize01(float(continuation.get("continuation_memory_shared_count", 1.0)) / 8.0),
            "public_effects": list(f.get("public_effects") or []),
            "support_mass": support_mass,
            "local_support": local_support,
            "exploit_component": exploit_component,
            "probe_component": probe_component,
            "path_cost": path_cost,
            "support_conf": base_state,
            "continuity": persistence_state,
            "uncertainty": uncertainty,
            "novelty": novelty,
            "contradiction": fracture_state,
            "contradiction_burden": fracture_state,
            "raw_burden_hint": f["contradiction_hint"],
            "burden_pressure": burden_pressure,
            "burden_relief": burden_relief,
            "preventive_support": preventive_support,
            "stability_under_change": stability_under_change,
            "continuation_viability": continuation_viability,
            "continuation_instability": continuation_instability,
            "burden_accumulation": burden_accumulation,
            "burden_trend": burden_trend,
            "fracture_trend": _normalize01(continuation.get("fracture_trend", 0.0)),
            "support_decay": _normalize01(continuation.get("support_decay", 0.0)),
            "support_persistence": support_persistence,
            "continuation_age": _normalize01(float(continuation.get("continuation_age", 1.0)) / 12.0),
            "sampling_demand": salience_state,
            "commitment_stability": persistence_state,
            "recent_mean": 0.0,
            "probe_debt": revisit_hint,
            "revisit_hint": revisit_hint,
            "coverage": coverage,
            "base_state": base_state,
            "persistence_state": persistence_state,
            "salience_state": salience_state,
            "fracture_state": fracture_state,
            "decision_state": decision_state,
            "dynamic_shape_effective_controls": dict(ctrls) if shape_field is not None else {},
            "dynamic_shape_controls_active": bool(shape_field is not None),
        })
    for row, f in zip(rows, first):
        if f.get("continuation_id") is not None:
            row["continuation_id"] = f.get("continuation_id")
        if f.get("branch_id") is not None:
            row["branch_id"] = f.get("branch_id")
    # Kernel-side RelationSurface: derive continuation identities and branch
    # relations from public burden/effect facts before RCF.  This closes the
    # prior gap where RCF could consume relations but candidate publication did
    # not derive them from public structure.
    rows, relations, relation_telemetry = apply_relation_surface(rows, ctrls, quotient_enabled=quotient_enabled)
    sequence_telemetry: Dict[str, Any] = {"sequence_composer_enabled": False, "sequence_transitions_accepted": 0}
    if sequence_composition_enabled and sequence_composer is not None:
        rows, sequence_telemetry = sequence_composer.apply(rows, feedback=runtime_feedback, controls=ctrls)
    else:
        for _row in rows:
            _row.setdefault("continuation_phase", "disabled")
            _row.setdefault("sequence_composition_active", False)
            _row.setdefault("sequence_composition_support", 0.0)
            _row.setdefault("sequence_phase_transition", "")
            _row.setdefault("sequence_composition_disabled", True)
        sequence_telemetry = {"sequence_composer_enabled": False, "sequence_transitions_accepted": 0, "sequence_disabled_for_ablation": True}
    out_rows = apply_continuation_field(rows, ctrls, relations=relations)
    # First-pass recursion scheduler: derive bounded public structural recursion
    # demand before certificates gate collapse.  This is telemetry/control
    # pressure, not hidden lookahead or action selection.
    if recursion_scheduler_enabled:
        out_rows = apply_recursion_scheduler(out_rows, relations=relations, controls=ctrls)
    else:
        for _row in out_rows:
            _row["recursion_scheduler_disabled"] = True
            _row.setdefault("recursion_scheduler_demand", 0.0)
            _row.setdefault("recursion_scheduler_budget", 0)
            _row.setdefault("recursion_scheduler_mode", "disabled")
            _row.setdefault("recursion_scheduler_reasons", ["disabled_for_ablation"])
    out_rows = apply_collapse_certificates(out_rows, relations=relations, controls=ctrls)
    dynamic_shape_update = None
    if shape_field is not None:
        dynamic_shape_update = shape_field.update(rows=out_rows, relations=relations, observation=obs, feedback=runtime_feedback)
        if isinstance(prims, dict):
            prims["__dynamic_shape_state__"] = shape_field.state_dict()
            prims["__dynamic_shape_update__"] = dict(dynamic_shape_update)
            prims["__dynamic_shape_enabled__"] = True
    for row in out_rows:
        row["relation_surface_telemetry"] = relation_telemetry
        row["sequence_composition_telemetry"] = dict(sequence_telemetry)
        if shape_field is not None:
            row["dynamic_shape_state_before"] = prims.get("__dynamic_shape_state_before__", {}) if isinstance(prims, dict) else {}
            row["dynamic_shape_state_after"] = shape_field.state_dict()
            row["dynamic_shape_update"] = dict(dynamic_shape_update or {})
            domain = row.get("relation_field_domain", "")
            row["dynamic_shape_domain_coarseness"] = shape_field.domain_coarseness_for(domain)
            row["dynamic_shape_domain_coarseness_domain"] = str(domain or "")
    return out_rows


def _candidate_publication_votes(
    obs: Dict[str, Any],
    prims: Dict[str, Any],
    header: Any,
    tracker: ContinuationStateTracker | None = None,
    shape_field: DynamicShapeField | None = None,
    feedback: Dict[str, Any] | None = None,
    *,
    quotient_enabled: bool = True,
    recursion_scheduler_enabled: bool = True,
    sequence_composer: SequenceContinuationComposer | None = None,
    sequence_composition_enabled: bool = True,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    rows = _candidate_state_rows(
        obs,
        prims,
        header,
        tracker=tracker,
        shape_field=shape_field,
        feedback=feedback,
        quotient_enabled=quotient_enabled,
        recursion_scheduler_enabled=recursion_scheduler_enabled,
        sequence_composer=sequence_composer,
        sequence_composition_enabled=sequence_composition_enabled,
    )
    if not rows:
        return [], []
    votes: List[Dict[str, Any]] = []
    for row in rows:
        a = row["action"]
        votes.append({"action": a, "weight": max(0.0, row["base_state"]), "scope": "base", "source": "candidate_surface/publication"})
        votes.append({"action": a, "weight": max(0.0, row["persistence_state"]), "scope": "persistence", "source": "candidate_surface/publication"})
        votes.append({"action": a, "weight": max(0.0, row["salience_state"]), "scope": "salience", "source": "candidate_surface/publication"})
        votes.append({"action": a, "weight": max(0.0, row["fracture_state"]), "scope": "fracture", "source": "candidate_surface/publication"})
    return votes, rows


class CandidateEvidenceSurface:
    """Pipeline surface that publishes candidate rows/votes for downstream CO runtime stages."""
    PRIMITIVE_DEPS = ("signal_bus (optional)",)
    COMBINATOR_DEPS = ()
    FORMULA_STATUS = "working"

    def __init__(
        self,
        max_continuations: int = 256,
        continuation_alpha: float = 0.42,
        dynamic_shape_enabled: bool = True,
        dynamic_shape_alpha: float = 0.35,
        quotient_enabled: bool = True,
        recursion_scheduler_enabled: bool = True,
        sequence_composition_enabled: bool = True,
    ) -> None:
        self._continuation_tracker = ContinuationStateTracker(max_entries=max_continuations, alpha=continuation_alpha)
        self.dynamic_shape_enabled = bool(dynamic_shape_enabled)
        self.quotient_enabled = bool(quotient_enabled)
        self.recursion_scheduler_enabled = bool(recursion_scheduler_enabled)
        self.sequence_composition_enabled = bool(sequence_composition_enabled)
        self._sequence_composer = SequenceContinuationComposer() if self.sequence_composition_enabled else None
        self._dynamic_shape_field = DynamicShapeField(alpha=dynamic_shape_alpha) if self.dynamic_shape_enabled else None

    def update(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None) -> Dict[str, Any]:
        return {}

    def step(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None = None) -> Dict[str, Any]:
        bus = primitives.get("signal_bus") if isinstance(primitives, dict) else None
        if bus is None or not hasattr(bus, "publish"):
            return {
                "candidate_surface_published": 0,
                "candidate_publication_rows": 0,
                "co_evidence_valid_for_step": False,
                "candidate_surface_contract_violation": "missing_signal_bus",
                "forbidden_fallback_avoided": True,
            }
        try:
            votes, rows = _candidate_publication_votes(
                observation,
                primitives,
                header,
                tracker=self._continuation_tracker,
                shape_field=self._dynamic_shape_field,
                feedback=feedback,
                quotient_enabled=self.quotient_enabled,
                recursion_scheduler_enabled=self.recursion_scheduler_enabled,
                sequence_composer=self._sequence_composer,
                sequence_composition_enabled=self.sequence_composition_enabled,
            )
            primitives["__candidate_publication_rows__"] = list(rows)
            primitives["__continuation_state_snapshots__"] = self._continuation_tracker.snapshots()
            if not votes:
                # Canonical CO must fail closed rather than invent a uniform
                # action proposal.  Nonclosure has to be represented by actual
                # candidate/burden/relation structure upstream, not by a silent
                # first-legal or uniform rescue at the intake surface.
                primitives["__candidate_surface_contract_violation__"] = {
                    "reason": "no_candidate_votes_published",
                    "co_evidence_valid_for_step": False,
                    "forbidden_fallback_avoided": True,
                }
                return {
                    "candidate_surface_published": 0,
                    "candidate_publication_rows": int(len(rows)),
                    "signal_bus_size": bus.size(scope_key=resolve_decision_scope(observation, primitives, header)) if hasattr(bus, "size") else 0,
                    "co_evidence_valid_for_step": False,
                    "candidate_surface_contract_violation": "no_candidate_votes_published",
                }
            scope_key = resolve_decision_scope(observation, primitives, header)
            for v in votes:
                bus.publish(scope_key=scope_key, action=v["action"], weight=v["weight"], channel=v.get("scope"), source=v.get("source"))
            size = bus.size(scope_key=scope_key) if hasattr(bus, "size") else len(votes)
            return {"candidate_surface_published": int(len(votes)), "candidate_publication_rows": int(len(rows)), "signal_bus_size": int(size)}
        except Exception as e:
            raise RuntimeError(f"CandidateEvidenceSurface failed without fallback: {e}") from e

    def metrics(self) -> Dict[str, Any]:
        return {}
