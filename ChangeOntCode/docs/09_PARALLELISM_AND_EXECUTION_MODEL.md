# Parallelism and Execution Model

This file describes the target-state execution dependency model.

## 1. Principle

The project should support parallel execution in a way that matches the natural structure of the suite:
- families
- modes within families
- runs within modes

## 2. Target-state dependency structure

The effective target-state behavior is:

- families run in parallel
- modes run in parallel within families
- runs `(agent × seed)` run in parallel within modes

Then:

- mode summaries wait for all runs in their mode
- family summaries wait for all modes in their family
- suite summary waits for all families

## 3. Allowed implementations

The implementation does not need to be one specific concurrency design.

It may use:
- nested executors
- dependency graph scheduling
- queue-based scheduling
- priority queues
- load-balanced job pickup

provided the effective dependency/barrier behavior matches the target state.

## 4. Queue-based interpretation

A queue-based implementation is acceptable if:
- all runnable jobs are conceptually available
- workers draw eligible jobs according to family/mode/run dependency rules
- summary jobs are only triggered once their dependencies are complete

## 5. Why this model is required

This model is needed because the suite is intended to:
- scale across families and modes
- support many STOA and CO configurations
- avoid unnecessary serialization
- still preserve correct summary barriers

## 6. Status/progress rule

Parallelism is not correctly implemented if:
- job states become unreliable
- summary barriers are violated
- or large parts of the suite are accidentally serialized contrary to the target model

## 7. Smoke and reliability

Even under parallel execution:
- runs must remain individually diagnosable
- statuses must remain truthful
- artifacts must still be written deterministically enough to inspect failures

## 8. Current vs target

The current code may still be more serial than this.

This file describes the target execution model the implementation should converge to.