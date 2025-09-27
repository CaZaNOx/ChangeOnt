# experiments/suites/renewal.py
from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
from .common import run_module, tmp_yaml, ensure_dir
from experiments.eval.renewal import evaluate_run, summarize_agent_vs_agent, summarize_phase_vs_last

def run_family(root: Path, spec: Dict[str, Any]) -> None:
    out_dir = root / "renewal"
    ensure_dir(out_dir)
    rows: List[Dict[str, Any]] = []

    instances: Dict[str, Any] = spec.get("instances", {})
    for inst_name, inst_cfg in instances.items():
        agents: List[str] = list(inst_cfg.get("agents", ["last", "phase", "ngram"]))
        seeds: List[int] = list(inst_cfg.get("seeds", [7]))
        env = inst_cfg.get("env", {})

        for agent in agents:
            for seed in seeds:
                run_dir = out_dir / inst_name / f"{agent}_s{seed}"
                cfg = {
                    "seed": int(seed),
                    "steps": int(env.get("T_max", 1000)),
                    "mode": agent,
                    "env": env,
                    "out_dir": str(run_dir),
                }
                tmp = tmp_yaml(cfg, run_dir / "_tmp.yaml")
                run_dir.mkdir(parents=True, exist_ok=True)
                run_module("experiments.runners.renewal_runner", "--config", str(tmp))
                metrics = run_dir / "metrics.jsonl"
                rows.append(
                    evaluate_run(metrics, "renewal", inst_name, agent, seed)
                )

    summarize_agent_vs_agent(rows, out_dir / "summary_runs.csv")
    summarize_phase_vs_last(rows, out_dir / "summary_rel.csv")
