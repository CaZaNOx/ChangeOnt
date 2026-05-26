"""First-pass quotient/equivalence helper for continuation branches.

This module implements the generic target from
``97_QUOTIENT_EQUIVALENCE_TARGET_STATE.md``.  It derives only conservative
quotient/equivalence relations from public residual profiles.  It is not a
state abstraction algorithm, not an action merger, and not a planner.

Guardrails:
- no problem-family names or native-action semantics;
- no scalar-score closeness;
- no weak decision-slot competition;
- no hidden/baseline/oracle facts;
- no topology editing;
- quotienting is based only on accepted public burden/effect profiles that
  preserve burden domain, operation family, coarse magnitude band, threshold /
  basin annotations, public scope, and coupling.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Hashable, Iterable, List, Mapping, Sequence, Tuple

from agents.co.runtime.surfaces.continuation_field import BranchRelation, clamp01


CARRY_OPS = {"carry", "increase", "amplify", "consume", "require"}
RELIEF_OPS = {"reduce", "relieve", "prevent"}
CANCEL_OPS = {"reset", "cancel"}
EXPOSE_OPS = {"reveal", "expose", "reduce_hiddenness"}
BUFFER_OPS = {"buffer", "absorb"}
MASK_OPS = {"mask", "postpone", "hide"}
TRANSFER_OPS = {"transfer"}
TRANSFORM_OPS = {"transform"}
THRESHOLD_OPS = {"threshold", "phase_shift"}
DECISION_SLOT_OPS = {"decision_slot", "single_decision_slot"}
EXCLUDE_OPS = {"exclude", "rival", "compete"}
MERGE_OPS = {"merge", "quotient", "equivalent"}

# Only public/parity/kernel-history effects should ever reach this helper via
# RelationSurface.  The leakage check remains here as a second guard so tests can
# exercise the helper directly without trusting callers.
ALLOWED_LEAKAGE_STATUS = {"public", "parity_honest", "kernel_history", "investigatory"}
FORBIDDEN_LEAKAGE_STATUS = {"forbidden", "hidden_policy", "optimal_policy", "oracle", "baseline_value"}


@dataclass(frozen=True)
class QuotientProfile:
    """Public residual profile used for conservative quotient derivation."""

    branch_id: Hashable
    signature: str
    entries: Tuple[str, ...]
    basis: str
    reason: str = "accepted"

    @property
    def accepted(self) -> bool:
        return self.reason == "accepted" and bool(self.entries)


@dataclass(frozen=True)
class QuotientDerivationResult:
    relations: List[BranchRelation]
    profiles: Dict[Hashable, QuotientProfile]
    telemetry: Dict[str, Any]


def _text(value: Any, default: str = "") -> str:
    if value is None:
        return default
    out = str(value).strip().lower()
    return out if out else default


def _weight(effect: Any) -> float:
    if hasattr(effect, "weight"):
        return clamp01(getattr(effect, "weight"), 1.0)
    mag = getattr(effect, "magnitude", None)
    if mag is None and isinstance(effect, Mapping):
        mag = effect.get("magnitude", effect.get("weight", 1.0))
    conf = getattr(effect, "confidence", None)
    if conf is None and isinstance(effect, Mapping):
        conf = effect.get("confidence", 1.0)
    return clamp01(clamp01(mag, 1.0) * clamp01(conf, 1.0), 1.0)


def _field(effect: Any, name: str, default: str = "") -> str:
    if isinstance(effect, Mapping):
        return _text(effect.get(name), default)
    return _text(getattr(effect, name, default), default)


def _operation_family(op: str) -> str:
    op = _text(op, "unknown")
    if op in CARRY_OPS:
        return "carry"
    if op in RELIEF_OPS:
        return "relief"
    if op in CANCEL_OPS:
        return "cancel"
    if op in EXPOSE_OPS:
        return "expose"
    if op in BUFFER_OPS:
        return "buffer"
    if op in MASK_OPS:
        return "mask"
    if op in TRANSFER_OPS:
        return "transfer"
    if op in TRANSFORM_OPS:
        return "transform"
    if op in THRESHOLD_OPS:
        return "threshold"
    if op in MERGE_OPS:
        return "declared_equivalence"
    if op in DECISION_SLOT_OPS:
        return "procedural_slot"
    if op in EXCLUDE_OPS:
        return "exclusion"
    return op


def _magnitude_band(value: float, threshold_status: str = "", basin_status: str = "", *, coarseness: float = 0.0) -> str:
    """Gauge-conditioned but conservative coarse residual band.

    The optional coarseness input comes from generic controls only.  It can
    smooth low/medium/high cut points slightly, but critical threshold/basin
    annotations always preserve separate identity.  This prevents quotienting
    across phase-relevant differences while allowing harmless magnitude jitter.
    """
    ts = _text(threshold_status)
    bs = _text(basin_status)
    if ts in {"critical", "phase_shift", "threshold", "phase-shift", "critical_transition"}:
        return "critical"
    if bs in {"unstable", "critical", "overload"}:
        return "critical"
    v = clamp01(value, 0.0)
    c = clamp01(coarseness, 0.0)
    # Wider coarse bands under higher coarseness, without merging critical range.
    low_cut = 0.22 + 0.04 * c
    med_cut = 0.52 + 0.05 * c
    high_cut = 0.80 + 0.03 * c
    if v <= 0.05:
        return "none"
    if v < low_cut:
        return "low"
    if v < med_cut:
        return "medium"
    if v < high_cut:
        return "high"
    return "critical"


def _controls_coarseness(controls: Mapping[str, Any] | None) -> float:
    if not controls:
        return 0.0
    # DynamicShapeField may expose coarseness_radius; older static controls do
    # not.  Treat absent value as zero additional coarseness.
    return clamp01(controls.get("coarseness_radius", controls.get("projection_coarseness", 0.0)), 0.0)


def quotient_profile_for_effects(
    branch_id: Hashable,
    effects: Sequence[Any],
    *,
    controls: Mapping[str, Any] | None = None,
) -> QuotientProfile:
    """Build a public residual profile, or explain why quotienting is disallowed."""
    if not effects:
        return QuotientProfile(branch_id=branch_id, signature="", entries=(), basis="none", reason="no_public_effects")

    coarseness = _controls_coarseness(controls)
    entries: List[str] = []
    rejected_procedural = 0
    rejected_exclusion = 0
    for effect in effects:
        leakage = _field(effect, "leakage_status", "public")
        if leakage in FORBIDDEN_LEAKAGE_STATUS or leakage not in ALLOWED_LEAKAGE_STATUS:
            return QuotientProfile(branch_id=branch_id, signature="", entries=(), basis="rejected", reason="nonpublic_or_solver_like_effect")
        op = _field(effect, "operation", _field(effect, "op", _field(effect, "effect", "unknown")))
        family = _operation_family(op)
        if family == "procedural_slot":
            rejected_procedural += 1
            continue
        if family == "exclusion":
            # Strong rivalry/exclusion changes relation topology and admissible
            # transformations.  It may be relevant for collapse, but it is not a
            # quotient basis in the first-pass helper.
            rejected_exclusion += 1
            continue
        burden = _field(effect, "burden_type", _field(effect, "type", _field(effect, "effect_type", "")))
        relation_scope = _field(effect, "relation_scope", _field(effect, "resource", _field(effect, "scope", "")))
        domain = burden or relation_scope
        if not domain:
            return QuotientProfile(branch_id=branch_id, signature="", entries=(), basis="rejected", reason="missing_public_domain")
        kind = _field(effect, "kind", "burden")
        scope = _field(effect, "scope", "candidate")
        coupling = _field(effect, "coupling", "uncoupled")
        threshold = _field(effect, "threshold_status", "none") or "none"
        basin = _field(effect, "basin_status", "unknown") or "unknown"
        band = _magnitude_band(_weight(effect), threshold, basin, coarseness=coarseness)
        # Preserve all fields that could change burden, admissibility, relation
        # topology, grey/recursion, collapse consequence, or readout expression.
        entries.append("/".join((domain, kind, family, scope, band, threshold, basin, coupling)))

    if not entries:
        reason = "procedural_only"
        if rejected_exclusion and not rejected_procedural:
            reason = "exclusion_only"
        elif rejected_exclusion and rejected_procedural:
            reason = "procedural_or_exclusion_only"
        return QuotientProfile(branch_id=branch_id, signature="", entries=(), basis="none", reason=reason)

    entries_tuple = tuple(sorted(entries))
    signature = "|".join(entries_tuple)[:260]
    return QuotientProfile(branch_id=branch_id, signature=signature, entries=entries_tuple, basis="public_residual_profile")


def derive_quotient_equivalence(
    effects_by_branch: Mapping[Hashable, Sequence[Any]],
    *,
    controls: Mapping[str, Any] | None = None,
) -> QuotientDerivationResult:
    """Derive conservative equivalence relations from public residual profiles."""
    profiles: Dict[Hashable, QuotientProfile] = {}
    buckets: Dict[str, List[Hashable]] = {}
    telemetry: Dict[str, Any] = {
        "quotient_profiles_total": 0,
        "quotient_profiles_accepted": 0,
        "quotient_profiles_rejected": {},
        "quotient_relations_derived": 0,
        "quotient_derivation_basis": "public_residual_profile",
    }

    rejected: Dict[str, int] = {}
    for branch_id, effects in effects_by_branch.items():
        profile = quotient_profile_for_effects(branch_id, list(effects), controls=controls)
        profiles[branch_id] = profile
        telemetry["quotient_profiles_total"] += 1
        if profile.accepted:
            telemetry["quotient_profiles_accepted"] += 1
            buckets.setdefault(profile.signature, []).append(branch_id)
        else:
            rejected[profile.reason] = rejected.get(profile.reason, 0) + 1
    telemetry["quotient_profiles_rejected"] = rejected
    telemetry["quotient_profile_summaries"] = [
        {
            "branch_id": str(branch_id),
            "accepted": bool(profile.accepted),
            "reason": profile.reason,
            "basis": profile.basis,
            "signature": profile.signature,
            "entries": list(profile.entries[:8]),
        }
        for branch_id, profile in profiles.items()
    ][:64]

    relations: List[BranchRelation] = []
    for signature, members in buckets.items():
        if len(members) < 2:
            continue
        # Weight is high because equality of conservative residual profiles is a
        # structural relation, but not policy.  RCF/certificate still decide what
        # the relation means for collapse.
        for i, a in enumerate(members):
            for b in members[i + 1 :]:
                relations.append(BranchRelation(source=a, target=b, relation_type="equivalence", weight=1.0))
                telemetry["quotient_relations_derived"] += 1
    telemetry["quotient_buckets_with_multiple_members"] = sum(1 for v in buckets.values() if len(v) > 1)
    telemetry["quotient_bucket_sizes"] = sorted([len(v) for v in buckets.values() if len(v) > 1], reverse=True)[:16]
    return QuotientDerivationResult(relations=relations, profiles=profiles, telemetry=telemetry)
