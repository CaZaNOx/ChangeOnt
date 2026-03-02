# docs/code_reference/agents/stoa/shared_models.md

# STOA Shared Models

## Purpose

This file documents any shared classical model support code used across STOA family implementations.

---

## Why it exists

Some classical support logic may be reused across:
- renewal baselines
- bandit-side helper models
- or other family-local classical implementations

Keeping shared support explicit prevents baseline behavior from becoming scattered and opaque.

---

## Documentation requirements

Any shared model/helper should document:
- which baselines use it
- what state it maintains
- what assumptions it encodes
- whether it is generic or family-specific support

---

## Status guidance

Shared classical support should be documented as:
- canonical support,
- optional support,
- experimental,
- or legacy/inactive.

---

## Misalignment examples

This area is misaligned if:
- baseline behavior depends heavily on a shared helper whose semantics are undocumented,
- or the shared helper effectively encodes major family assumptions that are never documented in the baseline docs.