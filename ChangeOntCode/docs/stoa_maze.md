<!-- docs/stoa_maze.md -->
# STOA: Unweighted Grid Maze (BFS)

**Reference**
- BFS finds shortest paths in unweighted graphs (standard CLRS/MIT notes).

**Expectation**
- `episode_steps` equals offline shortest path length for each episode; returns ≈ `-steps`, 0 upon reaching goal.

**Acceptance**
- BFS steps == optimal for every episode.
- Deterministic with fixed seed.

**Pitfalls**
- Illegal moves changing step cost, or reward shaping that deviates from 0-at-goal / −1 per step.
