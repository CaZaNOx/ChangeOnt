"""Relation-field concentration telemetry.

This helper implements a bounded CO-faithful summary of the idea that
function-like behavior is an earned collapse of a many-valued relation-field.
It does *not* create a full probability model, choose actions, use reward, read
hidden state, or inspect native action names.  It summarizes public effect mass
across generic relation domains so downstream surfaces can ask whether a local
relation is concentrated enough to be treated as function-like under the current
shape/gauge.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Hashable, Iterable, Mapping, Sequence

from agents.co.runtime.surfaces.continuation_field import clamp01


# Operation classes are intentionally generic.  They describe public relation
# grammar, not native task actions or policy labels.
CARRIER_OPS = {"carry", "increase", "amplify", "consume", "require", "mask", "postpone", "hide", "threshold", "phase_shift"}
RESOLVER_OPS = {"reduce", "relieve", "prevent", "reset", "cancel", "reveal", "expose", "reduce_hiddenness", "buffer", "absorb"}
REDIRECT_OPS = {"transform", "transfer"}
PROCEDURAL_OPS = {"decision_slot", "single_decision_slot"}


@dataclass(frozen=True)
class RelationFieldConcentration:
    branch_id: Hashable
    domain: str
    domain_mass: float
    total_domain_mass: float
    concentration: float
    ambiguity: float
    domain_ambiguity: float
    function_like_threshold: float
    function_like: bool
    dominant_operation_class: str
    row_count_in_domain: int

    def to_dict(self) -> Dict[str, Any]:
        out = asdict(self)
        out["branch_id"] = str(self.branch_id)
        return out


def _f(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return float(default)


def _op_class(op: str) -> str:
    op = str(op or "").strip().lower()
    if op in RESOLVER_OPS:
        return "resolver"
    if op in CARRIER_OPS:
        return "carrier"
    if op in REDIRECT_OPS:
        return "redirect"
    if op in PROCEDURAL_OPS:
        return "procedural"
    if op:
        return "other"
    return "unknown"


def _domain_for_effect(effect: Any) -> str:
    burden = str(getattr(effect, "burden_type", "") or "").strip().lower()
    scope = str(getattr(effect, "relation_scope", "") or "").strip().lower()
    if burden:
        return f"burden:{burden}"
    if scope:
        return f"scope:{scope}"
    return "unknown"


def _threshold_from_controls(controls: Mapping[str, Any] | None) -> float:
    """Return shape/gauge threshold for function-like collapse.

    Higher coarsening/collapse permission allows earlier function-like collapse;
    higher dynamic urgency/path-sensitivity/contradiction sensitivity demands
    stronger concentration before the relation is treated as function-like.
    """
    c = dict(controls or {})
    coarsening = clamp01(_f(c.get("dynamic_shape_coarsening", 0.0), 0.0))
    urgency = clamp01(_f(c.get("dynamic_shape_urgency", 0.0), 0.0))
    collapse = clamp01(_f(c.get("collapse_admissibility", c.get("collapse_permission", 0.5)), 0.5))
    local = clamp01(_f(c.get("local_authority", 0.5), 0.5))
    path = clamp01(_f(c.get("path_sensitivity", 0.5), 0.5))
    contra = clamp01(_f(c.get("contradiction_sensitivity", 0.5), 0.5))
    # Conservative default: two-way near-even relations are not function-like;
    # strong one-sided relations are.  Shape can move the threshold but not below
    # a still-material concentration demand.
    return clamp01(0.74 - 0.16 * coarsening - 0.09 * collapse - 0.05 * local + 0.10 * urgency + 0.06 * path + 0.05 * contra)


def derive_relation_field_concentration(
    effects_by_branch: Mapping[Hashable, Sequence[Any]],
    controls: Mapping[str, Any] | None = None,
) -> tuple[Dict[Hashable, RelationFieldConcentration], Dict[str, Any]]:
    """Summarize how concentrated public relation mass is by generic domain.

    Input effects should be already validated public facts.  The helper assumes
    no hidden access and refuses to use native action names or rewards.
    """
    threshold = _threshold_from_controls(controls)
    domain_branch_mass: Dict[str, Dict[Hashable, float]] = {}
    domain_op_mass: Dict[tuple[str, Hashable, str], float] = {}

    for bid, effects in effects_by_branch.items():
        for eff in effects:
            op = str(getattr(eff, "operation", "") or "").lower()
            cls = _op_class(op)
            if cls == "procedural":
                continue
            domain = _domain_for_effect(eff)
            if domain == "unknown":
                continue
            weight = clamp01(_f(getattr(eff, "weight", 0.0), 0.0))
            if weight <= 0.0:
                continue
            domain_branch_mass.setdefault(domain, {})[bid] = clamp01(domain_branch_mass.setdefault(domain, {}).get(bid, 0.0) + weight)
            key = (domain, bid, cls)
            domain_op_mass[key] = clamp01(domain_op_mass.get(key, 0.0) + weight)

    per_branch: Dict[Hashable, RelationFieldConcentration] = {}
    all_concentrations = []
    domain_ambiguities = []
    function_like_count = 0
    ambiguous_count = 0
    domains_seen = set(domain_branch_mass.keys())

    for domain, masses in domain_branch_mass.items():
        total = sum(float(v) for v in masses.values())
        if total <= 0.0:
            continue
        row_count = len(masses)
        max_share = max(float(v) / total for v in masses.values()) if masses else 0.0
        domain_ambiguity = clamp01(1.0 - max_share)
        domain_ambiguities.append(domain_ambiguity)
        for bid, mass in masses.items():
            share = clamp01(float(mass) / total)
            # Function-like collapse is a property of the domain distribution,
            # not simply the selected row.  A row is function-like only if it is
            # the dominant carrier of that public relation domain.
            is_dominant = abs(share - max_share) < 1e-9 and share >= threshold
            op_masses = {
                cls: domain_op_mass.get((domain, bid, cls), 0.0)
                for cls in ("carrier", "resolver", "redirect", "other", "unknown")
            }
            dominant_cls = max(op_masses.items(), key=lambda kv: kv[1])[0] if op_masses else "unknown"
            rec = RelationFieldConcentration(
                branch_id=bid,
                domain=domain,
                domain_mass=clamp01(mass),
                total_domain_mass=clamp01(total),
                concentration=share,
                ambiguity=clamp01(1.0 - share),
                domain_ambiguity=domain_ambiguity,
                function_like_threshold=threshold,
                function_like=bool(is_dominant),
                dominant_operation_class=dominant_cls,
                row_count_in_domain=row_count,
            )
            # Preserve the strongest concentration profile per branch.
            prev = per_branch.get(bid)
            if prev is None or rec.concentration > prev.concentration:
                per_branch[bid] = rec
            all_concentrations.append(share)
            if is_dominant:
                function_like_count += 1
            if share < threshold and row_count > 1:
                ambiguous_count += 1

    avg_conc = sum(all_concentrations) / len(all_concentrations) if all_concentrations else 0.0
    avg_domain_ambiguity = sum(domain_ambiguities) / len(domain_ambiguities) if domain_ambiguities else 0.0
    telemetry = {
        "relation_field_domains": len(domains_seen),
        "relation_field_profiles": len(all_concentrations),
        "relation_field_avg_concentration": float(avg_conc),
        "relation_field_avg_domain_ambiguity": float(avg_domain_ambiguity),
        "relation_field_function_like_count": int(function_like_count),
        "relation_field_ambiguous_count": int(ambiguous_count),
        "relation_field_function_like_threshold": float(threshold),
    }
    return per_branch, telemetry
