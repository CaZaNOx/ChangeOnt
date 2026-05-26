# experiments/runners/maze_runner.py
from __future__ import annotations

import argparse, json, os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional, Any

from environments.maze1.env import GridMazeEnv, MazeSpec
from agents.stoa.maze.stoa_agent_maze import bfs_path
from agents.stoa.maze.astar_maze import astar_path
from agents.stoa.maze.replanning_visible_astar import visible_replanning_astar_action
from experiments.logging.logging import write_metric_line, write_budget_csv
from experiments.config_utils import normalize_agent_config, extract_env_spec

# CO adapter + core builder
try:
    from agents.co.adapters.maze_adapter import COAdapterMaze
    HAS_CO = True
except Exception as e:
    import traceback, sys
    print("[CO import error] agents.co.adapters.maze_adapter / core_builder", file=sys.stderr)
    traceback.print_exc()
    HAS_CO = False

try:
    from agents.co.integration.core_builder import build_co_core
    HAS_CORE = True
except Exception:
    HAS_CORE = False

DIRS = ["UP", "DOWN", "LEFT", "RIGHT"]

@dataclass
class MazeConfig:
    spec_path: Optional[str]
    env_params: Dict[str, Any]
    episodes: int
    out: str
    agent: Dict[str, Any]
    seed: int = 0
    mode: Optional[str] = None

def _parse_yaml(text: str) -> dict:
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text) or {}
    except Exception:
        return {}

def _resolve_spec_path(spec_path: Optional[str], config_path: Optional[str]) -> Optional[str]:
    if not spec_path:
        return None
    p = Path(spec_path)
    if p.is_absolute() and p.exists():
        return str(p)
    project_root = Path(__file__).resolve().parents[2]
    cand = (project_root / p).resolve()
    if cand.exists():
        return str(cand)
    if config_path:
        cand = (Path(config_path).parent / p).resolve()
        if cand.exists():
            return str(cand)
    return str(p)

def _load_config(args: argparse.Namespace) -> MazeConfig:
    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            data = json.load(f) if args.config.endswith(".json") else _parse_yaml(f.read())
        job = data.get("job", {}) if isinstance(data.get("job"), dict) else {}
        env = data.get("env", {}) if isinstance(data.get("env"), dict) else {}
        run = data.get("run", {}) if isinstance(data.get("run"), dict) else {}
        out = data.get("out", data.get("out_dir", job.get("out_dir", "outputs/maze_bfs")))
        agent = data.get("agent", {"type": args.agent.lower(), "params": {}})
        episodes = int(run.get("episodes", data.get("episodes", 5)))
        env_spec = extract_env_spec(env)
        spec_path = env_spec.get("spec_path", env.get("spec_path"))
        spec_path = _resolve_spec_path(spec_path, args.config)
        env_params = dict(env.get("params", {})) if isinstance(env.get("params"), dict) else {}
        agent = normalize_agent_config(agent, default_algo="bfs")

        return MazeConfig(
            spec_path=spec_path,
            env_params=env_params,
            episodes=episodes,
            out=str(out),
            agent=agent if isinstance(agent, dict) else {"type": str(agent).lower(), "params": {}},
            seed=int(data.get("seed", job.get("seed", env_params.get("seed", 0)))),
            mode=data.get("mode", job.get("mode")),
        )
    return MazeConfig(
        spec_path=args.maze, env_params={}, episodes=int(args.episodes), out=str(args.out),
        agent={"type": args.agent.lower(), "params": {}}, seed=0, mode=None
    )


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_run_manifest(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _strict_errors() -> bool:
    return str(os.environ.get("CO_STRICT_ERRORS", "")).strip() == "1"

def main() -> None:
    ap = argparse.ArgumentParser(description="Maze runner (BFS / A* / CO)")
    ap.add_argument("--config", type=str, default=None, help="YAML/JSON config file")
    ap.add_argument("--maze", type=str, default=None, help="spec.yaml path (fallback)")
    ap.add_argument("--episodes", type=int, default=5)
    ap.add_argument("--out", type=str, default="outputs/maze_bfs")
    ap.add_argument("--agent", type=str, default="bfs", help="bfs | astar | co (CLI fallback)")
    args = ap.parse_args()

    cfg = _load_config(args)
    out_dir = Path(cfg.out); out_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = out_dir / "metrics.jsonl"
    budget_path  = out_dir / "budget.csv"
    plot_path    = out_dir / "quick_plot.png"
    manifest_path = out_dir / "run_manifest.json"
    started_at = _iso_now()
    status = "failed"
    error: Optional[str] = None
    co_runtime_contract: Optional[Dict[str, Any]] = None

    for p in (metrics_path, budget_path):
        if p.exists():
            p.unlink()
    if plot_path.exists():
        plot_path.unlink()
    try:
        if cfg.spec_path:
            env = GridMazeEnv(spec_path=cfg.spec_path)
        else:
            env = GridMazeEnv(spec=MazeSpec.from_params(cfg.env_params or {"seed": cfg.seed}))


        agent_dict = dict(cfg.agent)
        atype  = str(agent_dict.get("type", "bfs")).lower()
        aparams = dict(agent_dict.get("params", {}))
        aname  = agent_dict.get("name")
        agent_tag = atype if not aname else f"{atype}:{aname}"

        write_metric_line(metrics_path, {
            "record_type": "header",
            "runner": "maze",
            "family": "maze",
            "mode": cfg.mode,
            "seed": int(cfg.seed),
            "episodes": int(cfg.episodes),
            "agent": agent_tag,
            "out_dir": str(out_dir),
            "co_runtime_contract": None,
        })

        budget_rows = []

        for ep in range(cfg.episodes):
            env.reset(seed=cfg.seed)

            if atype in ("bfs", "astar"):
                actions = bfs_path(env) if atype == "bfs" else astar_path(env)
                agent_tag_ep = atype

                steps = 0
                total_reward = 0.0
                for act in actions:
                    _, r, done, _ = env.step(act)
                    steps += 1
                    total_reward += r
                    if done:
                        break
                write_metric_line(metrics_path, {"metric": "episode_steps", "episode": ep, "value": steps})
                write_metric_line(metrics_path, {"metric": "episode_return", "episode": ep, "value": total_reward})
                budget_rows.append({"episode": ep, "flops_step": 1, "memory_bytes": 0, "agent": agent_tag_ep})

            elif atype in ("astar_visible", "astar_visible_penalty"):
                optimistic_unknown = bool(aparams.get("optimistic_unknown", True))
                unknown_penalty = float(aparams.get("unknown_penalty", 0.35 if atype == "astar_visible_penalty" else 0.0) or 0.0)
                steps = 0
                total_reward = 0.0
                done = False
                while not done:
                    obs0 = env.get_observation() if hasattr(env, "get_observation") else {
                        "pos": tuple(getattr(env, "pos", (0, 0))),
                        "goal": tuple(getattr(env, "goal", (0, 0))),
                        "grid": getattr(env, "grid", None),
                        "width": getattr(env, "W", None) or getattr(env, "width", None),
                        "height": getattr(env, "H", None) or getattr(env, "height", None),
                    }
                    act = visible_replanning_astar_action(obs0, optimistic_unknown=optimistic_unknown, unknown_penalty=unknown_penalty)
                    if act not in ("UP", "DOWN", "LEFT", "RIGHT"):
                        act = DIRS[steps % 4]
                    _, r, done, _ = env.step(act)
                    steps += 1
                    total_reward += r
                    if steps > 5000:
                        break
                write_metric_line(metrics_path, {"metric": "episode_steps", "episode": ep, "value": steps})
                write_metric_line(metrics_path, {"metric": "episode_return", "episode": ep, "value": total_reward})
                budget_rows.append({"episode": ep, "flops_step": 1, "memory_bytes": 0, "agent": atype})

            elif atype == "co":
                if not HAS_CO:
                    raise RuntimeError("agent=co requested but agents.co.adapters.maze_adapter is not importable")
                if not HAS_CORE:
                    raise RuntimeError("agent=co requested but agents.co.integration.core_builder is not importable")

                core = build_co_core(aparams)
                co_runtime_contract = core.export_runtime_contract()
                agent = COAdapterMaze(core=core, name=(aname or "CO_canonical_core"))
                if ep == 0:
                    write_metric_line(metrics_path, {
                        "record_type": "co_runtime_contract",
                        "family": "maze",
                        "agent": agent_tag,
                        "co_runtime_contract": co_runtime_contract,
                    })

                steps = 0
                total_reward = 0.0
                done = False

                while not done:
                    env_obs = env.get_observation() if hasattr(env, "get_observation") else {}
                    grid = env_obs.get("grid", getattr(env, "grid", None))
                    H = env_obs.get("height", getattr(env, "H", None) or getattr(env, "height", None))
                    W = env_obs.get("width", getattr(env, "W", None) or getattr(env, "width", None))
                    goal = env_obs.get("goal", getattr(env, "goal", None))
                    pos_tuple = tuple(env_obs.get("pos", getattr(env, "pos", (0, 0))))
                    goal_tuple = tuple(goal) if isinstance(goal, (list, tuple)) and len(goal) == 2 else None

                    if grid is not None:
                        try:
                            grid = [[int(v) for v in row] for row in grid]
                        except Exception:
                            grid = None

                    obs = {
                        "family": "maze",
                        "t": steps,
                        "episode": ep,
                        "pos": pos_tuple,
                        "goal": goal_tuple,
                        "grid": grid,
                        "width": W,
                        "height": H,
                        "partial_observability": bool(env_obs.get("partial_observability", False)),
                        "dynamic_walls": bool(env_obs.get("dynamic_walls", False)),
                        "wall_flip_prob": float(env_obs.get("wall_flip_prob", 0.0) or 0.0),
                        "view_radius": env_obs.get("view_radius", None),
                    }

                    sel = None
                    try:
                        sel = agent.select(obs)
                    except Exception:
                        if _strict_errors():
                            raise
                        sel = None

                    if isinstance(sel, dict) and "action" in sel:
                        act = sel["action"]
                    else:
                        act = sel

                    co_policy = (sel.get("co_policy") if isinstance(sel, dict) else None) or "n/a"
                    co_weight = float(sel.get("co_weight", 1.0)) if isinstance(sel, dict) else 1.0
                    signal_bus_votes = int(sel.get("signal_bus_votes", 0)) if isinstance(sel, dict) else 0
                    write_metric_line(
                        metrics_path,
                        {
                            "metric": "co_debug",
                            "episode": ep,
                            "t": steps,
                            "co_policy": co_policy,
                            "co_weight": co_weight,
                            "signal_bus_votes": signal_bus_votes,
                            "agent": agent_tag,
                            **({
                                k: sel[k] for k in (
                                    "birth_events","merge_events","split_events","bend_triggers",
                                    "birth_count","prototype_count","class_count","cap_hits",
                                    "last_d","identity_ok","ghvc_pressure","ghvc_mdl_gain",
                                    "debug_header_updates","translator_mask_mode",
                                    "translator_mask_blocked","translator_mask_size","translator_mask_blocks_all",
                                    "signals","header_update_count","header_update_source","mask_mode","translator_mask",

                                "canonical_commitment_mode","canonical_commitment_reason",
                                "certificate_aware_stable_continuation_applied",
                                "certificate_aware_reopen_or_sample_applied",
                                "candidate_final_scores","candidate_obs_scores",
                                "canonical_commitment_assessment",
                                "commit_readiness","evidence_margin","evidence_support",
                                "co_sources","co_evidence_valid_for_step",
                                ) if isinstance(sel, dict) and k in sel
                            }),
                        },
                    )

                    if act not in ("UP", "DOWN", "LEFT", "RIGHT"):
                        act = DIRS[steps % 4]
                    _, r, done, _ = env.step(act)

                    try:
                        agent.update({
                            "observation": tuple(env.pos),
                            "reward": r,
                            "done": done,
                            "action": act
                        })
                    except Exception:
                        if _strict_errors():
                            raise

                    steps += 1
                    total_reward += r
                    if steps > 5000:
                        break

                write_metric_line(metrics_path, {"metric": "episode_steps", "episode": ep, "value": steps})
                write_metric_line(metrics_path, {"metric": "episode_return", "episode": ep, "value": total_reward})
                budget_rows.append({"episode": ep, "flops_step": 1, "memory_bytes": 0, "agent": agent_tag})

            else:
                raise ValueError(f"unknown agent: {atype}")

        write_budget_csv(budget_path, budget_rows)

        try:
            from experiments.plotting.plotting import save_quick_plot
            save_quick_plot(metrics_path, plot_path, title=f"Maze {agent_tag.upper()}")
        except Exception:
            if _strict_errors():
                raise
        status = "succeeded"
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        _write_run_manifest(
            manifest_path,
            {
                "family": "maze",
                "mode": cfg.mode,
                "seed": int(cfg.seed),
                "agent_name": str(dict(cfg.agent).get("name") or str(dict(cfg.agent).get("type", ""))),
                "agent_type": str(dict(cfg.agent).get("type", "")),
                "environment_spec": {"spec_path": cfg.spec_path, "env_params": dict(cfg.env_params or {})},
                "runner": "experiments.runners.maze_runner",
                "out_dir": str(out_dir),
                "started_at": started_at,
                "ended_at": _iso_now(),
                "status": status,
                "error": error,
                "co_runtime_contract": co_runtime_contract,
            },
        )

if __name__ == "__main__":
    main()
