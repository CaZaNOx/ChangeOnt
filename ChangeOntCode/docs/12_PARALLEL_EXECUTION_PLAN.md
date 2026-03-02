# Parallel Execution Plan

This file records the target parallel execution plan for the harness.

## 1. Target behavior

The target execution behavior is:

- one active branch per family
- one active branch per mode within each family
- one active branch per run within each mode

This produces a hierarchical or dependency-equivalent fan-out.

## 2. Barrier points

The required barrier points are:

### Mode barrier
Mode summary waits for all runs in the mode.

### Family barrier
Family summary waits for all modes in the family.

### Suite barrier
Suite summary waits for all families.

## 3. Allowed implementation patterns

The implementation may use:

- nested executors
- family/mode/run pools
- dependency queues
- priority queues
- load-balanced worker pulling

The exact mechanism is open as long as the dependency behavior is preserved.

## 4. Why this plan exists

The project needs:
- scalability across families and modes
- many STOA and CO variants
- reduced unnecessary serialization
- correct summaries at every level

## 5. Operational constraints

Even under parallelism:
- status/progress must remain truthful
- per-run artifacts must remain isolated and inspectable
- failures must remain visible
- plot/summary generation must respect barriers

## 6. Practical note

A queue-based implementation is acceptable and may be preferable if:
- all jobs are conceptually available
- workers pull eligible jobs under dependency constraints
- the effective behavior still matches the target fan-out and barrier structure

## 7. Relation to the target state

This file is a concrete execution-planning companion to:
- `09_PARALLELISM_AND_EXECUTION_MODEL.md`
- `14_EXECUTION_AND_ARTIFACT_CONTRACT.md`

It should be read as part of the same target-state scheduler specification.