from __future__ import annotations

"""Generic readout-swamping trace audit v1.

Audit-only study.  It inspects the current diagnostic trace after carrier-gate
calibration to decide whether remaining action-insensitivity looks like generic
readout swamping, legitimate non-decisiveness, or insufficient trace depth.  It
must not introduce family-specific fixes.
"""

import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, List, Mapping

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.studies.current_kernel_diagnostic_map_v1 import main as run_diagnostic_map

STEPS_JSONL = ROOT / "outputs" / "current_kernel_diagnostic_map_v1" / "steps.jsonl"
OUT_JSON = ROOT / "outputs" / "generic_readout_swamping_trace_audit_v1.json"
REPORT_MD = ROOT.parent / "GENERIC_READOUT_SWAMPING_TRACE_AUDIT_REPORT_2026-05-22.md"

CLAIM_BOUNDARY = (
    "Generic readout-swamping trace audit only. It is not a benchmark, not SOTA comparison, not CO proof, "
    "and not a license for family-specific tuning or action-name rules."
)


def _json_safe(x: Any) -> Any:
    if isinstance(x, Mapping):
        return {str(k): _json_safe(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_json_safe(v) for v in x]
    if isinstance(x, (str, int, float, bool)) or x is None:
        return x
    return str(x)


def _write_json(path: Path, data: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_json_safe(data), indent=2, sort_keys=True), encoding="utf-8")


def _load_steps() -> List[Dict[str, Any]]:
    if not STEPS_JSONL.exists():
        run_diagnostic_map()
    return [json.loads(line) for line in STEPS_JSONL.read_text(encoding="utf-8").splitlines() if line.strip()]


def _f(x: Any, default: float = 0.0) -> float:
    try:
        return float(x)
    except Exception:
        return default


def _selected_assessment(step: Mapping[str, Any]) -> Dict[str, Any]:
    a = step.get("action")
    ass = step.get("canonical_commitment_assessment_summary", {})
    if not isinstance(ass, Mapping):
        return {}
    if str(a) in ass and isinstance(ass[str(a)], Mapping):
        return dict(ass[str(a)])
    if a in ass and isinstance(ass[a], Mapping):
        return dict(ass[a])
    return {}


def _selected_row(step: Mapping[str, Any]) -> Dict[str, Any]:
    a = step.get("action")
    for row in step.get("row_trace_sample", []) or []:
        if isinstance(row, Mapping) and str(row.get("action")) == str(a):
            return dict(row)
    return {}


def _support_field_share(ass: Mapping[str, Any]) -> float:
    pos = _f(ass.get("dominance_positive_mass"))
    if pos <= 1e-9:
        return 0.0
    return max(0.0, min(1.0, (_f(ass.get("dominance_support_component")) + _f(ass.get("dominance_stability_component")) + _f(ass.get("dominance_field_component"))) / pos))


def _penalty_ratio(ass: Mapping[str, Any]) -> float:
    pos = _f(ass.get("dominance_positive_mass"))
    if pos <= 1e-9:
        return 0.0
    return max(0.0, (_f(ass.get("dominance_negative_mass"))) / pos)


def _candidate_has_resolver_alt(step: Mapping[str, Any]) -> bool:
    selected = str(step.get("action"))
    for row in step.get("row_trace_sample", []) or []:
        if not isinstance(row, Mapping) or str(row.get("action")) == selected:
            continue
        qprof = str(row.get("relation_surface_quotient_profile", "")).lower()
        bid = str(row.get("branch_id", "")).lower()
        # Generic operation names only; no native action labels.
        if any(tok in qprof or tok in bid for tok in ("/relief/", ":reduce:", ":reset:", ":cancel:", ":reveal:", ":expose:", "/expose/", "/cancel/", "/relief/")):
            return True
    return False


def _summarize_steps(steps: Iterable[Mapping[str, Any]]) -> Dict[str, Any]:
    steps = list(steps)
    support_shares: List[float] = []
    penalty_ratios: List[float] = []
    high_share_low_penalty = 0
    carrier_with_resolver = 0
    no_shape_trigger = 0
    dominance_count = 0
    sequence_active_steps = 0
    sequence_active_rows = 0
    samples: List[Dict[str, Any]] = []
    for s in steps:
        ass = _selected_assessment(s)
        if not ass:
            continue
        share = _support_field_share(ass)
        penalty = _penalty_ratio(ass)
        support_shares.append(share)
        penalty_ratios.append(penalty)
        if str(s.get("canonical_commitment_mode")) == "dominance":
            dominance_count += 1
        step_sequence_rows = 0
        for rr in s.get("row_trace_sample", []) or []:
            if isinstance(rr, Mapping) and rr.get("sequence_composition_active"):
                step_sequence_rows += 1
        sequence_active_rows += step_sequence_rows
        if step_sequence_rows > 0:
            sequence_active_steps += 1
        if share >= 0.80 and penalty <= 0.35:
            high_share_low_penalty += 1
        has_resolver = _candidate_has_resolver_alt(s)
        if has_resolver:
            carrier_with_resolver += 1
            if not s.get("shape_gauged_resolver_timing_applied"):
                no_shape_trigger += 1
                if len(samples) < 12:
                    sr = _selected_row(s)
                    samples.append({
                        "family": s.get("family"),
                        "mode": s.get("mode"),
                        "variant": s.get("variant"),
                        "t": s.get("t"),
                        "action": s.get("action"),
                        "commitment_mode": s.get("canonical_commitment_mode"),
                        "commitment_reason": s.get("canonical_commitment_reason"),
                        "support_stability_field_share": share,
                        "penalty_ratio": penalty,
                        "dominance_positive_mass": ass.get("dominance_positive_mass"),
                        "dominance_negative_mass": ass.get("dominance_negative_mass"),
                        "carrier_only_pressure": ass.get("carrier_only_pressure"),
                        "resolver_support": ass.get("resolver_support"),
                        "selected_memory_id": sr.get("continuation_memory_id"),
                        "selected_branch_id": sr.get("branch_id"),
                    })
    return {
        "steps": len(steps),
        "dominance_steps": dominance_count,
        "avg_support_stability_field_share": mean(support_shares) if support_shares else 0.0,
        "avg_penalty_ratio": mean(penalty_ratios) if penalty_ratios else 0.0,
        "high_support_field_low_penalty_steps": high_share_low_penalty,
        "carrier_with_resolver_alt_steps": carrier_with_resolver,
        "carrier_with_resolver_no_shape_trigger_steps": no_shape_trigger,
        "sequence_active_steps": sequence_active_steps,
        "sequence_active_rows": sequence_active_rows,
        "sample_carrier_resolver_no_trigger": samples,
    }


def _ablation_insensitivity(steps: List[Mapping[str, Any]]) -> Dict[str, Any]:
    by_key: Dict[tuple, List[Mapping[str, Any]]] = defaultdict(list)
    for s in steps:
        by_key[(s.get("family"), s.get("mode"), s.get("seed"), s.get("variant"))].append(s)
    comparisons: List[Dict[str, Any]] = []
    for (fam, mode, seed, variant), rows in by_key.items():
        if variant != "full_current":
            continue
        full = sorted(rows, key=lambda x: int(x.get("t", 0)))
        full_actions = [str(x.get("action")) for x in full]
        for ablation in ("static_shape", "no_quotient", "no_scheduler", "no_sequence", "minimal_recent_core"):
            alt = sorted(by_key.get((fam, mode, seed, ablation), []), key=lambda x: int(x.get("t", 0)))
            if not alt:
                continue
            alt_actions = [str(x.get("action")) for x in alt]
            n = min(len(full_actions), len(alt_actions))
            diffs = sum(1 for i in range(n) if full_actions[i] != alt_actions[i]) + abs(len(full_actions)-len(alt_actions))
            comparisons.append({"family": fam, "mode": mode, "seed": seed, "ablation": ablation, "steps_compared": n, "action_differences": diffs})
    insensitive = [c for c in comparisons if c["action_differences"] == 0]
    return {"comparisons": comparisons, "insensitive_count": len(insensitive), "sensitive_count": len(comparisons)-len(insensitive), "insensitive_examples": insensitive[:20]}


def main() -> Dict[str, Any]:
    os.environ["CO_STRICT_ERRORS"] = "1"
    steps = _load_steps()
    full = [s for s in steps if s.get("variant") == "full_current"]
    by_fm: Dict[str, Dict[str, Any]] = {}
    for key in sorted({(s.get("family"), s.get("mode")) for s in full}):
        f, m = key
        by_fm[f"{f}::{m}"] = _summarize_steps([s for s in full if s.get("family") == f and s.get("mode") == m])
    overall = _summarize_steps(full)
    ablation = _ablation_insensitivity(steps)
    findings = [
        {
            "id": "GRS1_READOUT_SWAMPING_REMAINS_GENERIC_WATCHPOINT",
            "severity": "medium",
            "finding": "Many selected commitments still have high support/stability/field dominance mass relative to burden/blocker penalties.",
            "evidence": f"avg_support_stability_field_share={overall['avg_support_stability_field_share']:.3f}; avg_penalty_ratio={overall['avg_penalty_ratio']:.3f}",
            "next_action": "Do not tune a family. Sequence composition is now present; use sequence on/off diagnostics and generic resolver-readout tests before any further coefficient change.",
        },
        {
            "id": "GRS2_CARRIER_RESOLVER_NO_TRIGGER_CASES_REMAIN",
            "severity": "medium",
            "finding": "The trace still contains cases where a selected carrier coexists with generic resolver alternatives but shape-gauged timing does not trigger.",
            "evidence": f"carrier_with_resolver_alt_steps={overall['carrier_with_resolver_alt_steps']}; no_shape_trigger={overall['carrier_with_resolver_no_shape_trigger_steps']}",
            "next_action": "Separate legitimate non-decisiveness from insufficient sequence-readout consumption; no native action-name patch.",
        },
        {
            "id": "GRS3_ABLATION_INSENSITIVITY_REMAINS_FAMILY_DEPENDENT",
            "severity": "medium",
            "finding": "Some families/modes remain action-prefix insensitive to recent generic mechanism ablations while others are sensitive.",
            "evidence": f"insensitive_comparisons={ablation['insensitive_count']}; sensitive_comparisons={ablation['sensitive_count']}",
            "next_action": "Inspect whether insensitive families lack decisive structural relations, have dominance swamping, or fail to consume sequence evidence before adding robot/sim.",
        },
    ]
    out = {
        "study": "generic_readout_swamping_trace_audit_v1",
        "claim_boundary": CLAIM_BOUNDARY,
        "full_current_steps": len(full),
        "overall": overall,
        "by_family_mode": by_fm,
        "ablation_insensitivity": ablation,
        "audit_findings": findings,
        "recommendation": "Do not add family-specific fixes. Generic sequence-composition is now present in first pass; next use sequence on/off diagnostics to decide whether remaining swamping is legitimate non-decisiveness, weak sequence-readout consumption, or a generic readout-design failure.",
    }
    _write_json(OUT_JSON, out)
    _write_report(out)
    return out


def _fmt(x: Any) -> str:
    try:
        return f"{float(x):.3f}"
    except Exception:
        return str(x)


def _write_report(data: Mapping[str, Any]) -> None:
    lines: List[str] = []
    lines.append("# Generic Readout-Swamping Trace Audit v1 — 2026-05-22")
    lines.append("")
    lines.append("## Claim boundary")
    lines.append("")
    lines.append(CLAIM_BOUNDARY)
    lines.append("")
    lines.append("## Overall")
    lines.append("")
    ov = data["overall"]
    lines.append(f"Full-current steps: {data['full_current_steps']}.")
    lines.append(f"Average support/stability/field share of positive dominance mass: {_fmt(ov['avg_support_stability_field_share'])}.")
    lines.append(f"Average dominance penalty ratio: {_fmt(ov['avg_penalty_ratio'])}.")
    lines.append(f"Carrier-with-resolver-alt steps: {ov['carrier_with_resolver_alt_steps']}.")
    lines.append(f"Carrier-with-resolver-alt without shape trigger: {ov['carrier_with_resolver_no_shape_trigger_steps']}.")
    lines.append(f"Steps with active sequence composition: {ov['sequence_active_steps']}.")
    lines.append(f"Active sequence rows: {ov['sequence_active_rows']}.")
    lines.append("")
    lines.append("## Findings")
    lines.append("")
    for f in data.get("audit_findings", []):
        lines.append(f"### {f['id']} ({f['severity']})")
        lines.append("")
        lines.append(f"Finding: {f['finding']}")
        lines.append("")
        lines.append(f"Evidence: {f['evidence']}")
        lines.append("")
        lines.append(f"Next action: {f['next_action']}")
        lines.append("")
    lines.append("## By family/mode")
    lines.append("")
    lines.append("| family/mode | steps | dominance steps | avg support-field share | avg penalty ratio | carrier+resolver | no trigger | seq steps | seq rows |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for k, v in sorted(data.get("by_family_mode", {}).items()):
        lines.append(f"| {k} | {v['steps']} | {v['dominance_steps']} | {_fmt(v['avg_support_stability_field_share'])} | {_fmt(v['avg_penalty_ratio'])} | {v['carrier_with_resolver_alt_steps']} | {v['carrier_with_resolver_no_shape_trigger_steps']} | {v['sequence_active_steps']} | {v['sequence_active_rows']} |")
    lines.append("")
    lines.append("## Sample carrier/resolver/no-trigger cases")
    lines.append("")
    for s in ov.get("sample_carrier_resolver_no_trigger", [])[:12]:
        lines.append(f"- `{s['family']}::{s['mode']}` t={s['t']} action=`{s['action']}` share={_fmt(s['support_stability_field_share'])} penalty={_fmt(s['penalty_ratio'])} reason=`{s['commitment_reason']}`")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("The remaining watchpoint is generic: current readout can still privilege support/stability/field mass over unresolved burden and phase-like resolver alternatives. Generic sequence-composition is now present in first pass, so the next question is not whether to add a sequence layer, but whether the readout consumes sequence evidence appropriately or still collapses into dominance scoring. The trace does not justify a family-specific patch.")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
