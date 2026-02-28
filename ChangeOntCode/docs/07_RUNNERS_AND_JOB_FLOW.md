# Runners and Job Flow (Current)

This document describes how `suite_cli` calls each runner today, what each runner receives, and what it is responsible for.

## How runners are called
`suite_cli` always calls runners as Python modules:
- Bandit: `python -m experiments.runners.bandit_runner --config <tmp.yaml>`
- Maze: `python -m experiments.runners.maze_runner --config <tmp.yaml> --agent <type> --episodes <n> --out <dir>`
- Renewal: `python -m experiments.runners.renewal_runner --config <tmp.yaml>`

Notes:
- The `--config` file is always provided by `suite_cli`.
- Maze also passes CLI flags, but the runner ignores them when a config is present.
- All runners run in-process and block; `suite_cli` waits for each subprocess to finish.

## Per-run config payloads (current)
Bandit (`bandit_runner`) config shape:
- `env.probs` (list of floats)
- `env.horizon` (int)
- `agent.type`, `agent.name` (optional), `agent.params`
- `seed` (int)
- `out` (directory for run artifacts)

Maze (`maze_runner`) config shape:
- `env.spec_path` (string path)
- `env.params` (dict) is written by `suite_cli` but not read by `maze_runner`
- `episodes` (int)
- `agent.type`, `agent.name` (optional), `agent.params`
- `out` (directory for run artifacts)

Renewal (`renewal_runner`) config shape:
- `seed` (int)
- `steps` (int)
- `agent.type`, `agent.name` (optional), `agent.params`
- `env` (dict: `A`, `L_win`, `p_ren`, `p_noise`, `T_max`)
- `out_dir` (directory for run artifacts)

## What each runner is responsible for
All runners:
- Create the run output directory.
- Construct the environment and agent.
- Run a single episode/loop series.
- Write `metrics.jsonl` and `budget.csv`.
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
- Config parsing and defaults.
- CO setup and observation construction.
- Metrics naming and summary expectations.
- Output cleanup behavior.

Current behavior vs future idea:
- Current: family-specific loops are duplicated in each runner and in `suite_cli`.
- Future idea (not implemented): centralize job creation and config schemas to reduce duplication and enforce consistent output conventions across families.
