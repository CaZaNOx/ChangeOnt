# FILE: scripts/run_toy_ren.sh
#!/usr/bin/env bash
set -euo pipefail
python -m experiments.run_experiment --config experiments/configs/toy_ren_haq_vs_fsm.yaml

# Optional plots (requires matplotlib)
python - <<'PY'
from experiments.logging.plots import plot_rewards, plot_flip_event_alignment
plot_rewards("outputs/run_haq.jsonl", "outputs/plot_rewards_haq.png", title="HAQ rewards")
plot_rewards("outputs/run_fsm.jsonl", "outputs/plot_rewards_fsm.png", title="FSM rewards")
plot_flip_event_alignment("outputs/run_haq.jsonl", "outputs/plot_align_haq.png", delta=6)
print("Saved plots in outputs/")
PY

#!/usr/bin/env bash  
set -euo pipefail  
python experiments/run_experiment.py --config experiments/configs/toy_ren_haq_vs_fsm.yaml  
echo ""  
echo "Wrote JSONLs under outputs/toy_ren_haq_vs_fsm/"