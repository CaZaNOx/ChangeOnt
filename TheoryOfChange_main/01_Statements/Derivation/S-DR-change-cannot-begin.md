---
id: stmt.change-cannot-begin
type: DR
aliases: ["FND 1.0"]
title: Change cannot have a beginning
concepts: ["[[02_Concepts/C-ontology-of-change]]"]
dependencies: ["[[01_Statements/FoundationalTruth/S-FT-immediate-datum]]"]
parents: ["[[01_Statements/FoundationalTruth/S-FT-immediate-datum]]"]
successors: ["[[01_Statements/FoundationalTruth/S-FT-continuity-noncessation]]"]
symbols_used: ["[[01_Statements/SYMBOLS/Delta]]"]
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:60
  - path: TheoryOfChange/02_Foundations/FND_1_ChangeCannotBegin.md:1
flags: []
tags: [foundations, logical, stable, "type/DR", "concept/ontology-of-change", "symbol/Delta"]
---
# Change cannot have a beginning
## Claim (formal)
Assume a first moment of change: (¬Δ → Δ) at t₀. The transition is already Δ; contradiction. Therefore no first change.

## Philosophical Translation (of formal claim)
If you claim there was a “first change,” you already presume change; so change cannot have a first moment. The very notion of “beginning” presupposes a difference between before and after. That difference is precisely what “change” names; the attempt to locate an absolute first instance therefore defeats itself.

## Philosophical Justification
To posit change “starting” invokes a transition from no‑change to change, which is itself a change. The notion of a first change defeats itself. One might try to appeal to time as a primitive, but temporal talk already encodes ordered difference. This result does not trivialize cosmologies (e.g., the Big Bang): it reframes them as transformations within ongoing change rather than creation ex nihilo. Change, as ontic condition, is the canvas on which such events are drawn.

## Explanation (informal)
“Beginning” is a local description within ongoing change, not an ontological boundary.

## Derivation (Philosophical)
- Any claimed “first moment” must itself be a change from a prior non‑change, which entails change.

## Derivation (Formal/Logical/Mathematical)
```math
\exists\, t_0: (\forall t < t_0, \lnot \Delta(t)) \wedge \Delta(t_0) \Rightarrow (\lnot \Delta \to \Delta) \equiv \Delta \Rightarrow \bot
```

## Proofs/Corollaries References
- corollary: [[S-FT-continuity-noncessation]]

## Clarifications / Further Context
- This does not forbid local rest; it rejects an absolute boundary from no‑change to change.
- See symbol: [[01_Statements/SYMBOLS/Delta]]

## Next Steps in Chain
- suggest: [[S-FT-continuity-noncessation]]

## Symbols
- [[01_Statements/SYMBOLS/Delta]]

## Tags
#type/DR #layer/foundations #domain/logical #concept/ontology-of-change #symbol/Delta #status/stable





































































































































<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-ontology-of-change]]
- Parents: [[01_Statements/FoundationalTruth/S-FT-immediate-datum]]
- Dependencies: [[01_Statements/FoundationalTruth/S-FT-immediate-datum]]
- Successors: [[01_Statements/FoundationalTruth/S-FT-continuity-noncessation]]
<!-- END:AUTOGEN:RELATIONSHIPS -->










































































































































































































<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Clarification/S-CL-change-not-mere-flux]]
- [[01_Statements/FoundationalTruth/S-FT-continuity-noncessation]]
- [[01_Statements/FoundationalTruth/S-FT-immediate-datum]]
<!-- END:AUTOGEN:REFERENCED_BY -->




































































































