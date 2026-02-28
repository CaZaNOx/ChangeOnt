# Architecture Doctrine

## Purpose

This page defines the **binding conceptual architecture** of the ChangeOnt kernel.

It does **not** claim that all formulas are final.  
It defines the roles of the layers so that implementation can remain modular, coherent, and philosophically aligned while the exact laws and constants are still being researched.

The kernel is designed to support:
- single implementation of each primitive
- single implementation of each combinator
- single implementation of each element
- controlled experimentation through assembly, weighting, and activation
- no semantic duplication across layers

---

## Core Principle

The kernel must distinguish clearly between:

1. **what semantic ingredients exist**
2. **how they are combined**
3. **what semantically meaningful mechanisms they form**
4. **how those mechanisms are controlled under stability**
5. **how the final package interfaces with a concrete task**

These are different architectural roles and must not be collapsed into one another.

---

## Layer Model

### Layer 0 — Primitives

Primitives are **candidate ontological ingredients** of Change Ontology.

A primitive expresses that some semantic quantity, operator, or relation is meaningful enough to exist in the kernel as a reusable component.

Examples:
- bend / distance
- gauge
- complexity / compressibility pressure
- precision / density
- loopiness
- closure / quotient support
- branching / convergence style structural operators

A primitive:
- must exist only once in code
- must not be duplicated inside elements
- may expose state and/or operations
- must not contain task-specific logic
- must not directly decide final actions

Primitives are not yet assumed to have final formulas.  
They are reusable semantic building blocks from which higher-level hypotheses are constructed.

---

### Layer 1 — Semantic Combinators

Semantic combinators define **how primitives are composed operationally**.

A combinator does not introduce a new primitive.  
It specifies a law of assembly between primitive outputs.

Examples:
- additive composition
- multiplicative composition
- gated composition
- weighted blending
- CO-native composition operators
- classical composition operators

Combinators answer questions like:
- is the relation additive or multiplicative?
- is one primitive gating another?
- does the same primitive contribute differently in different elements?

A semantic combinator:
- must exist only once in code
- must be reusable across elements
- must be explicit and logged
- must not smuggle task-specific logic
- must not silently inject dependencies

Semantic combinators are where candidate law-forms are explored.

---

### Layer 2 — Elements

Elements are **semantically meaningful mechanisms** built from primitives via semantic combinators.

An element is not a primitive.  
An element is a hypothesis that a certain grouping of primitives, composed in a certain way, expresses a coherent mechanism.

Examples:
- novelty modulation
- variable birth
- identity / closure
- density / precision control
- breadth / depth scheduling

An element:
- exists only once in code
- declares which primitives it uses
- declares which semantic combinators it uses
- may be run alone or in combination with other elements
- produces votes and/or scalar signals
- must not directly call other elements
- must not re-implement primitive logic locally

The same primitive may appear in multiple elements, but with different combinators, weights, or roles.

This is intentional.

---

### Layer 3 — Bus

The bus is a **transport and storage surface**, not a semantic decision-maker.

It carries:
- votes
- scalar signals
- canonical inter-element information

The bus:
- stores
- exposes
- routes

The bus must not:
- contain hidden policy
- perform semantic aggregation decisions
- become a god-object

Elements may communicate only through explicitly documented bus contracts.

---

### Layer 4 — Header

The header is the **internal control layer**.

The header does not define ontology primitives.  
It governs how strongly and how often the kernel should act under locally detected stability conditions.

Examples:
- co_weight
- update cadence
- hysteresis
- cooldown
- local stability modulation

The header:
- may read canonical signals from elements
- may update only on the update pass
- must not contain task-specific translator logic
- must not silently redefine primitive meaning

The header is about **deployment and control**, not semantic discovery.

---

### Layer 5 — Meta Header

The meta header is the **external prior/control layer**.

It introduces contextual information that is not discovered internally from kernel dynamics, for example:
- task-family priors
- external stability expectations
- provided assumptions about rule change likelihood

The meta header must:
- be explicitly logged
- remain separate from internal header logic
- never be confused with discovered ontology
- never use hidden oracle information

Meta-header influence is allowed only as an explicit prior.

---

### Layer 6 — Translators and Action Surface

The translator/action layer is the interface between:
- the abstract kernel
- the concrete task environment

Translators:
- convert task-specific observations into canonical contracts the kernel can use
- provide task-specific score hints and validity masks
- must not contain ontology logic that belongs in primitives/elements

ActionHead:
- collects final usable information
- respects masks and constraints
- combines kernel outputs and classical fallbacks
- emits final action and telemetry

This layer is task-facing, not ontology-defining.

---

## Runtime Combinators vs Semantic Combinators

The repo currently contains runtime orchestration components such as `C_Pipeline`.

These are **runtime combinators**, not semantic combinators.

- **Semantic combinators** define laws of composition between primitives.
- **Runtime combinators** define execution flow, update order, and orchestration.

These two categories must not be conflated.

---

## Research Posture

The architecture distinguishes between:

- **primitives** as candidate meaningful ingredients
- **semantic combinators** as candidate law-forms
- **elements** as candidate meaningful mechanisms

The kernel is not yet assumed to know the final true formulas.

The purpose of the framework is to allow disciplined testing of:
- which primitives are useful
- which semantic combinators best express their relations
- which elements provide transfer and explanatory value
- how combinations of elements behave across tasks
- how internal and external stability should govern deployment

---

## Single-Implementation Rule

The framework must avoid semantic duplication.

Therefore:
- each primitive exists once
- each semantic combinator exists once
- each element exists once
- experimentation happens by configuration, activation, weighting, and assembly
- not by cloning files into many near-duplicate variants

Variants should be expressed through:
- declared primitive dependencies
- declared combinator choices
- declared weights
- declared active element sets
- declared header/meta-header settings

---

## Prohibitions

The following are prohibited unless explicitly revised by future binding docs:

- duplicating primitive logic inside elements
- duplicating combinator logic inside elements
- task-specific ontology logic inside translators
- hidden policy inside the bus
- header updates during decision pass
- silent dependency injection
- uncontrolled proliferation of per-element fork files

---

## Current Status

The current codebase is an early working slice of this doctrine.

It is acceptable for:
- basic kernel execution
- telemetry
- QA/spec gating
- initial element isolation and smoke testing

It is not yet a complete realization of this doctrine.

In particular:
- semantic combinator semantics are underdeveloped
- primitive/combinator/element boundaries are not fully enforced
- some elements still contain logic that should later migrate into primitives or semantic combinators
- meta-header behavior is not yet fully specified as a separate binding layer

Future refactoring should move the code **toward** this doctrine without breaking existing working functionality.

---

## Immediate Design Consequence

The next stages of development should prefer:

1. clarifying primitive contracts  
2. clarifying semantic combinator contracts  
3. making element dependencies explicit  
4. supporting element-isolation and combination experiments through configuration  
5. preserving one implementation per semantic unit

This is the binding target architecture.