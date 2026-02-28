# Element Spec Requirements

## Purpose

This page defines what every element spec file must contain.

It is binding for all files in `05_ELEMENTS/`.

---

## Definition Reminder

An element spec defines a **semantically meaningful mechanism** built from primitives via semantic combinators.

An element is not:
- a primitive
- a translator
- a header
- the final action surface

---

## Every element spec must contain

### 1. Purpose
State what mechanism this element represents.

Examples:
- identity mechanism
- birth mechanism
- density/precision mechanism
- history-adaptive modulation mechanism

### 2. Element Role
State clearly why this is an element and not a primitive/header/translator.

### 3. Intended Primitive Dependencies
List which primitives this element should consume.

If current implementation is partial, say so honestly.

### 4. Intended Semantic Combinator Dependencies
State how the element conceptually combines primitives.

If the exact law is not yet frozen, say so.

### 5. Outputs
State what signals, votes, counters, or other outputs the element may produce.

### 6. State Mutation
State what local or canonical state the element may mutate.

This must be explicit.

### 7. Why this element exists
State the philosophical/architectural reason the primitive bundle forms a meaningful mechanism.

### 8. Forbidden
State what the element must not do.

Examples:
- directly choose final actions
- call other elements directly
- contain hidden translator logic
- duplicate primitive logic locally

### 9. Telemetry
State what telemetry is canonical, optional, or indirect.

### 10. Current Status
State whether the element is:
- active and central
- active but secondary
- reserved/future
- provisional in exact law but architecturally justified

---

## Most Important Rule

An element spec must say both:

- **what primitives it uses**
- **why those primitives belong together as one mechanism**

If it only does one of these, it is incomplete.

---

## Element Spec Anti-Patterns

An element spec is wrong if it:

- just describes implementation behavior with no mechanism role
- hides primitive dependencies
- acts like the element is itself a primitive
- silently invents task-specific rules
- directly collapses into ActionHead behavior

---

## Semantic Combinator Rule

Even if semantic combinators are not fully implemented yet, every element spec should already speak in that direction:

- what kind of relation between primitives is being assumed?
- additive?
- multiplicative?
- gated?
- thresholded?
- weighted blend?

If unknown, say unknown.  
Do not hide the issue.

---

## Reviewer Checklist

An element spec is complete only if a reviewer can answer:

- What mechanism is this?
- Why is it one mechanism rather than several unrelated primitives?
- Which primitives does it consume?
- How are they conceptually combined?
- What may it output?
- What may it mutate?
- What must it not do?