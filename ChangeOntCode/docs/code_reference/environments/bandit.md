# docs/code_reference/environments/bandit.md

# Bandit Environments

## Purpose

Bandit environments model repeated choice among arms under reward uncertainty.

---

## Why this family exists

The bandit family is useful for testing:
- local choice under uncertainty,
- gradual structure acquisition,
- stationarity vs non-stationarity,
- and collapse toward highly classical handling in strongly stabilized cases.

Bandit tasks are simpler than maze in path geometry, but still useful for testing:
- gauge-like adaptation,
- classicality collapse,
- simple change/reward structure,
- and whether CO adds anything beyond strong bandit baselines.

---

## Family-local semantics

A bandit environment typically defines:
- a finite set of arms,
- reward generation logic,
- optional stationarity/non-stationarity,
- a horizon or stopping condition.

---

## Reset contract

**Binding**

Reset should clearly define:
- whether arm reward distributions are fixed for the run,
- whether they change across resets,
- what is returned initially,
- and what state is preserved or discarded.

---

## Step contract

**Binding**

Step should clearly define:
- the chosen arm/action,
- returned reward/feedback,
- whether additional observation is returned,
- and whether the run is terminal.

---

## Classicality relevance

Bandit environments are especially relevant to:
- strong classical baselines such as UCB/KL-UCB/TS,
- and to testing whether CO correctly collapses toward near-classical behavior in strongly stationary settings.

For example:
- if the environment is highly stationary and clearly classical,
- CO should not be forced to fight STOA unnecessarily.

---

## Translator relevance

The bandit translator must convert bandit-local information into:
- path-space updates,
- local continuation structure,
- and update-relevant structural signals,

without silently reducing the kernel to a thin copy of classical bandit state.

---

## New environment integration rule

A new bandit-like environment should document:
- arm set semantics,
- reward-generation semantics,
- stationarity assumptions,
- and what family-local information can legitimately be used by STOA and CO.

---

## Misalignment examples

Bandit environment handling is misaligned if:
- stationarity/non-stationarity is unclear,
- reward observations are insufficiently documented,
- runner/translators assume APIs the environment does not actually provide,
- or the family is treated as more path-structured or less structured than it really is without explicit translation logic.