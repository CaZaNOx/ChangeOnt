### `ChangeOntCode/docs/10_HARNESS_TARGET_STATE.md`

# Harness Target State

This document defines the **target architecture** for the experiment harness.
It is not a description of current behavior. It is the desired structure the code should converge toward.

## Purpose

The harness must provide a **clean, modular, family-agnostic orchestration layer** for:

* environment execution
* STOA baseline execution
* CO execution
* per-run logging
* per-group summarization
* suite-level summarization

The harness must make it easy to add:

* a new environment family
* a new runner family
* a new STOA agent
* a new CO variant
* a new summary metric

without duplicating orchestration logic.

## Core idea

The harness should have a strict layered structure:

1. **Suite layer**

   * decides what jobs exist
   * expands configs into a concrete run list
   * schedules jobs
   * waits for completion
   * triggers summaries at the correct barrier points

2. **Runner layer**

   * executes exactly one self-contained job
   * builds one environment
   * builds one agent
   * runs one experiment loop
   * writes one run directory

3. **Agent layer**

   * STOA agents or CO adapters/core
   * runner talks to agents through a small common surface

4. **Output layer**

   * writes metrics
   * writes budget
   * writes plots
   * writes summary tables

## Target properties

The harness target state must satisfy all of the following:

### 1. One canonical job model

A run is always a single concrete tuple:

* family
* mode
* seed
* agent
* environment spec
* output directory

No runner should invent its own job model.

### 2. One canonical config shape

All per-run configs must follow one shared schema with family-specific payloads nested under stable keys.

### 3. One canonical output contract

Every run directory must contain the same core artifacts, even if some are empty or minimal.

### 4. Family-specific logic stays local

Bandit, maze, renewal specifics should live in family runners and family translators — not in suite orchestration.

### 5. Summary timing is explicit

Summaries should be produced only after the relevant barrier is reached:

* mode barrier
* family barrier
* suite barrier

### 6. Parallel execution must be possible

The suite must be able to fan out independent run jobs safely.

### 7. Partial failure must be survivable

A failed run must not corrupt the whole suite or silently poison summaries.

### 8. CO/STOA parity remains visible

The harness must make it easy to compare:

* STOA vs STOA
* CO vs STOA
* CO variant vs CO variant

## Target directory role split

### `experiments/`

Owns orchestration and experiment execution:

* suite launcher
* runner entrypoints
* shared config expansion
* summary triggers
* plotting/summarization calls

### `environments/`

Owns task worlds only:

* environment specs
* environment dynamics
* reset/step logic

### `agents/stoa/`

Owns family-specific baseline agents.

### `agents/co/`

Owns CO core, adapters, primitives, elements, headers, combinators, translators.

### `outputs/`

Owns generated artifacts only.
No source-of-truth configuration should live here permanently except generated temp configs and run results.

### `docs/`

Owns the project description, contracts, and target-state specifications.

## Target harness flow

### Stage 1 — load suite plan

The suite reads one suite config and constructs an abstract execution plan.

### Stage 2 — expand into concrete jobs

Each family/mode/seed/agent combination becomes a concrete job record.

### Stage 3 — write normalized run configs

Each job is materialized as a normalized per-run config.

### Stage 4 — execute jobs

Each job is executed by the appropriate family runner.

### Stage 5 — validate run outputs

Each completed run is checked for minimum required artifacts.

### Stage 6 — summarize mode groups

After all jobs in one mode complete, write mode summaries.

### Stage 7 — summarize family groups

After all modes in one family complete, write family summaries.

### Stage 8 — summarize full suite

After all families complete, write overall suite summaries.

## Current-state problems this target state is meant to fix

* duplicated runner logic
* inconsistent config shapes between families
* inconsistent output cleanup behavior
* sequential-only orchestration
* summary assumptions hidden in file naming conventions
* family-specific leakage into orchestration logic
* generated output directories being used as quasi-config sources
* inconsistent logging behavior across runners

## Non-goals

This target state does **not** define:

* kernel math
* CO primitive semantics
* element semantics
* translator semantics
* STOA algorithm internals

Those belong elsewhere.

## Acceptance idea

The harness target state is reached when:

* one canonical job schema exists
* one canonical runner contract exists
* one suite orchestration path exists
* summaries run at explicit barriers
* parallel execution is possible without changing runner semantics
* adding a new family does not require copying another family runner wholesale

