# Primitive Spec Requirements

## Purpose

This page defines what every primitive spec file must contain.

It is binding for all files in `04_PRIMITIVES/`.

---

## Definition Reminder

A primitive spec defines a **reusable semantic ingredient** of the kernel.

A primitive is not:
- a full mechanism
- an element
- a translator
- a final action policy

---

## Every primitive spec must contain

### 1. Purpose
State what recurring semantic demand this primitive encodes.

Examples:
- bend/difference
- modulation
- complexity pressure
- precision
- recurrence
- shared state support
- closure/grouping

### 2. Primitive Role
State clearly why this is a primitive and not an element/header/translator.

### 3. Inputs
State what kinds of inputs the primitive may consume.

This should be typed conceptually, not just “stuff from observation”.

### 4. Outputs
State what the primitive returns or exposes.

Examples:
- scalar
- distance
- gain
- threshold-like quantity
- shared store
- class/group assignments

### 5. State Mutation
State whether the primitive is:
- pure
- near-pure
- stateful by design

If stateful, say what canonical state it owns.

### 6. Why this primitive exists
State the philosophical/architectural motivation.

Not flowery language — real reason.

### 7. Forbidden
State what the primitive must not do.

Examples:
- choose final actions
- contain task logic
- become a full mechanism
- silently duplicate another unit’s role

### 8. Telemetry
State whether telemetry is:
- direct
- indirect via consuming element
- not required

### 9. Current Status
State whether the primitive is:
- binding and operational
- provisional but justified
- future/reserved

---

## Primitive Spec Anti-Patterns

A primitive spec is wrong if it:

- describes a whole mechanism rather than a reusable ingredient
- contains translator/task logic
- directly defines final action policy
- hides a semantic combinator inside “algorithm” language without saying so
- overclaims final truth where only minimal operationalization exists

---

## Formula Rule

A primitive spec may include a v1 formula if one is currently binding.

If the formula is not genuinely frozen, say:
- minimal v1 operationalization
- formula provisional
- role stable, exact law not yet final

This distinction is mandatory.

---

## Shared Store Rule

If a primitive is a canonical shared store primitive, the spec must explicitly state:
- what it stores
- why it is canonical
- what must not be duplicated elsewhere

This applies especially to primitives like state/prototype support primitives.

---

## Reviewer Checklist

A primitive spec is complete only if a reviewer can answer:

- What semantic ingredient is this?
- Why is it primitive-level?
- What may it read?
- What may it expose?
- Does it own state?
- What is forbidden?
- Is its exact law frozen or provisional?