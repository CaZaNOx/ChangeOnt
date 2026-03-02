# docs/DOCS_REMAINING_EXTENSIONS.md

# Remaining Extensions to Existing Docs

This file lists the current documentation files that should be **extended**, not merely supplemented by new files.

The goal is to ensure the full target state is captured directly in the main documentation spine and kernel docs, not only in added side files.

---

## 1. `docs/01_RUN_AND_OUTPUTS.md`

### Extend to include
- explicit statement that commands are expected to be run from the correct working directory or with explicit path rules
- stronger artifact contract summary
- explicit statement that plots are required artifacts
- clearer note on suite config snapshots/manifests/provenance if used

### Why
This is where users expect to learn how execution and outputs are supposed to work.

---

## 2. `docs/02_ARCHITECTURE_RUNTIME.md`

### Extend to include
- explicit canonical runtime backbone
- stronger distinction between:
  - runner
  - adapter
  - translator
  - kernel
  - final translator collapse into task action
- explicit note that the canonical internal representation is path-based and time-free
- stronger note on staged fusion and classical collapse

### Why
This file should describe the actual runtime should-state, not only a high-level architecture sketch.

---

## 3. `docs/03_BINDING_SPEC.md`

### Extend to include
- cross-reference to the new final-state rules
- explicit status-label usage
- explicit rule that docs are the target-state authority and code is implementation
- stronger statement on misalignment detection

### Why
This should become the clearest “how to read the docs” binding file.

---

## 4. `docs/04_ACCEPTANCE_AND_QA.md`

### Extend to include
- acceptance criteria for:
  - plots at every level
  - honest CO-only outputs
  - honest STOA-vs-CO outputs
  - manifest resolution correctness
  - no indefinite hanging in canonical smoke suites
- acceptance criteria for documentation completeness

### Why
Target-state acceptance needs to include not only runtime success but semantic correctness.

---

## 5. `docs/05_DEV_GUIDE.md`

### Extend to include
- rule for adding new environments:
  - environment
  - runner
  - translator
  - config
  - docs
- rule for adding new primitives/elements:
  - docs first or in lockstep
  - classification status
  - config exposure
  - honest integration testing

### Why
The final architecture is supposed to be extensible.

---

## 6. `docs/06_HARNESS_OVERVIEW.md`

### Extend to include
- stronger distinction between current implementation and target-state scheduler
- explicit note that target scheduler may be nested or queue-based as long as dependency semantics match
- explicit note that mandatory plots and provenance are part of harness responsibility

### Why
Harness overview should not underspecify the final target state.

---

## 7. `docs/07_RUNNERS_AND_JOB_FLOW.md`

### Extend to include
- stronger runner-level artifact contract
- stronger family-local select/update contract summary
- explicit mention that runner success requires required artifacts
- explicit note of family-local path differences but unified contract

### Why
Runners are where many current misalignments actually occur.

---

## 8. `docs/08_OUTPUTS_SUMMARIES_AND_PLOTS.md`

### Extend to include
- explicit semantic rules:
  - CO-only excludes STOA
  - STOA-vs-CO uses compatible metrics
  - identity normalization must be consistent
- explicit “missing plots = failure” rule
- more explicit file-by-file meaning at suite level

### Why
Current live issues make this especially important.

---

## 9. `docs/09_PARALLELISM_AND_EXECUTION_MODEL.md`

### Extend to include
- target-state dependency model:
  - families parallel
  - modes parallel
  - runs parallel
  - barriers
- explicit allowance for queue-based implementation
- distinction between current behavior and desired final behavior

### Why
This is one of the clearest places where target-state behavior should be frozen.

---

## 10. `docs/10_IMPLEMENTATION_ROADMAP.md`

### Extend to include
- explicit phase separation:
  - cleanup/canonicalization
  - contract completion
  - runtime correctness
  - honest variant investigation
  - extensibility
- explicit note that docs completion is a prerequisite to clean docs→code implementation

### Why
The roadmap should reflect the actual current state and desired repair path.

---

## 11. `docs/11_RUNNER_CONTRACT.md`

### Extend to include
- explicit run artifact contract
- explicit success/failure criteria
- explicit distinction between launchable vs semantically honest execution
- stronger note on select/update integrity
- explicit note that hanging/non-terminating canonical smoke runs are contract failures

### Why
This is a core contract file and should reflect the stronger clarified standard.

---

## 12. `docs/12_HARNESS_TARGET_STATE.md`

### Extend to include
- strong tie-in to the newly clarified project target:
  - clean
  - canonical
  - faithful
  - honest
  - investigatory
  - extensible
- explicit note that target-state docs must be sufficient to detect code misalignment

### Why
This file should be one of the clearest project target-state statements.

---

## 13. `docs/kernel_spec/00_INDEX.md`

### Extend to include
- links to new kernel-spec files
- explicit distinction between conceptual doctrine files and executable-contract files

### Why
The kernel spec index should make the expanded kernel-spec layer navigable.

---

## 14. `docs/kernel_spec/01A_ARCHITECTURE_DOCTRINE.md`

### Extend to include
- stronger explicit distinction between:
  - meta-header
  - header
  - primitives
  - elements
  - groups
  - fusion
  - translators
- explicit note that the kernel is time-free and path-based

### Why
This is the doctrine file and should reflect the clarified architecture more directly.

---

## 15. `docs/kernel_spec/02A_EXPERIMENT_DOCTRINE.md`

### Extend to include
- explicit mechanism-investigation role of the suite
- explicit rule that `CO_full` is the maximal coherent supported kernel
- stronger explanation of reduced and sweepable variants

### Why
This is critical for the “philosophical commitments as experimental questions” framing.

---

## 16. `docs/kernel_spec/03_WIRING_MAP.md`

### Extend to include
- explicit target-state path from environment to translator to kernel to translator to environment
- explicit note on path-space fragment and continuation surface
- explicit note on classical/STOA stream in final fusion

### Why
This is where wiring should be most visually clear.

---

## 17. `docs/kernel_spec/03A_TARGET_KERNEL_TABLE.md`

### Extend to include
- core vs optional vs experimental column
- packet/fusion/header/meta-header involvement columns
- note on which components are target-state baseline vs optional extension

### Why
This file should become much more useful as an implementation alignment table.

---

## 18. `docs/kernel_spec/10_IMPLEMENTATION_ROADMAP.md`

### Extend to include
- stronger note that docs completion is part of implementation work
- stronger note that stale/competing runtime paths must be resolved
- stronger tie-in to target-state contracts

### Why
Kernel roadmap should not assume target-state contracts are already fully frozen if they are not.

---

## 19. Legacy docs policy

### Add or clarify somewhere in the existing docs
- how and when legacy material may be promoted into binding docs
- rule that legacy concepts do not become binding unless explicitly promoted
- rule that code must not rely silently on legacy-only concepts

### Why
A lot of the richest kernel semantics are currently recoverable from legacy/history material, so the promotion rule must be explicit.

---

## Final extension rule

After these extensions, the docs should be checked against:

- `docs/code_reference/coverage_checklist.md`

Only when that checklist is satisfied should the docs be treated as a complete target-state basis for docs → code implementation.