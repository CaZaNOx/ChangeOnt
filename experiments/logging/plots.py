from future import annotations  
import json  
from pathlib import Path  
from typing import List, Dict, Optional

import matplotlib.pyplot as plt

def _load_jsonl(path: Path) -> List[Dict]:  
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]

def plot_flips_and_events(step_log: Path, out_png: Path, title: Optional[str] = None) -> None:  
    """  
    Draw a simple raster: flips (vertical lines) and events (vertical lines), plus actions/reward trace.

    ```
    Expects step JSONL rows with at least:
    - "t" (int)
    - "flip" (bool)
    - "event" (bool)   # renewal or kth-opportunity proxy
    - "reward" (float) # if present, we overlay it
    - "act" (int)      # 0/1 exit attempts (optional)

    Saves a single PNG to out_png.
    """
    rows = _load_jsonl(step_log)
    if not rows:
        raise ValueError(f"No rows found in {step_log}")

    ts = [r["t"] for r in rows]
    flips = [r["t"] for r in rows if r.get("flip")]
    events = [r["t"] for r in rows if r.get("event")]
    rewards = [r.get("reward", 0.0) for r in rows]
    actions = [r.get("act", 0) for r in rows]

    plt.figure(figsize=(10, 4.5))

    # reward trace (scaled)
    if any(abs(x) > 1e-12 for x in rewards):
        plt.plot(ts, rewards, label="reward")

    # action impulses
    if any(a != 0 for a in actions):
        y = [0.02 if a else None for a in actions]
        for t, yy in zip(ts, y):
            if yy is not None:
                plt.vlines(t, 0, 0.05)

    # flips & events as vertical markers
    for t in flips:
        plt.vlines(t, 0.0, 1.0, alpha=0.8)
    for t in events:
        plt.vlines(t, 0.0, 1.0, alpha=0.4)

    ttl = title or f"Flips (dark) & Events (light) — {step_log.name}"
    plt.title(ttl)
    plt.xlabel("time step")
    plt.ylabel("trace / markers")
    plt.tight_layout()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_png, dpi=150)
    plt.close()


def plot_episode_aggregates(ep_summary_jsonl: Path, out_png: Path, title: Optional[str] = None) -> None:  
    """  
    Bar-like summary for per-episode metrics: flips, FDR_windowed, slope_window, AUReg_window.

    ```
    Reads rows of shape:
    {"ep": int, "flips": int, "FDR_windowed": float, "slope_window": float, "AUReg_window": float}
    """
    rows = _load_jsonl(ep_summary_jsonl)
    if not rows:
        raise ValueError(f"No rows found in {ep_summary_jsonl}")

    eps = [r["ep"] for r in rows]
    flips = [r["flips"] for r in rows]
    fdr = [r["FDR_windowed"] for r in rows]
    slope = [r["slope_window"] for r in rows]
    aureg = [r["AUReg_window"] for r in rows]

    # 4 stacked rows
    fig, axes = plt.subplots(4, 1, figsize=(10, 8), sharex=True)

    axes[0].plot(eps, flips)
    axes[0].set_ylabel("flips")

    axes[1].plot(eps, fdr)
    axes[1].set_ylabel("FDR_w")

    axes[2].plot(eps, slope)
    axes[2].set_ylabel("slope")

    axes[3].plot(eps, aureg)
    axes[3].set_ylabel("AUReg")
    axes[3].set_xlabel("episode")

    ttl = title or f"Per-episode summary — {ep_summary_jsonl.name}"
    fig.suptitle(ttl)
    fig.tight_layout(rect=[0, 0.03, 1, 0.97])
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=150)
    plt.close(fig)
