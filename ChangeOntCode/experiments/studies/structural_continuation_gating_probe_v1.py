from __future__ import annotations

"""Continuation-gating microprobe v1.

This diagnostic follows ``structural_microcase_probe_v1`` and isolates the
remaining watchpoint found there:

    Can ``stable_continuation`` select a branch whose certificate blocks
    dominance while an unblocked alternative exists?

The probe is not a reward benchmark and does not prescribe a new runtime rule.
It sweeps controlled support gaps between a hiddenness-carrying blocked branch
and unblocked/exposure alternatives.  It records where current CommitmentSurface
permits stable continuation through an active blocker, and it reports a simple
counterfactual policy for review: choosing the best unblocked continuation when
one exists.  Any future behavior change must be justified separately in docs and
formula ledger before being made canonical.
"""

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence

from agents.co.tests.relation_path_trace_diagnostics import _run_candidate_commitment

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "structural_continuation_gating_probe_v1.json"

SUPPORT_VALUES = [0.48, 0.54, 0.58, 0.60, 0.62, 0.66, 0.70, 0.72, 0.76, 0.82, 0.90]


def _effect(
    operation: str,
    burden_type: str = "hiddenness",
    *,
    kind: str = "hiddenness",
    magnitude: float = 0.90,
    relation_scope: str = "hidden",
) -> Dict[str, Any]:
    return {
        "operation": operation,
        "kind": kind,
        "burden_type": burden_type,
        "scope": "candidate",
        "magnitude": float(magnitude),
        "relation_scope": relation_scope,
        "public_basis": "visible_observation",
        "leakage_status": "public",
    }


def _candidate(
    candidate_id: str,
    visible: float,
    *,
    uncertainty: float = 0.20,
    coverage: float = 0.70,
    tested: float = 0.60,
    reversibility: float = 0.70,
    effects: Sequence[Mapping[str, Any]] = (),
) -> Dict[str, Any]:
    return {
        "candidate_id": candidate_id,
        "legal": True,
        "visible_delta": float(visible),
        "line_support": float(visible),
        "coverage_adequacy": float(coverage),
        "tested_hint": float(tested),
        "uncertainty_hint": float(uncertainty),
        "reversibility_hint": float(reversibility),
        "public_effects": [dict(e) for e in effects],
    }


def _assessment(commit: Mapping[str, Any]) -> Dict[str, Dict[str, float]]:
    raw = commit.get("canonical_commitment_assessment", {})
    out: Dict[str, Dict[str, float]] = {}
    if not isinstance(raw, Mapping):
        return out
    keys = (
        "support",
        "dominance_score",
        "sampling_score",
        "continuation_score",
        "collapse_certificate_blocker_pressure",
        "collapse_certificate_recursion_demand",
        "certificate_gate_open",
        "certificate_blocks_dominance",
        "collapse_blocked",
    )
    for action, rec in raw.items():
        if not isinstance(rec, Mapping):
            continue
        out[str(action)] = {}
        for k in keys:
            try:
                out[str(action)][k] = round(float(rec.get(k, 0.0)), 6)
            except Exception:
                out[str(action)][k] = 0.0
    return out


def _rows_by_action(rows: Iterable[Mapping[str, Any]]) -> Dict[str, Mapping[str, Any]]:
    return {str(r.get("action")): r for r in rows if r.get("action") is not None}


def _is_blocked(action: str, rows: Sequence[Mapping[str, Any]], commit: Mapping[str, Any]) -> bool:
    by_action = _rows_by_action(rows)
    row = by_action.get(action, {})
    ass = _assessment(commit).get(action, {})
    return bool(row.get("collapse_blockers")) or float(ass.get("certificate_blocks_dominance", 0.0) or 0.0) >= 0.5


def _best_unblocked_by_continuation(rows: Sequence[Mapping[str, Any]], commit: Mapping[str, Any]) -> str | None:
    ass = _assessment(commit)
    actions = list(ass.keys())
    unblocked = [a for a in actions if not _is_blocked(a, rows, commit)]
    if not unblocked:
        return None
    return max(unblocked, key=lambda a: ass[a].get("continuation_score", 0.0))


def _relation_summary(rows: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    if not rows:
        return {}
    tel = rows[0].get("relation_surface_telemetry", {})
    if not isinstance(tel, Mapping):
        return {}
    return {
        "relations_total": int(tel.get("relations_total", 0) or 0),
        "relations_by_type": dict(tel.get("relations_by_type", {}) or {}),
        "branch_internal_operation_rows": int(tel.get("branch_internal_operation_rows", 0) or 0),
    }


def _run_scenario(name: str, candidates: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    rows, commit = _run_candidate_commitment([dict(c) for c in candidates], f"continuation_gating:{name}")
    selected = str(commit.get("action"))
    assessment = _assessment(commit)
    counterfactual = _best_unblocked_by_continuation(rows, commit)
    selected_blocked_stable = bool(
        selected
        and commit.get("canonical_commitment_mode") == "stable_continuation"
        and _is_blocked(selected, rows, commit)
        and counterfactual is not None
        and counterfactual != selected
    )
    assessment = _assessment(commit)
    selected_continuation_gap = None
    selected_support_gap = None
    comparable_unblocked_available = False
    if selected_blocked_stable and selected in assessment and counterfactual in assessment:
        selected_continuation_gap = round(
            float(assessment[selected].get("continuation_score", 0.0))
            - float(assessment[counterfactual].get("continuation_score", 0.0)),
            6,
        )
        selected_support_gap = round(
            float(assessment[selected].get("support", 0.0))
            - float(assessment[counterfactual].get("support", 0.0)),
            6,
        )
        comparable_unblocked_available = bool(
            selected_continuation_gap <= float(commit.get("continuation_gate_margin", 0.0) or 0.0)
            and selected_support_gap <= float(commit.get("support_advantage_limit", 0.0) or 0.0)
        )
    by_action = _rows_by_action(rows)
    return {
        "scenario": name,
        "selected_action": selected,
        "selected_mode": commit.get("canonical_commitment_mode"),
        "selected_reason": commit.get("canonical_commitment_reason"),
        "selected_is_certificate_blocked": _is_blocked(selected, rows, commit) if selected else False,
        "best_unblocked_continuation_counterfactual": counterfactual,
        "selected_blocked_stable_with_unblocked_alternative": selected_blocked_stable,
        "selected_blocked_stable_with_comparable_unblocked_alternative": bool(selected_blocked_stable and comparable_unblocked_available),
        "certificate_aware_stable_continuation_applied": bool(commit.get("certificate_aware_stable_continuation_applied", False)),
        "certificate_aware_stable_continuation_alternative": commit.get("certificate_aware_stable_continuation_alternative"),
        "continuation_gate_margin": commit.get("continuation_gate_margin"),
        "support_advantage_limit": commit.get("support_advantage_limit"),
        "selected_continuation_gap_to_unblocked": selected_continuation_gap,
        "selected_support_gap_to_unblocked": selected_support_gap,
        "assessment": assessment,
        "relation_summary": _relation_summary(rows),
        "rows": [
            {
                "action": r.get("action"),
                "collapse_blockers": list(r.get("collapse_blockers", []) or []),
                "collapse_certificate_status": r.get("collapse_certificate_status"),
                "collapse_certificate_reason_flags": list(r.get("collapse_certificate_reason_flags", []) or []),
                "branch_internal_operation_counts": dict(r.get("branch_internal_operation_counts", {}) or {}),
                "branch_internal_hiddenness_pressure": r.get("branch_internal_hiddenness_pressure"),
                "branch_internal_exposure_support": r.get("branch_internal_exposure_support"),
                "field_debt": r.get("field_debt"),
                "field_viability": r.get("field_viability"),
                "field_recursion_budget": r.get("field_recursion_budget"),
                "field_collapse_readiness": r.get("field_collapse_readiness"),
            }
            for r in rows
        ],
        "current_vs_counterfactual_differs": bool(counterfactual and counterfactual != selected),
    }


def _gap_scenarios() -> List[Dict[str, Any]]:
    scenarios: List[Dict[str, Any]] = []
    neutral_visible = 0.62
    for visible in SUPPORT_VALUES:
        gap = round(visible - neutral_visible, 3)
        scenarios.append(_run_scenario(
            f"blocked_hidden_vs_neutral_gap_{gap:+.2f}",
            [
                _candidate("continue_hidden", visible, effects=[_effect("carry")]),
                _candidate("neutral_probe", neutral_visible),
            ],
        ))
    # Resolver alternative: exposure can do relevant work, but local evidence is
    # lower.  This checks whether hiddenness support beats a structurally apt
    # branch before dominance is earned.
    for exposure_visible in [0.52, 0.56, 0.60, 0.64, 0.68]:
        scenarios.append(_run_scenario(
            f"blocked_hidden_0.72_vs_exposure_{exposure_visible:.2f}",
            [
                _candidate("continue_hidden", 0.72, effects=[_effect("carry")]),
                _candidate("inspect_exposes", exposure_visible, effects=[_effect("expose")]),
            ],
        ))
    # Overwhelming-support control: certificate-aware stable continuation is not
    # a hard veto.  A blocked branch may continue under unresolved burden if the
    # best unblocked alternative is far outside the comparable band.
    scenarios.append(_run_scenario(
        "overwhelming_support_continues_under_burden_control",
        [
            _candidate("continue_hidden", 0.98, effects=[_effect("carry")]),
            _candidate("weak_neutral_probe", 0.20),
        ],
    ))
    # No unblocked alternative control: the runtime may need to continue through
    # a blocker when every available branch is blocked in some relevant way.
    scenarios.append(_run_scenario(
        "all_branches_blocked_no_unblocked_counterfactual",
        [
            _candidate("continue_hidden", 0.70, effects=[_effect("carry")]),
            _candidate("mask_hidden", 0.62, effects=[_effect("mask")]),
        ],
    ))
    return scenarios


def _summarize(scenarios: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    blocked_stable = [s for s in scenarios if s.get("selected_blocked_stable_with_unblocked_alternative")]
    blocked_stable_comparable = [s for s in scenarios if s.get("selected_blocked_stable_with_comparable_unblocked_alternative")]
    certificate_aware_switches = [s for s in scenarios if s.get("certificate_aware_stable_continuation_applied")]
    counterfactual_diffs = [s for s in scenarios if s.get("current_vs_counterfactual_differs")]
    support_band = []
    for s in blocked_stable:
        ass = s.get("assessment", {}) if isinstance(s.get("assessment"), Mapping) else {}
        selected = str(s.get("selected_action"))
        alt = s.get("best_unblocked_continuation_counterfactual")
        if isinstance(alt, str) and selected in ass and alt in ass:
            support_band.append({
                "scenario": s.get("scenario"),
                "selected": selected,
                "alt": alt,
                "support_gap": round(float(ass[selected].get("support", 0.0)) - float(ass[alt].get("support", 0.0)), 6),
                "continuation_gap": round(float(ass[selected].get("continuation_score", 0.0)) - float(ass[alt].get("continuation_score", 0.0)), 6),
                "dominance_gap": round(float(ass[selected].get("dominance_score", 0.0)) - float(ass[alt].get("dominance_score", 0.0)), 6),
            })
    return {
        "scenarios": len(scenarios),
        "selected_blocked_stable_with_unblocked_alternative": len(blocked_stable),
        "selected_blocked_stable_with_comparable_unblocked_alternative": len(blocked_stable_comparable),
        "certificate_aware_stable_continuation_switches": len(certificate_aware_switches),
        "current_vs_best_unblocked_counterfactual_differs": len(counterfactual_diffs),
        "blocked_stable_gap_records": support_band,
        "interpretation": {
            "current_rule": "certificate-aware stable continuation prefers comparable unblocked alternatives but allows overwhelming blocked continuations under unresolved burden",
            "probe_question": "whether comparable blocked continuations are redirected while non-comparable controls remain permissive",
            "claim_boundary": "diagnostic only; no reward evidence and no empirical success claim",
        },
    }


def main() -> Dict[str, Any]:
    scenarios = _gap_scenarios()
    result = {
        "study": "structural_continuation_gating_probe_v1",
        "claim_boundary": "synthetic support-gap probe only; not benchmark evidence and not a canonical behavior change",
        "aggregate": _summarize(scenarios),
        "scenarios": scenarios,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"aggregate": result["aggregate"], "output": str(OUT.relative_to(ROOT))}, indent=2, sort_keys=True))
    return result


if __name__ == "__main__":
    main()
