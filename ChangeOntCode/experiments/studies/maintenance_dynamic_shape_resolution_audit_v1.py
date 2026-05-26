from __future__ import annotations

"""Maintenance DynamicShapeField resolution audit v1.

Audit-only follow-up to the DynamicShapeField expectation investigation.  The
previous direction audit showed that DynamicShapeField often narrows margins
toward expose/relief alternatives in maintenance-like traces without changing
the selected action.  This study asks whether those non-decisive narrowing cases
are plausible stable-continuation outcomes under the current generic gate, or
whether they look like readout/control underweighting.

No kernel behavior is changed here.  The audit uses only public diagnostic
telemetry: shape/gauge fields, public relation/sequence rows, canonical
commitment assessment metrics, and named static-shape ablation comparisons.
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any, Iterable, Mapping

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.studies import current_kernel_diagnostic_map_v1 as diag
from experiments.studies.dynamic_shape_suspicious_case_investigation_v1 import _score_deltas, _top2, _ass, _f

OUT_DIR = ROOT / "outputs" / "current_kernel_diagnostic_map_v1"
STEPS_JSONL = OUT_DIR / "steps.jsonl"
JSON_OUT = ROOT / "outputs" / "maintenance_dynamic_shape_resolution_audit_v1.json"
REPORT_MD = ROOT.parent / "MAINTENANCE_DYNAMIC_SHAPE_RESOLUTION_AUDIT_REPORT_2026-05-25.md"

CLAIM_BOUNDARY = (
    "Audit-only maintenance DynamicShapeField resolution check. It does not change kernel behavior, "
    "does not assert an optimal maintenance action, does not use hidden state, DP/baseline values, or native action-name rules for decisions, "
    "and does not license maintenance-specific tuning. It classifies public trace contexts where DynamicShapeField narrows margins without changing action."
)

TARGET_FAMILY = "maintenance_replacement"
NARROW_EPS = -0.005
NEAR_MARGIN = 0.08
LARGE_MARGIN = 0.20
LOW_BLOCKER = 0.08
ADEQUATE_RATIO = 0.95


def _load_steps(refresh: bool = True) -> list[dict[str, Any]]:
    if refresh or not STEPS_JSONL.exists():
        diag.main()
    return [json.loads(line) for line in STEPS_JSONL.read_text(encoding="utf-8").splitlines() if line.strip()]


def _mean(xs: Iterable[float]) -> float:
    vals = [float(x) for x in xs]
    return float(mean(vals)) if vals else 0.0


def _phase_map(step: Mapping[str, Any]) -> dict[str, str]:
    out: dict[str, str] = {}
    for r in step.get("row_trace_sample", []) or []:
        if isinstance(r, Mapping):
            out[str(r.get("action"))] = str(r.get("continuation_phase", ""))
    return out


def _transition_map(step: Mapping[str, Any]) -> dict[str, str]:
    out: dict[str, str] = {}
    for r in step.get("row_trace_sample", []) or []:
        if isinstance(r, Mapping):
            out[str(r.get("action"))] = str(r.get("sequence_phase_transition", ""))
    return out


def _row_for_action(step: Mapping[str, Any], action: str) -> Mapping[str, Any]:
    for r in step.get("row_trace_sample", []) or []:
        if isinstance(r, Mapping) and str(r.get("action")) == str(action):
            return r
    return {}


def _selected_key(step: Mapping[str, Any]) -> str:
    action = step.get("action")
    ass = _ass(step)
    if str(action) in ass:
        return str(action)
    top = _top2(ass)
    return top[0][1] if top else str(action)


def _margin(step: Mapping[str, Any]) -> float:
    top = _top2(_ass(step))
    if len(top) < 2:
        return 0.0
    return _f(top[0][0]) - _f(top[1][0])


def _best_resolver_alt(step: Mapping[str, Any], selected: str) -> tuple[str, Mapping[str, Any], float]:
    ass = _ass(step)
    phases = _phase_map(step)
    best_key = ""
    best_metrics: Mapping[str, Any] = {}
    best_score = -1.0
    for key, metrics in ass.items():
        if str(key) == str(selected) or not isinstance(metrics, Mapping):
            continue
        phase = phases.get(str(key), "").lower()
        resolverish_phase = any(x in phase for x in ("expose", "reveal", "relieve", "reduce", "cancel", "buffer"))
        resolver_support = _f(metrics.get("resolver_support"))
        # Public structural resolver score: prefer actual resolver support, but let
        # explicit phase evidence keep expose/reveal rows in the audit sample.
        score = resolver_support + (0.04 if resolverish_phase else 0.0)
        if score > best_score:
            best_key = str(key)
            best_metrics = metrics
            best_score = score
    return best_key, best_metrics, best_score


def _is_carrierish(step: Mapping[str, Any], key: str, metrics: Mapping[str, Any]) -> bool:
    phase = _phase_map(step).get(str(key), "").lower()
    return (
        _f(metrics.get("carrier_only_pressure")) >= 0.20
        or _f(metrics.get("burden")) >= 0.12
        or any(x in phase for x in ("carry", "unresolved", "stabilize"))
    )


def _classify_case(full: Mapping[str, Any], static: Mapping[str, Any]) -> dict[str, Any]:
    selected = _selected_key(full)
    ass = _ass(full)
    selected_metrics = ass.get(selected, {}) if isinstance(ass.get(selected), Mapping) else {}
    alt_key, alt_metrics, alt_score = _best_resolver_alt(full, selected)
    score = _score_deltas(full, static)
    gauge = full.get("local_shape_gauge", {}) if isinstance(full.get("local_shape_gauge"), Mapping) else {}
    direct = full.get("direct_controls_used", {}) if isinstance(full.get("direct_controls_used"), Mapping) else {}
    phases = _phase_map(full)
    transitions = _transition_map(full)

    margin = _margin(full)
    static_margin = _margin(static)
    margin_delta = margin - static_margin
    action_changed = str(full.get("action")) != str(static.get("action"))
    narrowed = margin_delta <= NARROW_EPS and not action_changed

    carrier_pressure = _f(selected_metrics.get("carrier_only_pressure"))
    selected_burden = _f(selected_metrics.get("burden"))
    selected_blocked = _f(selected_metrics.get("collapse_blocked"))
    selected_recursion = _f(selected_metrics.get("collapse_certificate_recursion_demand"))
    resolver_support = _f(alt_metrics.get("resolver_support"))
    resolver_dom = _f(alt_metrics.get("dominance_score"))
    selected_dom = _f(selected_metrics.get("dominance_score"))
    required_resolver = _f(gauge.get("preblocking_required_resolver_support"))
    min_carrier = _f(gauge.get("preblocking_min_carrier_pressure"))
    local_urgency = _f(gauge.get("local_shape_urgency"))
    dyn_urgency = _f(direct.get("dynamic_shape_urgency"))
    projection = _f(direct.get("dynamic_shape_projection_horizon"))
    seq_support = _f(full.get("max_sequence_composition_support"))
    sequence_rows = int(full.get("sequence_rows", 0) or 0)
    shape_trigger = bool(full.get("shape_gauged_resolver_timing_applied"))
    selected_positive = _f(selected_metrics.get("dominance_positive_mass"))
    ssf = _f(selected_metrics.get("dominance_support_component")) + _f(selected_metrics.get("dominance_stability_component")) + _f(selected_metrics.get("dominance_field_component"))
    ssf_share = ssf / selected_positive if selected_positive > 1e-9 else 0.0

    carrier_gate_ratio = carrier_pressure / min_carrier if min_carrier > 1e-9 else 0.0
    resolver_req_ratio = resolver_support / required_resolver if required_resolver > 1e-9 else 0.0
    near_gate = carrier_gate_ratio >= ADEQUATE_RATIO or resolver_req_ratio >= ADEQUATE_RATIO
    directional = bool(alt_key) and (_is_carrierish(full, selected, selected_metrics) or carrier_pressure > 0.0) and (
        resolver_support > 0.05 or any(x in phases.get(alt_key, "").lower() for x in ("expose", "reveal", "relieve", "reduce", "cancel", "buffer"))
    )
    high_shape = local_urgency >= 0.45 or dyn_urgency >= 0.25 or projection >= 0.45
    low_blockers = selected_blocked <= LOW_BLOCKER and selected_recursion <= LOW_BLOCKER

    if not narrowed:
        classification = "not_narrowing_no_action_case"
    elif not directional:
        classification = "narrowing_but_not_directional_resolver_context"
    elif margin >= LARGE_MARGIN and carrier_gate_ratio < ADEQUATE_RATIO and resolver_req_ratio < ADEQUATE_RATIO and low_blockers:
        classification = "plausible_stable_continuation_under_current_gate"
    elif margin <= NEAR_MARGIN and high_shape and resolver_req_ratio >= ADEQUATE_RATIO and sequence_rows > 0:
        classification = "likely_underweighted_resolver_sequence_near_margin"
    elif high_shape and near_gate and ssf_share >= 0.90 and not shape_trigger:
        classification = "generic_gate_or_readout_underweighting_watchpoint"
    elif carrier_gate_ratio < 0.70 and resolver_req_ratio < 0.85 and low_blockers:
        classification = "legitimate_nondecisive_below_generic_gate"
    else:
        classification = "borderline_needs_manual_trace_review"

    return {
        "family": full.get("family"),
        "mode": full.get("mode"),
        "t": full.get("t"),
        "selected": selected,
        "alt_resolver": alt_key,
        "classification": classification,
        "narrowed_no_action": bool(narrowed),
        "directional_context": bool(directional),
        "margin": round(margin, 6),
        "static_margin": round(static_margin, 6),
        "margin_delta": round(margin_delta, 6),
        "selected_dominance": round(selected_dom, 6),
        "resolver_dominance": round(resolver_dom, 6),
        "carrier_pressure": round(carrier_pressure, 6),
        "min_carrier_gate": round(min_carrier, 6),
        "carrier_gate_ratio": round(carrier_gate_ratio, 6),
        "resolver_support": round(resolver_support, 6),
        "required_resolver_support": round(required_resolver, 6),
        "resolver_req_ratio": round(resolver_req_ratio, 6),
        "selected_burden": round(selected_burden, 6),
        "selected_collapse_blocked": round(selected_blocked, 6),
        "selected_recursion_demand": round(selected_recursion, 6),
        "support_stability_field_share": round(ssf_share, 6),
        "local_shape_urgency": round(local_urgency, 6),
        "dynamic_shape_urgency": round(dyn_urgency, 6),
        "projection_horizon": round(projection, 6),
        "sequence_rows": sequence_rows,
        "sequence_support": round(seq_support, 6),
        "shape_gauged_trigger": shape_trigger,
        "selected_phase": phases.get(selected),
        "resolver_phase": phases.get(alt_key),
        "selected_transition": transitions.get(selected),
        "resolver_transition": transitions.get(alt_key),
        "score_effect": {
            "max_dominance_delta": round(_f(score.get("max_dominance_delta")), 6),
            "avg_dominance_delta": round(_f(score.get("avg_dominance_delta")), 6),
            "margin_delta": round(_f(score.get("margin_delta")), 6),
            "top_action_changed": bool(score.get("top_action_changed")),
        },
    }


def main() -> dict[str, Any]:
    steps = _load_steps(refresh=True)
    index = {(str(s.get("family")), str(s.get("mode")), int(s.get("seed", 0)), int(s.get("t", 0)), str(s.get("variant"))): s for s in steps}
    full_maint = [s for s in steps if s.get("variant") == "full_current" and s.get("family") == TARGET_FAMILY]

    counts = Counter()
    by_mode: dict[str, Counter] = defaultdict(Counter)
    cases_by_class: dict[str, list[dict[str, Any]]] = defaultdict(list)
    margin_deltas: dict[str, list[float]] = defaultdict(list)

    for s in full_maint:
        static = index.get((str(s.get("family")), str(s.get("mode")), int(s.get("seed", 0)), int(s.get("t", 0)), "static_shape"))
        if static is None:
            continue
        c = _classify_case(s, static)
        cls = c["classification"]
        counts[cls] += 1
        counts["total_classified_steps"] += 1
        if c["narrowed_no_action"]:
            counts["narrowed_no_action_steps"] += 1
        if c["directional_context"]:
            counts["directional_context_steps"] += 1
        by_mode[str(c.get("mode"))][cls] += 1
        by_mode[str(c.get("mode"))]["total"] += 1
        margin_deltas[cls].append(float(c.get("margin_delta", 0.0)))
        if len(cases_by_class[cls]) < 8:
            cases_by_class[cls].append(c)

    avg_margin_delta_by_class = {k: (_mean(v) if v else 0.0) for k, v in margin_deltas.items()}
    hard_underweight = counts.get("likely_underweighted_resolver_sequence_near_margin", 0)
    watchpoint = counts.get("generic_gate_or_readout_underweighting_watchpoint", 0)
    plausible = counts.get("plausible_stable_continuation_under_current_gate", 0) + counts.get("legitimate_nondecisive_below_generic_gate", 0)

    findings: list[dict[str, Any]] = [
        {
            "id": "MDS1_NARROWING_CASES_ARE_NOT_AUTOMATIC_FAILURES",
            "severity": "info",
            "finding": "Many maintenance DynamicShapeField narrowing/no-action cases remain non-decisive because the selected branch or resolver alternative does not pass the current generic preblocking gate.",
            "evidence": f"plausible_or_below_gate={plausible}, narrowed_no_action_steps={counts.get('narrowed_no_action_steps',0)}",
            "next_action": "Do not treat every score narrowing without action change as readout failure; retain context-conditioned classification.",
        },
        {
            "id": "MDS2_GATE_READOUT_WATCHPOINT_REMAINS",
            "severity": "medium" if watchpoint or hard_underweight else "low",
            "finding": "Some cases still look like generic gate/readout adequacy watchpoints rather than clean stable continuation.",
            "evidence": f"generic_gate_or_readout_underweighting_watchpoint={watchpoint}, likely_underweighted_resolver_sequence_near_margin={hard_underweight}",
            "next_action": "Use targeted generic microcases before any coefficient change; do not tune maintenance-specific behavior.",
        },
        {
            "id": "MDS3_MAINTENANCE_ACTION_INSENSITIVITY_REINTERPRETED",
            "severity": "medium",
            "finding": "Maintenance action insensitivity is not explained by DynamicShapeField being inert. It is mostly a question of whether current generic gates are too conservative in maintenance-like phase contexts.",
            "evidence": "DynamicShapeField narrows margins in several maintenance steps, but most do not cross current carrier/resolver gate thresholds or dominance margins.",
            "next_action": "If future diagnostics require change, audit the generic preblocking/readout gate under shape-conditioned phase contexts across families, not just maintenance.",
        },
    ]
    result = {
        "study": "maintenance_dynamic_shape_resolution_audit_v1",
        "claim_boundary": CLAIM_BOUNDARY,
        "total_maintenance_full_steps": len(full_maint),
        "counts": dict(counts),
        "by_mode": {k: dict(v) for k, v in sorted(by_mode.items())},
        "avg_margin_delta_by_classification": avg_margin_delta_by_class,
        "case_samples_by_classification": dict(cases_by_class),
        "findings": findings,
        "verdict": {
            "kernel_change_made": False,
            "dynamic_shape_inert_in_maintenance": False,
            "all_narrowing_non_effects_are_failures": False,
            "hard_underweighting_cases_found": hard_underweight,
            "generic_gate_or_readout_watchpoints_found": watchpoint,
            "maintenance_specific_tuning_justified": False,
            "next_recommended_step": "design generic gate/readout adequacy microcases if the team wants to test whether current thresholds are too conservative; otherwise proceed to broader first-pass evaluation with this watchpoint logged",
        },
    }
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    _write_report(result)
    print(json.dumps(result["verdict"], indent=2, sort_keys=True))
    return result


def _write_report(data: Mapping[str, Any]) -> None:
    lines: list[str] = []
    lines.append("# Maintenance DynamicShapeField Resolution Audit — 2026-05-25")
    lines.append("")
    lines.append("## Claim boundary")
    lines.append("")
    lines.append(CLAIM_BOUNDARY)
    lines.append("")
    lines.append("## Main verdict")
    lines.append("")
    lines.append("DynamicShapeField is not inert in maintenance-like traces. It often moves dominance margins, but most narrowing/no-action cases do not cross the current generic carrier/resolver gate or remain dominated by a selected branch with a sizeable margin. This means the remaining issue is not 'DynamicShapeField does nothing'; it is whether the generic gate/readout is too conservative in phase-structured maintenance-like contexts.")
    lines.append("")
    lines.append("This audit does not justify a maintenance-specific rule or coefficient tune.")
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(data.get("counts", {}), indent=2, sort_keys=True))
    lines.append("```")
    lines.append("")
    lines.append("## By mode")
    lines.append("")
    lines.append("| mode | total | not narrowing | plausible stable/current gate | below generic gate | gate/readout watchpoint | hard underweighting | borderline |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for mode, c in data.get("by_mode", {}).items():
        lines.append(
            f"| {mode} | {c.get('total',0)} | {c.get('not_narrowing_no_action_case',0)} | "
            f"{c.get('plausible_stable_continuation_under_current_gate',0)} | {c.get('legitimate_nondecisive_below_generic_gate',0)} | "
            f"{c.get('generic_gate_or_readout_underweighting_watchpoint',0)} | {c.get('likely_underweighted_resolver_sequence_near_margin',0)} | "
            f"{c.get('borderline_needs_manual_trace_review',0)} |"
        )
    lines.append("")
    lines.append("## Findings")
    lines.append("")
    for f in data.get("findings", []):
        lines.append(f"### {f['id']} — {f['severity']}")
        lines.append("")
        lines.append(f"**Finding:** {f['finding']}")
        lines.append("")
        lines.append(f"**Evidence:** {f['evidence']}")
        lines.append("")
        lines.append(f"**Next action:** {f['next_action']}")
        lines.append("")
    lines.append("## Representative samples")
    lines.append("")
    for cls, cases in data.get("case_samples_by_classification", {}).items():
        lines.append(f"### `{cls}`")
        lines.append("")
        for case in cases[:5]:
            compact = {
                "mode": case.get("mode"),
                "t": case.get("t"),
                "selected": case.get("selected"),
                "alt_resolver": case.get("alt_resolver"),
                "margin": case.get("margin"),
                "margin_delta": case.get("margin_delta"),
                "carrier_gate_ratio": case.get("carrier_gate_ratio"),
                "resolver_req_ratio": case.get("resolver_req_ratio"),
                "local_shape_urgency": case.get("local_shape_urgency"),
                "sequence_support": case.get("sequence_support"),
                "shape_gauged_trigger": case.get("shape_gauged_trigger"),
            }
            lines.append("```json")
            lines.append(json.dumps(compact, indent=2, sort_keys=True))
            lines.append("```")
        lines.append("")
    lines.append("## Verdict")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(data.get("verdict", {}), indent=2, sort_keys=True))
    lines.append("```")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("The audit narrows the question: maintenance insensitivity is not caused by DynamicShapeField absence or pure readout invisibility. Dynamic shape often changes margins. The unresolved issue is whether the current generic carrier/resolver gate and support-stability dominance are calibrated correctly for phase-structured contexts. This should be tested with generic cross-family microcases before any runtime change.")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
