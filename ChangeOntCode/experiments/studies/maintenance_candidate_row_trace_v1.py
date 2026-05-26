from __future__ import annotations

"""Trace candidate publication rows for maintenance/replacement.

Diagnostic purpose: compare the middle and renewal-like maintenance regimes after
canonical CandidateSurface/CommitmentSurface rewrites.  This study records the
public observation, raw adapter candidates, CandidateSurface publication rows,
and CommitmentSurface assessments at every step.

This is an audit/study script, not runtime logic.  It may record true health for
post-hoc diagnosis, but that value is never fed to the CO adapter.
"""

import argparse
import json
import math
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

from environments.maintenance_replacement.env import ACTIONS, MaintenanceReplacementEnv
from experiments.runners.maintenance_replacement_runner import build_agent, spec_from_name

DEFAULT_REGIMES: Tuple[str, ...] = ("middle", "renewal_like")
DEFAULT_SEEDS: Tuple[int, ...] = tuple(range(10))


def _f(x: Any, default: Optional[float] = None) -> Optional[float]:
    try:
        if x is None:
            return default
        v = float(x)
        if math.isnan(v) or math.isinf(v):
            return default
        return v
    except Exception:
        return default


def _safe_mean(xs: Iterable[Any]) -> Optional[float]:
    vals = [_f(x) for x in xs]
    vals = [v for v in vals if v is not None]
    return float(mean(vals)) if vals else None


def _summarize_action_rates(rows: Sequence[Mapping[str, Any]]) -> Dict[str, float]:
    n = float(len(rows) or 1)
    c = Counter(str(r.get("action")) for r in rows)
    return {a: float(c.get(a, 0)) / n for a in ACTIONS}


def _row_by_action(rows: Sequence[Mapping[str, Any]]) -> Dict[str, Mapping[str, Any]]:
    return {str(r.get("action")): r for r in rows if r.get("action") is not None}


def _assessment_by_action(assessment: Mapping[str, Any]) -> Dict[str, Mapping[str, Any]]:
    return {str(k): v for k, v in (assessment or {}).items() if isinstance(v, Mapping)}


def _pick_best_nonrun(row_by_action: Mapping[str, Mapping[str, Any]], field: str) -> Tuple[Optional[str], Optional[float]]:
    best_a: Optional[str] = None
    best_v: Optional[float] = None
    for a, row in row_by_action.items():
        if a == "RUN":
            continue
        v = _f(row.get(field))
        if v is None:
            continue
        if best_v is None or v > best_v:
            best_a, best_v = a, v
    return best_a, best_v


def _trace_episode(regime: str, seed: int, max_steps: Optional[int] = None) -> Dict[str, Any]:
    spec = spec_from_name(regime, int(seed))
    env = MaintenanceReplacementEnv(spec)
    obs, _, done, info = env.reset(seed=int(seed))
    agent = build_agent("co", int(seed), spec=spec)

    rows: List[Dict[str, Any]] = []
    total_reward = 0.0
    step_cap = int(max_steps) if max_steps is not None else int(spec.horizon)

    while not done and len(rows) < step_cap:
        # True health is post-hoc audit-only.  It is not provided to the adapter.
        true_health_before = int(getattr(env, "health", info.get("health_true", -1)))
        sel = dict(agent.select(obs) or {})
        action = str(sel.get("action", "RUN"))
        if action not in ACTIONS:
            action = "RUN"

        prims = getattr(getattr(agent, "core", None), "primitives", {}) or {}
        packet = dict(getattr(agent, "_last_obs", {}) or {})
        published_rows = [dict(r) for r in prims.get("__candidate_publication_rows__", []) if isinstance(r, dict)]
        raw_candidates = [dict(c) for c in packet.get("candidates", []) if isinstance(c, dict)]
        assessments = _assessment_by_action(sel.get("canonical_commitment_assessment", {}) or {})
        row_map = _row_by_action(published_rows)
        run_row = dict(row_map.get("RUN", {}) or {})
        best_nonrun_decision = _pick_best_nonrun(row_map, "decision_state")
        best_nonrun_preventive = _pick_best_nonrun(row_map, "preventive_support")
        best_nonrun_burden_relief = _pick_best_nonrun(row_map, "burden_relief")
        run_assessment = dict(assessments.get("RUN", {}) or {})
        best_nonrun_dom: Tuple[Optional[str], Optional[float]] = (None, None)
        for a, ass in assessments.items():
            if a == "RUN":
                continue
            v = _f(ass.get("dominance_score"))
            if v is not None and (best_nonrun_dom[1] is None or v > best_nonrun_dom[1]):
                best_nonrun_dom = (a, v)

        next_obs, reward, done, info = env.step(action)
        total_reward += float(reward)
        fb = {"action": action, "reward": float(reward), "done": bool(done), "info": dict(info)}
        if hasattr(agent, "update"):
            agent.update(fb)

        obs_health_norm = _f(obs.get("observed_health_norm"))
        true_norm_before = true_health_before / float(max(1, int(spec.max_health)))
        row = {
            "regime": regime,
            "seed": int(seed),
            "t": int(obs.get("t", 0) or 0),
            "action": action,
            "reward": float(reward),
            "event_after_action": str(info.get("last_event", "")),
            "true_health_before": int(true_health_before),
            "true_health_norm_before": float(true_norm_before),
            "true_health_after": int(info.get("health_true", -1)),
            "observed_health_norm": obs_health_norm,
            "health_observed": bool(obs.get("health_observed", False)),
            "observed_health_age": obs.get("observed_health_age"),
            "observed_health_fresh": bool(obs.get("observed_health_fresh", False)),
            "observation_mode": str(spec.observe_health),
            "degradation_prob": float(spec.degradation_prob),
            "failure_penalty": float(spec.failure_penalty),
            "repair_cost": float(spec.repair_cost),
            "replace_cost": float(spec.replace_cost),
            "shape_axes": dict((packet.get("shape_prior6") or {}).get("axes", {}) or {}),
            "direct_controls_used": dict(sel.get("direct_controls_used", {}) or {}),
            "canonical_commitment_mode": str(sel.get("canonical_commitment_mode", "")),
            "canonical_commitment_reason": str(sel.get("canonical_commitment_reason", "")),
            "dominance_margin": _f(sel.get("dominance_margin")),
            "unresolved_pressure": _f(sel.get("unresolved_pressure")),
            "candidate_publication_rows": published_rows,
            "raw_candidates": raw_candidates,
            "canonical_commitment_assessment": {str(k): dict(v) for k, v in assessments.items()},
            "candidate_final_scores": dict(sel.get("candidate_final_scores", {}) or {}),
            "candidate_obs_scores": dict(sel.get("candidate_obs_scores", {}) or {}),
            "run_snapshot": {
                "local_support": _f(run_row.get("local_support")),
                "burden_pressure": _f(run_row.get("burden_pressure")),
                "burden_relief": _f(run_row.get("burden_relief")),
                "preventive_support": _f(run_row.get("preventive_support")),
                "fracture_state": _f(run_row.get("fracture_state")),
                "decision_state": _f(run_row.get("decision_state")),
                "dominance_score": _f(run_assessment.get("dominance_score")),
                "continuation_score": _f(run_assessment.get("continuation_score")),
                "sampling_score": _f(run_assessment.get("sampling_score")),
            },
            "best_nonrun": {
                "by_decision_state": {"action": best_nonrun_decision[0], "value": best_nonrun_decision[1]},
                "by_preventive_support": {"action": best_nonrun_preventive[0], "value": best_nonrun_preventive[1]},
                "by_burden_relief": {"action": best_nonrun_burden_relief[0], "value": best_nonrun_burden_relief[1]},
                "by_dominance_score": {"action": best_nonrun_dom[0], "value": best_nonrun_dom[1]},
            },
        }
        rows.append(row)
        obs = next_obs

    return {
        "regime": regime,
        "seed": int(seed),
        "horizon": int(spec.horizon),
        "steps": len(rows),
        "total_reward": float(total_reward),
        "action_rates": _summarize_action_rates(rows),
        "rows": rows,
    }


def _summarize_regime(rows: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    action_rates = _summarize_action_rates(rows)
    mode_counts = Counter(str(r.get("canonical_commitment_mode")) for r in rows)
    n = float(len(rows) or 1)
    low_true = [r for r in rows if _f(r.get("true_health_norm_before"), 1.0) is not None and _f(r.get("true_health_norm_before"), 1.0) <= 0.50]
    masked_low = [r for r in low_true if (_f(r.get("observed_health_norm"), -1.0) is None or _f(r.get("observed_health_norm"), -1.0) >= 0.75)]
    run_when_low = [r for r in low_true if r.get("action") == "RUN"]
    run_when_masked_low = [r for r in masked_low if r.get("action") == "RUN"]

    run_snap = [r.get("run_snapshot", {}) or {} for r in rows]
    nonrun = [r.get("best_nonrun", {}) or {} for r in rows]
    nonrun_dec = [((nr.get("by_decision_state") or {}).get("value")) for nr in nonrun]
    nonrun_dom = [((nr.get("by_dominance_score") or {}).get("value")) for nr in nonrun]
    run_dom = [rs.get("dominance_score") for rs in run_snap]
    run_dec = [rs.get("decision_state") for rs in run_snap]
    run_burden = [rs.get("burden_pressure") for rs in run_snap]
    run_fracture = [rs.get("fracture_state") for rs in run_snap]

    # How often is RUN's dominance score above all non-RUN candidates despite true health being low?
    dominant_run_low = []
    for r in low_true:
        rs = r.get("run_snapshot", {}) or {}
        nr = r.get("best_nonrun", {}) or {}
        rd = _f(rs.get("dominance_score"), -999.0)
        nd = _f((nr.get("by_dominance_score") or {}).get("value"), -999.0)
        if rd is not None and nd is not None and rd > nd:
            dominant_run_low.append(r)

    # Time-bucket summaries expose whether burden rises early or only after collapse.
    buckets: Dict[str, List[Mapping[str, Any]]] = {"early": [], "mid": [], "late": []}
    max_t = max([int(r.get("t", 0) or 0) for r in rows] or [1])
    for r in rows:
        frac = float(int(r.get("t", 0) or 0)) / float(max(1, max_t))
        if frac < 0.33:
            buckets["early"].append(r)
        elif frac < 0.66:
            buckets["mid"].append(r)
        else:
            buckets["late"].append(r)
    bucket_summary: Dict[str, Any] = {}
    for name, brs in buckets.items():
        snaps = [r.get("run_snapshot", {}) or {} for r in brs]
        bucket_summary[name] = {
            "n": len(brs),
            "action_rates": _summarize_action_rates(brs),
            "mean_true_health_norm": _safe_mean(r.get("true_health_norm_before") for r in brs),
            "mean_observed_health_norm": _safe_mean(r.get("observed_health_norm") for r in brs),
            "mean_run_local_support": _safe_mean(s.get("local_support") for s in snaps),
            "mean_run_burden_pressure": _safe_mean(s.get("burden_pressure") for s in snaps),
            "mean_run_fracture_state": _safe_mean(s.get("fracture_state") for s in snaps),
            "mean_run_dominance_score": _safe_mean(s.get("dominance_score") for s in snaps),
        }

    return {
        "n_steps": len(rows),
        "action_rates": action_rates,
        "commitment_modes": {k: int(v) for k, v in mode_counts.items()},
        "commitment_mode_rates": {k: float(v) / n for k, v in mode_counts.items()},
        "mean_true_health_norm": _safe_mean(r.get("true_health_norm_before") for r in rows),
        "mean_observed_health_norm": _safe_mean(r.get("observed_health_norm") for r in rows),
        "mean_run_local_support": _safe_mean(rs.get("local_support") for rs in run_snap),
        "mean_run_burden_pressure": _safe_mean(run_burden),
        "mean_run_fracture_state": _safe_mean(run_fracture),
        "mean_run_decision_state": _safe_mean(run_dec),
        "mean_run_dominance_score": _safe_mean(run_dom),
        "mean_best_nonrun_decision_state": _safe_mean(nonrun_dec),
        "mean_best_nonrun_dominance_score": _safe_mean(nonrun_dom),
        "mean_run_dominance_minus_best_nonrun": _safe_mean(
            (_f(r.get("run_snapshot", {}).get("dominance_score"), 0.0) or 0.0)
            - (_f((r.get("best_nonrun", {}).get("by_dominance_score") or {}).get("value"), 0.0) or 0.0)
            for r in rows
        ),
        "low_true_health_steps": len(low_true),
        "masked_low_true_health_steps": len(masked_low),
        "run_rate_when_true_health_le_half": float(len(run_when_low)) / float(len(low_true) or 1),
        "run_rate_when_true_low_but_observed_high_or_absent": float(len(run_when_masked_low)) / float(len(masked_low) or 1),
        "run_dominates_when_true_health_le_half_rate": float(len(dominant_run_low)) / float(len(low_true) or 1),
        "time_buckets": bucket_summary,
    }


def _classify(summary: Mapping[str, Any]) -> Dict[str, Any]:
    regimes = summary.get("by_regime", {}) if isinstance(summary, Mapping) else {}
    middle = regimes.get("middle", {}) if isinstance(regimes, Mapping) else {}
    renewal = regimes.get("renewal_like", {}) if isinstance(regimes, Mapping) else {}
    findings: List[str] = []
    if middle:
        if float(middle.get("action_rates", {}).get("RUN", 0.0)) > 0.85:
            findings.append("middle remains RUN-dominant; candidate/readout does not create enough preventive action pressure.")
        if float(middle.get("run_rate_when_true_health_le_half", 0.0)) > 0.50:
            findings.append("middle often RUNs even when audit-only true health is <= 0.5; public candidate evidence does not anticipate degradation strongly enough.")
        if float(middle.get("mean_run_dominance_minus_best_nonrun", 0.0)) > 0.15:
            findings.append("middle RUN dominance score stays far above best non-RUN candidate; CommitmentSurface is not the immediate bottleneck because the candidate rows already favor RUN.")
    if renewal:
        if float(renewal.get("action_rates", {}).get("RUN", 1.0)) < 0.70:
            findings.append("renewal_like creates enough candidate contrast to move away from RUN; strong burden/hiddenness survives publication.")
        if float(renewal.get("commitment_mode_rates", {}).get("reopen_or_sample", 0.0)) > float(middle.get("commitment_mode_rates", {}).get("reopen_or_sample", 0.0)):
            findings.append("reopen/sample mode is much more active in renewal_like than middle, indicating intermediate burden is too weak/late in middle publication.")
    if not findings:
        findings.append("Trace did not isolate a clear candidate-row asymmetry; inspect raw traces.")
    return {
        "diagnosis": findings,
        "next_audit_target": "public middle-regime evidence mapping into candidate burden/sampling, especially observed-health masking and RUN dominance before visible collapse",
    }


def run_study(regimes: Sequence[str], seeds: Sequence[int], max_steps: Optional[int] = None) -> Dict[str, Any]:
    episodes: List[Dict[str, Any]] = []
    trace_rows: List[Dict[str, Any]] = []
    for regime in regimes:
        for seed in seeds:
            ep = _trace_episode(str(regime), int(seed), max_steps=max_steps)
            episodes.append({k: v for k, v in ep.items() if k != "rows"})
            trace_rows.extend(ep["rows"])
    by_regime: Dict[str, Any] = {}
    for regime in regimes:
        rrows = [r for r in trace_rows if r.get("regime") == regime]
        by_regime[str(regime)] = _summarize_regime(rrows)
    summary = {
        "study": "maintenance_candidate_row_trace_v1",
        "purpose": "trace public observations, raw candidates, CandidateSurface rows, and CommitmentSurface assessment for middle vs renewal_like maintenance",
        "oracle_note": "true_health_* fields are audit-only and are never fed to the CO adapter/runtime",
        "regimes": list(regimes),
        "seeds": [int(s) for s in seeds],
        "max_steps": max_steps,
        "episodes": episodes,
        "by_regime": by_regime,
    }
    summary["classification"] = _classify(summary)
    return {"summary": summary, "trace_rows": trace_rows}


def main() -> None:
    ap = argparse.ArgumentParser(description="Trace CandidateSurface rows in maintenance middle vs renewal_like")
    ap.add_argument("--out", default="outputs/maintenance_candidate_row_trace_v1.json")
    ap.add_argument("--regimes", nargs="*", default=list(DEFAULT_REGIMES))
    ap.add_argument("--seeds", nargs="*", type=int, default=list(DEFAULT_SEEDS))
    ap.add_argument("--max-steps", type=int, default=None)
    args = ap.parse_args()
    result = run_study(args.regimes, args.seeds, max_steps=args.max_steps)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    sys.stdout.flush()
    os._exit(0)


if __name__ == "__main__":
    main()
