---
id: stmt.locality-prior
type: DF
aliases: ["FND_3.LocalityPrior"]
title: Locality and Prior — constraints within LocalReach
concepts: ["[[02_Concepts/C-prior-pointer-reach]]"]
dependencies: ["[[01_Statements/Definition/S-DF-reach-relation]]", "[[01_Statements/Definition/S-DF-pointer-structural]]"]
parents: ["[[01_Statements/Definition/S-DF-reach-relation]]"]
successors: ["[[01_Statements/Definition/S-DF-depth-reach]]", "[[01_Statements/Definition/S-DF-locality-threshold]]"]
symbols_used: ["[[01_Statements/SYMBOLS/Pointer_field]]", "[[01_Statements/SYMBOLS/Pointer_local]]"]
sources:
  - path: TheoryOfChange/02_Foundations/FND_3_Locality_Prior_and_Pointer.md:1
flags: []
tags: [layer/foundations, domain/logical, foundations, "type/DF", "concept/prior-pointer-reach", "symbol/Pointer_field", "symbol/Pointer_local", status/stable]
---
# Locality and Prior — constraints within LocalReach
## Claim (formal)
Locality constrains admissible Reach paths to LocalReach neighborhoods; “prior” denotes reachable positions relative to Now under locality, tracked via field and local pointers.

## Philosophical Translation (of formal claim)
Not everything is equally “elsewhere.” What counts as prior is shaped by how change can actually move here and now.

## Clarifications / Further Context
- Field vs local pointers let us distinguish global vs subject‑centric locality.
- Locality constrains admissible priors for inference; distant points outside LocalReach should not be included in prior updates.

## Tags
#type/DF #layer/foundations #domain/logical #concept/prior-pointer-reach

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-depth-reach]]
- [[01_Statements/Definition/S-DF-localreach-topology]]
- [[01_Statements/Definition/S-DF-path-eventlet-chain]]
- [[01_Statements/Definition/S-DF-reach-relation]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-prior-pointer-reach]]
- Parents: [[01_Statements/Definition/S-DF-reach-relation]]
- Dependencies: [[01_Statements/Definition/S-DF-reach-relation]]; [[01_Statements/Definition/S-DF-pointer-structural]]
- Successors: [[01_Statements/Definition/S-DF-depth-reach]]; [[01_Statements/Definition/S-DF-locality-threshold]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

