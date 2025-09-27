# experiments/suites/bandit.py
from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
from .common import run_module, tmp_yaml, ensure_dir
from experiments.eval.bandit import evaluate_run, summarize

def run_family(root: Path, spec: Dict[str, Any]) -> None:
    out_dir = root / "bandit"
    ensure_dir(out_dir)
    rows: List[Dict[str, Any]] = []

    problems: Dict[str, Any] = spec.get("problems", {})
    agents: List[str] = list(spec.get("agents", []))
    seeds: List[int] = list(spec.get("seeds", [7]))

    for prob_name, prob_cfg in problems.items():
        for agent in agents:
            for seed in seeds:
                run_dir = out_dir / prob_name / f"{agent}_s{seed}"
                cfg = {
                    "agent": {"type": agent},
                    "env": {"probs": list(prob_cfg["probs"]), "horizon": int(prob_cfg["horizon"])},
                    "seed": int(seed),
                    "out": str(run_dir),
                }
                tmp = tmp_yaml(cfg, run_dir / "_tmp.yaml")
                run_dir.mkdir(parents=True, exist_ok=True)
                run_module("experiments.runners.bandit_runner", "--config", str(tmp))
                metrics = run_dir / "metrics.jsonl"
                rows.append(
                    evaluate_run(metrics, "bandit", prob_name, agent, seed, int(prob_cfg["horizon"]))
                )

    summarize(rows, out_dir / "summary.csv")
