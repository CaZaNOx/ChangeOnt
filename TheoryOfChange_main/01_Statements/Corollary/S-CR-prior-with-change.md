---
id: stmt.prior-with-change
type: CR
aliases: ["FND_4.PriorWithChange"]
title: Prior-with-Change — recursive prior induced by Reach and Locality
concepts: ["[[02_Concepts/C-prior-pointer-reach]]"]
dependencies: [
  "[[01_Statements/Definition/S-DF-pointer-structural]]",
  "[[01_Statements/Definition/S-DF-reach-relation]]",
  "[[01_Statements/Definition/S-DF-locality-prior]]",
  "[[01_Statements/Definition/S-DF-path-eventlet-chain]]",
  "[[01_Statements/FoundationalTruth/S-FT-continuity-noncessation]]"
]
parents: ["[[01_Statements/FoundationalTruth/S-FT-immediate-datum]]", "[[01_Statements/FoundationalTruth/S-FT-continuity-noncessation]]"]
successors: ["[[01_Statements/Clarification/S-CL-perception-as-error-correction]]"]
symbols_used: []
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:352
  - path: TheoryOfChange/02_Foundations/DerChain.md:3296
flags: []
tags: [layer/foundations, domain/logical, recursive, stable, "type/CR", "concept/prior-pointer-reach"]
---
# Prior-with-Change — recursive prior induced by Reach and Locality
## Statement (corollary)
Given Δ(Now), Reach, and Locality, the “prior” is not a static parameter but a recursively updated trace over LocalReach neighborhoods, maintained by pointers and path structure. Hence, prior belief/state evolves with the ongoing change it summarizes.

## Philosophical Translation
What you already “have” is not fixed; the very act of continuing updates what counts as your prior.

## Philosophical Justification
- Pointers + Reach encode admissible elsewhere; LocalReach bounds feasible updates.
- Continuity/non‑cessation ([[S-FT-continuity-noncessation]]) forces priors to be maintained across breaths.
- Path composition ([[S-DF-path-eventlet-chain]]) updates priors as new eventlets append; a static prior would contradict the ongoing Δ it is meant to summarize.

## Explanation (informal)
You never step into the same prior twice. As you move, the summary of “what’s already known” shifts because the reach graph and validation traces shift.

## Derivation (Philosophical)
- Start with Δ → pointer → reach.
- Add locality and path composition → rolling window of admissible states.
- Therefore prior = function(LocalReach, path-history), not constant parameter.

## Derivation (Formal/Logical/Mathematical)
```text
Prior_{t+1} := Update(Prior_t, Path(Eventlets_t), LocalReach_t)
```

## Proofs/Corollaries References
- corollary: informs [[S-CL-perception-as-error-correction]] (priors updated via errors).

## Clarifications / Links to definitions
- From [[01_Statements/Definition/S-DF-pointer-structural]] and [[01_Statements/Definition/S-DF-reach-relation]]: pointers and reach encode how the present is stitched from admissible steps.
- From [[01_Statements/Definition/S-DF-locality-prior]]: only locally reachable configurations inform the prior.
- From [[01_Statements/Definition/S-DF-path-eventlet-chain]]: priors compose along eventlet chains.

## Next Steps in Chain
- suggest: [[S-CL-perception-as-error-correction]]

## Tags
#type/CR #layer/foundations #domain/logical #concept/prior-pointer-reach #recursive #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-path-eventlet-chain]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-prior-pointer-reach]]
- Parents: [[01_Statements/FoundationalTruth/S-FT-immediate-datum]]; [[01_Statements/FoundationalTruth/S-FT-continuity-noncessation]]
- Dependencies: [[01_Statements/Definition/S-DF-pointer-structural]]; [[01_Statements/Definition/S-DF-reach-relation]]; [[01_Statements/Definition/S-DF-locality-prior]]; [[01_Statements/Definition/S-DF-path-eventlet-chain]]; [[01_Statements/FoundationalTruth/S-FT-continuity-noncessation]]
- Successors: [[01_Statements/Clarification/S-CL-perception-as-error-correction]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

