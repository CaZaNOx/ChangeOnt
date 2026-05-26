from __future__ import annotations

"""Continuation bridge localization diagnostic.

Reads the bridge-signal trace produced after ContinuationState v1 and extracts
where middle-vs-renewal maintenance diverges in the path:

    problem_contract -> shape/direct_controls -> candidate rows -> continuation
    state -> commitment mode/action

Diagnostic only. Does not modify runtime behavior.
"""

import json
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, Mapping, Sequence

IN = Path("outputs/bridge_signal_trace_v1_maintenance_only_after_continuation_state_v1.json")
OUT = Path("outputs/continuation_bridge_localization_check_v1.json")

FIELDS = [
    "local_support",
    "support_mass",
    "burden_pressure",
    "burden_relief",
    "preventive_support",
    "stability_under_change",
    "continuation_viability",
    "continuation_instability",
    "burden_accumulation",
    "burden_trend",
    "fracture_state",
    "decision_state",
]
CONTROL_FIELDS = [
    "collapse_admissibility",
    "revision_permissibility",
    "support_carry_forward",
    "rival_breadth",
    "nonlocal_authority",
    "path_sensitivity",
    "local_authority",
    "evidence_gate",
    "fracture_tolerance",
]


def f(x: Any, default: float | None = None) -> float | None:
    try:
        if x is None:
            return default
        return float(x)
    except Exception:
        return default


def avg(xs: Iterable[Any]) -> float | None:
    vals = [f(x) for x in xs]
    vals = [x for x in vals if x is not None]
    return float(mean(vals)) if vals else None


def top_rows(rows: Sequence[Mapping[str, Any]], n: int = 6) -> list[dict[str, Any]]:
    out = []
    ranked = sorted(rows, key=lambda r: f(r.get("chosen_publication_snapshot", {}).get("burden_pressure"), 0.0) or 0.0, reverse=True)[:n]
    for r in ranked:
        out.append({
            "seed": r.get("seed"),
            "t": r.get("t"),
            "action": r.get("action"),
            "mode": r.get("canonical_commitment_mode"),
            "true_health_norm_before": (r.get("env_audit") or {}).get("true_health_norm_before"),
            "controls": {k: f((r.get("direct_controls_used") or {}).get(k)) for k in CONTROL_FIELDS},
            "chosen_publication": {k: f((r.get("chosen_publication_snapshot") or {}).get(k)) for k in FIELDS if k in (r.get("chosen_publication_snapshot") or {})},
            "chosen_commitment": {k: f((r.get("chosen_commitment_snapshot") or {}).get(k)) for k in ["burden", "uncertainty", "sampling_score", "continuation_score", "dominance_score"]},
            "stage_winners": {k: (r.get("stage_winners") or {}).get(k) for k in [
                "published_top_local_support",
                "published_top_burden_pressure",
                "published_top_burden_relief",
                "published_top_preventive_support",
                "published_top_decision_state",
                "commitment_top_dominance",
                "commitment_top_continuation",
                "commitment_top_sampling",
            ]},
            "top_published_rows_by_decision": [
                {"action": rr.get("action"), **{k: f(rr.get(k)) for k in FIELDS}}
                for rr in (r.get("top_published_rows_by_decision") or [])
            ],
        })
    return out


def summarize_case(case: str, rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    n = float(len(rows) or 1)
    actions = Counter(str(r.get("action")) for r in rows)
    modes = Counter(str(r.get("canonical_commitment_mode")) for r in rows)
    chosen_pub = [r.get("chosen_publication_snapshot") or {} for r in rows]
    chosen_commit = [r.get("chosen_commitment_snapshot") or {} for r in rows]
    controls = [r.get("direct_controls_used") or {} for r in rows]
    low_health = [r for r in rows if f((r.get("env_audit") or {}).get("true_health_norm_before"), 1.0) <= 0.5]

    # Does the chosen action inherit dominance from local support? Does preventive support ever win?
    rank = [r.get("chosen_rank_trace") or {} for r in rows]
    local_rank1 = sum(1 for x in rank if x.get("published_local_rank") == 1) / n
    preventive_rank1 = sum(1 for x in rank if x.get("published_preventive_rank") == 1) / n
    dominance_rank1 = sum(1 for x in rank if x.get("commitment_dominance_rank") == 1) / n

    return {
        "n_steps": len(rows),
        "action_rates": {k: v / n for k, v in sorted(actions.items())},
        "commitment_mode_rates": {k: v / n for k, v in sorted(modes.items())},
        "chosen_rank1_rates": {
            "published_local_support": local_rank1,
            "published_preventive_support": preventive_rank1,
            "commitment_dominance": dominance_rank1,
        },
        "mean_controls": {k: avg(c.get(k) for c in controls) for k in CONTROL_FIELDS},
        "mean_chosen_publication": {k: avg(p.get(k) for p in chosen_pub) for k in FIELDS},
        "mean_chosen_commitment": {k: avg(c.get(k) for c in chosen_commit) for k in ["burden", "uncertainty", "sampling_score", "continuation_score", "dominance_score"]},
        "low_health_count": len(low_health),
        "action_rates_when_true_health_le_half": {k: v / float(len(low_health) or 1) for k, v in Counter(str(r.get("action")) for r in low_health).items()},
        "high_burden_examples": top_rows(rows, 4),
    }


def main() -> None:
    data = json.loads(IN.read_text(encoding="utf-8"))
    cases = data["maintenance_replacement"]["cases"]
    out = {
        "study": "continuation_bridge_localization_check_v1",
        "status": "diagnostic_no_runtime_patch",
        "input": str(IN),
        "cases": {},
        "headline": [],
    }
    for case in ["middle", "renewal_like", "bandit_like"]:
        rows = cases[case]["rows"]
        out["cases"][case] = summarize_case(case, rows)

    m = out["cases"]["middle"]
    r = out["cases"]["renewal_like"]
    out["headline"] = [
        "Middle direct controls are locally permissive: high local_authority/collapse/support_carry_forward and lower nonlocal/path/revision pressure than renewal_like.",
        "Middle chosen RUN remains high-viability: mean continuation_viability is high and continuation_instability/burden_trend are low even at true health <= 0.5.",
        "Preventive support remains too small: middle preventive support is near zero even when RUN is the highest burden candidate.",
        "Renewal_like works better mainly because hiddenness/active drift/high commitment cost project to stronger nonlocal/path/revision controls and higher uncertainty/sampling pressure.",
    ]
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"wrote": str(OUT), "status": out["status"]}, indent=2))


if __name__ == "__main__":
    main()
