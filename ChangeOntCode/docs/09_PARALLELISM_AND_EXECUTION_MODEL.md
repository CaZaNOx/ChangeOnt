# Parallelism and Execution Model (Current)

## Current execution model
Current behavior:
- `suite_cli` builds a concrete job list from the suite config.
- For each `(family, mode)` group, it executes jobs in parallel up to `max_workers` (default 1).
- Each run is a separate subprocess (`python -m ...`) invoked with `--config`.
- Per-mode summaries are generated only after all jobs in that mode complete.
- Per-family summaries are generated after all modes in the family complete.
- Suite-level summaries are generated once after all selected families finish.

Parallelism is managed by a worker pool at the suite level. If `max_workers: 1`, execution is sequential.

## Where task groups are formed
The task grouping is explicit in `suite_cli`:
- Family group: `maze`, `renewal`, `bandit` (in that order if present).
- Mode group: each `mode` entry under a family.
- Run group: the Cartesian product of `seeds × agents` within each mode.

Summaries are aligned with those groups:
- Per-mode summary consumes all runs in that mode’s directory.
- Per-family summary consumes all `_summary/summary.csv` files across modes.
- Suite summary consumes all family `combined_summary.csv` files.

## What would need to change for more parallelism
Future idea (not implemented):
- Optional parallelism at the mode or family level (in addition to run-level).
- More resilient summary logic for partially failed runs.
- Richer job status aggregation beyond `job_state.json`.
