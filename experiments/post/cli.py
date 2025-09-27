# experiments/post/cli.py
from __future__ import annotations
import argparse
from pathlib import Path

from experiments.post.collect import collect_bandit_problem, collect_maze_env, collect_renewal_instance
from experiments.post.plot import plot_bandit, plot_maze, plot_renewal


def summarize(suite_root: Path) -> None:
    # BANDIT
    bandit_root = suite_root / "bandit"
    if bandit_root.exists():
        for problem_dir in sorted(d for d in bandit_root.iterdir() if d.is_dir()):
            data = collect_bandit_problem(problem_dir)
            plot_bandit(problem_dir, data)
            print(f"[post] bandit -> {problem_dir/'eval'}")

    # MAZE
    maze_root = suite_root / "maze"
    if maze_root.exists():
        for env_dir in sorted(d for d in maze_root.iterdir() if d.is_dir()):
            data = collect_maze_env(env_dir)
            plot_maze(env_dir, data)
            print(f"[post] maze -> {env_dir/'eval'}")

    # RENEWAL
    renewal_root = suite_root / "renewal"
    if renewal_root.exists():
        for inst_dir in sorted(d for d in renewal_root.iterdir() if d.is_dir()):
            data = collect_renewal_instance(inst_dir)
            plot_renewal(inst_dir, data)
            print(f"[post] renewal -> {inst_dir/'eval'}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Post-processing for experiments (summaries and plots).")
    ap.add_argument("cmd", choices=["summarize"], help="What to do.")
    ap.add_argument("--suite-root", type=str, default="outputs/suite", help="Root where runs were written.")
    args = ap.parse_args()

    root = Path(args.suite_root)
    root.mkdir(parents=True, exist_ok=True)

    if args.cmd == "summarize":
        summarize(root)


if __name__ == "__main__":
    main()
