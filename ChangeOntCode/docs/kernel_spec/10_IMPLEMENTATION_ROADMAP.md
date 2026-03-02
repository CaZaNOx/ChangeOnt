# Implementation Roadmap

This roadmap describes the target-state path from the current prototype state to the desired canonical state.

## 1. Current state

The current state should be understood as:
- partially runnable
- semantically drifting
- not yet clean enough to claim CO-honesty
- not yet complete enough to trust all summaries/plots
- in need of cleanup and contract completion

## 2. Guiding rule

Implementation should proceed against the docs.

Completing the docs is part of implementation work because the project follows a docs → code pipeline.

## 3. Phases

### Phase 1 — Documentation completion
Complete the target-state docs so they:
- capture the full should-state
- expose code misalignment clearly
- classify binding vs recommended vs experimental vs legacy

### Phase 2 — Cleanup and canonicalization
Resolve:
- naming drift
- misleading file placement
- stale/competing runtime paths
- unclear statuses of files/components

### Phase 3 — Contract completion
Make interfaces real and explicit:
- environment ↔ runner
- runner ↔ adapter
- translator ↔ kernel
- primitive ↔ element
- element ↔ fusion
- suite ↔ artifacts

### Phase 4 — Runtime correctness
Fix:
- manifest resolution
- required artifact production
- plot generation everywhere
- summary semantic correctness
- header/classical weighting
- primitive/translator mismatches
- non-termination and lifecycle failures

### Phase 5 — Honest mechanism investigation
Define and support:
- `CO_full`
- reduced kernel variants
- parameter sweeps
- interaction studies
- honest STOA comparison

### Phase 6 — Extensibility
Make it easy to add:
- new environments
- new runners
- new translators
- new primitives
- new elements

without architectural drift.

## 4. Success criterion

The project reaches its intended target state when:
- the docs fully capture the should-state
- code aligns with the docs
- the suite behaves honestly
- plots and summaries are semantically correct
- `CO_full` and reduced variants can be investigated honestly
- new components can be added cleanly