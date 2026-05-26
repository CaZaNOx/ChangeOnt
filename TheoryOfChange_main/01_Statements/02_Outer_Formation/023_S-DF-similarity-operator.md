---
id: stmt.similarity-operator
type: DF
aliases:
- COT_5.Sim
- S-DF-similarity-operator
title: Similarity operator — graded retained-versus-altered comparison inside the identity branch
concepts:
- '[[02_Concepts/C-identity-change]]'
dependencies:
- '[[01_Statements/02_Outer_Formation/016_S-DF-identity-through-change]]'
- '[[01_Statements/02_Outer_Formation/016A_S-DF-bounded-continuation-profile.md]]'
- '[[01_Statements/02_Outer_Formation/013_S-DF-local-comparability-field.md]]'
parents:
- '[[01_Statements/02_Outer_Formation/016A_S-DF-bounded-continuation-profile.md]]'
- '[[01_Statements/02_Outer_Formation/013_S-DF-local-comparability-field.md]]'
successors:
- '[[01_Statements/02_Outer_Formation/024_S-DF-identity-admissibility]]'
- '[[01_Statements/02_Outer_Formation/025_S-DF-self-similarity-threshold]]'
- '[[01_Statements/02_Outer_Formation/027_S-DF-identity-invariants]]'
- '[[01_Statements/Definition/S-DF-metric-like-comparability-strengthening]]'
symbols_used:
- '[[01_Statements/SYMBOLS/Epsilon]]'
- '[[01_Statements/SYMBOLS/Sigma_epsilon]]'
sources:
- path: TheoryOfChange/01_CoreOntology/COT_5_Self_Similarity_and_the_Emergence_of_Identity.md:60
flags: []
tags:
- layer/foundations
- domain/ontological
- type/DF
- concept/identity
- symbol/Epsilon
- symbol/Sigma_epsilon
- status/stable
- strand/ontological
status: stable
---
# Similarity operator — graded retained-versus-altered comparison inside the identity branch
## Claim (formal)
A similarity operator `Sim(X,Y | C)` is a graded comparison over a declared context `C` that tracks how much of a bounded changing line is retained versus altered across transformation. It is prior to any thresholded same/not-same decision.

## Philosophical Translation (of formal claim)
Before identity can be sharpened, the theory needs a disciplined way to say: this transformed line remains more answerable to the bounded continuation-profile than that one. Similarity is that graded retained-versus-altered comparison. It does not yet decide identity; it makes profile-answerable preservation versus alteration explicit within the identity branch.

## Philosophical Justification
[[01_Statements/02_Outer_Formation/016A_S-DF-bounded-continuation-profile]] secures the weaker survivor to which later continuation is answerable, and [[01_Statements/02_Outer_Formation/016_S-DF-identity-through-change]] states identity as same-line answerability through change rather than frozen equality. [[01_Statements/02_Outer_Formation/013_S-DF-local-comparability-field]] already secures the more general pre-metric fact that continuations can be compared in terms of preservation, loss, and strain. The identity branch now needs a narrower comparison focused specifically on how much a transformed line remains answerable to its bounded continuation-profile. Without such a graded operator, later claims about identity-scoped admissibility, threshold, or invariant content remain rhetorical.

## Explanation (informal)
`Sim` does not ask whether two lines are identical in the strongest sense. It asks how much preservation versus alteration is present between them under a declared comparison frame. It is therefore later and narrower than general comparability, but still earlier than identity-recognition.

## Derivation (Philosophical)
- Identity-through-change requires comparing transformed continuations without collapsing them into strict equality.
- Local comparability already gives the weaker order relation: some continuations preserve more and strain less than others.
- The identity branch needs that weaker order specialized into retained-versus-altered comparison over a bounded continuing line.
- Therefore a graded similarity operator is needed before identity-scoped admissibility or threshold.

## Derivation (Formal/Logical/Mathematical)
```text
Sim: D×D×C → G
where D is a declared bounded comparison domain, C fixes context/tolerances,
and G is a graded codomain ordering more-retained/less-retained cases.
```

## Clarifications / Further Context
- `Sim` is not yet identity-recognition.
- `Sim` is context-sensitive because what counts as preserved is never free-floating.
- `Sim` is narrower than the general comparability field and should not be mistaken for a global metric.
- Thresholding and invariant-content are downstream uses of `Sim`, not prerequisites for it.

## Next Steps in Chain
- introduce an identity-scoped admissibility band over graded similarity;
- only later sharpen that admissibility band into thresholded recognition;
- then ask what content remains preserved within recognized continuity.

## Tags
#type/DF #layer/foundations #domain/ontological #concept/identity #symbol/Epsilon #symbol/Sigma_epsilon #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/02_Outer_Formation/016_S-DF-identity-through-change]]
- [[01_Statements/02_Outer_Formation/024_S-DF-identity-admissibility]]
- [[01_Statements/02_Outer_Formation/025_S-DF-self-similarity-threshold]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-identity-change]]
- Parents: [[01_Statements/02_Outer_Formation/016A_S-DF-bounded-continuation-profile.md]]; [[01_Statements/02_Outer_Formation/013_S-DF-local-comparability-field.md]]
- Dependencies: [[01_Statements/02_Outer_Formation/016_S-DF-identity-through-change]]; [[01_Statements/02_Outer_Formation/016A_S-DF-bounded-continuation-profile.md]]; [[01_Statements/02_Outer_Formation/013_S-DF-local-comparability-field.md]]
- Successors: [[01_Statements/02_Outer_Formation/024_S-DF-identity-admissibility]]; [[01_Statements/02_Outer_Formation/025_S-DF-self-similarity-threshold]]; [[01_Statements/02_Outer_Formation/027_S-DF-identity-invariants]]; [[01_Statements/Definition/S-DF-metric-like-comparability-strengthening]]
<!-- END:AUTOGEN:RELATIONSHIPS -->
