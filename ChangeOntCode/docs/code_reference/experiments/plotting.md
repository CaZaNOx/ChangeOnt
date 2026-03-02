# docs/code_reference/experiments/plotting.md

# Plotting and Summaries

## Purpose

The plotting layer collects run artifacts and turns them into:
- mode summaries,
- family summaries,
- suite summaries,
- and corresponding plots.

---

## Why it exists

The project does not only need raw runs.

It needs:
- interpretable comparisons,
- mechanism investigation views,
- and trustworthy STOA-vs-CO and CO-internal summary outputs.

---

## Main areas

### `collect.py`
Collects and normalizes per-run summary inputs.

#### Requirement
Agent identity normalization must be consistent across families.

---

### `main.py`
Suite-level aggregation and summary/plot generation.

#### Requirement
Must produce semantically correct:
- overall summary
- STOA-vs-CO comparison
- CO-only competition outputs

---

### Family-specific plotting files
Examples:
- bandit plotting
- maze plotting
- renewal plotting

#### Requirement
Must document:
- expected summary inputs,
- expected output files,
- and family-specific plot meanings.

---

## Binding semantic rules

### CO-only rule
CO-only competition files and plots must not include STOA rows.

### STOA-vs-CO rule
STOA-vs-CO plots/tables must use compatible metrics across rows.

### Identity normalization rule
Agent naming normalization must be consistent across:
- run folders,
- mode summaries,
- family summaries,
- suite summaries.

### Plot presence rule
Plots must exist at:
- mode level,
- family level,
- suite level.

---

## Current major risk areas

This area is a critical misalignment point if:
- CO-only summaries include STOA baselines,
- STOA-vs-CO files mix incompatible score columns,
- maze agents retain seed suffixes while other families normalize them away,
- labels differ across PNG/SVG/CSV outputs,
- or suite plots misrepresent what actually ran.

---

## Documentation requirement

Every plot/summarization artifact should document:
- what rows it uses,
- what aggregation it performs,
- what the plot is intended to mean,
- and what would make it semantically invalid.