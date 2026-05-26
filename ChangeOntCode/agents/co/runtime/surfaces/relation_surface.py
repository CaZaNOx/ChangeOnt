"""Kernel-side RelationSurface.

Implements ``80_KERNEL_SIDE_RELATION_SURFACE_CONTRACT.md`` and
``87_RELATION_SURFACE_PUBLIC_EFFECT_IMPLEMENTATION.md``.  Adapters publish
public burden/effect facts; this module derives relations kernel-side and keeps
weak decision-slot competition separate from structural rivalry.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, asdict
from typing import Any, Dict, Hashable, Iterable, List, Mapping, Sequence, Tuple

from agents.co.runtime.surfaces.continuation_field import BranchRelation, clamp01
from agents.co.runtime.surfaces.quotient_equivalence import derive_quotient_equivalence
from agents.co.runtime.surfaces.relation_field_concentration import derive_relation_field_concentration


ALLOWED_PUBLIC_BASES = {
    "visible_observation",
    "declared_transition_rule",
    "legal_constraint",
    "public_cost",
    "public_history",
    "parity_honest_uncertainty",
    "kernel_history",
    "problem_contract",
}

ALLOWED_LEAKAGE_STATUS = {"public", "parity_honest", "kernel_history", "investigatory"}
FORBIDDEN_LEAKAGE_STATUS = {"forbidden", "hidden_policy", "optimal_policy", "oracle", "baseline_value"}

CARRY_OPS = {"carry", "increase", "amplify", "consume", "require"}
RELIEF_OPS = {"reduce", "relieve", "prevent"}
CANCEL_OPS = {"reset", "cancel"}
EXPOSE_OPS = {"reveal", "expose", "reduce_hiddenness"}
BUFFER_OPS = {"buffer", "absorb"}
MASK_OPS = {"mask", "postpone", "hide"}
DECISION_SLOT_OPS = {"decision_slot", "single_decision_slot"}
EXCLUDE_OPS = {"exclude", "rival", "compete"}
MERGE_OPS = {"merge", "quotient", "equivalent"}
TRANSFER_OPS = {"transfer"}
TRANSFORM_OPS = {"transform"}
THRESHOLD_OPS = {"threshold", "phase_shift"}


@dataclass(frozen=True)
class PublicEffectFact:
    """Public burden/effect fact used by the kernel-side RelationSurface.

    The fact is not an action recommendation.  It is a public statement about
    transformation grammar: what burden/effect class a candidate carries,
    reduces, exposes, cancels, buffers, excludes, or transforms.
    """

    row_id: Hashable
    effect_id: str
    kind: str
    operation: str
    burden_type: str
    scope: str
    magnitude: float
    public_basis: str
    leakage_status: str
    relation_scope: str = ""
    direction: str = ""
    coupling: str = ""
    barrier: str = ""
    threshold_status: str = ""
    basin_status: str = ""
    confidence: float = 1.0
    relation_strength: str = ""

    @property
    def weight(self) -> float:
        return clamp01(self.magnitude * self.confidence, 1.0)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RelationSurfaceResult:
    rows: List[Dict[str, Any]]
    relations: List[BranchRelation]
    telemetry: Dict[str, Any]


def _key(value: Any) -> Hashable:
    try:
        hash(value)
        return value  # type: ignore[return-value]
    except Exception:
        return repr(value)


def branch_key_from_row(row: Mapping[str, Any]) -> Hashable:
    """Resolve branch identity with continuation/branch/candidate precedence before action fallback."""
    for field in ("continuation_id", "branch_id", "candidate_id", "action"):
        value = row.get(field)
        if value is not None:
            return _key(value)
    return "branch"


def _text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()


def _stable_text(value: Any, default: str = "unknown") -> str:
    out = _text(value)
    return out if out else default


def _raw_effects(row: Mapping[str, Any]) -> List[Mapping[str, Any]]:
    value = row.get("public_effects", row.get("burden_effects", row.get("effect_facts", [])))
    if isinstance(value, Mapping):
        return [value]
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
        return [v for v in value if isinstance(v, Mapping)]
    return []


def _normalize_operation(op: str) -> str:
    op = _stable_text(op, "unknown")
    aliases = {
        "relieves": "relieve",
        "relief": "relieve",
        "decrease": "reduce",
        "decreases": "reduce",
        "reduces": "reduce",
        "preventive": "prevent",
        "prevents": "prevent",
        "carries": "carry",
        "increases": "increase",
        "amplifies": "amplify",
        "reveals": "reveal",
        "exposes": "expose",
        "resets": "reset",
        "cancels": "cancel",
        "absorbs": "absorb",
        "buffers": "buffer",
        "masks": "mask",
        "postpones": "postpone",
        "excludes": "exclude",
        "rivals": "rival",
        "competes": "compete",
        "decision-slot": "decision_slot",
        "single_decision_slot": "decision_slot",
        "decision_slot": "decision_slot",
        "equivalent": "equivalent",
        "equivalence": "equivalent",
        "phase-shift": "phase_shift",
        "phase_shifted": "phase_shift",
    }
    return aliases.get(op, op)


def _basis_is_public(data: Mapping[str, Any]) -> Tuple[bool, str]:
    leakage = _stable_text(data.get("leakage_status", "public"), "public")
    basis = _stable_text(data.get("public_basis"), "")
    if leakage in FORBIDDEN_LEAKAGE_STATUS:
        return False, "forbidden_leakage_status"
    if leakage not in ALLOWED_LEAKAGE_STATUS:
        return False, "unknown_leakage_status"
    if basis not in ALLOWED_PUBLIC_BASES:
        return False, "missing_or_nonpublic_basis"
    return True, "accepted"


def _parse_effects(row: Mapping[str, Any]) -> Tuple[List[PublicEffectFact], Counter]:
    """Validate and normalize public effects from one candidate row; reject leakage as telemetry."""
    telemetry: Counter = Counter()
    row_id = branch_key_from_row(row)
    out: List[PublicEffectFact] = []
    for idx, raw in enumerate(_raw_effects(row)):
        ok, reason = _basis_is_public(raw)
        if not ok:
            telemetry[f"rejected_{reason}"] += 1
            continue
        op = _normalize_operation(str(raw.get("operation", raw.get("op", raw.get("effect", "unknown")))))
        burden_type = _stable_text(raw.get("burden_type", raw.get("type", raw.get("effect_type", ""))), "")
        kind = _stable_text(raw.get("kind"), "burden")
        # Most burden-derived relations need a type.  Pure legal/rivalry facts
        # can use relation_scope/resource when no burden type exists.
        relation_scope = _stable_text(raw.get("relation_scope", raw.get("resource", raw.get("resource_type", raw.get("scope", "")))), "")
        if not burden_type and op not in EXCLUDE_OPS and op not in MERGE_OPS and op not in DECISION_SLOT_OPS:
            telemetry["rejected_missing_burden_type"] += 1
            continue
        magnitude = clamp01(raw.get("magnitude", raw.get("weight", 1.0)), 1.0)
        confidence = clamp01(raw.get("confidence", 1.0), 1.0)
        effect_id = str(raw.get("effect_id", f"effect_{idx}"))
        out.append(
            PublicEffectFact(
                row_id=row_id,
                effect_id=effect_id,
                kind=kind,
                operation=op,
                burden_type=burden_type,
                scope=_stable_text(raw.get("scope"), "candidate"),
                magnitude=magnitude,
                public_basis=_stable_text(raw.get("public_basis"), ""),
                leakage_status=_stable_text(raw.get("leakage_status", "public"), "public"),
                relation_scope=relation_scope,
                direction=_stable_text(raw.get("direction"), ""),
                coupling=_stable_text(raw.get("coupling"), ""),
                barrier=_stable_text(raw.get("barrier"), ""),
                threshold_status=_stable_text(raw.get("threshold_status"), ""),
                basin_status=_stable_text(raw.get("basin_status"), ""),
                confidence=confidence,
                relation_strength=_stable_text(raw.get("relation_strength", raw.get("strength", "")), ""),
            )
        )
        telemetry["accepted_public_effects"] += 1
        telemetry[f"operation_{op}"] += 1
    return out, telemetry


def _magnitude_band(value: float, threshold_status: str = "", basin_status: str = "") -> str:
    """Coarse pressure regime band for continuation identity.

    Branch identity should change across material burden regimes, not across
    tiny magnitude jitter.  Explicit threshold/basin annotations can force a
    more specific regime label when the public effect says a phase/critical
    transition has been crossed.
    """
    ts = _stable_text(threshold_status, "")
    bs = _stable_text(basin_status, "")
    if ts in {"critical", "phase_shift", "threshold", "phase-shift", "critical_transition"}:
        return "critical"
    if bs in {"unstable", "critical", "overload"}:
        return "critical"
    v = clamp01(value, 0.0)
    if v <= 0.05:
        return "none"
    if v < 0.25:
        return "low"
    if v < 0.55:
        return "medium"
    if v < 0.82:
        return "high"
    return "critical"


def _signature_from_effects(effects: Sequence[PublicEffectFact], default_key: Hashable) -> Tuple[str, str]:
    if not effects:
        return str(default_key), "action"
    parts = []
    for e in effects:
        if e.operation in DECISION_SLOT_OPS:
            # Procedural slot competition is not a pressure identity source.
            continue
        band = _magnitude_band(e.weight, e.threshold_status, e.basin_status)
        parts.append(
            f"{e.burden_type or e.relation_scope}:{e.operation}:{e.scope}:{band}:{e.threshold_status or 'none'}:{e.basin_status or 'unknown'}:{e.coupling or 'uncoupled'}"
        )
    if not parts:
        return str(default_key), "action"
    sig = "|".join(sorted(parts))[:220]
    return sig, "public_effects"


def _overlap(a: PublicEffectFact, b: PublicEffectFact) -> bool:
    if a.burden_type and b.burden_type and a.burden_type == b.burden_type:
        return True
    if a.relation_scope and b.relation_scope and a.relation_scope == b.relation_scope:
        return True
    return False


def _sum_weights(effects: Sequence[PublicEffectFact], operations: set[str] | None = None, *, kinds: set[str] | None = None, burden_contains: Sequence[str] = ()) -> float:
    total = 0.0
    for e in effects:
        if operations is not None and e.operation not in operations:
            continue
        if kinds is not None and e.kind not in kinds:
            continue
        if burden_contains and not any(s in (e.burden_type or "") for s in burden_contains):
            continue
        total += e.weight
    return clamp01(total, 1.0)


def _summarize_branch_internal_operations(effects: Sequence[PublicEffectFact]) -> Dict[str, Any]:
    """Summarize branch-local burden operations from public effects.

    Cross-branch relations are not the only valid carrier for public effects.
    A candidate may carry, mask, expose, buffer, relieve, cancel, transform, or
    threshold-shift its own burden even when no other branch relates to it.
    These summaries let RCF/collapse consume that structure without requiring a
    second branch relation and without reading family/action names. Procedural
    single-slot facts are intentionally excluded: weak decision competition is
    telemetry, not a branch-internal burden operation.
    """
    internal_effects = [
        e for e in effects
        if e.operation not in DECISION_SLOT_OPS
        and not (e.kind == "legal_constraint" and not e.burden_type)
    ]
    op_counts: Counter = Counter(e.operation for e in internal_effects)
    burden_types = sorted({e.burden_type for e in internal_effects if e.burden_type})
    unresolved = _sum_weights(internal_effects, CARRY_OPS | MASK_OPS | THRESHOLD_OPS)
    relief = _sum_weights(internal_effects, RELIEF_OPS)
    cancellation = _sum_weights(internal_effects, CANCEL_OPS)
    exposure = _sum_weights(internal_effects, EXPOSE_OPS)
    buffering = _sum_weights(internal_effects, BUFFER_OPS)
    masking = _sum_weights(internal_effects, MASK_OPS)
    transfer_transform = _sum_weights(internal_effects, TRANSFER_OPS | TRANSFORM_OPS)
    threshold = _sum_weights(internal_effects, THRESHOLD_OPS)
    # Hiddenness can be a burden type or an uncertainty/evidence kind.  Carrying
    # hiddenness is an internal blocker; exposing hiddenness is a resolver.
    hidden_carry = 0.0
    hidden_expose = 0.0
    for e in internal_effects:
        is_hidden = (
            "hidden" in (e.burden_type or "")
            or "uncertainty" in (e.burden_type or "")
            or e.kind in {"uncertainty", "hiddenness"}
        )
        if not is_hidden:
            continue
        if e.operation in CARRY_OPS | MASK_OPS | THRESHOLD_OPS:
            hidden_carry += e.weight
        if e.operation in EXPOSE_OPS | RELIEF_OPS:
            hidden_expose += e.weight
    hiddenness = clamp01(hidden_carry, 1.0)
    exposure_support = clamp01(max(exposure, hidden_expose), 1.0)
    resolver = clamp01(max(relief, cancellation, buffering, exposure_support), 1.0)
    pressure = clamp01(0.46 * unresolved + 0.20 * masking + 0.16 * hiddenness + 0.12 * threshold + 0.06 * transfer_transform)
    rec = clamp01(0.36 * hiddenness * (1.0 - 0.35 * exposure_support) + 0.28 * masking + 0.22 * threshold + 0.14 * transfer_transform)
    return {
        "branch_internal_operation_count": int(len(internal_effects)),
        "branch_internal_public_effect_count": int(len(effects)),
        "branch_internal_operation_counts": dict(op_counts),
        "branch_internal_burden_types": burden_types,
        "branch_internal_unresolved_pressure": float(pressure),
        "branch_internal_raw_carry_pressure": float(unresolved),
        "branch_internal_resolver_support": float(resolver),
        "branch_internal_relief_support": float(relief),
        "branch_internal_cancellation_support": float(cancellation),
        "branch_internal_exposure_support": float(exposure_support),
        "branch_internal_buffering_support": float(buffering),
        "branch_internal_masking_pressure": float(masking),
        "branch_internal_threshold_pressure": float(threshold),
        "branch_internal_hiddenness_pressure": float(hiddenness),
        "branch_internal_transform_pressure": float(transfer_transform),
        "branch_internal_recursion_pressure": float(rec),
    }


def _relation_weight(a: PublicEffectFact, b: PublicEffectFact, scale: float = 1.0) -> float:
    return clamp01(scale * (0.50 * a.weight + 0.50 * b.weight), 1.0)


def _derive_relations(
    effects_by_row: Mapping[Hashable, Sequence[PublicEffectFact]],
    controls: Mapping[str, Any] | None = None,
    *,
    quotient_enabled: bool = True,
) -> Tuple[List[BranchRelation], Counter, Dict[Hashable, Dict[str, Any]]]:
    """Derive structural and weak-competition relations from normalized public effects."""
    relations: List[BranchRelation] = []
    telemetry: Counter = Counter()
    rows = list(effects_by_row.keys())
    for source in rows:
        source_effects = list(effects_by_row.get(source, []))
        for target in rows:
            if source == target:
                continue
            target_effects = list(effects_by_row.get(target, []))
            for se in source_effects:
                for te in target_effects:
                    if not _overlap(se, te):
                        telemetry["rejected_nonoverlap"] += 1
                        continue
                    if se.operation in RELIEF_OPS and te.operation in CARRY_OPS | MASK_OPS:
                        relations.append(BranchRelation(source=source, target=target, relation_type="relief", weight=_relation_weight(se, te)))
                        telemetry["relation_relief"] += 1
                    elif se.operation in CANCEL_OPS and te.operation in CARRY_OPS | MASK_OPS | RELIEF_OPS:
                        relations.append(BranchRelation(source=source, target=target, relation_type="cancellation", weight=_relation_weight(se, te)))
                        telemetry["relation_cancellation"] += 1
                    elif se.operation in EXPOSE_OPS and (te.operation in CARRY_OPS | MASK_OPS or te.kind in {"uncertainty", "evidence"}):
                        relations.append(BranchRelation(source=source, target=target, relation_type="shared_evidence", weight=_relation_weight(se, te, 0.85)))
                        telemetry["relation_shared_evidence"] += 1
                    elif se.operation in BUFFER_OPS and te.operation in CARRY_OPS | THRESHOLD_OPS:
                        relations.append(BranchRelation(source=source, target=target, relation_type="buffering", weight=_relation_weight(se, te, 0.80)))
                        telemetry["relation_buffering"] += 1
                    elif se.operation in TRANSFER_OPS and te.operation in CARRY_OPS:
                        relations.append(BranchRelation(source=source, target=target, relation_type="dependency", weight=_relation_weight(se, te, 0.70)))
                        telemetry["relation_dependency"] += 1
                    elif se.operation in TRANSFORM_OPS and te.operation in CARRY_OPS:
                        relations.append(BranchRelation(source=source, target=target, relation_type="dependency", weight=_relation_weight(se, te, 0.70)))
                        telemetry["relation_dependency"] += 1
                    elif se.operation in THRESHOLD_OPS or te.operation in THRESHOLD_OPS:
                        relations.append(BranchRelation(source=source, target=target, relation_type="proximity", weight=_relation_weight(se, te, 0.80)))
                        telemetry["relation_proximity"] += 1
            # legal/resource exclusions: relation scope is enough when both sides
            # publish public exclusion facts, even without a burden type.
            for se in source_effects:
                for te in target_effects:
                    if se.operation in DECISION_SLOT_OPS and te.operation in DECISION_SLOT_OPS and se.relation_scope and se.relation_scope == te.relation_scope:
                        relations.append(BranchRelation(source=source, target=target, relation_type="decision_slot_competition", weight=_relation_weight(se, te, 0.35)))
                        telemetry["relation_decision_slot_competition"] += 1
                    elif se.operation in EXCLUDE_OPS and te.operation in EXCLUDE_OPS and se.relation_scope and se.relation_scope == te.relation_scope:
                        rel_type = "rivalry" if (se.relation_strength in {"strong", "continuation"} or te.relation_strength in {"strong", "continuation"} or se.operation in {"rival", "compete"} or te.operation in {"rival", "compete"}) else "decision_slot_competition"
                        scale = 1.0 if rel_type == "rivalry" else 0.35
                        relations.append(BranchRelation(source=source, target=target, relation_type=rel_type, weight=_relation_weight(se, te, scale)))
                        telemetry[f"relation_{rel_type}"] += 1
    quotient_profiles: Dict[Hashable, Dict[str, Any]] = {}
    if quotient_enabled:
        # Quotient/equivalence is delegated to a narrow helper so the guardrails
        # are explicit and separately testable.  It derives only from public residual
        # profiles, not action labels, scalar-score closeness, or weak competition.
        quotient = derive_quotient_equivalence(effects_by_row, controls=controls)
        relations.extend(quotient.relations)
        if quotient.relations:
            telemetry["relation_equivalence"] += len(quotient.relations)
        for key, value in quotient.telemetry.items():
            telemetry[key] = value
        quotient_profiles = {
            bid: {
                "accepted": bool(profile.accepted),
                "reason": profile.reason,
                "basis": profile.basis,
                "signature": profile.signature,
                "entries": list(profile.entries[:8]),
            }
            for bid, profile in quotient.profiles.items()
        }
    else:
        telemetry["quotient_equivalence_disabled"] = 1
    return relations, telemetry, quotient_profiles


def derive_relation_surface(
    rows: Sequence[Mapping[str, Any]],
    controls: Mapping[str, Any] | None = None,
    *,
    quotient_enabled: bool = True,
) -> RelationSurfaceResult:
    """Return relation-enriched rows, relation objects, and audit telemetry for candidate rows."""
    """Derive kernel-side continuation identities and relations from public facts.

    This function performs no family/action-name policy.  It reads only generic
    public_effects/burden_effects/effect_facts and rejects non-public or
    solver-like effect facts.  It enriches rows with branch identity metadata and
    returns explicit BranchRelation objects for RCF.
    """
    telemetry: Counter = Counter()
    out_rows: List[Dict[str, Any]] = []
    effects_by_row: Dict[Hashable, List[PublicEffectFact]] = {}
    identity_source_counts: Counter = Counter()

    for raw in rows:
        row = dict(raw)
        existing_key = branch_key_from_row(row)
        effects, effect_telemetry = _parse_effects(row)
        telemetry.update(effect_telemetry)
        signature, sig_source = _signature_from_effects(effects, existing_key)

        if row.get("continuation_id") is not None:
            identity_source = "continuation_id"
            branch_id = _key(row.get("continuation_id"))
        elif row.get("branch_id") is not None:
            identity_source = "branch_id"
            branch_id = _key(row.get("branch_id"))
        elif effects:
            # Unique runtime handle derived from public pressure signature plus
            # the row's expression key.  The signature itself is stored for
            # equivalence/quotient derivation; action is only a disambiguating
            # interface expression, not the identity source.
            identity_source = "public_effects"
            branch_id = _key(f"pressure::{signature}::expr::{existing_key}")
            row["continuation_id"] = branch_id
            row["continuation_signature"] = signature
        elif row.get("candidate_id") is not None:
            identity_source = "candidate_id"
            branch_id = _key(row.get("candidate_id"))
        else:
            identity_source = "action"
            branch_id = _key(row.get("action", "branch"))

        row["branch_id"] = branch_id
        row["relation_surface_identity_source"] = identity_source
        row["relation_surface_public_effect_count"] = len(effects)
        row["relation_surface_effect_signature"] = signature if effects else ""
        row.update(_summarize_branch_internal_operations(effects))
        out_rows.append(row)
        effects_by_row[branch_id] = effects
        identity_source_counts[identity_source] += 1

    relations, rel_telemetry, quotient_profiles = _derive_relations(effects_by_row, controls=controls, quotient_enabled=quotient_enabled)
    concentration_profiles, concentration_telemetry = derive_relation_field_concentration(effects_by_row, controls=controls)
    for key, value in concentration_telemetry.items():
        if isinstance(value, (int, float)):
            telemetry[key] += value
        else:
            telemetry[key] = value
    for key, value in rel_telemetry.items():
        if isinstance(value, (int, float)):
            telemetry[key] += value
        else:
            telemetry[key] = value
    relations_by_type = Counter(r.relation_type for r in relations)
    rows_with_relations: Counter = Counter()
    for rel in relations:
        rows_with_relations[rel.source] += 1
        rows_with_relations[rel.target] += 1
    for row in out_rows:
        bid = branch_key_from_row(row)
        row["relation_surface_relation_count"] = int(rows_with_relations.get(bid, 0))
        if bid in concentration_profiles:
            cinfo = concentration_profiles[bid].to_dict()
            row["relation_field_domain"] = cinfo.get("domain", "")
            row["relation_field_concentration"] = float(cinfo.get("concentration", 0.0) or 0.0)
            row["relation_field_ambiguity"] = float(cinfo.get("ambiguity", 0.0) or 0.0)
            row["relation_field_domain_ambiguity"] = float(cinfo.get("domain_ambiguity", 0.0) or 0.0)
            row["relation_field_function_like_threshold"] = float(cinfo.get("function_like_threshold", 0.0) or 0.0)
            row["relation_field_function_like"] = bool(cinfo.get("function_like", False))
            row["relation_field_dominant_operation_class"] = cinfo.get("dominant_operation_class", "")
            row["relation_field_domain_row_count"] = int(cinfo.get("row_count_in_domain", 0) or 0)
        else:
            row["relation_field_concentration"] = 0.0
            row["relation_field_ambiguity"] = 0.0
            row["relation_field_domain_ambiguity"] = 0.0
            row["relation_field_function_like"] = False
        if bid in quotient_profiles:
            qinfo = quotient_profiles[bid]
            row["relation_surface_quotient_profile_accepted"] = bool(qinfo.get("accepted"))
            row["relation_surface_quotient_profile_reason"] = qinfo.get("reason", "")
            row["relation_surface_quotient_profile_basis"] = qinfo.get("basis", "")
            row["relation_surface_quotient_profile_entries"] = list(qinfo.get("entries", []))
            if qinfo.get("accepted"):
                row["relation_surface_quotient_profile"] = qinfo.get("signature", "")

    telemetry_out: Dict[str, Any] = dict(telemetry)
    telemetry_out["candidate_rows"] = len(out_rows)
    telemetry_out["branches_derived"] = len(effects_by_row)
    telemetry_out["relations_total"] = len(relations)
    telemetry_out["relations_by_type"] = dict(relations_by_type)
    telemetry_out["rows_with_public_effects"] = sum(1 for effects in effects_by_row.values() if effects)
    telemetry_out["rows_with_relations"] = sum(1 for row_id in effects_by_row if rows_with_relations.get(row_id, 0) > 0)
    telemetry_out["identity_source_counts"] = dict(identity_source_counts)
    telemetry_out["branch_internal_operation_rows"] = sum(1 for row in out_rows if int(row.get("branch_internal_operation_count", 0) or 0) > 0)
    telemetry_out["branch_internal_unresolved_pressure_total"] = float(sum(float(row.get("branch_internal_unresolved_pressure", 0.0) or 0.0) for row in out_rows))
    telemetry_out["branch_internal_hiddenness_pressure_total"] = float(sum(float(row.get("branch_internal_hiddenness_pressure", 0.0) or 0.0) for row in out_rows))
    telemetry_out["branch_internal_resolver_support_total"] = float(sum(float(row.get("branch_internal_resolver_support", 0.0) or 0.0) for row in out_rows))
    return RelationSurfaceResult(rows=out_rows, relations=relations, telemetry=telemetry_out)


def apply_relation_surface(
    rows: List[Dict[str, Any]],
    controls: Mapping[str, Any] | None = None,
    *,
    quotient_enabled: bool = True,
) -> Tuple[List[Dict[str, Any]], List[BranchRelation], Dict[str, Any]]:
    """Pipeline adapter for deriving RelationSurface output while preserving mutable row compatibility."""
    result = derive_relation_surface(rows, controls=controls, quotient_enabled=quotient_enabled)
    return result.rows, result.relations, result.telemetry
