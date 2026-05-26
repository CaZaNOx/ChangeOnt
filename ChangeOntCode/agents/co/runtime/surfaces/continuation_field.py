"""RecursiveContinuationField runtime carrier.

Implements the current mechanism bundle described in
``47_RECURSIVE_CONTINUATION_FIELD.md`` through
``50_RECURSIVE_CONTINUATION_FIELD_IMPLEMENTATION_READINESS.md``.  It updates
branch-local field state from candidate rows and RelationSurface topology; it is
not an ontological primitive and not a standalone planner.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Hashable, Iterable, List, Mapping, Optional, Tuple


def clamp01(x: Any, default: float = 0.0) -> float:
    try:
        v = float(x)
    except Exception:
        v = float(default)
    if v < 0.0:
        return 0.0
    if v > 1.0:
        return 1.0
    return v


def _key(value: Any) -> Hashable:
    try:
        hash(value)
        return value  # type: ignore[return-value]
    except Exception:
        return repr(value)


def branch_key_from_row(row: Mapping[str, Any]) -> Hashable:
    """Return the runtime continuation-branch key for a candidate row.

    Continuation/branch identity is kernel structure; the native action is only
    a last-resort interface placeholder.
    """
    for field in ("continuation_id", "branch_id", "candidate_id", "action"):
        value = row.get(field)
        if value is not None:
            return _key(value)
    return "branch"


@dataclass(frozen=True)
class ContinuationBranch:
    """Normalized branch-pressure signature consumed by the continuation field."""
    """Anonymous runtime branch for recursive continuation-field updates.

    A branch is a candidate continuation identity, not an action policy.  The
    field knows only support, burden/debt, uncertainty, relief capacity, and
    relational structure.  It must not inspect problem-family or action names.
    """

    branch_id: Hashable
    support: float = 0.0
    local_support: float = 0.0
    viability: float = 0.0
    burden: float = 0.0
    debt: float = 0.0
    instability: float = 0.0
    uncertainty: float = 0.0
    relief_capacity: float = 0.0
    grey_pressure: float = 0.0
    recursion_budget: float = 0.0
    quotient_id: Hashable | None = None

    @classmethod
    def from_row(cls, row: Mapping[str, Any]) -> "ContinuationBranch":
        bid = branch_key_from_row(row)
        support = clamp01(row.get("support_mass", row.get("support", row.get("decision_state", 0.0))))
        local_support = clamp01(row.get("local_support", support), support)
        viability = clamp01(row.get("continuation_viability", row.get("stability_under_change", support)), support)
        internal_pressure = clamp01(row.get("branch_internal_unresolved_pressure", 0.0))
        internal_masking = clamp01(row.get("branch_internal_masking_pressure", 0.0))
        internal_hiddenness = clamp01(row.get("branch_internal_hiddenness_pressure", 0.0))
        internal_threshold = clamp01(row.get("branch_internal_threshold_pressure", 0.0))
        internal_recursion = clamp01(row.get("branch_internal_recursion_pressure", 0.0))
        internal_relief = clamp01(row.get("branch_internal_relief_support", row.get("branch_internal_resolver_support", 0.0)))
        internal_cancel = clamp01(row.get("branch_internal_cancellation_support", 0.0))
        internal_buffer = clamp01(row.get("branch_internal_buffering_support", 0.0))
        internal_exposure = clamp01(row.get("branch_internal_exposure_support", 0.0))

        burden = max(
            clamp01(row.get("burden_pressure", row.get("contradiction_burden", row.get("fracture_state", 0.0)))),
            internal_pressure,
            0.72 * internal_masking,
            0.64 * internal_threshold,
        )
        accumulation = max(clamp01(row.get("burden_accumulation", burden), burden), internal_pressure)
        trend = max(clamp01(row.get("burden_trend", 0.0)), 0.50 * internal_threshold)
        instability = max(clamp01(row.get("continuation_instability", accumulation), accumulation), 0.55 * internal_masking, 0.45 * internal_threshold)
        uncertainty = max(clamp01(row.get("uncertainty", 0.0)), clamp01(internal_hiddenness * (1.0 - 0.35 * internal_exposure)))
        relief = max(clamp01(row.get("burden_relief", 0.0)), internal_relief, 0.85 * internal_cancel)
        preventive = max(clamp01(row.get("preventive_support", 0.0)), internal_buffer, 0.50 * internal_exposure)
        debt = clamp01(0.42 * accumulation + 0.20 * trend + 0.18 * instability + 0.12 * max(0.0, burden - relief) + 0.08 * internal_masking)
        # Stability is ordinary local viability, not relief.  A low-burden or
        # stable branch may remain viable, but it must not become a relational
        # relief branch unless the row explicitly exposes burden_relief,
        # preventive_support, or an explicit relation graph does so.
        relief_capacity = clamp01(0.58 * relief + 0.42 * preventive)
        return cls(
            branch_id=bid,
            support=support,
            local_support=local_support,
            viability=viability,
            burden=burden,
            debt=debt,
            instability=instability,
            uncertainty=uncertainty,
            relief_capacity=relief_capacity,
            grey_pressure=max(clamp01(row.get("field_grey_pressure", 0.0)), 0.42 * internal_hiddenness, 0.35 * internal_masking),
            recursion_budget=max(clamp01(row.get("field_recursion_budget", 0.0)), internal_recursion),
            quotient_id=_key(row.get("quotient_id")) if row.get("quotient_id") is not None else None,
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class BranchRelation:
    """Typed relation edge between two continuation branches."""
    """Typed generic relation between anonymous continuation branches."""

    source: Hashable
    target: Hashable
    relation_type: str
    weight: float = 1.0

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "BranchRelation":
        return cls(
            source=_key(data.get("source")),
            target=_key(data.get("target")),
            relation_type=str(data.get("relation_type", data.get("type", "similarity"))).lower(),
            weight=clamp01(data.get("weight", 1.0), 1.0),
        )


@dataclass
class FieldBranchState:
    """Field outputs for one branch after relation-aware update."""
    branch_id: Hashable
    support: float
    local_support: float
    base_viability: float
    field_viability: float
    field_debt: float
    field_relief_support: float
    field_grey_pressure: float
    field_recursion_budget: float
    field_collapse_readiness: float
    quotient_id: Hashable
    quotient_share_count: int = 1
    field_relation_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        out = asdict(self)
        out["branch_id"] = str(self.branch_id)
        out["quotient_id"] = str(self.quotient_id)
        return out


class ContinuationField:
    """Relation-aware continuation field that updates branch debt, relief, grey, recursion, and viability."""
    """Minimal recursive continuation-field updater.

    This class implements the doctrine-level distinction between action rows and
    continuation branches.  It is intentionally small: it only performs generic
    debt propagation, grey preservation, quotient marking, cancellation, and
    recursion-budget allocation.  It is not a planner and contains no problem or
    action literals.
    """

    def __init__(self, controls: Optional[Mapping[str, Any]] = None) -> None:
        self.controls = dict(controls or {})

    def _control(self, name: str, default: float = 0.5) -> float:
        return clamp01(self.controls.get(name, default), default)

    def _shape_pressure(self) -> Dict[str, float]:
        local = self._control("local_authority", 0.5)
        nonlocal_auth = self._control("nonlocal_authority", 0.5)
        path = self._control("path_sensitivity", 0.5)
        revision = self._control("revision_permissibility", 0.5)
        rival = self._control("rival_breadth", 0.5)
        collapse = self._control("collapse_admissibility", self._control("collapse_permission", 0.5))
        hidden = self._control("low_evidence_sampling", self._control("hidden_decisiveness", 0.5))
        consequence = self._control("contradiction_sensitivity", self._control("consequence_span", 0.5))
        nonclosure = clamp01(0.20 * nonlocal_auth + 0.18 * path + 0.17 * revision + 0.16 * rival + 0.14 * hidden + 0.10 * consequence + 0.05 * (1.0 - local))
        collapse_bias = clamp01(0.18 + 0.38 * collapse + 0.24 * local - 0.16 * revision - 0.12 * nonlocal_auth)
        return {
            "local": local,
            "nonlocal": nonlocal_auth,
            "path": path,
            "revision": revision,
            "rival": rival,
            "collapse": collapse,
            "hidden": hidden,
            "consequence": consequence,
            "nonclosure": nonclosure,
            "collapse_bias": collapse_bias,
        }

    @staticmethod
    def proximity(a: ContinuationBranch, b: ContinuationBranch) -> float:
        if a.branch_id == b.branch_id:
            return 1.0
        dist = (
            0.24 * abs(a.support - b.support)
            + 0.22 * abs(a.viability - b.viability)
            + 0.22 * abs(a.burden - b.burden)
            + 0.16 * abs(a.uncertainty - b.uncertainty)
            + 0.16 * abs(a.debt - b.debt)
        )
        return clamp01(1.0 - dist)

    def update(self, branches: Iterable[ContinuationBranch], relations: Optional[Iterable[BranchRelation | Mapping[str, Any]]] = None) -> Dict[Hashable, FieldBranchState]:
        branch_list = list(branches)
        by_id: Dict[Hashable, ContinuationBranch] = {b.branch_id: b for b in branch_list}
        if not by_id:
            return {}
        p = self._shape_pressure()
        field_debt = {bid: clamp01(b.debt) for bid, b in by_id.items()}
        # Local explicit relief/prevention can increase the source branch's
        # viability a little, but it does not propagate across branches.
        # Cross-branch relief requires explicit relation support below.
        relief_support = {bid: clamp01(0.18 * b.relief_capacity) for bid, b in by_id.items()}
        grey_pressure = {bid: clamp01(b.grey_pressure) for bid, b in by_id.items()}
        relation_count = {bid: 0 for bid in by_id}
        quotient_parent: Dict[Hashable, Hashable] = {bid: (b.quotient_id if b.quotient_id is not None else bid) for bid, b in by_id.items()}

        rels: List[BranchRelation] = []
        if relations is not None:
            for r in relations:
                if isinstance(r, BranchRelation):
                    rels.append(r)
                elif isinstance(r, Mapping):
                    rels.append(BranchRelation.from_mapping(r))

        # Do not infer cross-branch relief, rivalry, similarity, or quotient
        # relations merely from scalar closeness.  Scalar closeness made RCF v1
        # behave like a global burden/grey modifier: stable low-debt branches
        # could become relief branches, and close debtful branches could preserve
        # grey without any lawful relation support.  Branch interactions below
        # therefore require explicit relation inputs from the caller or row-level
        # relation hints extracted by apply_continuation_field.

        for rel in rels:
            s = by_id.get(rel.source)
            t = by_id.get(rel.target)
            if s is None or t is None or s.branch_id == t.branch_id:
                continue
            relation_count[s.branch_id] = relation_count.get(s.branch_id, 0) + 1
            relation_count[t.branch_id] = relation_count.get(t.branch_id, 0) + 1
            w = clamp01(rel.weight)
            prox = self.proximity(s, t)
            rel_w = clamp01(w * (0.35 + 0.65 * prox))
            typ = rel.relation_type
            if typ in {"relief", "burden_relief", "debt_relief"}:
                # Source branch becomes more viable insofar as it can relieve a
                # target branch's unresolved debt.  The target is not magically
                # fixed before the source is actually chosen, but collapse onto
                # the target is made less cheap by extra grey pressure.
                relief_support[s.branch_id] = clamp01(relief_support[s.branch_id] + rel_w * field_debt[t.branch_id] * (0.45 + 0.55 * p["path"]))
                grey_pressure[t.branch_id] = clamp01(grey_pressure[t.branch_id] + 0.18 * rel_w * field_debt[t.branch_id] * p["nonclosure"])
            elif typ in {"cancellation", "cancel", "compensation"}:
                cancel_power = rel_w * max(s.relief_capacity, s.viability) * (0.40 + 0.60 * p["path"])
                field_debt[t.branch_id] = clamp01(field_debt[t.branch_id] * (1.0 - 0.55 * cancel_power))
                relief_support[s.branch_id] = clamp01(relief_support[s.branch_id] + 0.35 * cancel_power)
            elif typ in {"equivalence", "quotient", "merge"}:
                qid = min(str(quotient_parent[s.branch_id]), str(quotient_parent[t.branch_id]))
                quotient_parent[s.branch_id] = qid
                quotient_parent[t.branch_id] = qid
                shared = min(field_debt[s.branch_id], field_debt[t.branch_id])
                field_debt[s.branch_id] = clamp01(0.72 * field_debt[s.branch_id] + 0.28 * shared)
                field_debt[t.branch_id] = clamp01(0.72 * field_debt[t.branch_id] + 0.28 * shared)
                grey_pressure[s.branch_id] = clamp01(grey_pressure[s.branch_id] * (1.0 - 0.20 * rel_w))
                grey_pressure[t.branch_id] = clamp01(grey_pressure[t.branch_id] * (1.0 - 0.20 * rel_w))
            elif typ in {"similarity", "proximity", "shared_evidence", "hiddenness_reduction", "exposure"}:
                avg_uncertainty = 0.5 * (s.uncertainty + t.uncertainty)
                spread = abs(s.viability - t.viability)
                shared_grey = rel_w * (0.35 * avg_uncertainty + 0.35 * (1.0 - spread) + 0.30 * max(s.debt, t.debt)) * p["nonclosure"]
                grey_pressure[s.branch_id] = clamp01(grey_pressure[s.branch_id] + 0.35 * shared_grey)
                grey_pressure[t.branch_id] = clamp01(grey_pressure[t.branch_id] + 0.35 * shared_grey)
                if typ in {"hiddenness_reduction", "exposure"}:
                    relief_support[s.branch_id] = clamp01(relief_support[s.branch_id] + 0.12 * rel_w * t.uncertainty)
            elif typ in {"buffering", "shielding", "absorption"}:
                # Buffering prevents some tension from becoming operative burden
                # at the target.  It is weaker than cancellation: the condition
                # remains, but less of it converts into field debt.
                buffer_power = rel_w * max(s.viability, s.relief_capacity) * (0.30 + 0.50 * p["local"] + 0.20 * (1.0 - p["hidden"]))
                field_debt[t.branch_id] = clamp01(field_debt[t.branch_id] * (1.0 - 0.30 * buffer_power))
                grey_pressure[t.branch_id] = clamp01(grey_pressure[t.branch_id] * (1.0 - 0.18 * buffer_power))
                relief_support[s.branch_id] = clamp01(relief_support[s.branch_id] + 0.10 * buffer_power)
            elif typ in {"dependency", "burden_transfer", "burden_transform"}:
                dep_pressure = rel_w * (0.30 * field_debt[t.branch_id] + 0.25 * t.uncertainty + 0.20 * p["path"] + 0.25 * p["revision"])
                grey_pressure[s.branch_id] = clamp01(grey_pressure[s.branch_id] + 0.22 * dep_pressure)
                grey_pressure[t.branch_id] = clamp01(grey_pressure[t.branch_id] + 0.22 * dep_pressure)
            elif typ in {"phase_shift", "critical_proximity"}:
                critical = rel_w * (0.40 * max(field_debt[s.branch_id], field_debt[t.branch_id]) + 0.30 * p["consequence"] + 0.30 * p["nonclosure"])
                grey_pressure[s.branch_id] = clamp01(grey_pressure[s.branch_id] + 0.28 * critical)
                grey_pressure[t.branch_id] = clamp01(grey_pressure[t.branch_id] + 0.28 * critical)
            elif typ in {"competition", "rivalry", "exclusive"}:
                closeness = 1.0 - abs(s.viability - t.viability)
                rivalry = rel_w * closeness * (0.45 * p["rival"] + 0.35 * p["revision"] + 0.20 * p["nonlocal"])
                grey_pressure[s.branch_id] = clamp01(grey_pressure[s.branch_id] + 0.32 * rivalry)
                grey_pressure[t.branch_id] = clamp01(grey_pressure[t.branch_id] + 0.32 * rivalry)

        quotient_counts: Dict[Hashable, int] = {}
        for q in quotient_parent.values():
            quotient_counts[q] = quotient_counts.get(q, 0) + 1

        out: Dict[Hashable, FieldBranchState] = {}
        for bid, b in by_id.items():
            debt = clamp01(field_debt[bid])
            relief = clamp01(relief_support[bid])
            grey = clamp01(grey_pressure[bid])
            qid = quotient_parent[bid]
            quotient_bonus = clamp01(0.08 * max(0, quotient_counts.get(qid, 1) - 1))
            recursion = clamp01(
                b.recursion_budget
                + p["nonclosure"] * (0.30 * grey + 0.28 * debt + 0.18 * b.uncertainty + 0.14 * (1.0 - b.viability) + 0.10 * relief)
            )
            field_viability = clamp01(
                0.34 * b.viability
                + 0.24 * b.support
                + 0.18 * relief
                + 0.08 * quotient_bonus
                - 0.26 * debt * (0.55 + 0.45 * p["path"])
                - 0.14 * grey * (0.45 + 0.55 * p["revision"])
                - 0.08 * b.instability
            )
            collapse_ready = clamp01(
                0.36 * field_viability
                + 0.24 * b.support
                + 0.18 * p["collapse_bias"]
                + 0.08 * quotient_bonus
                - 0.28 * debt * (0.55 + 0.45 * p["nonlocal"])
                - 0.22 * grey
                - 0.08 * b.uncertainty
            )
            out[bid] = FieldBranchState(
                branch_id=bid,
                support=clamp01(b.support),
                local_support=clamp01(b.local_support),
                base_viability=clamp01(b.viability),
                field_viability=field_viability,
                field_debt=debt,
                field_relief_support=relief,
                field_grey_pressure=grey,
                field_recursion_budget=recursion,
                field_collapse_readiness=collapse_ready,
                quotient_id=qid,
                quotient_share_count=quotient_counts.get(qid, 1),
                field_relation_count=int(relation_count.get(bid, 0)),
            )
        return out


def _relations_from_rows(rows: Iterable[Mapping[str, Any]]) -> List[BranchRelation]:
    """Compatibility reader for relation telemetry already attached to candidate rows."""
    """Extract explicit generic branch relations embedded in candidate rows.

    Accepted row fields are intentionally generic: branch_relations,
    continuation_relations, or relations.  A relation may omit source, in which
    case the source is the row's own branch id.  This lets adapters publish
    lawful public relation structure without letting the field inspect action or
    problem-family names.
    """
    out: List[BranchRelation] = []
    for row in rows:
        source = branch_key_from_row(row)
        bundles = []
        for key in ("branch_relations", "continuation_relations", "relations"):
            value = row.get(key)
            if value is None:
                continue
            if isinstance(value, Mapping):
                bundles.append(value)
            elif isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
                bundles.extend([v for v in value if isinstance(v, Mapping)])
        for rel in bundles:
            data = dict(rel)
            data.setdefault("source", source)
            if data.get("target") is None:
                continue
            out.append(BranchRelation.from_mapping(data))
    return out


def apply_continuation_field(rows: List[Dict[str, Any]], controls: Optional[Mapping[str, Any]] = None, relations: Optional[Iterable[BranchRelation | Mapping[str, Any]]] = None) -> List[Dict[str, Any]]:
    """Apply RCF update and attach field state to the candidate rows consumed downstream."""
    """Apply minimal continuation-field deformation to candidate rows."""
    if not rows:
        return []
    branches = [ContinuationBranch.from_row(r) for r in rows]
    effective_relations = relations if relations is not None else _relations_from_rows(rows)
    states = ContinuationField(controls=controls).update(branches, relations=effective_relations)
    out: List[Dict[str, Any]] = []
    for row in rows:
        nr = dict(row)
        bid = branch_key_from_row(row)
        st = states.get(bid)
        if st is None:
            out.append(nr)
            continue
        field_viability = clamp01(st.field_viability)
        field_debt = clamp01(st.field_debt)
        relief = clamp01(st.field_relief_support)
        grey = clamp01(st.field_grey_pressure)
        collapse_ready = clamp01(st.field_collapse_readiness)
        nr["field_viability"] = field_viability
        nr["field_debt"] = field_debt
        nr["field_relief_support"] = relief
        nr["field_grey_pressure"] = grey
        nr["field_recursion_budget"] = clamp01(st.field_recursion_budget)
        nr["field_collapse_readiness"] = collapse_ready
        nr["quotient_id"] = str(st.quotient_id)
        nr["quotient_share_count"] = int(st.quotient_share_count)
        nr["field_relation_count"] = int(st.field_relation_count)
        # Conservative integration: reshape existing fields, but do not replace
        # them wholesale.  This keeps v1 diagnostic rather than a benchmark tune.
        nr["continuation_viability"] = clamp01(0.72 * clamp01(nr.get("continuation_viability", field_viability)) + 0.28 * field_viability)
        nr["preventive_support"] = clamp01(0.70 * clamp01(nr.get("preventive_support", 0.0)) + 0.30 * relief)
        nr["burden_accumulation"] = clamp01(max(clamp01(nr.get("burden_accumulation", 0.0)), field_debt))
        nr["fracture_state"] = clamp01(max(clamp01(nr.get("fracture_state", 0.0)), 0.42 * field_debt + 0.28 * grey))
        nr["decision_state"] = clamp01(
            0.76 * clamp01(nr.get("decision_state", 0.0))
            + 0.14 * field_viability
            + 0.12 * relief
            + 0.08 * collapse_ready
            - 0.16 * field_debt
            - 0.08 * grey
        )
        nr["commitment_stability"] = clamp01(0.68 * clamp01(nr.get("commitment_stability", 0.0)) + 0.20 * collapse_ready + 0.12 * field_viability - 0.10 * grey)
        out.append(nr)
    return out
