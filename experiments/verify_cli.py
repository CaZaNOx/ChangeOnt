# experiments/verify_cli.py
from __future__ import annotations
import argparse, yaml
from pathlib import Path
from typing import Any, Dict

from experiments.suites.bandit import run_family as run_bandit
from experiments.suites.maze import run_family as run_maze
from experiments.suites.renewal import run_family as run_renewal

def main() -> None:
    ap = argparse.ArgumentParser(description="Verification suites: run problems, evaluate, and summarize.")
    ap.add_argument("--suite", type=str, choices=["bandit", "maze", "renewal", "all"], default="all")
    ap.add_argument("--config", type=str, required=True)
    ap.add_argument("--out_root", type=str, default="outputs/suite")
    args = ap.parse_args()

    cfg: Dict[str, Any] = yaml.safe_load(Path(args.config).read_text(encoding="utf-8")) or {}
    # Always run cheap first (renewal/maze), bandit last
    order = ["renewal", "maze", "bandit"] if args.suite == "all" else [args.suite]

    root = Path(args.out_root)
    root.mkdir(parents=True, exist_ok=True)

    for suite in order:
        if suite == "bandit":
            run_bandit(root, cfg.get("bandit", {}))
            print(f"[verify] bandit -> {root/'bandit'/'summary.csv'}")
        elif suite == "maze":
            run_maze(root, cfg.get("maze", {}))
            print(f"[verify] maze -> {root/'maze'/'summary.csv'}")
        elif suite == "renewal":
            run_renewal(root, cfg.get("renewal", {}))
            print(f"[verify] renewal -> {root/'renewal'/'summary_runs.csv'}")
            print(f"[verify] renewal -> {root/'renewal'/'summary_rel.csv'}")

if __name__ == "__main__":
    main()
