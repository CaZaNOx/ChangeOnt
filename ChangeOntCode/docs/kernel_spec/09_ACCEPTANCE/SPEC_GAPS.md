# Spec Gaps

## Purpose

This page records the remaining gap between the current working kernel slice and the target architecture doctrine.

## Current Working Status

The current kernel is sufficient for:
- canonical runtime execution
- smoke and moderate validation suites
- telemetry
- QA/spec gates
- explicit packet/group/fusion behavior
- explicit path-space fragment continuity
- explicit meta-header/header regime influence
- experiment-doctrine binding support

This means the active canonical runtime slice now materially implements the documented architecture.

## Remaining gaps

The remaining gaps are now primarily of three kinds:

### 1. Open design space
Some areas remain intentionally open rather than incorrectly implemented.

Examples:
- whether the primitive set is philosophically final
- whether some current structural profiles should later become primitives
- whether some local semantic behavior should later move further into dedicated semantic combinators

### 2. Optional/experimental refinement
Optional and experimental components are now classified and guarded, but may still be refined further.

### 3. Validation breadth
The repo now has smoke validation, a broader validation suite, QA/spec gates, and done-state checks. Future experiment matrices may still expand beyond the current validation surface.

## Design rule going forward

New code should continue to move the repo toward:
- clearer primitive contracts
- clearer semantic combinator contracts
- clearer element declarations
- one implementation per semantic unit
- experimentation by assembly rather than cloning

The active canonical slice should now be treated as implemented, while the remaining items above are treated as future refinement and open design space, not hidden implementation incompleteness.
