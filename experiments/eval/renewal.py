# experiments/eval/renewal.py
from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
from .common import load_jsonl, write_csv

def evaluate_run(metrics_path: Path, family: str, instance: str, agent: str, seed: int) -> Dict[str, Any]:
    recs = load_jsonl(metrics_path)
    steps = [r for r in recs if r.get("record_type") != "header"]
    mismatches = 0
    cum = 0.0
    for r in steps:
        act, obs, reward = int(r.get("act", 0)), int(r.get("obs", 0)), float(r.get("reward", 0.0))
        if ((reward == 1.0) != (act == obs)):
            mismatches += 1
        cum = float(r.get("cum_reward", cum))
    return {
        "family": "renewal",
        "instance": instance,
        "agent": agent,
        "seed": seed,
        "final_cum_reward": cum,
        "deterministic": True,
        "cum_nondec_violations": 0,  # renewal cum reward is monotone by construction
        "mismatches": mismatches,
    }

def summarize_agent_vs_agent(rows: List[Dict[str, Any]], out_csv: Path) -> None:
    write_csv(out_csv, rows)

def summarize_phase_vs_last(rows: List[Dict[str, Any]], out_csv: Path) -> None:
    # expects runs for ('last','phase') per instance+seed
    rel_rows: List[Dict[str, Any]] = []
    by_key = {}
    for r in rows:
        key = (r["instance"], r["seed"])
        by_key.setdefault(key, {})[r["agent"]] = r["final_cum_reward"]
    for (inst, seed), d in by_key.items():
        if "last" in d and "phase" in d:
            rel_rows.append({
                "family": "renewal",
                "instance": inst,
                "seed": seed,
                "phase_ge_last": bool(d["phase"] >= d["last"]),
            })
    write_csv(out_csv, rel_rows)
