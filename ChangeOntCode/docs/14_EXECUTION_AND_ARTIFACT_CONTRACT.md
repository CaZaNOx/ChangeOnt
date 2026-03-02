# docs/14_EXECUTION_AND_ARTIFACT_CONTRACT.md

# Execution and Artifact Contract

This file defines the target-state execution behavior and artifact contract.

## 1. Scheduler target state

**Binding**

The harness must support a scheduler equivalent to the following dependency structure:

- families run in parallel;
- modes run in parallel within families;
- runs `(agent × seed)` run in parallel within modes;
- mode summaries wait for all runs in that mode;
- family summaries wait for all modes in that family;
- suite summary waits for all families.

The implementation may use:
- nested executors,
- a dependency scheduler,
- a priority queue,
- or a load-balanced queue system,

provided the effective dependency/barrier behavior matches the target state.

---

## 2. Run-level contract

**Binding**

Every successful run must produce:

- `metrics.jsonl`
- `budget.csv`
- `run_manifest.json`
- `job_state.json`
- `quick_plot.png`

A run that does not produce its required artifacts is not fully successful.

---

## 3. Mode-level contract

**Binding**

Every completed mode must produce:

- a mode summary CSV
- one or more mode summary plots

Mode summaries must wait for all mode runs to complete.

---

## 4. Family-level contract

**Binding**

Every completed family must produce:

- a family combined summary CSV
- one or more family plots

Family summaries must wait for all family modes to complete.

---

## 5. Suite-level contract

**Binding**

Every completed suite must produce:

- overall summary CSV
- STOA-vs-CO comparison CSV
- CO-only competition CSV(s)
- suite-level plots
- failure summary/provenance artifacts

The suite summary must wait for all family summaries to complete.

---

## 6. Plotting rule

**Binding**

Plots are required artifacts, not best-effort niceties.

Plots must exist:
- at run level,
- at mode level,
- at family level,
- at suite level.

---

## 7. Plot semantic rule

**Binding**

A plot is only valid if:
- its source rows are semantically correct,
- labels correspond to actual agent identities,
- CO-only plots exclude STOA rows,
- STOA-vs-CO plots use compatible metrics,
- family and suite normalization of agent identity is consistent.

---

## 8. CO manifest resolution rule

**Binding**

If a suite config specifies a CO manifest, the system must resolve it unambiguously.

The implementation must not silently drop CO injection because of brittle path handling.

Manifest resolution should be relative to the suite config location or otherwise explicitly defined and documented.

---

## 9. Success rule

**Binding**

A suite should not be considered successful if:
- jobs remain indefinitely running,
- required artifacts are missing,
- summaries are semantically wrong,
- plots are missing,
- or comparison files are mislabeled.

---

## 10. Required provenance

**Recommended starting point**

Every suite output should also include:
- the suite config snapshot used,
- a suite manifest of expanded jobs,
- execution status/provenance,
- failure details for unsuccessful jobs.

This is strongly recommended and may be promoted to Binding if absent provenance materially blocks reproducibility.