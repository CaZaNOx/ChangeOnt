# experiments/eval/plots.py
from __future__ import annotations

from pathlib import Path
from typing import List, Optional
import math

try:
    import matplotlib.pyplot as plt  # type: ignore
except Exception:  # pragma: no cover
    plt = None  # type: ignore

from .utils import read_jsonl

def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

def bandit_overlay(family_dir: Path, out_path: Path, probs: Optional[List[float]] = None) -> None:
    if plt is None:
        return
    _ensure_parent(out_path)
    fig = plt.figure()
    # per-agent regret curves
    for agent_dir in sorted(p for p in family_dir.iterdir() if p.is_dir()):
        mpath = agent_dir / "metrics.jsonl"
        if not mpath.exists():
            continue
        xs, ys = [], []
        for r in read_jsonl(mpath):
            if r.get("metric") == "cumulative_regret":
                xs.append(int(r.get("t", len(xs) + 1)))
                ys.append(float(r.get("value", 0.0)))
        if xs and ys:
            plt.plot(xs, ys, label=agent_dir.name)
    # simple theory overlay ~ C * sum log(t)/Δ
    if probs:
        deltas = []
        best = max(probs)
        for p in probs:
            d = best - p
            if d > 0:
                deltas.append(d)
        if deltas:
            try:
                import numpy as np  # type: ignore
                tmax = max(xs) if 'xs' in locals() and xs else 1000
                ts = np.arange(2, tmax + 1)
                C = 2.0
                theory = [sum((C * math.log(t) / d) for d in deltas) for t in ts]
                plt.plot(ts, theory, linestyle="--", label="UCB1_theory~logT")
            except Exception:
                pass
    plt.xlabel("t")
    plt.ylabel("cumulative regret")
    plt.title("Bandit – regret overlay")
    plt.legend()
    plt.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)

def maze_overlay(family_dir: Path, out_path: Path) -> None:
    if plt is None:
        return
    _ensure_parent(out_path)
    fig = plt.figure()
    for agent_dir in sorted(p for p in family_dir.iterdir() if p.is_dir()):
        mpath = agent_dir / "metrics.jsonl"
        if not mpath.exists():
            continue
        xs, ys = [], []
        for r in read_jsonl(mpath):
            if r.get("metric") == "episode_steps":
                xs.append(int(r.get("episode", len(xs))))
                ys.append(float(r.get("value", 0.0)))
        if xs and ys:
            plt.plot(xs, ys, marker="o", label=agent_dir.name)
    plt.xlabel("episode")
    plt.ylabel("steps")
    plt.title("Maze – steps per episode")
    plt.legend()
    plt.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)

def renewal_overlay(family_dir: Path, out_path: Path) -> None:
    if plt is None:
        return
    _ensure_parent(out_path)
    fig = plt.figure()
    for agent_dir in sorted(p for p in family_dir.iterdir() if p.is_dir()):
        mpath = agent_dir / "metrics.jsonl"
        if not mpath.exists():
            continue
        xs, ys = [], []
        for r in read_jsonl(mpath):
            if "cum_reward" in r and "t" in r:
                xs.append(int(r.get("t", len(xs))))
                ys.append(float(r.get("cum_reward", 0.0)))
        if xs and ys:
            plt.plot(xs, ys, label=agent_dir.name)
    plt.xlabel("t")
    plt.ylabel("cumulative reward")
    plt.title("Renewal – cumulative reward")
    plt.legend()
    plt.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)
