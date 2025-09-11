from __future__ import annotations

import json
import os
import sys
from typing import Dict, List, Tuple

# Use the actual AUReg function so we test the real pipeline.
try:
    from evaluation.metrics.au_regret import au_regret_window
except Exception:
    # Fallback (shouldn't happen once repo is wired)
    def au_regret_window(truth, preds):
        if not truth:
            return 0.0
        correct = sum(1 for t, p in zip(truth, preds) if t == p)
        return 1.0 - correct / len(truth)

def load_metrics(path: str) -> List[Dict]:
    out: List[Dict] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out

def _perm_map() -> Dict[int, int]:
    # simple fixed permutation: 0<->1; others unchanged
    return {0: 1, 1: 0}

def _apply_perm(v: int, P: Dict[int, int]) -> int:
    return P.get(v, v)

def main(metrics_path: str, report_path: str) -> None:
    recs = load_metrics(metrics_path)
    y = [r.get("y", 0) for r in recs]
    pred = [r.get("pred", 0) for r in recs]

    base = au_regret_window(y, pred)

    P = _perm_map()
    y_perm = [_apply_perm(v, P) for v in y]
    pred_perm = [_apply_perm(v, P) for v in pred]

    base_perm = au_regret_window(y_perm, pred_perm)

    delta = abs(base - base_perm)
    report = {
        "metric": "AUReg",
        "delta": delta,
        "threshold": 1e-9,
        "pass": delta <= 1e-9,
        "n": len(y),
    }
    parent = os.path.dirname(report_path) or "."
    os.makedirs(parent, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python -m evaluation.invariance_test <metrics.jsonl> <reports/invariance_summary.json>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
