from __future__ import annotations
import json
from pathlib import Path
from typing import Optional, Iterable, Dict, Any


def _read_metrics(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def quick_plot(step_log: Path, out_png: Path, title: Optional[str] = None) -> None:
    try:
        import matplotlib.pyplot as plt  # type: ignore
    except Exception:
        return

    step_log = Path(step_log)
    out_png = Path(out_png)
    cum_t, cum_v = [], []
    regret_t, regret_v = [], []
    ep_t, ep_v = [], []
    fallback_t, fallback_v = [], []

    for rec in _read_metrics(step_log):
        if "t" in rec and isinstance(rec.get("cum_reward"), (int, float)):
            cum_t.append(rec["t"])
            cum_v.append(float(rec["cum_reward"]))
            continue
        if rec.get("metric") == "cumulative_regret":
            regret_t.append(rec.get("t"))
            regret_v.append(rec.get("value"))
            continue
        if rec.get("metric") == "episode_steps":
            ep_t.append(rec.get("episode"))
            ep_v.append(rec.get("value"))
            continue
        for k, v in rec.items():
            if k in ("t", "episode", "metric", "name"):
                continue
            if isinstance(v, (int, float)):
                fallback_t.append(rec.get("t", rec.get("episode", len(fallback_t))))
                fallback_v.append(float(v))
                break

    fig, ax = plt.subplots(figsize=(7.5, 4.2), dpi=160)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    if cum_t and cum_v:
        ax.plot(cum_t, cum_v, linewidth=1.5)
        ax.set_xlabel("step")
        ax.set_ylabel("cumulative reward")
    elif regret_t and regret_v:
        ax.plot(regret_t, regret_v, linewidth=1.5)
        ax.set_xlabel("step")
        ax.set_ylabel("cumulative regret")
    elif ep_t and ep_v:
        ax.plot(ep_t, ep_v, linewidth=1.5)
        ax.set_xlabel("episode")
        ax.set_ylabel("steps")
    elif fallback_v:
        ax.plot(fallback_t, fallback_v, linewidth=1.5)
        ax.set_xlabel("index")
        ax.set_ylabel("value")
    else:
        plt.close(fig)
        return

    if title:
        ax.set_title(title)
    ax.grid(True, linestyle=':', alpha=0.35)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_png, facecolor='white', bbox_inches='tight')
    plt.close(fig)
