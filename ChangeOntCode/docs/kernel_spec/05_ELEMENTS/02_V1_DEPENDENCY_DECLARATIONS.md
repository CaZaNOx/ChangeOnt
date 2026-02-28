# V1 Dependency Declarations

## Purpose

This page states the intended **v1 primitive dependencies** and **v1 semantic combinator forms** for the currently active elements.

It exists so that implementation work can stop hiding the relation between:
- primitives
- semantic combinators
- elements

This page is binding for v1 architectural intent.

---

## Rule

For each active element we now distinguish:

1. **primitive dependencies**
2. **semantic combinator form currently intended**
3. **what is already explicit in code**
4. **what is still only implicit / provisional**

This is a declaration page, not the full detailed element spec.

---

## EA_HAQ

### Primitive dependencies
- P2_Gauge
- optional history/state support
- optional P7_Precision influence later

### Intended semantic combinator form
- primarily **SC_MultiplicativeCoupling**
- optionally **SC_AdditiveBlend** for accumulated novelty contributions

### v1 meaning
EA_HAQ is a modulation mechanism, not merely a raw novelty counter.

Its core philosophical role is:
- recent history changes how strongly current signals should matter

That makes multiplicative modulation the right primary law-form.

### Status
- role binding
- exact formula provisional

---

## EB_GHVC

### Primitive dependencies
- P3_MDL
- P10_ChangeOpsCore
- optional P12_ClosureQuotient
- later richer birth-related primitives may be added

### Intended semantic combinator form
- primarily **SC_GatedThreshold**
- secondarily **SC_AdditiveBlend** or simple weighted accumulation inside the trigger score

### v1 meaning
EB_GHVC is a birth/admission mechanism.

Its core philosophical role is:
- not every fluctuation should create new structure
- admission requires sufficient pressure / evidence

That makes threshold gating the correct primary law-form.

### Status
- role binding
- exact scoring formula provisional
- threshold/admission structure binding

---

## EC_Identity

### Primitive dependencies
- P1_BendMetric
- optional P12_ClosureQuotient later
- canonical identity memory support

### Intended semantic combinator form
- primarily **SC_GatedThreshold**
- optionally **SC_MultiplicativeCoupling** later if precision/gauge modulates identity strictness

### v1 meaning
EC_Identity is an identity judgment mechanism.

Its core philosophical role is:
- sameness is not primitive identity, but locally admitted continuity under bounded difference

That makes threshold gating the right primary law-form in v1.

### Status
- role binding
- current bend-threshold structure binding
- richer modulation future/provisional

---

## EG_DensityPrecision

### Primitive dependencies
- P7_Precision
- local visit-density tracking support
- possibly P2_Gauge later

### Intended semantic combinator form
- primarily **SC_AdditiveBlend**
- optionally **SC_MultiplicativeCoupling** later

### v1 meaning
EG_DensityPrecision combines local density / revisit / precision-sensitive pressure into a continuous hint signal.

That makes additive accumulation the right default v1 law-form.

### Status
- role binding
- exact formula provisional

---

## EH_BreadthDepth

### Primitive dependencies
- P8_Loopiness
- possible future breadth/depth primitive support

### Intended semantic combinator form
- primarily **SC_WeightedSelection**
- optionally **SC_GatedThreshold**

### v1 meaning
EH_BreadthDepth is not about accumulation but about preference between exploration styles.

That makes weighted selection the right primary law-form.

### Status
- secondary / non-central
- role valid
- exact formula provisional

---

## VoteBridge

### Primitive dependencies
- no semantic primitive dependency in the strong sense
- consumes element outputs

### Intended semantic combinator form
- none in the ontology sense
- this is an infrastructure bridge

### v1 meaning
VoteBridge is not a semantic mechanism.
It is an output bridge from element-level mechanism results to bus votes.

### Status
- active infrastructure component
- not part of primitive-mechanism doctrine proper

---

## ActionHead

### Primitive dependencies
- no ontology primitive dependency in the strong sense
- consumes bus state, translator outputs, and header outputs

### Intended semantic combinator form
- not part of semantic combinator doctrine proper
- this is the final action surface

### v1 meaning
ActionHead is an action/deployment surface, not an ontology mechanism.

### Status
- active runtime surface
- not a primitive-combinator-element unit

---

## Binding takeaway

The current doctrine for v1 is:

- EA_HAQ -> modulation
- EB_GHVC -> thresholded admission
- EC_Identity -> thresholded continuity judgment
- EG_DensityPrecision -> additive continuous hinting
- EH_BreadthDepth -> weighted competition/preference

This is the intended architecture the code should now become more explicit about.