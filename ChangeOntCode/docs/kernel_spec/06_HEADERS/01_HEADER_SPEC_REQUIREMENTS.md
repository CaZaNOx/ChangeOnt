# Header Spec Requirements

## Purpose

This page defines what every header spec file must contain.

It is binding for all files in `06_HEADERS/`.

---

## Definition Reminder

A header spec defines an **internal control/deployment layer**.

A header is not:
- a primitive
- a semantic combinator
- an element
- a translator
- the final action chooser

---

## Every header spec must contain

### 1. Purpose
State what control posture or deployment role the header provides.

Examples:
- stability-sensitive control
- classical-slice control
- identity-biased control

### 2. Header Role
State clearly why this unit is a header and not ontology/mechanism.

### 3. Inputs
State what signals/state the header may consume.

### 4. Outputs
State what control-facing state the header may expose.

Examples:
- `co_weight`
- thresholds
- stability-sensitive control state
- deployment emphasis

### 5. State Mutation
State clearly that header mutation occurs on update pass only.

If there are exceptions, they must be explicit and justified.

### 6. Why this header exists
State the control reason for the header’s existence.

Not ontology proof — deployment rationale.

### 7. What this header is not
This is especially important for headers.

A header spec must explicitly say it is not:
- a primitive law
- an element
- a translator
- a direct action policy

### 8. Forbidden
State what the header must not do.

Examples:
- update on decision pass
- directly choose actions
- silently absorb translator logic
- redefine primitive meaning

### 9. Telemetry
State what debug/control telemetry may appear.

### 10. Current Status
State whether the header is:
- active current control layer
- secondary mode
- provisional in exact formula
- future/reserved

---

## Header Spec Anti-Patterns

A header spec is wrong if it:

- reads like ontology rather than control
- silently defines task-specific policy
- blurs into translator/action surface behavior
- hides update-pass ownership
- pretends exact equations are final when they are not

---

## Mandatory Ownership Rule

Every header spec must explicitly say:

- headers update only on update pass
- headers are control/deployment layers
- headers do not define primitives or elements

This is binding.

---

## Reviewer Checklist

A header spec is complete only if a reviewer can answer:

- What control role does this header play?
- What can it read?
- What can it expose?
- When may it update?
- What must it never do?
- Why is this not an ontology mechanism?