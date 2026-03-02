# docs/code_reference/agents/stoa/maze.md

# STOA Maze Baselines

## Purpose

This file documents the maze-side classical baselines.

---

## Why this family exists

Maze baselines provide strong classical planning/reference behavior.

Examples like BFS and A* are especially useful because they test:
- shortest-path style reasoning,
- explicit graph search,
- and highly classical navigation assumptions.

---

## Typical baseline types

Examples may include:
- BFS
- A*
- other search/planning baselines if added

---

## Runtime role

Maze STOA baselines are instantiated by the maze runner when the suite config selects a classical maze baseline.

Some may act as:
- planners that precompute a path,
- or iterative decision policies if added later.

---

## Documentation requirements

Each baseline implementation should document:
- whether it is a full planner or stepwise policy
- what map information it assumes
- what legality/graph structure it requires
- what guarantees or approximations it provides

---

## Relation to CO

Maze is a strong stress test for CO path-space reasoning.

To compare honestly against CO:
- classical maze baselines must be clearly documented,
- and the comparison must acknowledge that BFS/A* are highly classical strong fits in many fixed-rule maze settings.

This is exactly the kind of domain where CO may decide that the most honest answer is near-total classical collapse.

---

## Misalignment examples

This area is misaligned if:
- planners and reactive policies are mixed without explanation,
- baseline assumptions are unclear,
- or maze STOA is used as a reference in summaries without documenting what information it assumes.