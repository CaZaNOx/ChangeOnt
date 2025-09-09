from __future__ import annotations
import json
from pathlib import Path
from typing import List, Dict, Optional

import matplotlib.pyplot as plt

def _load_jsonl(path: Path) -> List[Dict]:
    if not path.exists():
        raise FileNotFoundError(path)
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out

def plot_flips_and_events(step_log: Path, out_png: Path, title: Optional[str] = None) -> None:
    records = _load_jsonl(step_log)
    steps = [r.get("step", i) for i, r in enumerate(records)]
    ys    = [r.get("y", 0) for r in records]
    modes = [r.get("mode", 0) for r in records]
    ema   = [r.get("loop_score", 0.0) for r in records]
    collapse = [r.get("collapse", 0) for r in records]

    fig = plt.figure()
    ax = plt.gca()
    ax.plot(steps, ys, label="env class y")
    ax.plot(steps, modes, label="mode (0/1)")
    ax.plot(steps, ema, label="loop_score/EMA")
    ax.plot(steps, collapse, label="collapse (0/1)")
    ax.set_xlabel("step")
    ax.set_ylabel("value")
    if title:
        ax.set_title(title)
    ax.legend()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png)
    plt.close(fig)
