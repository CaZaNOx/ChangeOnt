# Acceptance and QA

## QA gate (mandatory)
- QA script: `ChangeOntCode/tools/qa.sh`
- **No merge unless QA passes.**

What it checks (from the script):
- A header record exists in the latest `metrics.jsonl`
- Header update counters/sources if present (expects update to come from `run_update`)
- CO scalar signals if present (identity + GHVC)
- Identity variation (`EC_Identity.same` varies; `EC_Identity.last_d` sometimes > 0)
- GHVC birth suggest + state change
- Mask contract if mask fields are present
- Exactly one `co_debug` record per `t`

## How to run QA
From repo root:
- `bash ChangeOntCode/tools/qa.sh`

The script uses the most recent `ChangeOntCode/outputs/**/metrics.jsonl` and requires `jq`.

## Generate fresh outputs for QA (quick)
Use existing suite-generated configs to exercise CO quickly.

Bandit (CO):
- `python -m experiments.runners.bandit_runner --config ChangeOntCode/outputs/suite/tmp/bandit/easy/co_CO_full_s7.yaml`

Maze (CO):
- `python -m experiments.runners.maze_runner --config ChangeOntCode/outputs/suite/tmp/maze/maze_9x9/co_CO_full_s7.yaml`

Renewal (CO):
- `python -m experiments.runners.renewal_runner --config ChangeOntCode/outputs/suite/tmp/renewal/clean/co_CO_full_s7.yaml`

## If QA fails
- Fix the implementation or the binding contract. Do **not** “paper over” failures by changing docs alone.

