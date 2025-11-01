# STOA verification: properties and sources

This folder documents *what* we verify for each baseline and *why* it is justified by the literature.

---

## Bandit (UCB1; ε-greedy as contrast)

**We verify**
- Rewards are in **[0,1]** and **cumulative regret is nondecreasing**.
- **UCB1**: empirical regret is **better explained by log(T)** than by T (we compare R² of a log-fit vs. linear-fit after a burn-in).
- **ε-greedy (constant ε)**: regret is **better explained by T** than by log(T) (negative control).

**Primary source**
- Auer, Cesa-Bianchi, Fischer (2002). *Finite-time Analysis of the Multiarmed Bandit Problem*.  
  (UCB1 has O((K log T)/Δ) instance-dependent bounds and O(√(KT log T)) worst-case; empirically, log-like growth fits better than linear.)

---

## Maze (BFS)

**We verify**
- On an **unweighted grid**, BFS returns a **shortest path** from start to goal.
- With per-step reward -1 and terminal reward 0, **episode_return = −episode_steps** exactly.

**Background**
- Standard algorithms result (e.g., CLRS); BFS on unweighted graphs is optimal.

---

## Renewal (finite-state predictors)

**We verify**
- **Determinism**: same seed ⇒ identical metrics file (hash match).
- **Bookkeeping invariant**: reward==1 **iff** (act==obs) on every step.
- **cum_reward is nondecreasing** (because rewards are 0/1).
- **Sanity dominance** on clean configs: *PhaseFSM ≥ LastFSM* (predict-last baseline).

We intentionally avoid claiming a specific numeric bound here; instead we lock down invariants and relative ordering.

---

## Outputs

Running the verify CLI writes, per family:

outputs/verify/<family>/
runs.csv # per-run stats
summary.csv # pass/fail style summary
dominance.csv # (renewal) dominance checks
plots/*.png # quick visual sanity plots