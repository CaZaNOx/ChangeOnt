# Docs Reading Guide — Canonical Clean Set

Read the active kernel docs in this order after the top-level repo onboarding route has reached `TheoryOfChange_main/00_Meta/CANONICAL_REFERENCE_STACK.md`. This guide is the kernel-doc reading order, not a separate theory entrypoint.

## 1. Architecture target

Use the same order as `TheoryOfChange_main/00_Meta/CANONICAL_REFERENCE_STACK.md` and `102_DOCS_CONSOLIDATION_AND_IMPLEMENTATION_AUDIT_GATE.md`:

- `01B_TARGET_ARCHITECTURE_CONTRACT.md`
- `17_COMPONENT_CLASSIFICATION.md`
- `96_CONCEPTUAL_CLOSURE_LEDGER.md`
- `95_KERNEL_STRUCTURE_CARRIER_ALIGNMENT.md`
- `102_DOCS_CONSOLIDATION_AND_IMPLEMENTATION_AUDIT_GATE.md`
- `03C_IMPLEMENTATION_FIDELITY_STATUS.md`

## 2. Boundary and input discipline

- `16_TRANSLATOR_BOUNDARY_CONTRACT.md`
- `77_PUBLIC_BURDEN_EFFECT_SCHEMA.md`
- `08_TRANSLATORS/README.md`
- `78_RUNTIME_SAFETY_AND_FALLBACK_CONTRACT.md`

## 3. Kernel execution loop

- `03_WIRING_MAP.md`
- `44_CANONICAL_CANDIDATE_SURFACE.md`
- `76_CONTINUATION_IDENTITY_AND_RELATION_PUBLICATION_CONTRACT.md`
- `84_BURDEN_OPERATION_ALGEBRA.md`
- `80_KERNEL_SIDE_RELATION_SURFACE_CONTRACT.md`
- `95_KERNEL_STRUCTURE_CARRIER_ALIGNMENT.md`
- `47_RECURSIVE_CONTINUATION_FIELD.md`
- `91_EARNED_COLLAPSE_CERTIFICATE_IMPLEMENTATION.md`
- `43_CANONICAL_COMMITMENT_RULE.md`
- `103_DYNAMIC_SHAPE_FIELD_CONTRACT.md`
- `104_DYNAMIC_SHAPE_UPDATE_MICROCASE_EXPECTATIONS.md`

## 4. Implemented first-pass dynamic shape and open target-state boundaries

- `103_DYNAMIC_SHAPE_FIELD_CONTRACT.md`
- `104_DYNAMIC_SHAPE_UPDATE_MICROCASE_EXPECTATIONS.md`
- runtime carrier: `ChangeOntCode/agents/co/runtime/surfaces/dynamic_shape_field.py`

Then continue with target-state boundaries:

- `97_QUOTIENT_EQUIVALENCE_TARGET_STATE.md`
- `98_RECURSION_DEMAND_TARGET_STATE.md`
- `99_RELATION_ALGEBRA_TARGET_STATE.md`
- `100_SHAPE_PRIOR_FORMULA_AND_EVIDENCE_STATUS.md`
- `101_RCF_ALGORITHM_COMPARISON_AND_CONSCIOUSNESS_SCOPE.md`

## 5. Validation and implementation audit

- `79_CANDIDATE_AND_COMMITMENT_FORMULA_GROUNDING_PROTOCOL.md`
- `88_ADAPTER_PUBLIC_EFFECT_RELATION_COVERAGE.md`
- `89_RELATION_PATH_TRACE_VALIDATION.md`
- `92_ARCHITECTURE_ACCEPTANCE_AUDITS.md`
- `94_REAL_TRACE_STRUCTURAL_VALIDATION_AND_FORMULA_GROUNDING.md`

## Non-negotiable target

The active runtime path is Boundary / Adapter → CandidateSurface → Continuation Identity → Burden Operations → RelationSurface → RecursiveContinuationField → CollapseCertificate → DynamicShapeField update/next-cycle gauge → CommitmentSurface. Evidence-bearing runs must preserve this loop and fail closed when required structure is absent.


## Relation-field collapse update

Read `106_RELATION_FIELD_FUNCTION_LIKE_COLLAPSE.md` after RelationSurface and DynamicShapeField. It defines the bounded telemetry by which function-like behavior is treated as a shape-conditioned collapse of public relation-field concentration, not as a primitive point-function assumption.

- `107_DOMAIN_RELATIVE_COARSENESS_FIELD.md` — domain-relative coarseness field: global fallback plus bounded public-domain coarseness profile.
