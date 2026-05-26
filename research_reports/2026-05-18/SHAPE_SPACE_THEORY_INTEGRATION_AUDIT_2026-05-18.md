# Shape / Space / Directed-Unfolding Theory Integration Audit — 2026-05-18

## Purpose

Audit whether the new canonical derivation
`TheoryOfChange_main/01_Statements/02_Outer_Formation/022A_S-DR-shape-space-directed-unfolding-from-change.md`
is integrated into the active theory/docs route rather than standing as an isolated addition.

This audit is theory/docs work only. It is not runtime validation, performance evidence, or a claim that a persistent dynamic shape field has been implemented.

## Files read / checked

Primary theory route:

```text
TheoryOfChange_main/01_Statements/02_Outer_Formation/001_S-DF-carried-constraint.md
TheoryOfChange_main/01_Statements/02_Outer_Formation/002A_S-DF-selective-residue.md
TheoryOfChange_main/01_Statements/02_Outer_Formation/003_S-DF-trace-retention.md
TheoryOfChange_main/01_Statements/02_Outer_Formation/004_S-DF-contrast-within-now.md
TheoryOfChange_main/01_Statements/02_Outer_Formation/005_S-DF-structural-prior-implication.md
TheoryOfChange_main/01_Statements/02_Outer_Formation/006_S-DF-reach-relation.md
TheoryOfChange_main/01_Statements/02_Outer_Formation/007_S-DF-localreach-zone.md
TheoryOfChange_main/01_Statements/02_Outer_Formation/008_S-DF-asymmetric-local-contribution.md
TheoryOfChange_main/01_Statements/02_Outer_Formation/012_S-DF-continuation-admissibility.md
TheoryOfChange_main/01_Statements/02_Outer_Formation/013_S-DF-local-comparability-field.md
TheoryOfChange_main/01_Statements/02_Outer_Formation/014_S-DF-remaining-transformation-burden.md
TheoryOfChange_main/01_Statements/02_Outer_Formation/020_S-DF-regime-signature.md
TheoryOfChange_main/01_Statements/02_Outer_Formation/021_S-DF-minimal-adequate-retention.md
TheoryOfChange_main/01_Statements/02_Outer_Formation/022_S-DF-thin-collapse-law.md
TheoryOfChange_main/01_Statements/02_Outer_Formation/022A_S-DR-shape-space-directed-unfolding-from-change.md
```

Concept/meta integration:

```text
TheoryOfChange_main/02_Concepts/C-dynamic-shape-coarseness-field.md
TheoryOfChange_main/02_Concepts/C-outer-formation-route.md
TheoryOfChange_main/02_Concepts/C-change-trace-invariants.md
TheoryOfChange_main/02_Concepts/C-change-space-metric.md
TheoryOfChange_main/00_Meta/FIRST_LAYER_CANONICAL_PATH.md
TheoryOfChange_main/00_Meta/CANONICAL_REFERENCE_STACK.md
TheoryOfChange_main/00_Meta/EXECUTION_REALIZATION_MAP.md
```

Kernel docs checked for shape/status alignment:

```text
ChangeOntCode/docs/kernel_spec/34_CANONICAL_PROBLEM_DEFINITION_AND_PLACEMENT_BASIS.md
ChangeOntCode/docs/kernel_spec/74_SIX_QUESTION_SHAPE_PRIOR.md
ChangeOntCode/docs/kernel_spec/100_SHAPE_PRIOR_FORMULA_AND_EVIDENCE_STATUS.md
ChangeOntCode/docs/kernel_spec/102_DOCS_CONSOLIDATION_AND_IMPLEMENTATION_AUDIT_GATE.md
```

## Audit result

The derivation is conceptually compatible with the active route, but the route needed two clarifications.

### 1. Earlier “local shape” usage was too easy to misread

`001` and `002A` use “local shape” before `022A` gives the full derived meaning. This is not fatal, because the early files only need a thin sense of present local differentiation that can matter for continuation. However, without an explicit note, a reader could accuse the route of using the full later shape concept before deriving it.

Fix made:

```text
001_S-DF-carried-constraint.md
002A_S-DF-selective-residue.md
```

now state that early “local shape” is thin/provisional and does not yet import CO-space, coarseness, metric structure, or dynamic shape update.

### 2. Earlier “coarse-grained” usage needed a non-import note

`005_S-DF-structural-prior-implication.md` uses “coarse-grained present articulation” before the coarseness-field doctrine is derived. This is acceptable only as descriptive shorthand for minimal resolution in the current argument.

Fix made:

```text
005_S-DF-structural-prior-implication.md
```

now states that the phrase does not import the later coarseness-field / point-as-ball account.

## Concept integration fixes

Updated:

```text
TheoryOfChange_main/02_Concepts/C-outer-formation-route.md
TheoryOfChange_main/02_Concepts/C-change-trace-invariants.md
TheoryOfChange_main/02_Concepts/C-change-space-metric.md
```

Effects:

```text
- fixed duplicate numbering in the outer formation route;
- added `022A` as the canonical shape/space consolidation point;
- clarified that metric-like change-space is downstream of CO-space, not primitive;
- marked persistent dynamic shape update as a future contract/implementation target.
```

## Current conceptual status after audit

Passes enough for Phase 2 contract work:

```text
shape-as-such = invariant fact that structured continuation has some local relational organization;
local shape-state = current relational-gauge/coarseness configuration;
CO-space = earned reach/comparability/admissibility/burden field;
directed unfolding = asymmetric contribution under retained trace, not full time;
tension = local shape asymmetry relative to continuation;
burden = retained continuation-relevant tension;
point = thin collapse of a local region under gauge;
dynamic shape update = lawful deformation from public retained trace, not hidden optimality.
```

Not yet implemented:

```text
persistent DynamicShapeField;
coarseness radius state;
projection horizon state;
shape-update memory across runtime cycles;
relation-density or delay-amplification update law.
```

## Remaining risks

1. The full 681-file theory tree was not line-by-line rederived. This audit covered the active first-layer route and canonical docs affected by the new derivation.
2. Older exploratory/clarification files may still use “space,” “shape,” “time,” or “point” loosely. They should not override the first-layer route.
3. The dynamic shape contract must remain non-evidence-bearing until implemented and tested.
4. If implemented badly, dynamic shape update can become a hidden solver or tuning patch.

## Phase gate verdict

Phase 1 — theory integration after the new derivation — is sufficiently clean to proceed to a Phase 2 dynamic-shape contract.

It is not a proof of full theory completion.
