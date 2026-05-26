# Canonical Reference Stack

This file is the active reader handoff for the clean ChangeOnt kernel documentation set. It lists the canonical chain only. If another file conflicts with this chain, the other file must be corrected before implementation-audit work proceeds.

## Minimal active reading stack

Read in this order for the current kernel target state:

```text
1. TheoryOfChange_main/00_Meta/FIRST_LAYER_CANONICAL_PATH.md
2. TheoryOfChange_main/00_Meta/TARGET_KERNEL_ARCHITECTURE_DOCTRINE.md
3. ChangeOntCode/docs/kernel_spec/00A_DOCS_READING_GUIDE.md
4. ChangeOntCode/docs/kernel_spec/01B_TARGET_ARCHITECTURE_CONTRACT.md
5. ChangeOntCode/docs/kernel_spec/17_COMPONENT_CLASSIFICATION.md
6. ChangeOntCode/docs/kernel_spec/96_CONCEPTUAL_CLOSURE_LEDGER.md
7. ChangeOntCode/docs/kernel_spec/95_KERNEL_STRUCTURE_CARRIER_ALIGNMENT.md
8. ChangeOntCode/docs/kernel_spec/102_DOCS_CONSOLIDATION_AND_IMPLEMENTATION_AUDIT_GATE.md
9. ChangeOntCode/docs/kernel_spec/03C_IMPLEMENTATION_FIDELITY_STATUS.md
10. ChangeOntCode/docs/kernel_spec/00_INDEX.md
```

## Reading-order rule

`00_INDEX.md` is the kernel-doc catalog. It is useful after the stack above is understood, but it does not override this file's reading order.

## Active execution loop

```text
0. Problem state / observation
1. Boundary / Adapter
2. Candidate Surface
3. Continuation Identity Construction
4. Burden Interpretation
5. Burden Operation Typing
6. Relation Surface
7. Recursive Continuation Field
8. Collapse Certificate
9. Commitment Surface / Readout
10. Environment update / next loop
```

## Layer rule

```text
_main: defines what the project is allowed to mean.
docs: define what code is allowed to do.
code: shows what currently happens.
tests/runs: show whether code matches the docs and whether behavior is interpretable.
```

Do not collapse those layers. Performance results are interpretable only after boundary, relation, certificate, formula, and fail-closed audits pass.

## Concept-specific canonical docs

```text
Boundary / public facts:
  ChangeOntCode/docs/kernel_spec/16_TRANSLATOR_BOUNDARY_CONTRACT.md
  ChangeOntCode/docs/kernel_spec/77_PUBLIC_BURDEN_EFFECT_SCHEMA.md
  ChangeOntCode/docs/kernel_spec/78_RUNTIME_SAFETY_AND_FALLBACK_CONTRACT.md

Shape / regime:
  ChangeOntCode/docs/kernel_spec/34_CANONICAL_PROBLEM_DEFINITION_AND_PLACEMENT_BASIS.md
  ChangeOntCode/docs/kernel_spec/74_SIX_QUESTION_SHAPE_PRIOR.md
  ChangeOntCode/docs/kernel_spec/100_SHAPE_PRIOR_FORMULA_AND_EVIDENCE_STATUS.md

Kernel loop:
  ChangeOntCode/docs/kernel_spec/44_CANONICAL_CANDIDATE_SURFACE.md
  ChangeOntCode/docs/kernel_spec/76_CONTINUATION_IDENTITY_AND_RELATION_PUBLICATION_CONTRACT.md
  ChangeOntCode/docs/kernel_spec/84_BURDEN_OPERATION_ALGEBRA.md
  ChangeOntCode/docs/kernel_spec/80_KERNEL_SIDE_RELATION_SURFACE_CONTRACT.md
  ChangeOntCode/docs/kernel_spec/47_RECURSIVE_CONTINUATION_FIELD.md
  ChangeOntCode/docs/kernel_spec/91_EARNED_COLLAPSE_CERTIFICATE_IMPLEMENTATION.md
  ChangeOntCode/docs/kernel_spec/43_CANONICAL_COMMITMENT_RULE.md

Open target-state boundaries:
  ChangeOntCode/docs/kernel_spec/97_QUOTIENT_EQUIVALENCE_TARGET_STATE.md
  ChangeOntCode/docs/kernel_spec/98_RECURSION_DEMAND_TARGET_STATE.md
  ChangeOntCode/docs/kernel_spec/99_RELATION_ALGEBRA_TARGET_STATE.md
  ChangeOntCode/docs/kernel_spec/101_RCF_ALGORITHM_COMPARISON_AND_CONSCIOUSNESS_SCOPE.md
```

## Claim boundary

The current docs specify a coherent implementation target. They do not claim:

```text
full proof of the six-question prior;
final coefficient derivations;
complete CO mathematics;
benchmark success;
consciousness theory beyond continuation-relevance motivation.
```
