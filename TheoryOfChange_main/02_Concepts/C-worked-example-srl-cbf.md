---
id: concept.worked-example-srl-cbf
title: Worked Example — Identity, SRL, CBF, GH/Tx, Benchmark
tags: ["concept/worked-example", validation, ontological]
status: draft
---
# Worked Example — Identity, SRL, CBF, GH/Tx, Benchmark
Overview:
Illustrative toy scenario showing how to (1) define Sim≈ and invariants for a pattern P; (2) evaluate SRL(P); (3) compute CBF(P); (4) detect GH/Tx during a phase shift; and (5) score the benchmark against a classical baseline.

Setup
- Pattern P: relational configuration (graph of 5 nodes) with invariant degree sequence and cycle structure.
- Transformations T_k: small rewires and weight changes within LocalReach.
- Similarity: Sim(T_k(P),P) based on graph edit distance normalized to [0,1].
- Threshold: θ = 0.8; resolution ε chosen to ignore micro weight jitters; σ(ε) moderate.

Identity via ≈ and invariants
- Use [[S-DF-similarity-operator]] and [[S-DF-identity-invariants]].
- Invariants I: degree sequence, presence of 5‑cycle; Sim≥θ over window K.

SRL(P)
- Use [[S-DF-structural-recurrence-likelihood]] and [[S-DF-rtv-operator]].
- Breath cycles accept when both RTV holds and Sim≥θ; frame SRL on the [[01_Statements/Definition/S-DF-evaluation-surface]] rather than probability language; see [[01_Statements/Clarification/S-CL-probabilistic-language-srl]].

CBF(P)
- Use [[S-DF-change-fitness]] and [[S-DR-fitness-vs-srl-se]].
- CBF combines SRL, stability via [[S-DF-stabilization-energy]] and threshold, minus GH backlog + Tx penalties.

Phase shift with GH/Tx
- At cycle k*, detector flags “variable creation” and boundary deformation — see [[S-DF-nonclassical-indicators]].
- Cross‑audit [[S-DF-cross-audit-markov-gh-tx]] marks GH at k*; introduce Tx to express new frame.
- Pointers transported under Tx per [[S-DR-pointer-behavior-under-tx]].

Benchmark scoring
- Apply [[S-DF-change-benchmark-protocol]]: report SRL, SE‑weighted identity persistence, indicator incidence, collapse ⊘ avoidance, GH backlog.
- Score via [[S-DR-benchmark-scores]]; classical baseline lacks Tx, accumulates GH, fails new attractor detection [[S-DR-predictive-statement-nonclassical]].

Summary
- Identity persists via invariants + ≈; SRL high pre‑shift; CBF stable.
- Phase shift detected; Tx resolves GH; SRL recovers; CBF penalized briefly then restored.
- Classical baseline under‑performs on emergence and accumulates unresolved GH.

## Tags
#concept/worked-example #layer/validation #domain/ontological
















































































































<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

<!-- END:AUTOGEN:RELATIONSHIPS -->




































































































