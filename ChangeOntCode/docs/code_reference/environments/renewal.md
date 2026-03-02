# docs/code_reference/environments/renewal.md

# Renewal Environments

## Purpose

Renewal environments model sequential/event-based unfolding where recurrence, return, closure, and predictive structure matter.

---

## Why this family exists

Renewal is important for testing:
- recurrence,
- sequence structure,
- closure tendencies,
- compressibility,
- order sensitivity,
- and the distinction between highly classical repeating regimes and more structurally shifting sequence regimes.

This family is especially useful for seeing whether CO can reason over unfolding sequence structure rather than only over spatial navigation.

---

## Family-local semantics

A renewal environment typically defines:
- sequence/event generation rules,
- current observation context,
- reward or correctness feedback,
- and stopping/horizon conditions.

---

## Reset contract

**Binding**

Reset should clearly define:
- starting context,
- what sequence state is reinitialized,
- whether generative rules remain stable,
- and what initial observation is returned.

---

## Step contract

**Binding**

Step should clearly define:
- what the chosen action/prediction means,
- what correctness/reward/feedback is returned,
- and how terminality or horizon limits are represented.

---

## Classicality relevance

Renewal environments may sit on a spectrum from:
- highly classical/stationary recurrence,
to
- more deforming or structurally shifting sequential worlds.

This makes them useful for testing:
- when classical sequence models are enough,
- and when CO-sensitive mechanisms reopen.

---

## Translator relevance

The renewal translator must convert sequence-local context into:
- path-space relevant updates,
- recurrence/closure/compressibility-relevant structure,
- and update feedback meaningful to the kernel.

A translator that collapses renewal entirely to shallow “last symbol only” behavior is not an honest implementation unless that collapse is explicitly justified by regime/classicality.

---

## New environment integration rule

A new renewal-like environment should document:
- event generation semantics
- stability/change assumptions
- feedback semantics
- horizon/terminality behavior
- what sequence-local structure is legitimately available to STOA and CO

---

## Misalignment examples

Renewal environment handling is misaligned if:
- sequence structure is undocumented,
- translator/primitives expect APIs the environment family does not support,
- or the family is treated as recurrent/closure-rich in docs but only shallow last-step information reaches the kernel.