# Harness Overview

This file describes the purpose and target-state behavior of the harness.

## 1. Purpose

The harness is responsible for:
- running STOA and CO comparably
- scaling across multiple task families
- producing trustworthy artifacts
- enabling mechanism investigation, not only benchmarking

## 2. Harness role in the project

The harness is not just a convenience runner.

It is the layer that makes the project:
- investigatory
- comparative
- reproducible
- extensible

## 3. Canonical harness flow

The target-state harness flow is:

1. load suite config
2. resolve CO manifest injection if configured
3. expand jobs
4. schedule jobs under the documented dependency model
5. execute family runners
6. collect run artifacts
7. generate mode summaries
8. generate family summaries
9. generate suite summaries and plots

## 4. Scheduler target state

The harness must behave as if:
- families run in parallel
- modes run in parallel within families
- runs run in parallel within modes
- summaries wait at the correct barriers

Implementation may be:
- nested executors
- dependency graph scheduling
- queue-based or load-balanced execution

as long as the effective dependency behavior matches the documented target state.

## 5. Artifact rule

The harness is responsible for ensuring:
- required artifacts exist at every level
- plotting is mandatory, not best-effort
- provenance is preserved
- failures are visible

## 6. Comparison rule

The harness must support:
- honest STOA-vs-CO comparison
- honest CO-only competition outputs
- honest reduced vs full CO investigation

## 7. Config rule

The harness must:
- resolve configs and manifests robustly
- not silently drop CO injection
- preserve enough provenance to reconstruct what actually ran

## 8. Current vs target

The current code may still differ from this target state.

The purpose of this file is to describe the target harness behavior that code should converge to.