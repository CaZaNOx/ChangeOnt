#!/usr/bin/env bash  
set -euo pipefail  
RUN_DIR="${1:-outputs/toy_ren_haq_vs_fsm}"  
OUT="${2:-${RUN_DIR}/report.md}"  
python evaluation/reports/build_report.py --run_dir "$RUN_DIR" --out "$OUT"  
echo "Wrote report to: $OUT"