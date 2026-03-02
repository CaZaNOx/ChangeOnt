# docs/code_reference/environments/maze1.md

# Maze Environments

## Purpose

Maze environments model local navigation under spatial constraints, path branching, revisitation, and goal-directed continuation.

---

## Why this family exists

Maze is especially important for CO because it naturally expresses:
- local path geometry,
- branching,
- recurrence,
- density/revisitation,
- closure/opening,
- and directional/asymmetric path dependence.

It is one of the strongest families for testing whether the kernel genuinely reasons over unfolding path structure.

---

## Family-local semantics

A maze environment typically defines:
- spatial layout,
- legal moves,
- start location,
- goal relation or objective,
- terminality,
- walls/constraints,
- and episode reset behavior.

---

## Reset contract

**Binding**

Reset should clearly define:
- start position semantics,
- whether layout is fixed or regenerated,
- what the initial observation contains,
- and what parts of the episode state are reinitialized.

---

## Step contract

**Binding**

Step should clearly define:
- what a move/action means,
- how legality is handled,
- what position or local feedback is returned,
- whether reward/penalty exists,
- and how terminality is represented.

---

## Path-space relevance

Maze environments are strongly relevant to:
- local branch-space,
- bend/deformation of continuation,
- recurrence/loopiness,
- closure/opening,
- density/precision,
- asymmetry and order sensitivity.

Because of that, maze is also one of the strongest stress tests for whether CO is actually wired honestly.

---

## Translator relevance

The maze translator must convert spatial-local task information into a CO-facing path-space update.

That includes, where appropriate:
- local branch candidates,
- constraints,
- realized movement transitions,
- revisitation/density effects,
- local goal-related continuation shaping,
- and update-relevant feedback.

---

## Important current risk

Maze is also the family most likely to reveal:
- pathological oscillation,
- endless local loops,
- bad masking,
- or weakly grounded multi-element interactions.

For that reason, the maze family documentation must be especially explicit.

---

## New environment integration rule

A new maze-like environment should document:
- action set
- legal move semantics
- layout/source-of-constraints
- terminality conditions
- reward/penalty semantics
- and what local structure is available to the translator

---

## Misalignment examples

Maze environment handling is misaligned if:
- move legality is unclear,
- local branch-space is erased before translation,
- resets destroy documented continuity assumptions without disclosure,
- or CO maze runs can enter endless local oscillation without the family contract documenting how progress/termination is supposed to work.