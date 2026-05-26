from __future__ import annotations

"""DynamicShapeField direction/adequacy audit v1.

Audit-only follow-up.  DynamicShapeField can be readout-visible through score
changes without changing actions.  This audit asks whether those score changes
move margins in structurally plausible directions in contexts where a locally
stable/carrier branch is opposed by a public expose/relief alternative.
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any, Mapping, Tuple

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.studies import context_conditioned_expectation_audit_v1 as cce
from experiments.studies.dynamic_shape_suspicious_case_investigation_v1 import _score_deltas, _top2, _ass, _f

OUT_DIR = ROOT / "outputs" / "current_kernel_diagnostic_map_v1"
STEPS_JSONL = OUT_DIR / "steps.jsonl"
JSON_OUT = ROOT / "outputs" / "dynamic_shape_direction_adequacy_audit_v1.json"
REPORT_MD = ROOT.parent / "DYNAMIC_SHAPE_DIRECTION_ADEQUACY_AUDIT_REPORT_2026-05-25.md"

CLAIM_BOUNDARY = (
    "Audit-only DynamicShapeField direction/adequacy check. It does not change the kernel, "
    "does not use native family/action rules, and does not assert an optimal action. It only checks whether score/margin effects are structurally directional in public carrier/resolver contexts."
)

MARGIN_EPS = 0.005


def _load_steps() -> list[dict[str, Any]]:
    return [json.loads(line) for line in STEPS_JSONL.read_text(encoding="utf-8").splitlines() if line.strip()]


def _phase_map(step: Mapping[str, Any]) -> dict[str, str]:
    out = {}
    for r in step.get("row_trace_sample", []) or []:
        if isinstance(r, Mapping) and "action" in r:
            out[str(r.get("action"))] = str(r.get("continuation_phase", ""))
    return out


def _row_for_action(step: Mapping[str, Any], action_key: str) -> Mapping[str, Any]:
    for r in step.get("row_trace_sample", []) or []:
        if isinstance(r, Mapping) and str(r.get("action")) == str(action_key):
            return r
    return {}


def _is_carrierish_phase(phase: str) -> bool:
    p = str(phase).lower()
    return any(x in p for x in ("carry", "stabilize", "unresolved"))


def _is_resolverish_phase(phase: str) -> bool:
    p = str(phase).lower()
    return any(x in p for x in ("expose", "reveal", "relieve", "reduce", "cancel", "buffer"))


def _classify_direction(full: Mapping[str, Any], static: Mapping[str, Any], trig: Mapping[str, Any], shape: Mapping[str, Any]) -> dict[str, Any]:
    score = _score_deltas(full, static)
    fa = _ass(full)
    top = _top2(fa)
    phase = _phase_map(full)
    selected_key = top[0][1] if top else ""
    runner_key = top[1][1] if len(top) > 1 else ""
    selected_phase = phase.get(selected_key, "")
    runner_phase = phase.get(runner_key, "")
    selected_row = _row_for_action(full, selected_key)
    runner_row = _row_for_action(full, runner_key)

    directional_context = bool(trig.get("resolver_alt")) and bool(trig.get("unresolved_burden")) and _is_carrierish_phase(selected_phase) and _is_resolverish_phase(runner_phase)
    margin_delta = _f(score.get("margin_delta"))
    if not directional_context:
        verdict = "not_directional_carrier_resolver_context"
    elif margin_delta < -MARGIN_EPS:
        verdict = "margin_narrows_toward_resolver_or_exposure"
    elif margin_delta > MARGIN_EPS:
        verdict = "margin_widens_toward_selected_carrier"
    else:
        verdict = "margin_neutral"
    return {
        "verdict": verdict,
        "score": score,
        "selected_key": selected_key,
        "runner_key": runner_key,
        "selected_phase": selected_phase,
        "runner_phase": runner_phase,
        "selected_sequence_transition": selected_row.get("sequence_phase_transition"),
        "runner_sequence_transition": runner_row.get("sequence_phase_transition"),
        "selected_support": selected_row.get("support_mass"),
        "runner_support": runner_row.get("support_mass"),
        "selected_burden": selected_row.get("burden_pressure"),
        "runner_burden": runner_row.get("burden_pressure"),
        "directional_context": directional_context,
    }


def main() -> dict[str, Any]:
    steps = _load_steps()
    index = {(str(s.get("family")), str(s.get("mode")), int(s.get("seed", 0)), int(s.get("t", 0)), str(s.get("variant"))): s for s in steps}
    full_steps = [s for s in steps if s.get("variant") == "full_current"]
    counts = Counter()
    by_family: dict[str, Counter] = defaultdict(Counter)
    samples: dict[str, list[dict[str, Any]]] = defaultdict(list)
    margin_by_class: dict[str, list[float]] = defaultdict(list)

    for s in full_steps:
        static = index.get((str(s.get("family")), str(s.get("mode")), int(s.get("seed", 0)), int(s.get("t", 0)), "static_shape"))
        if static is None:
            continue
        shape = cce._shape_context(s)
        trig = cce._local_triggers(s)
        expected = cce._expected_levels(s, shape, trig)["dynamic_shape"]
        if expected not in ("strong", "weak"):
            continue
        info = _classify_direction(s, static, trig, shape)
        verdict = info["verdict"]
        counts[verdict] += 1
        if expected == "strong":
            counts[f"strong_{verdict}"] += 1
        fm = f"{s.get('family')}/{s.get('mode')}"
        by_family[fm][verdict] += 1
        by_family[fm]["total"] += 1
        margin_by_class[verdict].append(_f(info["score"].get("margin_delta")))
        if len(samples[verdict]) < 8:
            samples[verdict].append({
                "family": s.get("family"),
                "mode": s.get("mode"),
                "t": s.get("t"),
                "action": s.get("action"),
                "expected": expected,
                "verdict": verdict,
                "selected_key": info.get("selected_key"),
                "runner_key": info.get("runner_key"),
                "selected_phase": info.get("selected_phase"),
                "runner_phase": info.get("runner_phase"),
                "selected_sequence_transition": info.get("selected_sequence_transition"),
                "runner_sequence_transition": info.get("runner_sequence_transition"),
                "margin_delta": round(_f(info["score"].get("margin_delta")), 6),
                "max_dominance_delta": round(_f(info["score"].get("max_dominance_delta")), 6),
                "full_top": info["score"].get("full_top"),
                "static_top": info["score"].get("static_top"),
                "shape": {
                    "dynamic_shape_urgency": round(_f(shape.get("dynamic_shape_urgency")), 4),
                    "projection_horizon": round(_f(shape.get("projection_horizon")), 4),
                    "coarsening": round(_f(shape.get("coarsening")), 4),
                    "local_shape_urgency": round(_f(shape.get("local_shape_urgency")), 4),
                },
                "triggers": {
                    "resolver_alt": bool(trig.get("resolver_alt")),
                    "unresolved_burden": bool(trig.get("unresolved_burden")),
                    "sequence_active_rows": trig.get("sequence_active_rows"),
                    "dominance_margin": round(_f(trig.get("dominance_margin")), 4),
                },
            })

    avg_margins = {k: (float(mean(v)) if v else 0.0) for k, v in margin_by_class.items()}
    findings: list[dict[str, Any]] = []
    directional_total = counts.get("margin_narrows_toward_resolver_or_exposure", 0) + counts.get("margin_widens_toward_selected_carrier", 0) + counts.get("margin_neutral", 0)
    if directional_total:
        findings.append({
            "id": "DS_DIRECTIONAL_CONTEXTS_EXIST",
            "severity": "info",
            "finding": "Dynamic-shape directional contexts exist where a selected carrier/stabilizer is opposed by a public resolver/exposure runner-up.",
            "evidence": f"directional_contexts={directional_total}, narrows={counts.get('margin_narrows_toward_resolver_or_exposure',0)}, widens={counts.get('margin_widens_toward_selected_carrier',0)}, neutral={counts.get('margin_neutral',0)}",
            "next_action": "Use these directional contexts for future adequacy checks; do not rely on aggregate action changes alone.",
        })
        if counts.get("margin_widens_toward_selected_carrier", 0) > counts.get("margin_narrows_toward_resolver_or_exposure", 0):
            findings.append({
                "id": "DS_DIRECTION_WATCHPOINT_SELECTED_CARRIER_WIDENING",
                "severity": "medium",
                "finding": "In directional carrier/resolver contexts, DynamicShapeField more often widens the selected carrier/stabilizer margin than narrows it toward the resolver/exposure alternative.",
                "evidence": f"widens={counts.get('margin_widens_toward_selected_carrier',0)}, narrows={counts.get('margin_narrows_toward_resolver_or_exposure',0)}",
                "next_action": "Investigate whether dynamic controls over-amplify local authority/support stability in these contexts or whether selected carrier stabilization is actually justified by shape.",
            })
    else:
        findings.append({
            "id": "DS_NO_DIRECTIONAL_CONTEXTS_FOUND",
            "severity": "low",
            "finding": "No strict selected-carrier vs resolver-runner-up directional contexts were found under this classifier.",
            "evidence": "directional_contexts=0",
            "next_action": "Broaden the directional classifier before drawing adequacy conclusions.",
        })

    result = {
        "study": "dynamic_shape_direction_adequacy_audit_v1",
        "claim_boundary": CLAIM_BOUNDARY,
        "counts": dict(counts),
        "avg_margin_delta_by_classification": avg_margins,
        "by_family_mode": {k: dict(v) for k, v in sorted(by_family.items())},
        "findings": findings,
        "sample_cases_by_classification": dict(samples),
        "verdict": {
            "dynamic_shape_direction_not_fully_resolved": True,
            "next_recommended_step": "inspect whether widening toward selected carrier/stabilizer is legitimate shape-conditioned stabilization or a readout/control adequacy problem",
        },
    }
    JSON_OUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    REPORT_MD.write_text(_report(result), encoding="utf-8")
    return result


def _report(result: Mapping[str, Any]) -> str:
    lines = [
        "# DynamicShapeField Direction/Adequacy Audit — 2026-05-25",
        "",
        CLAIM_BOUNDARY,
        "",
        "## Summary",
        "",
        "The previous investigation showed that DynamicShapeField was not inert: many allegedly suspicious cases had score/margin effects. This audit asks the next question: in public carrier/resolver contexts, do those score effects move in a structurally plausible direction?",
        "",
        "## Counts",
        "",
        "```json",
        json.dumps({
            "counts": result.get("counts"),
            "avg_margin_delta_by_classification": result.get("avg_margin_delta_by_classification"),
        }, indent=2, sort_keys=True),
        "```",
        "",
        "## By family/mode",
        "",
        "| family/mode | counts |",
        "|---|---|",
    ]
    for fm, vals in result.get("by_family_mode", {}).items():
        lines.append(f"| {fm} | `{json.dumps(vals, sort_keys=True)}` |")
    lines += ["", "## Findings", ""]
    for f in result.get("findings", []):
        lines.append(f"- **{f.get('id')}** ({f.get('severity')}): {f.get('finding')} Evidence: {f.get('evidence')}. Next: {f.get('next_action')}")
    lines += [
        "",
        "## Interpretation",
        "",
        "DynamicShapeField is readout-visible, but adequacy is not settled. The important remaining question is directional: when shape should make an exposure/relief alternative matter against a selected carrier/stabilizer, does dynamic shape narrow the margin toward that alternative, widen the selected carrier, or remain neutral?",
        "",
        "This audit does not assert which action is optimal. It only marks generic public structural contexts for manual review. Widening the selected carrier may be legitimate if the local shape really supports stabilization; it is a watchpoint if CO expected pre-blocking exposure/relief pressure.",
        "",
        "## Next recommended step",
        "",
        "Manually inspect the directional contexts, especially maintenance modes. If widening toward the selected carrier is not justified by shape/certificate state, the issue is readout/control adequacy, not a missing new concept.",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
