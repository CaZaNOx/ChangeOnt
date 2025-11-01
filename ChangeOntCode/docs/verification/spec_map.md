# Spec ↔ Code Map (SoTA baselines)

This document maps each paper-level equation/assumption to its implementation in this repo.
Use it during code review and when answering “is this really the SoTA algorithm?”.

---

## Bandit

**Papers & textbook references**
- Auer, Cesa-Bianchi, Fischer (2002) “Finite-time Analysis of the Multiarmed Bandit Problem” — UCB1.
- Sutton & Barto (2018) — ε-greedy incremental update.

**Environment**
- Bernoulli K-armed bandit with stationary means  
  → `environments/bandit/bandit.py::BernoulliBanditEnv`
  - Sampling: `step(arm)` returns `r ∈ {0,1}` with `P(r=1)=p_arm`.
  - Horizon handling: `horizon` stops at `t==H`.

**UCB1 Agent**
- Index: \( \text{UCB}_a(t) = \hat{Q}_a + \sqrt{(2\ln t)/N_a} \)
- Initialization: play each arm once before using the index.
- Update: \( \hat{Q} \leftarrow \hat{Q} + (r - \hat{Q})/N \)
  → `experiments/runners/bandit_runner.py::UCB1Agent`
  - `select()`:
    - “play each arm once” loop
    - compute `ucb_vals = value[a] + sqrt(2*log(t)/counts[a])`
  - `update(a,r)`: incremental average

**ε-greedy (fixed ε)**
- Action selection: with prob ε pick random arm; else argmax \(\hat{Q}\)
- Same incremental update as above
  → `experiments/runners/bandit_runner.py::EpsilonGreedyAgent`

**Metrics**
- Cumulative pseudo-regret:  
  \( R_T = \sum_{t=1}^T (\mu_* - \mu_{a_t}) \)  
  → computed in `bandit_runner.py` using known `probs`.

---

## Maze

**Ground truth**
- Shortest-path length on unit-cost grid.
- BFS must match the optimal steps exactly.

**Environment & BFS**
- Grid maze, passability from `environments/maze1/env.py::GridMazeEnv`
- BFS implementation & deterministic DIR order  
  → `experiments/runners/maze_runner.py::_bfs_path` and `main()`
- Episode semantics: reward = −1 per move, 0 at goal; return = −steps.

**Metrics**
- `episode_steps`, `episode_return` per episode; budget line per episode.

---

## Renewal

**FSM baselines**
- `last` = action at t equals previous observation
- `phase` = finite-state machine tracking renewal phases (frozen logic)
- `ngram` = short history table (k = L_win − 1)

**Environment**
- Codebook renewal process with params \(\{A, L_{\text{win}}, p_{\text{ren}}, p_{\text{noise}}, T_{\max}\}\)  
  → `experiments/env.py::CodebookRenewalEnvW, EnvCfg`

**Runner & invariant**
- Invariant: `reward==1 ⇔ act==obs` must hold  
  → `experiments/runners/renewal_runner.py::run()` (mismatch check is in the evaluation scripts)

**Metrics**
- `cum_reward` written each step; header logs `mode` (last|phase|ngram|haq).

---

## Cross-cutting

**Writers**
- JSONL writer: `kernel.logging.JSONLWriter` if available, else local fallback.
- Budget CSV: always at least one data row (`params_bits, flops_per_step, memory_bytes`).
- Artifacts are hashed in verification scripts for reproducibility.

