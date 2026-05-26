"""First-pass recursion-demand scheduler.

The scheduler implements the target-state distinction in
``98_RECURSION_DEMAND_TARGET_STATE.md``: recursion demand is not ordinary depth
expansion.  It is a bounded request for another unfolding layer when the current
layer cannot settle relation, quotient, grey, burden, hiddenness, admissibility,
or collapse status.

It is intentionally generic.  It does not read domain labels, interface
expressions, benchmark outcomes, hidden state, or external value estimates.  It
only consumes anonymous candidate rows, public relation topology, and generic
shape controls already available to the kernel.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from typing import Any, Dict, Hashable, Iterable, List, Mapping, Sequence

from agents.co.runtime.surfaces.continuation_field import BranchRelation, branch_key_from_row, clamp01


_EQUIV = {"equivalence", "quotient", "merge"}
_RIVAL = {"rivalry", "competition", "exclusive"}
_WEAK = {"decision_slot_competition", "weak_rivalry"}
_GREY = {"shared_evidence", "similarity", "proximity", "hiddenness_reduction", "exposure"}
_RECURSION = {"dependency", "burden_transfer", "burden_transform", "phase_shift", "critical_proximity"}
_RELIEF = {"relief", "burden_relief", "debt_relief"}
_CANCEL = {"cancellation", "cancel", "compensation"}
_BUFFER = {"buffering", "shielding", "absorption"}


@dataclass(frozen=True)
class RecursionSchedule:
    """Bounded structural recursion schedule for one anonymous branch.

    ``demand`` is the structural channel consumed by certificates.  Sampling or
    weak-procedural pressure is logged separately so uncertainty-heavy traces do
    not masquerade as a public structural reason to recurse.
    """

    branch_id: Hashable
    demand: float
    budget: int
    mode: str
    reasons: tuple[str, ...]
    non_equivalent_density: float = 0.0
    equivalent_density: float = 0.0
    unresolved_relation_pressure: float = 0.0
    sparse_high_consequence_pressure: float = 0.0
    quotient_pressure: float = 0.0
    structural_channel: float = 0.0
    sampling_uncertainty_channel: float = 0.0
    weak_procedural_channel: float = 0.0
    inherited_field_channel: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        out = asdict(self)
        out["branch_id"] = str(self.branch_id)
        out["reasons"] = list(self.reasons)
        return out


def _ctl(controls: Mapping[str, Any] | None, name: str, default: float = 0.5) -> float:
    if not isinstance(controls, Mapping):
        return float(default)
    return clamp01(controls.get(name, default), default)


def _rel_obj(rel: BranchRelation | Mapping[str, Any]) -> BranchRelation:
    if isinstance(rel, BranchRelation):
        return rel
    return BranchRelation.from_mapping(dict(rel))


def _row_pressure(row: Mapping[str, Any], key: str, *fallbacks: str) -> float:
    for k in (key,) + fallbacks:
        if k in row:
            return clamp01(row.get(k, 0.0))
    return 0.0


def derive_recursion_schedule(
    rows: Sequence[Mapping[str, Any]],
    relations: Iterable[BranchRelation | Mapping[str, Any]] | None = None,
    controls: Mapping[str, Any] | None = None,
) -> Dict[Hashable, RecursionSchedule]:
    """Return bounded recursion schedules from public field and relation state.

    The result is telemetry/control pressure only.  It does not create successor
    states, rank external outcomes, or select an interface expression.
    """
    by_id: Dict[Hashable, Mapping[str, Any]] = {branch_key_from_row(r): r for r in rows}
    if not by_id:
        return {}

    rels: List[BranchRelation] = []
    if relations is not None:
        for rel in relations:
            try:
                rr = _rel_obj(rel)
            except Exception:
                continue
            if rr.source in by_id and rr.target in by_id and rr.source != rr.target:
                rels.append(rr)

    by_branch: Dict[Hashable, List[BranchRelation]] = defaultdict(list)
    relation_counts: Dict[Hashable, Counter] = defaultdict(Counter)
    quotient_parent: Dict[Hashable, str] = {bid: str((row.get("quotient_id") or bid)) for bid, row in by_id.items()}
    for rel in rels:
        typ = str(rel.relation_type).lower()
        by_branch[rel.source].append(rel)
        by_branch[rel.target].append(rel)
        relation_counts[rel.source][typ] += 1
        relation_counts[rel.target][typ] += 1
        if typ in _EQUIV:
            qid = min(str(quotient_parent.get(rel.source, rel.source)), str(quotient_parent.get(rel.target, rel.target)))
            quotient_parent[rel.source] = qid
            quotient_parent[rel.target] = qid

    q_counts: Counter = Counter(quotient_parent.values())
    path = _ctl(controls, "path_sensitivity", 0.5)
    revision = _ctl(controls, "revision_permissibility", 0.5)
    nonlocal_auth = _ctl(controls, "nonlocal_authority", 0.5)
    rival_breadth = _ctl(controls, "rival_breadth", 0.5)
    collapse = _ctl(controls, "collapse_admissibility", 0.5)
    consequence = _ctl(controls, "contradiction_sensitivity", _ctl(controls, "consequence_span", 0.5))
    hidden_shape = _ctl(controls, "low_evidence_sampling", _ctl(controls, "hidden_decisiveness", 0.5))
    scheduler_gain = clamp01(0.18 + 0.20 * path + 0.18 * revision + 0.18 * nonlocal_auth + 0.14 * rival_breadth + 0.12 * consequence)
    collapse_relief = clamp01(0.20 + 0.55 * collapse)

    out: Dict[Hashable, RecursionSchedule] = {}
    for bid, row in by_id.items():
        counts = relation_counts.get(bid, Counter())
        equiv_count = sum(counts.get(t, 0) for t in _EQUIV) + max(0, q_counts.get(quotient_parent.get(bid, str(bid)), 1) - 1)
        weak_count = sum(counts.get(t, 0) for t in _WEAK)
        rival_count = sum(counts.get(t, 0) for t in _RIVAL)
        grey_count = sum(counts.get(t, 0) for t in _GREY)
        recursion_count = sum(counts.get(t, 0) for t in _RECURSION)
        relief_count = sum(counts.get(t, 0) for t in _RELIEF)
        cancel_count = sum(counts.get(t, 0) for t in _CANCEL)
        buffer_count = sum(counts.get(t, 0) for t in _BUFFER)
        structural_count = max(0, len(by_branch.get(bid, [])) - weak_count)
        non_equiv_edges = max(0, structural_count - equiv_count)
        non_equiv_density = clamp01(non_equiv_edges / 4.0)
        equiv_density = clamp01(equiv_count / 4.0)
        resolver_density = clamp01((relief_count + cancel_count + buffer_count) / 3.0)

        field_debt = _row_pressure(row, "field_debt", "burden_accumulation", "burden_pressure", "contradiction_burden")
        field_grey = _row_pressure(row, "field_grey_pressure")
        inherited_field_channel = _row_pressure(row, "field_recursion_budget")
        sampling_demand = _row_pressure(row, "sampling_demand")
        hidden = max(
            _row_pressure(row, "branch_internal_hiddenness_pressure"),
            _row_pressure(row, "uncertainty"),
        )
        exposure = _row_pressure(row, "branch_internal_exposure_support")
        masking = _row_pressure(row, "branch_internal_masking_pressure")
        threshold = _row_pressure(row, "branch_internal_threshold_pressure")
        transform = _row_pressure(row, "branch_internal_transform_pressure")
        branch_recursion = _row_pressure(row, "branch_internal_recursion_pressure")
        viability_gap = clamp01(1.0 - _row_pressure(row, "field_viability", "continuation_viability", "decision_state"))
        unresolved_relation = clamp01(
            0.24 * non_equiv_density
            + 0.18 * min(1.0, rival_count / 3.0)
            + 0.18 * min(1.0, grey_count / 3.0)
            + 0.16 * min(1.0, recursion_count / 2.0)
            + 0.12 * field_grey
            + 0.12 * transform
        )
        sparse_high_consequence = clamp01(
            (1.0 - non_equiv_density)
            * (0.30 * field_debt + 0.22 * hidden * (1.0 - 0.55 * exposure) + 0.20 * masking + 0.16 * threshold + 0.12 * viability_gap)
            * (0.45 + 0.55 * consequence)
        )
        hidden_pressure = clamp01(hidden * (1.0 - 0.60 * exposure) * (0.40 + 0.60 * hidden_shape))
        quotient_pressure = clamp01(equiv_density * (0.45 + 0.35 * collapse_relief + 0.20 * (1.0 - field_grey)))
        resolver_relief = clamp01(resolver_density * (0.42 + 0.38 * collapse + 0.20 * (1.0 - field_debt)))

        weak_procedural_channel = clamp01(weak_count / 4.0)
        sampling_uncertainty_channel = clamp01(0.52 * sampling_demand + 0.32 * hidden + 0.16 * viability_gap)
        relation_structural_base = clamp01(
            scheduler_gain
            * (
                0.44 * unresolved_relation
                + 0.30 * sparse_high_consequence
                + 0.30 * field_grey
                + 0.22 * hidden_pressure
                + 0.18 * field_debt
                + 0.12 * threshold
                + 0.32 * non_equiv_density
            )
            - 0.26 * quotient_pressure
            - 0.18 * resolver_relief
        )
        # Provenance split: only structurally grounded relation/field pressure
        # becomes certificate-facing recursion demand.  Pure uncertainty or weak
        # decision-slot competition remains visible telemetry, not a recursion
        # justification.
        structural_channel = clamp01(max(branch_recursion, relation_structural_base))
        if recursion_count > 0 and sparse_high_consequence >= 0.34:
            structural_channel = max(
                structural_channel,
                clamp01(0.70 + 0.14 * sparse_high_consequence + 0.08 * min(1.0, recursion_count / 2.0)),
            )
        if structural_count <= 0 and masking < 0.34 and threshold < 0.34 and field_grey < 0.30 and field_debt < 0.34:
            structural_channel = min(structural_channel, 0.20)
        if equiv_density >= 0.50 and non_equiv_density <= 0.20 and field_grey < 0.42 and sparse_high_consequence < 0.42:
            structural_channel = min(structural_channel, 0.32)

        reasons: List[str] = []
        if non_equiv_density >= 0.26:
            reasons.append("dense_non_equivalent_region")
        if equiv_density >= 0.26:
            reasons.append("equivalent_region_contracts")
        if sparse_high_consequence >= 0.34:
            reasons.append("sparse_high_consequence_unresolved")
        if hidden_pressure >= 0.34 and structural_count > 0:
            reasons.append("hiddenness_above_gauge_tolerance")
        elif hidden_pressure >= 0.34:
            reasons.append("hiddenness_sampling_channel_only")
        if masking >= 0.42:
            reasons.append("masking_pressure")
        if threshold >= 0.42:
            reasons.append("threshold_phase_shift_pressure")
        if recursion_count > 0:
            reasons.append("relation_may_change_next_layer_status")
        if sampling_uncertainty_channel >= 0.42 and structural_channel < 0.42:
            reasons.append("sampling_uncertainty_channel_logged_only")
        if weak_count > 0 and structural_channel < 0.26:
            reasons.append("weak_competition_logged_only")
        if not reasons:
            reasons.append("no_structural_recursion_trigger")

        demand = clamp01(structural_channel)
        if demand >= 0.62:
            mode = "request_unfolding_layer"
        elif demand >= 0.42:
            mode = "preserve_grey_monitor"
        elif equiv_density >= 0.26 and non_equiv_density <= 0.20:
            mode = "quotient_contract"
        elif sampling_uncertainty_channel >= 0.42 or weak_procedural_channel > 0.0:
            mode = "monitor_nonstructural_pressure"
        else:
            mode = "no_recursion_demand"
        budget = 0
        if demand >= 0.42:
            budget = 1
        if demand >= 0.66 and (non_equiv_density >= 0.40 or sparse_high_consequence >= 0.52):
            budget = 2
        if demand >= 0.82 and non_equiv_density >= 0.60 and sparse_high_consequence >= 0.60:
            budget = 3

        out[bid] = RecursionSchedule(
            branch_id=bid,
            demand=demand,
            budget=int(budget),
            mode=mode,
            reasons=tuple(dict.fromkeys(reasons)),
            non_equivalent_density=non_equiv_density,
            equivalent_density=equiv_density,
            unresolved_relation_pressure=unresolved_relation,
            sparse_high_consequence_pressure=sparse_high_consequence,
            quotient_pressure=quotient_pressure,
            structural_channel=structural_channel,
            sampling_uncertainty_channel=sampling_uncertainty_channel,
            weak_procedural_channel=weak_procedural_channel,
            inherited_field_channel=inherited_field_channel,
        )
    return out


def apply_recursion_scheduler(
    rows: List[Dict[str, Any]],
    relations: Iterable[BranchRelation | Mapping[str, Any]] | None = None,
    controls: Mapping[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    """Attach first-pass recursion schedule telemetry to rows.

    The scheduler may raise generic structural recursion pressure for
    certificate gating, but it never creates candidates or chooses among them.
    Sampling/uncertainty and weak-procedural channels are logged separately and
    do not raise certificate-facing ``field_recursion_budget``.
    """
    if not rows:
        return []
    schedules = derive_recursion_schedule(rows, relations=relations, controls=controls)
    out: List[Dict[str, Any]] = []
    for row in rows:
        nr = dict(row)
        bid = branch_key_from_row(row)
        schedule = schedules.get(bid)
        if schedule is None:
            out.append(nr)
            continue
        d = clamp01(schedule.demand)
        nr["recursion_schedule"] = schedule.to_dict()
        nr["recursion_scheduler_demand"] = d
        nr["recursion_scheduler_budget"] = int(schedule.budget)
        nr["recursion_scheduler_mode"] = schedule.mode
        nr["recursion_scheduler_reasons"] = list(schedule.reasons)
        nr["recursion_scheduler_non_equivalent_density"] = schedule.non_equivalent_density
        nr["recursion_scheduler_equivalent_density"] = schedule.equivalent_density
        nr["recursion_scheduler_unresolved_relation_pressure"] = schedule.unresolved_relation_pressure
        nr["recursion_scheduler_sparse_high_consequence_pressure"] = schedule.sparse_high_consequence_pressure
        nr["recursion_scheduler_quotient_pressure"] = schedule.quotient_pressure
        nr["recursion_scheduler_structural_channel"] = schedule.structural_channel
        nr["recursion_scheduler_sampling_uncertainty_channel"] = schedule.sampling_uncertainty_channel
        nr["recursion_scheduler_weak_procedural_channel"] = schedule.weak_procedural_channel
        nr["recursion_scheduler_inherited_field_channel"] = schedule.inherited_field_channel
        # Certificate integration: only raise public structural recursion
        # pressure; do not lower existing field pressure or decide a winner.
        nr["field_recursion_budget_before_scheduler"] = clamp01(nr.get("field_recursion_budget", 0.0))
        nr["field_recursion_budget"] = d
        nr["branch_internal_recursion_pressure"] = clamp01(max(clamp01(nr.get("branch_internal_recursion_pressure", 0.0)), 0.72 * d))
        out.append(nr)
    return out
