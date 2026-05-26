# experiments/plotting/main.py
# Central orchestrator for running mode/family/suite summaries & plots.
from __future__ import annotations
import argparse
import csv
import math
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple, Sequence

from experiments.plotting.bandit import (
    aggregate_family as bandit_aggregate,
    summarize_problem as bandit_summarize_problem,
)
from experiments.plotting.maze import (
    aggregate_family as maze_aggregate,
    summarize_env as maze_summarize_env,
)
from experiments.plotting.renewal import (
    aggregate_family as renewal_aggregate,
    summarize_instance as renewal_summarize_instance,
)
from experiments.plotting.collect import (
    collect_bandit_problem,
    collect_maze_env,
    collect_renewal_instance,
)
from experiments.plotting.raster import bar_chart_png

def summarize_bandit_mode(mode_dir: Path) -> None:
    data = collect_bandit_problem(mode_dir)
    bandit_summarize_problem(mode_dir, data)

def summarize_maze_mode(mode_dir: Path) -> None:
    data = collect_maze_env(mode_dir)
    maze_summarize_env(mode_dir, data)

def summarize_renewal_mode(mode_dir: Path) -> None:
    data = collect_renewal_instance(mode_dir)
    renewal_summarize_instance(mode_dir, data)

def summarize_family(suite_root: Path, family: str) -> None:
    fam_root = suite_root / family
    if not fam_root.exists():
        return
    if family == "bandit":
        bandit_aggregate(fam_root)
    elif family == "maze":
        maze_aggregate(fam_root)
    elif family == "renewal":
        renewal_aggregate(fam_root)

def summarize_families(suite_root: Path, families: List[str]) -> None:
    for fam in families:
        summarize_family(suite_root, fam)

def _normalize_agent(name: str) -> str:
    m = re.match(r"(.+)_s\d+$", name)
    return m.group(1) if m else name

def _collect_family_scores(fam_csv_map: Dict[str, Path]) -> Dict[str, Dict[str, float]]:
    per_family_scores: Dict[str, Dict[str, float]] = {}
    for fam, fam_csv in fam_csv_map.items():
        if not fam_csv.exists():
            continue
        with fam_csv.open("r", encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        if not rows:
            continue
        scores: Dict[str, float] = {}
        if fam == "bandit":
            best, worst = None, None
            for r in rows:
                agent = r.get("agent", "")
                try:
                    val = float(r.get("family_mean_final_regret", "nan"))
                except Exception:
                    continue
                if math.isnan(val):
                    continue
                best = val if best is None else min(best, val)
                worst = val if worst is None else max(worst, val)
                scores[agent] = val
            if worst is not None and best is not None and worst > best:
                norm = {}
                for agent, val in scores.items():
                    norm_val = 1.0 - (val - best) / (worst - best)
                    norm[agent] = float(norm_val)
                per_family_scores[fam] = norm
                continue
        elif fam == "maze":
            best = None
            for r in rows:
                agent = r.get("agent", "")
                try:
                    val = float(r.get("family_mean_steps", "nan"))
                except Exception:
                    continue
                if math.isnan(val):
                    continue
                best = val if best is None else min(best, val)
                scores[agent] = val
            if best is not None:
                per_family_scores[fam] = {agent: float(min(1.0, best / val if val > 0 else 1.0)) for agent, val in scores.items()}
                continue
        elif fam == "renewal":
            best = None
            for r in rows:
                agent = r.get("agent", "")
                try:
                    val = float(r.get("family_mean_final_cum_reward", "nan"))
                except Exception:
                    continue
                if math.isnan(val):
                    continue
                best = val if best is None else max(best, val)
                scores[agent] = val
            if best is not None and best > 0:
                per_family_scores[fam] = {agent: float(val / best) for agent, val in scores.items()}
                continue
        per_family_scores[fam] = scores
    return per_family_scores

def summarize_suite(suite_root: Path, families: List[str]) -> None:
    out_dir = suite_root / "summary"
    out_dir.mkdir(parents=True, exist_ok=True)
    fam_csv_map = {
        fam: suite_root / fam / "_summary" / "combined_summary.csv"
        for fam in families
    }
    rows: List[Dict[str, Any]] = []
    found_files: List[Path] = []
    missing: List[str] = []
    for fam, fam_csv in fam_csv_map.items():
        if fam_csv.exists():
            found_files.append(fam_csv)
            with fam_csv.open("r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for rec in reader:
                    row: Dict[str, Any] = {"family": fam}
                    row.update(rec)
                    rows.append(row)
        else:
            missing.append(fam)
    out_csv = out_dir / "overall_summary.csv"
    if rows:
        headers: List[str] = []
        for r in rows:
            for k in r.keys():
                if k not in headers:
                    headers.append(k)
        with out_csv.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
    else:
        out_csv.write_text("", encoding="utf-8")
    if found_files:
        print("[overall] found:", ", ".join(str(p) for p in found_files))
    if missing:
        print("[overall] missing family combined_summary.csv for:", ", ".join(missing))

    per_family_scores = _collect_family_scores(fam_csv_map)
    families_present = [f for f in families if f in per_family_scores and per_family_scores[f]]
    overall_rows: List[Dict[str, Any]] = []
    if families_present:
        stoa_per_family: Dict[str, float] = {}
        STOA_PREFIXES = {
            "bandit": ("ucb1", "epsgreedy", "kl_ucb", "ts"),
            "maze": ("bfs", "astar"),
            "renewal": ("last", "ngram", "phase", "vom"),
        }
        for fam in families_present:
            stoa_scores = [
                score for agent, score in per_family_scores[fam].items()
                if any(agent.startswith(pref) for pref in STOA_PREFIXES.get(fam, ()))
            ]
            if stoa_scores:
                stoa_per_family[fam] = max(stoa_scores)
        if stoa_per_family:
            overall_stoa = sum(stoa_per_family.values()) / len(stoa_per_family)
            row = {"agent": "STOA_BEST", "overall_accuracy": overall_stoa}
            for fam, v in stoa_per_family.items():
                row[f"{fam}_acc"] = v
            overall_rows.append(row)
    co_family_scores: Dict[str, Dict[str, List[float]]] = {}
    for fam in families_present:
        for agent, score in per_family_scores[fam].items():
            norm = _normalize_agent(agent)
            co_family_scores.setdefault(norm, {}).setdefault(fam, []).append(score)
    for name, fam_scores in co_family_scores.items():
        vals = []
        row = {"agent": name}
        for fam, scores in fam_scores.items():
            avg = sum(scores) / len(scores)
            row[f"{fam}_score"] = float(avg)
            vals.append(avg)
        if vals:
            row["overall_score"] = sum(vals) / len(vals)
            overall_rows.append(row)
    out_csv2 = out_dir / "overall_stoa_vs_co.csv"
    if overall_rows:
        headers: List[str] = []
        for r in overall_rows:
            for k in r.keys():
                if k not in headers:
                    headers.append(k)
        with out_csv2.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(overall_rows)
    else:
        out_csv2.write_text("", encoding="utf-8")
    labels = [r["agent"] for r in overall_rows if "overall_accuracy" in r]
    vals = [r["overall_accuracy"] for r in overall_rows if "overall_accuracy" in r]
    if vals:
        bar_chart_png(out_dir / "overall_stoa_vs_co.png", labels, vals, "STOA vs CO (overall)", "overall accuracy")
    bar_chart_svg(out_dir / "overall_stoa_vs_co.svg", labels, vals, "STOA vs CO (overall)", "overall accuracy")
    co_rows_by_family: List[Dict[str, Any]] = []
    for fam in families_present:
        for agent, score in per_family_scores[fam].items():
            if not any(agent.startswith(pref) for pref in ("ucb1", "epsgreedy", "kl_ucb", "ts", "bfs", "astar", "last", "ngram", "phase", "vom")):
                co_rows_by_family.append({"family": fam, "agent": agent, "normalized_score": score})
    out_co_overall = out_dir / "co_competition_overall.csv"
    co_rows_overall: List[Dict[str, Any]] = []
    for name, fam_scores in co_family_scores.items():
        row = {"agent": name}
        vals = []
        for fam, scores in fam_scores.items():
            val = sum(scores) / len(scores)
            row[f"{fam}_score"] = float(val)
            vals.append(val)
        if vals:
            row["overall_score"] = sum(vals) / len(vals)
            co_rows_overall.append(row)
    if co_rows_overall:
        headers: List[str] = []
        for r in co_rows_overall:
            for k in r.keys():
                if k not in headers:
                    headers.append(k)
        with out_co_overall.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(co_rows_overall)
    else:
        out_co_overall.write_text("", encoding="utf-8")
    labels = [r["agent"] for r in co_rows_overall if "overall_score" in r]
    vals = [r["overall_score"] for r in co_rows_overall if "overall_score" in r]
    if vals:
        bar_chart_png(out_dir / "co_competition_overall.png", labels, vals, "CO Competition (overall)", "overall score")
    bar_chart_svg(out_dir / "co_competition_overall.svg", labels, vals, "CO Competition (overall)", "overall score")
    out_co_family = out_dir / "co_competition_by_family.csv"
    if co_rows_by_family:
        with out_co_family.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["family", "agent", "normalized_score"])
            writer.writeheader()
            writer.writerows(co_rows_by_family)
    else:
        out_co_family.write_text("", encoding="utf-8")
    fams = [fam for fam in families_present if any(r["family"] == fam for r in co_rows_by_family)]
    rows_by_family = {fam: [r for r in co_rows_by_family if r["family"] == fam] for fam in fams}
    if fams and any(rows_by_family.values()):
        bar_chart_png(
            out_dir / "co_competition_by_family.png",
            [f for f in fams for _ in rows_by_family[f]],
            [r["normalized_score"] for f in fams for r in rows_by_family[f]],
            "CO Competition by Family",
            "normalized score",
        )
    family_labels = []
    family_vals = []
    for fam in fams:
        for r in rows_by_family.get(fam, []):
            family_labels.append(f"{fam}:{r['agent']}")
            family_vals.append(r["normalized_score"])
    bar_chart_svg(out_dir / "co_competition_by_family.svg", family_labels, family_vals, "CO Competition by Family", "normalized score")

def bar_chart_svg(out_path: Path, labels: List[str], values: List[float], title: str, ylabel: str) -> None:
    if not labels or not values:
        out_path.write_text("", encoding="utf-8")
        return
    width = max(480, 80 * len(labels))
    height = 320
    bars = []
    for idx, (label, value) in enumerate(zip(labels, values)):
        bars.append(f'<rect x="{50 + idx*40}" y="{height - 60 - int(value*180)}" width="30" height="{int(value*180)}" fill="#4c78a8" />')
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        f'<rect x="0" y="0" width="{width}" height="{height}" fill="#111f2b"/>',
        f'<text x="{width/2:.1f}" y="24" text-anchor="middle" font-size="18" fill="#fff">{title}</text>',
        f'<text x="{width - 60:.1f}" y="40" text-anchor="middle" font-size="12" fill="#eee">{ylabel}</text>',
        *bars,
        '</svg>'
    ]
    out_path.write_text("\n".join(svg), encoding="utf-8")

def main() -> None:
    ap = argparse.ArgumentParser(description="Plotting & summaries")
    ap.add_argument("cmd", choices=["summarize-family", "summarize-suite"])
    ap.add_argument("--suite-root", type=str, default="outputs/suite")
    ap.add_argument("--family", type=str, default="bandit")
    ap.add_argument("--families", type=str, default="bandit,maze,renewal")
    args = ap.parse_args()
    root = Path(args.suite_root)
    if args.cmd == "summarize-family":
        summarize_family(root, args.family)
    elif args.cmd == "summarize-suite":
        fams = [s.strip() for s in args.families.split(",") if s.strip()]
        summarize_families(root, fams)
        summarize_suite(root, fams)

if __name__ == "__main__":
    main()
