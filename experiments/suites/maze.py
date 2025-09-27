# experiments/suites/maze.py
from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
from .common import run_module, tmp_yaml, ensure_dir
from experiments.eval.maze import evaluate_run, summarize

def run_family(root: Path, spec: Dict[str, Any]) -> None:
    out_dir = root / "maze"
    ensure_dir(out_dir)
    rows: List[Dict[str, Any]] = []

    envs: Dict[str, Any] = spec.get("envs", {})
    agents: List[str] = list(spec.get("agents", ["bfs"]))

    for env_name, env_cfg in envs.items():
        episodes = int(env_cfg.get("episodes", 5))
        for agent in agents:
            run_dir = out_dir / env_name / f"{agent}"
            cfg = {
                "episodes": episodes,
                "agent": {"type": agent},
                "out": str(run_dir),
                "env": {"spec_path": env_cfg.get("spec_path")},
            }
            tmp = tmp_yaml(cfg, run_dir / "_tmp.yaml")
            run_dir.mkdir(parents=True, exist_ok=True)
            run_module("experiments.runners.maze_runner", "--config", str(tmp))
            metrics = run_dir / "metrics.jsonl"
            rows.append(
                evaluate_run(metrics, "maze", env_name, agent, episodes, gt_shortest_steps=8)
            )

    summarize(rows, out_dir / "summary.csv")
