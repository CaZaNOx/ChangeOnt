"""First-pass generic sequence-level continuation composition.

This helper composes public phase transitions across runtime steps without
reading problem-family names, native action meanings, hidden state, rewards, or
baseline values.  It is deliberately narrow: it uses prior selected interface
identity only to find the previously committed row, then derives all sequence
semantics from public burden/effect operations and current row telemetry.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Hashable, Iterable, List, Mapping, Optional, Sequence, Tuple

from agents.co.runtime.surfaces.continuation_field import BranchRelation, clamp01
from agents.co.runtime.surfaces.relation_surface import branch_key_from_row

_ALLOWED_PUBLIC_BASES = {
    "visible_observation",
    "declared_transition_rule",
    "legal_constraint",
    "public_cost",
    "public_history",
    "parity_honest_uncertainty",
    "kernel_history",
    "problem_contract",
}
_ALLOWED_LEAKAGE = {"public", "parity_honest", "kernel_history", "investigatory"}
_FORBIDDEN_LEAKAGE = {"forbidden", "hidden_policy", "optimal_policy", "oracle", "baseline_value", "hidden", "solver", "policy", "dp", "private"}

_CARRY = {"carry", "increase", "amplify", "consume", "require", "mask", "postpone", "hide", "threshold", "phase_shift"}
_EXPOSE = {"reveal", "expose", "reduce_hiddenness"}
_RELIEVE = {"reduce", "relieve", "prevent", "reset", "cancel", "buffer", "absorb"}
_TRANSFER = {"transfer", "transform"}
_DECISION_SLOT = {"decision_slot", "single_decision_slot", "slot", "compete", "competition"}

_ALIASES = {
    "relieves": "relieve",
    "relief": "relieve",
    "reduces": "reduce",
    "decrease": "reduce",
    "decreases": "reduce",
    "preventive": "prevent",
    "prevents": "prevent",
    "reveals": "reveal",
    "exposes": "expose",
    "resets": "reset",
    "cancels": "cancel",
    "buffers": "buffer",
    "absorbs": "absorb",
    "carries": "carry",
    "postpones": "postpone",
    "decision-slot": "decision_slot",
    "single_decision_slot": "decision_slot",
    "phase-shift": "phase_shift",
}


def _key(value: Any) -> Hashable:
    try:
        hash(value)
        return value  # type: ignore[return-value]
    except Exception:
        return repr(value)


def _txt(value: Any, default: str = "") -> str:
    out = "" if value is None else str(value).strip().lower()
    return out if out else default


def _op(value: Any) -> str:
    out = _txt(value, "unknown")
    return _ALIASES.get(out, out)


def _public_effects(value: Any) -> List[Mapping[str, Any]]:
    if isinstance(value, Mapping):
        return [value]
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
        return [v for v in value if isinstance(v, Mapping)]
    return []


def _is_public(raw: Mapping[str, Any]) -> bool:
    leakage = _txt(raw.get("leakage_status", "public"), "public")
    basis = _txt(raw.get("public_basis"), "")
    return leakage not in _FORBIDDEN_LEAKAGE and leakage in _ALLOWED_LEAKAGE and basis in _ALLOWED_PUBLIC_BASES


def _effect_domain(raw: Mapping[str, Any]) -> Tuple[str, str, str, str]:
    burden = _txt(raw.get("burden_type", raw.get("type", raw.get("effect_type", ""))), "")
    relation_scope = _txt(raw.get("relation_scope", raw.get("resource", raw.get("resource_type", raw.get("scope", "")))), "")
    scope = _txt(raw.get("scope"), relation_scope or "candidate")
    coupling = _txt(raw.get("coupling"), relation_scope or scope or "uncoupled")
    domain = burden or relation_scope or scope
    return coupling or "uncoupled", scope or "candidate", domain or "unknown", relation_scope or ""


def _magnitude(raw: Mapping[str, Any]) -> float:
    return clamp01(raw.get("magnitude", raw.get("weight", 1.0)), 1.0) * clamp01(raw.get("confidence", 1.0), 1.0)


@dataclass(frozen=True)
class PhaseSignature:
    """Public phase signature for one branch row."""

    branch_id: Hashable
    phase: str
    domain_key: str
    coupling: str
    scope: str
    domain: str
    relation_scope: str
    expose: float
    relieve: float
    carry: float
    stabilize: float
    transfer: float
    hidden: float
    support: float
    burden: float
    source: str = "public_effects"

    def to_dict(self) -> Dict[str, Any]:
        out = asdict(self)
        out["branch_id"] = str(self.branch_id)
        return out


@dataclass(frozen=True)
class SequenceTransition:
    """Accepted sequence transition from a previous public phase to a current phase."""

    previous: PhaseSignature
    current: PhaseSignature
    transition: str
    compatibility: float
    support: float
    reason: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "previous": self.previous.to_dict(),
            "current": self.current.to_dict(),
            "transition": self.transition,
            "compatibility": float(self.compatibility),
            "support": float(self.support),
            "reason": self.reason,
        }


def derive_phase_signature(row: Mapping[str, Any]) -> PhaseSignature:
    """Derive a public phase signature from one relation-enriched row."""
    branch_id = branch_key_from_row(row)
    expose = clamp01(row.get("branch_internal_exposure_support", 0.0))
    relieve = clamp01(max(
        row.get("branch_internal_relief_support", 0.0),
        row.get("branch_internal_cancellation_support", 0.0),
        row.get("branch_internal_buffering_support", 0.0),
        row.get("branch_internal_resolver_support", 0.0),
        row.get("burden_relief", 0.0),
        row.get("preventive_support", 0.0),
    ))
    carry = clamp01(max(
        row.get("branch_internal_unresolved_pressure", 0.0),
        row.get("branch_internal_raw_carry_pressure", 0.0),
        row.get("branch_internal_masking_pressure", 0.0),
        row.get("branch_internal_threshold_pressure", 0.0),
        row.get("burden_pressure", 0.0),
    ))
    transfer = clamp01(row.get("branch_internal_transform_pressure", 0.0))
    hidden = clamp01(max(row.get("branch_internal_hiddenness_pressure", 0.0), row.get("uncertainty", 0.0)))
    support = clamp01(max(row.get("field_viability", 0.0), row.get("continuation_viability", 0.0), row.get("support_mass", 0.0), row.get("decision_state", 0.0)))
    burden = clamp01(max(row.get("field_debt", 0.0), row.get("burden_accumulation", 0.0), row.get("burden_pressure", 0.0)))
    stabilize = clamp01((0.44 * support + 0.34 * (1.0 - burden) + 0.22 * clamp01(row.get("stability_under_change", support))) * (1.0 - 0.40 * carry))

    chosen_domain: Tuple[float, Tuple[str, str, str, str]] | None = None
    for raw in _public_effects(row.get("public_effects", row.get("burden_effects", row.get("effect_facts", [])))):
        if not _is_public(raw):
            continue
        op = _op(raw.get("operation", raw.get("op", raw.get("effect", "unknown"))))
        if op in _DECISION_SLOT:
            continue
        raw_weight = _magnitude(raw)
        if op in _EXPOSE:
            expose = max(expose, raw_weight)
            weight = raw_weight * 1.08
        elif op in _RELIEVE:
            relieve = max(relieve, raw_weight)
            weight = raw_weight * 1.04
        elif op in _CARRY:
            carry = max(carry, raw_weight)
            weight = raw_weight * 1.00
        elif op in _TRANSFER:
            transfer = max(transfer, raw_weight)
            weight = raw_weight * 0.82
        else:
            weight = raw_weight * 0.74
        dom = _effect_domain(raw)
        if chosen_domain is None or weight > chosen_domain[0]:
            chosen_domain = (weight, dom)
    if chosen_domain is not None:
        coupling, scope, domain, relation_scope = chosen_domain[1]
        domain_key = "::".join([coupling, scope, domain])
        source = "public_effects"
    else:
        mem = row.get("continuation_memory_id", row.get("continuation_id", branch_id))
        domain_key = str(mem)
        coupling, scope, domain, relation_scope = "memory", "candidate", domain_key, ""
        source = "continuation_memory"

    # Explicit public effect operations carry the phase identity.  A high
    # local stability score should not erase a branch's public role as exposure,
    # relief, or carried burden; otherwise sequence composition collapses back
    # into one-step scoring.  Stabilize is therefore reserved for rows with no
    # active public transform/relief/carry role or after relief has made burden
    # genuinely low.
    if expose >= 0.18 and expose >= 0.55 * max(relieve, carry):
        phase = "expose"
    elif relieve >= 0.18 and relieve >= 0.42 * carry:
        phase = "relieve"
    elif carry >= 0.18:
        phase = "carry"
    elif transfer >= 0.18:
        phase = "transform"
    elif stabilize >= 0.22:
        phase = "stabilize"
    else:
        phase = "neutral"
    if phase == "relieve" and burden <= 0.18 and stabilize >= 0.46:
        phase = "stabilize"
    return PhaseSignature(
        branch_id=branch_id,
        phase=phase,
        domain_key=domain_key,
        coupling=coupling,
        scope=scope,
        domain=domain,
        relation_scope=relation_scope,
        expose=clamp01(expose),
        relieve=clamp01(relieve),
        carry=clamp01(carry),
        stabilize=clamp01(stabilize),
        transfer=clamp01(transfer),
        hidden=clamp01(hidden),
        support=clamp01(support),
        burden=clamp01(burden),
        source=source,
    )


def _domain_compatibility(prev: PhaseSignature, cur: PhaseSignature) -> float:
    if prev.domain_key == cur.domain_key:
        return 1.0
    score = 0.0
    if prev.coupling and cur.coupling and prev.coupling == cur.coupling:
        score = max(score, 0.78)
    if prev.scope and cur.scope and prev.scope == cur.scope:
        score = max(score, 0.64)
    if prev.relation_scope and cur.relation_scope and prev.relation_scope == cur.relation_scope:
        score = max(score, 0.72)
    # Exposure can lawfully open a different burden domain under the same local
    # packet/scope when what changed is public hiddenness/exposure, not a native
    # action template.  Keep this below exact-domain compatibility.
    if prev.phase == "expose" and cur.phase in {"relieve", "stabilize"} and prev.hidden >= 0.22:
        if prev.scope == cur.scope or prev.coupling == cur.coupling:
            score = max(score, 0.58)
    return clamp01(score)


def derive_sequence_transition(previous: Optional[PhaseSignature], current: PhaseSignature) -> Optional[SequenceTransition]:
    """Return an accepted generic sequence transition if public phase structure warrants it."""
    if previous is None:
        return None
    if current.phase in {"neutral", "carry", "transform"}:
        return None
    compatibility = _domain_compatibility(previous, current)
    if compatibility < 0.50:
        return None

    transition = f"{previous.phase}_to_{current.phase}"
    reason = ""
    base = 0.0
    if previous.phase in {"carry", "neutral"} and current.phase == "expose" and current.expose >= 0.18:
        base = 0.38 * current.expose + 0.24 * previous.carry + 0.18 * current.hidden + 0.20 * current.support
        reason = "carried_or_unresolved_burden_to_public_exposure"
    elif previous.phase == "carry" and current.phase == "relieve" and current.relieve >= 0.18:
        base = 0.36 * current.relieve + 0.26 * previous.carry + 0.18 * compatibility + 0.20 * current.support
        reason = "carried_burden_to_direct_relief"
    elif previous.phase == "expose" and current.phase == "relieve" and current.relieve >= 0.18:
        base = 0.40 * current.relieve + 0.24 * previous.expose + 0.18 * compatibility + 0.18 * current.support
        reason = "public_exposure_to_burden_relief"
    elif previous.phase in {"relieve", "expose"} and current.phase == "stabilize" and current.stabilize >= 0.34:
        base = 0.42 * current.stabilize + 0.20 * previous.relieve + 0.18 * previous.expose + 0.20 * (1.0 - current.burden)
        reason = "resolution_phase_to_stabilized_continuation"
    elif previous.phase == "relieve" and current.phase == "relieve" and current.relieve >= 0.28:
        base = 0.36 * current.relieve + 0.28 * previous.relieve + 0.18 * compatibility + 0.18 * current.support
        reason = "continued_burden_relief_phase"
    else:
        return None
    support = clamp01(base * (0.55 + 0.45 * compatibility))
    if support < 0.12:
        return None
    return SequenceTransition(previous=previous, current=current, transition=transition, compatibility=compatibility, support=support, reason=reason)


class SequenceContinuationComposer:
    """Stateful first-pass public sequence composer.

    The composer stores only prior public row signatures and uses feedback action
    solely as an interface handle to identify which previously published row was
    committed.  It never interprets the action string.
    """

    def __init__(self, alpha: float = 0.40) -> None:
        self.alpha = clamp01(alpha, 0.40)
        self._previous_rows_by_action: Dict[Hashable, Dict[str, Any]] = {}
        self._last_selected_phase: Optional[PhaseSignature] = None
        self._sequence_support_ema: Dict[str, float] = {}
        self._tick = 0

    def _observe_feedback(self, feedback: Optional[Mapping[str, Any]]) -> None:
        if not isinstance(feedback, Mapping):
            return
        if "action" not in feedback:
            return
        key = _key(feedback.get("action"))
        prior = self._previous_rows_by_action.get(key)
        if prior is None:
            return
        self._last_selected_phase = derive_phase_signature(prior)

    def apply(
        self,
        rows: Sequence[Mapping[str, Any]],
        *,
        feedback: Optional[Mapping[str, Any]] = None,
        controls: Optional[Mapping[str, Any]] = None,
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        self._observe_feedback(feedback)
        out: List[Dict[str, Any]] = []
        accepted = 0
        phases: Dict[str, int] = {}
        samples: List[Dict[str, Any]] = []
        path_sens = clamp01((controls or {}).get("path_sensitivity", 0.5), 0.5)
        revision = clamp01((controls or {}).get("revision_permissibility", 0.5), 0.5)
        nonlocal_auth = clamp01((controls or {}).get("nonlocal_authority", 0.5), 0.5)
        sequence_gain = clamp01(0.32 + 0.24 * path_sens + 0.22 * revision + 0.22 * nonlocal_auth)
        prev = self._last_selected_phase
        current_signatures = [derive_phase_signature(r) for r in rows]

        def _current_topology_transition(cur: PhaseSignature) -> Optional[SequenceTransition]:
            best: Optional[SequenceTransition] = None
            for prior in current_signatures:
                if prior.branch_id == cur.branch_id:
                    continue
                candidate = derive_sequence_transition(prior, cur)
                if candidate is None:
                    continue
                # Current-set topology is weaker than observed selected sequence:
                # it marks lawful public phase adjacency, not an executed plan.
                attenuated = SequenceTransition(
                    previous=candidate.previous,
                    current=candidate.current,
                    transition=candidate.transition,
                    compatibility=candidate.compatibility,
                    support=clamp01(0.62 * candidate.support),
                    reason="current_candidate_phase_topology::" + candidate.reason,
                )
                if best is None or attenuated.support > best.support:
                    best = attenuated
            return best

        for raw, cur in zip(rows, current_signatures):
            row = dict(raw)
            phases[cur.phase] = phases.get(cur.phase, 0) + 1
            trans = derive_sequence_transition(prev, cur)
            if trans is None:
                trans = _current_topology_transition(cur)
            row["continuation_phase"] = cur.phase
            row["sequence_phase_signature"] = cur.to_dict()
            row["sequence_composition_active"] = False
            row["sequence_composition_support"] = 0.0
            row["sequence_phase_transition"] = ""
            if trans is not None:
                seq_id = f"sequence::{trans.transition}::{cur.domain_key}"
                prior_ema = self._sequence_support_ema.get(seq_id, 0.0)
                support = clamp01((1.0 - self.alpha) * prior_ema + self.alpha * trans.support)
                self._sequence_support_ema[seq_id] = support
                row["sequence_composition_active"] = True
                row["sequence_composition_id"] = seq_id
                row["sequence_continuation_id"] = seq_id
                row["ordered_continuation_id"] = seq_id
                row["sequence_phase_transition"] = trans.transition
                row["sequence_previous_phase"] = trans.previous.phase
                row["sequence_domain_compatibility"] = float(trans.compatibility)
                row["sequence_composition_support"] = float(support)
                row["sequence_composition_reason"] = trans.reason
                row["sequence_composition_basis"] = "selected_feedback" if not str(trans.reason).startswith("current_candidate_phase_topology::") else "current_candidate_phase_topology"
                # Bounded generic coupling into existing surfaces.  The sequence
                # layer does not choose the action; it slightly raises generic
                # relief/continuity channels when public phase progression is
                # coherent under the current shape gauge.
                boost = clamp01(support * sequence_gain)
                row["preventive_support"] = clamp01(row.get("preventive_support", 0.0) + 0.10 * boost)
                row["branch_internal_resolver_support"] = clamp01(max(row.get("branch_internal_resolver_support", 0.0), 0.62 * boost))
                row["branch_internal_relief_support"] = clamp01(max(row.get("branch_internal_relief_support", 0.0), 0.46 * boost if cur.phase in {"relieve", "stabilize"} else row.get("branch_internal_relief_support", 0.0)))
                row["support_persistence"] = clamp01(row.get("support_persistence", 0.0) + 0.06 * boost)
                row["continuation_viability"] = clamp01(row.get("continuation_viability", 0.0) + 0.06 * boost)
                row["stability_under_change"] = clamp01(row.get("stability_under_change", 0.0) + (0.07 * boost if cur.phase == "stabilize" else 0.03 * boost))
                row["decision_state"] = clamp01(row.get("decision_state", 0.0) + 0.04 * boost)
                accepted += 1
                if len(samples) < 8:
                    samples.append(trans.to_dict())
            out.append(row)
        self._previous_rows_by_action = {_key(r.get("action")): dict(r) for r in out if r.get("action") is not None}
        self._tick += 1
        telemetry = {
            "sequence_composer_enabled": True,
            "sequence_previous_phase_available": prev is not None,
            "sequence_rows": len(out),
            "sequence_transitions_accepted": accepted,
            "sequence_phase_counts": dict(phases),
            "sequence_transition_samples": samples,
        }
        return out, telemetry
