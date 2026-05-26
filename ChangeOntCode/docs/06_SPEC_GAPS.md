# Spec Gaps

This file tracks the remaining gap between the target-state docs and the current codebase.

## Current status

The major **implementation blockers** that previously prevented an honest docs→code claim are now closed for the canonical runtime slice. In particular:

- the canonical smoke path completes cleanly
- required artifacts and plots are produced at the smoke-validation level
- QA/spec gates pass
- the active runtime path is explicit and working
- packet/group/fusion structure is real
- path-space fragments are real internal runtime objects
- semantic combinator support is active
- component classification and experimental opt-in are enforced
- a broader validation suite exists beyond smoke

## Remaining gap types

### Open design space
The remaining gaps are primarily open design space or future richness questions rather than blocking implementation defects.

Examples:
- how philosophically final the primitive set should be
- whether additional structural profiles should later become primitives
- how much further semantic combinators should absorb currently local behavior
- how exhaustive future experiment matrices should be beyond the existing validation suite

### Cleanup / refinement
Further cleanup may still be desirable, especially for:
- optional/experimental component refinement
- deeper path-space centrality across more mechanisms
- additional code-tree simplification of inactive paths

## Practical meaning

The project is now in a state where the docs meaningfully describe the implemented canonical runtime, and the remaining differences are best understood as:
- future refinement
- broader validation expansion
- or open design space

rather than hidden implementation drift in the active canonical slice.
