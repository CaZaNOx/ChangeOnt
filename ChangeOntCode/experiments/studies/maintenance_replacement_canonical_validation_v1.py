from __future__ import annotations

"""Canonical validation for the maintenance/replacement family.

This study is diagnostic, not a success claim.  It asks whether the active
six-question placement bridge does causal work in the CO maintenance runner:

1. derive public shape_prior6 for each regime,
2. compare CO against public baselines,
3. run native-shape versus wrong-shape CO interventions,
4. classify failures into coarse architectural buckets.

Wrong-shape runs use a study-only ``shape_prior6_override`` placed on the public
problem packet.  The normal runtime path remains public problem_contract ->
shape_prior6 -> direct_controls.
"""

import argparse
import json
import math
import os
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, pstdev
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from agents.co.adapters.maintenance_replacement_adapter import COAdapterMaintenanceReplacement
from agents.co.placement.shape_prior6 import SHAPE_PRIOR6_AXES, derive_shape_prior6, shape_prior6_to_direct_controls
from environments.maintenance_replacement.env import ACTIONS, MaintenanceReplacementEnv
from experiments.baselines.maintenance_replacement import BASELINE_ALIASES, make_maintenance_policy
from experiments.runners.maintenance_replacement_runner import build_agent, spec_from_name

REGIMES: Tuple[str, ...] = ("bandit_like", "middle", "renewal_like")
BASELINES: Tuple[str, ...] = ("random", "threshold", "threshold_opt", "q_learning", "finite_horizon_dp")
CO_SHAPE_LABELS: Tuple[str, ...] = ("native", "bandit_like", "middle", "renewal_like", "neutral")
DEFAULT_SEEDS: Tuple[int, ...] = (0, 1, 2, 3, 4)


def _safe_mean(xs: Sequence[float]) -> Optional[float]:
    return float(mean(xs)) if xs else None


def _safe_std(xs: Sequence[float]) -> Optional[float]:
    return float(pstdev(xs)) if len(xs) > 1 else 0.0 if xs else None


def _l1_rates(a: Mapping[str, float], b: Mapping[str, float]) -> float:
    return float(sum(abs(float(a.get(k, 0.0)) - float(b.get(k, 0.0))) for k in ACTIONS))


def _shape_report_for_regime(regime: str) -> Dict[str, Any]:
    spec = spec_from_name(regime, 0)
    env = MaintenanceReplacementEnv(spec)
    obs, _, _, _ = env.reset(seed=0)
    adapter = COAdapterMaintenanceReplacement(core=None)
    contract = adapter._problem_contract(obs)
    shape = derive_shape_prior6(contract)
    controls = shape_prior6_to_direct_controls(shape)
    return {
        "regime": regime,
        "observation_mode": str(spec.observe_health),
        "problem_contract": contract,
        "shape_prior6": shape,
        "direct_controls": controls,
    }


def _shape_library() -> Dict[str, Dict[str, Any]]:
    lib = {r: _shape_report_for_regime(r)["shape_prior6"] for r in REGIMES}
    lib["neutral"] = {
        "schema": "co_shape_prior6_v2",
        "axes": {k: 0.5 for k in SHAPE_PRIOR6_AXES},
        "source": "study_neutral_override",
        "status": "study_override",
        "notes": "Neutral five-point six-question shape used only for wrong-shape validation.",
    }
    return lib


def _action_rates(counts: Mapping[str, int], steps: int) -> Dict[str, float]:
    denom = float(max(1, int(steps)))
    return {a: float(counts.get(a, 0)) / denom for a in ACTIONS}


def _run_episode_with_trace(
    *,
    regime: str,
    agent_kind: str,
    seed: int,
    shape_label: Optional[str] = None,
    shape_override: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    spec = spec_from_name(regime, int(seed))
    env = MaintenanceReplacementEnv(spec)
    obs, _, done, info = env.reset(seed=int(seed))
    if agent_kind == "co":
        co_params: Dict[str, Any] = {}
        if shape_override is not None:
            co_params["shape_prior6_override"] = shape_override
        agent = build_agent("co", int(seed), spec=spec, co_params=co_params or None)
    else:
        agent = make_maintenance_policy(agent_kind, spec, seed=int(seed))

    total = 0.0
    counts: Counter[str] = Counter()
    rows: List[Dict[str, Any]] = []
    header_rows: List[Dict[str, float]] = []
    selection_rows: List[Dict[str, Any]] = []

    while not done:
        if agent_kind == "co":
            sel = dict(agent.select(obs) or {})
            action = str(sel.get("action", "RUN"))
            selection_rows.append({
                "action": action,
                "commit_readiness": float(sel.get("commit_readiness", 0.0) or 0.0),
                "evidence_margin": float(sel.get("evidence_margin", 0.0) or 0.0),
                "evidence_support": float(sel.get("evidence_support", 0.0) or 0.0),
                "candidate_final_scores": dict(sel.get("candidate_final_scores", {}) or {}),
                "candidate_obs_scores": dict(sel.get("candidate_obs_scores", {}) or {}),
                "problem_packet_keys": list(sel.get("problem_packet_keys", []) or []),
            })
        else:
            action = str(agent.select(obs))
        if action not in ACTIONS:
            action = "RUN"

        next_obs, reward, done, info = env.step(action)
        total += float(reward)
        counts[action] += 1
        fb = {"action": action, "reward": float(reward), "done": bool(done), "info": dict(info)}
        if hasattr(agent, "update"):
            agent.update(fb)

        if agent_kind == "co":
            st = getattr(getattr(agent, "core", None), "header", None)
            state = getattr(st, "state", None)
            if state is not None:
                header_rows.append({
                    "co_weight": float(getattr(state, "co_weight", 0.0)),
                    "collapse_admissibility": float(getattr(state, "collapse_admissibility", 0.5)),
                    "revision_permissibility": float(getattr(state, "revision_permissibility", 0.5)),
                    "support_carry_forward": float(getattr(state, "support_carry_forward", 0.5)),
                    "rival_breadth": float(getattr(state, "rival_breadth", 0.5)),
                    "nonlocal_authority": float(getattr(state, "nonlocal_authority", 0.5)),
                    "path_sensitivity": float(getattr(state, "path_sensitivity", 0.5)),
                    "local_authority": float(getattr(state, "local_authority", 0.5)),
                    "evidence_gate": float(getattr(state, "evidence_gate", 0.0)),
                    "support_evidence": float(getattr(state, "support_evidence", 0.0)),
                    "retention_depth": float(getattr(state, "retention_depth", 0.0)),
                    "fracture_tolerance": float(getattr(state, "fracture_tolerance", 0.0)),
                })

        rows.append({
            "t": int(obs.get("t", 0) or 0),
            "action": action,
            "reward": float(reward),
            "done": bool(done),
            "observed_health_norm": obs.get("observed_health_norm"),
            "health_observed": bool(obs.get("health_observed", False)),
            "health_true_after": int(info.get("health_true", -1)),
            "event": str(info.get("last_event", "")),
        })
        obs = next_obs

    steps = len(rows)
    metrics: Dict[str, Any] = {}
    if header_rows:
        for k in header_rows[0].keys():
            metrics[f"mean_{k}"] = _safe_mean([float(r[k]) for r in header_rows])
    if selection_rows:
        for k in ("commit_readiness", "evidence_margin", "evidence_support"):
            metrics[f"mean_{k}"] = _safe_mean([float(r[k]) for r in selection_rows])
        override_seen = any("shape_prior6" in set(r.get("problem_packet_keys", [])) for r in selection_rows)
        metrics["shape_override_packet_seen"] = bool(override_seen)

    return {
        "family": "maintenance_replacement",
        "regime": regime,
        "agent": agent_kind,
        "shape_label": shape_label,
        "seed": int(seed),
        "horizon": int(spec.horizon),
        "observation_mode": str(spec.observe_health),
        "total_reward": float(total),
        "final_health_true": int(info.get("health_true", -1)),
        "steps": int(steps),
        "action_counts": {a: int(counts.get(a, 0)) for a in ACTIONS},
        "action_rates": _action_rates(counts, steps),
        "metrics": metrics,
    }


def _aggregate_rows(rows: Sequence[Mapping[str, Any]], keys: Sequence[str]) -> List[Dict[str, Any]]:
    buckets: Dict[Tuple[Any, ...], List[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        if "error" in row:
            continue
        buckets[tuple(row.get(k) for k in keys)].append(row)
    out: List[Dict[str, Any]] = []
    for key_vals, vals in sorted(buckets.items(), key=lambda kv: tuple(str(x) for x in kv[0])):
        rewards = [float(v["total_reward"]) for v in vals]
        merged_counts = Counter()
        for v in vals:
            merged_counts.update({a: int(v.get("action_counts", {}).get(a, 0)) for a in ACTIONS})
        steps = sum(int(v.get("steps", 0)) for v in vals)
        rec = {k: key_vals[i] for i, k in enumerate(keys)}
        rec.update({
            "n": len(vals),
            "mean_total_reward": _safe_mean(rewards),
            "std_total_reward": _safe_std(rewards),
            "min_total_reward": float(min(rewards)) if rewards else None,
            "max_total_reward": float(max(rewards)) if rewards else None,
            "action_counts_total": {a: int(merged_counts.get(a, 0)) for a in ACTIONS},
            "action_rates_meaned_by_step": _action_rates(merged_counts, steps),
        })
        # Aggregate selected CO metrics when available.
        metric_keys = sorted({mk for v in vals for mk in (v.get("metrics", {}) or {}).keys() if isinstance((v.get("metrics", {}) or {}).get(mk), (int, float, bool))})
        if metric_keys:
            rec["metrics_mean"] = {}
            for mk in metric_keys:
                xs = [float((v.get("metrics", {}) or {}).get(mk)) for v in vals if isinstance((v.get("metrics", {}) or {}).get(mk), (int, float, bool))]
                rec["metrics_mean"][mk] = _safe_mean(xs)
        out.append(rec)
    return out


def _failure_classification(
    *,
    baseline_aggregate: Sequence[Mapping[str, Any]],
    co_shape_aggregate: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    by_regime_shape = {(r["regime"], r["shape_label"]): r for r in co_shape_aggregate}
    by_regime_baseline: Dict[str, List[Mapping[str, Any]]] = defaultdict(list)
    for r in baseline_aggregate:
        by_regime_baseline[str(r["regime"])].append(r)

    per_regime: Dict[str, Any] = {}
    for regime in REGIMES:
        native = by_regime_shape.get((regime, "native"))
        shapes = [by_regime_shape[(regime, lab)] for lab in CO_SHAPE_LABELS if (regime, lab) in by_regime_shape]
        shape_rewards = {str(r["shape_label"]): float(r.get("mean_total_reward") or 0.0) for r in shapes}
        native_reward = float(native.get("mean_total_reward") or 0.0) if native else None
        best_shape_label = max(shape_rewards, key=lambda k: shape_rewards[k]) if shape_rewards else None
        best_shape_reward = shape_rewards.get(best_shape_label) if best_shape_label else None
        native_rank = None
        if native_reward is not None:
            native_rank = 1 + sum(1 for v in shape_rewards.values() if v > native_reward + 1e-9)
        rewards = list(shape_rewards.values())
        spread = (max(rewards) - min(rewards)) if rewards else None

        native_rates = native.get("action_rates_meaned_by_step", {}) if native else {}
        l1_to_native = {}
        for r in shapes:
            lab = str(r["shape_label"])
            l1_to_native[lab] = _l1_rates(native_rates, r.get("action_rates_meaned_by_step", {})) if native else None
        max_l1 = max([float(v) for k, v in l1_to_native.items() if v is not None and k != "native"] or [0.0])

        baselines = by_regime_baseline.get(regime, [])
        baseline_rewards = {str(r["agent"]): float(r.get("mean_total_reward") or 0.0) for r in baselines}
        best_baseline_label = max(baseline_rewards, key=lambda k: baseline_rewards[k]) if baseline_rewards else None
        best_baseline_reward = baseline_rewards.get(best_baseline_label) if best_baseline_label else None
        baseline_gap = (native_reward - best_baseline_reward) if native_reward is not None and best_baseline_reward is not None else None

        flags: List[str] = []
        if spread is not None and spread < 2.0 and max_l1 < 0.20:
            flags.append("shape_controls_have_low_observed_effect")
        elif spread is not None and spread < 2.0:
            flags.append("reward_insensitive_to_shape")
        if native_rank is not None and native_rank > 1:
            flags.append("native_shape_not_best")
        if baseline_gap is not None and baseline_gap < -5.0:
            flags.append("native_co_below_best_public_baseline")
        if max_l1 < 0.20:
            flags.append("action_distribution_weakly_sensitive_to_shape")
        if native and float((native.get("action_rates_meaned_by_step", {}) or {}).get("RUN", 0.0)) > 0.80 and regime in {"middle", "renewal_like"}:
            flags.append("native_co_overruns_relative_to_degradation_regime")
        if native and float((native.get("action_rates_meaned_by_step", {}) or {}).get("INSPECT", 0.0)) > 0.40 and regime == "bandit_like":
            flags.append("native_co_overinspects_in_direct_low_degradation_regime")

        if "shape_controls_have_low_observed_effect" in flags or "action_distribution_weakly_sensitive_to_shape" in flags:
            likely_bucket = "controls_or_readout_are_insensitive"
        elif "native_shape_not_best" in flags:
            likely_bucket = "shape_projection_or_control_mapping_misaligned"
        elif "native_co_below_best_public_baseline" in flags:
            likely_bucket = "generic_readout_candidate_quality_gap"
        else:
            likely_bucket = "no_clear_failure_from_this_small_validation"

        per_regime[regime] = {
            "native_mean_reward": native_reward,
            "best_shape_label": best_shape_label,
            "best_shape_mean_reward": best_shape_reward,
            "native_shape_rank": native_rank,
            "shape_reward_spread": spread,
            "l1_action_distance_to_native": l1_to_native,
            "max_l1_action_distance_to_native": max_l1,
            "best_public_baseline": best_baseline_label,
            "best_public_baseline_mean_reward": best_baseline_reward,
            "native_minus_best_public_baseline": baseline_gap,
            "flags": flags,
            "likely_bucket": likely_bucket,
        }

    return {
        "method": "heuristic_failure_classification_from_reward_spread_action_distribution_and_baseline_gap",
        "per_regime": per_regime,
        "global_read": _global_read(per_regime),
    }


def _global_read(per_regime: Mapping[str, Any]) -> List[str]:
    reads: List[str] = []
    native_not_best = [r for r, v in per_regime.items() if "native_shape_not_best" in v.get("flags", [])]
    weak_action = [r for r, v in per_regime.items() if "action_distribution_weakly_sensitive_to_shape" in v.get("flags", [])]
    below_baseline = [r for r, v in per_regime.items() if "native_co_below_best_public_baseline" in v.get("flags", [])]
    if native_not_best:
        reads.append("Native six-question shape is not consistently best: " + ", ".join(native_not_best))
    if weak_action:
        reads.append("Wrong-shape interventions weakly affect action distribution in: " + ", ".join(weak_action))
    if below_baseline:
        reads.append("Native CO remains below best public baseline in: " + ", ".join(below_baseline))
    if not reads:
        reads.append("No coarse failure triggered by this small validation; this is not a success proof.")
    return reads


def run_study(seeds: Sequence[int] = DEFAULT_SEEDS) -> Dict[str, Any]:
    shape_reports = [_shape_report_for_regime(r) for r in REGIMES]
    shapes = _shape_library()
    rows: List[Dict[str, Any]] = []
    skips: List[Dict[str, Any]] = []

    # Baseline comparison.
    for regime in REGIMES:
        spec0 = spec_from_name(regime, 0)
        for agent in BASELINES:
            if agent == "finite_horizon_dp" and str(spec0.observe_health) != "direct":
                skips.append({
                    "section": "baseline_comparison",
                    "regime": regime,
                    "agent": agent,
                    "reason": "finite_horizon_dp is parity-valid only when health is publicly direct-observed",
                })
                continue
            for seed in seeds:
                try:
                    rows.append(_run_episode_with_trace(regime=regime, agent_kind=agent, seed=int(seed)))
                except Exception as exc:
                    rows.append({"section": "baseline_comparison", "regime": regime, "agent": agent, "seed": int(seed), "error": type(exc).__name__, "message": str(exc)})

    # Native and wrong-shape CO tests.
    co_rows: List[Dict[str, Any]] = []
    for regime in REGIMES:
        for shape_label in CO_SHAPE_LABELS:
            override = None if shape_label == "native" else shapes[shape_label]
            for seed in seeds:
                try:
                    co_rows.append(_run_episode_with_trace(regime=regime, agent_kind="co", seed=int(seed), shape_label=shape_label, shape_override=override))
                except Exception as exc:
                    co_rows.append({"section": "wrong_shape_tests", "regime": regime, "agent": "co", "shape_label": shape_label, "seed": int(seed), "error": type(exc).__name__, "message": str(exc)})

    baseline_aggregate = _aggregate_rows(rows, ["regime", "agent"])
    co_shape_aggregate = _aggregate_rows(co_rows, ["regime", "agent", "shape_label"])
    classification = _failure_classification(baseline_aggregate=baseline_aggregate, co_shape_aggregate=co_shape_aggregate)

    return {
        "study": "maintenance_replacement_canonical_validation_v1",
        "status": "diagnostic_validation_not_general_success_claim",
        "seeds": [int(s) for s in seeds],
        "sections": {
            "shape_derivation": shape_reports,
            "baseline_comparison": {
                "rows": rows,
                "aggregate": baseline_aggregate,
                "skips": skips,
            },
            "wrong_shape_tests": {
                "rows": co_rows,
                "aggregate": co_shape_aggregate,
                "shape_library": shapes,
            },
            "failure_classification": classification,
        },
        "non_claims": [
            "This study does not prove CO generality.",
            "Wrong-shape overrides are study interventions; the normal active path remains problem_contract-derived shape_prior6.",
            "finite_horizon_dp is skipped outside direct public health observation to avoid oracle access.",
            "Reward changes are interpreted together with action-distribution changes to avoid benchmark theater.",
        ],
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Canonical maintenance/replacement validation v1")
    ap.add_argument("--out", default="outputs/maintenance_replacement_canonical_validation_v1.json")
    ap.add_argument("--seeds", default=",".join(str(s) for s in DEFAULT_SEEDS))
    args = ap.parse_args()
    seeds = tuple(int(x.strip()) for x in str(args.seeds).split(",") if x.strip())
    result = run_study(seeds=seeds)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"wrote": str(out), "seeds": list(seeds), "baseline_rows": len(result["sections"]["baseline_comparison"]["rows"]), "co_rows": len(result["sections"]["wrong_shape_tests"]["rows"]), "skips": len(result["sections"]["baseline_comparison"]["skips"]), "global_read": result["sections"]["failure_classification"]["global_read"]}, indent=2, sort_keys=True), flush=True)
    # Some container/Python combinations used in this project keep non-daemon
    # resources alive after CO imports.  Force process termination after durable
    # JSON has been written so CLI studies are scriptable.
    os._exit(0)


if __name__ == "__main__":
    main()
