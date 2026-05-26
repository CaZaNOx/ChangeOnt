# EI: ChangeOps
Current classification: **Provisional**

Substantive change-structure element on the default path, but still narrower and less closed than EC.

## What this element is
EI is the element that operates on change-structure itself rather than merely on static summaries of state. In current runtime terms, this means extracting and using motif, prototype, and composition structure across unfolding histories to build candidate continuation guidance.

## Why this element exists
If change is ontologically primary, the kernel cannot remain limited to state features plus generic adaptation. It must have at least one element that:
- reads recurring change-patterns,
- composes them,
- and uses them to shape future continuation preference.

EI is the clearest current expression of that requirement.

## What EI is not
EI is not:
- a vague bucket for every second-order adaptation,
- a translator in disguise,
- or a hidden planner.

It is the element that makes motif/composition structure from unfolding available to the kernel.

## Intended upstream support
Typical supporting primitives include:
- P10 ChangeOpsCore / prototype persistence
- P12 ClosureQuotient or equivalent merge/closure support
- P5 TemporalOps for ordered trace shaping
- family packet history/trace inputs

## Inputs
Typical inputs include:
- history/trace
- local candidate fields
- prototype stores or motif stores
- merge/composition signals

## Outputs
EI should produce signals such as:
- motif strength,
- composition preference,
- continuation proposals shaped by recurring change-patterns,
- prototype-supported candidate weighting.

## Why this matters philosophically
Without an element like EI, the kernel risks saying “change is primary” while still behaving as if only state snapshots matter. EI is the runtime pressure-test of whether the system can really operate on unfolding itself.

## Current status
Substantive and important. Still worth auditing against drift or over-broad interpretation, but now clear enough to be a meaningful content doc rather than a label.