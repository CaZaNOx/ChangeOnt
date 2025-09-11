# Maze1 Environment

A minimal grid maze to sanity-check kernel/evaluation path.
- **State:** (x, y) on a width�height grid.
- **Actions:** up, down, left, right.
- **Terminal:** bottom-right corner.
- **Baselines:** FSM, LSTM-lite.
- **Status:** will be frozen after baseline parity checks.

References for baseline behavior: see `docs/stoa/Baseline_Fidelity.md`.

Reward convention (frozen):
- -1 for every non-terminal move
- 0 on the terminal transition into the goal
Implication: shortest-path length L yields return = -(L-1). With our 5x5 maze (seed=0), L=8 -> return -7
