### `ChangeOntCode/docs/12_PARALLEL_EXECUTION_PLAN.md`

# Parallel Execution Plan

This document defines the **target plan** for safe harness parallelism.

It describes how to parallelize execution without breaking run isolation or summary correctness.

## Purpose

Parallelism should reduce wall-clock time without changing:

* runner semantics
* run outputs
* summary semantics
* CO/STOA comparability

Parallelism must be introduced at the **job orchestration layer**, not by making runners interdependent.

## Current state

Current suite execution is sequential:

* family by family
* mode by mode
* seed × agent jobs one at a time

This is simple but slow.

## Recommended parallelization unit

The correct parallelization unit is:

**one concrete run job**

That means one tuple of:

* family
* mode
* seed
* agent
* environment spec
* out_dir

Each such run is independent and can be executed in parallel as long as `out_dir` is unique.

## Why run-level parallelism is the right first step

Because it preserves the clean separation:

* suite schedules jobs
* runner executes one job
* summaries happen only after all jobs in a group finish

This avoids coupling runners to each other.

## Parallelization levels considered

### Option A — parallelize inside runners

Not recommended as first move.

Why:

* family-specific
* harder to reason about
* mixes harness concerns with loop concerns
* complicates debugging

### Option B — parallelize at mode level only

Possible, but too coarse.

Why:

* wastes available independence within a mode
* still leaves unnecessary serialization

### Option C — parallelize at run level

Recommended.

Why:

* natural job unit
* least conceptual distortion
* easiest to implement with barriers

## Required invariants for parallel execution

### 1. Unique output directory per run

No two jobs may write to the same run directory.

### 2. Summary barriers

Per-mode summary runs only after all jobs in that mode are finished.
Per-family summary runs only after all modes in that family are finished.
Suite summary runs only after all selected families are finished.

### 3. No runner-owned summary side effects

Runners must not produce family/suite summaries directly.

### 4. Failure isolation

One failed run must not corrupt outputs of sibling runs.

### 5. Stable manifesting

Each run should leave behind enough metadata to be counted as:

* success
* failed
* incomplete

## Target orchestration model

### Phase 1 — expand plan

Suite expands config into a full job list.

### Phase 2 — group jobs

Group by:

* family
* mode

### Phase 3 — fan out run jobs

Launch all jobs in a group, up to a configurable worker limit.

### Phase 4 — wait for group completion

Do not summarize early.

### Phase 5 — summarize completed group

After the group barrier is reached, write summaries.

### Phase 6 — continue upward

Repeat for family barrier and suite barrier.

## Required job states

Each run job should be classifiable as one of:

* `pending`
* `running`
* `succeeded`
* `failed`
* `incomplete`

This does not require a huge framework.
A simple manifest/status file per run is enough.

## Minimal implementation strategy

Start with the smallest change that preserves correctness.

### Step 1

Normalize runner output cleanup and manifest writing.

### Step 2

Normalize suite job creation.

### Step 3

Add a small worker pool at suite level.

### Step 4

Add barrier-based summary triggering.

### Step 5

Add failure reporting in overall suite summary.

This is enough for first real parallelism.

## What must not happen

* summaries reading half-written metrics
* two jobs writing the same output path
* family-specific concurrency hacks
* different parallel logic per family
* using output directory existence alone as proof of success

## Suggested control knobs

Suite config should eventually expose:

* `max_workers`
* `parallelize_by`

  * `run`
  * maybe later `mode`
* `continue_on_failure`
* `rerun_failed_only`

These are harness-level controls, not runner-level controls.

## Philosophical fit

This execution model fits the broader project structure well:

* kernel stays modular
* runners stay self-contained
* suite becomes the scheduler
* summary logic becomes explicit
* parallelism reflects independence of experiments, not entanglement of implementations

That is the cleanest architecture.

## Acceptance idea

Parallel execution is ready when:

* run jobs can be launched concurrently
* outputs remain isolated
* summaries wait for correct barriers
* failures are visible and do not silently poison aggregates
* sequential and parallel runs produce the same summary semantics
