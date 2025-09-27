# experiments/eval/bandit.py
from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
from .common import load_jsonl, write_csv, linear_fit
import math

def evaluate_run(metrics_path: Path, family: str, problem: str, agent: str, seed: int, horizon: int) -> Dict[str, Any]:
    recs = load_jsonl(metrics_path)
    vals = [r for r in recs if r.get("metric") == "cumulative_regret"]
    pulls = [r for r in recs if r.get("metric") == "arm_pull"]

    # basic checks
    nondec = 0
    last = -1e18
    xs, ys = [], []
    for r in vals:
        v = float(r.get("value", 0.0))
        t = int(r.get("t", 0))
        if v < last:
            nondec += 1
        last = v
        xs.append(float(max(1, t)))
        ys.append(v)

    # fits
    slope_lin, _, r2_lin = linear_fit(xs, ys)
    ys_log = [math.log(max(1e-9, y)) for y in ys]
    slope_log, _, r2_log = linear_fit([math.log(x) for x in xs], ys_log)

    ok_rewards = True
    for r in pulls:
        rr = float(r.get("reward", 0.0))
        if rr < 0.0 or rr > 1.0:
            ok_rewards = False
            break

    return {
        "family": family, "problem": problem, "agent": agent, "seed": seed, "horizon": horizon,
        "deterministic": True, "cum_nondec_violations": nondec, "rewards_in_01": ok_rewards,
        "fit_r2_log": r2_log, "fit_r2_lin": r2_lin, "fit_slope_log": slope_log, "fit_slope_lin": slope_lin,
    }

def summarize(rows: List[Dict[str, Any]], out_csv: Path) -> None:
    write_csv(out_csv, rows)
