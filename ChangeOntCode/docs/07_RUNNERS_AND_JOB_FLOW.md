# Runners and Job Flow

This file documents the target-state job flow and the role of family runners.

## 1. Job model

A suite run expands into concrete jobs identified by:
- family
- mode/environment
- agent
- seed
- runner path
- output location

Each job should be self-contained enough that:
- it can be launched independently
- it has its own run artifacts
- it can be summarized correctly later

## 2. Job flow

The canonical job flow is:

1. suite creates a concrete job
2. suite writes or resolves per-run config if needed
3. family runner loads that config
4. runner constructs environment
5. runner constructs STOA or CO path
6. runner executes family loop
7. runner writes required artifacts
8. suite later aggregates completed runs into summaries

## 3. Runner responsibilities

Every runner must:
- own the family-local loop
- preserve honest select/update behavior
- call the correct STOA or CO path
- write required artifacts
- return enough information for summaries

## 4. CO path responsibilities

For CO runs, the runner must preserve:
- translator boundary integrity
- adapter select/update integrity
- honest kernel update behavior
- no hidden bypasses that deactivate documented kernel semantics

## 5. STOA path responsibilities

For STOA runs, the runner must preserve:
- family-appropriate baseline semantics
- clear action/update logic
- honest comparison conditions

## 6. Artifact contract at runner level

A successful runner invocation must produce:
- `metrics.jsonl`
- `budget.csv`
- `run_manifest.json`
- `job_state.json`
- `quick_plot.png`

## 7. Known target-state risk areas

The runner layer is a common misalignment point if:
- CO maze hangs indefinitely
- update semantics are too thin
- status files are inaccurate
- plotting is not produced
- family-local assumptions are not documented

## 8. Family differences, unified contract

Families differ in:
- environment structure
- baseline algorithms
- translator behavior
- metrics

But all runners still satisfy one unified contract:
- environment construction
- agent construction
- select/update loop
- artifact generation
- summary compatibility