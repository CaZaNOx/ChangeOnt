# experiments/plotting/renewal.py
from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
from experiments.plotting.util import ensure_dir, write_csv, safe_import_plt

plt = safe_import_plt()

def summarize_instance(inst_dir: Path, data: Dict[str, Any]) -> None:
    eval_dir = inst_dir / "eval"
    ensure_dir(eval_dir)

    rows: List[Dict[str, Any]] = []
    for agent, d in sorted(data["agents"].items()):
        finals = d.get("finals", [])
        rows.append({
            "instance": data["instance"],
            "agent": agent,
            "mean_final_cum_reward": sum(finals)/len(finals) if finals else "",
            "n_runs": len(finals),
        })
    write_csv(eval_dir / "summary.csv", rows)

    if plt:
        plt.figure()
        for agent, d in sorted(data["agents"].items()):
            mc = d.get("mean_curve", {})
            t = mc.get("t", [])
            cm = mc.get("cum", [])
            if not t or not cm:
                continue
            plt.plot(t, cm, label=agent, linewidth=2)
        plt.xlabel("t")
        plt.ylabel("mean cumulative reward")
        plt.title(f"Renewal: {data['instance']}")
        plt.legend()
        plt.tight_layout()
        plt.savefig(eval_dir / "summary.png", dpi=160)
        plt.close()

def aggregate_family(renewal_root: Path) -> None:
    eval_dir = renewal_root / "eval"
    ensure_dir(eval_dir)

    matrix: List[Dict[str, Any]] = []
    for inst_dir in sorted(d for d in renewal_root.iterdir() if d.is_dir()):
        s = inst_dir / "eval" / "summary.csv"
        if not s.exists():
            continue
        lines = s.read_text(encoding="utf-8").splitlines()
        if not lines:
            continue
        header = lines[0].split(",")
        a_idx, m_idx = header.index("agent"), header.index("mean_final_cum_reward")
        for b in lines[1:]:
            cols = b.split(",")
            if len(cols) != len(header):
                continue
            matrix.append({"instance": inst_dir.name, "agent": cols[a_idx], "mean_final_cum_reward": float(cols[m_idx] or "nan")})

    agg: Dict[str, List[float]] = {}
    for r in matrix:
        agg.setdefault(r["agent"], []).append(r["mean_final_cum_reward"])
    fam_rows = [{
        "agent": agent,
        "family_mean_final_cum_reward": sum(v)/len(v) if v else float("nan"),
        "n_instances": len(v)
    } for agent, v in sorted(agg.items())]
    write_csv(eval_dir / "combined_summary.csv", fam_rows)

    if plt and fam_rows:
        labels = [r["agent"] for r in fam_rows]
        vals = [r["family_mean_final_cum_reward"] for r in fam_rows]
        plt.figure()
        plt.bar(range(len(labels)), vals)
        plt.xticks(range(len(labels)), labels, rotation=30, ha="right")
        plt.ylabel("mean final cumulative reward (higher is better)")
        plt.title("Renewal: aggregated over instances")
        plt.tight_layout()
        plt.savefig(eval_dir / "combined_summary.png", dpi=160)
        plt.close()
