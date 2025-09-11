from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

def run(cmd: list[str]):
    print(">>", " ".join(cmd), flush=True)
    proc = subprocess.run(cmd, cwd=ROOT)
    if proc.returncode != 0:
        sys.exit(proc.returncode)


def last_metric_value(path: Path, metric: str, key: str):
    val = None
    for line in path.read_text(encoding="utf-8").splitlines():
        rec = json.loads(line)
        if rec.get("metric") == metric:
            val = rec.get(key)
    return val


def theil_sen(xs, ys):
    # simple O(n^2) Theil–Sen; fine for our lengths
    slopes = []
    n = len(xs)
    for i in range(n):
        for j in range(i + 1, n):
            dx = xs[j] - xs[i]
            if dx != 0:
                slopes.append((ys[j] - ys[i]) / dx)
    slopes.sort()
    return slopes[len(slopes)//2] if slopes else float("nan")


def slope_ln(metrics_path: Path):
    xs, ys = [], []
    for line in metrics_path.read_text(encoding="utf-8").splitlines():
        rec = json.loads(line)
        if rec.get("metric") == "cumulative_regret":
            t = rec["t"]
            if t > 1:
                xs.append(math.log(t))
                ys.append(rec["value"])
    return theil_sen(xs, ys)


def main():
    # Bandit UCB1 @5k and @10k, and eps-greedy @5k
    run([sys.executable, "-m", "experiments.runners.bandit_runner",
         "--agent", "ucb1", "--probs", "0.1,0.2,0.8", "--horizon", "5000",
         "--out", "outputs/bandit_ucb_T5000"])
    run([sys.executable, "-m", "experiments.runners.bandit_runner",
         "--agent", "ucb1", "--probs", "0.1,0.2,0.8", "--horizon", "10000",
         "--out", "outputs/bandit_ucb_T10000"])
    run([sys.executable, "-m", "experiments.runners.bandit_runner",
         "--config", "experiments/configs/bandit_eps.yaml"])

    # Maze BFS (5 episodes)
    run([sys.executable, "-m", "experiments.runners.maze_runner",
         "--episodes", "5", "--out", "outputs/maze_bfs"])

    # --- Checks ---
    # UCB1 ratio and slopes
    m5 = ROOT / "outputs/bandit_ucb_T5000/metrics.jsonl"
    m10 = ROOT / "outputs/bandit_ucb_T10000/metrics.jsonl"
    reg5 = last_metric_value(m5, "cumulative_regret", "value")
    reg10 = last_metric_value(m10, "cumulative_regret", "value")
    ratio = float(reg10) / float(reg5)
    slope5 = slope_ln(m5)
    slope10 = slope_ln(m10)

    # ε-greedy final regret
    meps = ROOT / "outputs/bandit_eps_T5000/metrics.jsonl"
    regeps = last_metric_value(meps, "cumulative_regret", "value")

    # Maze steps/return first episode
    maze_metrics = ROOT / "outputs/maze_bfs/metrics.jsonl"
    ep_steps = None
    ep_return = None
    for line in maze_metrics.read_text(encoding="utf-8").splitlines():
        rec = json.loads(line)
        if rec.get("episode") == 0 and rec.get("metric") == "episode_steps":
            ep_steps = rec["value"]
        if rec.get("episode") == 0 and rec.get("metric") == "episode_return":
            ep_return = rec["value"]

    summary = {
        "bandit": {
            "ucb1": {"regret5k": reg5, "regret10k": reg10, "ratio10k_over_5k": ratio,
                     "slope_ln_5k": slope5, "slope_ln_10k": slope10},
            "epsgreedy": {"regret5k": regeps}
        },
        "maze": {"episode0_steps": ep_steps, "episode0_return": ep_return}
    }
    outp = ROOT / "outputs/smoke_summary.json"
    outp.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))

    # Hard, falsifiable expectations:
    expected = math.log(10000.0) / math.log(5000.0)  # ~1.081
    tol = 0.10 # +/- 10% tolerance
    low, high = expected * (1 - tol), expected * (1 + tol)
    
    failures = []
    if not (low <= ratio <= high):
        failures.append(f"UCB1 ratio expected in [{low:.3f},{high:.3f}] " f"(~log(10k)/log(5k)), got {ratio:.3f}")
    if regeps <= reg5:
        failures.append(f"ε-greedy regret should exceed UCB1 (got eps={regeps:.2f}, ucb={reg5:.2f})")
    if ep_steps is None:
        failures.append("maze episode_steps missing")
    # If you standardized reward to -1/step, enforce equality:
    # if ep_return != -ep_steps:
    #     failures.append(f"maze return mismatch: return={ep_return}, steps={ep_steps}")

    if failures:
        print("\nFAIL:", *failures, sep="\n- ")
        sys.exit(2)
    print("\nPASS: baselines within expected bands.")


if __name__ == "__main__":
    main()
