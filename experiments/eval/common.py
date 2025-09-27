# experiments/eval/common.py
from __future__ import annotations
import json, math, csv
from pathlib import Path
from typing import List, Dict, Any, Tuple

def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

def linear_fit(xs: List[float], ys: List[float]) -> Tuple[float, float, float]:
    """
    Returns (slope, intercept, r2) of least squares linear fit.
    """
    n = len(xs)
    if n < 2:
        return 0.0, 0.0, 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs) or 1e-12
    slope = num / den
    intercept = my - slope * mx
    ss_tot = sum((y - my) ** 2 for y in ys) or 1e-12
    ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(xs, ys))
    r2 = 1.0 - (ss_res / ss_tot)
    return slope, intercept, r2

def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    cols = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
