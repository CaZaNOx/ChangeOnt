from __future__ import annotations

"""Pass-1 kernel closure audit v1.

This is a freeze/evaluation audit for the rough kernel closure candidate. It does
not add kernel behavior, tune coefficients, or claim empirical proof. It parses
already-run first-pass diagnostic outputs and classifies the state of the rough
kernel against the Pass-1 project goal:

- Are the known required kernel mechanisms present?
- Are they telemetry-visible?
- Are they behavior-causal across current families?
- Which watchpoints block public release / Pass-2 transition?

The verdict is intentionally conservative.
"""

import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, List

ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = ROOT / "outputs" / "pass1_kernel_closure_audit_v1.json"
REPORT_MD = ROOT.parent / "PASS1_KERNEL_CLOSURE_AUDIT_REPORT_2026-05-22.md"

CLAIM_BOUNDARY = (
    "Freeze/evaluation audit only. It does not add a kernel mechanism, does not tune performance, "
    "does not constitute benchmark evidence, and does not prove CO's usefulness or novelty."
)


def _read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    rows: List[Dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _safe_float(x: Any) -> float:
    try:
        return float(x or 0.0)
    except Exception:
        return 0.0


def _fmt(x: Any) -> str:
    try:
        return f"{float(x):.3f}"
    except Exception:
        return str(x)


def _sum_cmp(comparisons: Iterable[Mapping[str, Any]]) -> Dict[str, Any]:
    by_ablation: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
        "comparisons": 0,
        "families_with_action_diff": 0,
        "prefix_action_differences": 0,
        "metric_abs_delta_sum": 0.0,
        "sequence_active_step_delta": 0,
        "dynamic_step_delta": 0,
    })
    by_family: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"comparisons": 0, "ablation_diff_cases": 0, "prefix_action_differences": 0})
    for c in comparisons:
        ab = str(c.get("ablation", ""))
        fam = f"{c.get('family')}::{c.get('mode')}"
        diff = int(c.get("prefix_action_differences_vs_full", 0) or 0)
        b = by_ablation[ab]
        b["comparisons"] += 1
        b["families_with_action_diff"] += int(diff > 0)
        b["prefix_action_differences"] += diff
        b["metric_abs_delta_sum"] += abs(_safe_float(c.get("metric_delta_vs_full")))
        b["sequence_active_step_delta"] += int(c.get("sequence_active_step_delta_vs_full", 0) or 0)
        b["dynamic_step_delta"] += int(c.get("dynamic_shape_step_delta_vs_full", 0) or 0)
        bf = by_family[fam]
        bf["comparisons"] += 1
        bf["ablation_diff_cases"] += int(diff > 0)
        bf["prefix_action_differences"] += diff
    return {"by_ablation": dict(by_ablation), "by_family_mode": dict(by_family)}


def _presence_check() -> Dict[str, bool]:
    files = {
        "dynamic_shape_field": ROOT / "agents" / "co" / "runtime" / "surfaces" / "dynamic_shape_field.py",
        "sequence_composition": ROOT / "agents" / "co" / "runtime" / "surfaces" / "sequence_composition.py",
        "quotient_equivalence": ROOT / "agents" / "co" / "runtime" / "surfaces" / "quotient_equivalence.py",
        "recursion_scheduler": ROOT / "agents" / "co" / "runtime" / "surfaces" / "recursion_scheduler.py",
        "relation_surface": ROOT / "agents" / "co" / "runtime" / "surfaces" / "relation_surface.py",
        "collapse_certificate": ROOT / "agents" / "co" / "runtime" / "surfaces" / "collapse_certificate.py",
        "commitment_surface": ROOT / "agents" / "co" / "runtime" / "surfaces" / "commitment_surface.py",
        "candidate_surface": ROOT / "agents" / "co" / "runtime" / "surfaces" / "candidate_surface.py",
    }
    return {k: p.exists() for k, p in files.items()}


def main() -> Dict[str, Any]:
    diag = _read_json(ROOT / "outputs" / "current_kernel_diagnostic_map_v1" / "summary.json", {})
    runs = _read_jsonl(ROOT / "outputs" / "current_kernel_diagnostic_map_v1" / "runs.jsonl")
    seq = _read_json(ROOT / "outputs" / "sequence_level_continuation_composition_audit_v1.json", {})
    swamping = _read_json(ROOT / "outputs" / "generic_readout_swamping_trace_audit_v1.json", {})
    maint = _read_json(ROOT / "outputs" / "maintenance_action_insensitivity_audit_v1.json", {})
    arch = _read_json(ROOT / "outputs" / "architecture_acceptance_audit_v1.json", {})
    structural = _read_json(ROOT / "outputs" / "structural_trace_validation_v1.json", {})
    quotient = _read_json(ROOT / "outputs" / "quotient_accept_reject_audit_v1.json", {})
    adapter_cov = _read_json(ROOT / "outputs" / "adapter_public_effect_relation_coverage_v1.json", {})
    structural_ab = _read_json(ROOT / "outputs" / "real_adapter_structural_ablation_review_v1.json", {})
    cert_gate = _read_json(ROOT / "outputs" / "real_adapter_certificate_gating_review_v1.json", {})
    formula = _read_json(ROOT / "outputs" / "real_adapter_formula_sensitivity_probe_v1.json", {})

    comparisons = list(diag.get("comparisons", []) or [])
    cmp_summary = _sum_cmp(comparisons)
    presence = _presence_check()

    full_runs = [r for r in runs if r.get("variant") == "full_current"]
    def avg(key: str) -> float:
        return sum(_safe_float(r.get(key)) for r in full_runs) / max(len(full_runs), 1)

    mechanism_visibility = {
        "full_current_runs": len(full_runs),
        "avg_dynamic_shape_applied_steps": avg("dynamic_shape_applied_steps"),
        "avg_sequence_active_steps": avg("sequence_active_steps"),
        "avg_sequence_rows": avg("avg_sequence_rows"),
        "avg_quotient_rows": avg("avg_quotient_rows"),
        "avg_recursion_scheduler_demand": avg("avg_recursion_scheduler_demand"),
        "runs_with_sequence_steps": sum(1 for r in full_runs if int(r.get("sequence_active_steps", 0) or 0) > 0),
        "runs_with_quotient_rows": sum(1 for r in full_runs if _safe_float(r.get("avg_quotient_rows")) > 0.0),
        "runs_with_dynamic_shape": sum(1 for r in full_runs if int(r.get("dynamic_shape_applied_steps", 0) or 0) > 0),
    }

    blocking_watchpoints = [
        {
            "id": "P1A_RELEASE_NOT_READY_ARCHITECTURE_WATCHPOINTS",
            "severity": "blocking-for-release",
            "evidence": f"architecture_acceptance_audit_v1 status={arch.get('status')}",
            "interpretation": "The closure candidate is not architecture-accepted; Pass-1 can proceed only as a diagnostic/research state.",
        },
        {
            "id": "P1A_STRUCTURAL_TRACE_WATCHPOINTS_REMAIN",
            "severity": "blocking-for-release",
            "evidence": f"structural_trace_validation_v1 status={structural.get('status')}; cases_with_watchpoints={(structural.get('summary', {}) or {}).get('cases_with_watchpoints') or (structural.get('aggregate', {}) or {}).get('cases_with_watchpoints') or structural.get('cases_with_watchpoints')}",
            "interpretation": "Structural trace validation is not clean enough for public strong claims.",
        },
        {
            "id": "P1A_SEQUENCE_PRESENT_EFFECT_UNPROVEN",
            "severity": "major-pass1-watchpoint",
            "evidence": f"sequence_field_rows={seq.get('sequence_field_rows')}; sequence_active_rows={seq.get('sequence_active_rows')}; no_sequence action-diff cases={cmp_summary['by_ablation'].get('no_sequence', {}).get('families_with_action_diff')}",
            "interpretation": "Sequence composition exists and is telemetry-visible, but current capped diagnostics show limited action-level causal effect.",
        },
        {
            "id": "P1A_MAINTENANCE_INSENSITIVITY_UNRESOLVED",
            "severity": "major-pass1-watchpoint",
            "evidence": f"maintenance insensitive={maint.get('insensitive_comparison_count')}; sensitive={maint.get('sensitive_comparison_count')}",
            "interpretation": "Maintenance middle/renewal-like remain insensitive under recent-mechanism ablations; do not patch maintenance specifically.",
        },
        {
            "id": "P1A_READOUT_SWAMPING_REMAINS",
            "severity": "major-pass1-watchpoint",
            "evidence": f"carrier_with_resolver_alt_steps={(swamping.get('overall', {}) or {}).get('carrier_with_resolver_alt_steps')}; carrier_with_resolver_no_shape_trigger_steps={(swamping.get('overall', {}) or {}).get('carrier_with_resolver_no_shape_trigger_steps')}; support/stability share={(swamping.get('overall', {}) or {}).get('avg_support_stability_field_share')}",
            "interpretation": "Support/stability/field dominance still risks collapsing CO structure into ordinary scoring-like readout.",
        },
        {
            "id": "P1A_QUOTIENT_CONSERVATIVE_CALIBRATION_OPEN",
            "severity": "medium-watchpoint",
            "evidence": f"duplicate_signature_bug_count={quotient.get('duplicate_signature_bug_count')}; possible_calibration_site_count={quotient.get('possible_calibration_site_count')}; accepted_singletons={quotient.get('accepted_singletons_in_trace_sample')}",
            "interpretation": "No obvious duplicate-signature bug found, but quotienting is mostly conservative/singleton and needs false/missed quotient calibration.",
        },
        {
            "id": "P1A_ADAPTER_BOUNDARY_AND_FORMULA_GROUNDING_STILL_REQUIRED",
            "severity": "major-pass1-watchpoint",
            "evidence": "adapter structural ablations are behavior-causal, but formulas and translator richness remain possible hidden-shaping risks.",
            "interpretation": "Before public release, adapter-boundary adversarial tests and formula/coefficient grounding must be strengthened.",
        },
    ]

    verdict = {
        "pass1_kernel_mechanism_set_present": all(presence.values()),
        "pass1_kernel_closure_candidate": all(presence.values()) and int(diag.get("runs_failed", 999)) == 0,
        "release_ready": False,
        "publication_ready": False,
        "recommended_state": "freeze rough kernel for evaluation; do not add new mechanisms unless necessity gate passes",
    }

    next_actions = [
        "Do not add robot/sim yet as evidence. First resolve/characterize sequence-readout consumption and maintenance/readout insensitivity.",
        "Run broader multi-seed/current-family diagnostics after freezing mechanism set, including no_sequence, no_scheduler, no_quotient, static_shape and minimal_recent_core.",
        "Add adapter-boundary adversarial tests: thin translator, remove public effects, perturb irrelevant labels, and compare rich vs minimal public effects.",
        "Add coefficient sensitivity around readout/sequence consumption, not just resolver thresholds; classify coefficients as derived/provisional/empirical.",
        "Decide whether remaining readout swamping is a bug, an expected limitation, or evidence that CO currently degenerates into scoring in some regimes.",
        "Only after that, design small robot/sim tasks as stress tests for dynamic admissibility, exposure, affordance, and sequence continuation.",
    ]

    result = {
        "study": "pass1_kernel_closure_audit_v1",
        "claim_boundary": CLAIM_BOUNDARY,
        "presence": presence,
        "diagnostic_map": {
            "runs_attempted": diag.get("runs_attempted"),
            "runs_succeeded": diag.get("runs_succeeded"),
            "runs_failed": diag.get("runs_failed"),
            "tasks": diag.get("tasks"),
            "variants": list((diag.get("variants") or {}).keys()),
        },
        "mechanism_visibility": mechanism_visibility,
        "ablation_sensitivity": cmp_summary,
        "adapter_boundary_snapshot": {
            "public_effect_coverage": adapter_cov.get("aggregate", {}),
            "structural_ablation_summary": (structural_ab.get("summary", {}) or {}).get("comparisons_vs_full", {}),
            "certificate_gating_summary": cert_gate.get("summary", {}),
            "formula_sensitivity_summary": formula.get("summary", {}),
        },
        "blocking_watchpoints": blocking_watchpoints,
        "verdict": verdict,
        "next_actions": next_actions,
    }
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    _write_report(result)
    return result


def _write_report(result: Mapping[str, Any]) -> None:
    v = result["verdict"]
    vis = result["mechanism_visibility"]
    ab = result["ablation_sensitivity"]["by_ablation"]
    fam = result["ablation_sensitivity"]["by_family_mode"]
    lines: List[str] = []
    lines.append("# Pass-1 Kernel Closure Audit v1 — 2026-05-22")
    lines.append("")
    lines.append("## Claim boundary")
    lines.append("")
    lines.append(CLAIM_BOUNDARY)
    lines.append("")
    lines.append("## Verdict")
    lines.append("")
    lines.append(f"- Known rough mechanism files present: `{v['pass1_kernel_mechanism_set_present']}`.")
    lines.append(f"- Pass-1 kernel closure candidate: `{v['pass1_kernel_closure_candidate']}`.")
    lines.append(f"- Release-ready: `{v['release_ready']}`.")
    lines.append(f"- Publication-ready: `{v['publication_ready']}`.")
    lines.append("")
    lines.append("Interpretation: the rough mechanism set is present, but this is not a clean release state. The correct state is to freeze the rough kernel for evaluation and treat the remaining findings as blockers/watchpoints, not as justification for hidden benchmark rescue patches.")
    lines.append("")
    lines.append("## Mechanism presence")
    lines.append("")
    lines.append("| mechanism file | present |")
    lines.append("|---|---:|")
    for k, val in sorted(result["presence"].items()):
        lines.append(f"| `{k}` | {val} |")
    lines.append("")
    d = result["diagnostic_map"]
    lines.append("## Diagnostic map scope")
    lines.append("")
    lines.append(f"Runs attempted: `{d.get('runs_attempted')}`; succeeded: `{d.get('runs_succeeded')}`; failed: `{d.get('runs_failed')}`.")
    lines.append("")
    lines.append("Variants: `" + "`, `".join(d.get("variants") or []) + "`.")
    lines.append("")
    lines.append("## Mechanism visibility in full-current runs")
    lines.append("")
    lines.append(f"- Full-current runs: `{vis['full_current_runs']}`.")
    lines.append(f"- Avg dynamic-shape-applied steps: `{_fmt(vis['avg_dynamic_shape_applied_steps'])}`.")
    lines.append(f"- Avg sequence-active steps: `{_fmt(vis['avg_sequence_active_steps'])}`.")
    lines.append(f"- Avg sequence rows: `{_fmt(vis['avg_sequence_rows'])}`.")
    lines.append(f"- Avg quotient rows: `{_fmt(vis['avg_quotient_rows'])}`.")
    lines.append(f"- Avg recursion scheduler demand: `{_fmt(vis['avg_recursion_scheduler_demand'])}`.")
    lines.append("")
    lines.append("## Ablation sensitivity")
    lines.append("")
    lines.append("### By ablation")
    lines.append("")
    lines.append("| ablation | comparisons | families/modes with action diff | prefix action diffs | metric abs delta sum | sequence step delta | dynamic step delta |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for k, row in sorted(ab.items()):
        lines.append(f"| `{k}` | {row['comparisons']} | {row['families_with_action_diff']} | {row['prefix_action_differences']} | {_fmt(row['metric_abs_delta_sum'])} | {row['sequence_active_step_delta']} | {row['dynamic_step_delta']} |")
    lines.append("")
    lines.append("### By family/mode")
    lines.append("")
    lines.append("| family/mode | ablation comparisons | comparisons with action diff | prefix action diffs |")
    lines.append("|---|---:|---:|---:|")
    for k, row in sorted(fam.items()):
        lines.append(f"| `{k}` | {row['comparisons']} | {row['ablation_diff_cases']} | {row['prefix_action_differences']} |")
    lines.append("")
    lines.append("## Blocking watchpoints")
    lines.append("")
    for w in result["blocking_watchpoints"]:
        lines.append(f"### {w['id']} — {w['severity']}")
        lines.append("")
        lines.append(f"Evidence: {w['evidence']}")
        lines.append("")
        lines.append(f"Interpretation: {w['interpretation']}")
        lines.append("")
    lines.append("## Required next actions")
    lines.append("")
    for i, action in enumerate(result["next_actions"], start=1):
        lines.append(f"{i}. {action}")
    lines.append("")
    lines.append("## Release statement")
    lines.append("")
    lines.append("This repo state may be called a Pass-1 kernel closure candidate, not a finished kernel, not a public empirical result, and not a publication-ready CO system. The next work should evaluate and simplify/harden this frozen candidate rather than automatically adding mechanisms.")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
