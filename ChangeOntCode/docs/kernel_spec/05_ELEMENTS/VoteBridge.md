# VoteBridge

## Purpose

VoteBridge is the infrastructure bridge from element-level mechanism outputs into bus votes.

It is part of runtime delivery, not ontology discovery.

---

## Element Role

VoteBridge is present in the element folder because it sits in the element pipeline, but architecturally it is an **infrastructure bridge**, not a semantic ontology mechanism.

---

## Primitive Dependencies

No strong ontology primitive dependency.

It consumes:
- mechanism outputs
- local scores or vote-ready quantities

---

## Semantic Combinator Form

None in the strong doctrine sense.

VoteBridge should not be treated as a primitive-mechanism relation-form.

---

## Inputs

VoteBridge may consume:
- element-level score outputs
- action candidates
- runtime context needed to publish votes

---

## Outputs

It publishes:
- bus votes via the canonical vote store

---

## State Mutation

VoteBridge may mutate only:
- vote bus content

It must not:
- select final actions
- redefine element meaning
- own ontology state

---

## Why this unit exists

Semantic mechanisms need a disciplined path into the action surface.
VoteBridge is that disciplined path.

---

## Forbidden

VoteBridge must not:
- become an ontology mechanism in disguise
- absorb ActionHead responsibilities
- drain votes
- choose final actions

---

## Telemetry

Indirect:
- visible via bus vote counts and downstream co_debug fields

---

## Current Status

- active infrastructure unit
- not part of primitive-mechanism doctrine proper