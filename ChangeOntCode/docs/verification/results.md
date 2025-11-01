# Verification Results — How to Read

This repo ships automated checks that mirror the claims in the cited papers.

## Bandit
- **Monotonicity**: `cumulative_regret` is non-decreasing (sanity).
- **UCB1**: high R² when fitting `regret ~ a*ln(t)+b`; low R² for linear fit; empirical regret **below** classic upper bound.
- **ε-greedy (fixed ε)**: high R² when fitting `regret ~ c*t + d`; slope increases with ε and decreases with gaps.

Pass criteria (default):
- R²_log (UCB1) ≥ 0.90 and R²_lin (UCB1) ≤ 0.90
- R²_lin (ε-greedy) ≥ 0.95
- All seeds satisfy monotonicity & reward∈[0,1].
- Empirical regret ≤ theoretical bound for each config (reported).

## Maze
- **BFS** steps == independently-computed shortest path every episode.
- Returns = −steps (all runs).

Pass criteria:
- All episodes in all seeds: `steps == gt_shortest_steps`.

## Renewal
- **Invariant**: `reward==1` iff `act==obs` (mismatch==0).
- **Ordering**: `phase` ≫ `last` and `ngram` in clean regime (median final cum_reward is highest).

Pass criteria:
- All seeds: mismatch=0; ordering checks pass.

## Reproducibility
- Every artifact (metrics, CSV, plots) has SHA-256 in the console log.
- Configs, seeds, and code commit are printed at run time.

