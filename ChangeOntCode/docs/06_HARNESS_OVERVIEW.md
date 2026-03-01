# Harness Overview (Current)

## What `suite_cli` is
`suite_cli` is the current top-level experiment harness for the multi-family suite. It is implemented in `ChangeOntCode/experiments/suite_cli.py` and is invoked as:
- `python -m experiments.suite_cli`
- `python -m experiments.suite_cli --config experiments/configs/suite_demo.yaml`

It loads a suite config, expands it into per-run configs, runs each job by calling a family runner as a subprocess, and emits per-mode, per-family, and suite-level summaries.

## Families that exist today
The harness currently recognizes three families (as keys under `families` in the suite config):
- `bandit`
- `maze`
- `renewal`

Any other family name is ignored by `suite_cli` unless corresponding code is added.

## High-level flow (current behavior)
1. Load suite config from `ChangeOntCode/experiments/configs/suite_all.yaml` (or `--config`).
2. Determine `out_root` (default: `outputs/suite/suite`, which results in a run directory like `outputs/suite/suite_YYYY-MM-DD-HH-MM-SS`).
3. Load CO agent manifest from `ChangeOntCode/experiments/configs/co_agents/co_agents_selection.yaml` and append those agents to each family’s agent lists (unless `inject_co: false`).
4. For each family present (order is `maze`, then `renewal`, then `bandit`):
    - For each mode in that family:
      - For each seed × agent pair:
        - Write a per-run YAML config under `ChangeOntCode/outputs/suite/<suite_run>/tmp/<family>/<mode>/<agent>_s<seed>.yaml`.
       - Invoke the corresponding runner as `python -m experiments.runners.<family>_runner --config <tmp.yaml> ...`.
     - After all runs for that mode complete, generate the per-mode summary for that family.
   - After all modes in the family complete, generate the per-family summary.
5. After all requested families finish, generate the suite summary.
6. Print a JSON blob containing `suite_out`.

## Parallelism and rerun controls (current)
The suite supports run-level parallelism and optional mode-level parallelism:
- `max_workers`: number of workers for the parallelization unit
- `parallelize_by`: `"run"` (default) or `"mode"`
- `continue_on_failure`: `true|false`
- `rerun_failed_only`: `true|false` (skips previously succeeded jobs)
- `suffix_out_root`: `true|false` (append timestamp when `--config` is used)

## Configuration sources (current)
- Suite config: `ChangeOntCode/experiments/configs/suite_all.yaml` (or `--config` override)
  - Defines `out_root` and `families` entries for bandit/maze/renewal.
- Optional: `inject_co: true|false` and `co_manifest: <path>`
- CO agents manifest: `ChangeOntCode/experiments/configs/co_agents/co_agents_selection.yaml`
  - CO agent entries are appended to each family’s `agents` list.
  - The manifest contains `apply_to_all_families` / `apply_to_all_modes`, and `suite_cli` honors those flags.

## Current behavior vs future idea
Current behavior:
- The flow above is the literal code path in `suite_cli`.
- Runs execute in parallel within each mode group when `max_workers > 1`, otherwise sequential.
- Per-run configs are written into `outputs/suite/<suite_run>/tmp/...` before being passed to runners.
