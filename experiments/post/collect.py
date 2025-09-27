# experiments/post/collect.py
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any, Iterable, List, Tuple, Optional
import math


def read_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except Exception:
                continue


def _mean(xs: List[float]) -> float:
    xs2 = [x for x in xs if isinstance(x, (int, float)) and not math.isnan(x)]
    return sum(xs2) / len(xs2) if xs2 else float("nan")


# ----------------- BANDIT -----------------

def collect_bandit_problem(problem_dir: Path) -> Dict[str, Any]:
    """
    Layout expected:
      problem_dir/
        <agent_label>_s<seed>/
          metrics.jsonl
    Returns dict with:
      {
        "problem": <name>,
        "agents": {
           "<label>": {
              "runs": { seed: {"t": [...], "regret": [...], "final": float} },
              "mean_curve": {"t": [...], "regret": [...]},  # averaged over seeds when possible
              "final_regrets": [ ... ],
           }, ...
        }
      }
    """
    out: Dict[str, Any] = {"problem": problem_dir.name, "agents": {}}
    for run in sorted(problem_dir.iterdir()):
        if not run.is_dir():
            continue
        # agent label is dir name without seed suffix if present
        name = run.name
        # allow either "<agent>_s7" or just "<agent>"
        if "_s" in name:
            agent_label = name[: name.rfind("_s")]
            try:
                seed = int(name[name.rfind("_s")+2:])
            except Exception:
                seed = -1
        else:
            agent_label, seed = name, -1

        mpath = run / "metrics.jsonl"
        if not mpath.exists():
            continue

        ts: List[int] = []
        vals: List[float] = []
        for rec in read_jsonl(mpath):
            if rec.get("metric") == "cumulative_regret":
                t = int(rec.get("t", 0))
                v = float(rec.get("value", 0.0))
                ts.append(t)
                vals.append(v)

        if not ts:
            continue

        d = out["agents"].setdefault(agent_label, {"runs": {}, "final_regrets": []})
        d["runs"][seed] = {"t": ts, "regret": vals, "final": float(vals[-1])}
        d["final_regrets"].append(float(vals[-1]))

    # mean curve (align by min length)
    for agent_label, d in out["agents"].items():
        runs = list(d["runs"].values())
        if not runs:
            d["mean_curve"] = {"t": [], "regret": []}
            continue
        min_len = min(len(r["t"]) for r in runs)
        t = runs[0]["t"][:min_len]
        reg = []
        for i in range(min_len):
            reg.append(_mean([r["regret"][i] for r in runs]))
        d["mean_curve"] = {"t": t, "regret": reg}
    return out


# ----------------- MAZE -----------------

def collect_maze_env(env_dir: Path) -> Dict[str, Any]:
    """
    Layout:
      env_dir/
        <agent_label>/
          metrics.jsonl
    Output:
      {
        "env": <name>,
        "agents": {
           "<label>": {
              "episodes": [steps...],
              "mean_steps": float,
              "returns": [ret...],  # optional
           }
        }
      }
    """
    out: Dict[str, Any] = {"env": env_dir.name, "agents": {}}
    for run in sorted(env_dir.iterdir()):
        if not run.is_dir():
            continue
        agent_label = run.name
        mpath = run / "metrics.jsonl"
        if not mpath.exists():
            continue

        steps: Dict[int, int] = {}
        rets: Dict[int, float] = {}
        for rec in read_jsonl(mpath):
            if rec.get("metric") == "episode_steps":
                ep = int(rec.get("episode", 0))
                steps[ep] = int(rec.get("value", 0))
            elif rec.get("metric") == "episode_return":
                ep = int(rec.get("episode", 0))
                rets[ep] = float(rec.get("value", 0.0))

        if not steps:
            continue

        # normalize order
        episodes = [steps[k] for k in sorted(steps.keys())]
        returns = [rets[k] for k in sorted(rets.keys())] if rets else []
        out["agents"][agent_label] = {
            "episodes": episodes,
            "mean_steps": _mean([float(x) for x in episodes]),
            "returns": returns,
        }
    return out


# ----------------- RENEWAL -----------------

def collect_renewal_instance(inst_dir: Path) -> Dict[str, Any]:
    """
    Layout:
      inst_dir/
        <agent_label>_s<seed>/
          metrics.jsonl
    Output:
      {
        "instance": <name>,
        "agents": {
          "<label>": {
             "runs": {seed: {"t":[...], "cum":[...], "final": float}},
             "mean_curve": {"t":[...], "cum":[...]},
             "finals": [ ... ],
          }
        }
      }
    """
    out: Dict[str, Any] = {"instance": inst_dir.name, "agents": {}}
    for run in sorted(inst_dir.iterdir()):
        if not run.is_dir():
            continue
        name = run.name
        if "_s" in name:
            agent_label = name[: name.rfind("_s")]
            try:
                seed = int(name[name.rfind("_s")+2:])
            except Exception:
                seed = -1
        else:
            agent_label, seed = name, -1

        mpath = run / "metrics.jsonl"
        if not mpath.exists():
            continue

        ts: List[int] = []
        cum: List[float] = []
        for rec in read_jsonl(mpath):
            if "cum_reward" in rec:  # renewal runner writes cum_reward
                ts.append(int(rec.get("t", 0)))
                cum.append(float(rec.get("cum_reward", 0.0)))

        if not ts:
            continue

        d = out["agents"].setdefault(agent_label, {"runs": {}, "finals": []})
        d["runs"][seed] = {"t": ts, "cum": cum, "final": float(cum[-1])}
        d["finals"].append(float(cum[-1]))

    for agent_label, d in out["agents"].items():
        runs = list(d["runs"].values())
        if not runs:
            d["mean_curve"] = {"t": [], "cum": []}
            continue
        min_len = min(len(r["t"]) for r in runs)
        t = runs[0]["t"][:min_len]
        cm = []
        for i in range(min_len):
            cm.append(_mean([r["cum"][i] for r in runs]))
        d["mean_curve"] = {"t": t, "cum": cm}
    return out
