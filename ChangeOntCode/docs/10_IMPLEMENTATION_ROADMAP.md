# Implementation Roadmap

## Purpose

This page defines the intended implementation order for strengthening the kernel without breaking what already works.

It is a sequencing document, not a philosophical argument.

Its job is to tell future agents:
- what to do first
- what not to touch prematurely
- what dependencies must be respected

---

## Current State Summary

The codebase now has:

- a working v1 kernel slice
- primitive docs
- element docs
- header docs
- semantic combinator docs
- QA gate
- spec gate

The architecture still lacks:
- explicit primitive -> combinator -> element code structure
- fully stabilized primitive set
- explicit meta-header layer
- systematic experiment harness for primitive/element/combinator comparisons

---

## Priority Rule

Do not destabilize the working slice in order to prematurely build the full final ontology.

The current priority is:

1. make architecture explicit
2. preserve working runtime
3. isolate changes
4. only then deepen ontology-mechanism implementation

---

## Phase 1

### Goal
Make code structure match the docs more closely without changing overall runtime behavior unless required.

### Tasks
1. make primitive ownership explicit in code
2. reduce hidden duplication of primitive logic inside elements
3. document current primitive dependencies in code comments/config
4. ensure canonical keys/names are used consistently
5. keep QA/spec gates passing at all times

### Do not do yet
- no major runner harmonization
- no broad environment refactor
- no speculative addition of many new primitives
- no rewriting working ActionHead/runtime path unless necessary

---

## Phase 2

### Goal
Introduce explicit semantic combinator usage into code-facing architecture.

### Tasks
1. add explicit combinator selection/config surface
2. make element docs and configs declare:
   - primitives used
   - semantic combinators used
3. refactor elements so primitive combination law is less hidden
4. avoid behavior drift while doing so

### Do not do yet
- no giant all-at-once rewrite of every element
- no uncontrolled redesign of headers at the same time

---

## Phase 3

### Goal
Build the experiment layer for doctrine discovery.

### Tasks
1. allow isolated running of single elements
2. allow multiple versions of one element
3. allow combinator sweeps
4. allow parameter sweeps for primitive constants
5. allow controlled element combination experiments
6. log outcomes cleanly and comparably

This is the stage where the architecture begins to support:
- “is this primitive relation valid?”
- “is this threshold stable across tasks?”
- “does this mechanism generalize?”

---

## Phase 4

### Goal
Separate internal header vs meta-header properly.

### Tasks
1. freeze what belongs to internal header
2. define what belongs to meta-header
3. keep environment-specific prior information out of ontology mechanisms
4. preserve clean separation:
   - primitives/elements = problem-agnostic semantic kernel
   - headers = control
   - meta-header = external/task-level prior/control
   - translators = task interface

---

## Phase 5

### Goal
Expand the primitive/element doctrine only after the architecture can support honest testing.

### Tasks
Possible future additions:
- branching primitive
- convergence primitive
- local topology primitive
- persistence/depth primitive
- coupling primitive
- richer closure/quotient machinery

But these should be added only when:
- role is justified
- docs are explicit
- architecture can test them cleanly

---

## Safety Rules for Agents

### Rule 1
Never refactor multiple architectural layers at once unless explicitly ordered.

### Rule 2
Do not overwrite working kernel behavior casually.

### Rule 3
If changing primitive semantics, update the relevant docs first or in the same task.

### Rule 4
If a code change breaks QA/spec gates, fix that before moving on.

### Rule 5
Do not invent new ontology semantics ad hoc in code.

### Rule 6
If the docs are unclear, stop and request clarification rather than improvising doctrine.

---

## Recommended Immediate Next Task

The next best implementation task is:

### Primitive/element dependency cleanup
Make the code explicitly reflect:
- which primitives each current element consumes
- which parts are still provisional
- which semantic combinator form is currently assumed implicitly

This is the best next move because it:
- improves clarity
- reduces drift
- does not yet require a dangerous all-at-once rewrite

---

## Not recommended yet

Do not prioritize these yet:

- runner harmonization
- broad suite restructuring
- large-scale parallelization
- massive environment additions
- full meta-header implementation
- speculative new ontology modules

Those matter later, but not before the kernel doctrine/code alignment is tightened.