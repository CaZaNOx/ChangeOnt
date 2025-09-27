# experiments/eval/maze.py
from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
from .common import load_jsonl, write_csv

def evaluate_run(metrics_path: Path, family: str, env_name: str, agent: str, episodes: int, gt_shortest_steps: int) -> Dict[str, Any]:
    recs = load_jsonl(metrics_path)
    steps = [int(r.get("value", 0)) for r in recs if r.get("metric") == "episode_steps"]
    returns = [float(r.get("value", 0.0)) for r in recs if r.get("metric") == "episode_return"]
    mean_steps = sum(steps) / max(1, len(steps)) if steps else float("nan")
    steps_ok = all(s >= 0 for s in steps) and len(steps) == episodes
    return_is_neg_steps = all(abs(ret + (s - 1)) < 1e-9 for ret, s in zip(returns, steps)) if steps and returns else False
    optimality = abs(mean_steps - float(gt_shortest_steps)) < 1e-9 if steps_ok else False
    return {
        "family": "maze",
        "env": env_name,
        "agent": agent,
        "episodes": episodes,
        "gt_shortest_steps": gt_shortest_steps,
        "mean_steps": mean_steps,
        "steps_all_ok": steps_ok,
        "return_is_neg_steps_all": return_is_neg_steps,
        "optimality_matches_all": optimality,
    }

def summarize(rows: List[Dict[str, Any]], out_csv: Path) -> None:
    write_csv(out_csv, rows)
