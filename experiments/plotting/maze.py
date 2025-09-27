# experiments/plotting/maze.py
from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
from experiments.plotting.util import ensure_dir, write_csv, safe_import_plt

plt = safe_import_plt()

def summarize_env(env_dir: Path, data: Dict[str, Any]) -> None:
    eval_dir = env_dir / "eval"
    ensure_dir(eval_dir)

    rows: List[Dict[str, Any]] = []
    for agent, d in sorted(data["agents"].items()):
        rows.append({
            "env": data["env"],
            "agent": agent,
            "episodes": len(d.get("episodes", [])),
            "mean_steps": d.get("mean_steps", ""),
        })
    write_csv(eval_dir / "summary.csv", rows)

    if plt and rows:
        labels = [r["agent"] for r in rows]
        vals = [float(r["mean_steps"]) if r["mean_steps"] != "" else float("nan") for r in rows]
        plt.figure()
        plt.bar(range(len(labels)), vals)
        plt.xticks(range(len(labels)), labels, rotation=30, ha="right")
        plt.ylabel("mean steps (lower is better)")
        plt.title(f"Maze: {data['env']}")
        plt.tight_layout()
        plt.savefig(eval_dir / "summary.png", dpi=160)
        plt.close()

def aggregate_family(maze_root: Path) -> None:
    eval_dir = maze_root / "eval"
    ensure_dir(eval_dir)

    # collect mean_steps per agent per env
    matrix: List[Dict[str, Any]] = []  # rows: env, agent, mean_steps
    for env_dir in sorted(d for d in maze_root.iterdir() if d.is_dir()):
        s = env_dir / "eval" / "summary.csv"
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
    write_csv(eval_dir / "combined_summary.csv", fam_rows)

    if plt and fam_rows:
        labels = [r["agent"] for r in fam_rows]
        vals = [r["family_mean_steps"] for r in fam_rows]
        plt.figure()
        plt.bar(range(len(labels)), vals)
        plt.xticks(range(len(labels)), labels, rotation=30, ha="right")
        plt.ylabel("mean steps (lower is better)")
        plt.title("Maze: aggregated over envs")
        plt.tight_layout()
        plt.savefig(eval_dir / "combined_summary.png", dpi=160)
        plt.close()
