# experiments/post/plot.py
from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
import csv

try:
    import matplotlib.pyplot as plt  # type: ignore
except Exception:
    plt = None  # plotting optional


def _ensure(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    keys = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow(r)


# ----------------- BANDIT -----------------

def plot_bandit(problem_dir: Path, data: Dict[str, Any]) -> None:
    eval_dir = problem_dir / "eval"
    _ensure(eval_dir)

    # summary CSV: final regrets per agent (mean over seeds)
    rows: List[Dict[str, Any]] = []
    for agent_label, d in sorted(data["agents"].items()):
        finals = d.get("final_regrets", [])
        rows.append({
            "problem": data["problem"],
            "agent": agent_label,
            "mean_final_regret": sum(finals)/len(finals) if finals else "",
            "n_runs": len(finals),
        })
    write_csv(eval_dir / "summary.csv", rows)

    if plt is None:
        return

    # overlay mean regret curves
    plt.figure()
    for agent_label, d in sorted(data["agents"].items()):
        mc = d.get("mean_curve", {})
        t = mc.get("t", [])
        reg = mc.get("regret", [])
        if not t or not reg:
            continue
        plt.plot(t, reg, label=agent_label)
    plt.xlabel("t")
    plt.ylabel("mean cumulative regret")
    plt.title(f"Bandit: {data['problem']}")
    plt.legend()
    plt.tight_layout()
    plt.savefig(eval_dir / "summary.png", dpi=160)
    plt.close()


# ----------------- MAZE -----------------

def plot_maze(env_dir: Path, data: Dict[str, Any]) -> None:
    eval_dir = env_dir / "eval"
    _ensure(eval_dir)

    rows: List[Dict[str, Any]] = []
    for agent_label, d in sorted(data["agents"].items()):
        rows.append({
            "env": data["env"],
            "agent": agent_label,
            "episodes": len(d.get("episodes", [])),
            "mean_steps": d.get("mean_steps", ""),
        })
    write_csv(eval_dir / "summary.csv", rows)

    if plt is None:
        return

    # bar chart of mean steps
    labels = []
    means = []
    for agent_label, d in sorted(data["agents"].items()):
        labels.append(agent_label)
        means.append(float(d.get("mean_steps", float("nan"))))
    if labels:
        plt.figure()
        plt.bar(range(len(labels)), means)
        plt.xticks(range(len(labels)), labels, rotation=30, ha="right")
        plt.ylabel("mean steps (lower is better)")
        plt.title(f"Maze: {data['env']}")
        plt.tight_layout()
        plt.savefig(eval_dir / "summary.png", dpi=160)
        plt.close()


# ----------------- RENEWAL -----------------

def plot_renewal(inst_dir: Path, data: Dict[str, Any]) -> None:
    eval_dir = inst_dir / "eval"
    _ensure(eval_dir)

    rows: List[Dict[str, Any]] = []
    for agent_label, d in sorted(data["agents"].items()):
        finals = d.get("finals", [])
        rows.append({
            "instance": data["instance"],
            "agent": agent_label,
            "mean_final_cum_reward": sum(finals)/len(finals) if finals else "",
            "n_runs": len(finals),
        })
    write_csv(eval_dir / "summary.csv", rows)

    if plt is None:
        return

    plt.figure()
    for agent_label, d in sorted(data["agents"].items()):
        mc = d.get("mean_curve", {})
        t = mc.get("t", [])
        cm = mc.get("cum", [])
        if not t or not cm:
            continue
        plt.plot(t, cm, label=agent_label)
    plt.xlabel("t")
    plt.ylabel("mean cumulative reward")
    plt.title(f"Renewal: {data['instance']}")
    plt.legend()
    plt.tight_layout()
    plt.savefig(eval_dir / "summary.png", dpi=160)
    plt.close()
