# experiments/eval/paper_checks.py
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

from .utils import read_jsonl

# -------- Bandit --------
def check_bandit_agent(agent_dir: Path) -> Dict[str, float]:
    mpath = agent_dir / "metrics.jsonl"
    recs = read_jsonl(mpath)
    last = -1e18
    cum_nondec = 0
    final_t = 0
    final_reg = 0.0
    pulls = None
    best_arm = None
    for r in recs:
        if r.get("metric") == "cumulative_regret":
            t = int(r.get("t", 0))
            v = float(r.get("value", 0.0))
            if v < last:
                cum_nondec += 1
            last = v
            final_t = t
            final_reg = v
        if r.get("metric") == "pulls_summary":
            pulls = r.get("pulls", None)
            best_arm = r.get("best_arm", None)
    opt_frac = 0.0
    if isinstance(pulls, list):
        s = sum(pulls) or 1
        if isinstance(best_arm, int) and 0 <= best_arm < len(pulls):
            opt_frac = pulls[best_arm] / s
    return {
        "final_t": float(final_t),
        "final_cum_regret": float(final_reg),
        "cum_nondec_violations": float(cum_nondec),
        "optimal_pull_fraction": float(opt_frac),
    }

# -------- Maze --------
def check_maze_agent(agent_dir: Path) -> Dict[str, float]:
    mpath = agent_dir / "metrics.jsonl"
    recs = read_jsonl(mpath)
    ep_steps: List[float] = []
    for r in recs:
        if r.get("metric") == "episode_steps":
            ep_steps.append(float(r.get("value", 0.0)))
    mean_steps = sum(ep_steps) / len(ep_steps) if ep_steps else 0.0
    return {"episodes": float(len(ep_steps)), "mean_steps": float(mean_steps)}

# -------- Renewal --------
def check_renewal_agent(agent_dir: Path) -> Dict[str, float]:
    mpath = agent_dir / "metrics.jsonl"
    recs = read_jsonl(mpath)
    T = 0
    acc_hits = 0
    final_cum = 0.0
    mismatches = 0
    for r in recs:
        if r.get("record_type") == "header":
            continue
        if {"obs", "act", "reward", "cum_reward"} <= set(r.keys()):
            T += 1
            if int(r["obs"]) == int(r["act"]):
                acc_hits += 1
            reward = float(r["reward"])
            if (reward == 1.0) != (int(r["obs"]) == int(r["act"])):
                mismatches += 1
            final_cum = float(r["cum_reward"])
    acc = (acc_hits / T) if T else 0.0
    return {
        "steps": float(T),
        "final_cum_reward": float(final_cum),
        "final_accuracy": float(acc),
        "mismatches": float(mismatches),
    }
