---
id: stmt.shape-space-directed-unfolding-from-change
type: DR
aliases:
  - S-DR-shape-space-directed-unfolding-from-change
  - DynamicShapeFieldDerivation
  - ShapeSpaceDirectedUnfolding
  - CoarsenessFieldDerivation
title: Shape, CO-space, and directed unfolding from change
concepts:
  - '[[02_Concepts/C-dynamic-shape-coarseness-field]]'
  - '[[02_Concepts/C-outer-formation-route]]'
  - '[[02_Concepts/C-change-trace-invariants]]'
dependencies:
  - '[[01_Statements/02_Outer_Formation/001_S-DF-carried-constraint.md]]'
  - '[[01_Statements/02_Outer_Formation/006_S-DF-reach-relation.md]]'
  - '[[01_Statements/02_Outer_Formation/007_S-DF-localreach-zone.md]]'
  - '[[01_Statements/02_Outer_Formation/008_S-DF-asymmetric-local-contribution.md]]'
  - '[[01_Statements/02_Outer_Formation/012_S-DF-continuation-admissibility.md]]'
  - '[[01_Statements/02_Outer_Formation/013_S-DF-local-comparability-field.md]]'
  - '[[01_Statements/02_Outer_Formation/014_S-DF-remaining-transformation-burden.md]]'
  - '[[01_Statements/02_Outer_Formation/020_S-DF-regime-signature.md]]'
  - '[[01_Statements/02_Outer_Formation/021_S-DF-minimal-adequate-retention.md]]'
  - '[[01_Statements/02_Outer_Formation/022_S-DF-thin-collapse-law.md]]'
parents:
  - '[[01_Statements/02_Outer_Formation/013_S-DF-local-comparability-field.md]]'
  - '[[01_Statements/02_Outer_Formation/014_S-DF-remaining-transformation-burden.md]]'
  - '[[01_Statements/02_Outer_Formation/020_S-DF-regime-signature.md]]'
  - '[[01_Statements/02_Outer_Formation/021_S-DF-minimal-adequate-retention.md]]'
  - '[[01_Statements/02_Outer_Formation/022_S-DF-thin-collapse-law.md]]'
successors:
  - '[[01_Statements/02_Outer_Formation/023_S-DF-similarity-operator.md]]'
  - '[[01_Statements/Definition/S-DF-prm-gauge.md]]'
  - '[[01_Statements/Definition/S-DF-prm-closure-quotient.md]]'
symbols_used: []
sources:
  - path: chat/2026-05-18 user challenge that shape, space, directedness, and coarseness must be explicitly derived rather than assumed
flags:
  - open_proof
tags:
  - layer/foundations
  - domain/ontological
  - type/DR
  - route/outer
  - concept/dynamic-shape-coarseness-field
  - status/evolving
status: evolving
---
# Shape, CO-space, and directed unfolding from change

## Claim (formal)
After carried constraint, bounded reach, asymmetric local contribution, continuation admissibility, local comparability, remaining transformation burden, regime signature, minimal adequate retention, and thin collapse have been earned, CO can define local shape, CO-space, proto-sequencing, coarseness, and dynamic shape update without importing a pre-given container-space, fixed timeline, or static state point.

Shape is the current relational-gauge organization of a bounded local unfolding. CO-space is the locally earned comparability/reach/admissibility field in which continuations stand nearer, farther, open, blocked, strained, or equivalent relative to the current regime. Directed unfolding arises from asymmetric contribution under retained trace and carried constraint, not from a globally presupposed timeline. Coarseness arises because bounded continuation retains only distinctions that remain operative under the current gauge; apparent points are thin collapses of local regions. Shape update is the lawful deformation of local shape-state after continuation, result, trace, and changed burden/relation/admissibility.

## Philosophical Translation (of formal claim)
The theory may now stop using “shape” as an intuitive word and give it a disciplined role. A local unfolding has a shape when its relations, burdens, admissibilities, invariants, and retained distinctions form a gauge that biases what can sensibly continue. That shape is not a fixed object. It is a formed local state of the unfolding. It can deform when what happens next leaves a trace, changes burden, opens or closes admissible continuations, or changes what distinctions need to be retained.

Likewise, CO-space is not a container filled with points. It is the earned local field in which continuations can be compared, reached, blocked, strained, or thinned. A “point” in such a field is not primitive. It is a coarse local ball treated as point-like because finer differences do not currently matter enough to be retained.

## Why this claim is needed
Earlier files already use or imply:
- local shape,
- reach,
- admissibility,
- comparability,
- burden,
- regime signature,
- retention,
- and collapse.

Without this derivation, several later concepts risk jumping their own foundation:
- shape can become a loose metaphor;
- space can smuggle in a pre-given container;
- before/after can smuggle in a full timeline;
- tension/burden can become a generic label for difficulty;
- gauge can be introduced as mathematical rhetoric;
- point/state/action can be treated as primitive rather than as earned thin collapses;
- dynamic shape update can become an ad hoc performance patch.

This file consolidates the bridge from change to relational unfolding, local shape, CO-space, directed sequencing, coarseness, tension/burden, and shape update.

## Definitions

### DF 1.1
*Shape-as-such* :=
The invariant fact that any bounded local unfolding which can continue non-arbitrarily has some relational-gauge organization of admissibility, reach, burden, invariant preservation, and retained distinction.

Shape-as-such does not mean that one specific shape is fixed forever. It means that wherever supportable continuation is locally structured rather than arbitrary, continuation occurs through some formed organization.

### DF 1.2
*Local shape-state* :=
The currently formed relational-gauge configuration of a bounded local unfolding: the operative profile of what bears on what, what can continue, what is blocked, what strains, what can be ignored, what must be retained, and what differences remain relevant under the current regime.

### DF 1.3
*CO-space* :=
The locally earned field of reach, comparability, admissibility, burden, and retained relation in which continuations stand near/far, open/blocked, strained/relieved, equivalent/non-equivalent, or collapse-ready/non-collapse-ready relative to the current gauge.

CO-space is not primitive container-space. Container-like and metric-like spaces are later possible thin collapses or strengthenings of this more basic relational field.

### DF 1.4
*Directed unfolding* :=
The proto-sequential structure that appears when carried constraint and retained trace make some local contributions asymmetrically bear on later/current articulation.

Directed unfolding is weaker than full time. It earns a before/after-like ordering only as asymmetric contribution under retained unfolding; it does not presuppose a global timeline.

### DF 1.5
*Tension* :=
A local asymmetry in the current shape-state relative to supportable continuation.

Tension is not yet burden. It is the deformation-pressure or mismatch implied by the way a formed local structure stands against possible continuation.

### DF 1.6
*Burden* :=
Tension retained as continuation-relevant because it affects supportable continuation, admissibility, stabilization, transformation, collapse, or future shape.

Burden is therefore not cost, reward, generic uncertainty, or subjective difficulty. Cost and uncertainty may later track some burdens in special regimes, but they do not define burden.

### DF 1.7
*Coarseness field* :=
The distribution of retained resolution across a local shape-state: where the unfolding keeps fine distinctions, where it brackets or quotients details, and where a local region may be treated as point-like under the current gauge.

### DF 1.8
*Point-as-ball* :=
A point is a thin collapse of a local region under a coarseness gauge. It is treated as point-like only because distinctions inside that region do not currently alter active burden, admissibility, relation topology, collapse consequence, or continuation identity.

### DF 1.9
*Dynamic shape update* :=
The lawful deformation of local shape-state after selected continuation, public/world response, retained trace, changed burden, changed relation topology, changed admissibility, and changed coarseness requirements.

Dynamic shape update may not be inferred from hidden optimality, post-hoc reward fitting, or baseline performance. It must be grounded in public retained trace and allowed deformation of the current regime.

## Philosophical Justification
The outer route has already earned the following sequence.

1. **Carried constraint**: in a locally persistent structured regime, continuation occurs through local shape rather than beside it.
2. **Reach and local reach-zone**: carried constraint can still bear on current articulation, but only locally and boundedly.
3. **Asymmetric local contribution**: within bounded unfolding, some articulations contribute more directly than others.
4. **Continuation admissibility**: not every deformation remains supportable.
5. **Local comparability field**: admissible and near-admissible continuations can be compared by preservation, loss, and strain before full metric geometry.
6. **Remaining transformation burden**: a present unfolding can stand at a remove from an admissible region; something still has to change.
7. **Regime signature**: the local profile of preservation, burden, admissibility, openness, and history can be characterized.
8. **Minimal adequate retention**: bounded continuation should retain no more and no less structure than remains operative.
9. **Thin collapse law**: when richer structure no longer changes supportable continuation, it may lawfully thin to a sharper special case.

Together these entail a relational-gauge organization of unfolding. That organization is what “local shape” should mean. Since it is built from reach, admissibility, comparability, burden, regime signature, retention, and collapse, it cannot be a primitive container or static label.

## Derivation (Philosophical)

### 1. From carried constraint to relation-bearing unfolding
If continuation occurs through present local shape, then present formation is not inert. Some current differentiations bear on what can follow. This is not yet a full relation network, but it is enough for relation-bearing unfolding: difference can matter for continuation.

### 2. From reach to locality without primitive space
If bearing is bounded and clustered, locality is earned as bounded relevance/reach rather than imported as geometric nearness. A local region is first a reach-zone: a field of what can still bear on what under retained constraint.

### 3. From asymmetric contribution to proto-sequencing
If some articulations contribute more directly than others inside bounded unfolding, then contribution has direction. This gives a before/after-like ordering in the weak sense: not a global timeline, but asymmetric bearing within retained unfolding.

### 4. From admissibility and comparability to CO-space
If some continuations are supportable and others are not, and if supportable/near-supportable continuations can be compared by preservation, loss, and strain, then the unfolding has a local field of admissible relation. This is CO-space: a relational comparability/admissibility/reach field.

### 5. From burden to tension in shape
If a current unfolding remains at a transformation deficit relative to an admissible region, then the current shape-state is asymmetric relative to supportable continuation. That asymmetry is tension. When retained because it matters for continuation, it is burden.

### 6. From regime signature to local shape-state
If a regime has a profile of preservation, burden, admissibility, openness, and history, then shape is not a bare outline. Shape is the local relational-gauge state of that profile.

### 7. From minimal adequate retention to coarseness
If only operative structure should be retained, then resolution is not globally uniform. Some regions require fine distinctions; others can be bracketed, quotientized, or collapsed. This yields a coarseness field.

### 8. From thin collapse to point-as-ball
If richer structure may thin when distinctions no longer matter, then a point is earned as a collapsed local region. It is a ball under a gauge, not an ontological atom.

### 9. From selected continuation to shape update
If continuation occurs through local shape, and later unfolding carries trace, changes burden, changes admissibility, or changes relation topology, then the next local shape-state may differ. Shape update is therefore lawful deformation of the relational-gauge field after retained continuation, not free rewriting of the problem.

## Derivation (Formal/Logical/Mathematical)
```text
Let H_t be a bounded local unfolding at a retained articulation t.
Let Reach_t encode bounded bearing among articulations.
Let Adm_t encode continuation admissibility.
Let Comp_t encode local preservation/loss/strain comparison.
Let B_t encode remaining transformation burden.
Let Sig_t encode regime signature.
Let Ret_t encode minimal adequate retention.
Let Collapse_t encode lawful thinning under current gauge.

Then local shape-state may be represented schematically as:

Shape_t = <Reach_t, Adm_t, Comp_t, B_t, Sig_t, Ret_t, Collapse_t>

CO-space at t is not an added container. It is the relational field induced by
<Reach_t, Adm_t, Comp_t, B_t> under Sig_t.

Directed unfolding is the asymmetric dependency/order relation induced by
carried constraint and trace:

Dir_t(a, b) holds when articulation a bears on b under retained trace
more directly than b bears on a within the current bounded unfolding.

Coarseness may be represented as a resolution function:

rho_t(region) = retained resolution required for distinctions inside region
to remain operative for Adm_t, B_t, Comp_t, Sig_t, or Collapse_t.

A point-like item p is lawful only when there exists a local region U such that:

for all distinctions d inside U,
d does not alter current admissibility, burden, relation topology,
collapse consequence, or continuation identity beyond tolerance theta_t.

Then p = Collapse_t(U) under gauge theta_t.

Dynamic shape update is schematically:

Shape_{t+1} = Update(
  Shape_t,
  selected_continuation_t,
  observed_response_{t+1},
  retained_trace_{t+1},
  changed_burden_{t+1},
  changed_relation_topology_{t+1},
  changed_admissibility_{t+1},
  changed_coarseness_need_{t+1}
)

subject to the no-oracle condition:
Update may use only public/retained trace and allowed regime deformation,
not hidden optimality or post-hoc baseline success.
```

## Consequences for kernel interpretation
This derivation does not immediately require implementation of a full `DynamicShapeField`. It does require that later implementation treat shape carefully.

Valid downstream use:
- problem shape may act as a public prior/gauge;
- local branch relations may deform the immediate commitment gauge;
- public action/result traces may update local shape-state if the update rule is explicit;
- coarseness may determine which differences are retained or quotientized;
- apparent states and points may be treated as thin collapses only when the collapse is earned.

Invalid downstream use:
- shape as an all-purpose explanation for any behavior;
- shape updates inferred from hidden state or benchmark success;
- problem-shape values that encode the answer policy;
- point/state/action treated as primitive atoms without earned collapse;
- dynamic shape as a new name for tuning thresholds after failures.

## Clarifications / Further Context
- Shape-as-such is invariant only in the weak sense that structured continuation always has some local relational organization. A particular local shape-state is formed and can change.
- The current implementation has a static problem-shape prior, a local shape-gauged readout correction, and a first-pass persistent DynamicShapeField. It does not yet implement a final mathematical coarseness topology or fully validated family-wide dynamic shape behavior.
- CO-space is earlier and weaker than metric space. Metric structure requires later strengthening.
- Proto-sequencing is earlier and weaker than full time. It is directed asymmetry in retained unfolding.
- Coarsening is primarily a feature of bounded retention/modeling/problem closure, not a claim that reality itself loses detail elsewhere when a bounded agent focuses locally.

## Objection 1: “Is shape being smuggled in?”
No, not if this file is read after the dependencies. Shape is introduced only after carried constraint, reach, locality, asymmetric contribution, admissibility, comparability, burden, regime signature, retention, and collapse. Shape names their formed local organization; it is not a new primitive.

## Objection 2: “Is this just space in new words?”
No. Classical container-space assumes a field of points in which things are located. CO-space begins as relational comparability/reach/admissibility under unfolding. Container-like or metric-like space may later be recovered as a special stabilized/thinned case.

## Objection 3: “Does this make before/after circular?”
No. The file does not assume full temporal order. It derives proto-sequencing from asymmetric local contribution under retained trace. Full timeline structure remains downstream.

## Objection 4: “Does dynamic shape update create a hidden solver?”
It would if unconstrained. That is why the update rule is restricted to public/retained trace, changed burden, relation topology, admissibility, and coarseness need. Hidden optimality, baseline success, and post-hoc reward are not valid update evidence.

## What this file establishes
This file establishes:
1. shape as relational-gauge organization, not metaphor;
2. CO-space as earned reach/comparability/admissibility field, not primitive container;
3. directed unfolding as asymmetric contribution under retained trace, not full presupposed time;
4. tension as shape-asymmetry relative to continuation;
5. burden as retained continuation-relevant tension;
6. point/state as possible thin collapse of local region under coarseness gauge;
7. dynamic shape update as a lawful but not yet fully implemented target.

## What this file does not yet establish
It does **not** yet establish:
- a full mathematical topology of CO-space;
- a metric tensor, norm, or distance function;
- a complete dynamic shape update algorithm;
- a full temporal theory;
- a full theory of attention, subjectivity, or consciousness;
- empirical evidence that a kernel using these notions performs well.

## Next Steps in Chain
- suggest: [[01_Statements/02_Outer_Formation/023_S-DF-similarity-operator.md]]
- suggest: [[01_Statements/Definition/S-DF-prm-gauge.md]]
- suggest: [[01_Statements/Definition/S-DF-prm-closure-quotient.md]]
- suggest: future `S-DR-dynamic-shape-update-contract`
- suggest: future `S-DR-coarseness-field-and-projection-horizon`

## Active-chain status
**Status band:** derived-consolidating / implementation-target-opening

**Reason:** the file consolidates implications already present in the first outer route and prevents shape, space, directedness, coarseness, and update from remaining loose metaphors. The dynamic-shape-update part is a derived target, not a completed implementation.

## Tags
#type/DR #layer/foundations #domain/ontological #route/outer #concept/dynamic-shape-coarseness-field #status/evolving
