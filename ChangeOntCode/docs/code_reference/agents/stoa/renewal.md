# docs/code_reference/agents/stoa/renewal.md

# STOA Renewal Baselines

## Purpose

This file documents the renewal-side classical baselines.

---

## Why this family exists

Renewal baselines provide classical sequence/event predictors and heuristics.

These are important because many renewal-like environments may be:
- strongly stationary,
- weakly shifting,
- or classically well handled by relatively simple sequence models.

---

## Typical baseline types

Examples may include:
- last
- phase
- ngram
- vom-like models
- other clearly documented classical sequence baselines

---

## Runtime role

Renewal STOA baselines are instantiated by the renewal runner when the suite config selects a classical renewal baseline.

They must expose a clear family-local prediction/action/update surface.

---

## Documentation requirements

Each baseline implementation should document:
- what sequence assumptions it makes
- whether it models stationarity
- whether it supports changing recurrence structure
- what state it maintains
- how it updates

---

## Relation to CO

Renewal is one of the better current families for testing:
- recurrence-sensitive structure
- closure and compressibility behavior
- and when classical sequence models are already enough

CO should not try to “beat” renewal STOA everywhere if the regime is highly classical.

---

## Misalignment examples

This area is misaligned if:
- renewal baselines are used in suite comparison without clear semantics,
- API expectations are unclear,
- or the project claims honest renewal comparison while the baseline path is not well documented.