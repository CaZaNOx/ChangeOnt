---
id: stmt.minimal-adequate-retention
type: DF
aliases:
- S-DF-minimal-adequate-retention
- S-DF-minimal-adequate-representation
- MinimalAdequateRetention
- RegimeAdequateRetention
title: Minimal adequate retention — the least retained structure sufficient for operative continuation
concepts:
- '[[02_Concepts/C-change-trace-invariants]]'
dependencies:
- '[[01_Statements/02_Outer_Formation/020_S-DF-regime-signature]]'
- '[[01_Statements/02_Outer_Formation/010_S-DF-selective-recurrence.md]]'
- '[[01_Statements/02_Outer_Formation/014_S-DF-remaining-transformation-burden]]'
parents:
- '[[01_Statements/02_Outer_Formation/020_S-DF-regime-signature]]'
- '[[01_Statements/02_Outer_Formation/010_S-DF-selective-recurrence.md]]'
successors:
- '[[01_Statements/02_Outer_Formation/022_S-DF-thin-collapse-law]]'
symbols_used: []
sources:
- path: chat/2026-04-02 clarification that bounded local structure should retain only
    the least structure sufficient to preserve operative continuation in the current
    regime, replacing premature MDL elevation
flags: []
tags:
- layer/foundations
- domain/ontological
- type/DF
- status/stable
- strand/ontological
- route/outer
chain_status_band: strongly-derived
chain_status_note: States the deeper retention discipline without canonizing MDL or
  another compression formalism too early.
---
# Minimal adequate retention — the least retained structure sufficient for operative continuation
## Claim (formal)
For any bounded local unfolding, the retained structure should be no richer than required to preserve operative invariants and supportable continuation in the current regime.

## Philosophical Translation (of formal claim)
A local hold should keep enough to continue well, but no more than the regime actually needs. Richness is earned by burden, admissibility risk, and history-sensitivity, not by a blanket preference for maximal detail or maximal compression.

## Philosophical Justification
[[S-DF-selective-recurrence]] already shows that retention is selective rather than total. [[S-DF-regime-signature]] clarifies what the current regime actually requires. [[S-DF-remaining-transformation-burden]] adds that retention must remain answerable to what still needs transformation. Therefore the question is not “compress as much as possible” in the abstract. It is: what is the least retained structure sufficient to preserve operative continuation here and now?

## Explanation (informal)
Some regimes need rich path-sensitive retention because history, burden, and openness still matter. Other regimes can be held by a thinner summary because the operative structure has stabilized sharply. Minimal adequate retention names that regime-sensitive discipline.

## Derivation (Philosophical)
- Retention is selective rather than total.
- What is retained must answer to the current regime signature.
- Regime signature specifies which invariants matter, how burden is accumulating, and how much history still matters.
- Therefore the adequate retained structure is the least one that still preserves operative continuation under that signature.

## Derivation (Formal/Logical/Mathematical)
```text
For regime signature Sigma_R(x), let Ret(x) be the retained local structure.

Ret(x) is minimally adequate iff:
(1) operative invariants I*_R(x) remain recoverable within tolerance,
(2) supportable continuation A_R(x) remains sufficiently preserved,
(3) additional retained structure can be dropped without changing (1) or (2).
```

## Proofs/Corollaries References
- corollary: [[01_Statements/02_Outer_Formation/022_S-DF-thin-collapse-law]]

## Clarifications / Further Context
- This is the deeper ontological need behind later representation/compression policy.
- MDL may become one candidate downstream formalization in some contexts, but it is not prior to this doctrine.
- Adequacy is regime-relative and continuation-relative, not merely byte-minimizing.
- This file is about what must be retained, not yet about any specific codec, model family, or runtime implementation.

## Counterfactuals (refs)
- If retention were always maximally rich, the chain would lose economy and collapse discipline.
- If retention were always maximally thin, it would erase history and burden exactly where they remain operative.

## Next Steps in Chain
- suggest: [[01_Statements/02_Outer_Formation/022_S-DF-thin-collapse-law]]

## Active-chain status
**Band:** strongly-derived

**Why this status:** Once selective retention and regime signature are in place, the chain needs a principled rule for how much structure may be retained.

## Tags
#type/DF #layer/foundations #domain/ontological #status/stable #status-band/strongly-derived

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/02_Outer_Formation/020_S-DF-regime-signature]]
- [[01_Statements/02_Outer_Formation/022_S-DF-thin-collapse-law]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-change-trace-invariants]]
- Parents: [[01_Statements/02_Outer_Formation/020_S-DF-regime-signature]]; [[01_Statements/02_Outer_Formation/010_S-DF-selective-recurrence.md]]
- Dependencies: [[01_Statements/02_Outer_Formation/020_S-DF-regime-signature]]; [[01_Statements/02_Outer_Formation/010_S-DF-selective-recurrence.md]]; [[01_Statements/02_Outer_Formation/014_S-DF-remaining-transformation-burden]]
- Successors: [[01_Statements/02_Outer_Formation/022_S-DF-thin-collapse-law]]
<!-- END:AUTOGEN:RELATIONSHIPS -->
