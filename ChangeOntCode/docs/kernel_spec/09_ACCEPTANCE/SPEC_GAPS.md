# Spec Gaps

## Purpose

This page records architectural and implementation gaps between the current working kernel slice and the target architecture doctrine.

It is binding as the official list of known incompletenesses.

---

## Current Working Status

The current kernel is sufficient for:
- canonical runtime execution
- telemetry
- QA/spec gates
- initial element isolation smoke tests
- minimal identity / GHVC / ActionHead behavior

This does **not** mean the full target architecture is complete.

---

## Known Gaps

### 1. Semantic combinator layer is not yet properly realized
Current combinator files are mostly runtime-oriented.
The architecture requires a distinct semantic combinator layer for primitive interaction law-forms.

### 2. Primitive / combinator / element boundaries are not yet fully enforced
Some logic still lives inside elements that should later migrate into primitives or semantic combinators.

### 3. Element declarations are not yet explicit enough
Elements should eventually declare:
- primitive dependencies
- semantic combinator dependencies
- weight/composition roles

This is only partially represented today.

### 4. Meta-header layer is not yet clearly specified as a separate binding layer
External priors and provided stability assumptions are conceptually separated, but not yet fully documented/implemented as a dedicated layer.

### 5. Primitive set is not yet finalized
Current primitives are a plausible v1 subset, but not yet a final or complete target set.

Potential later additions/reframes include:
- branching/divergence support
- convergence support
- temporal persistence/depth
- local topology/neighborhood
- coupling/influence support

### 6. Some current primitives may need reframing
In particular:
- some implementation-shaped names may not be ideal final semantic names
- some weaker primitives may later be demoted to mechanism-level roles instead

### 7. ActionHead still carries pragmatic aggregation logic
Current ActionHead is acceptable as a working final surface, but must continue to be protected from semantic drift.

### 8. Experiment doctrine is not yet fully frozen
A formal binding page for:
- element isolation
- element combinations
- weight sweeps
- combinator-form comparisons
- stability prior vs no-prior comparisons

still needs to be added.

---

## Design Rule Going Forward

New code should move the repo **toward**:
- clear primitive contracts
- clear semantic combinator contracts
- clear element dependency declarations
- one implementation per semantic unit
- experimentation by assembly rather than file cloning

No future implementation should silently assume the current working slice already equals the final architecture.