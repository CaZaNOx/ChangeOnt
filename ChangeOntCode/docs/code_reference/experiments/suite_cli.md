# docs/code_reference/experiments/suite_cli.md

# Suite CLI

## Purpose

`suite_cli.py` is the primary suite entrypoint.

It turns a suite config into runnable jobs and orchestrates execution, artifact generation, and summary generation.

---

## Why it exists

The project needs one central harness entrypoint that can:
- run STOA and CO side by side,
- scale from demo to larger suites,
- preserve reproducibility,
- and support mechanism investigation.

---

## Canonical responsibilities

**Binding**

`suite_cli.py` must:

1. load suite config
2. resolve CO injection if requested
3. expand concrete jobs
4. generate per-run configs as needed
5. schedule jobs according to the execution contract
6. track run status honestly
7. trigger mode/family/suite summaries only after the proper barriers
8. ensure artifact generation and provenance behavior align with target-state contract

---

## Expected target-state scheduler behavior

**Binding**

The suite layer must behave equivalently to:

- families in parallel
- modes in parallel within families
- runs in parallel within modes
- mode summary barrier
- family summary barrier
- suite summary barrier

The implementation may use nested executors or a queue-based scheduler if the dependency behavior matches.

---

## Important current risk areas

The suite CLI is a critical misalignment point if:

- CO manifest resolution is brittle or silent when failing
- CO jobs are silently not injected
- job status remains `running` when jobs are actually complete
- summaries are generated from semantically wrong rows
- family/mode scheduling is far more serial than the documented target state
- temporary config generation does not preserve enough provenance

---

## Required provenance

**Recommended starting point**

The suite layer should write:
- suite config snapshot
- expanded suite manifest
- job state/provenance
- failure summaries

If these are missing and reproducibility suffers, this should be promoted to Binding.