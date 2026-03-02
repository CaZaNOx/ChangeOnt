# docs/code_reference/agents/stoa/README.md

# Agents STOA

## Purpose

`agents/stoa/` contains classical baseline algorithms used for comparison against the CO kernel.

---

## Why it exists

The project does not compare CO against nothing.

It compares CO against:
- state-of-the-art or strong classical baselines,
- or task-family-appropriate baseline heuristics/models.

This is also the source of the explicit classical continuation stream used in comparison and, where appropriate, classical collapse.

---

## Runtime role

Runners instantiate STOA agents when the suite job specifies a classical baseline.

STOA paths should be:
- honest,
- cleanly documented,
- family-appropriate,
- and not hidden inside CO logic.

---

## Expected family coverage

### Bandit
Examples:
- UCB
- KL-UCB
- Thompson sampling
- epsilon-greedy variants

### Maze
Examples:
- BFS
- A*
- other explicit planners if added

### Renewal
Examples:
- last
- phase
- ngram/vom-like classical sequence models if supported

---

## Contract

STOA code should have:
- clearly documented inputs/outputs,
- family-local meaning,
- no silent role confusion with CO,
- and honest integration into summaries/plots.

---

## Status guidance

The STOA tree is canonical for baseline comparison, but not ontologically primary in the project.

It exists to make honest comparison possible and to provide the explicit classical stream that CO may partially collapse toward in highly classical regimes.