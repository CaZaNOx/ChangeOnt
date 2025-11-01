# experiments/plotting/bandit.py
from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List, Tuple
from experiments.plotting.util import ensure_dir, write_csv, safe_import_plt

plt = safe_import_plt()

def summarize_problem(problem_dir: Path, data: Dict[str, Any]) -> None:
    summary_dir = problem_dir / "_summary"
    ensure_dir(summary_dir)

    rows: List[Dict[str, Any]] = []
    for agent, d in sorted(data["agents"].items()):
        finals = d.get("final_regrets", [])
        rows.append({
            "problem": data["problem"],
            "agent": agent,
            "mean_final_regret": sum(finals)/len(finals) if finals else "",
            "n_runs": len(finals),
        })
    write_csv(summary_dir / "summary.csv", rows)

    if plt:
        plt.figure()
        for agent, d in sorted(data["agents"].items()):
            mc = d.get("mean_curve", {})
            t = mc.get("t", [])
            reg = mc.get("regret", [])
            if not t or not reg:
                continue
            plt.plot(t, reg, label=agent, linewidth=2)
        plt.xlabel("t")
        plt.ylabel("mean cumulative regret")
        plt.title(f"Bandit: {data['problem']}")
        plt.legend()
        plt.tight_layout()
        plt.savefig(summary_dir / "summary.png", dpi=160)
        plt.close()

def aggregate_family(bandit_root: Path) -> None:
    # combine all problem summaries into a family-level summary & plot
    summary_dir = bandit_root / "_summary"
    ensure_dir(summary_dir)

    # load each problem summary
    per_problem: List[Tuple[str, List[Dict[str, Any]]]] = []
    for problem_dir in sorted(d for d in bandit_root.iterdir() if d.is_dir()):
        s = problem_dir / "_summary" / "summary.csv"
        if s.exists():
            rows = [r.strip().split(",") for r in s.read_text(encoding="utf-8").splitlines()]
            if rows and rows[0] and rows[0][0].startswith("problem"):
                hdr = rows[0]
                idx_agent = hdr.index("agent")
                idx_mean = hdr.index("mean_final_regret")
                body = rows[1:]
                per_problem.append((problem_dir.name, [
                    {"agent": b[idx_agent], "mean_final_regret": float(b[idx_mean]) if b[idx_mean] else float("nan")}
                    for b in body if len(b) == len(hdr)
                ]))

    # average (over problems) mean_final_regret per agent
    agg: Dict[str, List[float]] = {}
    for _, rows in per_problem:
        for r in rows:
            agg.setdefault(r["agent"], []).append(r["mean_final_regret"])
    fam_rows = [{
        "agent": agent,
        "family_mean_final_regret": sum(v)/len(v) if v else float("nan"),
        "n_problems": len(v)
    } for agent, v in sorted(agg.items())]
    write_csv(summary_dir / "combined_summary.csv", fam_rows)

    if plt and fam_rows:
        agents = [r["agent"] for r in fam_rows]
        vals = [r["family_mean_final_regret"] for r in fam_rows]
        plt.figure()
        plt.bar(range(len(agents)), vals)
        plt.xticks(range(len(agents)), agents, rotation=30, ha="right")
        plt.ylabel("mean final regret (lower is better)")
        plt.title("Bandit: aggregated over problems")
        plt.tight_layout()
        plt.savefig(summary_dir / "combined_summary.png", dpi=160)
        plt.close()
 