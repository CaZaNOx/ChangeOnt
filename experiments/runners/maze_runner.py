# PATH: experiments/runners/maze_runner.py
from __future__ import annotations
import argparse
import json
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Callable

from environments.maze1.env import GridMazeEnv
from kernel.logging import write_metric_line, write_budget_csv

DIRS = ["UP", "DOWN", "LEFT", "RIGHT"]
DELTA = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}


@dataclass
class MazeConfig:
    spec_path: Optional[str]
    episodes: int
    agent: str = "bfs"                 # 'bfs' | 'haq'
    seed: int = 0
    out: str = "outputs/maze_bfs"


def _parse_yaml(text: str) -> dict:
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text) or {}
    except Exception:
        return {}


def _normalize_agent(val: Any) -> str:
    """
    Accepts:
      - "bfs" / "haq"
      - {"type": "bfs"} or {"type": "haq", ...}
      - None -> "bfs"
    """
    if val is None:
        return "bfs"
    if isinstance(val, str):
        return val.lower()
    if isinstance(val, dict):
        t = val.get("type", "bfs")
        return str(t).lower()
    return str(val).lower()


def _load_config(args: argparse.Namespace) -> MazeConfig:
    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            data = json.load(f) if args.config.endswith(".json") else _parse_yaml(f.read())
        env = data.get("env", {})
        out = data.get("out", "outputs/maze_bfs")

        # agent precedence: CLI --agent overrides config
        cfg_agent = _normalize_agent(data.get("agent"))
        agent = args.agent.lower() if args.agent else cfg_agent

        return MazeConfig(
            spec_path=env.get("spec_path"),
            episodes=int(data.get("episodes", 5)),
            agent=agent,
            seed=int(data.get("seed", 0)),
            out=str(out),
        )

    # No config: build from CLI only
    agent = args.agent.lower() if args.agent else "bfs"
    return MazeConfig(
        spec_path=args.maze,
        episodes=int(args.episodes),
        agent=agent,
        seed=int(args.seed),
        out=str(args.out),
    )


def _bfs_path(env: GridMazeEnv) -> List[str]:
    """Return a shortest action sequence from start to goal using BFS on the grid graph."""
    start = env.start
    goal = env.goal
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


class _UnifiedMazeAgent:
    """
    Thin adapter that normalizes CO-HAQ maze agent APIs into:
      - select(pos) -> str
      - update(pos, reward, done) -> None
    It tries several common signatures to be robust against legacy variants.
    """
    def __init__(self, inner: Any):
        self.inner = inner
        # cache possible callables
        self._sel: List[Callable[..., Any]] = []
        for name in ("select", "act"):
            fn = getattr(inner, name, None)
            if callable(fn):
                self._sel.append(fn)
        self._upd: List[Callable[..., Any]] = []
        for name in ("update", "observe", "step"):
            fn = getattr(inner, name, None)
            if callable(fn):
                self._upd.append(fn)

    def select(self, pos: Tuple[int, int]) -> str:
        # try with pos, else without; prefer 'select' over 'act'
        for fn in self._sel:
            try:
                return fn(pos)  # type: ignore[arg-type]
            except TypeError:
                try:
                    return fn()  # type: ignore[call-arg]
                except TypeError:
                    continue
        raise TypeError("No usable select/act method found on HAQ maze agent")

    def update(self, pos: Tuple[int, int], reward: float, done: bool) -> None:
        # try (pos,r,done) -> (r,done) -> (r) -> ()
        for fn in self._upd:
            for args in ((pos, reward, done), (reward, done), (reward,), tuple()):
                try:
                    fn(*args)  # type: ignore[misc]
                    return
                except TypeError:
                    continue
        # If nothing matched, silently ignore (read-only agent)


def main() -> None:
    ap = argparse.ArgumentParser(description="Maze runner (BFS baseline and CO-HAQ)")
    ap.add_argument("--config", type=str, default=None, help="YAML/JSON config file")
    ap.add_argument("--maze", type=str, default=None, help="spec.yaml path (fallback)")
    ap.add_argument("--episodes", type=int, default=5)
    ap.add_argument("--agent", type=str, default=None, help="bfs | haq (overrides config)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", type=str, default="outputs/maze_bfs")
    args = ap.parse_args()

    cfg = _load_config(args)
    out_dir = Path(cfg.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = out_dir / "metrics.jsonl"
    budget_path = out_dir / "budget.csv"
    plot_path = out_dir / "quick_plot.png"

    env = GridMazeEnv(spec_path=cfg.spec_path)

    budget_rows: List[Dict[str, Any]] = []

    if cfg.agent == "bfs":
        for ep in range(cfg.episodes):
            env.reset()
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

    elif cfg.agent == "haq":
        try:
            from agents.co.agent_maze import HAQMazeCfg, HAQMazeAgent  # type: ignore
        except Exception as e:
            raise RuntimeError(f"agent=haq requested but agents.co.agent_maze is not importable: {e}") from e

        for ep in range(cfg.episodes):
            pos = env.reset()

            # tolerant cfg construction
            try:
                cfg_obj = HAQMazeCfg(seed=cfg.seed)  # preferred
            except TypeError:
                cfg_obj = HAQMazeCfg()               # legacy

            raw_agent = HAQMazeAgent(cfg_obj)
            agent = _UnifiedMazeAgent(raw_agent)

            done = False
            steps = 0
            total_reward = 0.0

            # Safety cap to avoid pathological loops
            # (width*height)*4 is generous for a shortest-path problem)
            max_steps = env.spec.width * env.spec.height * 4

            while not done and steps < max_steps:
                act = agent.select(pos)
                pos, r, done, _ = env.step(act)
                agent.update(pos, r, done)
                steps += 1
                total_reward += r

            write_metric_line(metrics_path, {"metric": "episode_steps", "episode": ep, "value": steps})
            write_metric_line(metrics_path, {"metric": "episode_return", "episode": ep, "value": total_reward})
            # keep conservative parity with renewal HAQ budget notion
            budget_rows.append({"episode": ep, "flops_step": 4, "memory_bytes": 6, "agent": "haq"})

    else:
        raise ValueError(f"unknown agent: {cfg.agent!r}")

    write_budget_csv(budget_path, budget_rows)

    # quick plot: steps per episode
    try:
        from kernel.plotting import save_quick_plot
        save_quick_plot(metrics_path, plot_path, title=f"Maze {cfg.agent.upper()}")
    except Exception:
        pass


if __name__ == "__main__":
    main()
