# experiments/runners/maze_runner.py
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Any

from environments.maze1.env import GridMazeEnv
from agents.stoa.maze.stoa_agent_maze import bfs_path
from agents.stoa.maze.astar_maze import astar_path
from experiments.logging.logging import write_metric_line, write_budget_csv

# CO adapter + core builder
try:
    from agents.co.adapters.maze_adapter import COAdapterMaze
    from agents.co.integration.core_builder import build_co_core
    HAS_CO = True
except Exception:
    HAS_CO = False

DIRS = ["UP", "DOWN", "LEFT", "RIGHT"]

@dataclass
class MazeConfig:
    spec_path: Optional[str]
    episodes: int
    out: str
    agent: Dict[str, Any]

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
        env = data.get("env", {})
        out = data.get("out", "outputs/maze_bfs")
        agent = data.get("agent", {"type": args.agent.lower(), "params": {}})
        episodes = int(data.get("episodes", 5))
        spec_path = _resolve_spec_path(env.get("spec_path"), args.config)
        return MazeConfig(spec_path=spec_path, episodes=episodes, out=str(out),
                          agent=agent if isinstance(agent, dict) else {"type": str(agent).lower(), "params": {}})
    return MazeConfig(spec_path=args.maze, episodes=int(args.episodes), out=str(args.out),
                      agent={"type": args.agent.lower(), "params": {}})

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
    budget_path = out_dir / "budget.csv"
    plot_path = out_dir / "quick_plot.png"

    env = GridMazeEnv(spec_path=cfg.spec_path)

    agent_dict = dict(cfg.agent)
    atype = str(agent_dict.get("type", "bfs")).lower()
    aparams = dict(agent_dict.get("params", {}))
    aname = agent_dict.get("name")
    agent_tag = atype if not aname else f"{atype}:{aname}"

    budget_rows = []

    for ep in range(cfg.episodes):
        env.reset()

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

        elif atype == "co":
            if not HAS_CO:
                raise RuntimeError("agent=co requested but agents.co.adapters.maze_adapter is not importable")

            core = build_co_core(aparams)
            agent = COAdapterMaze(core=core, name=(aname or "CO_full"))

            if ep == 0:
                write_metric_line(metrics_path, {
                    "record_type": "header",
                    "runner": "maze",
                    "episodes": int(cfg.episodes),
                    "agent": agent_tag
                })

            steps = 0
            total_reward = 0.0
            done = False
            while not done:
                sel = None
                try:
                    sel = agent.select({"pos": env.pos, "episode": ep})  # type: ignore[attr-defined]
                except Exception:
                    pass
                if isinstance(sel, dict) and "action" in sel:
                    act = sel["action"]
                else:
                    act = DIRS[steps % 4]

                if act not in ("UP", "DOWN", "LEFT", "RIGHT"):
                    act = DIRS[steps % 4]

                _, r, done, _ = env.step(act)
                try:
                    agent.update({"observation": env.pos, "reward": r, "done": done})  # type: ignore[attr-defined]
                except Exception:
                    pass
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
        pass

if __name__ == "__main__":
    main()