# docs/code_reference/outputs/summaries_and_plots.md

# Summaries and Plots

## Purpose

This file documents the outputs produced above run level:
- mode summaries
- family summaries
- suite summaries
- corresponding plots

---

## Why they exist

The project needs:
- honest comparison across runs
- family-level and suite-level aggregation
- mechanism investigation views
- trustworthy STOA-vs-CO and CO-only comparison outputs

---

## Mode-level outputs

**Binding**

Every completed mode must produce:
- mode summary CSV
- mode plot(s)

### Meaning
A mode summary aggregates all runs inside one concrete environment/mode.

### Requirements
- all runs in the mode must have finished first
- labels must reflect actual agent identities consistently
- plots must represent the aggregated mode semantics honestly

---

## Family-level outputs

**Binding**

Every completed family must produce:
- family combined summary CSV
- family plot(s)

### Meaning
A family summary aggregates all completed modes in that family.

### Requirements
- all modes in the family must have finished first
- family plots must not silently mislabel agents or blend incompatible semantics

---

## Suite-level outputs

**Binding**

Every completed suite must produce:
- overall summary CSV
- STOA-vs-CO comparison CSV
- CO-only competition CSV(s)
- suite plot(s)
- failure/provenance artifacts

### Meaning
Suite outputs provide the highest-level cross-family comparison view.

---

## Semantic rules

### CO-only rule
**Binding**

CO-only competition outputs must exclude STOA rows.

### STOA-vs-CO rule
**Binding**

STOA-vs-CO outputs must use comparable metric semantics across rows.

### Identity rule
**Binding**

Agent identity normalization must be consistent across:
- run-level folder names
- mode summaries
- family summaries
- suite summaries
- plot labels

### Plot presence rule
**Binding**

Plots must exist at mode/family/suite levels, not just CSVs.

---

## Failure/provenance outputs

**Recommended starting point**

A suite should also include:
- failure summary CSV
- expanded suite manifest
- suite config snapshot
- execution provenance

If absence of these blocks honest diagnosis, promote them to Binding.

---

## Misalignment examples

This layer is misaligned if:
- CO-only plots include STOA baselines,
- STOA-vs-CO outputs mix incompatible score columns,
- agent naming drifts between levels,
- plots are missing,
- or suite outputs are presented as trustworthy while semantically broken.