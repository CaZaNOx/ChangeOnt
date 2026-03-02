# docs/code_reference/outputs/run_artifacts.md

# Run Artifacts

## Purpose

This file documents the required per-run artifacts and what each one means.

Per-run artifacts are not optional debugging leftovers.  
They are part of the execution contract.

---

## Required per-run artifacts

**Binding**

Every successful run must produce:

- `metrics.jsonl`
- `budget.csv`
- `run_manifest.json`
- `job_state.json`
- `quick_plot.png`

If one or more required artifacts are missing, the run is not fully successful.

---

## `metrics.jsonl`

### Purpose
Primary structured metric log for the run.

### What it should contain
- run header/context line(s)
- family-relevant metrics over execution
- CO diagnostic lines where relevant
- enough information to support summary generation and run-level plot generation

### Why it is needed
This is the main execution trace for:
- analysis
- summary aggregation
- debugging semantic/runtime issues

### Misalignment examples
- metrics file missing
- metrics shape too thin to support the family summary
- misleading CO diagnostics that do not reflect real runtime state

---

## `budget.csv`

### Purpose
Budget/comparison artifact for runtime resource-like accounting.

### What it should contain
A standardized schema sufficient for cross-run comparison.

### Why it is needed
The project needs honest comparison not only of output metrics but also of budget-like runtime characteristics.

### Misalignment examples
- missing file
- inconsistent column naming across runners without normalization
- placeholder values presented as if meaningful

---

## `run_manifest.json`

### Purpose
Structured provenance for the run.

### What it should contain
- family
- mode
- seed
- agent identity
- config identity or variant identity
- output directory
- status/provenance fields
- enough metadata to reconstruct what was intended to run

### Why it is needed
This is the canonical run identity/provenance file.

### Misalignment examples
- missing file
- missing agent/family/mode identity
- status inconsistent with actual artifact completion

---

## `job_state.json`

### Purpose
Job state/progress/status marker at run level.

### What it should contain
- running / succeeded / failed status
- timestamps or ordering/progress metadata as needed by the harness
- failure information if present

### Why it is needed
The harness needs to know whether a run is finished, failed, or still active.

### Misalignment examples
- run has completed but job_state still says running
- failure exists but job_state hides it
- status is inconsistent with actual artifacts

---

## `quick_plot.png`

### Purpose
Immediate run-level visual artifact.

### What it should show
A family-appropriate quick visualization where possible.

Examples:
- bandit regret-like trajectory
- maze episode/path/return progression
- renewal cumulative reward or equivalent sequence metric

### Why it is needed
Run-level plots are required artifacts and provide the fastest sanity check.

### Misalignment examples
- plot missing
- plot exists but is unrelated to meaningful run data
- family-specific plot should exist but only a meaningless fallback is produced

---

## Additional recommended provenance

**Recommended starting point**

A run may also include:
- config snapshot
- richer error trace
- additional debug traces
- internal CO packet/continuation snapshots where useful

These are recommended but not yet required unless promoted later.