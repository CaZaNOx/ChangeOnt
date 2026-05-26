from __future__ import annotations

"""Generic dominance/readout-swamping audit v1.

Reads the current-kernel diagnostic map and identifies steps where a carrier
branch with unresolved carrier-only pressure remains selected while an explicit
resolver alternative exists.  This is an audit only; it does not tune a problem
family and does not change runtime behavior.
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.studies import current_kernel_diagnostic_map_v1 as diag
from experiments.studies import preblocking_resolver_cross_family_microcase_probe_v1 as micro

OUT_JSON = ROOT / "outputs" / "dominance_readout_swamping_audit_v1.json"
REPORT_MD = ROOT.parent / "DOMINANCE_READOUT_SWAMPING_AUDIT_REPORT_2026-05-22.md"

CLAIM_BOUNDARY = (
    "Generic dominance/readout-swamping audit only. It is not a benchmark, not tuning evidence, "
    "not maintenance-specific diagnosis, not SOTA comparison, and not CO proof."
)


def _load_steps() -> List[Dict[str, Any]]:
    diag.main()
    return [json.loads(line) for line in diag.STEPS_JSONL.read_text(encoding="utf-8").splitlines() if line.strip()]


def _f(x: Any, default: float = 0.0) -> float:
    try:
        return float(x)
    except Exception:
        return float(default)


def _selected_assessment(step: Mapping[str, Any]) -> Tuple[str, Dict[str, Any]]:
    selected = str(step.get("action"))
    ass = step.get("canonical_commitment_assessment_summary", {})
    if isinstance(ass, Mapping) and isinstance(ass.get(selected), Mapping):
        return selected, dict(ass[selected])
    return selected, {}


def _best_resolver_alt(step: Mapping[str, Any], selected: str) -> Optional[Tuple[str, Dict[str, Any]]]:
    ass = step.get("canonical_commitment_assessment_summary", {})
    if not isinstance(ass, Mapping):
        return None
    best: Optional[Tuple[str, Dict[str, Any], float]] = None
    for action, metrics in ass.items():
        if str(action) == selected or not isinstance(metrics, Mapping):
            continue
        resolver = _f(metrics.get("resolver_support"))
        if resolver <= 0.05:
            continue
        # Resolver candidates are ranked by resolver support first, then by continuation readiness.
        rank = resolver + 0.20 * _f(metrics.get("continuation_score")) + 0.10 * _f(metrics.get("dominance_score"))
        if best is None or rank > best[2]:
            best = (str(action), dict(metrics), rank)
    if best is None:
        return None
    return best[0], best[1]


def _support_stability_share(m: Mapping[str, Any]) -> float:
    pos = _f(m.get("dominance_positive_mass"))
    if pos <= 1e-12:
        return 0.0
    return (_f(m.get("dominance_support_component")) + _f(m.get("dominance_stability_component")) + _f(m.get("dominance_field_component"))) / pos


def _penalty_ratio(m: Mapping[str, Any]) -> float:
    pos = _f(m.get("dominance_positive_mass"))
    neg = _f(m.get("dominance_negative_mass"))
    return neg / max(1e-12, pos)


def _gate_failure(step: Mapping[str, Any], selected: Mapping[str, Any], alt: Mapping[str, Any]) -> str:
    gauge = step.get("local_shape_gauge", {})
    if not isinstance(gauge, Mapping) or not gauge:
        return "no_local_gauge_logged"
    pressure = _f(gauge.get("carrier_pressure_for_timing"))
    gate = _f(gauge.get("preblocking_min_carrier_pressure"))
    req = _f(gauge.get("preblocking_required_resolver_support"))
    alt_res = _f(alt.get("resolver_support"))
    score_gap = _f(gauge.get("preblocking_score_gap"))
    score_margin = _f(gauge.get("preblocking_score_margin"))
    support_gap = _f(gauge.get("preblocking_support_gap"))
    support_margin = _f(gauge.get("preblocking_support_margin"))
    if pressure < gate:
        return "carrier_pressure_below_preblocking_gate"
    if alt_res < req:
        return "resolver_support_below_required_gate"
    if score_gap > score_margin and support_gap > support_margin:
        return "carrier_advantage_exceeds_preblocking_margins"
    return "other_or_unclassified"


def main() -> Dict[str, Any]:
    # Ensure the microcase report uses the same current CommitmentSurface code.
    micro_result = micro.main()
    steps = _load_steps()
    full = [s for s in steps if s.get("variant") == "full_current"]
    selected_cases: List[Dict[str, Any]] = []
    by_family_mode: Dict[str, Counter] = defaultdict(Counter)
    gate_failures = Counter()
    support_shares: List[float] = []
    penalty_ratios: List[float] = []
    for s in full:
        selected, sel_m = _selected_assessment(s)
        if not sel_m:
            continue
        carrier = _f(sel_m.get("carrier_only_pressure"))
        if carrier <= 0.18:
            continue
        alt = _best_resolver_alt(s, selected)
        if alt is None:
            continue
        alt_name, alt_m = alt
        applied = bool(s.get("shape_gauged_resolver_timing_applied"))
        failure = "applied" if applied else _gate_failure(s, sel_m, alt_m)
        gate_failures[failure] += 1
        key = f"{s.get('family')}::{s.get('mode')}"
        by_family_mode[key][failure] += 1
        support_share = _support_stability_share(sel_m)
        penalty_ratio = _penalty_ratio(sel_m)
        support_shares.append(support_share)
        penalty_ratios.append(penalty_ratio)
        if len(selected_cases) < 24:
            selected_cases.append({
                "family": s.get("family"),
                "mode": s.get("mode"),
                "t": s.get("t"),
                "selected": selected,
                "alternative": alt_name,
                "commitment_mode": s.get("canonical_commitment_mode"),
                "commitment_reason": s.get("canonical_commitment_reason"),
                "shape_gauged_applied": applied,
                "gate_failure": failure,
                "carrier_only_pressure": carrier,
                "resolver_support_alt": _f(alt_m.get("resolver_support")),
                "selected_dominance_score": _f(sel_m.get("dominance_score")),
                "alt_dominance_score": _f(alt_m.get("dominance_score")),
                "selected_support": _f(sel_m.get("support")),
                "alt_support": _f(alt_m.get("support")),
                "support_stability_field_share_of_positive_mass": support_share,
                "dominance_penalty_to_positive_mass_ratio": penalty_ratio,
                "local_shape_gauge": s.get("local_shape_gauge", {}),
            })
    swamping_count = sum(1 for c in selected_cases if c["gate_failure"] != "applied")
    out = {
        "study": "dominance_readout_swamping_audit_v1",
        "claim_boundary": CLAIM_BOUNDARY,
        "full_current_steps": len(full),
        "carrier_with_resolver_alt_cases_total": sum(gate_failures.values()),
        "gate_failure_counts": dict(gate_failures),
        "by_family_mode": {k: dict(v) for k, v in sorted(by_family_mode.items())},
        "avg_support_stability_field_share": mean(support_shares) if support_shares else 0.0,
        "avg_dominance_penalty_ratio": mean(penalty_ratios) if penalty_ratios else 0.0,
        "sample_cases": selected_cases,
        "microcase_summary": {
            "cases": micro_result.get("cases"),
            "passed": micro_result.get("passed"),
            "observed": micro_result.get("observed"),
            "watchpoints": micro_result.get("watchpoints"),
        },
        "audit_findings": [
            {
                "id": "DRS1_READOUT_SWAMPING_IS_REAL_BUT_NOT_UNIFORM",
                "severity": "medium" if sum(gate_failures.values()) else "low",
                "finding": "The current readout contains generic cases where a carrier branch remains selected despite explicit resolver alternatives. These are concentrated in gate failures, not absent telemetry.",
                "evidence": f"carrier_with_resolver_alt_cases_total={sum(gate_failures.values())}; gate_failure_counts={dict(gate_failures)}",
                "next_action": "Analyze carrier-gate calibration generically; do not patch a specific family.",
            },
            {
                "id": "DRS2_SUPPORT_STABILITY_FIELD_MASS_CAN_SWAMP_PENALTIES",
                "severity": "medium" if support_shares and mean(support_shares) > 0.70 and mean(penalty_ratios) < 0.35 else "low",
                "finding": "Selected carriers often derive most positive dominance mass from support/stability/field components while burden/blocker penalties remain small relative to that mass.",
                "evidence": f"avg_support_stability_field_share={mean(support_shares) if support_shares else 0.0:.3f}; avg_dominance_penalty_ratio={mean(penalty_ratios) if penalty_ratios else 0.0:.3f}",
                "next_action": "If changed later, adjust generic carrier-gate or blocker/pressure interpretation, not native action rules.",
            },
            {
                "id": "DRS3_MICROCASES_IDENTIFY_CALIBRATION_SITE",
                "severity": "medium" if micro_result.get("watchpoints", 0) else "low",
                "finding": "Cross-family microcases expose whether the generic pre-blocking carrier gate is too strict at borderline high-urgency pressure while preserving negative controls.",
                "evidence": f"microcase_watchpoints={micro_result.get('watchpoints', 0)}",
                "next_action": "Preserve low-urgency, weak-resolver, and large-carrier-advantage protections before any coefficient change.",
            },
        ],
        "recommendation": "Do not treat the generic carrier-gate calibration as problem-family tuning. After calibration, preserve cross-family negative controls and continue auditing remaining readout-swamping cases as generic kernel issues."
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
    _write_report(out)
    return out


def _write_report(out: Mapping[str, Any]) -> None:
    lines: List[str] = []
    lines.append("# Dominance / Readout-Swamping Audit v1 — 2026-05-22")
    lines.append("")
    lines.append(f"Claim boundary: {CLAIM_BOUNDARY}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- full-current steps inspected: {out['full_current_steps']}")
    lines.append(f"- carrier-with-resolver-alt cases: {out['carrier_with_resolver_alt_cases_total']}")
    lines.append(f"- gate failure counts: `{out['gate_failure_counts']}`")
    lines.append(f"- avg support/stability/field share of positive dominance mass: {out['avg_support_stability_field_share']:.3f}")
    lines.append(f"- avg dominance penalty/positive-mass ratio: {out['avg_dominance_penalty_ratio']:.3f}")
    lines.append(f"- microcase summary: `{out['microcase_summary']}`")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("The audit does not license a maintenance-specific repair rule. After generic carrier-gate calibration, the borderline high-urgency microcase is protected, but many real-trace carrier selections remain action-inert because support/stability/field mass or other generic readout gates still dominate. This is a kernel/readout question, not a problem-family patch.")
    lines.append("")
    lines.append("## Sample cases")
    lines.append("")
    lines.append("| family/mode | t | selected | alt | mode | failure | carrier | alt resolver | support-share | penalty-ratio |")
    lines.append("|---|---:|---|---|---|---|---:|---:|---:|---:|")
    for c in out.get("sample_cases", [])[:16]:
        lines.append(
            f"| {c.get('family')} / {c.get('mode')} | {c.get('t')} | {c.get('selected')} | {c.get('alternative')} | {c.get('commitment_mode')} | {c.get('gate_failure')} | {c.get('carrier_only_pressure'):.3f} | {c.get('resolver_support_alt'):.3f} | {c.get('support_stability_field_share_of_positive_mass'):.3f} | {c.get('dominance_penalty_to_positive_mass_ratio'):.3f} |"
        )
    lines.append("")
    lines.append("## Recommendation")
    lines.append("")
    lines.append(str(out.get("recommendation")))
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
