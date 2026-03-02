# docs/00_START_HERE.md

# Start Here

This documentation set is the canonical source of truth for the **target state** of the ChangeOnt codebase.

The purpose of the docs is not only to explain the project. The docs must be precise enough that code can be judged against them. If code differs from the documented target state, that difference is a **misalignment** that must either be:
- implemented,
- corrected,
- explicitly marked experimental,
- or explicitly marked legacy/inactive.

## Documentation status labels

Every major design statement in the docs should be read using these labels.

### Binding
Part of the canonical target state. Code should converge to this.

### Recommended starting point
The best current implementation choice under the ontology and architecture, but not claimed as the only possible faithful realization.

### Open design space
Not yet fully frozen. Multiple CO-faithful realizations may be possible.

### Experimental
May be implemented or theorized, but not baseline-supported as canonical runtime behavior.

### Legacy / inactive
Historical material or old paths that must not compete with the canonical active architecture.

---

## Reading order

### 1. Top-level spine
Read these first.

- `01_RUN_AND_OUTPUTS.md`
- `02_ARCHITECTURE_RUNTIME.md`
- `03_BINDING_SPEC.md`
- `04_ACCEPTANCE_AND_QA.md`
- `05_DEV_GUIDE.md`
- `06_HARNESS_OVERVIEW.md`
- `07_RUNNERS_AND_JOB_FLOW.md`
- `08_OUTPUTS_SUMMARIES_AND_PLOTS.md`
- `09_PARALLELISM_AND_EXECUTION_MODEL.md`
- `10_IMPLEMENTATION_ROADMAP.md`
- `11_RUNNER_CONTRACT.md`
- `12_HARNESS_TARGET_STATE.md`
- `13_FINAL_STATE_RULES.md`
- `14_EXECUTION_AND_ARTIFACT_CONTRACT.md`

### 2. Kernel specification
These define the target-state CO kernel and boundary contracts.

- `kernel_spec/00_INDEX.md`
- `kernel_spec/01A_ARCHITECTURE_DOCTRINE.md`
- `kernel_spec/02A_EXPERIMENT_DOCTRINE.md`
- `kernel_spec/03_WIRING_MAP.md`
- `kernel_spec/03A_TARGET_KERNEL_TABLE.md`
- `kernel_spec/10_IMPLEMENTATION_ROADMAP.md`
- `kernel_spec/11_INTERNAL_REPRESENTATION.md`
- `kernel_spec/12_HEADER_AND_METAHEADER_CONTRACT.md`
- `kernel_spec/13_PRIMITIVE_ELEMENT_COMPOSITION.md`
- `kernel_spec/14_ELEMENT_CONTRIBUTION_PACKET.md`
- `kernel_spec/15_FUSION_AND_CLASSICAL_COLLAPSE.md`
- `kernel_spec/16_TRANSLATOR_BOUNDARY_CONTRACT.md`
- `kernel_spec/17_COMPONENT_CLASSIFICATION.md`

### 3. Code reference
These mirror the code tree and explain each major folder/subsystem.

- `code_reference/00_INDEX.md`
- `code_reference/01_REPO_MAP.md