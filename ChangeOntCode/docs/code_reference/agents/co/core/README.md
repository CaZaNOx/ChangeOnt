# docs/code_reference/agents/co/core/README.md

# CO Core

## Purpose

`agents/co/core/` contains the internal mechanics of the CO kernel.

This is where the kernel’s internal operation lives:
- primitives
- elements
- combinators
- contribution contracts
- logic helpers
- final continuation fusion logic

---

## Why it exists

The project’s main claim is not only that it can run tasks, but that it can run them via a kernel faithful to Change Ontology.

The core is therefore the place where philosophical claims must become executable mechanism.

---

## Runtime role

The core sits in the middle of the active CO loop.

The target-state loop is:

1. translators/adapters provide a path-space update
2. headers and primitives interpret the fragment
3. elements emit structural contribution packets
4. fusion logic combines these packets into higher-order outputs
5. a continuation surface is produced
6. translators collapse that continuation surface into concrete task action

---

## Main subareas

### `elements/`
Mechanism families such as EA / EB / EC / density / compressibility / router / etc.

### `primitives/`
Reusable basis terms or structural lenses such as bend, gauge, MDL, loopiness, closure, asymmetry, etc.

### `combinators/`
Runtime or semantic composition helpers:
- element-local semantic combinators,
- pipeline or other structural combinators,
- local operator forms.

### `contracts/`
Shared signal/packet contracts.

### `context/`
Kernel-side context objects such as math context.

### `logic/`
Supporting logic/math utilities.

---

## Key target-state rules

**Binding**

The core must reflect the kernel contracts documented in:
- internal representation
- header/meta-header contract
- primitive→element composition
- element contribution packet
- fusion and classical collapse
- translator boundary contract

---

## Status guidance

The core is the most load-bearing part of the repo for the “CO-honest implementation” claim.

Anything in `core/` that is:
- stale,
- decorative,
- underwired,
- or conflicting with the active runtime path

must be documented and eventually resolved.