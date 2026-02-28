# ActionHead

## Purpose

ActionHead is the final action/deployment surface.

It is responsible for:
- draining bus votes
- combining them with translator-facing scores
- applying masks
- blending CO vs classical deployment
- returning the final action plus telemetry

---

## Element Role

Although it lives in the element pipeline, ActionHead is **not** an ontology mechanism element in the strong sense.

It is the final deployment surface.

It is not:
- a primitive
- a semantic combinator
- a header
- a translator

---

## Primitive Dependencies

No direct ontology primitive dependency in the doctrinal sense.

It consumes:
- bus votes
- bus signals
- translator outputs
- header outputs

---

## Semantic Combinator Form

Not part of semantic combinator doctrine proper.

Its responsibility is runtime/action deployment.

---

## Inputs

ActionHead consumes:
- observation envelope
- action domain / action space
- bus votes
- bus signal snapshot
- translator scores
- translator mask
- header control state

---

## Outputs

ActionHead returns at minimum:
- `action`
- `co_policy`
- `co_weight`
- `co_bus_votes`
- `signals`

It may also expose telemetry aliases and counters as documented.

---

## State Mutation

ActionHead may maintain:
- local anti-oscillation state
- local action-surface helper state

It must not mutate:
- primitive doctrine
- header ownership
- translator responsibilities

---

## Why this unit exists

The kernel still requires a final action surface.

Ontology mechanisms do not directly become actions by magic.
A disciplined runtime surface is required.

That is ActionHead.

---

## Forbidden

ActionHead must not:
- pretend to be ontology
- redefine primitive meanings
- silently absorb translator semantics
- call `header.update`
- drain votes more than once per step

It must not casually violate mask discipline.

---

## Mask rule

Mask semantics are binding.

If an action is masked, it must not be chosen except under the explicitly documented mask-blocks-all fallback doctrine.

That fallback is a runtime safety exception, not a semantic endorsement.

---

## Telemetry

ActionHead is responsible for surfacing:
- canonical signal snapshot
- runtime deployment telemetry
- mask-related debug telemetry where enabled

---

## Current Status

- active and essential runtime surface
- not part of primitive-mechanism doctrine proper
- role binding