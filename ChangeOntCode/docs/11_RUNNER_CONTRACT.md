### `ChangeOntCode/docs/11_RUNNER_CONTRACT.md`

# Runner Contract

This document defines the **binding target contract** for family runners.

A runner executes exactly **one** self-contained experiment job.

## Purpose

A runner is the boundary between:

* suite orchestration
* environment execution
* agent execution
* run artifact generation

A runner must not own suite-level concerns.

## Runner responsibilities

Each runner must do exactly these things:

1. read one per-run config
2. create one output directory
3. construct one environment instance
4. construct one agent instance
5. execute the experiment loop
6. write per-run artifacts
7. exit with a success/failure status

That is all.

## Runner non-responsibilities

A runner must **not**:

* decide global suite scheduling
* launch sibling jobs
* compute family-level summaries
* compute suite-level summaries
* mutate other run directories
* infer missing global config structure
* silently mix multiple runs into one metrics file

## Canonical per-run config schema

All runners should converge to this shape.

```yaml
job:
  family: "<bandit|maze|renewal|...>"
  mode: "<mode_name>"
  seed: 0
  agent_id: "<display_name>"
  out_dir: "outputs/suite/<suite_run>/<family>/<mode>/<agent>_s<seed>"

env:
  kind: "<family_specific_env_kind>"
  spec: {}
  params: {}

agent:
  type: "<stoa|co>"
  name: "<agent_name>"
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

Notes:

* not every family uses `steps`, `episodes`, and `horizon`, but the keys should exist where meaningful
* family-specific details belong under `env.spec` or `env.params`, not scattered across top-level keys

## Canonical runner input

A runner must accept:

* `--config <path>`

Optional debug flags are allowed, but `--config` is the canonical path.

If `--config` is present, the runner must treat that config as authoritative.

## Canonical runner output directory contract

Each run directory must contain:

* `metrics.jsonl`
* `budget.csv`
* `run_manifest.json`
* `quick_plot.png` if plotting succeeds
* optional debug files only if explicitly enabled

### `run_manifest.json`

This file should contain enough metadata to identify the run unambiguously:

* family
* mode
* seed
* agent name
* agent type
* environment spec reference
* runner name
* start/end timestamps
* success/failure status

## Canonical metrics contract

Each run must write `metrics.jsonl`.

### Required first record

A header record containing at least:

* `record_type: "header"`
* `runner`
* `family`
* `mode`
* `seed`
* `agent`
* `out_dir`

### Required run records

The exact fields vary by family, but every run should have:

* a stable step/episode index
* a stable metric name field
* enough context to reconstruct the run behavior

### CO-specific records

If the agent is CO, runner must emit `co_debug` consistently when the adapter returns it.

## Canonical cleanup policy

Before a runner starts a run in `out_dir`:

* `metrics.jsonl` must be cleared or recreated
* `budget.csv` must be cleared or recreated
* stale `quick_plot.png` should be overwritten on success

A runner must **not append old runs into a reused run directory**.

This is binding.

## Canonical environment/agent construction pattern

Runner does:

1. parse config
2. build env from `env.kind/spec/params`
3. build agent from `agent.type/name/params`
4. run loop

### STOA path

Runner directly constructs a STOA agent.

### CO path

Runner:

* builds CO core
* wraps it in the family adapter
* constructs family observation payloads each step
* calls adapter `select()`
* passes feedback through adapter `update()`

## Canonical family observation rule

Each family runner owns the translation from raw environment state into:

* STOA-consumable input
* CO observation envelope

This translation must be explicit and local to the family runner plus translator path.

## Canonical success/failure behavior

If a run fails:

* runner must exit non-zero
* runner should still try to write a manifest with failure status if possible
* suite layer decides whether to continue other jobs

A runner must not silently swallow structural failures.

## What still may differ by family

Allowed family differences:

* environment construction details
* loop semantics
* reward/return metrics
* action space type
* family-specific plot logic
* family-specific translator inputs

Not allowed:

* ad hoc top-level config schemas
* inconsistent cleanup behavior
* different meanings of success/failure
* one family writing summaries directly while another does not

## Acceptance idea

A runner contract is satisfied when:

* every runner accepts normalized per-run config
* every runner produces the same core artifact set
* every runner clears stale per-run outputs
* CO and STOA both fit the same runner lifecycle
* family-specific differences stay local
