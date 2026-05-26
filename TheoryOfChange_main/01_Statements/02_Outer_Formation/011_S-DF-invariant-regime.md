---
id: stmt.invariant-regime
type: DF
aliases:
  - S-DF-invariant-regime
  - CO.Root.InvariantRegime
title: Invariant regime — stable profile of preservation, tolerance, and failure under selective recurrence
concepts:
  - '[[02_Concepts/C-change-trace-invariants]]'
  - '[[02_Concepts/C-outer-formation-route]]'
dependencies:
  - '[[01_Statements/02_Outer_Formation/010_S-DF-selective-recurrence.md]]'
parents:
  - '[[01_Statements/02_Outer_Formation/010_S-DF-selective-recurrence.md]]'
successors:
  - '[[01_Statements/02_Outer_Formation/027_S-DF-identity-invariants]]'
  - '[[01_Statements/Derivation/S-DR-categories-from-invariant-regimes]]'
  - '[[01_Statements/Derivation/S-DR-kernel-primitives-from-invariant-regimes]]'
symbols_used:
  - '[[01_Statements/SYMBOLS/Identity]]'
  - '[[01_Statements/SYMBOLS/Approx]]'
sources:
  - path: TheoryOfChange/01_CoreOntology/COT_5_Self_Similarity_and_the_Emergence_of_Identity.md:80
  - path: chat/2026-03-23 discussion on invariant types and closure profiles
flags: []
tags:
  - layer/foundations
  - domain/ontological
  - invariants
  - type/DF
  - concept/change-trace-invariants
  - route/outer
  - status/stable
status: stable
chain_status_band: strongly-derived
chain_status_note: Invariant regime is derived from selective recurrence and bounded filtering, not from a prior object ontology.
---
# Invariant regime — stable profile of preservation, tolerance, and failure under selective recurrence

## Claim (formal)
An invariant regime is the stable profile of what a selectively recurrent unfolding preserves, tolerates, repairs, and loses across repeated re-entry.

## Philosophical Translation (of formal claim)
When recurrence becomes stable enough, it is no longer enough to say merely that "something comes back." One can now say more precisely:
- these aspects tend to survive,
- these alterations can be absorbed,
- these deviations can be repaired,
- and these changes break the recurrence.

That patterned profile is an invariant regime.

## Why this claim is needed
Without invariant regime, recurrence remains too thin for later work. The theory would know that something re-enters, but not what the recurrence can survive or what destroys it. Later files need exactly this profile in order to discuss:
- admissibility,
- burden,
- identity,
- and operative invariants.

## Philosophical Justification
Selective recurrence already says not everything is carried equally through re-entry. Once recurrence is repeatable enough, this unequal carrying ceases to be a one-off accident and becomes a stable profile. The unfolding then has a characteristic way of handling perturbation: some changes are absorbed, some corrected, some fatal. That stable profile is more than recurrence but less than full object identity. It is the correct intermediate node.

## Explanation (informal)
This file should be read as the first genuine stabilization of a change-process into a rule-like profile. It does not yet say that a thing exists in the everyday sense. It says only that the recurrent unfolding now exhibits a stable pattern of preserved and non-preserved change.

## Derivation (Philosophical)
- Selective recurrence means some aspects repeatedly re-enter while others do not.
- If this selectivity stabilizes over repeated re-entry, then the unfolding has a repeatable preservation profile.
- A repeatable preservation profile determines:
  - what is preserved,
  - what is tolerated,
  - what is repaired,
  - what destroys continuity.
- Therefore selective recurrence yields invariant regime.

## Derivation (Formal/Logical/Mathematical)
```text
Given a selectively recurrent unfolding R,
InvariantRegime(R) =
  {preserved aspects, tolerated deviations, repairable deviations, failure conditions}
that remain stable across repeated re-entry of R.
```

## Clarifications / Further Context
- This is not yet object identity.
- It is not yet full law in the strongest sense.
- It is a change-native profile of persistence under transformation.
- Later identity claims will depend on such regimes rather than justify them.

## Objection 1: “Why isn’t recurrence by itself enough?”
Because recurrence alone does not yet tell us what kinds of transformation preserve the recurrence and what kinds break it. Invariant regime names that stronger, stabilized profile.

## Objection 2: “Does this already assume a thing with properties?”
No. The regime belongs first to the recurrent unfolding itself. Only later may some such regimes support thing-like identity claims.

## What this file establishes
This file establishes:
1. recurrence can stabilize into a preservation profile,
2. that profile includes survival, tolerance, repair, and breakdown,
3. this profile is the correct precursor to later admissibility and identity machinery.

## What this file does not yet establish
It does **not** yet establish:
- objecthood,
- identity in the full sense,
- or complete metric/formal packaging.

## Next Steps in Chain
- suggest: [[01_Statements/02_Outer_Formation/012_S-DF-continuation-admissibility.md]]
- suggest: [[01_Statements/02_Outer_Formation/024_S-DF-identity-admissibility.md]]
- suggest: [[01_Statements/02_Outer_Formation/027_S-DF-identity-invariants]]

## Tags
#type/DF #layer/foundations #domain/ontological #route/outer #concept/change-trace-invariants #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/02_Outer_Formation/010_S-DF-selective-recurrence]]
- [[01_Statements/02_Outer_Formation/012_S-DF-continuation-admissibility]]
- [[01_Statements/02_Outer_Formation/027_S-DF-identity-invariants]]
- [[01_Statements/Definition/S-DF-embedded-stabilized-layers]]
- [[01_Statements/Derivation/S-DR-categories-from-invariant-regimes]]
- [[01_Statements/Derivation/S-DR-kernel-primitives-from-invariant-regimes]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-change-trace-invariants]]; [[02_Concepts/C-outer-formation-route]]
- Parents: [[01_Statements/02_Outer_Formation/010_S-DF-selective-recurrence.md]]
- Dependencies: [[01_Statements/02_Outer_Formation/010_S-DF-selective-recurrence.md]]
- Successors: [[01_Statements/02_Outer_Formation/027_S-DF-identity-invariants]]; [[01_Statements/Derivation/S-DR-categories-from-invariant-regimes]]; [[01_Statements/Derivation/S-DR-kernel-primitives-from-invariant-regimes]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

