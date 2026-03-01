# Outputs, Summaries, and Plots (Current)

This document is strictly about what the current harness writes today and when it writes it.

## Per-run outputs (current)
Each runner writes into a run directory constructed by `suite_cli`:
- Path pattern: `ChangeOntCode/outputs/suite/<family>/<mode>/<agent>_s<seed>/`

Files written by all runners:
- `metrics.jsonl` — JSONL log (one record per line).
- `budget.csv` — a single CSV file (rewritten on each run).
- `run_manifest.json` — run metadata and success/failure status.
- `quick_plot.png` — best-effort plot derived from `metrics.jsonl` (skipped if plotting deps are missing).

Additional per-run files:
- `progress.json` (bandit only) — a heartbeat file updated every 500 steps.
- `job_state.json` (suite only) — suite-level job status with timestamps.

Notes on overwrite behavior:
- All runners delete existing `metrics.jsonl` and `budget.csv` before starting.
- `quick_plot.png` is overwritten on success.

## Per-mode summaries (current)
After all runs for a given mode complete, `suite_cli` calls a per-mode summarizer.

Location:
- `ChangeOntCode/outputs/suite/<family>/<mode>/_summary/summary.csv`
- `ChangeOntCode/outputs/suite/<family>/<mode>/_summary/summary.png`

What the summaries contain (current):
- Bandit: `mean_final_regret` per agent, averaged over seeds.
- Maze: `mean_steps` per agent, averaged over episodes.
- Renewal: `mean_final_cum_reward` per agent, averaged over seeds.

## Per-family summaries (current)
After all modes in a family finish, `suite_cli` calls `summarize_family`.

Location:
- `ChangeOntCode/outputs/suite/<family>/_summary/combined_summary.csv`
- `ChangeOntCode/outputs/suite/<family>/_summary/combined_summary.png`

What the summaries contain (current):
- Bandit: mean of `mean_final_regret` over problems per agent.
- Maze: mean of `mean_steps` over envs per agent.
- Renewal: mean of `mean_final_cum_reward` over instances per agent.

## Suite-level summaries (current)
At the end of the suite run, `suite_cli` calls `summarize_suite`.

Location:
- `ChangeOntCode/outputs/suite/summary/overall_summary.csv`
- `ChangeOntCode/outputs/suite/summary/overall_stoa_vs_co.csv`
- `ChangeOntCode/outputs/suite/summary/overall_stoa_vs_co.png`
- `ChangeOntCode/outputs/suite/summary/overall_failures.csv`

What they contain (current):
- `overall_summary.csv` concatenates each family’s `combined_summary.csv` with a `family` column.
- `overall_stoa_vs_co.csv` normalizes per-family metrics to compute a simple cross-family “overall_accuracy”.
- `overall_failures.csv` lists any runs that did not succeed based on `job_state.json`.

## Plots (current)
There are two plotting layers:
- Per-run `quick_plot.png` created by each runner (best-effort, minimal heuristics).
- Per-mode and per-family plots created by `experiments/plotting/*` using matplotlib.

If matplotlib is not installed, plots are silently skipped but CSV summaries are still written.

## Current behavior vs future idea
Current behavior:
- Summaries are generated synchronously: per-mode after all runs for that mode; per-family after all modes; suite-level at the end.
- No run is considered complete until its runner finishes and its output files are written.

Future idea (not implemented):
- Make summary generation robust to missing/partial runs and handle parallel execution, so summaries can be produced incrementally or after a parallel fan-in.

## Known limitations or ambiguity (current)
- The harness relies on specific directory names (`_summary`, `combined_summary.csv`, etc.). There is no schema validation for these outputs.
- Maze and renewal runners append to `metrics.jsonl` if the file already exists. This can lead to mixed runs if outputs are reused.
- `suite_cli` writes `env.params` for maze runs, but `maze_runner` does not read or use those params today.
