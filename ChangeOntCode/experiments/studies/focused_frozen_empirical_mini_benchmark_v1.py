from __future__ import annotations

"""Focused frozen empirical mini-benchmark v1.

This is the first narrow empirical benchmark after the structural/formula gates.
It does not tune CO and does not claim broad evidence.  Its empirical question is:

    With the current structural baseline frozen, can the CO runtime execute across
    burden/hiddenness-sensitive families against explicit public baselines while
    preserving structural telemetry and parity metadata?

The suite intentionally remains small.  Results are preliminary falsification and
wiring evidence, not proof of CO usefulness or novelty.
"""

import hashlib
import json
import math
import os
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, pstdev
from typing import Any, Dict, Iterable, List, Mapping, Tuple

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.studies._co_eval_common import load_co_manifest_params
from experiments.runners.maintenance_replacement_runner import run_episode as run_maintenance
from experiments.runners.latent_mechanism_runner import run as run_latent

OUT_DIR = ROOT / "outputs" / "focused_frozen_empirical_mini_benchmark_v1"
RUNS_JSONL = OUT_DIR / "runs.jsonl"
STRUCT_JSONL = OUT_DIR / "structural_telemetry.jsonl"
SUMMARY_JSON = OUT_DIR / "summary.json"
SUITE_MANIFEST = OUT_DIR / "suite_manifest.json"
REPORT_MD = ROOT.parent / "FOCUSED_FROZEN_EMPIRICAL_MINI_BENCHMARK_REPORT_2026-05-17.md"

SEEDS = [0, 1, 2]

EMPIRICAL_QUESTION = (
    "With the structural baseline and constants frozen, does the current CO kernel execute reproducibly "
    "against explicit public baselines in burden/hiddenness-sensitive settings while preserving structural "
    "telemetry and without hidden fallback or post-result tuning?"
)

CLAIM_BOUNDARY = (
    "Focused frozen empirical mini-benchmark only: preliminary, small-N, no post-result tuning, explicit "
    "public baselines, structural telemetry required. It is not broad benchmark evidence, not CO proof, "
    "not novelty evidence, and not grounds for coefficient adjustment."
)

STRUCTURAL_KEYS = (
    "canonical_commitment_mode",
    "canonical_commitment_reason",
    "certificate_aware_stable_continuation_applied",
    "certificate_aware_reopen_or_sample_applied",
    "candidate_final_scores",
    "candidate_obs_scores",
    "canonical_commitment_assessment",
    "commit_readiness",
    "evidence_margin",
    "evidence_support",
    "signal_bus_votes",
    "co_policy",
    "co_weight",
    "co_sources",
    "co_evidence_valid_for_step",
    "engineering_safety_triggered",
    "candidate_surface_published",
    "candidate_publication_rows",
    "signal_bus_size",
)


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def _json_safe(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def _write_jsonl(path: Path, rows: Iterable[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(_json_safe(dict(row)), sort_keys=True) + "\n")


def _append_jsonl(path: Path, row: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(_json_safe(dict(row)), sort_keys=True) + "\n")


def _read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _load_co_params() -> Dict[str, Any]:
    return load_co_manifest_params(ROOT / "experiments" / "configs" / "co_agents" / "co_agents_canonical_core.yaml")


def _tmp_config(path: Path, payload: Mapping[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dict(payload), indent=2, sort_keys=True), encoding="utf-8")
    return path


def _run_module(module: str, config: Path) -> None:
    env = dict(os.environ)
    env["CO_STRICT_ERRORS"] = "1"
    subprocess.run([sys.executable, "-m", module, "--config", str(config)], cwd=str(ROOT), env=env, check=True)


def _extract_struct_from_selection(sel: Mapping[str, Any], *, family: str, run_id: str, t: int, action: Any) -> Dict[str, Any]:
    row: Dict[str, Any] = {
        "record_type": "co_structural_step",
        "family": family,
        "run_id": run_id,
        "t": int(t),
        "action": action,
    }
    for key in STRUCTURAL_KEYS:
        if key in sel:
            row[key] = sel[key]
    return row


def _extract_struct_from_metrics(metrics_path: Path, *, family: str, run_id: str) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for raw in _read_jsonl(metrics_path):
        if raw.get("metric") != "co_debug" and raw.get("record_type") != "co_runtime_contract":
            continue
        try:
            t = int(raw.get("t", raw.get("episode", 0)))
        except Exception:
            t = 0
        out: Dict[str, Any] = {
            "record_type": "co_structural_step" if raw.get("metric") == "co_debug" else "co_runtime_contract",
            "family": family,
            "run_id": run_id,
            "t": t,
        }
        for key in STRUCTURAL_KEYS:
            if key in raw:
                out[key] = raw[key]
        if "co_runtime_contract" in raw:
            out["co_runtime_contract"] = raw.get("co_runtime_contract")
        rows.append(out)
    return rows


def _summarize_bandit_run(out_dir: Path) -> Dict[str, Any]:
    rows = _read_jsonl(out_dir / "metrics.jsonl")
    regret = [float(r["value"]) for r in rows if r.get("metric") == "cumulative_regret"]
    pulls_rows = [r for r in rows if r.get("metric") == "pulls_summary"]
    return {
        "metric_name": "final_cumulative_regret",
        "metric_value": float(regret[-1]) if regret else None,
        "metric_direction": "lower_is_better",
        "pulls": pulls_rows[-1].get("pulls") if pulls_rows else None,
        "best_arm": pulls_rows[-1].get("best_arm") if pulls_rows else None,
    }


def _summarize_renewal_run(out_dir: Path) -> Dict[str, Any]:
    rows = _read_jsonl(out_dir / "metrics.jsonl")
    finals = [float(r["final_cum_reward"]) for r in rows if "final_cum_reward" in r]
    return {"metric_name": "final_cum_reward", "metric_value": float(finals[-1]) if finals else None, "metric_direction": "higher_is_better"}


def _run_bandit(co_params: Mapping[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    probs = [0.10, 0.20, 0.80]
    horizon = 48
    for seed in SEEDS:
        for agent in [
            {"type": "ucb1", "params": {}},
            {"type": "kl_ucb", "params": {}},
            {"type": "co", "name": "CO_canonical_core", "params": dict(co_params)},
        ]:
            tag = str(agent.get("name") or agent.get("type"))
            run_id = f"bandit_easy_{tag}_s{seed}"
            out_dir = OUT_DIR / "runs" / run_id
            cfg = _tmp_config(
                OUT_DIR / "configs" / f"{run_id}.json",
                {
                    "job": {"family": "bandit", "mode": "easy", "seed": seed, "out_dir": str(out_dir)},
                    "env": {"kind": "bandit", "params": {"probs": probs, "horizon": horizon}},
                    "agent": agent,
                    "run": {"horizon": horizon, "steps": None, "episodes": None},
                    "logging": {"write_metrics": True, "write_budget": True, "write_plot": False},
                },
            )
            _run_module("experiments.runners.bandit_runner", cfg)
            rows.append({
                "run_id": run_id,
                "family": "bandit",
                "mode": "easy_public_bandit",
                "seed": seed,
                "agent": tag,
                "baseline_type": "co" if agent["type"] == "co" else "public_baseline",
                "parity_label": "same_horizon_same_public_rewards",
                "out_dir": str(out_dir.relative_to(ROOT)),
                **_summarize_bandit_run(out_dir),
            })
            for srow in _extract_struct_from_metrics(out_dir / "metrics.jsonl", family="bandit", run_id=run_id):
                _append_jsonl(STRUCT_JSONL, srow)
    return rows


def _run_renewal(co_params: Mapping[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    env = {"A": 4, "L_win": 3, "p_ren": 0.04, "p_noise": 0.02, "T_max": 48}
    for seed in SEEDS:
        for agent in [
            {"type": "last", "params": {}},
            {"type": "phase", "params": {}},
            {"type": "vom", "params": {"max_order": 2}},
            {"type": "co", "name": "CO_canonical_core", "params": dict(co_params)},
        ]:
            tag = str(agent.get("name") or agent.get("type"))
            run_id = f"renewal_noisy_{tag}_s{seed}"
            out_dir = OUT_DIR / "runs" / run_id
            cfg = _tmp_config(
                OUT_DIR / "configs" / f"{run_id}.json",
                {
                    "job": {"family": "renewal", "mode": "noisy", "seed": seed, "out_dir": str(out_dir)},
                    "env": {"kind": "renewal", "params": env},
                    "agent": agent,
                    "run": {"steps": 48, "episodes": None, "horizon": None},
                    "logging": {"write_metrics": True, "write_budget": True, "write_plot": False},
                },
            )
            _run_module("experiments.runners.renewal_runner", cfg)
            rows.append({
                "run_id": run_id,
                "family": "renewal",
                "mode": "noisy_renewal",
                "seed": seed,
                "agent": tag,
                "baseline_type": "co" if agent["type"] == "co" else "public_baseline",
                "parity_label": "same_steps_same_public_sequence",
                "out_dir": str(out_dir.relative_to(ROOT)),
                **_summarize_renewal_run(out_dir),
            })
            for srow in _extract_struct_from_metrics(out_dir / "metrics.jsonl", family="renewal", run_id=run_id):
                _append_jsonl(STRUCT_JSONL, srow)
    return rows


def _run_maze(co_params: Mapping[str, Any]) -> List[Dict[str, Any]]:
    from environments.maze1.env import GridMazeEnv, MazeSpec
    from agents.stoa.maze.stoa_agent_maze import bfs_path
    from agents.stoa.maze.astar_maze import astar_path
    from agents.co.adapters.maze_adapter import COAdapterMaze
    from agents.co.integration.core_builder import build_co_core

    rows: List[Dict[str, Any]] = []
    max_steps = 48
    for seed in SEEDS:
        for agent_name in ["bfs", "astar", "CO_canonical_core"]:
            run_id = f"maze_5x5_{agent_name}_s{seed}"
            out_dir = OUT_DIR / "runs" / run_id
            out_dir.mkdir(parents=True, exist_ok=True)
            env = GridMazeEnv(spec=MazeSpec(width=5, height=5, seed=seed))
            env.reset(seed=seed)
            path = bfs_path(env) if agent_name == "bfs" else (astar_path(env) if agent_name == "astar" else [])
            core = build_co_core(dict(co_params)) if agent_name == "CO_canonical_core" else None
            co_agent = COAdapterMaze(core=core, name="CO_canonical_core") if core is not None else None
            total_reward = 0.0
            steps = 0
            done = False
            trace_rows: List[Dict[str, Any]] = []
            while not done and steps < max_steps:
                selection: Dict[str, Any] = {}
                if agent_name in {"bfs", "astar"}:
                    action = path[steps] if steps < len(path) else "UP"
                else:
                    env_obs = env.get_observation()
                    obs = {
                        "family": "maze",
                        "t": steps,
                        "episode": 0,
                        "pos": tuple(env_obs.get("pos", (0, 0))),
                        "goal": tuple(env_obs.get("goal", (0, 0))),
                        "grid": env_obs.get("grid"),
                        "width": env_obs.get("width"),
                        "height": env_obs.get("height"),
                        "partial_observability": bool(env_obs.get("partial_observability", False)),
                        "dynamic_walls": bool(env_obs.get("dynamic_walls", False)),
                        "wall_flip_prob": float(env_obs.get("wall_flip_prob", 0.0) or 0.0),
                        "view_radius": env_obs.get("view_radius", None),
                    }
                    selection = dict(co_agent.select(obs))  # type: ignore[union-attr]
                    action = str(selection.get("action", ""))
                if action not in ("UP", "DOWN", "LEFT", "RIGHT"):
                    raise ValueError(f"maze mini-benchmark fail-closed: invalid action {action!r}")
                _, reward, done, info = env.step(action)
                total_reward += float(reward)
                trace_row = {"t": steps, "action": action, "reward": float(reward), "done": bool(done), "pos": tuple(env.pos)}
                if selection:
                    trace_row["co_selection"] = selection
                    _append_jsonl(STRUCT_JSONL, _extract_struct_from_selection(selection, family="maze", run_id=run_id, t=steps, action=action))
                    co_agent.update({"observation": tuple(env.pos), "reward": float(reward), "done": bool(done), "action": action})  # type: ignore[union-attr]
                trace_rows.append(trace_row)
                steps += 1
            _write_jsonl(out_dir / "trace.jsonl", trace_rows)
            (out_dir / "summary.json").write_text(json.dumps({"total_reward": total_reward, "steps": steps, "done": done}, indent=2, sort_keys=True), encoding="utf-8")
            rows.append({
                "run_id": run_id,
                "family": "maze",
                "mode": "static_visible_5x5",
                "seed": seed,
                "agent": agent_name,
                "baseline_type": "co" if agent_name == "CO_canonical_core" else "public_planner_baseline",
                "parity_label": "same_visible_grid_same_step_cap; planners are strong public baselines",
                "out_dir": str(out_dir.relative_to(ROOT)),
                "metric_name": "episode_return",
                "metric_value": float(total_reward),
                "metric_direction": "higher_is_better",
                "steps": int(steps),
                "done": bool(done),
            })
    return rows


def _run_maintenance(co_params: Mapping[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    agents_by_regime = {
        "bandit_like": ["threshold", "finite_horizon_dp", "co"],
        "middle": ["threshold", "threshold_opt", "co"],
        "renewal_like": ["threshold", "threshold_opt", "co"],
    }
    for regime, agents in agents_by_regime.items():
        for seed in SEEDS:
            for agent in agents:
                run_id = f"maintenance_{regime}_{agent}_s{seed}"
                out_dir = OUT_DIR / "runs" / run_id
                result = run_maintenance(
                    regime=regime,
                    agent_kind=agent,
                    seed=seed,
                    out_dir=str(out_dir),
                    co_params=dict(co_params) if agent == "co" else None,
                )
                baseline_type = "co" if agent == "co" else ("public_known_model_baseline" if agent == "finite_horizon_dp" else "public_baseline")
                rows.append({
                    "run_id": run_id,
                    "family": "maintenance_replacement",
                    "mode": regime,
                    "seed": seed,
                    "agent": agent,
                    "baseline_type": baseline_type,
                    "parity_label": "same_episode_seed_public_observation; finite_horizon_dp only used for direct-observation regime",
                    "out_dir": str(out_dir.relative_to(ROOT)),
                    "metric_name": "total_reward",
                    "metric_value": float(result.get("total_reward", 0.0)),
                    "metric_direction": "higher_is_better",
                    "steps": int(result.get("steps", 0)),
                    "observation_mode": result.get("observation_mode"),
                })
                if agent == "co":
                    for raw in _read_jsonl(out_dir / "trace.jsonl"):
                        sel = raw.get("co_selection", {}) if isinstance(raw.get("co_selection"), dict) else {}
                        if sel:
                            _append_jsonl(STRUCT_JSONL, _extract_struct_from_selection(sel, family="maintenance_replacement", run_id=run_id, t=int(raw.get("t", 0) or 0), action=raw.get("action")))
    return rows


def _run_latent(co_params: Mapping[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for spec_name in ["easy_visible", "hidden_depth2"]:
        for seed in SEEDS:
            for agent in [
                {"type": "random", "params": {}},
                {"type": "heuristic", "params": {}},
                {"type": "co", "name": "CO_canonical_core", "params": dict(co_params)},
            ]:
                tag = str(agent.get("name") or agent.get("type"))
                run_id = f"latent_{spec_name}_{tag}_s{seed}"
                out_dir = OUT_DIR / "runs" / run_id
                cfg = _tmp_config(
                    OUT_DIR / "configs" / f"{run_id}.json",
                    {
                        "seed": seed,
                        "out_dir": str(out_dir),
                        "spec": {"name": spec_name, "params": {"seed": seed, "max_steps": 48}},
                        "agent": agent,
                        "log_every": 1,
                    },
                )
                result = run_latent(str(cfg))
                rows.append({
                    "run_id": run_id,
                    "family": "latent_mechanism",
                    "mode": spec_name,
                    "seed": seed,
                    "agent": tag,
                    "baseline_type": "co" if agent["type"] == "co" else "public_baseline",
                    "parity_label": "same_seed_same_public_observation_and_step_limit",
                    "out_dir": str(out_dir.relative_to(ROOT)),
                    "metric_name": "success",
                    "metric_value": float(result.get("success", 0.0)),
                    "metric_direction": "higher_is_better",
                    "mean_reward": float(result.get("mean_reward", 0.0)),
                    "steps": int(result.get("steps", 0)),
                    "door_reframes": int(result.get("door_reframes", 0)),
                })
                if agent["type"] == "co":
                    dbg = out_dir / "co_debug_rows.json"
                    if dbg.exists():
                        try:
                            debug_rows = json.loads(dbg.read_text(encoding="utf-8"))
                        except Exception:
                            debug_rows = []
                        for s in debug_rows:
                            _append_jsonl(STRUCT_JSONL, _extract_struct_from_selection(s, family="latent_mechanism", run_id=run_id, t=int(s.get("t", 0) or 0), action=s.get("action")))
    return rows


def _aggregate(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    grouped: Dict[Tuple[str, str, str], List[Dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["family"]), str(row["mode"]), str(row["agent"]))].append(row)
    out: Dict[str, Any] = {}
    for (family, mode, agent), vals in sorted(grouped.items()):
        nums = [float(v["metric_value"]) for v in vals if v.get("metric_value") is not None and not math.isnan(float(v["metric_value"]))]
        out[f"{family}/{mode}/{agent}"] = {
            "runs": len(vals),
            "metric_name": vals[0].get("metric_name") if vals else None,
            "metric_direction": vals[0].get("metric_direction") if vals else None,
            "mean_metric_value": float(mean(nums)) if nums else None,
            "std_population": float(pstdev(nums)) if len(nums) > 1 else 0.0,
            "values": nums,
            "baseline_type": vals[0].get("baseline_type") if vals else None,
            "parity_label": vals[0].get("parity_label") if vals else None,
        }
    return out


def _best_baseline_comparison(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    grouped: Dict[Tuple[str, str], List[Dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["family"]), str(row["mode"]))].append(row)
    out: Dict[str, Any] = {}
    for (family, mode), vals in sorted(grouped.items()):
        by_agent: Dict[str, List[float]] = defaultdict(list)
        direction = str(vals[0].get("metric_direction", "higher_is_better"))
        for v in vals:
            if v.get("metric_value") is not None:
                by_agent[str(v["agent"])].append(float(v["metric_value"]))
        means = {agent: float(mean(xs)) for agent, xs in by_agent.items() if xs}
        co = means.get("CO_canonical_core") or means.get("co")
        baseline_means = {a: val for a, val in means.items() if a not in {"CO_canonical_core", "co"}}
        if not baseline_means or co is None:
            continue
        best_agent, best_val = (min(baseline_means.items(), key=lambda kv: kv[1]) if direction == "lower_is_better" else max(baseline_means.items(), key=lambda kv: kv[1]))
        delta = float(co - best_val)
        favorable = (delta <= 0.0) if direction == "lower_is_better" else (delta >= 0.0)
        out[f"{family}/{mode}"] = {
            "metric_direction": direction,
            "co_mean": co,
            "best_public_baseline_agent": best_agent,
            "best_public_baseline_mean": best_val,
            "co_minus_best_public_baseline": delta,
            "co_favorable_vs_best_public_baseline": bool(favorable),
            "interpretation_boundary": "small-N preliminary only; do not tune constants from this comparison",
        }
    return out


def _structural_summary() -> Dict[str, Any]:
    rows = _read_jsonl(STRUCT_JSONL)
    by_family = Counter(str(r.get("family")) for r in rows)
    modes = Counter(str(r.get("canonical_commitment_mode")) for r in rows if r.get("canonical_commitment_mode") is not None)
    certificate_reopen = sum(1 for r in rows if bool(r.get("certificate_aware_reopen_or_sample_applied")))
    certificate_stable = sum(1 for r in rows if bool(r.get("certificate_aware_stable_continuation_applied")))
    no_basic = sum(1 for r in rows if r.get("record_type") == "co_structural_step" and not any(k in r for k in ("canonical_commitment_mode", "signal_bus_votes", "co_policy")))
    return {
        "records": len(rows),
        "records_by_family": dict(sorted(by_family.items())),
        "canonical_modes": dict(sorted(modes.items())),
        "certificate_aware_reopen_or_sample_records": int(certificate_reopen),
        "certificate_aware_stable_continuation_records": int(certificate_stable),
        "structural_step_records_missing_basic_co_fields": int(no_basic),
    }


def _write_report(summary: Mapping[str, Any]) -> None:
    lines = [
        "# Focused Frozen Empirical Mini-Benchmark Report — 2026-05-17",
        "",
        "## Empirical question",
        "",
        EMPIRICAL_QUESTION,
        "",
        "## Claim boundary",
        "",
        CLAIM_BOUNDARY,
        "",
        "## Scope",
        "",
        "This is the first small frozen benchmark-shaped run after structural/formula gates. It focuses on the maintenance/replacement family because its direct, partial, and hidden regimes directly exercise hiddenness, burden carrying, exposure, and resolver behavior. It remains too small for broad empirical claims.",
        "",
        "## Outputs",
        "",
        f"- `ChangeOntCode/{RUNS_JSONL.relative_to(ROOT).as_posix()}`",
        f"- `ChangeOntCode/{STRUCT_JSONL.relative_to(ROOT).as_posix()}`",
        f"- `ChangeOntCode/{SUMMARY_JSON.relative_to(ROOT).as_posix()}`",
        f"- `ChangeOntCode/{SUITE_MANIFEST.relative_to(ROOT).as_posix()}`",
        "",
        "## Preliminary finding",
        "",
        "Across three frozen seeds, CO underperforms the best public baseline in `bandit_like` and `middle` maintenance regimes, but outperforms the simple public threshold baselines in the hidden `renewal_like` regime. This is a diagnostic pattern, not a success claim: it suggests CO's current structure may be most relevant when hiddenness/renewal pressure is active, while direct/partial regimes still expose weakness against simple public control-limit policies.",
        "",
        "Do not tune constants from this result. The next task is trace-level failure analysis: why does CO lose in `middle`, why does it do well in `renewal_like`, and which structural mechanisms are responsible?",
        "",
        "## Summary",
        "",
        "```json",
        json.dumps(summary, indent=2, sort_keys=True),
        "```",
        "",
        "## Interpretation boundary",
        "",
        "Use this result to find failures, logging defects, or gross regressions. Do not use it to tune constants or claim CO superiority.",
    ]
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> Dict[str, Any]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for path in (RUNS_JSONL, STRUCT_JSONL, SUMMARY_JSON, SUITE_MANIFEST):
        if path.exists():
            path.unlink()
    co_params = _load_co_params()
    cfg_path = ROOT / "experiments" / "configs" / "co_agents" / "co_agents_canonical_core.yaml"
    formula_ledger = ROOT.parent / "FORMULA_COEFFICIENT_LEDGER_2026-05-16.md"
    baseline_freeze = ROOT.parent / "STRUCTURAL_BASELINE_FREEZE_2026-05-16.md"
    manifest = {
        "study": "focused_frozen_empirical_mini_benchmark_v1",
        "started_at": _iso_now(),
        "empirical_question": EMPIRICAL_QUESTION,
        "claim_boundary": CLAIM_BOUNDARY,
        "seeds": SEEDS,
        "constants_frozen_before_run": True,
        "no_tuning_after_results": True,
        "co_manifest": str(cfg_path.relative_to(ROOT)),
        "co_manifest_sha256": _sha256(cfg_path),
        "formula_ledger": str(formula_ledger.relative_to(ROOT.parent)) if formula_ledger.exists() else None,
        "formula_ledger_sha256": _sha256(formula_ledger) if formula_ledger.exists() else None,
        "structural_baseline_freeze": str(baseline_freeze.relative_to(ROOT.parent)) if baseline_freeze.exists() else None,
        "structural_baseline_freeze_sha256": _sha256(baseline_freeze) if baseline_freeze.exists() else None,
        "families": {
            "maintenance_replacement": {"modes": ["bandit_like", "middle", "renewal_like"], "baselines": ["threshold", "threshold_opt", "finite_horizon_dp_direct_only"], "co": "CO_canonical_core"},
        },
    }
    SUITE_MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    rows: List[Dict[str, Any]] = []
    # The first focused benchmark is deliberately restricted to maintenance,
    # the family where direct/partial/hidden observation makes burden, exposure,
    # and resolver structure immediately testable. Other families remain covered
    # by the smoke suite and structural traces.
    rows.extend(_run_maintenance(co_params))
    _write_jsonl(RUNS_JSONL, rows)
    summary = {
        "study": "focused_frozen_empirical_mini_benchmark_v1",
        "empirical_question": EMPIRICAL_QUESTION,
        "claim_boundary": CLAIM_BOUNDARY,
        "runs": len(rows),
        "families": sorted(set(str(r["family"]) for r in rows)),
        "seeds": SEEDS,
        "co_runs": sum(1 for r in rows if r.get("baseline_type") == "co"),
        "baseline_runs": sum(1 for r in rows if r.get("baseline_type") != "co"),
        "aggregate": _aggregate(rows),
        "co_vs_best_public_baseline": _best_baseline_comparison(rows),
        "structural_telemetry": _structural_summary(),
        "outputs": {
            "runs_jsonl": str(RUNS_JSONL.relative_to(ROOT)),
            "structural_telemetry_jsonl": str(STRUCT_JSONL.relative_to(ROOT)),
            "suite_manifest": str(SUITE_MANIFEST.relative_to(ROOT)),
        },
        "completed_at": _iso_now(),
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    _write_report(summary)
    return summary


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
