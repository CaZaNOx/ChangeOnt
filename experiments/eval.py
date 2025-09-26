# PATH: experiments/eval.py
from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any

@dataclass
class Series:
    name: str
    xs: List[float]
    ys: List[float]
    extra: Dict[str, Any]

def _read_jsonl(path: Path) -> List[Dict]:
    recs: List[Dict] = []
    if not path.exists():
        return recs
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                recs.append(json.loads(line))
            except Exception:
                # tolerate partial/broken lines
                pass
    return recs

def _ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)

def _write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    keys = list(rows[0].keys())
    lines = []
    lines.append(",".join(keys))
    for r in rows:
        vals = []
        for k in keys:
            v = r.get(k, "")
            if isinstance(v, (list, dict)):
                v = json.dumps(v, ensure_ascii=False)
            vals.append(str(v))
        lines.append(",".join(vals))
    path.write_text("\n".join(lines), encoding="utf-8")

def _try_plot_xy(out_png: Path, title: str, series: List[Series], xlabel: str, ylabel: str, ground: Optional[Series] = None) -> None:
    try:
        import matplotlib.pyplot as plt  # do plain matplotlib; no seaborn
        fig = plt.figure()
        ax = fig.add_subplot(111)
        # ground truth first (if any)
        if ground is not None and len(ground.xs) == len(ground.ys) and len(ground.xs) > 0:
            ax.plot(ground.xs, ground.ys, linestyle="--", linewidth=1.0, label=f"ground:{ground.name}")
        for s in series:
            if len(s.xs) == len(s.ys) and len(s.xs) > 0:
                ax.plot(s.xs, s.ys, label=s.name)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.legend()
        fig.tight_layout()
        fig.savefig(str(out_png))
        plt.close(fig)
    except Exception:
        # plotting optional; skip if no matplotlib
        pass

# ------------------------
# BANDIT EVAL
# ------------------------

def eval_bandit(runs: List[Path], out_dir: Path) -> Dict[str, Any]:
    """
    Expect metrics.jsonl with:
      {"metric":"cumulative_regret","t": <int>,"value": <float>}
      {"metric":"arm_pull","t": <int>,"arm": <int>,"reward": <0/1>}
    and a final tail:
      {"metric":"pulls_summary","t": <int>,"pulls": [..],"best_arm": <int>}
    """
    _ensure_dir(out_dir)
    series: List[Series] = []
    rows: List[Dict[str, Any]] = []
    max_t = 0
    for run in runs:
        mpath = run / "metrics.jsonl"
        recs = _read_jsonl(mpath)
        xs, ys = [], []
        pulls_summary = None
        for r in recs:
            if r.get("metric") == "cumulative_regret":
                xs.append(float(r.get("t", 0)))
                ys.append(float(r.get("value", 0.0)))
            if r.get("metric") == "pulls_summary":
                pulls_summary = r
        if xs:
            max_t = max(max_t, int(xs[-1]))
            extra = {}
            if pulls_summary is not None:
                pulls = pulls_summary.get("pulls", [])
                best = pulls_summary.get("best_arm", None)
                total = sum(pulls) if pulls else 0
                opt_frac = (pulls[best] / total) if (pulls and best is not None and total > 0) else ""
                extra.update({
                    "final_t": int(xs[-1]),
                    "final_cum_regret": ys[-1],
                    "optimal_pull_fraction": opt_frac,
                    "pulls": pulls,
                    "best_arm": best,
                })
            else:
                extra.update({
                    "final_t": int(xs[-1]),
                    "final_cum_regret": ys[-1],
                })
            series.append(Series(name=run.name, xs=xs, ys=ys, extra=extra))
            row = {"run": run.name, **extra}
            rows.append(row)

    # ground truth: zero-regret line
    ground = Series(name="zero_regret", xs=list(range(1, max_t+1)), ys=[0.0]*max_t, extra={})
    _write_csv(out_dir / "summary.csv", rows)
    _try_plot_xy(out_dir / "compare.png", "Bandit: cumulative regret", series, xlabel="t", ylabel="cum_regret", ground=ground)
    return {"summary_rows": rows, "plot": str(out_dir / "compare.png")}

# ------------------------
# MAZE EVAL
# ------------------------

def eval_maze(runs: List[Path], out_dir: Path) -> Dict[str, Any]:
    """
    Expect metrics.jsonl with per-episode:
      {"metric":"episode_steps","episode": <int>,"value": <int>}
      {"metric":"episode_return","episode": <int>,"value": <float>}
    We plot episode_steps across episodes. Ground truth = the best (min) steps among runs (or BFS run if included).
    """
    _ensure_dir(out_dir)
    series: List[Series] = []
    rows: List[Dict[str, Any]] = []
    max_ep = 0
    all_steps_by_ep: Dict[int, List[float]] = {}

    bfs_series: Optional[Series] = None

    for run in runs:
        mpath = run / "metrics.jsonl"
        recs = _read_jsonl(mpath)
        steps_by_ep: Dict[int, float] = {}
        for r in recs:
            if r.get("metric") == "episode_steps":
                ep = int(r.get("episode", 0))
                val = float(r.get("value", 0.0))
                steps_by_ep[ep] = val
                max_ep = max(max_ep, ep)
                all_steps_by_ep.setdefault(ep, []).append(val)

        if steps_by_ep:
            xs = sorted(steps_by_ep.keys())
            ys = [steps_by_ep[e] for e in xs]
            s = Series(name=run.name, xs=[float(x) for x in xs], ys=ys, extra={
                "mean_steps": sum(ys)/len(ys) if ys else "",
                "episodes": len(ys),
            })
            series.append(s)
            rows.append({"run": run.name, "episodes": len(ys), "mean_steps": s.extra["mean_steps"]})
            if "bfs" in run.name.lower():
                bfs_series = s

    # ground truth: best (min) steps per episode among provided runs or BFS if present
    ground = None
    if bfs_series is not None:
        ground = Series(name="bfs", xs=bfs_series.xs, ys=bfs_series.ys, extra={})
    elif all_steps_by_ep:
        xs = sorted(all_steps_by_ep.keys())
        ys = [min(all_steps_by_ep[e]) for e in xs]
        ground = Series(name="min_over_runs", xs=[float(x) for x in xs], ys=ys, extra={})

    _write_csv(out_dir / "summary.csv", rows)
    _try_plot_xy(out_dir / "compare.png", "Maze: episode steps", series, xlabel="episode", ylabel="steps", ground=ground)
    return {"summary_rows": rows, "plot": str(out_dir / "compare.png")}

# ------------------------
# RENEWAL (FSM) EVAL
# ------------------------

def eval_renewal(runs: List[Path], out_dir: Path) -> Dict[str, Any]:
    """
    Expect metrics.jsonl lines like:
      header: {"record_type":"header", ...}
      step:   {"t": <int>, "obs": <int>, "act": <int>, "reward": <0/1>, "cum_reward": <float>}
    We plot cumulative reward vs t with ideal y=t line.
    """
    _ensure_dir(out_dir)
    series: List[Series] = []
    rows: List[Dict[str, Any]] = []
    max_t = 0
    for run in runs:
        mpath = run / "metrics.jsonl"
        recs = _read_jsonl(mpath)
        xs, ys = [], []
        mismatches = 0
        steps = 0
        for r in recs:
            if r.get("record_type") == "header":
                continue
            t = int(r.get("t", 0))
            cr = float(r.get("cum_reward", 0.0))
            xs.append(float(t+1))   # human t starts at 1
            ys.append(cr)
            steps += 1
            # bookkeeping check
            reward = float(r.get("reward", 0.0))
            obs = r.get("obs", None); act = r.get("act", None)
            if obs is not None and act is not None:
                if ((reward == 1.0) != (act == obs)):
                    mismatches += 1
        if xs:
            max_t = max(max_t, int(xs[-1]))
            acc = (ys[-1] / xs[-1]) if xs[-1] > 0 else 0.0
            series.append(Series(name=run.name, xs=xs, ys=ys, extra={"final_acc": acc, "mismatches": mismatches}))
            rows.append({"run": run.name, "steps": steps, "final_cum_reward": ys[-1], "final_accuracy": acc, "mismatches": mismatches})

    # ground truth: ideal predictor would have cum_reward = t
    ground = Series(name="ideal", xs=list(range(1, max_t+1)), ys=list(range(1, max_t+1)), extra={})
    _write_csv(out_dir / "summary.csv", rows)
    _try_plot_xy(out_dir / "compare.png", "Renewal: cumulative reward", series, xlabel="t", ylabel="cum_reward", ground=ground)
    return {"summary_rows": rows, "plot": str(out_dir / "compare.png")}
