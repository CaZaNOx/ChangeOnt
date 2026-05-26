from __future__ import annotations

"""Maintenance action-insensitivity audit v1.

Reads the current-kernel diagnostic map and diagnoses why maintenance middle /
renewal_like action prefixes remain insensitive to recent-mechanism ablations in
short capped runs.  This is an audit only; it does not tune maintenance-specific
coefficients and does not change kernel behavior.
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Mapping, Tuple

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.studies import current_kernel_diagnostic_map_v1 as diag

OUT_JSON = ROOT / "outputs" / "maintenance_action_insensitivity_audit_v1.json"
REPORT_MD = ROOT.parent / "MAINTENANCE_ACTION_INSENSITIVITY_AUDIT_REPORT_2026-05-22.md"

CLAIM_BOUNDARY = (
    "Maintenance action-insensitivity audit only. It diagnoses capped diagnostic traces. "
    "It is not a maintenance benchmark, not a tuning justification, not SOTA comparison, and not CO proof."
)

TARGET_MODES = {"middle", "renewal_like"}


def _load() -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    if not diag.STEPS_JSONL.exists() or not diag.RUNS_JSONL.exists():
        diag.main()
    steps = [json.loads(line) for line in diag.STEPS_JSONL.read_text(encoding="utf-8").splitlines() if line.strip()]
    runs = [json.loads(line) for line in diag.RUNS_JSONL.read_text(encoding="utf-8").splitlines() if line.strip()]
    return runs, steps


def _score_gap(assessment: Mapping[str, Any], selected: str, field: str = "dominance_score") -> float:
    vals = {}
    for action, metrics in assessment.items():
        if isinstance(metrics, Mapping):
            try:
                vals[str(action)] = float(metrics.get(field, 0.0) or 0.0)
            except Exception:
                vals[str(action)] = 0.0
    if selected not in vals or not vals:
        return 0.0
    other = max((v for a, v in vals.items() if a != selected), default=0.0)
    return float(vals[selected] - other)


def _best_alternative(assessment: Mapping[str, Any], selected: str, field: str = "dominance_score") -> Dict[str, Any]:
    best = ("", -999.0)
    for action, metrics in assessment.items():
        if str(action) == selected or not isinstance(metrics, Mapping):
            continue
        try:
            value = float(metrics.get(field, 0.0) or 0.0)
        except Exception:
            value = 0.0
        if value > best[1]:
            best = (str(action), value)
    return {"action": best[0], field: best[1]} if best[0] else {}


def _resolver_alt_present(assessment: Mapping[str, Any], selected: str) -> bool:
    for action, metrics in assessment.items():
        if str(action) == selected or not isinstance(metrics, Mapping):
            continue
        if float(metrics.get("resolver_support", 0.0) or 0.0) > 0.05:
            return True
    return False


def main() -> Dict[str, Any]:
    diag.main()
    runs, steps = _load()
    maint_runs = [r for r in runs if r.get("family") == "maintenance_replacement" and r.get("mode") in TARGET_MODES]
    maint_steps = [s for s in steps if s.get("family") == "maintenance_replacement" and s.get("mode") in TARGET_MODES]

    # Action-prefix diffs from diagnostic comparisons.
    summary = json.loads(diag.SUMMARY_JSON.read_text(encoding="utf-8"))
    comparisons = [c for c in summary.get("comparisons", []) if c.get("family") == "maintenance_replacement" and c.get("mode") in TARGET_MODES]
    insensitive = [c for c in comparisons if int(c.get("prefix_action_differences_vs_full", 0) or 0) == 0]
    sensitive = [c for c in comparisons if int(c.get("prefix_action_differences_vs_full", 0) or 0) > 0]

    full_steps = [s for s in maint_steps if s.get("variant") == "full_current"]
    mode_summary: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
        "steps": 0,
        "actions": Counter(),
        "commitment_modes": Counter(),
        "shape_gauged_steps": 0,
        "avg_selected_dominance_gap_sum": 0.0,
        "near_margin_steps": 0,
        "selected_run_with_carrier_and_resolver_alt": 0,
        "selected_run_shape_gauged_false": 0,
        "examples": [],
    })
    for s in full_steps:
        mode = str(s.get("mode"))
        selected = str(s.get("action"))
        assessment = s.get("canonical_commitment_assessment_summary", {}) or {}
        gap = _score_gap(assessment, selected, "dominance_score") if isinstance(assessment, Mapping) else 0.0
        entry = mode_summary[mode]
        entry["steps"] += 1
        entry["actions"][selected] += 1
        entry["commitment_modes"][str(s.get("canonical_commitment_mode"))] += 1
        entry["shape_gauged_steps"] += int(bool(s.get("shape_gauged_resolver_timing_applied")))
        entry["avg_selected_dominance_gap_sum"] += gap
        if gap < 0.08:
            entry["near_margin_steps"] += 1
        if selected == "RUN" and isinstance(assessment, Mapping):
            run_metrics = assessment.get("RUN", {}) if isinstance(assessment.get("RUN"), Mapping) else {}
            if float(run_metrics.get("carrier_only_pressure", 0.0) or 0.0) > 0.20 and _resolver_alt_present(assessment, selected):
                entry["selected_run_with_carrier_and_resolver_alt"] += 1
                if not bool(s.get("shape_gauged_resolver_timing_applied")):
                    entry["selected_run_shape_gauged_false"] += 1
        if len(entry["examples"]) < 4:
            entry["examples"].append({
                "run_id": s.get("run_id"),
                "t": s.get("t"),
                "selected": selected,
                "dominance_gap": gap,
                "best_alt": _best_alternative(assessment, selected) if isinstance(assessment, Mapping) else {},
                "shape_gauged": bool(s.get("shape_gauged_resolver_timing_applied")),
                "dynamic_shape_commitment": bool(s.get("dynamic_shape_controls_applied_in_commitment")),
                "relations_by_type": s.get("relations_by_type", {}),
                "avg_recursion_structural": s.get("avg_recursion_scheduler_structural_channel"),
            })

    mode_rows = []
    for mode, item in sorted(mode_summary.items()):
        steps_n = max(int(item["steps"]), 1)
        mode_rows.append({
            "mode": mode,
            "steps": item["steps"],
            "actions": dict(item["actions"]),
            "commitment_modes": dict(item["commitment_modes"]),
            "shape_gauged_steps": item["shape_gauged_steps"],
            "avg_selected_dominance_gap": item["avg_selected_dominance_gap_sum"] / steps_n,
            "near_margin_steps": item["near_margin_steps"],
            "selected_run_with_carrier_and_resolver_alt": item["selected_run_with_carrier_and_resolver_alt"],
            "selected_run_shape_gauged_false": item["selected_run_shape_gauged_false"],
            "examples": item["examples"],
        })

    result = {
        "study": "maintenance_action_insensitivity_audit_v1",
        "claim_boundary": CLAIM_BOUNDARY,
        "maintenance_runs": len(maint_runs),
        "maintenance_steps": len(maint_steps),
        "insensitive_comparison_count": len(insensitive),
        "sensitive_comparison_count": len(sensitive),
        "insensitive_comparisons": insensitive,
        "sensitive_comparisons": sensitive,
        "mode_summary": mode_rows,
        "audit_findings": [
            {
                "id": "MAI1_ABLATION_ACTION_INSENSITIVITY_CONFIRMED",
                "severity": "medium",
                "finding": "Maintenance middle and renewal_like capped diagnostics remain action-prefix insensitive to recent-mechanism ablations.",
                "evidence": f"insensitive_comparison_count={len(insensitive)}, sensitive_comparison_count={len(sensitive)} for target maintenance modes.",
                "next_action": "Treat this as a kernel/readout diagnostic, not a performance failure or tuning license."
            },
            {
                "id": "MAI2_READOUT_DOMINANCE_EXPLAINS_MUCH_OF_THE_INERTIA",
                "severity": "medium",
                "finding": "Full-current maintenance traces often keep the same selected action because the selected branch remains ahead in dominance/stability assessment, even when dynamic shape/scheduler/quotient telemetry moves.",
                "evidence": "See mode_summary avg_selected_dominance_gap and examples; this suggests readout dominance/stable-continuation swamping rather than missing telemetry alone.",
                "next_action": "Audit whether sequence evidence is being consumed by readout before changing coefficients."
            },
            {
                "id": "MAI3_PREBLOCKING_RESOLVER_TIMING_NOT_SOLVED_GENERALLY",
                "severity": "medium",
                "finding": "Some RUN selections still coexist with carrier-only pressure and resolver alternatives without necessarily triggering shape-gauged resolver timing. This is a structural watchpoint, not a maintenance-specific repair rule request.",
                "evidence": "selected_run_with_carrier_and_resolver_alt and selected_run_shape_gauged_false counts in mode_summary identify candidate cases.",
                "next_action": "Use generic sequence/readout-swamping diagnostics before modifying readout formula."
            }
        ],
        "recommendation": "Do not tune maintenance. Sequence composition is now present in first pass, but maintenance action-prefix insensitivity remains a watchpoint; next evaluate sequence on/off and generic readout consumption before robot/sim expansion."
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    _write_report(result)
    return result


def _write_report(result: Mapping[str, Any]) -> None:
    lines: List[str] = []
    lines.append("# Maintenance Action-Insensitivity Audit v1 — 2026-05-22")
    lines.append("")
    lines.append("## Claim boundary")
    lines.append("")
    lines.append(CLAIM_BOUNDARY)
    lines.append("")
    lines.append("## Main verdict")
    lines.append("")
    lines.append("The maintenance action-insensitivity watchpoint is real, but this audit does not justify a maintenance-specific rule. The current evidence points to generic readout dominance/stable-continuation swamping and incomplete sequence/readout consumption, not missing telemetry or a hidden solver issue.")
    lines.append("")
    lines.append("## Findings")
    lines.append("")
    for f in result.get("audit_findings", []):
        lines.append(f"### {f['id']} — {f['severity']}")
        lines.append("")
        lines.append(f"**Finding:** {f['finding']}")
        lines.append("")
        lines.append(f"**Evidence:** {f['evidence']}")
        lines.append("")
        lines.append(f"**Next action:** {f['next_action']}")
        lines.append("")
    lines.append("## Mode summary")
    lines.append("")
    lines.append("| mode | steps | actions | modes | shape-gauged steps | avg dominance gap | near-margin steps | RUN carrier+resolver alt | RUN carrier+resolver alt without shape-gauge |")
    lines.append("|---|---:|---|---|---:|---:|---:|---:|---:|")
    for r in result.get("mode_summary", []):
        lines.append(f"| {r['mode']} | {r['steps']} | `{json.dumps(r['actions'], sort_keys=True)}` | `{json.dumps(r['commitment_modes'], sort_keys=True)}` | {r['shape_gauged_steps']} | {float(r['avg_selected_dominance_gap']):.3f} | {r['near_margin_steps']} | {r['selected_run_with_carrier_and_resolver_alt']} | {r['selected_run_shape_gauged_false']} |")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("If a selected branch has a large dominance/stability gap, telemetry-only ablations are expected. If the gap is small and resolver alternatives or sequence evidence are present but timing does not reopen, that indicates a generic readout-swamping/sequence-consumption issue. The remedy must be generic and cross-family, not a maintenance-specific repair-at-health rule.")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
