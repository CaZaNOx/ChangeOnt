# Runners and Job Flow (Current)

This document describes how `suite_cli` calls each runner today, what each runner receives, and what it is responsible for.

## How runners are called
`suite_cli` always calls runners as Python modules:
- Bandit: `python -m experiments.runners.bandit_runner --config <tmp.yaml>`
- Maze: `python -m experiments.runners.maze_runner --config <tmp.yaml>`
- Renewal: `python -m experiments.runners.renewal_runner --config <tmp.yaml>`

Notes:
- The `--config` file is always provided by `suite_cli`.
- Runners treat `--config` as authoritative.
- All runners are invoked as subprocesses; `suite_cli` manages concurrency via a worker pool (default `max_workers: 1`).

## Per-run config payloads (current)
All runners accept a **canonical per-run config**:

```yaml
job:
  family: "<bandit|maze|renewal>"
  mode: "<mode_name>"
  seed: 0
  agent_id: "<display_name>"
  agent_type: "<raw_agent_type>"
  agent_name: "<optional_name>"
  out_dir: "outputs/suite/<suite_run>/<family>/<mode>/<agent>_s<seed>"
  runner: "experiments.runners.<family>_runner"

env:
  kind: "<family>"
  spec: {}
  params: {}

agent:
  type: "<stoa|co>"
  name: "<algo_or_variant>"
  params: {}

run:
  steps: null
  episodes: null
  horizon: null

logging:
  write_metrics: true
  write_budget: true
  write_plot: true
```

Family payload conventions:
- Bandit: `env.params.probs`, `env.params.horizon`, `run.horizon`.
- Maze: `env.spec.spec_path`, `run.episodes`, and optional `env.params` (width/height/seed).
- Renewal: `env.params.A/L_win/p_ren/p_noise/T_max`, `run.steps`.

## What each runner is responsible for
All runners:
- Create the run output directory.
- Construct the environment and agent.
- Run a single episode/loop series.
- Write `metrics.jsonl` and `budget.csv`.
- Write `run_manifest.json`.
- Optionally write `quick_plot.png` (best-effort; silently skipped if plotting deps are missing).

Bandit runner (`experiments/runners/bandit_runner.py`):
- Builds a `BernoulliBanditEnv`.
- Supports STOA agents: `ucb1`, `epsgreedy`, `kl_ucb`, `ts`.
- Supports CO via `COAdapterBandit` and `build_co_core` when `agent.type == "co"`.
- Writes a header record and per-step metrics (regret, arm pulls), plus `progress.json` every 500 steps.
- Deletes existing `metrics.jsonl` and `budget.csv` if present before starting.

Maze runner (`experiments/runners/maze_runner.py`):
- Builds a `GridMazeEnv` from `env.spec_path`.
- Supports STOA agents: `bfs`, `astar` (path planning, no learning).
- Supports CO via `COAdapterMaze` + `build_co_core` when `agent.type == "co"`.
- Logs per-episode `episode_steps` and `episode_return`.
- Does not delete existing `metrics.jsonl` before writing (new runs append).

Renewal runner (`experiments/runners/renewal_runner.py`):
- Builds a `CodebookRenewalEnvW` using `env` values.
- Supports STOA agents: `last` (default), `phase`, `ngram`, `vom`.
- Supports CO via `COAdapterRenewal` + `build_co_core` when `agent.type == "co"`.
- Logs a header record plus per-step `cum_reward` lines and a final summary line.
- Does not delete existing `metrics.jsonl` before writing (new runs append).

## CO vs STOA instantiation (current)
CO is instantiated inside the runner when `agent.type` (or `mode` for renewal) is `co`:
- `build_co_core(params)` builds the CO core.
- A family-specific adapter (`COAdapterBandit`, `COAdapterMaze`, `COAdapterRenewal`) wraps the core.
- The runner constructs the CO observation dict and calls `select()` and `update()` for each step.

STOA agents are constructed directly inside each runner:
- Bandit: UCB1 / ε-greedy / KL-UCB / TS.
- Maze: direct `bfs_path` / `astar_path` with no per-step agent state.
- Renewal: small FSM-style agents or `VOKT`.

## Duplications and family-specific logic (current)
There is no shared runner base class. Each family has its own:
- Environment construction and observation translation.
- CO setup and observation construction.
- Metrics naming and summary expectations.

Suite orchestration now centralizes job creation and config schema generation, while family-specific loops remain in runners.
