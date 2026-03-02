# docs/code_reference/agents/co/translators.md

# CO Translators

## Purpose

This file documents the translator layer inside the CO integration path.

Translators are first-class boundary operators between:
- family-local task structure
and
- the CO kernel’s internal path-space representation.

They are also the boundary operators between:
- the CO continuation surface
and
- concrete task actions.

---

## Why this layer exists

The CO kernel is not supposed to think natively in:
- maze move tokens,
- bandit arm IDs,
- renewal symbol labels,
- or flat task-state features.

The translator layer exists so that:
- task-local semantics remain local,
- the kernel can remain problem-agnostic internally,
- and the same general CO loop can operate across multiple families.

---

## Canonical translator responsibilities

**Binding**

Every translator must do three things:

### 1. Input translation
Translate task-local observation/input into a CO-facing path-space update.

### 2. Output translation
Translate the kernel’s continuation surface into a concrete task action.

### 3. Feedback translation
Translate environment feedback back into CO-relevant update structure.

---

## Important principle

**Binding**

The bus or continuation surface is richer than the final task action.

The translator is the legitimate collapse point into family-local action semantics.

This means:
- the kernel may carry partial preselection, weighted branch preferences, constraints, confidence, etc.
- the translator collapses that into a legal concrete task action.

---

## Main translator files

### `bandit_translator.py`
#### Purpose
Translate bandit-local structure into CO-facing path-space updates and continuation/action mappings.

#### Expected input-side behavior
Should convert bandit-local information such as:
- current choice context
- reward-related local structure
- stationarity/deformation-relevant hints
into path-space relevant updates rather than flat state copying.

#### Expected output-side behavior
Should convert the continuation surface into:
- a concrete arm selection

#### Important target-state requirement
Must not rely on broken/mismatched primitive APIs.
If a primitive such as a bandit statistics holder is part of the contract, translator and primitive APIs must match.

---

### `maze_translator.py`
#### Purpose
Translate maze-local structure into path-space updates and continuation/action mappings.

#### Expected input-side behavior
Should convert local maze information such as:
- realized movement transitions
- local constraints
- local branch-space
- revisitation or density information
- goal-relevant continuation shaping
into the kernel’s path-space update form.

#### Expected output-side behavior
Should convert the continuation surface into:
- a legal maze action or move direction

#### Why maze translator matters
Maze is one of the strongest tests of whether the path-space view is being implemented honestly.

---

### `renewal_translator.py`
#### Purpose
Translate renewal/sequence-local structure into path-space updates and continuation/action mappings.

#### Expected input-side behavior
Should convert sequence/event context into:
- recurrence-sensitive updates
- closure/compressibility relevant structure
- continuation-relevant branch or next-event candidate shaping

#### Expected output-side behavior
Should convert the continuation surface into:
- a concrete renewal action/prediction

#### Important target-state requirement
Must not silently collapse the family to shallow “last event only” behavior unless that collapse is explicitly justified by regime/classicality.

---

## Translator contracts

### Contract A — task-local in, CO-form out
**Binding**

Translators must output CO-facing updates in terms of the kernel’s internal representation, not just pass raw task-local objects through unchanged.

### Contract B — continuation surface in, action out
**Binding**

Translators must be able to collapse the richer continuation surface into a concrete legal task action.

### Contract C — feedback back into CO form
**Binding**

Translators must feed back task-local results into a kernel-relevant update structure.

---

## Relation to adapters

Adapters and translators are closely related but not identical.

### Adapter
Owns runner-facing family loop bridging.

### Translator
Owns the semantic mapping between:
- family-local task structure
and
- kernel-internal structure.

Implementations may co-locate some behavior, but the conceptual distinction must remain explicit.

---

## Relation to classical collapse

In highly classical regimes:
- the continuation surface may already be strongly collapsed toward the classical stream

Even then, translators remain necessary because they still:
- interpret the continuation surface,
- apply legality and family-local semantics,
- and map back task-local feedback.

---

## Misalignment examples

Translator handling is misaligned if:
- the kernel is forced to think directly in final task action tokens,
- translators merely relay flat task-state features unchanged,
- family-local legality is hidden inside the kernel rather than at the boundary,
- or feedback is not translated back into path-space relevant structure.