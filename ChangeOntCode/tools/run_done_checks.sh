#!/usr/bin/env bash
set -euo pipefail

CODE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$CODE_DIR/.." && pwd)"

(cd "$CODE_DIR" && python -m agents.co.tests.smoke_co_runner)
(cd "$CODE_DIR" && MPLCONFIGDIR=/tmp/mpl python -m experiments.suite_cli --config experiments/configs/suite_demo.yaml)
(cd "$REPO_ROOT" && bash ChangeOntCode/tools/qa.sh)
(cd "$REPO_ROOT" && bash ChangeOntCode/tools/spec_gate.sh)
(cd "$CODE_DIR" && python tools/validate_co_configs.py)
(cd "$CODE_DIR" && python tools/check_done_state.py)
(cd "$CODE_DIR" && MPLCONFIGDIR=/tmp/mpl python -m experiments.suite_cli --config experiments/configs/suite_validation.yaml)

echo "DONE_CHECKS_OK"
