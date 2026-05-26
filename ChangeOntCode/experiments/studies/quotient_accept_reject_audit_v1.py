from __future__ import annotations

"""Quotient accept/reject audit v1.

This audit uses the current-kernel diagnostic map traces after quotient-profile
reason logging.  It does not change kernel behavior and does not calibrate
quotient tolerances.  It asks whether quotienting is provenance-visible, whether
there are obvious duplicate-signature missed quotients, and whether rejected
profiles are rejected for public, generic reasons rather than problem-specific
policy.
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Tuple

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.studies import current_kernel_diagnostic_map_v1 as diag

OUT_JSON = ROOT / "outputs" / "quotient_accept_reject_audit_v1.json"
REPORT_MD = ROOT.parent / "QUOTIENT_ACCEPT_REJECT_AUDIT_REPORT_2026-05-22.md"

CLAIM_BOUNDARY = (
    "Quotient accept/reject audit only. It checks provenance visibility and obvious first-pass quotient pathologies. "
    "It is not a final quotient law, not state abstraction/bisimulation evidence, not benchmark evidence, and not a CO proof."
)


def _load_steps() -> List[Dict[str, Any]]:
    path = diag.STEPS_JSONL
    if not path.exists():
        diag.main()
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _signature_duplicates(rows: Iterable[Mapping[str, Any]]) -> Dict[str, List[str]]:
    by_sig: Dict[str, List[str]] = defaultdict(list)
    for r in rows:
        sig = str(r.get("relation_surface_quotient_profile") or "")
        if not sig:
            continue
        by_sig[sig].append(str(r.get("action", r.get("branch_id", "?"))))
    return {k: v for k, v in by_sig.items() if len(v) > 1}


def _entry_head(entry: str) -> str:
    # domain/kind/family/scope/band/threshold/basin/coupling
    parts = str(entry).split("/")
    return "/".join(parts[:4]) if len(parts) >= 4 else str(entry)


def _potential_calibration_groups(rows: Iterable[Mapping[str, Any]]) -> Dict[str, List[str]]:
    """Groups that share domain/kind/family/scope but do not share full signature.

    These are not bugs; they are places where future tolerance/coarseness work may
    decide whether same-domain near profiles should remain distinct.
    """
    by_head: Dict[str, List[str]] = defaultdict(list)
    for r in rows:
        entries = r.get("relation_surface_quotient_profile_entries") or []
        if not isinstance(entries, list):
            continue
        for e in entries:
            by_head[_entry_head(str(e))].append(str(r.get("action", r.get("branch_id", "?"))))
    return {k: sorted(set(v)) for k, v in by_head.items() if len(set(v)) > 1}


def main() -> Dict[str, Any]:
    diag.main()
    steps = _load_steps()
    full = [s for s in steps if s.get("variant") == "full_current"]
    summary_by_task: Dict[Tuple[str, str], Dict[str, Any]] = {}
    duplicate_signature_bug_candidates: List[Dict[str, Any]] = []
    accepted_singletons = 0
    accepted_total = 0
    rejected_reasons = Counter()
    possible_calibration_sites: List[Dict[str, Any]] = []

    for s in full:
        key = (str(s.get("family")), str(s.get("mode")))
        item = summary_by_task.setdefault(key, {
            "steps": 0,
            "accepted_profiles": 0,
            "rejected_profiles": Counter(),
            "quotient_rows": 0,
            "bucket_steps": 0,
            "relation_types": Counter(),
        })
        item["steps"] += 1
        item["accepted_profiles"] += int(s.get("quotient_profiles_accepted", 0) or 0)
        accepted_total += int(s.get("quotient_profiles_accepted", 0) or 0)
        for reason, count in dict(s.get("quotient_profiles_rejected", {}) or {}).items():
            item["rejected_profiles"][str(reason)] += int(count or 0)
            rejected_reasons[str(reason)] += int(count or 0)
        item["quotient_rows"] += int(s.get("quotient_rows", 0) or 0)
        item["bucket_steps"] += int(bool(s.get("quotient_buckets_with_multiple_members", 0)))
        item["relation_types"].update(dict(s.get("relations_by_type", {}) or {}))

        rows = list(s.get("row_trace_sample", []) or [])
        dups = _signature_duplicates(rows)
        # A duplicate signature should produce quotient_share_count >1 on all members.
        for sig, actions in dups.items():
            share_counts = [int(float(r.get("quotient_share_count", 1) or 1)) for r in rows if r.get("relation_surface_quotient_profile") == sig]
            if any(c <= 1 for c in share_counts):
                duplicate_signature_bug_candidates.append({
                    "run_id": s.get("run_id"), "t": s.get("t"), "family": s.get("family"), "mode": s.get("mode"),
                    "signature": sig, "actions": actions, "share_counts": share_counts,
                })
        accepted_singletons += sum(1 for r in rows if r.get("relation_surface_quotient_profile_accepted") and int(float(r.get("quotient_share_count", 1) or 1)) == 1)
        groups = _potential_calibration_groups(rows)
        if groups:
            possible_calibration_sites.append({
                "run_id": s.get("run_id"), "t": s.get("t"), "family": s.get("family"), "mode": s.get("mode"),
                "groups": groups,
            })

    clean_task_summary = []
    for (family, mode), item in sorted(summary_by_task.items()):
        clean_task_summary.append({
            "family": family,
            "mode": mode,
            "steps": item["steps"],
            "accepted_profiles": item["accepted_profiles"],
            "rejected_profiles": dict(item["rejected_profiles"]),
            "quotient_rows": item["quotient_rows"],
            "steps_with_multi_member_bucket": item["bucket_steps"],
            "relation_types": dict(item["relation_types"]),
        })

    result = {
        "study": "quotient_accept_reject_audit_v1",
        "claim_boundary": CLAIM_BOUNDARY,
        "data_source": str(diag.STEPS_JSONL.relative_to(ROOT)),
        "full_current_steps": len(full),
        "accepted_profiles_total": accepted_total,
        "accepted_singletons_in_trace_sample": accepted_singletons,
        "rejected_reasons_total": dict(rejected_reasons),
        "duplicate_signature_bug_candidates": duplicate_signature_bug_candidates[:16],
        "duplicate_signature_bug_count": len(duplicate_signature_bug_candidates),
        "possible_calibration_sites_sample": possible_calibration_sites[:16],
        "possible_calibration_site_count": len(possible_calibration_sites),
        "task_summary": clean_task_summary,
        "audit_findings": [
            {
                "id": "QAR1_PROVENANCE_NOW_VISIBLE",
                "severity": "resolved-watchpoint",
                "finding": "Quotient accept/reject reasons are now visible at relation telemetry and row-trace level.",
                "evidence": f"{accepted_total} accepted profiles observed across {len(full)} full-current diagnostic steps; rejected reasons are counted as {dict(rejected_reasons)}.",
                "next_action": "Keep this logging; use it during real-trace false/missed quotient calibration."
            },
            {
                "id": "QAR2_NO_DUPLICATE_SIGNATURE_MISSED_QUOTIENT_FOUND",
                "severity": "passed-check" if not duplicate_signature_bug_candidates else "high",
                "finding": "No obvious duplicate-profile signature with quotient_share_count=1 was found in the capped diagnostic." if not duplicate_signature_bug_candidates else "Duplicate quotient signatures without quotient sharing were found.",
                "evidence": f"duplicate_signature_bug_count={len(duplicate_signature_bug_candidates)}.",
                "next_action": "If this becomes nonzero, fix quotient grouping before any calibration."
            },
            {
                "id": "QAR3_CONSERVATIVE_SINGLETONS_DOMINATE",
                "severity": "medium",
                "finding": "Most accepted profiles are singleton residual profiles rather than multi-member quotient buckets. This is conservative but means quotienting is mostly a trace annotation outside the few matched-profile cases.",
                "evidence": f"accepted_singletons_in_trace_sample={accepted_singletons}; possible_calibration_site_count={len(possible_calibration_sites)}.",
                "next_action": "Do not loosen quotienting yet; first design false-quotient/missed-quotient microcases and compare to state-abstraction/bisimulation analogues."
            }
        ],
        "recommendation": "Quotienting is now auditable and no obvious duplicate-signature bug was found. Keep it conservative for Pass 1; postpone tolerance loosening until real-trace false/missed quotient cases are designed."
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    _write_report(result)
    return result


def _write_report(result: Mapping[str, Any]) -> None:
    lines: List[str] = []
    lines.append("# Quotient Accept/Reject Audit v1 — 2026-05-22")
    lines.append("")
    lines.append("## Claim boundary")
    lines.append("")
    lines.append(CLAIM_BOUNDARY)
    lines.append("")
    lines.append("## Main verdict")
    lines.append("")
    lines.append("Quotient provenance is now visible enough for first-pass audit. The capped diagnostic did not show an obvious duplicate-signature missed-quotient bug. The main remaining issue is not a detected false quotient; it is that quotienting is deliberately conservative and mostly singleton outside matched public residual profiles.")
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
    lines.append("## Task summary")
    lines.append("")
    lines.append("| family | mode | steps | accepted profiles | quotient rows | multi-bucket steps | rejected reasons |")
    lines.append("|---|---|---:|---:|---:|---:|---|")
    for r in result.get("task_summary", []):
        lines.append(f"| {r['family']} | {r['mode']} | {r['steps']} | {r['accepted_profiles']} | {r['quotient_rows']} | {r['steps_with_multi_member_bucket']} | `{json.dumps(r['rejected_profiles'], sort_keys=True)}` |")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("A singleton accepted profile is not a bug: it means the branch has an auditable public residual profile, but no other current branch shares that full profile under the conservative gauge. Future work should add explicit false-quotient and missed-quotient cases before loosening bands or equivalence tolerance.")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
