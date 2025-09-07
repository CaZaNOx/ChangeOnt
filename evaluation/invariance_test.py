# evaluation/invariance_test.py
from __future__ import annotations

import json
import sys
from typing import Callable, Dict, List

def load_metrics(path: str) -> List[Dict]:
    out: List[Dict] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out

def au_regret(records: List[Dict]) -> float:
    """
    Dummy AUReg: 1 - accuracy with a moving window proxy, purely as example.
    Real implementation should be replaced by your evaluation.metrics functions.
    """
    if not records:
        return 0.0
    correct = 0
    for r in records:
        # pretend mode==y predicts correctly half the time
        correct += 1 if (r["mode"] % 2) == (r["y"] % 2) else 0
    acc = correct / len(records)
    return 1.0 - acc

def permute_ids(records: List[Dict], key: str = "y") -> List[Dict]:
    # simple permutation 0<->1, others unchanged
    def p(v: int) -> int:
        if v == 0:
            return 1
        if v == 1:
            return 0
        return v
    out = []
    for r in records:
        r2 = dict(r)
        if key in r2:
            r2[key] = p(r2[key])
        out.append(r2)
    return out

def main(metrics_path: str, report_path: str) -> None:
    recs = load_metrics(metrics_path)
    base = au_regret(recs)
    recs_perm = permute_ids(recs, key="y")
    base_perm = au_regret(recs_perm)
    delta = abs(base - base_perm)
    report = {
        "metric": "AUReg_dummy",
        "delta": delta,
        "threshold": 1e-9,
        "pass": delta <= 1e-9,
    }
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python -m evaluation.invariance_test <metrics.jsonl> <reports/invariance_summary.json>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
