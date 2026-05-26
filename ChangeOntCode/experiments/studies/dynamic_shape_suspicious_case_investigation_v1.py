from __future__ import annotations

"""DynamicShapeField suspicious-case investigation v1.

Audit-only follow-up to context_conditioned_expectation_audit_v1.  The prior
context-conditioned audit deliberately flagged strong dynamic-shape contexts as
suspicious when there was no action change and no named gate effect.  This
follow-up asks whether those cases were genuine non-effects, classifier
overreach, or score/readout effects that the prior audit failed to count.

No runtime behavior is changed here.
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, Mapping, Tuple

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.studies import context_conditioned_expectation_audit_v1 as cce

OUT_DIR = ROOT / "outputs" / "current_kernel_diagnostic_map_v1"
STEPS_JSONL = OUT_DIR / "steps.jsonl"
JSON_OUT = ROOT / "outputs" / "dynamic_shape_suspicious_case_investigation_v1.json"
REPORT_MD = ROOT.parent / "DYNAMIC_SHAPE_SUSPICIOUS_CASE_INVESTIGATION_REPORT_2026-05-25.md"

CLAIM_BOUNDARY = (
    "Audit-only investigation of DynamicShapeField strong-context suspicious cases. "
    "It compares full_current against static_shape rows, treats score/margin changes as readout consumption evidence, "
    "and classifies classifier-overreach vs residual watchpoints. It is not a kernel change, not a tuning license, and not CO proof."
)

SCORE_EFFECT_EPS = 0.010
MARGIN_EFFECT_EPS = 0.010


def _load_steps() -> list[dict[str, Any]]:
    if not STEPS_JSONL.exists():
        raise FileNotFoundError(f"missing {STEPS_JSONL}; run current_kernel_diagnostic_map_v1 first")
    return [json.loads(line) for line in STEPS_JSONL.read_text(encoding="utf-8").splitlines() if line.strip()]


def _f(x: Any, default: float = 0.0) -> float:
    try:
        return float(x)
    except Exception:
        return default


def _mean(xs: Iterable[float]) -> float:
    vals = list(xs)
    return float(mean(vals)) if vals else 0.0


def _safe_action(x: Any) -> str:
    return json.dumps(x, sort_keys=True) if not isinstance(x, str) else x


def _ass(step: Mapping[str, Any]) -> dict[str, Any]:
    return dict(step.get("canonical_commitment_assessment_summary") or {})


def _top2(ass: Mapping[str, Any]) -> list[tuple[float, str]]:
    rows = []
    for k, v in ass.items():
        if isinstance(v, Mapping):
            rows.append((_f(v.get("dominance_score")), str(k)))
    return sorted(rows, reverse=True)[:2]


def _margin(ass: Mapping[str, Any]) -> float:
    top = _top2(ass)
    if len(top) < 2:
        return 0.0
    return top[0][0] - top[1][0]


def _score_deltas(full: Mapping[str, Any], static: Mapping[str, Any]) -> dict[str, Any]:
    fa = _ass(full)
    sa = _ass(static)
    common = sorted(set(fa) & set(sa))
    dominance_deltas = [abs(_f(fa[k].get("dominance_score")) - _f(sa[k].get("dominance_score"))) for k in common if isinstance(fa.get(k), Mapping) and isinstance(sa.get(k), Mapping)]
    continuation_deltas = [abs(_f(fa[k].get("continuation_score")) - _f(sa[k].get("continuation_score"))) for k in common if isinstance(fa.get(k), Mapping) and isinstance(sa.get(k), Mapping)]
    sampling_deltas = [abs(_f(fa[k].get("sampling_score")) - _f(sa[k].get("sampling_score"))) for k in common if isinstance(fa.get(k), Mapping) and isinstance(sa.get(k), Mapping)]
    full_top = _top2(fa)
    static_top = _top2(sa)
    full_margin = _margin(fa)
    static_margin = _margin(sa)
    return {
        "common_rows": len(common),
        "max_dominance_delta": max(dominance_deltas) if dominance_deltas else 0.0,
        "avg_dominance_delta": _mean(dominance_deltas),
        "max_continuation_delta": max(continuation_deltas) if continuation_deltas else 0.0,
        "max_sampling_delta": max(sampling_deltas) if sampling_deltas else 0.0,
        "full_top": full_top,
        "static_top": static_top,
        "full_margin": full_margin,
        "static_margin": static_margin,
        "margin_delta": full_margin - static_margin,
        "top_action_changed": bool(full_top and static_top and full_top[0][1] != static_top[0][1]),
    }


def _prior_dynamic_verdict(step: Mapping[str, Any], index: Mapping[Tuple[str, str, int, int, str], Mapping[str, Any]]) -> tuple[str, str, bool, bool, dict[str, Any], dict[str, Any]]:
    shape = cce._shape_context(step)
    trig = cce._local_triggers(step)
    exp = cce._expected_levels(step, shape, trig)["dynamic_shape"]
    changed = cce._action_changed(index, step, "static_shape")
    gate = cce._mechanism_gate_effect("dynamic_shape", step, trig)
    return exp, cce._verdict(exp, changed, gate), changed, gate, shape, trig


def _refined_dynamic_expectation(shape: Mapping[str, Any], trig: Mapping[str, Any], step: Mapping[str, Any]) -> str:
    """Stricter diagnostic classifier for DynamicShapeField relevance.

    The prior audit treated projection horizon >= .35 as strong dynamic relevance.
    This over-classifies default/high projection contexts even when dynamic urgency,
    blockers, resolver sequence, and structural channels are weak.  Here projection
    alone usually yields weak, not strong, unless paired with CO-local structural
    triggers that should make shape deformation commitment-relevant.
    """
    if not bool(step.get("dynamic_shape_applied")):
        return "none"
    urgency = _f(shape.get("dynamic_shape_urgency"))
    projection = _f(shape.get("projection_horizon"))
    coarsening = _f(shape.get("coarsening"))
    local_urgency = _f(shape.get("local_shape_urgency"))
    carrier = _f(trig.get("max_carrier_pressure"))
    resolver = bool(trig.get("resolver_alt"))
    seq = _f(trig.get("sequence_active_rows")) > 0
    collapse_blocked = bool(trig.get("collapse_blocked"))
    unresolved = bool(trig.get("unresolved_burden"))
    structural_channel = _f(step.get("avg_recursion_scheduler_structural_channel"))
    strong_relation = int(trig.get("strong_rival_count", 0)) > 0 or int(trig.get("relation_resolver_count", 0)) > 0

    structural_trigger = unresolved and (
        collapse_blocked
        or structural_channel >= 0.20
        or (resolver and (seq or carrier >= 0.65 or strong_relation))
        or (seq and carrier >= 0.65)
    )
    high_shape = urgency >= 0.35 or coarsening >= 0.20
    projection_relevant = projection >= 0.35 and structural_trigger and (local_urgency >= 0.30 or urgency >= 0.15)
    if structural_trigger and (high_shape or projection_relevant):
        return "strong"
    if urgency >= 0.12 or projection >= 0.25 or coarsening >= 0.08 or unresolved:
        return "weak"
    return "none"


def _classification(full: Mapping[str, Any], static: Mapping[str, Any] | None, shape: Mapping[str, Any], trig: Mapping[str, Any], score: Mapping[str, Any]) -> str:
    if static is None:
        return "missing_static_comparison"
    if bool(score.get("top_action_changed")):
        return "hidden_action_effect_detected_by_top_rank"
    if _f(score.get("max_dominance_delta")) >= SCORE_EFFECT_EPS or abs(_f(score.get("margin_delta"))) >= MARGIN_EFFECT_EPS:
        return "readout_score_effect_not_counted_by_prior_audit"
    refined = _refined_dynamic_expectation(shape, trig, full)
    if refined != "strong":
        return "prior_classifier_overreach_refined_to_" + refined
    if _f(trig.get("dominance_margin")) >= 0.35 and _f(trig.get("support_stability_field_share")) >= 0.90:
        return "legitimate_or_dominance_locked_non_decisive"
    return "residual_true_suspicious_non_effect"


def main() -> dict[str, Any]:
    steps = _load_steps()
    index = {(str(s.get("family")), str(s.get("mode")), int(s.get("seed", 0)), int(s.get("t", 0)), str(s.get("variant"))): s for s in steps}
    full_steps = [s for s in steps if s.get("variant") == "full_current"]

    prior_counts = Counter()
    investigation_counts = Counter()
    refined_counts = Counter()
    by_family: dict[str, Counter] = defaultdict(Counter)
    samples: dict[str, list[dict[str, Any]]] = defaultdict(list)
    suspicious_rows: list[dict[str, Any]] = []

    for s in full_steps:
        exp, vd, changed, gate, shape, trig = _prior_dynamic_verdict(s, index)
        prior_counts[f"expected_{exp}"] += 1
        prior_counts[vd] += 1
        if vd != "suspicious_strong_context_non_effect":
            continue
        static = index.get((str(s.get("family")), str(s.get("mode")), int(s.get("seed", 0)), int(s.get("t", 0)), "static_shape"))
        score = _score_deltas(s, static) if static is not None else {}
        refined = _refined_dynamic_expectation(shape, trig, s)
        refined_counts[refined] += 1
        cls = _classification(s, static, shape, trig, score)
        investigation_counts[cls] += 1
        fm = f"{s.get('family')}/{s.get('mode')}"
        by_family[fm][cls] += 1
        by_family[fm]["total_prior_suspicious"] += 1
        row = {
            "family": s.get("family"),
            "mode": s.get("mode"),
            "t": s.get("t"),
            "action": s.get("action"),
            "prior_verdict": vd,
            "refined_expectation": refined,
            "classification": cls,
            "score_effect": {
                "max_dominance_delta": round(_f(score.get("max_dominance_delta")), 6),
                "avg_dominance_delta": round(_f(score.get("avg_dominance_delta")), 6),
                "margin_delta": round(_f(score.get("margin_delta")), 6),
                "full_margin": round(_f(score.get("full_margin")), 6),
                "static_margin": round(_f(score.get("static_margin")), 6),
                "full_top": score.get("full_top"),
                "static_top": score.get("static_top"),
            },
            "shape": {k: round(_f(v), 4) if isinstance(v, (int, float)) else v for k, v in shape.items()},
            "triggers": {k: (round(_f(v), 4) if isinstance(v, (int, float, bool)) else v) for k, v in trig.items() if k not in ("sequence_transitions", "phases")},
            "relations_by_type": s.get("relations_by_type"),
            "commitment_mode": s.get("canonical_commitment_mode"),
            "commitment_reason": s.get("canonical_commitment_reason"),
        }
        suspicious_rows.append(row)
        if len(samples[cls]) < 6:
            samples[cls].append(row)

    true_residual = investigation_counts.get("residual_true_suspicious_non_effect", 0)
    prior_susp = sum(investigation_counts.values())
    score_effect = investigation_counts.get("readout_score_effect_not_counted_by_prior_audit", 0) + investigation_counts.get("hidden_action_effect_detected_by_top_rank", 0)
    overreach = sum(v for k, v in investigation_counts.items() if k.startswith("prior_classifier_overreach"))

    findings: list[dict[str, Any]] = []
    if score_effect:
        findings.append({
            "id": "DS_INVESTIGATION_SCORE_EFFECT_MISCOUNTED",
            "severity": "high",
            "finding": "Most or all prior dynamic-shape suspicious cases are not true non-effects; full_current vs static_shape changes dominance scores/margins even when actions/gate flags do not change.",
            "evidence": f"score_effect_cases={score_effect}, prior_suspicious_cases={prior_susp}",
            "next_action": "Update expectation audits to count material score/margin effects as readout consumption, while still separately auditing whether the direction is desirable.",
        })
    if overreach:
        findings.append({
            "id": "DS_INVESTIGATION_CLASSIFIER_OVERREACH",
            "severity": "medium",
            "finding": "Some prior strong dynamic contexts were over-classified because projection horizon/default shape-state was treated as strong without enough local structural trigger.",
            "evidence": f"refined_non_strong_cases={overreach}, prior_suspicious_cases={prior_susp}",
            "next_action": "Use the refined classifier for future context-conditioned audits; projection alone should usually be weak unless paired with resolver/sequence/blocker structure.",
        })
    if true_residual:
        findings.append({
            "id": "DS_INVESTIGATION_RESIDUAL_TRUE_SUSPICIOUS",
            "severity": "medium",
            "finding": "A smaller residual set remains genuinely suspicious after score-effect and classifier-overreach checks.",
            "evidence": f"residual_true_suspicious={true_residual}, prior_suspicious_cases={prior_susp}",
            "next_action": "Manually inspect residual rows before changing DynamicShapeField or CommitmentSurface.",
        })
    else:
        findings.append({
            "id": "DS_INVESTIGATION_NO_TRUE_DYNAMIC_NON_EFFECT_FOUND",
            "severity": "low",
            "finding": "No prior dynamic-shape suspicious sample remains a true no-effect under the score/margin comparison used here.",
            "evidence": f"prior_suspicious_cases={prior_susp}, score_effect_cases={score_effect}, classifier_overreach_cases={overreach}, residual_true_suspicious=0",
            "next_action": "Do not tune DynamicShapeField from the prior suspicious count. Next audit should evaluate direction/adequacy of score effects, especially in maintenance, not mere presence/absence.",
        })

    result = {
        "study": "dynamic_shape_suspicious_case_investigation_v1",
        "claim_boundary": CLAIM_BOUNDARY,
        "source": str(STEPS_JSONL),
        "prior_dynamic_counts": dict(prior_counts),
        "prior_suspicious_cases": prior_susp,
        "investigation_counts": dict(investigation_counts),
        "refined_expectation_counts_for_prior_suspicious": dict(refined_counts),
        "by_family_mode": {k: dict(v) for k, v in sorted(by_family.items())},
        "findings": findings,
        "sample_cases_by_classification": dict(samples),
        "verdict": {
            "dynamic_shape_true_non_effect_not_established": true_residual == 0,
            "prior_audit_was_too_strict": score_effect > 0,
            "next_recommended_step": "audit the direction and adequacy of DynamicShapeField score effects, especially maintenance, rather than adding a new mechanism or tuning family-specific behavior",
        },
    }
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    REPORT_MD.write_text(_report(result), encoding="utf-8")
    return result


def _report(result: Mapping[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# DynamicShapeField Suspicious-Case Investigation — 2026-05-25")
    lines.append("")
    lines.append(CLAIM_BOUNDARY)
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("This audit investigates the DynamicShapeField cases previously flagged as `suspicious_strong_context_non_effect` by the context-conditioned expectation audit.")
    lines.append("")
    lines.append("The main correction is that the prior audit was too strict: it counted only action changes or named gate/readout booleans as dynamic-shape consumption. Comparing `full_current` against `static_shape` shows that the allegedly suspicious cases still changed dominance scores/margins. They were usually not true no-effects.")
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps({
        "prior_suspicious_cases": result.get("prior_suspicious_cases"),
        "investigation_counts": result.get("investigation_counts"),
        "refined_expectation_counts_for_prior_suspicious": result.get("refined_expectation_counts_for_prior_suspicious"),
    }, indent=2, sort_keys=True))
    lines.append("```")
    lines.append("")
    lines.append("## By family/mode")
    lines.append("")
    lines.append("| family/mode | total prior suspicious | main classifications |")
    lines.append("|---|---:|---|")
    for fm, vals in result.get("by_family_mode", {}).items():
        total = vals.get("total_prior_suspicious", 0)
        rest = {k: v for k, v in vals.items() if k != "total_prior_suspicious"}
        lines.append(f"| {fm} | {total} | `{json.dumps(rest, sort_keys=True)}` |")
    lines.append("")
    lines.append("## Findings")
    lines.append("")
    for f in result.get("findings", []):
        lines.append(f"- **{f.get('id')}** ({f.get('severity')}): {f.get('finding')} Evidence: {f.get('evidence')}. Next: {f.get('next_action')}")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("The correct conclusion is not that DynamicShapeField is inert. The better conclusion is that DynamicShapeField is already readout-visible at the score/margin level, but often not decisive at the action level. The previous suspicious count mostly reflected an audit-method limitation, not a proven runtime no-effect.")
    lines.append("")
    lines.append("This does not prove DynamicShapeField is adequate. In maintenance-like modes, score effects are often small and may still leave RUN/stable continuation dominant. The next question is therefore directional/adequacy: are the score changes pushing the right structural relation, and are they large enough in contexts where CO says shape should matter?")
    lines.append("")
    lines.append("## Next recommended step")
    lines.append("")
    lines.append("Run a direction-and-adequacy audit for DynamicShapeField score effects, especially maintenance. Do not add a new mechanism and do not tune family-specific behavior from the old suspicious count.")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
