# Parallelism and Execution Model (Current)

## Current execution model
Current behavior:
- `suite_cli` runs sequentially.
- For each family, it iterates modes, then seeds, then agents, and invokes one runner at a time.
- Each runner is a separate subprocess (`python -m ...`) that blocks until completion.
- Per-mode summaries are generated immediately after the last run for that mode completes.
- Per-family summaries are generated after all modes in the family complete.
- Suite-level summaries are generated once after all selected families finish.

There is no concurrency control or job queue in the current harness. The only “parallelism” is whatever an individual runner or library might do internally, which is not managed by `suite_cli`.

## Where task groups are formed
The task grouping is implicit in the nested loops in `suite_cli`:
- Family group: `maze`, `renewal`, `bandit` (in that order if present).
- Mode group: each `mode` entry under a family.
- Run group: the Cartesian product of `seeds × agents` within each mode.

Summaries are aligned with those groups:
- Per-mode summary consumes all runs in that mode’s directory.
- Per-family summary consumes all `_summary/summary.csv` files across modes.
- Suite summary consumes all family `combined_summary.csv` files.

## What would need to change for real parallel execution
Future idea (not implemented):
- Introduce a job scheduler (e.g., multiprocessing, subprocess pool, or an external job runner) so runs can execute concurrently.
- Add a barrier or explicit “all runs complete” signal before per-mode summaries run.
- Ensure per-run output paths are unique and avoid per-mode summary directories being written while runs are still in progress.
- Make summary steps resilient to missing or partial `metrics.jsonl` files.
- Optionally redirect per-run logs to unique files for easier debugging when multiple runs are active.

## Current behavior vs future idea
Current behavior:
- Single-process, sequential orchestration in `suite_cli`.
- Summaries are generated in-line immediately after the last run in their group finishes.

Future idea (not implemented):
- Parallelize at the run level (seed × agent) or mode level with a fan-out/fan-in pattern.
- Defer summary generation until all parallel jobs for that group finish.
