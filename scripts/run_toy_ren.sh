#!/usr/bin/env bash
set -e
source .venv/bin/activate
python experiments/run_experiment.py --config experiments/configs/toy_ren_haq_vs_fsm.yaml