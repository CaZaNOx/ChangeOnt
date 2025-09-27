from __future__ import annotations
import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from environments.maze1.env import GridMazeEnv
from kernel.logging import write_metric_line, write_budget_csv

DIRS = ["UP", "DOWN", "LEFT", "RIGHT"]
DELTA = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}


@dataclass
class MazeConfig:
    spec_path: Optional[str]
    episodes: int
    out: str
    agent: Dict


def _parse_yaml(text: str) -> dict:
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text) or {}
    except Exception:
        return {}


def _load_config(args: argparse.Namespace) -> MazeConfig:
    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            data = json.load(f) if args.config.endswith(".json") else _parse_yaml(f.read())
        env = data.get("env", {})
        out = data.get("out", "outputs/maze_bfs")
        agent = data.get("agent", {"type": args.agent.lower(), "params": {}}) if args.agent else data.get("agent", {"type": "bfs", "params": {}})
        return MazeConfig(
            spec_path=env.get("spec_path"),
            episodes=int(data.get("episodes", 5)),
            out=str(out),
            agent=agent
        )
    # CLI fallbacks
    return MazeConfig(
        spec_path=args.maze,
        episodes=int(args.episodes),
        out=str(args.out),
        agent={"type": args.agent.lower(), "params": {}}
    )


def _bfs_path(env: GridMazeEnv) -> List[str]:
    """Return a shortest action sequence from start to goal using BFS on the grid graph."""
    start = env.start
    goal = env.goal
    from collections import deque
    q = deque([start])
    prev: Dict[Tuple[int, int], Tuple[int, int] | None] = {start: None}
    prev_act: Dict[Tuple[int, int], str | None] = {start: None}

    while q:
        r, c = q.popleft()
        if (r, c) == goal:
            break
        for act in DIRS:
            dr, dc = DELTA[act]
            nr, nc = r + dr, c + dc
            if not env.passable(nr, nc):
                continue
            if (nr, nc) in prev:
                continue
            prev[(nr, nc)] = (r, c)
            prev_act[(nr, nc)] = act
            q.append((nr, nc))

    # reconstruct
    if goal not in prev:
        return []  # no path
    path_actions: List[str] = []
    cur = goal
    while cur != start:
        act = prev_act[cur]
        assert act is not None
        path_actions.append(act)
        cur = prev[cur]  # type: ignore
        assert cur is not None
    path_actions.reverse()
    return path_actions


def main() -> None:
    ap = argparse.ArgumentParser(description="Maze runner (BFS or CO-HAQ)")
    ap.add_argument("--config", type=str, default=None, help="YAML/JSON config file")
    ap.add_argument("--maze", type=str, default=None, help="spec.yaml path (fallback)")
    ap.add_argument("--episodes", type=int, default=5)
    ap.add_argument("--out", type=str, default="outputs/maze_bfs")
    ap.add_argument("--agent", type=str, default="bfs", help="bfs | haq (CLI fallback)")
    args = ap.parse_args()

    cfg = _load_config(args)
    out_dir = Path(cfg.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = out_dir / "metrics.jsonl"
    budget_path = out_dir / "budget.csv"
    plot_path = out_dir / "quick_plot.png"

    env = GridMazeEnv(spec_path=cfg.spec_path)

    atype = str(cfg.agent.get("type", "bfs")).lower()
    aparams = dict(cfg.agent.get("params", {}))

    budget_rows = []
    for ep in range(cfg.episodes):
        env.reset()
        if atype == "bfs":
            actions = _bfs_path(env)
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
            budget_rows.append({"episode": ep, "flops_step": 1, "memory_bytes": 0, "agent": "bfs"})
        elif atype == "haq":
            # CO agent for maze
            try:
                from agents.co.agent_maze import HAQMazeCfg, HAQMazeAgent  # type: ignore
                try:
                    agent = HAQMazeAgent(HAQMazeCfg(**aparams))
                except Exception:
                    agent = HAQMazeAgent(HAQMazeCfg())
            except Exception:
                raise RuntimeError("agent=haq requested but agents.co.agent_maze is not importable")

            env.reset()
            steps = 0
            total_reward = 0.0
            # simple greedy with HAQ policy (select action each step)
            done = False
            while not done:
                act = agent.select()  # agent decides among DIRS internally or via internal policy
                if act not in ("UP", "DOWN", "LEFT", "RIGHT"):
                    # fallback: cycle dirs
                    act = DIRS[steps % 4]
                _, r, done, _ = env.step(act)
                agent.update(env.pos, r, done)  # pass obs-like + reward
                steps += 1
                total_reward += r
                if steps > 5000:  # safety bail to avoid infinite loop if bug
                    break
            write_metric_line(metrics_path, {"metric": "episode_steps", "episode": ep, "value": steps})
            write_metric_line(metrics_path, {"metric": "episode_return", "episode": ep, "value": total_reward})
            budget_rows.append({"episode": ep, "flops_step": 1, "memory_bytes": 0, "agent": "haq"})
        else:
            raise ValueError(f"unknown agent: {atype}")

    write_budget_csv(budget_path, budget_rows)

    # quick plot: steps per episode
    try:
        from kernel.plotting import save_quick_plot
        save_quick_plot(metrics_path, plot_path, title=f"Maze {atype.upper()}")
    except Exception:
        pass


if __name__ == "__main__":
    main()
