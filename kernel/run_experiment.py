from __future__ import annotations
import argparse
import subprocess
from pathlib import Path

def main() -> None:
    ap = argparse.ArgumentParser(description="Thin dispatcher to specific runners")
    ap.add_argument("--runner", type=str, required=True, choices=["bandit", "maze", "renewal"])
    ap.add_argument("--config", type=str, default=None, help="YAML/JSON config file for the runner")
    ap.add_argument("--out", type=str, default=None, help="output directory override")
    args, unknown = ap.parse_known_args()

    cmd = ["python", "-m"]
    if args.runner == "bandit":
        cmd += ["experiments.runners.bandit_runner"]
    elif args.runner == "maze":
        cmd += ["experiments.runners.maze_runner"]
    elif args.runner == "renewal":
        cmd += ["experiments.runners.renewal_runner"]
    if args.config:
        cmd += ["--config", args.config]
    if args.out:
        cmd += ["--out", args.out]
    cmd += unknown  # allow passing runner-specific flags

    Path("outputs").mkdir(exist_ok=True)
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    main()
