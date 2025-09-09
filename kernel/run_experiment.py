from __future__ import annotations
import argparse, json
from experiments.runners.renewal_runner import RunnerConfig, run

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=500)
    ap.add_argument("--seed", type=int, default=1729)
    ap.add_argument("--phase-len", type=int, default=50)
    ap.add_argument("--out-dir", type=str, default="outputs")
    args = ap.parse_args()
    cfg = RunnerConfig(steps=args.steps, seed=args.seed, phase_len=args.phase_len, out_dir=args.out_dir)
    paths = run(cfg)
    print(json.dumps(paths, indent=2))

if __name__ == "__main__":
    main()
