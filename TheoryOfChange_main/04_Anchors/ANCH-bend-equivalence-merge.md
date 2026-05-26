---
title: Bend-equivalence merging beats edit-based clustering
status: draft
tags: [anchor, identity, bend-equivalence]
sources:
  - path: TheoryOfChange/00_Meta/AI_RecursiveChats_slim/AI_13_Spiral_5_Hero.md:39421-39453
---
# Bend-equivalence merging beats edit-based clustering

Toy experiment: many surface contexts (`A*`, `B*`), each with only 2 training samples; futures differ by family (A vs B). Tested three predictors on next-event NLL:
- No merge (one model per context).
- Edit-merge (merge if strings differ by ≤1).
- CO bend-equivalence (merge only if edit distance ≤1 *and* empirical future distributions match within JS ≤ θ).

Result (80 runs, sparse regime):
- No merge: NLL ≈ 0.872.
- Edit-merge: NLL ≈ 0.933 (over-merges, biases).
- Bend-equivalence: NLL ≈ 0.592 (wins in 100% of seeds).
- If θ loosened to ~0.03, performance collapses toward edit-merge, showing the bend-tolerance “sweet spot”.

Takeaway: defining identity by future agreement under bounded bends materially reduces variance without cross-family bias; it’s not just attention reweighting.
