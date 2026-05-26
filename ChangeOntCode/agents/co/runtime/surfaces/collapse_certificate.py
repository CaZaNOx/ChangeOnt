"""Earned-collapse certificate derivation.

Implements ``91_EARNED_COLLAPSE_CERTIFICATE_IMPLEMENTATION.md`` and the collapse
side of ``85_RELATION_TO_COLLAPSE_DIAGNOSTIC_CONTRACT.md``.  Certificates record
whether commitment is earned and why collapse may remain blocked by unresolved
rivalry, burden, hiddenness, grey pressure, or recursion demand.
"""

from __future__ import annotations


from collections import Counter, defaultdict
from typing import Any, Dict, Hashable, Iterable, List, Mapping, MutableMapping, Sequence

from agents.co.runtime.surfaces.continuation_field import BranchRelation, branch_key_from_row


def _clamp01(x: Any, default: float = 0.0) -> float:
    try:
        v = float(x)
    except Exception:
        v = float(default)
    if v < 0.0:
        return 0.0
    if v > 1.0:
        return 1.0
    return v


def _ctl(controls: Mapping[str, Any] | None, name: str, default: float = 0.5) -> float:
    if not isinstance(controls, Mapping):
        return float(default)
    return _clamp01(controls.get(name, default), default)


def _relation_obj(rel: BranchRelation | Mapping[str, Any]) -> BranchRelation:
    if isinstance(rel, BranchRelation):
        return rel
    return BranchRelation.from_mapping(dict(rel))


_EQUIV = {"equivalence", "quotient", "merge"}
_RIVAL = {"rivalry", "competition", "exclusive"}
_WEAK_COMPETITION = {"decision_slot_competition", "weak_rivalry"}
_RELIEF = {"relief", "burden_relief", "debt_relief"}
_CANCEL = {"cancellation", "cancel", "compensation"}
_GREY = {"shared_evidence", "similarity", "proximity", "hiddenness_reduction", "exposure"}
_RECURSION = {"dependency", "burden_transfer", "burden_transform", "phase_shift", "critical_proximity"}
_BUFFER = {"buffering", "shielding", "absorption"}


def derive_collapse_certificates(
    rows: Sequence[Mapping[str, Any]],
    relations: Iterable[BranchRelation | Mapping[str, Any]] | None = None,
    controls: Mapping[str, Any] | None = None,
) -> Dict[Hashable, Dict[str, Any]]:
    """Return per-branch earned-collapse certificate dictionaries.

    The certificate is deliberately conservative: it does not make a policy
    choice.  It exposes whether relation topology permits collapse, demands grey
    preservation, or calls for recursion.  CommitmentSurface can then consume
    these reasons without reconstructing relation topology from scalar proxies.
    """

    by_id: Dict[Hashable, Mapping[str, Any]] = {branch_key_from_row(r): r for r in rows}
    rels: List[BranchRelation] = []
    if relations is not None:
        for rel in relations:
            try:
                rr = _relation_obj(rel)
            except Exception:
                continue
            if rr.source in by_id and rr.target in by_id:
                rels.append(rr)

    by_branch: Dict[Hashable, List[BranchRelation]] = defaultdict(list)
    relations_by_type: Dict[Hashable, Counter] = defaultdict(Counter)
    for rel in rels:
        typ = str(rel.relation_type).lower()
        by_branch[rel.source].append(rel)
        by_branch[rel.target].append(rel)
        relations_by_type[rel.source][typ] += 1
        relations_by_type[rel.target][typ] += 1

    collapse_adm = _ctl(controls, "collapse_admissibility", 0.5)
    revision = _ctl(controls, "revision_permissibility", 0.5)
    path = _ctl(controls, "path_sensitivity", 0.5)
    nonlocal_authority = _ctl(controls, "nonlocal_authority", 0.5)
    rival_breadth = _ctl(controls, "rival_breadth", 0.5)
    fracture_tol = _ctl(controls, "fracture_tolerance", 0.5)

    grey_threshold = max(0.28, min(0.72, 0.58 - 0.18 * collapse_adm + 0.14 * revision + 0.10 * nonlocal_authority))
    debt_threshold = max(0.32, min(0.78, 0.62 - 0.16 * fracture_tol + 0.10 * path + 0.10 * revision))
    recursion_threshold = max(0.35, min(0.80, 0.56 - 0.12 * collapse_adm + 0.16 * path + 0.12 * rival_breadth))
    hiddenness_threshold = max(0.30, min(0.78, 0.58 - 0.16 * collapse_adm + 0.14 * revision + 0.12 * nonlocal_authority))
    masking_threshold = max(0.28, min(0.76, 0.52 - 0.12 * collapse_adm + 0.16 * revision + 0.10 * path))

    out: Dict[Hashable, Dict[str, Any]] = {}
    for bid, row in by_id.items():
        field_debt = _clamp01(row.get("field_debt", row.get("burden_accumulation", row.get("contradiction_burden", 0.0))))
        field_grey = _clamp01(row.get("field_grey_pressure", 0.0))
        field_recursion = _clamp01(row.get("field_recursion_budget", row.get("sampling_demand", 0.0)))
        field_ready = _clamp01(row.get("field_collapse_readiness", row.get("commitment_stability", 0.0)))
        quotient_share = int(row.get("quotient_share_count", 1) or 1)
        field_relation_count = int(row.get("field_relation_count", 0) or 0)
        branch_hiddenness = _clamp01(row.get("branch_internal_hiddenness_pressure", 0.0))
        branch_exposure = _clamp01(row.get("branch_internal_exposure_support", 0.0))
        branch_masking = _clamp01(row.get("branch_internal_masking_pressure", 0.0))
        branch_buffering = _clamp01(row.get("branch_internal_buffering_support", 0.0))
        branch_relief = _clamp01(row.get("branch_internal_relief_support", row.get("branch_internal_resolver_support", 0.0)))
        branch_cancel = _clamp01(row.get("branch_internal_cancellation_support", 0.0))
        branch_threshold = _clamp01(row.get("branch_internal_threshold_pressure", 0.0))
        branch_transform = _clamp01(row.get("branch_internal_transform_pressure", 0.0))
        branch_recursion = _clamp01(row.get("branch_internal_recursion_pressure", 0.0))

        unresolved_rivals = 0
        quotient_relations = 0
        relief_out = 0
        relief_in = 0
        cancellation_out = 0
        cancellation_in = 0
        grey_relations = 0
        recursion_relations = 0
        buffering_relations = 0
        weak_decision_competition = 0
        blockers: List[str] = []
        reason_flags: List[str] = []

        for rel in by_branch.get(bid, []):
            typ = str(rel.relation_type).lower()
            w = _clamp01(rel.weight, 1.0)
            if typ in _WEAK_COMPETITION:
                weak_decision_competition += 1
            elif typ in _EQUIV:
                quotient_relations += 1
            elif typ in _RIVAL and w >= 0.18:
                unresolved_rivals += 1
            elif typ in _RELIEF:
                if rel.source == bid:
                    relief_out += 1
                if rel.target == bid:
                    relief_in += 1
            elif typ in _CANCEL:
                if rel.source == bid:
                    cancellation_out += 1
                if rel.target == bid:
                    cancellation_in += 1
            elif typ in _GREY:
                grey_relations += 1
            elif typ in _RECURSION:
                recursion_relations += 1
            elif typ in _BUFFER:
                buffering_relations += 1

        # Rivalry should block collapse only when it remains unresolved by
        # quotient/cancellation and is accompanied by nontrivial grey/debt or by
        # a regime that assigns authority to rivals/nonlocal structure.
        rivalry_unresolved = max(0, unresolved_rivals - quotient_relations - cancellation_out - cancellation_in)
        branch_resolution = max(branch_relief, branch_cancel, branch_buffering, branch_exposure)
        effective_buffering = buffering_relations + (1 if branch_buffering >= 0.18 else 0)
        effective_relief = relief_out + (1 if branch_relief >= 0.18 else 0)
        effective_cancellation = cancellation_out + (1 if branch_cancel >= 0.18 else 0)
        if rivalry_unresolved > 0 and (field_grey >= 0.18 or field_debt >= 0.22 or rival_breadth >= 0.55 or revision >= 0.55):
            blockers.append("unresolved_non_equivalent_rival")
        if field_grey >= grey_threshold and quotient_share <= 1:
            blockers.append("operative_grey_difference")
        if field_debt >= debt_threshold and effective_relief == 0 and effective_cancellation == 0 and effective_buffering == 0:
            blockers.append("unresolved_burden")
        if branch_hiddenness >= hiddenness_threshold and branch_exposure < 0.24 and (revision >= 0.40 or nonlocal_authority >= 0.40):
            blockers.append("unresolved_hiddenness_burden")
        if branch_masking >= masking_threshold and branch_buffering < 0.22 and branch_resolution < 0.22:
            blockers.append("masked_unresolved_burden")
        if branch_threshold >= 0.72 and branch_resolution < 0.30:
            blockers.append("threshold_phase_shift")
        if max(field_recursion, branch_recursion) >= recursion_threshold and (recursion_relations > 0 or rivalry_unresolved > 0 or grey_relations > 0 or branch_hiddenness >= hiddenness_threshold or branch_threshold >= 0.55 or branch_transform >= 0.45):
            blockers.append("recursion_demand")

        if quotient_share > 1 or quotient_relations > 0:
            reason_flags.append("quotient_or_equivalence_support")
        if relief_out > 0:
            reason_flags.append("relieves_burden_elsewhere")
        if cancellation_out > 0:
            reason_flags.append("cancels_burden_condition")
        if buffering_relations > 0 or branch_buffering > 0.0:
            reason_flags.append("buffers_tension_conversion")
        if branch_hiddenness > 0.0:
            reason_flags.append("branch_internal_hiddenness_carried")
        if branch_exposure > 0.0:
            reason_flags.append("branch_internal_exposure_support")
        if branch_masking > 0.0:
            reason_flags.append("branch_internal_masking_pressure")
        if branch_relief > 0.0 or branch_cancel > 0.0:
            reason_flags.append("branch_internal_resolution_support")
        if branch_threshold > 0.0:
            reason_flags.append("branch_internal_threshold_pressure")
        if weak_decision_competition > 0:
            reason_flags.append("weak_decision_competition_logged")
        if not blockers and field_relation_count > 0:
            reason_flags.append("relation_topology_nonblocking")

        blocker_pressure = _clamp01(0.30 * min(1.0, len(blockers) / 4.0) + 0.18 * min(1.0, rivalry_unresolved / 3.0) + 0.18 * field_grey + 0.16 * field_debt + 0.14 * branch_hiddenness * (1.0 - 0.35 * branch_exposure) + 0.10 * branch_masking + 0.04 * branch_threshold)
        resolver_support = _clamp01(0.24 * min(1.0, quotient_share / 2.0) + 0.22 * min(1.0, (relief_out + cancellation_out + buffering_relations) / 2.0) + 0.20 * branch_resolution + 0.16 * (1.0 - field_debt) + 0.10 * (1.0 - field_grey) + 0.08 * field_ready)
        earnedness = _clamp01(0.44 * field_ready + 0.24 * resolver_support + 0.14 * collapse_adm + 0.08 * (1.0 - revision) + 0.10 * (1.0 - blocker_pressure))
        recursion_demand = _clamp01(max(field_recursion, branch_recursion, 0.30 * min(1.0, recursion_relations / 2.0) + 0.24 * min(1.0, rivalry_unresolved / 3.0) + 0.20 * field_grey + 0.14 * branch_hiddenness + 0.08 * branch_threshold + 0.04 * path))

        ready = bool(not blockers and earnedness >= max(0.42, 0.58 - 0.18 * collapse_adm))
        if ready:
            status = "earned_collapse_ready"
        elif "recursion_demand" in blockers:
            status = "blocked_by_recursion_demand"
        elif "operative_grey_difference" in blockers or "unresolved_non_equivalent_rival" in blockers:
            status = "blocked_by_unresolved_relation"
        elif "unresolved_burden" in blockers:
            status = "blocked_by_unresolved_burden"
        elif field_relation_count > 0:
            status = "relation_present_not_earned"
        else:
            status = "relation_neutral"

        cert = {
            "status": status,
            "ready": bool(ready),
            "score": float(earnedness),
            "earnedness": float(earnedness),
            "blocker_pressure": float(blocker_pressure),
            "recursion_demand": float(recursion_demand),
            "blockers": list(dict.fromkeys(blockers)),
            "reason_flags": list(dict.fromkeys(reason_flags)),
            "unresolved_rival_count": int(unresolved_rivals),
            "relation_unresolved_rival_count": int(unresolved_rivals),
            "weak_decision_competition_count": int(weak_decision_competition),
            "quotient_resolved_rival_count": int(quotient_relations + max(0, quotient_share - 1)),
            "relief_out_count": int(relief_out),
            "relief_in_count": int(relief_in),
            "cancellation_out_count": int(cancellation_out),
            "cancellation_in_count": int(cancellation_in),
            "grey_relation_count": int(grey_relations),
            "recursion_relation_count": int(recursion_relations),
            "buffering_relation_count": int(buffering_relations),
            "field_relation_count": int(field_relation_count),
            "branch_internal_hiddenness_pressure": float(branch_hiddenness),
            "branch_internal_exposure_support": float(branch_exposure),
            "branch_internal_masking_pressure": float(branch_masking),
            "branch_internal_buffering_support": float(branch_buffering),
            "branch_internal_relief_support": float(branch_relief),
            "branch_internal_cancellation_support": float(branch_cancel),
            "branch_internal_threshold_pressure": float(branch_threshold),
            "branch_internal_transform_pressure": float(branch_transform),
            "branch_internal_recursion_pressure": float(branch_recursion),
            "relations_by_type": dict(relations_by_type.get(bid, Counter())),
            "thresholds": {
                "grey": float(grey_threshold),
                "debt": float(debt_threshold),
                "recursion": float(recursion_threshold),
                "hiddenness": float(hiddenness_threshold),
                "masking": float(masking_threshold),
            },
        }
        out[bid] = cert
    return out


def apply_collapse_certificates(
    rows: List[Dict[str, Any]],
    relations: Iterable[BranchRelation | Mapping[str, Any]] | None = None,
    controls: Mapping[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    """Attach collapse-certificate fields to candidate rows for CommitmentSurface."""
    if not rows:
        return []
    certs = derive_collapse_certificates(rows, relations=relations, controls=controls)
    out: List[Dict[str, Any]] = []
    for row in rows:
        nr = dict(row)
        bid = branch_key_from_row(row)
        cert = certs.get(bid, {})
        nr["collapse_certificate"] = dict(cert)
        nr["collapse_certificate_status"] = str(cert.get("status", "relation_neutral"))
        nr["collapse_certificate_ready"] = bool(cert.get("ready", False))
        nr["collapse_certificate_score"] = float(cert.get("score", 0.0) or 0.0)
        nr["collapse_certificate_earnedness"] = float(cert.get("earnedness", nr.get("collapse_certificate_score", 0.0)) or 0.0)
        nr["collapse_certificate_blocker_pressure"] = float(cert.get("blocker_pressure", 0.0) or 0.0)
        nr["collapse_certificate_recursion_demand"] = float(cert.get("recursion_demand", 0.0) or 0.0)
        nr["collapse_blockers"] = list(cert.get("blockers", []) or [])
        nr["collapse_blocker_count"] = int(len(nr["collapse_blockers"]))
        nr["unresolved_rival_count"] = int(cert.get("unresolved_rival_count", 0) or 0)
        nr["relation_unresolved_rival_count"] = int(cert.get("relation_unresolved_rival_count", nr.get("unresolved_rival_count", 0)) or 0)
        nr["quotient_resolved_rival_count"] = int(cert.get("quotient_resolved_rival_count", 0) or 0)
        nr["weak_decision_competition_count"] = int(cert.get("weak_decision_competition_count", 0) or 0)
        nr["collapse_certificate_reason_flags"] = list(cert.get("reason_flags", []) or [])
        nr["collapse_certificate_relations_by_type"] = dict(cert.get("relations_by_type", {}) or {})
        for key in (
            "branch_internal_hiddenness_pressure",
            "branch_internal_exposure_support",
            "branch_internal_masking_pressure",
            "branch_internal_buffering_support",
            "branch_internal_relief_support",
            "branch_internal_cancellation_support",
            "branch_internal_threshold_pressure",
            "branch_internal_transform_pressure",
            "branch_internal_recursion_pressure",
        ):
            if key in cert:
                nr[key] = float(cert.get(key, 0.0) or 0.0)
        out.append(nr)
    return out
