---
id: stmt.df-candidate-surface
type: DF
title: CandidateSurface
concepts:
  - '[[02_Concepts/C-kernel]]'
parents:
  - '[[01_Statements/Derivation/S-DR-continuation-branch-identity-from-bounded-continuation-profile]]'
dependencies:
successors:
  - '[[../ChangeOntCode/docs/kernel_spec/44_CANONICAL_CANDIDATE_SURFACE.md]]'
symbols_used:
tags:
  - layer/kernel-runtime
  - type/DF
  - concept/candidate-surface
status: runtime-surface-definition
---
# S-DF CandidateSurface

CandidateSurface :=
The runtime intake surface that publishes candidate expressions and public evidence as candidate rows. It is not a deep ontology element and must not decide branch identity or action commitment.

Layer: kernel runtime surface.

Canonical role: expose public candidate structure to continuation identity, burden, relation, RCF, and collapse-certificate stages.
