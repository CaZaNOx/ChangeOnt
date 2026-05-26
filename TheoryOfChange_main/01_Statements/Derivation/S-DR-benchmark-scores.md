---
id: stmt.benchmark-scores
type: DR
aliases: ["AI13.BenchScores"]
title: Benchmark scoring — structural outperformance
concepts: ["[[02_Concepts/C-markov-closure]]"]
dependencies: ["[[01_Statements/Definition/S-DF-change-benchmark-protocol]]"]
parents: ["[[01_Statements/Definition/S-DF-change-benchmark-protocol]]"]
successors: []
symbols_used: []
sources:
  - path: TheoryOfChange/00_Meta/AI_Summaries/AI_13_THEORY_ONLY.md:27
flags: []
tags: [layer/validation, domain/logical, stable, "type/DR", "concept/markov-closure"]
---
# Benchmark scoring — structural outperformance
## Claim (formal)
Define an aggregate score combining SRL, SE‑weighted identity persistence, indicator coverage, and collapse avoidance; outperforms classical if aggregate exceeds baseline with justified Tx use and minimal GH backlog.

## Philosophical Translation (of formal claim)
Winning means: it recurs, it holds together, it detects when structure must change, and it doesn’t hide failures.

## Clarifications / Further Context
- “Minimal GH backlog” encourages explicit resolution rather than sweeping gaps under the rug.
- Tx use must be declared and justified; unacknowledged Tx counts against the score.

## Derivation (Formal/Operational)
```text
score := w1·SRL + w2·SE_weighted + w3·(1−collapse_rate) + w4·indicator_coverage
penalty for GH_backlog, unreported Tx
```

## Proofs/Corollaries References
- derived from [[S-DF-change-benchmark-protocol]] components.

## Next Steps in Chain
- suggest: publish benchmark cards with component breakdowns and Tx/GH disclosures.

## Tags
#type/DR #layer/validation #domain/logical #concept/markov-closure #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-change-benchmark-protocol]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-markov-closure]]
- Parents: [[01_Statements/Definition/S-DF-change-benchmark-protocol]]
- Dependencies: [[01_Statements/Definition/S-DF-change-benchmark-protocol]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

