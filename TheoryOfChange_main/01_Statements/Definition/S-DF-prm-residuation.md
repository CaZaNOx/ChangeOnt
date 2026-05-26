---
id: stmt.prm-residuation
type: DF
aliases:
- PRM_11.Residuation
title: Candidate formalization — residuation for remaining transformation burden
concepts:
- '[[02_Concepts/C-math-structures]]'
dependencies:
- '[[01_Statements/02_Outer_Formation/014_S-DF-remaining-transformation-burden]]'
- '[[01_Statements/Definition/S-DF-quantale-logic]]'
- '[[01_Statements/Definition/S-DF-hdr-algebra-mode]]'
- '[[01_Statements/Derivation/S-DR-kernel-primitives-from-invariant-regimes]]'
parents:
- '[[01_Statements/Definition/S-DF-quantale-logic]]'
successors:
- '[[01_Statements/Derivation/S-DR-quantale-residuation-implication]]'
symbols_used: []
sources:
- path: TheoryOfChange/02_Foundations/DerChain.md:5580
flags:
- partial
- imported
tags:
- layer/foundations
- domain/formal
- primitive
- logic
- implication
- partial
- imported
- type/DF
- concept/math-structures
- core/peripheral-investigate
status: evolving
---
# Candidate formalization — residuation for remaining transformation burden
## Claim (formal)
In a residuated quantale (L, ≤, ⊕, ⊗), define residual a ⇒ b as the greatest x with a ⊗ x ≤ b. This interprets implication as the extra effort needed to reach b after a.

## Philosophical Translation (of formal claim)
Implication is not merely truth-preservation. In CO-sensitive algebra it can be read as what still has to be done to continue from one change-configuration into another.

## Philosophical Justification
[[S-DF-remaining-transformation-burden]] names the deeper ontological need: once change composes, one must sometimes say what still has to happen for one local configuration to reach another admissible one. [[S-DF-hdr-algebra-mode]] and [[S-DF-quantale-logic]] then permit one formal articulation of that need. Residuation is therefore not the deepest root of the issue. It is one strong candidate formalization of remaining transformation burden or admissibility deficit under a suitable algebra.

## Explanation (informal)
Residuation sits at the edge of the subtree: useful, conceptually aligned, but more imported and formal than bend, recurrence, or closure. It should therefore remain explicitly marked as a weaker, later primitive rather than silently equalized with the strongest roots.

## Derivation (Philosophical)
- If the kernel uses semiring/quantale-like composition, implication should be recast in that native algebra rather than borrowed uncritically from Boolean logic.
- Residuation provides exactly that move: a way of expressing the missing continuation required to reach a target under the chosen composition law.
- It is therefore a disciplined formal descendant of the algebra branch, not a first ontological necessity.

## Derivation (Formal/Logical/Mathematical)
```text
a ⊗ x ≤ b  iff  x ≤ a ⇒ b
```
Read operationally: x is the greatest remaining effort compatible with reaching b after a.

## Clarifications / Further Context
- The deeper core issue is remaining transformation / reachability / admissibility burden.
- Residuation is one strong candidate formalization of that issue, especially once non-classical composition is in play.
- Alternative formal directions include cost-to-go, reachability deficit, or constraint/admissibility deficit formulations.
- Keep this node explicitly secondary to the deeper ontological need it articulates.

## Next Steps in Chain
- suggest: [[S-DR-quantale-residuation-implication]]

## Active-chain status
Band: imported-formal-aid.
Strong formal candidate for non-classical implication, but not yet uniquely forced by the ontological chain.

## Tags
#type/DF #layer/foundations #domain/formal #primitive #logic #implication #partial #imported #concept/math-structures #status/evolving

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/02_Outer_Formation/014_S-DF-remaining-transformation-burden]]
- [[01_Statements/Derivation/S-DR-quantale-residuation-implication]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-math-structures]]
- Parents: [[01_Statements/Definition/S-DF-quantale-logic]]
- Dependencies: [[01_Statements/02_Outer_Formation/014_S-DF-remaining-transformation-burden]]; [[01_Statements/Definition/S-DF-quantale-logic]]; [[01_Statements/Definition/S-DF-hdr-algebra-mode]]; [[01_Statements/Derivation/S-DR-kernel-primitives-from-invariant-regimes]]
- Successors: [[01_Statements/Derivation/S-DR-quantale-residuation-implication]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

