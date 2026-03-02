# docs/code_reference/agents/stoa/bandit.md

# STOA Bandit Baselines

## Purpose

This file documents the bandit-side classical baselines.

---

## Why this family exists

Bandit baselines are important because they are often strong in highly classical/stationary choice settings.

They therefore provide:
- a meaningful benchmark,
- and a concrete classical continuation stream that CO may partially collapse toward.

---

## Typical baseline types

Examples may include:
- UCB1
- KL-UCB
- Thompson sampling
- epsilon-greedy variants
- other documented strong bandit baselines

---

## Runtime role

Bandit STOA baselines are instantiated by the bandit runner when the suite config selects a classical bandit agent.

They must expose a clear runner-facing action/update surface.

---

## Documentation requirements

Each baseline implementation should document:
- what family-local assumptions it makes
- what state it maintains
- what action rule it uses
- how it updates on reward/feedback
- whether it assumes stationarity or can handle structured non-stationarity

---

## Relation to CO

CO should not be judged honestly against bandit STOA unless the bandit baselines are:
- correctly implemented,
- well documented,
- and not accidentally handicapped.

In highly classical bandit regimes, strong bandit STOA may legitimately dominate.

---

## Misalignment examples

This area is misaligned if:
- baseline assumptions are undocumented,
- the runner-facing API is unclear,
- or bandit STOA is used in plots/summaries without clarity about what each baseline actually is.