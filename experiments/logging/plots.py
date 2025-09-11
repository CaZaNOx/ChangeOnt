from __future__ import annotations
import json
from pathlib import Path
from typing import Optional, Iterable, Dict, Any

import matplotlib.pyplot as plt


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
    """
    Minimal, generic plotter.
    - If it sees 'metric' == 'cumulative_regret' → line plot over t.
    - If it sees 'metric' == 'episode_steps' → bar/line over episode index.
    - Otherwise: plot first numeric series it can find.
    """
    step_log = Path(step_log)
    out_png = Path(out_png)
    series_regret_t = []
    series_regret_v = []
    series_steps_ep = []
    series_steps_v = []

    fallback_t = []
    fallback_v = None

    for rec in _read_metrics(step_log):
        if rec.get("metric") == "cumulative_regret":
            series_regret_t.append(rec.get("t"))
            series_regret_v.append(rec.get("value"))
        elif rec.get("metric") == "episode_steps":
            series_steps_ep.append(rec.get("episode"))
            series_steps_v.append(rec.get("value"))
        else:
            # fallback: first numeric metric
            if fallback_v is None:
                # try to pick a numeric key other than t/episode/metric
                for k, v in rec.items():
                    if k in ("t", "episode", "metric", "name"):
                        continue
                    if isinstance(v, (int, float)):
                        if "t" in rec:
                            fallback_t.append(rec["t"])
                        elif "episode" in rec:
                            fallback_t.append(rec["episode"])
                        else:
                            fallback_t.append(len(fallback_t) + 1)
                        fallback_v = [] if fallback_v is None else fallback_v
                        fallback_v.append(v)
                        break
            else:
                if "t" in rec:
                    fallback_t.append(rec["t"])
                elif "episode" in rec:
                    fallback_t.append(rec["episode"])
                else:
                    fallback_t.append(len(fallback_t) + 1)
                # append last numeric value seen
                num = None
                for k, v in rec.items():
                    if isinstance(v, (int, float)):
                        num = v
                if num is not None:
                    fallback_v.append(num)

    plt.figure()
    plotted = False
    if series_regret_t and series_regret_v:
        plt.plot(series_regret_t, series_regret_v)
        plt.xlabel("t")
        plt.ylabel("cumulative regret")
        plotted = True
    if series_steps_ep and series_steps_v:
        if plotted:
            plt.figure()
        plt.plot(series_steps_ep, series_steps_v)
        plt.xlabel("episode")
        plt.ylabel("steps")
        plotted = True
    if not plotted and fallback_v:
        plt.plot(fallback_t, fallback_v)
        plt.xlabel("index")
        plt.ylabel("value")
        plotted = True
    if title:
        plt.title(title)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()
