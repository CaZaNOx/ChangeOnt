from __future__ import annotations

"""Context-conditioned expectation audit v1.

Diagnostic-only audit. It does not change runtime behavior and does not judge
mechanism relevance from global action-difference counts alone. Instead it first
classifies each full-current decision step by public shape/gauge context and
local public structural triggers, then asks whether each mechanism matters in
contexts where CO would expect it to matter.

The audit is deliberately conservative: action changes are not required in all
strong contexts, but strong contexts with neither action change nor gate/readout
telemetry are flagged as suspicious non-effects.
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, List, Mapping, Tuple

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

OUT_DIR = ROOT / "outputs" / "current_kernel_diagnostic_map_v1"
STEPS_JSONL = OUT_DIR / "steps.jsonl"
JSON_OUT = ROOT / "outputs" / "context_conditioned_expectation_audit_v1.json"
REPORT_MD = ROOT.parent / "CONTEXT_CONDITIONED_EXPECTATION_AUDIT_REPORT_2026-05-25.md"

CLAIM_BOUNDARY = (
    "Context-conditioned expectation audit only. It uses public shape/gauge telemetry, public relation/burden/sequence/certificate signals, "
    "and named ablations from the diagnostic map. It is not a benchmark, not CO proof, not a tuning license, and not a kernel change."
)

MECHANISMS = ("dynamic_shape", "sequence", "quotient", "recursion")
ABLATION_FOR = {
    "dynamic_shape": "static_shape",
    "sequence": "no_sequence",
    "quotient": "no_quotient",
    "recursion": "no_scheduler",
}


def _load_steps() -> List[Dict[str, Any]]:
    if not STEPS_JSONL.exists():
        raise FileNotFoundError(f"missing {STEPS_JSONL}; run experiments.studies.current_kernel_diagnostic_map_v1 first")
    rows: List[Dict[str, Any]] = []
    with STEPS_JSONL.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def _f(x: Any, default: float = 0.0) -> float:
    try:
        return float(x)
    except Exception:
        return default


def _mean(xs: Iterable[float]) -> float:
    vals = [float(x) for x in xs]
    return float(mean(vals)) if vals else 0.0


def _safe_action(x: Any) -> str:
    return json.dumps(x, sort_keys=True) if not isinstance(x, str) else x


def _assessment_values(step: Mapping[str, Any]) -> List[Mapping[str, Any]]:
    ass = step.get("canonical_commitment_assessment_summary", {})
    if not isinstance(ass, dict):
        return []
    vals = []
    for v in ass.values():
        if isinstance(v, dict):
            vals.append(v)
    return vals


def _selected_assessment(step: Mapping[str, Any]) -> Mapping[str, Any]:
    ass = step.get("canonical_commitment_assessment_summary", {})
    if not isinstance(ass, dict):
        return {}
    action = step.get("action")
    candidates = [str(action), _safe_action(action)]
    for key in candidates:
        if isinstance(ass.get(key), dict):
            return ass[key]
    # Fall back to the highest dominance row if the action key is not represented.
    vals = _assessment_values(step)
    if not vals:
        return {}
    return max(vals, key=lambda v: _f(v.get("dominance_score")))


def _shape_context(step: Mapping[str, Any]) -> Dict[str, Any]:
    dc = step.get("direct_controls_used", {}) if isinstance(step.get("direct_controls_used"), dict) else {}
    gauge = step.get("local_shape_gauge", {}) if isinstance(step.get("local_shape_gauge"), dict) else {}
    hidden_decisiveness = _f(dc.get("shape_hidden_decisiveness", 0.0))
    local_cue_reliability = _f(dc.get("shape_local_cue_reliability", 0.5))
    consequence_span = _f(dc.get("shape_consequence_span", 0.0))
    revision_cost = _f(dc.get("shape_revision_cost", 0.0))
    topology_constraint = _f(dc.get("shape_topology_constraint", 0.0))
    reshapeability = _f(dc.get("shape_reshapeability", 0.0))
    dyn_urgency = _f(dc.get("dynamic_shape_urgency", 0.0))
    projection = _f(dc.get("dynamic_shape_projection_horizon", 0.0))
    coarsening = _f(dc.get("dynamic_shape_coarsening", 0.0))
    path_sensitivity = _f(dc.get("path_sensitivity", 0.0))
    collapse_admissibility = _f(dc.get("collapse_admissibility", 0.0))
    revision_permissibility = _f(dc.get("revision_permissibility", 0.0))
    hidden_risk = hidden_decisiveness * max(0.0, 1.0 - local_cue_reliability)
    commitment_risk = _mean([consequence_span, revision_cost, max(0.0, 1.0 - revision_permissibility), path_sensitivity])
    shape_risk = _mean([hidden_risk, commitment_risk, dyn_urgency, projection])
    return {
        "hidden_decisiveness": hidden_decisiveness,
        "local_cue_reliability": local_cue_reliability,
        "hidden_risk": hidden_risk,
        "consequence_span": consequence_span,
        "revision_cost": revision_cost,
        "topology_constraint": topology_constraint,
        "reshapeability": reshapeability,
        "dynamic_shape_urgency": dyn_urgency,
        "projection_horizon": projection,
        "coarsening": coarsening,
        "path_sensitivity": path_sensitivity,
        "collapse_admissibility": collapse_admissibility,
        "revision_permissibility": revision_permissibility,
        "shape_risk": shape_risk,
        "preblocking_min_carrier_pressure": _f(gauge.get("preblocking_min_carrier_pressure", 0.0)),
        "carrier_pressure_for_timing": _f(gauge.get("carrier_pressure_for_timing", 0.0)),
        "local_shape_urgency": _f(gauge.get("local_shape_urgency", 0.0)),
    }


def _local_triggers(step: Mapping[str, Any]) -> Dict[str, Any]:
    rel = step.get("relations_by_type", {}) if isinstance(step.get("relations_by_type"), dict) else {}
    rows = step.get("row_trace_sample", []) if isinstance(step.get("row_trace_sample"), list) else []
    ass_vals = _assessment_values(step)
    sel = _selected_assessment(step)
    relation_resolver_count = sum(int(rel.get(k, 0) or 0) for k in ("relief", "cancellation", "buffer", "exposure"))
    strong_rival_count = sum(int(rel.get(k, 0) or 0) for k in ("rivalry", "exclusion", "contradiction"))
    weak_competition_count = int(rel.get("decision_slot_competition", 0) or 0)
    sequence_active_rows = int(step.get("sequence_rows", 0) or 0)
    max_seq_support = _f(step.get("max_sequence_composition_support", 0.0))
    seq_transitions = Counter(str(r.get("sequence_phase_transition")) for r in rows if r.get("sequence_composition_active"))
    phases = Counter(str(r.get("continuation_phase")) for r in rows if r.get("continuation_phase") is not None)
    has_exposure_phase = any("reveal" in p or "expose" in p for p in list(phases) + list(seq_transitions))
    has_relief_phase = any("relieve" in p or "reduce" in p or "cancel" in p or "buffer" in p for p in list(phases) + list(seq_transitions))
    has_carry_phase = any("carry" in p or "unresolved" in p for p in list(phases) + list(seq_transitions))
    max_carrier_pressure = max([_f(v.get("carrier_only_pressure")) for v in ass_vals] + [0.0])
    max_resolver_support = max([_f(v.get("resolver_support")) for v in ass_vals] + [0.0])
    avg_collapse_blocked = _mean([_f(v.get("collapse_blocked")) for v in ass_vals])
    avg_recursion_cert = _mean([_f(v.get("collapse_certificate_recursion_demand")) for v in ass_vals])
    dominance_margin = _f(sel.get("dominance_score")) - max([_f(v.get("dominance_score")) for v in ass_vals if v is not sel] + [0.0])
    positive_mass = _f(sel.get("dominance_positive_mass"))
    ssf = (_f(sel.get("dominance_support_component")) + _f(sel.get("dominance_stability_component")) + _f(sel.get("dominance_field_component")))
    ssf_share = ssf / positive_mass if positive_mass > 1e-9 else 0.0
    penalty_ratio = _f(sel.get("dominance_negative_mass")) / positive_mass if positive_mass > 1e-9 else 0.0
    quotient_rows = int(step.get("quotient_rows", 0) or 0)
    quotient_multi = int(step.get("quotient_buckets_with_multiple_members", 0) or 0)
    quotient_accepted = int(step.get("quotient_profiles_accepted", 0) or 0)
    unresolved_burden = bool(_f(step.get("avg_field_debt")) >= 0.18 or max_carrier_pressure >= 0.55 or _f(step.get("max_field_grey_pressure")) >= 0.10)
    collapse_blocked = bool(_f(step.get("avg_collapse_blockers")) > 0 or avg_collapse_blocked >= 0.20)
    # Resolver alternatives must be public-structural, not merely a high resolver_support score.
    # High score alone would reintroduce the aggregate/score-first mistake this audit is meant to avoid.
    resolver_alt = bool(relation_resolver_count > 0 or has_relief_phase)
    return {
        "relation_resolver_count": relation_resolver_count,
        "strong_rival_count": strong_rival_count,
        "weak_competition_count": weak_competition_count,
        "sequence_active_rows": sequence_active_rows,
        "max_sequence_support": max_seq_support,
        "sequence_transitions": dict(seq_transitions),
        "phases": dict(phases),
        "has_exposure_phase": has_exposure_phase,
        "has_relief_phase": has_relief_phase,
        "has_carry_phase": has_carry_phase,
        "max_carrier_pressure": max_carrier_pressure,
        "max_resolver_support": max_resolver_support,
        "avg_collapse_blocked": avg_collapse_blocked,
        "avg_recursion_cert": avg_recursion_cert,
        "dominance_margin": dominance_margin,
        "support_stability_field_share": ssf_share,
        "penalty_ratio": penalty_ratio,
        "quotient_rows": quotient_rows,
        "quotient_multi": quotient_multi,
        "quotient_accepted": quotient_accepted,
        "unresolved_burden": unresolved_burden,
        "collapse_blocked": collapse_blocked,
        "resolver_alt": resolver_alt,
    }


def _expected_levels(step: Mapping[str, Any], shape: Mapping[str, Any], trig: Mapping[str, Any]) -> Dict[str, str]:
    dyn_applied = bool(step.get("dynamic_shape_applied"))
    dyn_relevant = dyn_applied and (
        _f(shape["dynamic_shape_urgency"]) >= 0.35
        or _f(shape["projection_horizon"]) >= 0.35
        or _f(shape["coarsening"]) >= 0.20
    ) and (bool(trig["unresolved_burden"]) or bool(trig["resolver_alt"]) or _f(trig["sequence_active_rows"]) > 0)

    seq_present = int(trig["sequence_active_rows"]) > 0 or _f(trig["max_sequence_support"]) > 0.08
    seq_strong = seq_present and bool(trig["resolver_alt"]) and bool(trig["unresolved_burden"]) and (
        _f(shape["dynamic_shape_urgency"]) >= 0.20
        or _f(shape["local_shape_urgency"]) >= 0.30
        or _f(shape["path_sensitivity"]) >= 0.50
        or bool(trig["collapse_blocked"])
    )

    quotient_strong = int(trig["quotient_multi"]) > 0 or int(trig["quotient_rows"]) > 0
    quotient_weak = int(trig["quotient_accepted"]) > 0

    recursion_strong = (
        _f(step.get("avg_recursion_scheduler_structural_channel")) >= 0.25
        or bool(trig["collapse_blocked"])
        or (int(trig["strong_rival_count"]) > 0 and bool(trig["unresolved_burden"]))
    ) and not (int(trig["weak_competition_count"]) > 0 and int(trig["strong_rival_count"]) == 0 and not bool(trig["collapse_blocked"]))
    recursion_weak = _f(step.get("avg_recursion_scheduler_demand")) > 0.05 or _f(trig["avg_recursion_cert"]) > 0.05

    return {
        "dynamic_shape": "strong" if dyn_relevant else ("weak" if dyn_applied else "none"),
        "sequence": "strong" if seq_strong else ("weak" if seq_present else "none"),
        "quotient": "strong" if quotient_strong else ("weak" if quotient_weak else "none"),
        "recursion": "strong" if recursion_strong else ("weak" if recursion_weak else "none"),
    }


def _mechanism_gate_effect(mech: str, step: Mapping[str, Any], trig: Mapping[str, Any]) -> bool:
    if mech == "dynamic_shape":
        return bool(step.get("dynamic_shape_controls_applied_in_commitment")) and (
            bool(step.get("shape_gauged_resolver_timing_applied"))
            or _f(step.get("avg_recursion_scheduler_structural_channel")) >= 0.20
            or _f(trig.get("penalty_ratio")) >= 0.18
        )
    if mech == "sequence":
        return bool(step.get("shape_gauged_resolver_timing_applied")) or bool(step.get("certificate_aware_reopen_or_sample_applied")) or _f(trig.get("max_sequence_support")) >= 0.22
    if mech == "quotient":
        return int(step.get("quotient_rows", 0) or 0) > 0 or int(step.get("quotient_buckets_with_multiple_members", 0) or 0) > 0
    if mech == "recursion":
        return _f(step.get("avg_recursion_scheduler_structural_channel")) >= 0.20 or _f(trig.get("avg_recursion_cert")) >= 0.20
    return False


def _action_changed(index: Mapping[Tuple[str, str, int, int, str], Mapping[str, Any]], step: Mapping[str, Any], ablation: str) -> bool:
    key = (str(step.get("family")), str(step.get("mode")), int(step.get("seed", 0)), int(step.get("t", 0)), ablation)
    alt = index.get(key)
    if not alt:
        return False
    return _safe_action(alt.get("action")) != _safe_action(step.get("action"))


def _verdict(expected: str, action_changed: bool, gate_effect: bool) -> str:
    if expected == "none":
        return "expected_non_effect" if not action_changed else "unexpected_action_effect"
    if expected == "weak":
        if action_changed:
            return "weak_context_action_effect"
        if gate_effect:
            return "weak_context_gate_effect"
        return "acceptable_telemetry_only_or_non_effect"
    if expected == "strong":
        if action_changed:
            return "strong_context_action_effect"
        if gate_effect:
            return "strong_context_gate_effect_only"
        return "suspicious_strong_context_non_effect"
    return "unknown"


def main() -> Dict[str, Any]:
    steps = _load_steps()
    index: Dict[Tuple[str, str, int, int, str], Dict[str, Any]] = {}
    for s in steps:
        index[(str(s.get("family")), str(s.get("mode")), int(s.get("seed", 0)), int(s.get("t", 0)), str(s.get("variant")))] = s

    full = [s for s in steps if s.get("variant") == "full_current"]
    counts: Dict[str, Counter] = {m: Counter() for m in MECHANISMS}
    by_family: Dict[str, Dict[str, Counter]] = defaultdict(lambda: {m: Counter() for m in MECHANISMS})
    strong_cases: Dict[str, List[Dict[str, Any]]] = {m: [] for m in MECHANISMS}
    suspicious_cases: Dict[str, List[Dict[str, Any]]] = {m: [] for m in MECHANISMS}
    bucket_counts = Counter()

    for s in full:
        shape = _shape_context(s)
        trig = _local_triggers(s)
        expected = _expected_levels(s, shape, trig)
        fm = f"{s.get('family')}/{s.get('mode')}"
        # High-level context bucket labels for human audit.
        labels: List[str] = []
        if trig["unresolved_burden"] and trig["resolver_alt"]:
            labels.append("carrier_plus_resolver")
        if trig["sequence_active_rows"]:
            labels.append("sequence_present")
        if shape["dynamic_shape_urgency"] >= 0.30 or shape["projection_horizon"] >= 0.30:
            labels.append("dynamic_shape_relevant")
        if trig["collapse_blocked"]:
            labels.append("collapse_blocked_or_grey")
        if trig["quotient_rows"] or trig["quotient_multi"]:
            labels.append("quotient_active")
        if not labels:
            labels.append("simple_or_low_structural_trigger")
        for lab in labels:
            bucket_counts[lab] += 1

        for mech in MECHANISMS:
            exp = expected[mech]
            changed = _action_changed(index, s, ABLATION_FOR[mech])
            gate = _mechanism_gate_effect(mech, s, trig)
            vd = _verdict(exp, changed, gate)
            counts[mech][f"expected_{exp}"] += 1
            counts[mech][vd] += 1
            by_family[fm][mech][f"expected_{exp}"] += 1
            by_family[fm][mech][vd] += 1
            if exp == "strong":
                sample = {
                    "family": s.get("family"),
                    "mode": s.get("mode"),
                    "t": s.get("t"),
                    "action": s.get("action"),
                    "expected": exp,
                    "verdict": vd,
                    "action_changed_under_ablation": changed,
                    "gate_effect": gate,
                    "context_labels": labels,
                    "shape": {k: round(_f(v), 4) if isinstance(v, (int, float)) else v for k, v in shape.items()},
                    "triggers": {k: (round(_f(v), 4) if isinstance(v, (int, float)) else v) for k, v in trig.items() if k not in ("sequence_transitions", "phases")},
                    "relations_by_type": s.get("relations_by_type"),
                    "commitment_mode": s.get("canonical_commitment_mode"),
                    "commitment_reason": s.get("canonical_commitment_reason"),
                }
                if len(strong_cases[mech]) < 10:
                    strong_cases[mech].append(sample)
                if vd == "suspicious_strong_context_non_effect" and len(suspicious_cases[mech]) < 12:
                    suspicious_cases[mech].append(sample)

    # Findings from counts.
    findings: List[Dict[str, Any]] = []
    for mech in MECHANISMS:
        c = counts[mech]
        strong = c.get("expected_strong", 0)
        suspicious = c.get("suspicious_strong_context_non_effect", 0)
        action_effect = c.get("strong_context_action_effect", 0)
        gate_effect = c.get("strong_context_gate_effect_only", 0)
        rate = suspicious / strong if strong else 0.0
        if strong and rate >= 0.50:
            sev = "high" if rate >= 0.75 else "medium"
            findings.append({
                "id": f"CCE_{mech.upper()}_STRONG_CONTEXT_UNDERCONSUMPTION",
                "severity": sev,
                "finding": f"{mech} has many strong-context cases without action or gate/readout effect.",
                "evidence": f"strong={strong}, suspicious={suspicious}, action_effect={action_effect}, gate_effect_only={gate_effect}, suspicious_rate={rate:.3f}",
                "next_action": "Audit readout consumption before changing concepts or tuning family-specific behavior.",
            })
        elif strong:
            findings.append({
                "id": f"CCE_{mech.upper()}_STRONG_CONTEXT_PARTIALLY_CONSUMED",
                "severity": "low",
                "finding": f"{mech} strong-context cases show at least some action/gate consumption.",
                "evidence": f"strong={strong}, suspicious={suspicious}, action_effect={action_effect}, gate_effect_only={gate_effect}, suspicious_rate={rate:.3f}",
                "next_action": "Keep in mechanism map; inspect representative misses before changing runtime.",
            })
        else:
            findings.append({
                "id": f"CCE_{mech.upper()}_NO_STRONG_CONTEXTS_IN_CAPPED_TRACE",
                "severity": "low",
                "finding": f"No strong expected {mech} contexts were classified in the capped trace.",
                "evidence": f"expected_weak={c.get('expected_weak', 0)}, expected_none={c.get('expected_none', 0)}",
                "next_action": "Do not infer mechanism weakness from this trace; design targeted contexts if the mechanism matters conceptually.",
            })

    out = {
        "study": "context_conditioned_expectation_audit_v1",
        "claim_boundary": CLAIM_BOUNDARY,
        "source": str(STEPS_JSONL.relative_to(ROOT)),
        "full_current_steps": len(full),
        "context_bucket_counts": dict(bucket_counts),
        "mechanism_counts": {m: dict(c) for m, c in counts.items()},
        "by_family_mode": {fm: {m: dict(c) for m, c in mm.items()} for fm, mm in sorted(by_family.items())},
        "strong_case_samples": strong_cases,
        "suspicious_case_samples": suspicious_cases,
        "findings": findings,
        "verdict": {
            "aggregate_action_counts_were_insufficient": True,
            "context_conditioning_added": True,
            "strong_context_suspicion_remaining": any(f["severity"] in {"medium", "high"} for f in findings),
            "kernel_change_made": False,
            "next_recommended_step": "inspect strong-context suspicious cases and decide whether readout consumption is a wiring/formula bug, legitimate non-effect, or architecture limitation",
        },
    }
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
    _write_report(out)
    print(json.dumps(out["verdict"], indent=2, sort_keys=True))
    return out


def _write_report(data: Mapping[str, Any]) -> None:
    mech_lines = []
    for mech, c in data["mechanism_counts"].items():
        mech_lines.append(
            f"| {mech} | {c.get('expected_none',0)} | {c.get('expected_weak',0)} | {c.get('expected_strong',0)} | "
            f"{c.get('strong_context_action_effect',0)} | {c.get('strong_context_gate_effect_only',0)} | {c.get('suspicious_strong_context_non_effect',0)} |"
        )
    findings_md = "\n".join(
        f"- **{f['id']}** ({f['severity']}): {f['finding']} Evidence: {f['evidence']}"
        for f in data["findings"]
    )
    buckets = "\n".join(f"- `{k}`: {v}" for k, v in sorted(data["context_bucket_counts"].items()))
    report = f"""# Context-Conditioned Expectation Audit — 2026-05-25

## Claim boundary

{CLAIM_BOUNDARY}

This audit was added because aggregate ablation counts are too naive. A mechanism can be active and correctly non-decisive. The audit first asks what the public context expects, then checks whether observed action/gate/readout effects match that expectation.

## Input

- Source trace: `{data['source']}`
- Full-current steps inspected: `{data['full_current_steps']}`
- Kernel behavior changed by this audit: `false`

## Context buckets observed

{buckets}

## Mechanism expectation/effect table

| mechanism | expected none | expected weak | expected strong | strong action effect | strong gate/readout effect only | suspicious strong non-effect |
|---|---:|---:|---:|---:|---:|---:|
""" + "\n".join(mech_lines) + f"""

## Findings

{findings_md}

## Interpretation

The prior global statement “sequence only changed actions in 1/8 modes” was too coarse. This audit conditions on public shape/gauge and local triggers such as carrier burden, resolver alternatives, sequence phase, quotient activity, and structural recursion pressure.

A `suspicious_strong_context_non_effect` does not prove CO failure. It means the trace satisfied generic CO conditions where the mechanism should plausibly affect commitment/gating, but the capped diagnostic showed neither an action difference under the corresponding ablation nor an explicit gate/readout effect. These cases should be manually inspected before changing formulas.

## Verdict

```json
{json.dumps(data['verdict'], indent=2, sort_keys=True)}
```

## Next step

Inspect the suspicious strong-context samples, especially for sequence and dynamic-shape contexts. The next action should be a readout-consumption/wiring audit, not a new ontology concept and not a family-specific tuning patch.
"""
    REPORT_MD.write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
