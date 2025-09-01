# FILE: scripts/run_toy_ren.ps1
python -m experiments.run_experiment --config experiments\configs\toy_ren_haq_vs_fsm.yaml

# Optional plots (requires matplotlib)
python - << 'PY'
from experiments.logging.plots import plot_rewards, plot_flip_event_alignment
plot_rewards("outputs/run_haq.jsonl", "outputs/plot_rewards_haq.png", title="HAQ rewards")
plot_rewards("outputs/run_fsm.jsonl", "outputs/plot_rewards_fsm.png", title="FSM rewards")
plot_flip_event_alignment("outputs/run_haq.jsonl", "outputs/plot_align_haq.png", delta=6)
print("Saved plots in outputs/")
PY


# BEGIN FILE: scripts/run_examples.sh

#!/usr/bin/env bash  
set -euo pipefail

OUTDIR="${1:-outputs}"

echo "[*] Running renewal (FSM)…"  
python experiments/run_experiment.py --config experiments/configs/toy_ren_haq_vs_fsm.yaml --out_dir "$OUTDIR"

echo "[*] Running bandit (UCB)…"  
python experiments/run_experiment.py --config experiments/configs/bandit_ucb.yaml --out_dir "$OUTDIR"

echo "[*] Running maze (BFS)…"  
python experiments/run_experiment.py --config experiments/configs/maze_bfs.yaml --out_dir "$OUTDIR"