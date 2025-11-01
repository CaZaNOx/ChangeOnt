# experiments/plotting/main.py
# Centralized summary wrappers + suite-level aggregator.
from __future__ import annotations
import argparse
import csv
from pathlib import Path
from typing import List, Dict, Any, Tuple

# Collectors
from experiments.plotting.collect import (
    collect_bandit_problem,
    collect_maze_env,
    collect_renewal_instance,
)

# Per-family summarizers & aggregators
from experiments.plotting.bandit import (
    summarize_problem as bandit_summarize_problem,
    aggregate_family as bandit_aggregate,
)
from experiments.plotting.maze import (
    summarize_env as maze_summarize_env,
    aggregate_family as maze_aggregate,
)
from experiments.plotting.renewal import (
    summarize_instance as renewal_summarize_instance,
    aggregate_family as renewal_aggregate,
)

# ---------- PER-MODE WRAPPERS (called by suite_cli right after each mode finishes) ----------

def summarize_bandit_mode(mode_dir: Path) -> None:
    data = collect_bandit_problem(mode_dir)
    bandit_summarize_problem(mode_dir, data)

def summarize_maze_mode(mode_dir: Path) -> None:
    data = collect_maze_env(mode_dir)
    maze_summarize_env(mode_dir, data)

def summarize_renewal_mode(mode_dir: Path) -> None:
    data = collect_renewal_instance(mode_dir)
    renewal_summarize_instance(mode_dir, data)

# ---------- PER-FAMILY AGGREGATION (called once per family after all modes finished) ----------

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

# ---------- SUITE-LEVEL AGGREGATION (optional; called once at end) ----------

def _read_csv_as_dicts(path: Path) -> Tuple[List[str], List[Dict[str, str]]]:
    if not path.exists():
        return [], []
    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        rows = [dict(row) for row in r]
        return r.fieldnames or [], rows

# experiments/plotting/main.py  (replace summarize_suite with this enhanced version)
def summarize_suite(suite_root: Path, families: List[str]) -> None:
    """
    1) Concatenate each family's <family>/summary/combined_summary.csv into
       <suite_root>/summary/overall_summary.csv  (what you had before).
    2) Build a STOA-vs-CO comparison with a simple, family-local normalization:
         - bandit:    accuracy = 1 - minmax_norm(family_mean_final_regret)
         - maze:      accuracy = min_steps / family_mean_steps
         - renewal:   accuracy = family_mean_final_cum_reward / max_reward
       Then average across families → overall accuracy.
       Writes <suite_root>/summary/overall_stoa_vs_co.csv (+ .png).
    """
    out_dir = suite_root / "summary"
    out_dir.mkdir(parents=True, exist_ok=True)

    # ---- (1) keep your existing "overall_summary.csv" behavior ----
    import csv, math
    rows: List[Dict[str, Any]] = []
    found_files: List[Path] = []
    missing: List[str] = []

    fam_csv_map: Dict[str, Path] = {
        fam: suite_root / fam / "summary" / "combined_summary.csv"
        for fam in families
    }

    for fam, fam_csv in fam_csv_map.items():
        if fam_csv.exists():
            found_files.append(fam_csv)
            with fam_csv.open("r", encoding="utf-8", newline="") as f:
                r = csv.DictReader(f)
                for rec in r:
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
            w = csv.DictWriter(f, fieldnames=headers)
            w.writeheader()
            w.writerows(rows)
    else:
        with out_csv.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["family", "agent"])
            w.writeheader()

    if found_files:
        print("[overall] found:", ", ".join(str(p) for p in found_files))
    if missing:
        print("[overall] missing family combined_summary.csv for:", ", ".join(missing))

    # ---- (2) STOA vs CO overall scoring using current family combined summaries ----
    # Identify STOA agent labels by family (name prefixes). Expand as you add more STOAs.
    STOA_PREFIXES = {
        "bandit":  ("ucb1", "epsgreedy", "kl_ucb", "ts"),
        "maze":    ("bfs", "astar"),
        "renewal": ("last", "ngram", "phase", "vom"),
    }

    # Load each family's combined_summary again, compute a normalized "accuracy"
    # per agent suitable for averaging across families (but based on per-family scaling).
    per_family_scores: Dict[str, Dict[str, float]] = {}  # family -> {agent -> accuracy}

    def _read_rows(p: Path) -> List[Dict[str, Any]]:
        if not p.exists():
            return []
        with p.open("r", encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))

    for fam, fam_csv in fam_csv_map.items():
        R = _read_rows(fam_csv)
        if not R:
            continue

        # make an agent->value map for the family, according to the family metric
        fam_scores: Dict[str, float] = {}
        if fam == "bandit":
            # column: family_mean_final_regret (lower is better)
            vals = []
            for r in R:
                a = r.get("agent", "")
                v = r.get("family_mean_final_regret", "")
                try:
                    v = float(v)
                    if math.isfinite(v):
                        vals.append((a, v))
                except Exception:
                    pass
            if vals:
                regrets = [v for _, v in vals]
                vmin, vmax = min(regrets), max(regrets)
                for a, v in vals:
                    if vmax > vmin:
                        acc = 1.0 - (v - vmin) / (vmax - vmin)
                    else:
                        acc = 1.0  # all equal
                    fam_scores[a] = float(acc)

        elif fam == "maze":
            # column: family_mean_steps (lower is better)
            vals = []
            for r in R:
                a = r.get("agent", "")
                v = r.get("family_mean_steps", "")
                try:
                    v = float(v)
                    if math.isfinite(v):
                        vals.append((a, v))
                except Exception:
                    pass
            if vals:
                min_steps = min(v for _, v in vals)
                for a, v in vals:
                    # accuracy = optimal/observed, capped to 1.0
                    fam_scores[a] = float(min(1.0, (min_steps / v) if v > 0 else 1.0))

        elif fam == "renewal":
            # column: family_mean_final_cum_reward (higher is better)
            vals = []
            for r in R:
                a = r.get("agent", "")
                v = r.get("family_mean_final_cum_reward", "")
                try:
                    v = float(v)
                    if math.isfinite(v):
                        vals.append((a, v))
                except Exception:
                    pass
            if vals:
                max_reward = max(v for _, v in vals)
                for a, v in vals:
                    fam_scores[a] = float((v / max_reward) if max_reward > 0 else 0.0)

        per_family_scores[fam] = fam_scores

    # Aggregate to overall: best STOA per family vs each CO agent (if any).
    # CO agents are any agent not matching a known STOA prefix for that family.
    overall_rows: List[Dict[str, Any]] = []
    families_present = [f for f in families if f in per_family_scores and per_family_scores[f]]

    if families_present:
        # STOA best per family
        stoa_per_family: Dict[str, float] = {}
        for fam in families_present:
            fam_scores = per_family_scores[fam]
            prefixes = STOA_PREFIXES.get(fam, tuple())
            stoa_scores = [v for a, v in fam_scores.items() if any(a.startswith(p) for p in prefixes)]
            if stoa_scores:
                stoa_per_family[fam] = max(stoa_scores)

        if stoa_per_family:
            overall_stoa = sum(stoa_per_family.values()) / len(stoa_per_family)
            row = {"agent": "STOA_BEST", "overall_accuracy": overall_stoa}
            for fam in families_present:
                if fam in stoa_per_family:
                    row[f"{fam}_acc"] = stoa_per_family[fam]
            overall_rows.append(row)

        # Collect all candidate CO agent names across families
        co_names: set[str] = set()
        for fam in families_present:
            fam_scores = per_family_scores[fam]
            prefixes = STOA_PREFIXES.get(fam, tuple())
            for a in fam_scores.keys():
                if not any(a.startswith(p) for p in prefixes):
                    co_names.add(a)

        # For each CO name, average across families where it appears
        for co in sorted(co_names):
            vals = []
            row = {"agent": co}
            for fam in families_present:
                v = per_family_scores[fam].get(co)
                if v is not None and math.isfinite(v):
                    vals.append(v)
                    row[f"{fam}_acc"] = v
            if vals:
                row["overall_accuracy"] = sum(vals) / len(vals)
                overall_rows.append(row)

    # Write STOA vs CO CSV
    out_csv2 = out_dir / "overall_stoa_vs_co.csv"
    if overall_rows:
        headers: List[str] = []
        for r in overall_rows:
            for k in r.keys():
                if k not in headers:
                    headers.append(k)
        with out_csv2.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=headers)
            w.writeheader()
            w.writerows(overall_rows)
    else:
        # still write empty header so downstream readers don't crash
        with out_csv2.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["agent", "overall_accuracy"])
            w.writeheader()

    # Simple bar plot for STOA vs CO (if any)
    if overall_rows:
        try:
            import matplotlib.pyplot as plt
            labels = [r["agent"] for r in overall_rows if "overall_accuracy" in r]
            vals   = [r["overall_accuracy"] for r in overall_rows if "overall_accuracy" in r]
            if vals:
                plt.figure(figsize=(8, 4))
                plt.bar(range(len(vals)), vals)
                plt.xticks(range(len(vals)), labels, rotation=30, ha="right")
                plt.ylabel("overall accuracy (normalized per family)")
                plt.title("STOA vs CO (overall)")
                plt.tight_layout()
                plt.savefig(out_dir / "overall_stoa_vs_co.png", dpi=160)
                plt.close()
        except Exception:
            pass


# ---------- CLI (kept for manual runs if desired) ----------

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
        summarize_suite(root, fams)

if __name__ == "__main__":
    main()
