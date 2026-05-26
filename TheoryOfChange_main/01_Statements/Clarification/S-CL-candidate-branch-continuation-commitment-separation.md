---
id: stmt.candidate-branch-continuation-commitment-separation
type: CL
aliases:
- S-CL-candidate-branch-continuation-commitment-separation
- CandidateBranchContinuationCommitmentSeparation
title: Candidate, branch, continuation, and commitment separation
concepts:
- '[[02_Concepts/C-identity-change]]'
dependencies:
- '[[01_Statements/Derivation/S-DR-pressure-signature-continuation-branch-identity.md]]'
- '[[01_Statements/02_Outer_Formation/022_S-DF-thin-collapse-law.md]]'
parents:
- '[[01_Statements/Derivation/S-DR-pressure-signature-continuation-branch-identity.md]]'
successors:
- '[[../ChangeOntCode/docs/kernel_spec/44_CANONICAL_CANDIDATE_SURFACE.md]]'
- '[[../ChangeOntCode/docs/kernel_spec/47_RECURSIVE_CONTINUATION_FIELD.md]]'
- '[[../ChangeOntCode/docs/kernel_spec/80_KERNEL_SIDE_RELATION_SURFACE_CONTRACT.md]]'
symbols_used: []
flags:
- requires-code-audit-before-runtime-claim
tags:
- layer/foundations
- domain/operational
- type/CL
- concept/candidate
- concept/branch
- concept/commitment
- concept/kernel-bridge
status: canonical-scaffold
---
# Candidate, branch, continuation, and commitment separation

## Purpose
This clarification prevents four distinct layers from collapsing into one another.

## Distinctions

### Native action
A native action is the domain-level interface expression available in a problem family: move north, pull arm 2, inspect, repair, replace, wait.

A native action is not a continuation identity. It is what the final commitment may have to output into the environment.

### Candidate
A candidate is a surfaced possible expression at a decision point. It may be a native action, a grouped expression, or a local continuation-expression proposed for consideration.

CandidateSurface may publish candidate expressions and public signals about them. It should not itself silently decide final branch topology unless that role is explicitly assigned and documented.

### Continuation
A continuation is a live unfolding profile across time. It is richer than a current action and may persist through multiple native actions.

### Branch
A branch is the retained identity of a continuation inside the field. It is individuated by pressure-signature continuity, not by action label.

### Commitment
A commitment is earned collapse of the live continuation field into an expression/action under the active boundary and shape regime.

## Why the separation matters
If these layers collapse into each other, the system becomes ordinary action scoring:

```text
candidate ≈ action ≈ branch ≈ commitment
```

That is incompatible with a recursive continuation field. RCF can only be a CO-native mechanism if branches can persist across actions, actions can express different branches, and commitment occurs only after live structure has been lawfully thinned.

## Correct architecture
```text
adapter publishes public facts and native action affordances
→ CandidateSurface surfaces candidate expressions and public local signals
→ RelationSurface derives continuation identities and relations
→ RecursiveContinuationField evolves branch pressure topology
→ CommitmentSurface performs earned collapse into native action expression
```

## Implementation implication
Any runtime that uses action as the primary branch identifier must be marked provisional. If `continuation_id` or `branch_id` is present, it has authority over `action` for field identity. Action may be used as a last-resort placeholder only when no continuation identity exists.

## Tags
#type/CL #layer/foundations #domain/operational #concept/candidate #concept/branch #concept/commitment #concept/kernel-bridge #status/canonical-scaffold
