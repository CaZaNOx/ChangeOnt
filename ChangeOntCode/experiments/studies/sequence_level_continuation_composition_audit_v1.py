from __future__ import annotations

"""Sequence-level continuation composition audit v1.

Audit-only study.  It checks whether the current first-pass kernel has moved
beyond action-keyed continuation memory into ordered sequence composition, without
using any family-specific rule as a fix.  It consumes the current-kernel
diagnostic map traces and reports what is visible in generic runtime telemetry.
"""

import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Tuple

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.studies.current_kernel_diagnostic_map_v1 import main as run_diagnostic_map

STEPS_JSONL = ROOT / "outputs" / "current_kernel_diagnostic_map_v1" / "steps.jsonl"
OUT_JSON = ROOT / "outputs" / "sequence_level_continuation_composition_audit_v1.json"
REPORT_MD = ROOT.parent / "SEQUENCE_LEVEL_CONTINUATION_COMPOSITION_AUDIT_REPORT_2026-05-22.md"

CLAIM_BOUNDARY = (
    "Sequence-level continuation composition audit only. It is not a performance test, not a benchmark, "
    "not CO proof, and not a license to introduce family-specific sequence rules."
)

SEQUENCE_FIELD_NAMES = {
    "sequence_continuation_id",
    "sequence_composition_id",
    "continuation_sequence_id",
    "continuation_phase",
    "phase_id",
    "phase_transition",
    "sequence_edge",
    "ordered_continuation_id",
}


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


def _selected_row(step: Mapping[str, Any]) -> Dict[str, Any]:
    action = step.get("action")
    for row in step.get("row_trace_sample", []) or []:
        if isinstance(row, Mapping) and str(row.get("action")) == str(action):
            return dict(row)
    return {}


def _has_sequence_field(row: Mapping[str, Any]) -> bool:
    return any(k in row for k in SEQUENCE_FIELD_NAMES)


def _summarize_cross_action_memory(steps: Iterable[Mapping[str, Any]]) -> Tuple[int, List[Dict[str, Any]], Dict[str, int]]:
    total_groups = 0
    samples: List[Dict[str, Any]] = []
    by_family_mode: Counter[str] = Counter()
    for step in steps:
        groups: Dict[str, set[str]] = defaultdict(set)
        for row in step.get("row_trace_sample", []) or []:
            if not isinstance(row, Mapping):
                continue
            mid = row.get("continuation_memory_id")
            act = row.get("action")
            if mid is not None and act is not None:
                groups[str(mid)].add(str(act))
        for mid, acts in groups.items():
            if len(acts) > 1:
                total_groups += 1
                key = f"{step.get('family')}::{step.get('mode')}"
                by_family_mode[key] += 1
                if len(samples) < 12:
                    samples.append({
                        "family": step.get("family"),
                        "mode": step.get("mode"),
                        "variant": step.get("variant"),
                        "t": step.get("t"),
                        "continuation_memory_id": mid,
                        "actions": sorted(acts),
                    })
    return total_groups, samples, dict(by_family_mode)


def _action_transition_summary(steps: List[Mapping[str, Any]]) -> Dict[str, Any]:
    by_run: Dict[str, List[Mapping[str, Any]]] = defaultdict(list)
    for s in steps:
        if s.get("variant") == "full_current":
            by_run[str(s.get("run_id"))].append(s)
    transitions: Counter[str] = Counter()
    selected_memory_transitions: Counter[str] = Counter()
    examples: List[Dict[str, Any]] = []
    for run_id, rows in by_run.items():
        rows = sorted(rows, key=lambda x: int(x.get("t", 0)))
        for a, b in zip(rows, rows[1:]):
            aa, bb = str(a.get("action")), str(b.get("action"))
            transitions[f"{aa}->{bb}"] += 1
            ra, rb = _selected_row(a), _selected_row(b)
            ma, mb = ra.get("continuation_memory_id"), rb.get("continuation_memory_id")
            selected_memory_transitions[f"{ma}->{mb}"] += 1
            if aa != bb and len(examples) < 10:
                examples.append({
                    "run_id": run_id,
                    "family": a.get("family"),
                    "mode": a.get("mode"),
                    "t": a.get("t"),
                    "action_transition": f"{aa}->{bb}",
                    "memory_transition": f"{ma}->{mb}",
                    "branch_transition": f"{ra.get('branch_id')}->{rb.get('branch_id')}",
                })
    return {
        "top_action_transitions": dict(transitions.most_common(20)),
        "top_selected_memory_transitions": dict(selected_memory_transitions.most_common(20)),
        "action_change_examples": examples,
        "action_change_count": sum(v for k, v in transitions.items() if k.split("->")[0] != k.split("->")[1]),
    }


def main() -> Dict[str, Any]:
    os.environ["CO_STRICT_ERRORS"] = "1"
    steps = _load_steps()
    full = [s for s in steps if s.get("variant") == "full_current"]
    row_count = 0
    sequence_field_rows = 0
    sequence_active_rows = 0
    sequence_field_samples: List[Dict[str, Any]] = []
    for s in full:
        for row in s.get("row_trace_sample", []) or []:
            if isinstance(row, Mapping):
                row_count += 1
                if _has_sequence_field(row):
                    sequence_field_rows += 1
                    if row.get("sequence_composition_active"):
                        sequence_active_rows += 1
                    if len(sequence_field_samples) < 5:
                        sample = {k: row.get(k) for k in SEQUENCE_FIELD_NAMES if k in row}
                        sample["sequence_composition_active"] = bool(row.get("sequence_composition_active"))
                        sample["sequence_composition_support"] = row.get("sequence_composition_support")
                        sample["sequence_phase_transition"] = row.get("sequence_phase_transition")
                        sample["sequence_composition_basis"] = row.get("sequence_composition_basis")
                        sequence_field_samples.append(sample)
    cross_total, cross_samples, cross_by_fm = _summarize_cross_action_memory(full)
    transition_summary = _action_transition_summary(steps)
    maintenance_full = [s for s in full if s.get("family") == "maintenance_replacement" and s.get("mode") in {"middle", "renewal_like"}]
    maint_cross_total, maint_cross_samples, maint_cross_by = _summarize_cross_action_memory(maintenance_full)
    findings = [
        {
            "id": "SLC1_CROSS_ACTION_MEMORY_EXISTS",
            "severity": "low",
            "finding": "First-pass continuation memory can group multiple native action expressions by public burden-domain key.",
            "evidence": f"cross_action_memory_groups={cross_total}; maintenance_target_groups={maint_cross_total}",
            "next_action": "Preserve this as a substrate; do not mistake it for ordered sequence composition.",
        },
        {
            "id": "SLC2_SEQUENCE_COMPOSITION_FIRST_PASS_PRESENT",
            "severity": "medium" if sequence_field_rows > 0 else "high",
            "finding": "Explicit sequence-composition carriers are now visible in diagnostic row telemetry, but this remains first-pass and not proof of correct behavior.",
            "evidence": f"sequence_field_rows={sequence_field_rows} of row_trace_sample rows={row_count}; active_sequence_rows={sequence_active_rows}",
            "next_action": "Evaluate sequence-on/off behavior and remaining readout swamping; do not add family-specific sequence templates.",
        },
        {
            "id": "SLC3_MAINTENANCE_SEQUENCE_EFFECT_REMAINS_UNPROVEN",
            "severity": "medium",
            "finding": "Maintenance traces now expose generic sequence carriers, but whether they reduce real readout swamping or action-prefix insensitivity remains unproven.",
            "evidence": "See active_sequence_rows, maintenance_cross_action_memory_samples, and selected action/memory transition examples.",
            "next_action": "Rerun maintenance/readout-swamping diagnostics with sequence on/off; do not add maintenance-specific sequence templates.",
        },
    ]
    out = {
        "study": "sequence_level_continuation_composition_audit_v1",
        "claim_boundary": CLAIM_BOUNDARY,
        "full_current_steps": len(full),
        "row_trace_sample_rows": row_count,
        "sequence_field_rows": sequence_field_rows,
        "sequence_active_rows": sequence_active_rows,
        "sequence_field_samples": sequence_field_samples,
        "cross_action_memory_groups": cross_total,
        "cross_action_memory_by_family_mode": cross_by_fm,
        "cross_action_memory_samples": cross_samples,
        "maintenance_target_cross_action_memory_groups": maint_cross_total,
        "maintenance_cross_action_memory_by_mode": maint_cross_by,
        "maintenance_cross_action_memory_samples": maint_cross_samples,
        "transition_summary": transition_summary,
        "audit_findings": findings,
        "recommendation": "Sequence-composition now has a generic first-pass implementation. Freeze the rough kernel for diagnostic evaluation unless a later failure passes the necessity gate; do not add family-specific sequence templates.",
    }
    _write_json(OUT_JSON, out)
    _write_report(out)
    return out


def _write_report(data: Mapping[str, Any]) -> None:
    lines: List[str] = []
    lines.append("# Sequence-Level Continuation Composition Audit v1 — 2026-05-22")
    lines.append("")
    lines.append("## Claim boundary")
    lines.append("")
    lines.append(CLAIM_BOUNDARY)
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"Full-current diagnostic steps inspected: {data['full_current_steps']}.")
    lines.append(f"Row trace sample rows inspected: {data['row_trace_sample_rows']}.")
    lines.append(f"Rows with explicit sequence/composition fields: {data['sequence_field_rows']}.")
    lines.append(f"Rows with active sequence composition: {data['sequence_active_rows']}.")
    lines.append(f"Cross-action continuation-memory groups: {data['cross_action_memory_groups']}.")
    lines.append(f"Maintenance target cross-action groups: {data['maintenance_target_cross_action_memory_groups']}.")
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
    lines.append("## Cross-action memory examples")
    lines.append("")
    for s in data.get("cross_action_memory_samples", [])[:10]:
        lines.append(f"- `{s['family']}::{s['mode']}` t={s['t']} memory=`{s['continuation_memory_id']}` actions={s['actions']}")
    lines.append("")
    lines.append("## Selected action-change examples")
    lines.append("")
    for s in data.get("transition_summary", {}).get("action_change_examples", [])[:10]:
        lines.append(f"- `{s['family']}::{s['mode']}` t={s['t']} {s['action_transition']} memory `{s['memory_transition']}`")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("The current kernel has a useful first-pass substrate: public burden-domain memory can persist across different action expressions, and generic sequence-composition carriers are now visible. This is still only a first-pass mechanism: it does not prove that ordered continuation improves readout behavior or solves maintenance action-prefix insensitivity, and it should not be patched by naming maintenance actions.")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
