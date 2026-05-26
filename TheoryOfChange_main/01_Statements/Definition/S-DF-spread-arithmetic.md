---
id: stmt.df-spread-arithmetic
type: DF
title: Spread arithmetic and probabilistic Hoare interpretation
concepts: ["[[02_Concepts/C-math-structures]]"]
dependencies: ["[[01_Statements/Definition/S-DF-evaluation-surface]]"]
parents: []
successors: []
symbols_used: []
sources:
  - path: TheoryOfChange_main/00_Meta/Context/AI_13_leads_master.txt:94
  - path: TheoryOfChange_main/00_Meta/Context/AI_13_leads_master.txt:95
flags: []
tags: [formal, logic/quantale, "type/DF", "concept/math-structures"]
---
# Spread arithmetic and probabilistic Hoare interpretation

## Claim (formal)
Treating costs as negative log-likelihoods yields a “probabilistic Hoare” view of the evaluation surface. Spread-valued quantities (b, d) support addition/multiplication on the open domain |μ_y| > b_y + d_y, with division defined by first-order Taylor propagation of spreads; closure holds on that domain.

## Philosophical Translation (of formal claim)
When we measure uncertainty as spread around a mean, composing or inverting those quantities is just composing or inverting their implied log-likelihoods—division works as long as the noise is small enough to keep the approximation honest.

## Notes
- Domain guard: require |μ_y| > b_y + d_y before applying division to avoid singularities.
- Approximate division: use first-order Taylor to propagate spreads through inversion; acceptable when spreads are small relative to the mean.
- Compatibility: aligns with the quantale-based evaluation surface; reduces to ordinary real arithmetic when spreads collapse to zero.

## Tags
#type/DF #layer/foundations #domain/formal #concept/math-structures

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By

<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-math-structures]]
- Dependencies: [[01_Statements/Definition/S-DF-evaluation-surface]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

