# experiments/plotting/main.py
from __future__ import annotations
import argparse
from pathlib import Path
from typing import List

from experiments.plotting.collect import (
    collect_bandit_problem, collect_maze_env, collect_renewal_instance
)
from experiments.plotting.bandit import summarize_problem as bandit_summarize_problem, aggregate_family as bandit_aggregate
from experiments.plotting.maze import summarize_env as maze_summarize_env, aggregate_family as maze_aggregate
from experiments.plotting.renewal import summarize_instance as renewal_summarize_instance, aggregate_family as renewal_aggregate

def summarize_family(suite_root: Path, family: str) -> None:
    fam_root = suite_root / family
    if not fam_root.exists():
        return

    if family == "bandit":
        for problem_dir in sorted(d for d in fam_root.iterdir() if d.is_dir()):
            data = collect_bandit_problem(problem_dir)
            bandit_summarize_problem(problem_dir, data)
        bandit_aggregate(fam_root)

    elif family == "maze":
        for env_dir in sorted(d for d in fam_root.iterdir() if d.is_dir()):
            data = collect_maze_env(env_dir)
            maze_summarize_env(env_dir, data)
        maze_aggregate(fam_root)

    elif family == "renewal":
        for inst_dir in sorted(d for d in fam_root.iterdir() if d.is_dir()):
            data = collect_renewal_instance(inst_dir)
            renewal_summarize_instance(inst_dir, data)
        renewal_aggregate(fam_root)

def summarize_families(suite_root: Path, families: List[str]) -> None:
    for fam in families:
        summarize_family(suite_root, fam)

def main() -> None:
    ap = argparse.ArgumentParser(description="Plotting & summaries")
    ap.add_argument("cmd", choices=["summarize"])
    ap.add_argument("--suite-root", type=str, default="outputs/suite")
    ap.add_argument("--families", type=str, default="bandit,maze,renewal")
    args = ap.parse_args()

    root = Path(args.suite_root)
    fams = [s.strip() for s in args.families.split(",") if s.strip()]

    if args.cmd == "summarize":
        summarize_families(root, fams)

if __name__ == "__main__":
    main()
