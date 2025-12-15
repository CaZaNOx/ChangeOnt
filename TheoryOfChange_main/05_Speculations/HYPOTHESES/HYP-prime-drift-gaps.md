---
id: hypothesis.prime-drift-gaps
title: Hypothesis — Primes as drift-exposed gaps in coverage
status: hypothesis
tags: [speculation, hypothesis, primes, drift, coverage]
sources:
  - path: TheoryOfChange/00_Meta/AI_RecursiveChats/AI_21.md:326-369
links_core: []
---
# Hypothesis — Primes as drift-exposed gaps in coverage

Claim (speculative)
- Primes mark low-coverage “gaps” in the lattice induced by existing factors; adding a new prime increases coverage depth and reduces drift sensitivity up to a range, after which new gaps appear. Predicting the next prime corresponds to predicting where the current factor coverage thins under drift/perturbation.

Exploratory sketch
- Define coverage of integers (or rationals at a given depth) by current primes; measure uncovered density and proxy “drift force” needed to disturb the covered set. Track how coverage improves when a new factor is added and where new uncovered pockets arise.

Questions/falsifiers
- Can uncovered density or drift-sensitivity metrics predict prime locations better than chance?
- Does the gap picture reduce to known sieve/analytic structure (trivial), or does it yield new bounds/heuristics?

Why it matters
- Reframes primes as structural gaps created by coverage/closure rules, aligning with CO drift/identity language; could suggest new heuristics or refute the framing if it adds nothing beyond standard number theory.
