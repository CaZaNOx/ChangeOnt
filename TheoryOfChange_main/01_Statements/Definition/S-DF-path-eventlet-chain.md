---
id: stmt.path-eventlet-chain
type: DF
aliases: ["FND_8.Path"]
title: Path — recursive chain of eventlets
concepts: ["[[02_Concepts/C-prior-pointer-reach]]"]
dependencies: ["[[01_Statements/Definition/S-DF-eventlet]]", "[[01_Statements/Definition/S-DF-reach-relation]]"]
parents: ["[[01_Statements/Definition/S-DF-eventlet]]"]
successors: ["[[01_Statements/Definition/S-DF-locality-prior]]", "[[01_Statements/Corollary/S-CR-prior-with-change]]"]
symbols_used: []
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:692
flags: []
tags: [layer/foundations, domain/logical, stable, "type/DF", "concept/prior-pointer-reach"]
---
# Path — recursive chain of eventlets
## Claim (formal)
Paths are composable sequences of eventlets within LocalReach; depth computes via minimal path length.

## Philosophical Translation (of formal claim)
Continuous change is tracked as a string of smallest-noticeable steps. Stitching those steps yields a path; its length is how many discriminable moves it takes to get from here to there.

## Philosophical Justification
- [[S-DF-eventlet]] gives the generators; [[S-DF-reach-relation]] constrains which generators can follow which.
- Counting eventlets respects the current ε; path depth measures effort/complexity under that discrimination level.
- Paths allow defining priors and locality updates as cumulative traces rather than one-shot jumps.

## Explanation (informal)
Think of a path as a breadcrumb trail of eventlets. Each link is admissible per Reach; the chain encodes both where you can go and what it costs (depth).

## Derivation (Philosophical)
- Eventlet e_i ∈ LocalReach; Reach(e_i, e_{i+1}) must hold.
- Depth(path) := min length of such chains connecting endpoints.

## Derivation (Formal/Logical/Mathematical)
```text
Path(x,y) := {⟨e_1,...,e_n⟩ | e_1=x, e_n=y, ∀i Reach(e_i, e_{i+1}) }.
depth(x,y) := min n over Path(x,y).
```

## Proofs/Corollaries References
- corollary: supports [[S-CR-prior-with-change]] by composing priors along eventlet chains.

## Clarifications / Further Context
- Depth is relative to ε; refining ε can increase depth counts.
- Non-uniqueness: multiple minimal paths may exist; tie-breaking depends on evaluation surfaces later.

## Next Steps in Chain
- suggest: [[S-DF-locality-prior]]
- suggest: [[S-CR-prior-with-change]]

## Tags
#type/DF #layer/foundations #domain/logical #concept/prior-pointer-reach #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-eventlet]]
- [[01_Statements/Definition/S-DF-prm-change-ops]]
- [[01_Statements/Definition/S-DF-reach-relation]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-prior-pointer-reach]]
- Parents: [[01_Statements/Definition/S-DF-eventlet]]
- Dependencies: [[01_Statements/Definition/S-DF-eventlet]]; [[01_Statements/Definition/S-DF-reach-relation]]
- Successors: [[01_Statements/Definition/S-DF-locality-prior]]; [[01_Statements/Corollary/S-CR-prior-with-change]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

