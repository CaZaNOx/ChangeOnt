from __future__ import annotations

"""Pass-1 all-current-problem CO vs STOA/baseline comparison v1.

Bounded, timeout-safe empirical comparison across the current active problem
families.  This is diagnostic evidence only.  It derives public six-question
shape reports from each adapter's public problem_contract, runs CO through the
same public runner/adapter route used by the repo, and compares against explicit
public baselines / STOA-style baselines where the repo currently has them.

Claim boundary:
- not proof of CO usefulness or novelty;
- not a tuning target;
- no post-result coefficient changes;
- baselines labelled with parity/oracle status;
- finite-horizon DP used only when public direct observation makes it parity-valid.
"""

import argparse
import json
import math
import os
import random
import subprocess
import sys
import time
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, pstdev
from types import SimpleNamespace
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "outputs" / "pass1_all_problem_stoa_comparison_v1"
RUNS_JSONL = OUT_DIR / "runs.jsonl"
SUMMARY_JSON = OUT_DIR / "summary.json"
SHAPES_JSON = OUT_DIR / "shape_reports.json"
REPORT_MD = ROOT.parent / "PASS1_ALL_PROBLEM_STOA_COMPARISON_REPORT_2026-05-25.md"

SEEDS = [0, 1, 2]
BANDIT_HORIZON = 128
RENEWAL_HORIZON = 128
MAZE_MAX_STEPS = 96
LATENT_MAX_STEPS = 64

STUDY = "pass1_all_problem_stoa_comparison_v1"
CLAIM_BOUNDARY = (
    "Pass-1 bounded diagnostic comparison only: current active problem families, "
    "small seed count, capped horizons, no post-result tuning, public baselines labelled. "
    "This is not proof of CO usefulness, not novelty evidence, and not publication-grade SOTA evidence."
)


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _json_safe(v: Any) -> Any:
    if isinstance(v, Mapping):
        return {str(k): _json_safe(val) for k, val in v.items()}
    if isinstance(v, (list, tuple)):
        return [_json_safe(x) for x in v]
    if isinstance(v, (str, int, float, bool)) or v is None:
        return v
    return str(v)


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_json_safe(payload), indent=2, sort_keys=True), encoding="utf-8")


def _append_jsonl(path: Path, row: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(_json_safe(row), sort_keys=True) + "\n")


def _read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _clear_outputs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for p in (RUNS_JSONL, SUMMARY_JSON, SHAPES_JSON):
        if p.exists():
            p.unlink()


def _load_co_params() -> Dict[str, Any]:
    from experiments.studies._co_eval_common import load_co_manifest_params
    return load_co_manifest_params(ROOT / "experiments" / "configs" / "co_agents" / "co_agents_canonical_core.yaml")


def _shape_from_contract(family: str, mode: str, contract: Mapping[str, Any]) -> Dict[str, Any]:
    from agents.co.placement.shape_prior6 import derive_shape_prior6, shape_prior6_to_direct_controls
    shape = derive_shape_prior6(dict(contract))
    controls = shape_prior6_to_direct_controls(shape)
    return {
        "family": family,
        "mode": mode,
        "problem_contract": dict(contract),
        "shape_prior6": shape,
        "direct_controls": controls,
    }


def _shape_reports() -> List[Dict[str, Any]]:
    """Derive shape reports through adapter public problem contracts."""
    reports: List[Dict[str, Any]] = []
    stub = SimpleNamespace(combinators={}, primitives={})

    from agents.co.adapters.bandit_adapter import COAdapterBandit
    from agents.co.adapters.renewal_adapter import COAdapterRenewal
    from agents.co.adapters.maze_adapter import COAdapterMaze
    from agents.co.adapters.latent_mechanism_adapter import COAdapterLatentMechanism
    from agents.co.adapters.maintenance_replacement_adapter import COAdapterMaintenanceReplacement
    from environments.maze1.env import GridMazeEnv, MazeSpec
    from environments.latent_mechanism.env import LatentMechanismDoorWorld, MechanismSpec
    from environments.maintenance_replacement.env import MaintenanceReplacementEnv
    from experiments.runners.maintenance_replacement_runner import spec_from_name

    b = COAdapterBandit(core=stub, n_arms=3)
    reports.append(_shape_from_contract("bandit", "easy_public_bandit", b._problem_contract({"family": "bandit", "t": 0, "n_arms": 3})))

    r = COAdapterRenewal(core=stub)
    reports.append(_shape_from_contract("renewal", "noisy_renewal", r._problem_contract({"family": "renewal", "obs": 0, "t": 0, "A": 4, "L_win": 3})))

    m = COAdapterMaze(core=stub)
    env_m = GridMazeEnv(spec=MazeSpec(width=5, height=5, seed=0, partial_observability=False, dynamic_walls=False))
    reports.append(_shape_from_contract("maze", "static_visible_5x5", m._problem_contract({"family": "maze", **env_m.get_observation()})))

    l = COAdapterLatentMechanism(core=stub)
    for spec_name, spec in [
        ("easy_visible", MechanismSpec.easy_visible(seed=0)),
        ("hidden_depth2", MechanismSpec.hidden_depth2(seed=0)),
    ]:
        env_l = LatentMechanismDoorWorld(spec=spec)
        obs, _, _, _ = env_l.reset(seed=0)
        reports.append(_shape_from_contract("latent_mechanism", spec_name, l._problem_contract({"family": "latent_mechanism", **obs})))

    maint = COAdapterMaintenanceReplacement(core=None)
    for regime in ("bandit_like", "middle", "renewal_like"):
        spec = spec_from_name(regime, 0)
        env = MaintenanceReplacementEnv(spec)
        obs, _, _, _ = env.reset(seed=0)
        reports.append(_shape_from_contract("maintenance_replacement", regime, maint._problem_contract(obs)))
    return reports


def _mean(xs: Sequence[float]) -> Optional[float]:
    return float(mean(xs)) if xs else None


def _std(xs: Sequence[float]) -> float:
    return float(pstdev(xs)) if len(xs) > 1 else 0.0


def _record_run(row: Mapping[str, Any]) -> Dict[str, Any]:
    out = dict(row)
    _append_jsonl(RUNS_JSONL, out)
    return out


def _run_bandit(co_params: Mapping[str, Any]) -> List[Dict[str, Any]]:
    from environments.bandit.bandit import BernoulliBanditEnv
    from agents.stoa.bandit.stoa_agent_bandit import UCB1Agent, EpsilonGreedyAgent
    from agents.stoa.bandit.ts import ThompsonSampling
    from agents.stoa.bandit.k1_ucb import KLUCB
    from agents.co.adapters.bandit_adapter import COAdapterBandit
    from experiments.studies._co_eval_common import build_validated_co_core, DEFAULT_CANONICAL_MANIFEST, DEFAULT_CANONICAL_AGENT_NAME, assert_valid_co_rollout

    probs = [0.10, 0.20, 0.80]
    agents = ["co", "ucb1", "kl_ucb", "ts", "epsgreedy"]
    rows: List[Dict[str, Any]] = []

    def make_agent(name: str, n: int, seed: int):
        if name == "ucb1":
            return UCB1Agent(n)
        if name == "kl_ucb":
            return KLUCB(n)
        if name == "ts":
            return ThompsonSampling(n)
        if name == "epsgreedy":
            return EpsilonGreedyAgent(n, epsilon=0.1, seed=seed)
        if name == "co":
            core = build_validated_co_core(dict(co_params), study_name=STUDY, manifest_path=DEFAULT_CANONICAL_MANIFEST, agent_name=DEFAULT_CANONICAL_AGENT_NAME)
            return COAdapterBandit(core=core, n_arms=n)
        raise ValueError(name)

    for seed in SEEDS:
        for agent_name in agents:
            t0 = time.perf_counter()
            env = BernoulliBanditEnv(probs, horizon=BANDIT_HORIZON)
            env.reset(seed=seed)
            agent = make_agent(agent_name, env.n_arms, seed)
            regret = 0.0
            total_reward = 0.0
            actions: List[int] = []
            votes: List[int] = []
            policies: List[str] = []
            best = max(probs)
            done = False
            t = 0
            while not done and t < BANDIT_HORIZON:
                if agent_name == "co":
                    sel = agent.select({"family": "bandit", "t": t, "n_arms": env.n_arms})
                    act = int(sel.get("action", 0)) if isinstance(sel, dict) else int(sel or 0)
                    if isinstance(sel, dict):
                        votes.append(int(sel.get("signal_bus_votes", 0) or 0))
                        policies.append(str(sel.get("co_policy", "bandit:safe_default")))
                else:
                    if hasattr(agent, "select"):
                        act = int(agent.select())
                    elif hasattr(agent, "act"):
                        act = int(agent.act())
                    else:
                        raise RuntimeError(agent_name)
                _, r, done, _ = env.step(act)
                total_reward += float(r)
                regret += max(0.0, best - probs[act])
                actions.append(int(act))
                if agent_name == "co":
                    agent.update({"action": act, "reward": float(r), "done": bool(done)})
                else:
                    try:
                        agent.update(act, r)
                    except TypeError:
                        try:
                            agent.update(r)
                        except Exception:
                            pass
                t += 1
            if agent_name == "co":
                assert_valid_co_rollout(study_name=STUDY, signal_bus_votes=votes, co_policies=policies)
            rows.append(_record_run({
                "family": "bandit", "mode": "easy_public_bandit", "seed": seed, "agent": agent_name,
                "baseline_type": "co" if agent_name == "co" else "public_stoa_baseline",
                "metric_name": "final_cumulative_regret", "metric_value": float(regret), "metric_direction": "lower_is_better",
                "secondary_metric": {"total_reward": float(total_reward)},
                "horizon": BANDIT_HORIZON, "first_actions": actions[:20], "runtime_seconds": time.perf_counter() - t0,
            }))
    return rows


def _run_renewal(co_params: Mapping[str, Any]) -> List[Dict[str, Any]]:
    from environments.renewal.env import CodebookRenewalEnvW, EnvCfg
    from agents.stoa.renewal.agent_fsm import LastFSM, PhaseFSM, NGramFSM
    from agents.stoa.renewal.vo_markov import VOKT
    from agents.co.adapters.renewal_adapter import COAdapterRenewal
    from experiments.studies._co_eval_common import build_validated_co_core, DEFAULT_CANONICAL_MANIFEST, DEFAULT_CANONICAL_AGENT_NAME

    env_params = {"A": 4, "L_win": 3, "p_ren": 0.04, "p_noise": 0.02, "T_max": RENEWAL_HORIZON}
    agents = ["co", "last", "phase", "ngram", "vom"]
    rows: List[Dict[str, Any]] = []

    def make_agent(name: str, A: int, L: int):
        if name == "last":
            return LastFSM(A)
        if name == "phase":
            return PhaseFSM(A=A, L_win=L)
        if name == "ngram":
            return NGramFSM(A=A, k=max(0, L - 1))
        if name == "vom":
            return VOKT(A=A, max_order=max(0, L - 1))
        if name == "co":
            core = build_validated_co_core(dict(co_params), study_name=STUDY, manifest_path=DEFAULT_CANONICAL_MANIFEST, agent_name=DEFAULT_CANONICAL_AGENT_NAME)
            return COAdapterRenewal(core=core)
        raise ValueError(name)

    A, L = int(env_params["A"]), int(env_params["L_win"])
    for seed in SEEDS:
        for agent_name in agents:
            t0 = time.perf_counter()
            env = CodebookRenewalEnvW(EnvCfg(**env_params), seed=seed)
            obs, _, done, _ = env.reset()
            agent = make_agent(agent_name, A, L)
            if agent_name != "co" and hasattr(agent, "reset"):
                agent.reset(int(obs))
            rewards: List[float] = []
            actions: List[int] = []
            t = 0
            while not done and t < RENEWAL_HORIZON:
                if agent_name == "co":
                    sel = agent.select({"family": "renewal", "obs": int(obs), "t": t, "A": A, "L_win": L})
                    act = int(sel.get("action", 0)) if isinstance(sel, dict) else int(sel or 0)
                else:
                    act = int(agent.act(int(obs)))
                obs, r, done, _ = env.step(act)
                if agent_name == "co":
                    agent.update({"observation": int(obs), "reward": float(r), "done": bool(done), "action": act})
                rewards.append(float(r)); actions.append(int(act)); t += 1
            rows.append(_record_run({
                "family": "renewal", "mode": "noisy_renewal", "seed": seed, "agent": agent_name,
                "baseline_type": "co" if agent_name == "co" else "public_stoa_baseline",
                "metric_name": "mean_reward", "metric_value": float(sum(rewards) / float(len(rewards) or 1)), "metric_direction": "higher_is_better",
                "secondary_metric": {"total_reward": float(sum(rewards))},
                "horizon": RENEWAL_HORIZON, "first_actions": actions[:25], "runtime_seconds": time.perf_counter() - t0,
            }))
    return rows


def _run_maze(co_params: Mapping[str, Any]) -> List[Dict[str, Any]]:
    from environments.maze1.env import GridMazeEnv, MazeSpec
    from agents.stoa.maze.stoa_agent_maze import bfs_path
    from agents.stoa.maze.astar_maze import astar_path
    from agents.stoa.maze.replanning_visible_astar import visible_replanning_astar_action
    from agents.co.adapters.maze_adapter import COAdapterMaze
    from experiments.studies._co_eval_common import build_validated_co_core, DEFAULT_CANONICAL_MANIFEST, DEFAULT_CANONICAL_AGENT_NAME

    agents = ["co", "bfs_full_grid", "astar_full_grid", "visible_replanning_astar"]
    rows: List[Dict[str, Any]] = []
    for seed in SEEDS:
        for agent_name in agents:
            t0 = time.perf_counter()
            spec = MazeSpec(width=5, height=5, seed=seed, partial_observability=False, dynamic_walls=False)
            env = GridMazeEnv(spec=spec)
            env.reset(seed=seed)
            total_reward = 0.0
            actions: List[str] = []
            done = False
            steps = 0
            if agent_name == "bfs_full_grid":
                planned = bfs_path(env)
            elif agent_name == "astar_full_grid":
                planned = astar_path(env)
            else:
                planned = []
            co_agent = None
            if agent_name == "co":
                core = build_validated_co_core(dict(co_params), study_name=STUDY, manifest_path=DEFAULT_CANONICAL_MANIFEST, agent_name=DEFAULT_CANONICAL_AGENT_NAME)
                co_agent = COAdapterMaze(core=core, name="CO_canonical_core")
            while not done and steps < MAZE_MAX_STEPS:
                if agent_name in {"bfs_full_grid", "astar_full_grid"}:
                    act = planned[steps] if steps < len(planned) else "UP"
                elif agent_name == "visible_replanning_astar":
                    act = visible_replanning_astar_action(env.get_observation(), optimistic_unknown=True, unknown_penalty=0.0) or "UP"
                else:
                    obs = {"family": "maze", "t": steps, "episode": 0, **env.get_observation()}
                    sel = co_agent.select(obs)  # type: ignore[union-attr]
                    act = str(sel.get("action", "")) if isinstance(sel, dict) else str(sel)
                if act not in ("UP", "DOWN", "LEFT", "RIGHT"):
                    raise ValueError(f"maze comparison fail-closed: invalid action {act!r}")
                _, r, done, _ = env.step(act)
                total_reward += float(r)
                actions.append(str(act))
                if agent_name == "co":
                    co_agent.update({"observation": tuple(env.pos), "reward": float(r), "done": bool(done), "action": act})  # type: ignore[union-attr]
                steps += 1
            rows.append(_record_run({
                "family": "maze", "mode": "static_visible_5x5", "seed": seed, "agent": agent_name,
                "baseline_type": "co" if agent_name == "co" else "public_planner_baseline",
                "metric_name": "episode_return", "metric_value": float(total_reward), "metric_direction": "higher_is_better",
                "secondary_metric": {"solved": bool(env.pos == env.goal), "steps": int(steps)},
                "horizon": MAZE_MAX_STEPS, "first_actions": actions[:25], "runtime_seconds": time.perf_counter() - t0,
            }))
    return rows


def _tmp_config(path: Path, payload: Mapping[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_json_safe(payload), indent=2, sort_keys=True), encoding="utf-8")
    return str(path)


def _run_latent(co_params: Mapping[str, Any]) -> List[Dict[str, Any]]:
    from experiments.runners.latent_mechanism_runner import run as run_latent
    rows: List[Dict[str, Any]] = []
    for spec_name in ["easy_visible", "hidden_depth2"]:
        for seed in SEEDS:
            for agent in [
                {"type": "co", "name": "CO_canonical_core", "params": dict(co_params)},
                {"type": "heuristic", "params": {}},
                {"type": "random", "params": {}},
            ]:
                t0 = time.perf_counter()
                tag = str(agent.get("name") or agent.get("type"))
                cfg = _tmp_config(OUT_DIR / "configs" / f"latent_{spec_name}_{tag}_s{seed}.json", {
                    "seed": seed,
                    "out_dir": str(OUT_DIR / "raw_runs" / f"latent_{spec_name}_{tag}_s{seed}"),
                    "spec": {"name": spec_name, "params": {"seed": seed, "max_steps": LATENT_MAX_STEPS}},
                    "agent": agent,
                    "log_every": 1,
                })
                result = run_latent(cfg)
                rows.append(_record_run({
                    "family": "latent_mechanism", "mode": spec_name, "seed": seed, "agent": tag,
                    "baseline_type": "co" if agent["type"] == "co" else "public_baseline",
                    "metric_name": "success", "metric_value": float(result.get("success", 0.0)), "metric_direction": "higher_is_better",
                    "secondary_metric": {"mean_reward": float(result.get("mean_reward", 0.0)), "steps": int(result.get("steps", 0)), "door_reframes": int(result.get("door_reframes", 0))},
                    "horizon": LATENT_MAX_STEPS, "runtime_seconds": time.perf_counter() - t0,
                }))
    return rows


def _run_maintenance(co_params: Mapping[str, Any]) -> List[Dict[str, Any]]:
    from experiments.runners.maintenance_replacement_runner import run_episode, spec_from_name
    rows: List[Dict[str, Any]] = []
    agents = ["co", "random", "threshold", "threshold_opt", "q_learning", "finite_horizon_dp"]
    for regime in ["bandit_like", "middle", "renewal_like"]:
        spec = spec_from_name(regime, 0)
        for seed in SEEDS:
            for agent in agents:
                if agent == "finite_horizon_dp" and str(spec.observe_health) != "direct":
                    _record_run({
                        "family": "maintenance_replacement", "mode": regime, "seed": seed, "agent": agent,
                        "baseline_type": "public_known_model_baseline_skipped", "skipped": True,
                        "skip_reason": "finite_horizon_dp parity-valid only for direct public health observation",
                    })
                    continue
                t0 = time.perf_counter()
                result = run_episode(
                    regime=regime,
                    agent_kind=agent,
                    seed=seed,
                    out_dir=str(OUT_DIR / "raw_runs" / f"maintenance_{regime}_{agent}_s{seed}"),
                    co_params=dict(co_params) if agent == "co" else None,
                )
                rows.append(_record_run({
                    "family": "maintenance_replacement", "mode": regime, "seed": seed, "agent": agent,
                    "baseline_type": "co" if agent == "co" else ("public_known_model_baseline" if agent == "finite_horizon_dp" else "public_baseline"),
                    "metric_name": "total_reward", "metric_value": float(result.get("total_reward", 0.0)), "metric_direction": "higher_is_better",
                    "secondary_metric": {"steps": int(result.get("steps", 0)), "observation_mode": result.get("observation_mode"), "final_health_true": result.get("final_health_true")},
                    "horizon": int(result.get("horizon", 0)), "runtime_seconds": time.perf_counter() - t0,
                }))
    return rows


def _aggregate(rows: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    grouped: Dict[Tuple[str, str, str], List[Dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row.get("skipped") or row.get("error"):
            continue
        grouped[(str(row["family"]), str(row["mode"]), str(row["agent"]))].append(row)

    aggregates: Dict[str, Any] = {}
    for (family, mode, agent), vals in sorted(grouped.items()):
        nums = [float(v["metric_value"]) for v in vals if v.get("metric_value") is not None]
        aggregates[f"{family}/{mode}/{agent}"] = {
            "family": family, "mode": mode, "agent": agent,
            "runs": len(vals),
            "metric_name": vals[0].get("metric_name"),
            "metric_direction": vals[0].get("metric_direction"),
            "mean_metric_value": _mean(nums),
            "std_population": _std(nums),
            "values": nums,
            "baseline_type": vals[0].get("baseline_type"),
            "mean_runtime_seconds": _mean([float(v.get("runtime_seconds", 0.0) or 0.0) for v in vals]),
        }

    by_mode: Dict[Tuple[str, str], List[Dict[str, Any]]] = defaultdict(list)
    for key, val in aggregates.items():
        by_mode[(str(val["family"]), str(val["mode"]))].append(val)

    comparisons: Dict[str, Any] = {}
    for (family, mode), vals in sorted(by_mode.items()):
        co_vals = [v for v in vals if v["agent"] in {"co", "CO_canonical_core"}]
        if not co_vals:
            continue
        co = co_vals[0]
        direction = str(co.get("metric_direction"))
        baselines = [v for v in vals if v["agent"] not in {"co", "CO_canonical_core"}]
        if not baselines:
            continue
        if direction == "lower_is_better":
            best = min(baselines, key=lambda v: float(v["mean_metric_value"]))
            delta = float(co["mean_metric_value"]) - float(best["mean_metric_value"])
            favorable = delta <= 0.0
        else:
            best = max(baselines, key=lambda v: float(v["mean_metric_value"]))
            delta = float(co["mean_metric_value"]) - float(best["mean_metric_value"])
            favorable = delta >= 0.0
        comparisons[f"{family}/{mode}"] = {
            "metric_name": co.get("metric_name"),
            "metric_direction": direction,
            "co_mean": co.get("mean_metric_value"),
            "best_baseline_agent": best.get("agent"),
            "best_baseline_mean": best.get("mean_metric_value"),
            "co_minus_best_baseline": float(delta),
            "co_favorable_vs_best_baseline": bool(favorable),
            "claim_boundary": "small-N bounded diagnostic only; do not tune constants from this comparison",
        }
    return aggregates, comparisons


def _write_report(summary: Mapping[str, Any]) -> None:
    comp = summary.get("co_vs_best_baseline", {})
    lines = [
        "# Pass-1 All-Problem CO vs STOA/Baseline Comparison — 2026-05-25",
        "",
        "## Claim boundary",
        "",
        CLAIM_BOUNDARY,
        "",
        "## Procedure",
        "",
        "- Derived six-question shape reports from each adapter's public `problem_contract` before scoring results.",
        "- Ran CO through the canonical current kernel manifest.",
        "- Ran explicit repo-available public baselines/STOA-style baselines per active family/mode.",
        "- Used small seed count and capped horizons to avoid timeouts; this is diagnostic, not publication-grade evidence.",
        "- Finite-horizon DP is skipped outside direct public health observation to avoid hidden-state oracle leakage.",
        "",
        "## CO vs best public baseline summary",
        "",
        "| family/mode | metric | direction | CO mean | best baseline | best mean | CO-best | favorable? |",
        "|---|---:|---|---:|---|---:|---:|---|",
    ]
    for key, val in sorted(comp.items()):
        lines.append(
            f"| {key} | {val.get('metric_name')} | {val.get('metric_direction')} | "
            f"{float(val.get('co_mean')):.4f} | {val.get('best_baseline_agent')} | "
            f"{float(val.get('best_baseline_mean')):.4f} | {float(val.get('co_minus_best_baseline')):.4f} | "
            f"{val.get('co_favorable_vs_best_baseline')} |"
        )
    lines += [
        "",
        "## Interpretation",
        "",
        "This comparison is a first bounded pass over current active problem families. It should be used to identify failure modes and where CO is or is not competitive under the current rough kernel. It must not be used to tune coefficients or claim proof of CO.",
        "",
        "## Full JSON summary",
        "",
        "```json",
        json.dumps(_json_safe(summary), indent=2, sort_keys=True),
        "```",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")



def _finalize_summary(*, status: str = "executed") -> Dict[str, Any]:
    raw_rows = _read_jsonl(RUNS_JSONL)
    perf_rows = [r for r in raw_rows if not r.get("skipped") and not r.get("error") and "metric_value" in r]
    aggregates, comparisons = _aggregate(perf_rows)
    shape_count = 0
    if SHAPES_JSON.exists():
        try:
            shape_count = len(json.loads(SHAPES_JSON.read_text(encoding="utf-8")).get("shape_reports", []))
        except Exception:
            shape_count = 0
    summary = {
        "study": STUDY,
        "status": status,
        "claim_boundary": CLAIM_BOUNDARY,
        "started_at": "family-by-family subprocess execution; see row runtime_seconds",
        "completed_at": _iso_now(),
        "seeds": SEEDS,
        "bounded_run_settings": {
            "bandit_horizon": BANDIT_HORIZON,
            "renewal_horizon": RENEWAL_HORIZON,
            "maze_max_steps": MAZE_MAX_STEPS,
            "latent_max_steps": LATENT_MAX_STEPS,
            "maintenance_native_horizons": "regime defaults: 60/80/100",
        },
        "raw_rows": len(raw_rows),
        "performance_rows": len(perf_rows),
        "skipped_rows": sum(1 for r in raw_rows if r.get("skipped")),
        "errors": [r for r in raw_rows if r.get("error")],
        "shape_report_count": shape_count,
        "families": sorted(set(str(r.get("family")) for r in perf_rows if r.get("family"))),
        "modes": sorted(set(f"{r.get('family')}/{r.get('mode')}" for r in perf_rows if r.get("family"))),
        "aggregates": aggregates,
        "co_vs_best_baseline": comparisons,
        "outputs": {
            "runs_jsonl": str(RUNS_JSONL.relative_to(ROOT)),
            "summary_json": str(SUMMARY_JSON.relative_to(ROOT)),
            "shape_reports_json": str(SHAPES_JSON.relative_to(ROOT)),
            "report_md": str(REPORT_MD.relative_to(ROOT.parent)),
        },
        "execution_note": (
            "Default execution uses one subprocess per family to avoid timeout/state accumulation in this environment. "
            "The same family run functions are used; results are appended to one JSONL file and aggregated after all families complete."
        ),
        "non_claims": [
            "Not a publication-grade SOTA suite.",
            "Not broad empirical proof.",
            "Do not tune constants from this result.",
            "Some baselines are strong public baselines, some are simple public heuristics; labels must be preserved.",
        ],
    }
    _write_json(SUMMARY_JSON, summary)
    _write_report(summary)
    return summary


def _run_family_by_name(name: str) -> List[Dict[str, Any]]:
    co_params = _load_co_params()
    if name == "bandit":
        return _run_bandit(co_params)
    if name == "renewal":
        return _run_renewal(co_params)
    if name == "maze":
        return _run_maze(co_params)
    if name == "latent":
        return _run_latent(co_params)
    if name == "maintenance":
        return _run_maintenance(co_params)
    raise ValueError(name)


def main(argv: Optional[Sequence[str]] = None) -> Dict[str, Any]:
    ap = argparse.ArgumentParser(description="Pass-1 all-current-problem CO vs STOA/baseline comparison")
    ap.add_argument("--family", choices=["bandit", "renewal", "maze", "latent", "maintenance"], default=None)
    ap.add_argument("--finalize-only", action="store_true")
    ap.add_argument("--init-only", action="store_true")
    args = ap.parse_args(list(argv) if argv is not None else None)

    if args.init_only:
        _clear_outputs()
        shapes = _shape_reports()
        _write_json(SHAPES_JSON, {"study": STUDY, "shape_reports": shapes})
        print(json.dumps({"initialized": True, "shape_reports": len(shapes)}, indent=2, sort_keys=True))
        return {"initialized": True, "shape_reports": len(shapes)}

    if args.family:
        rows = _run_family_by_name(args.family)
        print(json.dumps({"family": args.family, "rows": len(rows)}, indent=2, sort_keys=True))
        return {"family": args.family, "rows": len(rows)}

    if args.finalize_only:
        summary = _finalize_summary(status="executed_family_by_family_timeout_safe")
        print(json.dumps(_json_safe({"status": summary["status"], "rows": summary["raw_rows"], "summary": str(SUMMARY_JSON)}), indent=2, sort_keys=True))
        return summary

    # Default: timeout-safe orchestration via one subprocess per family.  This avoids
    # state accumulation that has previously made a single long Python process slow
    # or time out in this environment.
    _clear_outputs()
    shapes = _shape_reports()
    _write_json(SHAPES_JSON, {"study": STUDY, "shape_reports": shapes})
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT) + (os.pathsep + env.get("PYTHONPATH", "") if env.get("PYTHONPATH") else "")
    for fam in ("bandit", "renewal", "maze", "latent", "maintenance"):
        subprocess.run([sys.executable, "-m", "experiments.studies.pass1_all_problem_stoa_comparison_v1", "--family", fam], cwd=str(ROOT), env=env, check=True)
    summary = _finalize_summary(status="executed_family_by_family_timeout_safe")
    print(json.dumps(_json_safe({"status": summary["status"], "rows": summary["raw_rows"], "summary": str(SUMMARY_JSON)}), indent=2, sort_keys=True))
    return summary


if __name__ == "__main__":
    main()
