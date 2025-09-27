from __future__ import annotations

import csv
import json
import math
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Optional


# ---------- IO helpers ----------

def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def read_jsonl(p: Path) -> List[Dict]:
    out: List[Dict] = []
    with open(p, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except Exception:
                pass
    return out


def write_csv_header_then_rows(path: Path, rows: List[Dict]) -> None:
    if not rows:
        return
    ensure_dir(path.parent)
    cols = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow(r)


# ---------- simple regression (no numpy) ----------

@dataclass
class FitResult:
    slope: float
    intercept: float
    r2: float
    n: int


def _linreg(xs: List[float], ys: List[float]) -> FitResult:
    n = len(xs)
    if n < 2:
        return FitResult(0.0, float("nan"), 0.0, n)
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    den = sum((x - mean_x) ** 2 for x in xs)
    slope = num / den if den != 0 else 0.0
    intercept = mean_y - slope * mean_x
    ss_tot = sum((y - mean_y) ** 2 for y in ys)
    ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(xs, ys))
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
    return FitResult(slope, intercept, r2, n)


def fit_regret_vs_t(ts: List[int], vals: List[float]) -> FitResult:
    xs = [float(t) for t in ts]
    ys = [float(v) for v in vals]
    return _linreg(xs, ys)


def fit_regret_vs_logt(ts: List[int], vals: List[float], burn_in: int = 1) -> FitResult:
    xs: List[float] = []
    ys: List[float] = []
    for t, v in zip(ts, vals):
        if t < burn_in:
            continue
        if t <= 0:
            continue
        xs.append(math.log(float(t)))
        ys.append(float(v))
    if not xs:
        return FitResult(0.0, float("nan"), 0.0, 0)
    return _linreg(xs, ys)


# ---------- metric extraction ----------

def series_from_metrics(recs: List[Dict], name: str, x_key: str = "t", y_key: str = "value") -> Tuple[List[int], List[float]]:
    ts: List[int] = []
    ys: List[float] = []
    for r in recs:
        if r.get("metric") == name:
            x = r.get(x_key)
            y = r.get(y_key)
            if isinstance(x, (int, float)) and isinstance(y, (int, float)):
                ts.append(int(x))
                ys.append(float(y))
    return ts, ys


def last_value_of_metric(recs: List[Dict], name: str, y_key: str = "value") -> Optional[float]:
    val: Optional[float] = None
    for r in recs:
        if r.get("metric") == name and isinstance(r.get(y_key), (int, float)):
            val = float(r[y_key])
    return val


# ---------- generic checks ----------

def count_nondecreasing_violations(seq: List[float]) -> int:
    bad = 0
    last = -float("inf")
    for v in seq:
        if v < last:
            bad += 1
        last = v
    return bad


def all_rewards_in_01(recs: List[Dict]) -> bool:
    ok = True
    for r in recs:
        if r.get("metric") == "arm_pull":
            rv = r.get("reward")
            if not isinstance(rv, (int, float)):
                continue
            if rv < 0.0 or rv > 1.0:
                ok = False
                break
    return ok


def renewal_mismatch_count(recs: List[Dict]) -> int:
    """reward==1 iff act==obs on renewal logs."""
    bad = 0
    for r in recs:
        if "reward" in r and "act" in r and "obs" in r:
            rew = float(r["reward"])
            act = int(r["act"])
            obs = int(r["obs"])
            if ((rew == 1.0) != (act == obs)):
                bad += 1
    return bad


def renewal_cum_reward_series(recs: List[Dict]) -> List[float]:
    ys: List[float] = []
    for r in recs:
        if "cum_reward" in r:
            ys.append(float(r["cum_reward"]))
    return ys


# ---------- maze BFS recomputation ----------

def bfs_shortest_steps_passable(start: Tuple[int, int], goal: Tuple[int, int], passable_fn) -> Optional[int]:
    from collections import deque
    DIRS = [(1,0),(-1,0),(0,1),(0,-1)]
    q = deque([start])
    dist = {start: 0}
    while q:
        r, c = q.popleft()
        if (r, c) == goal:
            return dist[(r, c)]
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if not passable_fn(nr, nc):
                continue
            if (nr, nc) in dist:
                continue
            dist[(nr, nc)] = dist[(r, c)] + 1
            q.append((nr, nc))
    return None
