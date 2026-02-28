# Wiring Map

## Purpose

This page maps the conceptual layers of the ChangeOnt kernel to the current codebase.

It is binding as the target architecture map, even where current implementation is still partial.

---

## Layered Wiring

### Layer 0 — Primitives
Canonical primitive store in current code lives under:
- `agents/co/core/primitives/`

Examples currently present:
- bend metric
- gauge
- mdl / compressibility-related support
- precision
- loopiness
- change/prototype support
- closure/quotient support
- `co_bus`

Primitive instances are stored in the kernel primitive registry and are shared reusable components.

---

### Layer 1 — Semantic Combinators
Target location:
- `agents/co/core/combinators/` for reusable semantic composition laws

Current state:
- this layer is **not yet properly realized**
- current combinator files are mostly runtime-oriented rather than semantic-law oriented

Target role:
- additive, multiplicative, gated, weighted, and CO-native composition laws reused by elements

---

### Layer 2 — Elements
Canonical element implementations live under:
- `agents/co/core/elements/`

Examples currently present:
- EA_HAQ
- EB_GHVC
- EC_Identity
- EG_DensityPrecision
- EH_BreadthDepth
- VoteBridge
- ActionHead

Elements must consume primitives (and later semantic combinators) and emit votes/signals.

Elements must not directly call one another.

---

### Layer 3 — Bus
Canonical bus primitive:
- `primitives["co_bus"]`

Bus responsibilities:
- store votes
- store scalar signals
- expose them to ActionHead / runtime surfaces

The bus is not a semantic decision-maker.

---

### Layer 4 — Header
Current header implementations live under:
- `agents/co/headers/`

Examples:
- H_SSI
- H_CS
- H_ID

Header role:
- internal control based on signals and detected stability
- update only on update pass

---

### Layer 5 — Meta Header
Target role:
- external priors / provided task-family stability assumptions

Current state:
- not yet clearly realized as a separate binding layer
- must remain distinct from internal header logic

---

### Layer 6 — Translators and Action Surface

Translators live under:
- `agents/co/integration/translators/`

Action surface:
- `agents/co/core/elements/action_head.py`

Adapters live under:
- `agents/co/adapters/`

Runtime entrypoints:
- runners create env and adapter
- adapter constructs canonical observation/update flow
- translators are task-facing
- ActionHead is final action surface

---

## Dependency Rules

### Allowed
- elements depend on primitives
- elements depend on semantic combinators
- header depends on canonical signals/state
- translators depend on runner-exposed task observation
- ActionHead depends on bus + translator output + header state

### Not allowed
- primitives depending on task-specific translators
- elements directly depending on other elements
- bus containing hidden policy
- translators containing ontology logic that belongs in primitives/elements
- header updating during decision pass
- ActionHead redefining primitive semantics

---

## Runtime Path

Current canonical runtime path:

1. runner
2. adapter
3. core builder
4. runtime combinator (`C_Pipeline`)
5. elements
6. translator
7. ActionHead
8. telemetry

This is a **runtime orchestration path**, not a full statement of semantic composition.

---

## Current Status

What is already reasonably present:
- primitive store
- element layer
- bus
- header layer
- translators
- ActionHead
- runtime pipeline

What is still missing or underdeveloped:
- semantic combinator layer
- explicit element → combinator declarations
- explicit meta-header layer
- stronger enforcement of primitive/combinator/element boundaries