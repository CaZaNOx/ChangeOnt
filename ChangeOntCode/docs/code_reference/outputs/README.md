# docs/code_reference/outputs/README.md

# Outputs Folder

## Purpose

`outputs/` contains generated artifacts from runs and suites.

---

## Why it exists

The project needs outputs that make execution:
- inspectable,
- reproducible,
- comparable,
- and diagnosable.

Outputs are not side clutter. They are part of the contract.

---

## Runtime role

The outputs tree stores:
- per-run artifacts,
- per-mode summaries,
- per-family summaries,
- suite summaries,
- plots,
- manifests,
- and temporary generated run configs where applicable.

---

## Required artifact levels

### Run level
Required:
- `metrics.jsonl`
- `budget.csv`
- `run_manifest.json`
- `job_state.json`
- `quick_plot.png`

### Mode level
Required:
- summary CSV
- mode plot(s)

### Family level
Required:
- combined summary CSV
- family plot(s)

### Suite level
Required:
- overall summary CSV
- STOA-vs-CO comparison CSV
- CO-only competition CSV(s)
- suite plot(s)
- failure/provenance summary artifacts

---

## Documentation requirement

The outputs documentation should make it easy to answer:
- what each file means,
- what produced it,
- which contract it belongs to,
- and when missing or malformed output counts as a real failure.