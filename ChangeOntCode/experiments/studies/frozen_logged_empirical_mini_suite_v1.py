from __future__ import annotations

"""Frozen logged empirical mini-suite v1.

This study is the first post-structural, post-formula-gate empirical smoke with
explicit public baselines.  It is intentionally small and frozen: the constants
and agents are loaded from the current structural baseline, the outputs are
logged as JSONL, and the report carries a hard claim boundary.  It is not a
benchmark, not tuning evidence, and not a novelty claim.
"""

import hashlib
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import yaml  # type: ignore

from experiments.studies._co_eval_common import load_co_manifest_params
from experiments.runners.maintenance_replacement_runner import run_episode as run_maintenance
from experiments.runners.latent_mechanism_runner import run as run_latent

OUT_DIR = ROOT / "outputs" / "frozen_logged_empirical_mini_suite_v1"
RUNS_JSONL = OUT_DIR / "runs.jsonl"
STRUCT_JSONL = OUT_DIR / "structural_telemetry.jsonl"
SUMMARY_JSON = OUT_DIR / "summary.json"
SUITE_MANIFEST = OUT_DIR / "suite_manifest.json"
REPORT_MD = ROOT.parent / "FROZEN_LOGGED_EMPIRICAL_MINI_SUITE_REPORT_2026-05-17.md"

CLAIM_BOUNDARY = (
    "Frozen logged empirical mini-suite only: checks execution, logging, explicit public baselines, "
    "and structural telemetry preservation. It is not benchmark evidence, not tuning evidence, "
    "not CO proof, and not an RCF novelty claim."
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
    rows: List[Dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


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
        t_val = raw.get("t", raw.get("episode", 0))
        try:
            t = int(t_val)
        except Exception:
            t = 0
        out = {"record_type": "co_structural_step" if raw.get("metric") == "co_debug" else "co_runtime_contract", "family": family, "run_id": run_id, "t": t}
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
        "pulls": pulls_rows[-1].get("pulls") if pulls_rows else None,
        "best_arm": pulls_rows[-1].get("best_arm") if pulls_rows else None,
    }


def _summarize_renewal_run(out_dir: Path) -> Dict[str, Any]:
    rows = _read_jsonl(out_dir / "metrics.jsonl")
    finals = [float(r["final_cum_reward"]) for r in rows if "final_cum_reward" in r]
    return {"metric_name": "final_cum_reward", "metric_value": float(finals[-1]) if finals else None}


def _summarize_maze_run(out_dir: Path) -> Dict[str, Any]:
    rows = _read_jsonl(out_dir / "metrics.jsonl")
    returns = [float(r["value"]) for r in rows if r.get("metric") == "episode_return"]
    steps = [float(r["value"]) for r in rows if r.get("metric") == "episode_steps"]
    return {
        "metric_name": "mean_episode_return",
        "metric_value": float(mean(returns)) if returns else None,
        "mean_episode_steps": float(mean(steps)) if steps else None,
        "episodes": len(returns),
    }


def _run_bandit(co_params: Mapping[str, Any]) -> List[Dict[str, Any]]:
    out_rows: List[Dict[str, Any]] = []
    probs = [0.10, 0.20, 0.80]
    horizon = 24
    for seed in [0]:
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
            summary = _summarize_bandit_run(out_dir)
            out_rows.append({
                "run_id": run_id,
                "family": "bandit",
                "mode": "easy",
                "seed": seed,
                "agent": tag,
                "baseline_type": "co" if agent["type"] == "co" else "stoa_public",
                "out_dir": str(out_dir.relative_to(ROOT)),
                **summary,
            })
            for srow in _extract_struct_from_metrics(out_dir / "metrics.jsonl", family="bandit", run_id=run_id):
                _append_jsonl(STRUCT_JSONL, srow)
    return out_rows


def _run_renewal(co_params: Mapping[str, Any]) -> List[Dict[str, Any]]:
    out_rows: List[Dict[str, Any]] = []
    env = {"A": 4, "L_win": 3, "p_ren": 0.02, "p_noise": 0.00, "T_max": 24}
    for seed in [0]:
        for agent in [
            {"type": "last", "params": {}},
            {"type": "phase", "params": {}},
            {"type": "vom", "params": {"max_order": 2}},
            {"type": "co", "name": "CO_canonical_core", "params": dict(co_params)},
        ]:
            tag = str(agent.get("name") or agent.get("type"))
            run_id = f"renewal_clean_{tag}_s{seed}"
            out_dir = OUT_DIR / "runs" / run_id
            cfg = _tmp_config(
                OUT_DIR / "configs" / f"{run_id}.json",
                {
                    "job": {"family": "renewal", "mode": "clean", "seed": seed, "out_dir": str(out_dir)},
                    "env": {"kind": "renewal", "params": env},
                    "agent": agent,
                    "run": {"steps": 24, "episodes": None, "horizon": None},
                    "logging": {"write_metrics": True, "write_budget": True, "write_plot": False},
                },
            )
            _run_module("experiments.runners.renewal_runner", cfg)
            summary = _summarize_renewal_run(out_dir)
            out_rows.append({
                "run_id": run_id,
                "family": "renewal",
                "mode": "clean",
                "seed": seed,
                "agent": tag,
                "baseline_type": "co" if agent["type"] == "co" else "stoa_public",
                "out_dir": str(out_dir.relative_to(ROOT)),
                **summary,
            })
            for srow in _extract_struct_from_metrics(out_dir / "metrics.jsonl", family="renewal", run_id=run_id):
                _append_jsonl(STRUCT_JSONL, srow)
    return out_rows


def _run_maze(co_params: Mapping[str, Any]) -> List[Dict[str, Any]]:
    """Run a tiny maze smoke directly with a hard step cap.

    The canonical maze runner allows long CO episodes because it is a general
    runner.  The frozen mini-suite instead uses a fixed cap so this remains a
    smoke/telemetry check rather than a performance study.
    """
    from environments.maze1.env import GridMazeEnv, MazeSpec
    from agents.stoa.maze.stoa_agent_maze import bfs_path
    from agents.stoa.maze.astar_maze import astar_path
    from agents.co.adapters.maze_adapter import COAdapterMaze
    from agents.co.integration.core_builder import build_co_core

    out_rows: List[Dict[str, Any]] = []
    max_steps = 24
    seed = 0
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
            if agent_name in {"bfs", "astar"}:
                action = path[steps] if steps < len(path) else "UP"
                selection: Dict[str, Any] = {}
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
                raise ValueError(f"maze mini-suite fail-closed: invalid action {action!r}")
            _, reward, done, info = env.step(action)
            total_reward += float(reward)
            row = {"t": steps, "action": action, "reward": float(reward), "done": bool(done), "pos": tuple(env.pos)}
            if selection:
                row["co_selection"] = selection
                _append_jsonl(STRUCT_JSONL, _extract_struct_from_selection(selection, family="maze", run_id=run_id, t=steps, action=action))
                try:
                    co_agent.update({"observation": tuple(env.pos), "reward": float(reward), "done": bool(done), "action": action})  # type: ignore[union-attr]
                except Exception:
                    raise
            trace_rows.append(row)
            steps += 1
        _write_jsonl(out_dir / "trace.jsonl", trace_rows)
        (out_dir / "summary.json").write_text(json.dumps({"total_reward": total_reward, "steps": steps, "done": done}, indent=2, sort_keys=True), encoding="utf-8")
        out_rows.append({
            "run_id": run_id,
            "family": "maze",
            "mode": "maze_5x5",
            "seed": seed,
            "agent": agent_name,
            "baseline_type": "co" if agent_name == "CO_canonical_core" else "stoa_public",
            "out_dir": str(out_dir.relative_to(ROOT)),
            "metric_name": "episode_return",
            "metric_value": float(total_reward),
            "steps": int(steps),
            "done": bool(done),
        })
    return out_rows


def _run_maintenance(co_params: Mapping[str, Any]) -> List[Dict[str, Any]]:
    out_rows: List[Dict[str, Any]] = []
    for regime in ["bandit_like", "middle"]:
        for seed in [0]:
            agents = ["random", "threshold", "co"]
            if regime == "bandit_like":
                agents.insert(2, "finite_horizon_dp")
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
                out_rows.append({
                    "run_id": run_id,
                    "family": "maintenance_replacement",
                    "mode": regime,
                    "seed": seed,
                    "agent": agent,
                    "baseline_type": "co" if agent == "co" else "public_baseline",
                    "out_dir": str(out_dir.relative_to(ROOT)),
                    "metric_name": "total_reward",
                    "metric_value": float(result.get("total_reward", 0.0)),
                    "steps": int(result.get("steps", 0)),
                    "observation_mode": result.get("observation_mode"),
                })
                if agent == "co":
                    for raw in _read_jsonl(out_dir / "trace.jsonl"):
                        sel = raw.get("co_selection", {}) if isinstance(raw.get("co_selection"), dict) else {}
                        if sel:
                            _append_jsonl(STRUCT_JSONL, _extract_struct_from_selection(sel, family="maintenance_replacement", run_id=run_id, t=int(raw.get("t", 0) or 0), action=raw.get("action")))
    return out_rows


def _run_latent(co_params: Mapping[str, Any]) -> List[Dict[str, Any]]:
    out_rows: List[Dict[str, Any]] = []
    for spec_name in ["easy_visible", "hidden_depth2"]:
        for seed in [0]:
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
                        "spec": {"name": spec_name, "params": {"seed": seed, "max_steps": 24}},
                        "agent": agent,
                        "log_every": 1,
                    },
                )
                result = run_latent(str(cfg))
                out_rows.append({
                    "run_id": run_id,
                    "family": "latent_mechanism",
                    "mode": spec_name,
                    "seed": seed,
                    "agent": tag,
                    "baseline_type": "co" if agent["type"] == "co" else "public_baseline",
                    "out_dir": str(out_dir.relative_to(ROOT)),
                    "metric_name": "success",
                    "metric_value": float(result.get("success", 0.0)),
                    "mean_reward": float(result.get("mean_reward", 0.0)),
                    "steps": int(result.get("steps", 0)),
                    "door_reframes": int(result.get("door_reframes", 0)),
                })
                if agent["type"] == "co":
                    for raw in _read_jsonl(out_dir / "metrics.jsonl"):
                        pass
                    dbg = out_dir / "co_debug_rows.json"
                    if dbg.exists():
                        try:
                            rows = json.loads(dbg.read_text(encoding="utf-8"))
                        except Exception:
                            rows = []
                        for s in rows:
                            _append_jsonl(STRUCT_JSONL, _extract_struct_from_selection(s, family="latent_mechanism", run_id=run_id, t=int(s.get("t", 0) or 0), action=s.get("action")))
    return out_rows


def _aggregate(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    grouped: Dict[Tuple[str, str, str], List[Dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["family"]), str(row["mode"]), str(row["agent"]))].append(row)
    out: Dict[str, Any] = {}
    for (family, mode, agent), vals in sorted(grouped.items()):
        key = f"{family}/{mode}/{agent}"
        nums = [float(v["metric_value"]) for v in vals if v.get("metric_value") is not None]
        out[key] = {
            "runs": len(vals),
            "metric_name": vals[0].get("metric_name") if vals else None,
            "mean_metric_value": float(mean(nums)) if nums else None,
            "values": nums,
        }
    return out


def _structural_summary() -> Dict[str, Any]:
    rows = _read_jsonl(STRUCT_JSONL)
    by_family = Counter(str(r.get("family")) for r in rows)
    modes = Counter(str(r.get("canonical_commitment_mode")) for r in rows if r.get("canonical_commitment_mode") is not None)
    no_struct = sum(1 for r in rows if r.get("record_type") == "co_structural_step" and not any(k in r for k in ("canonical_commitment_mode", "signal_bus_votes", "co_policy")))
    return {
        "records": len(rows),
        "records_by_family": dict(sorted(by_family.items())),
        "canonical_modes": dict(sorted(modes.items())),
        "structural_step_records_missing_basic_co_fields": int(no_struct),
    }


def _write_report(summary: Mapping[str, Any]) -> None:
    lines = [
        "# Frozen Logged Empirical Mini-Suite Report — 2026-05-17",
        "",
        "## Claim boundary",
        "",
        CLAIM_BOUNDARY,
        "",
        "## Scope",
        "",
        "This suite runs fixed small episodes/seeds across the active families with explicit public baselines and CO.",
        "It is the first frozen logged mini-suite after structural/formula gates, not a reward benchmark.",
        "",
        "## Outputs",
        "",
        f"- `ChangeOntCode/{RUNS_JSONL.relative_to(ROOT).as_posix()}`",
        f"- `ChangeOntCode/{STRUCT_JSONL.relative_to(ROOT).as_posix()}`",
        f"- `ChangeOntCode/{SUMMARY_JSON.relative_to(ROOT).as_posix()}`",
        f"- `ChangeOntCode/{SUITE_MANIFEST.relative_to(ROOT).as_posix()}`",
        "",
        "## Summary",
        "",
        "```json",
        json.dumps(summary, indent=2, sort_keys=True),
        "```",
        "",
        "## Interpretation boundary",
        "",
        "These numbers only show that the frozen runtime executes, logs, and can be compared against explicit public baselines without tuning. Broad empirical or novelty claims remain disallowed.",
    ]
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> Dict[str, Any]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for p in (RUNS_JSONL, STRUCT_JSONL, SUMMARY_JSON, SUITE_MANIFEST):
        if p.exists():
            p.unlink()
    co_params = _load_co_params()
    cfg_path = ROOT / "experiments" / "configs" / "co_agents" / "co_agents_canonical_core.yaml"
    formula_ledger = ROOT.parent / "FORMULA_COEFFICIENT_LEDGER_2026-05-16.md"
    baseline_freeze = ROOT.parent / "STRUCTURAL_BASELINE_FREEZE_2026-05-16.md"
    manifest = {
        "study": "frozen_logged_empirical_mini_suite_v1",
        "started_at": _iso_now(),
        "claim_boundary": CLAIM_BOUNDARY,
        "constants_frozen_before_run": True,
        "no_tuning_after_results": True,
        "co_manifest": str(cfg_path.relative_to(ROOT)),
        "co_manifest_sha256": _sha256(cfg_path),
        "formula_ledger": str(formula_ledger.relative_to(ROOT.parent)) if formula_ledger.exists() else None,
        "formula_ledger_sha256": _sha256(formula_ledger) if formula_ledger.exists() else None,
        "structural_baseline_freeze": str(baseline_freeze.relative_to(ROOT.parent)) if baseline_freeze.exists() else None,
        "structural_baseline_freeze_sha256": _sha256(baseline_freeze) if baseline_freeze.exists() else None,
        "families": {
            "bandit": {"baselines": ["ucb1", "kl_ucb"], "co": "CO_canonical_core"},
            "renewal": {"baselines": ["last", "phase", "vom"], "co": "CO_canonical_core"},
            "maze": {"baselines": ["bfs", "astar"], "co": "CO_canonical_core"},
            "maintenance_replacement": {"baselines": ["random", "threshold", "threshold_opt", "finite_horizon_dp_direct_only", "q_learning"], "co": "CO_canonical_core"},
            "latent_mechanism": {"baselines": ["random", "heuristic"], "co": "CO_canonical_core"},
        },
    }
    SUITE_MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    rows: List[Dict[str, Any]] = []
    rows.extend(_run_bandit(co_params))
    rows.extend(_run_renewal(co_params))
    rows.extend(_run_maze(co_params))
    rows.extend(_run_maintenance(co_params))
    rows.extend(_run_latent(co_params))
    _write_jsonl(RUNS_JSONL, rows)
    summary = {
        "study": "frozen_logged_empirical_mini_suite_v1",
        "claim_boundary": CLAIM_BOUNDARY,
        "runs": len(rows),
        "families": sorted(set(str(r["family"]) for r in rows)),
        "co_runs": sum(1 for r in rows if r.get("baseline_type") == "co"),
        "baseline_runs": sum(1 for r in rows if r.get("baseline_type") != "co"),
        "aggregate": _aggregate(rows),
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
