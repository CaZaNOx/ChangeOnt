# experiments/plotting/maze.py
from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List

from experiments.plotting.raster import bar_chart_png
from experiments.plotting.util import ensure_dir, write_csv


def summarize_env(env_dir: Path, data: Dict[str, Any]) -> None:
    summary_dir = env_dir / "_summary"
    ensure_dir(summary_dir)

    rows: List[Dict[str, Any]] = []
    for agent, d in sorted(data["agents"].items()):
        rows.append({
            "env": data["env"],
            "agent": agent,
            "episodes": len(d.get("episodes", [])),
            "mean_steps": d.get("mean_steps", ""),
        })
    write_csv(summary_dir / "summary.csv", rows)

    labels = [r["agent"] for r in rows]
    vals = [float(r["mean_steps"]) if r["mean_steps"] != "" else float("nan") for r in rows]
    bar_chart_png(summary_dir / "summary.png", labels, vals, f"Maze: {data['env']}", "mean steps")


def aggregate_family(maze_root: Path) -> None:
    summary_dir = maze_root / "_summary"
    ensure_dir(summary_dir)

    # collect mean_steps per agent per env
    matrix: List[Dict[str, Any]] = []  # rows: env, agent, mean_steps
    for env_dir in sorted(d for d in maze_root.iterdir() if d.is_dir()):
        s = env_dir / "_summary" / "summary.csv"
        if not s.exists():
            continue
        lines = s.read_text(encoding="utf-8").splitlines()
        if not lines:
            continue
        header = lines[0].split(",")
        a_idx, m_idx = header.index("agent"), header.index("mean_steps")
        for b in lines[1:]:
            cols = b.split(",")
            if len(cols) != len(header):
                continue
            matrix.append({"env": env_dir.name, "agent": cols[a_idx], "mean_steps": float(cols[m_idx] or "nan")})

    # family-level average per agent across envs
    agg: Dict[str, List[float]] = {}
    for r in matrix:
        agg.setdefault(r["agent"], []).append(r["mean_steps"])
    fam_rows = [{
        "agent": agent,
        "family_mean_steps": sum(v)/len(v) if v else float("nan"),
        "n_envs": len(v)
    } for agent, v in sorted(agg.items())]
    write_csv(summary_dir / "combined_summary.csv", fam_rows)

    agents = [r["agent"] for r in fam_rows]
    vals = [r["family_mean_steps"] for r in fam_rows]
    bar_chart_png(summary_dir / "combined_summary.png", agents, vals, "Maze: aggregated over envs", "mean steps")
