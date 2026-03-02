# Spec Gaps

This file tracks known gaps between:
- target-state docs
- current code
- and remaining open design choices

It is not a place to silently normalize drift.  
It is a place to record it.

## 1. Purpose

A spec gap exists when:
- docs say X but code does Y
- code supports behavior not yet captured in docs
- or an important design area remains genuinely open

## 2. Gap categories

### Documentation gap
The docs are too weak to determine the intended behavior.

### Implementation gap
The intended behavior is clear, but code does not yet implement it.

### Classification gap
A component/file/path exists, but its status is unclear:
- canonical
- optional
- experimental
- legacy

### Open design space
Several CO-faithful realizations remain possible and should not yet be falsely frozen as uniquely derived.

## 3. Current high-priority gaps

### Documentation-level
- exact final integration of all current top-level docs with new target-state docs
- exact YAML/config syntax details in some areas

### Implementation-level
- manifest path resolution
- maze CO non-termination / oscillatory failure
- summary semantic correctness
- header/classical blend correctness
- primitive/translator API mismatches
- honest parameter/config consumption

### Classification-level
- status of several advanced elements
- status of stale or alternate runtime paths
- status of combo/registry/factory artifacts

## 4. Legacy promotion rule

Legacy material may inform target-state docs, but does not become binding unless explicitly promoted into the canonical docs.

Code must not rely on legacy-only semantics without promotion.

## 5. How to use this file

When a gap is resolved:
- update the canonical docs
- update code if needed
- remove or revise the gap entry

This file should shrink over time, not become the hidden home of permanent unresolved drift.