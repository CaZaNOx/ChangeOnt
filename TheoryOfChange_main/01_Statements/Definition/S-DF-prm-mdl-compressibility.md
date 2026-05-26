---
id: stmt.prm-mdl-compressibility
type: DF
aliases:
- PRM_3.MDL
title: Candidate formalization — MDL / compressibility for selective-retention economy
concepts:
- '[[02_Concepts/C-math-structures]]'
- '[[02_Concepts/C-identity-change]]'
dependencies:
- '[[01_Statements/Definition/S-DF-self-propagating-selective-retention]]'
- '[[01_Statements/Derivation/S-DR-kernel-primitives-from-invariant-regimes]]'
- '[[01_Statements/02_Outer_Formation/011_S-DF-invariant-regime]]'
- '[[01_Statements/Definition/S-DF-structural-recurrence-likelihood]]'
parents:
- '[[01_Statements/Derivation/S-DR-kernel-primitives-from-invariant-regimes]]'
successors:
- '[[01_Statements/Definition/S-DF-prm-variable-birth]]'
- '[[01_Statements/Definition/S-DF-elm-ee-compressibility]]'
- '[[01_Statements/Definition/S-DF-elm-ef-router]]'
symbols_used:
- '[[01_Statements/SYMBOLS/Lambda]]'
sources:
- path: TheoryOfChange/02_Foundations/DerChain.md:2524
- path: TheoryOfChange/02_Foundations/DerChain.md:5468
flags:
- partial
- imported
tags:
- layer/formal
- domain/operational
- primitive
- mdl
- information
- partial
- imported
- type/DF
- concept/math-structures
- concept/identity-change
- symbol/Lambda
- core/peripheral-investigate
status: evolving
---
# Candidate formalization — MDL / compressibility for selective-retention economy
## Claim (formal)
Prefer recurring representations that compress without losing invariant-relevant structure: MDL gain = error_drop − λ·parameters. Use this as a disciplined economy criterion over candidate reorganizations.

## Philosophical Translation (of formal claim)
What lasts should not only fit; it should fit economically. If two ways of carrying structure work, prefer the one that preserves what matters with less wasted machinery.

## Philosophical Justification
[[S-DF-self-propagating-selective-retention]] gives the deeper ontological reason why some economy principle is needed at all: self-propagating change cannot carry the full prior unfolding explicitly and must therefore retain selectively under admissible loss. [[S-DR-kernel-primitives-from-invariant-regimes]] permits an economy criterion only after recurrence and invariance are already in place. MDL is therefore not itself the root ontological principle. It is one formal candidate for expressing selective-retention economy over recurring structure.

## Explanation (informal)
MDL is one of the weaker primitives in the subtree because it imports a formal selection discipline rather than arising as directly as bend, recurrence, or closure. It stays in the kernel because it provides a reusable, auditable way to reject gratuitous complexity. That role is real, but more provisional than the strongest chain-native primitives.

## Derivation (Philosophical)
- Recurrence produces reusable structure.
- Invariant regimes specify which aspects must be preserved.
- Once multiple candidate descriptions preserve the same relevant aspects, an economy criterion is allowed.
- MDL/compressibility is one such criterion: it favors shorter faithful descriptions over bloated ones.

## Derivation (Formal/Logical/Mathematical)
```text
MDL_gain = error_drop − λ · params_added
Accept change only if MDL_gain > 0 while declared invariants remain preserved.
```

## Clarifications / Further Context
- The deeper core issue is selective retention under admissible loss and recurrent stability.
- MDL is one candidate implementation of that issue, not the only possible one.
- Alternative formal candidates include quotient/closure stability, admissible lossy retention, and predictive sufficiency.
- λ must be declared; comparisons are invalid if they silently change the invariant regime being preserved.

## Next Steps in Chain
- suggest: [[S-DF-prm-variable-birth]]
- suggest: [[S-DF-elm-ee-compressibility]]
- suggest: [[S-DF-elm-ef-router]]

## Active-chain status
Band: imported-formal-aid.
Useful as an economy discipline over already-derived recurring structure, but not yet earned as one of the deepest kernel-resolution primitives.

## Tags
#type/DF #layer/formal #domain/operational #primitive #mdl #information #partial #imported #concept/math-structures #concept/identity-change #symbol/Lambda #status/evolving

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-elm-eb-ghvc]]
- [[01_Statements/Definition/S-DF-elm-ee-compressibility]]
- [[01_Statements/Definition/S-DF-prm-variable-birth]]
- [[01_Statements/Definition/S-DF-self-propagating-selective-retention]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-math-structures]]; [[02_Concepts/C-identity-change]]
- Parents: [[01_Statements/Derivation/S-DR-kernel-primitives-from-invariant-regimes]]
- Dependencies: [[01_Statements/Definition/S-DF-self-propagating-selective-retention]]; [[01_Statements/Derivation/S-DR-kernel-primitives-from-invariant-regimes]]; [[01_Statements/02_Outer_Formation/011_S-DF-invariant-regime]]; [[01_Statements/Definition/S-DF-structural-recurrence-likelihood]]
- Successors: [[01_Statements/Definition/S-DF-prm-variable-birth]]; [[01_Statements/Definition/S-DF-elm-ee-compressibility]]; [[01_Statements/Definition/S-DF-elm-ef-router]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

