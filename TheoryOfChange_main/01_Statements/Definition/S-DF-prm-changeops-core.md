---
id: stmt.prm-changeops-core
type: DF
aliases:
- PRM_10.ChangeOpsCore
title: Primitive — ChangeOps core (kernel-resolution subset of the relational operator family)
concepts:
- '[[02_Concepts/C-ontology-of-change]]'
dependencies:
- '[[01_Statements/Definition/S-DF-prm-change-ops]]'
- '[[01_Statements/Definition/S-DF-prm-closure-quotient]]'
- '[[01_Statements/Derivation/S-DR-kernel-primitives-from-invariant-regimes]]'
parents:
- '[[01_Statements/Definition/S-DF-prm-change-ops]]'
- '[[01_Statements/Definition/S-DF-prm-closure-quotient]]'
successors:
- '[[01_Statements/Definition/S-DF-elm-ei-change-operators]]'
- '[[01_Statements/Definition/S-DF-ops-j1-bend-substitution]]'
symbols_used: []
sources:
- path: TheoryOfChange/02_Foundations/DerChain.md:2624
- path: TheoryOfChange/02_Foundations/DerChain.md:5568
- path: chat/2026-03-24 clarification distinguishing broad operator family from kernel-usable subset
flags:
- partial
tags:
- layer/operators
- domain/operational
- primitive
- algebra
- library
- type/DF
- concept/ontology-of-change
status: evolving
chain_status_band: derived-but-weaker
chain_status_note: Better understood as the kernel-resolution reusable subset of ChangeOps, not as an independent second root primitive.
---
# Primitive — ChangeOps core (kernel-resolution subset of the relational operator family)
## Claim (formal)
ChangeOpsCore is the compact reusable subset of the broader ChangeOps family that the kernel can stably carry as a shared library across elements and J-operators.

## Philosophical Translation (of formal claim)
The family of possible relational change operations is broad; the kernel needs the disciplined subset that it can repeatedly reuse without turning every operation into a fresh invention.

## Philosophical Justification
[[S-DF-prm-change-ops]] licenses the broader relational family. [[S-DR-kernel-primitives-from-invariant-regimes]] then asks what must be repeatedly available at kernel resolution. ChangeOpsCore is that answer: not a second root, but the reusable subset needed for the actual kernel.

## Explanation (informal)
This is the compact library version of ChangeOps. It exists because the kernel needs stable, shared, law-like operations for motif manipulation. It does not replace the broader family; it packages the currently indispensable subset.

## Derivation (Philosophical)
- The broader operator family is too large to treat as one undifferentiated kernel primitive.
- Downstream elements repeatedly need a smaller stable subset.
- Therefore a kernel-resolution core is legitimate.

## Derivation (Formal/Logical/Mathematical)
```text
ChangeOpsCore ⊂ ChangeOpsFamily
such that ChangeOpsCore contains the operations repeatedly required by EI and J-operators under fixed quotient semantics.
```

## Clarifications / Further Context
- The family/core distinction is a level distinction, not intended duplication.
- The exact boundary of the core may still evolve as the kernel matures.

## Next Steps in Chain
- suggest: [[S-DF-elm-ei-change-operators]]
- suggest: [[S-DF-ops-j1-bend-substitution]]

## Active-chain status
Band: derived-but-weaker.
Useful and now conceptually cleaner, but still not maximally frozen.

## Tags
#type/DF #layer/operators #domain/operational #primitive #algebra #library #concept/ontology-of-change #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Clarification/S-CL-co-on-co-meta-operators]]
- [[01_Statements/Definition/S-DF-elm-ei-change-operators]]
- [[01_Statements/Definition/S-DF-j-criterion]]
- [[01_Statements/Definition/S-DF-ops-j1-bend-substitution]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-ontology-of-change]]
- Parents: [[01_Statements/Definition/S-DF-prm-change-ops]]; [[01_Statements/Definition/S-DF-prm-closure-quotient]]
- Dependencies: [[01_Statements/Definition/S-DF-prm-change-ops]]; [[01_Statements/Definition/S-DF-prm-closure-quotient]]; [[01_Statements/Derivation/S-DR-kernel-primitives-from-invariant-regimes]]
- Successors: [[01_Statements/Definition/S-DF-elm-ei-change-operators]]; [[01_Statements/Definition/S-DF-ops-j1-bend-substitution]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

