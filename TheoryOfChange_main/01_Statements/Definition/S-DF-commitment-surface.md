---
id: stmt.df-commitment-surface
type: DF
title: CommitmentSurface
concepts:
  - '[[02_Concepts/C-kernel]]'
  - '[[02_Concepts/C-collapse]]'
parents:
  - '[[01_Statements/Clarification/S-CL-scalarization-as-thin-collapse]]'
dependencies:
  - '[[01_Statements/Clarification/S-CL-public-facts-vs-policy-advice]]'
successors:
  - '[[../ChangeOntCode/docs/kernel_spec/43_CANONICAL_COMMITMENT_RULE.md]]'
symbols_used:
tags:
  - layer/kernel-runtime
  - type/DF
  - concept/commitment-surface
status: runtime-surface-definition
---
# S-DF CommitmentSurface

CommitmentSurface :=
The runtime readout surface that expresses an earned collapse as a native action. It is not a deep ontology element and must not act as a hidden policy head.

Layer: kernel/readout boundary.

Canonical role: convert certified branch commitment into native action expression without non-CO rescue selection.
