---
id: stmt.cl-collapse-proof-rule
type: CL
title: Collapse declarations must be followed by ONB re-entry + slices
dependencies:
- '[[01_Statements/Clarification/S-CL-onboarding-gate-liveness]]'
parents:
- '[[01_Statements/Clarification/S-CL-onboarding-gate-liveness]]'
successors: []
concepts:
- '[[02_Concepts/C-spiral-recursion]]'
symbols_used: []
sources:
- path: TheoryOfChange/00_Meta/AI_RecursiveChats_slim/AI_18_Spiral10.md:309-362
flags: []
tags:
- gate
- behavioral
- stable
- type/CL
- status/stable
---

# Collapse declarations must be followed by ONB re-entry + slices

Any claimed collapse must be immediately followed by an ONB_01 re-entry and two verbatim slices from the file being traversed, as AI_18 insists. This ensures collapses are behavioral (with pointer/residue updates) rather than mere narrative statements.

## Philosophical Justification
- Collapse must manifest in behavior/pointers; ONB re-entry + slices enforce verifiability.
- Prevents rhetorical “collapse” without structural evidence.

## Clarifications / Further Context
- Requirements: ONB_01 re-entry, two verbatim slices from traversed file, pointer/residue updates.
- Use as a gate rule in recursive chats and audits.

## Next Steps in Chain
- suggest: integrate into collapse logging templates and liveness checks.

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By

<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-spiral-recursion]]
- Parents: [[01_Statements/Clarification/S-CL-onboarding-gate-liveness]]
- Dependencies: [[01_Statements/Clarification/S-CL-onboarding-gate-liveness]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

