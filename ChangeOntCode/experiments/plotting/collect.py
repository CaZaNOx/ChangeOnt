# experiments/plotting/collect.py
from __future__ import annotations
import json, math
from pathlib import Path
from typing import Dict, Any, Iterable, List

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

# ---------- BANDIT ----------

def collect_bandit_problem(problem_dir: Path) -> Dict[str, Any]:
    out: Dict[str, Any] = {"problem": problem_dir.name, "agents": {}}
    for run in sorted(problem_dir.iterdir()):
        if not run.is_dir():
            continue
        name = run.name
        if "_s" in name:
            agent_label = name[: name.rfind("_s")]
        else:
            agent_label = name
        mpath = run / "metrics.jsonl"
        if not mpath.exists():
            continue

        ts, vals = [], []
        for rec in read_jsonl(mpath):
            if rec.get("metric") == "cumulative_regret":
                ts.append(int(rec.get("t", 0)))
                vals.append(float(rec.get("value", 0.0)))
        if not ts:
            continue

        d = out["agents"].setdefault(agent_label, {"runs": [], "final_regrets": []})
        d["runs"].append({"t": ts, "regret": vals})
        d["final_regrets"].append(float(vals[-1]))

    # mean curve
    for agent_label, d in out["agents"].items():
        runs = d["runs"]
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

# ---------- MAZE ----------

def collect_maze_env(env_dir: Path) -> Dict[str, Any]:
    out: Dict[str, Any] = {"env": env_dir.name, "agents": {}}
    for run in sorted(env_dir.iterdir()):
        if not run.is_dir():
            continue
        agent_label = run.name
        mpath = run / "metrics.jsonl"
        if not mpath.exists():
            continue

        steps, rets = {}, {}
        for rec in read_jsonl(mpath):
            if rec.get("metric") == "episode_steps":
                steps[int(rec.get("episode", 0))] = int(rec.get("value", 0))
            elif rec.get("metric") == "episode_return":
                rets[int(rec.get("episode", 0))] = float(rec.get("value", 0.0))
        if not steps:
            continue

        episodes = [steps[k] for k in sorted(steps.keys())]
        returns = [rets[k] for k in sorted(rets.keys())] if rets else []
        out["agents"][agent_label] = {
            "episodes": episodes,
            "mean_steps": _mean([float(x) for x in episodes]),
            "returns": returns,
        }
    return out

# ---------- RENEWAL ----------

def collect_renewal_instance(inst_dir: Path) -> Dict[str, Any]:
    out: Dict[str, Any] = {"instance": inst_dir.name, "agents": {}}
    for run in sorted(inst_dir.iterdir()):
        if not run.is_dir():
            continue
        name = run.name
        if "_s" in name:
            agent_label = name[: name.rfind("_s")]
        else:
            agent_label = name
        mpath = run / "metrics.jsonl"
        if not mpath.exists():
            continue

        ts, cum = [], []
        for rec in read_jsonl(mpath):
            if "cum_reward" in rec:
                ts.append(int(rec.get("t", 0)))
                cum.append(float(rec.get("cum_reward", 0.0)))
        if not ts:
            continue

        d = out["agents"].setdefault(agent_label, {"runs": [], "finals": []})
        d["runs"].append({"t": ts, "cum": cum})
        d["finals"].append(float(cum[-1]))

    for agent_label, d in out["agents"].items():
        runs = d["runs"]
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
