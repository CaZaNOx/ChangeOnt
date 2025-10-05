# BENCHMARKS — Task Families

We choose small but honest families where CO’s edge is visible without supercompute.

## 1) Renewal / Codebook

- Latent codebook with merges/splits; geometric renewals; emissions with small noise; an implicit k-opportunity motif.
- **Separates (a,e,f):** HAQ produces abrupt flips aligned to events; baselines thrash without oracle signals.

## 2) Drifting Bandit

- Means drift by bounded random walk; nonstationary arms.
- **Separates (a,d,f):** Diversity control and LLN guards prevent over-commitment; CO adapts on the right timescale.

## 3) Grid Maze with Holes

- Small mazes with sporadic corridor blockages; local observations only.
- **Separates (a,e,h,i):** flips and turns recover faster from topology-preserving costs than greedy BFS-like heuristics.

## Adversarial Controls (CO-disadvantaged)

- Fully stationary tasks with IID emissions: classical dynamic programming or UCB dominates; collapse header should engage.
