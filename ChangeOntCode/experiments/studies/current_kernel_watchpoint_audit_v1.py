from __future__ import annotations

"""Current-kernel watchpoint audit v1.

Reads the current-kernel diagnostic map outputs and classifies the main
watchpoints that must be understood before adding robot/sim problems.  This is
an audit/report generator, not a benchmark and not a tuning pass.
"""

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Tuple

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "outputs" / "current_kernel_diagnostic_map_v1"
AUDIT_JSON = ROOT / "outputs" / "current_kernel_watchpoint_audit_v1.json"
REPORT_MD = ROOT.parent / "CURRENT_KERNEL_WATCHPOINT_AUDIT_REPORT_2026-05-22.md"

CLAIM_BOUNDARY = (
    "Audit of first-pass diagnostic-map watchpoints only. It interprets mechanism "
    "visibility/action sensitivity and code-path alignment. It is not benchmark "
    "evidence, not CO proof, not novelty evidence, and not a coefficient-tuning pass."
)


def _load_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"required diagnostic output missing: {path}")
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def _avg(vals: Iterable[Any]) -> float:
    xs: List[float] = []
    for v in vals:
        try:
            xs.append(float(v or 0.0))
        except Exception:
            pass
    return sum(xs) / float(len(xs) or 1)


def _max(vals: Iterable[Any]) -> float:
    xs: List[float] = []
    for v in vals:
        try:
            xs.append(float(v or 0.0))
        except Exception:
            pass
    return max(xs) if xs else 0.0


def _prefix_diff(a: List[Any], b: List[Any]) -> int:
    n = min(len(a), len(b))
    return sum(1 for i in range(n) if str(a[i]) != str(b[i])) + abs(len(a) - len(b))


def _variant_map(runs: List[Mapping[str, Any]]) -> Dict[Tuple[str, str, int], Dict[str, Mapping[str, Any]]]:
    out: Dict[Tuple[str, str, int], Dict[str, Mapping[str, Any]]] = defaultdict(dict)
    for r in runs:
        if "variant" not in r:
            continue
        out[(str(r.get("family")), str(r.get("mode")), int(r.get("seed", 0)))][str(r.get("variant"))] = r
    return out


def _relation_summary(steps: List[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[Tuple[str, str, str], List[Mapping[str, Any]]] = defaultdict(list)
    for s in steps:
        grouped[(str(s.get("family")), str(s.get("mode")), str(s.get("variant")))].append(s)
    out: List[Dict[str, Any]] = []
    for (family, mode, variant), rows in sorted(grouped.items()):
        c: Counter = Counter()
        modes: Counter = Counter()
        for s in rows:
            c.update(s.get("relations_by_type") or {})
            modes[str(s.get("canonical_commitment_mode"))] += 1
        out.append({
            "family": family,
            "mode": mode,
            "variant": variant,
            "steps": len(rows),
            "relations_by_type_total": dict(c),
            "avg_recursion_demand": _avg(s.get("avg_recursion_scheduler_demand", 0.0) for s in rows),
            "max_recursion_demand": _max(s.get("max_recursion_scheduler_demand", 0.0) for s in rows),
            "avg_quotient_rows": _avg(s.get("quotient_rows", 0.0) for s in rows),
            "shape_resolver_steps": sum(1 for s in rows if s.get("shape_gauged_resolver_timing_applied")),
            "commitment_modes": dict(modes),
        })
    return out


def main() -> Dict[str, Any]:
    runs = _load_jsonl(OUT_DIR / "runs.jsonl")
    steps = _load_jsonl(OUT_DIR / "steps.jsonl")
    vmap = _variant_map(runs)

    telemetry_only: List[Dict[str, Any]] = []
    action_sensitive: List[Dict[str, Any]] = []
    for key, variants in sorted(vmap.items()):
        full = variants.get("full_current")
        if not full:
            continue
        full_prefix = list(full.get("action_trace_prefix", []))
        for ablation in ("static_shape", "no_scheduler", "no_quotient", "minimal_recent_core"):
            row = variants.get(ablation)
            if not row:
                continue
            diff = _prefix_diff(full_prefix, list(row.get("action_trace_prefix", [])))
            dyn_delta = int(row.get("dynamic_shape_applied_steps", 0) or 0) - int(full.get("dynamic_shape_applied_steps", 0) or 0)
            rec_delta = float(row.get("avg_recursion_scheduler_demand", 0.0) or 0.0) - float(full.get("avg_recursion_scheduler_demand", 0.0) or 0.0)
            q_delta = float(row.get("avg_quotient_rows", 0.0) or 0.0) - float(full.get("avg_quotient_rows", 0.0) or 0.0)
            telemetry_delta = (
                (ablation == "static_shape" and dyn_delta != 0)
                or (ablation == "no_scheduler" and abs(rec_delta) > 1e-9)
                or (ablation == "no_quotient" and abs(q_delta) > 1e-9)
                or (ablation == "minimal_recent_core" and (dyn_delta != 0 or abs(rec_delta) > 1e-9 or abs(q_delta) > 1e-9))
            )
            rec = {
                "family": key[0],
                "mode": key[1],
                "seed": key[2],
                "ablation": ablation,
                "prefix_action_diffs": diff,
                "metric_delta": float(row.get("metric_value", 0.0) or 0.0) - float(full.get("metric_value", 0.0) or 0.0),
                "dynamic_step_delta": dyn_delta,
                "avg_recursion_delta": rec_delta,
                "avg_quotient_row_delta": q_delta,
                "full_modes": dict(full.get("commitment_modes", {}) or {}),
                "ablation_modes": dict(row.get("commitment_modes", {}) or {}),
            }
            if diff == 0 and telemetry_delta:
                telemetry_only.append(rec)
            if diff > 0:
                action_sensitive.append(rec)

    weak_only_high_recursion = []
    for s in steps:
        if s.get("variant") != "full_current":
            continue
        rel_types = set((s.get("relations_by_type") or {}).keys())
        if rel_types and rel_types <= {"decision_slot_competition"} and float(s.get("avg_recursion_scheduler_demand", 0.0) or 0.0) >= 0.35:
            weak_only_high_recursion.append({
                "run_id": s.get("run_id"),
                "family": s.get("family"),
                "mode": s.get("mode"),
                "t": int(s.get("t", 0)),
                "avg_recursion_demand": float(s.get("avg_recursion_scheduler_demand", 0.0) or 0.0),
                "max_recursion_demand": float(s.get("max_recursion_scheduler_demand", 0.0) or 0.0),
                "avg_blockers": float(s.get("avg_collapse_blockers", 0.0) or 0.0),
                "commitment_mode": s.get("canonical_commitment_mode"),
            })

    full_relation_summaries = [r for r in _relation_summary(steps) if r["variant"] == "full_current"]
    dynamic_controls_commitment_steps = sum(1 for s in steps if s.get("variant") == "full_current" and bool(s.get("dynamic_shape_controls_applied_in_commitment")))
    deep_trace_steps = sum(1 for s in steps if s.get("row_trace_sample"))
    result = {
        "study": "current_kernel_watchpoint_audit_v1",
        "claim_boundary": CLAIM_BOUNDARY,
        "data_source": {
            "runs_jsonl": str((OUT_DIR / "runs.jsonl").relative_to(ROOT)),
            "steps_jsonl": str((OUT_DIR / "steps.jsonl").relative_to(ROOT)),
        },
        "telemetry_only_ablations": telemetry_only,
        "action_sensitive_ablations": action_sensitive,
        "weak_only_high_recursion_count": len(weak_only_high_recursion),
        "weak_only_high_recursion_examples": weak_only_high_recursion[:8],
        "dynamic_controls_commitment_steps": dynamic_controls_commitment_steps,
        "deep_trace_steps": deep_trace_steps,
        "full_current_relation_summaries": full_relation_summaries,
        "audit_findings": [
            {
                "id": "HF1_DYNAMIC_SHAPE_NOW_READOUT_VISIBLE",
                "severity": "resolved-watchpoint",
                "finding": "DynamicShapeField effective controls are now consumed by CommitmentSurface direct-control snapshot when present, so dynamic shape is no longer only CandidateSurface telemetry.",
                "evidence": f"{dynamic_controls_commitment_steps} full-current diagnostic steps report dynamic_shape_controls_applied_in_commitment=true; direct_controls_used now logs dynamic_shape_* gauge fields.",
                "next_action": "Continue treating dynamic shape as first-pass: audit whether remaining telemetry-only cases are legitimate non-decisiveness or readout dominance."
            },
            {
                "id": "HF2_RECURSION_PROVENANCE_SPLIT",
                "severity": "resolved-watchpoint",
                "finding": "RecursionScheduler now publishes structural, sampling/uncertainty, weak-procedural, and inherited-field channels separately; only the structural channel becomes certificate-facing recursion demand.",
                "evidence": f"{len(weak_only_high_recursion)} full-current steps had avg structural recursion demand >= 0.35 with only decision_slot_competition relations after the split.",
                "next_action": "Audit false negatives/positives on real traces before changing coefficients."
            },
            {
                "id": "HF3_DEEP_TRACE_LOGGING_ADDED",
                "severity": "partially-resolved-watchpoint",
                "finding": "Diagnostic map now logs compact row-level traces, final direct controls, DynamicShapeField effective controls, recursion provenance channels, and canonical commitment assessments.",
                "evidence": f"{deep_trace_steps} diagnostic steps contain row_trace_sample data.",
                "next_action": "Still add quotient accept/reject reason logging; row trace now exposes quotient output but not every rejected profile comparison."
            },
            {
                "id": "WF3_QUOTIENT_CONSERVATIVE_BUT_UNAUDITED_FOR_MISSES",
                "severity": "medium",
                "finding": "Quotienting remains conservative and appears where public residual profiles match, but missed-quotient status is not yet auditable because rejected profile reasons are not logged.",
                "evidence": "quotient rows are mainly latent/maze/maintenance-bandit_like; renewal and maintenance middle/renewal_like still show zero quotient rows despite relation traffic.",
                "next_action": "Log quotient profile accept/reject reasons per step and add a false-quotient/missed-quotient audit before calibration."
            },
            {
                "id": "WF4_MAINTENANCE_ACTION_INSENSITIVITY_REMAINS",
                "severity": "medium",
                "finding": "Maintenance middle/renewal_like remain mostly action-insensitive under recent mechanism ablations in this capped diagnostic even after readout visibility hardening. Some metrics/modes move, but action prefixes remain unchanged.",
                "evidence": "maintenance middle and renewal_like still have zero prefix action differences for static_shape/no_scheduler/no_quotient in the map.",
                "next_action": "Use the new row-level traces to decide whether this is legitimate non-decisiveness or dominance/stable-continuation swamping before tuning coefficients."
            }
        ],
        "recommendation": "Do not add robot/simulation yet. Next audit quotient missed/false equivalence and maintenance action-insensitivity using the newly deepened row-level traces."
    }
    AUDIT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    _write_report(result)
    return result


def _write_report(result: Mapping[str, Any]) -> None:
    lines: List[str] = []
    lines.append("# Current Kernel Watchpoint Audit v1 — 2026-05-22")
    lines.append("")
    lines.append("## Claim boundary")
    lines.append("")
    lines.append(CLAIM_BOUNDARY)
    lines.append("")
    lines.append("## Data source")
    lines.append("")
    lines.append("This audit reads `ChangeOntCode/outputs/current_kernel_diagnostic_map_v1/runs.jsonl` and `steps.jsonl`. It does not rerun benchmarks and does not change kernel behavior.")
    lines.append("")
    lines.append("## Main verdict")
    lines.append("")
    lines.append("The targeted hardening pass made DynamicShapeField readout-visible, split recursion-pressure provenance, and added compact row-level traces. Remaining watchpoints are narrower: quotient missed/false-equivalence audit and maintenance action-insensitivity under capped diagnostic ablations.")
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
    lines.append("## Telemetry-only ablations")
    lines.append("")
    lines.append("These are cases where a recent-mechanism ablation changed mechanism telemetry but did not change the action prefix in the capped run.")
    lines.append("")
    lines.append("| family | mode | ablation | metric Δ | dyn-step Δ | recursion Δ | quotient-row Δ | full modes | ablation modes |")
    lines.append("|---|---|---|---:|---:|---:|---:|---|---|")
    for r in result.get("telemetry_only_ablations", []):
        lines.append(
            "| {family} | {mode} | {ablation} | {md:.3f} | {dd} | {rd:.3f} | {qd:.3f} | `{fm}` | `{am}` |".format(
                family=r["family"], mode=r["mode"], ablation=r["ablation"],
                md=float(r["metric_delta"]), dd=int(r["dynamic_step_delta"]),
                rd=float(r["avg_recursion_delta"]), qd=float(r["avg_quotient_row_delta"]),
                fm=json.dumps(r["full_modes"], sort_keys=True), am=json.dumps(r["ablation_modes"], sort_keys=True),
            )
        )
    lines.append("")
    lines.append("## Full-current relation summaries")
    lines.append("")
    lines.append("| family | mode | avg recursion | max recursion | avg quotient rows | shape resolver steps | relations by type | modes |")
    lines.append("|---|---|---:|---:|---:|---:|---|---|")
    for r in result.get("full_current_relation_summaries", []):
        lines.append(
            "| {family} | {mode} | {ar:.3f} | {mr:.3f} | {q:.3f} | {srs} | `{rel}` | `{modes}` |".format(
                family=r["family"], mode=r["mode"], ar=float(r["avg_recursion_demand"]),
                mr=float(r["max_recursion_demand"]), q=float(r["avg_quotient_rows"]),
                srs=int(r["shape_resolver_steps"]), rel=json.dumps(r["relations_by_type_total"], sort_keys=True),
                modes=json.dumps(r["commitment_modes"], sort_keys=True),
            )
        )
    lines.append("")
    lines.append("## Weak-only high-recursion watchpoint")
    lines.append("")
    lines.append(f"Count: `{result.get('weak_only_high_recursion_count')}` full-current steps had avg recursion demand >= 0.35 while relation types were only `decision_slot_competition`.")
    lines.append("")
    for ex in result.get("weak_only_high_recursion_examples", []):
        lines.append(f"- `{ex['run_id']}` t={ex['t']}: avg={ex['avg_recursion_demand']:.3f}, max={ex['max_recursion_demand']:.3f}, mode={ex['commitment_mode']}")
    lines.append("")
    lines.append("## Recommendation")
    lines.append("")
    lines.append(str(result.get("recommendation")))
    lines.append("")
    lines.append("## Publication/evidence boundary")
    lines.append("")
    lines.append("This audit supports only a local engineering/theory-alignment conclusion: the first-pass kernel has visible generic mechanisms, but the current traces expose specific alignment gaps. It should not be cited as performance evidence or as evidence that CO is useful or novel.")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
