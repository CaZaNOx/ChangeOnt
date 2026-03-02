# Binding Spec

This file explains how to interpret the documentation set as a target-state specification.

## 1. Docs are the target-state authority

The documentation is the canonical source of truth for the target state.

The code is the implementation.

If code and docs differ, then one of the following must be true:
- code is incomplete
- code is incorrect
- code is experimental
- code is legacy/inactive
- docs are incomplete and must be updated

This distinction must be made explicitly.

## 2. Status labels

The docs use these status labels.

### Binding
Part of the canonical target state. Code should converge to this.

### Recommended starting point
Best current implementation choice under CO and current architecture, but not claimed as uniquely derived.

### Open design space
A genuine design space remains. Multiple CO-faithful realizations may be possible.

### Experimental
May exist in code or theory, but is not baseline-supported canonical runtime behavior.

### Legacy / inactive
Historical or non-binding material. Must not compete as an equal active runtime truth.

## 3. Binding rule

A statement is binding when it defines:
- the target-state architecture
- a required contract
- a required artifact
- a required runtime separation
- a required semantic rule
- a required classification boundary

## 4. Misalignment detection rule

The docs must be strong enough that a developer can identify whether code is:
- aligned
- incomplete
- incorrect
- experimental
- legacy

If the docs are too weak to make that judgment, they are not complete enough for the docs → code pipeline.

## 5. What the docs must capture

The docs must capture enough detail that a developer can answer:

- what the system should do
- why it should do it
- what each major subsystem is for
- what interfaces it should expose
- what inputs and outputs it should use
- what artifacts it must produce
- what is binding vs recommended vs experimental vs legacy

## 6. Legacy promotion rule

Legacy material is not binding unless explicitly promoted into the main docs.

Code must not rely on concepts that only exist in legacy/reference material without promoting them into the binding docs.

## 7. Canonical runtime path rule

There must be one canonical active runtime path for:
- suite execution
- runner execution
- translator boundaries
- kernel construction
- kernel execution
- artifact generation
- summary generation

Other paths must be clearly marked experimental or legacy.

## 8. Documentation completeness rule

The docs are complete enough only when they are sufficient to:
- rebuild the intended runtime behavior in principle
- detect code misalignment
- define acceptance conditions
- support extension without drift