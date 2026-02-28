# H_SSI

## Purpose

H_SSI is the default **internal control header** for the current ChangeOnt kernel slice.

Its role is to regulate how strongly the kernel should act as CO-like versus classical-like under locally detected stability conditions.

H_SSI does **not** define ontology primitives.  
It is a control layer.

---

## Header Role

H_SSI is a **header**, not:
- a primitive
- a semantic combinator
- an element
- a translator
- the ActionHead

It consumes kernel-visible signals and maintains internal control state.

Its job is to answer questions like:
- how stable does the current local regime appear?
- how strongly should CO weighting currently matter?
- how much should update-sensitive behavior influence action blending?

---

## Inputs

H_SSI may consume:
- canonical signals emitted by elements
- bounded internal header state
- current observation envelope on update pass
- optional feedback passed via update path

Typical relevant influences may include:
- identity stability
- birth pressure
- density/precision hints
- recurrence / loopiness hints
- bounded running estimates of regime stability

---

## Outputs

H_SSI may expose header state such as:
- `co_weight`
- effective threshold values
- local stability estimates
- other control-facing state needed by runtime surfaces

These outputs influence runtime deployment.  
They do not constitute a semantic ontology mechanism by themselves.

---

## State Mutation

H_SSI may mutate only on the **update pass**.

That means:
- `C_Pipeline.run_update(...)` may call `header.update(...)`
- decision pass must not update header state

This ownership rule is binding.

---

## Why this header exists

The ontology-facing kernel may contain meaningful semantic machinery, but not every local regime should deploy the same way at every moment.

If some local situations are:
- more stable
- more recurrent
- less likely to require reinterpretation

then control intensity and blending behavior should adapt.

H_SSI is the current internal control surface for that adaptation.

---

## What H_SSI is not

H_SSI is not:
- a primitive law of change
- a replacement for semantic combinators
- an element that discovers ontology
- a translator of task semantics

It is an **internal deployment/control layer**.

---

## Forbidden

H_SSI must not:
- update on decision pass
- use hidden oracle state
- silently absorb translator responsibilities
- silently redefine primitive meanings
- directly choose final actions

---

## Telemetry

H_SSI may surface or influence telemetry such as:
- `co_weight`
- debug header update counters/sources
- regime-control state if explicitly logged

Header telemetry is about deployment and control, not ontology truth claims.

---

## Current Status

H_SSI is the default usable internal header for v1.

Its exact equations may still evolve, but its architectural role is fixed:
- internal stability-sensitive control header