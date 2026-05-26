---
id: stmt.df-time-kernel
type: DF
title: Time kernel — compressing recent history into the specious present
concepts: ["[[02_Concepts/C-ontology-of-change]]"]
dependencies: ["[[01_Statements/Definition/S-DF-prm-temporal-ops]]"]
parents: ["[[01_Statements/Definition/S-DF-prm-temporal-ops]]"]
successors: ["[[01_Statements/Definition/S-DF-global-broadcast]]"]
symbols_used: []
sources:
  - path: TheoryOfChange/00_Meta/AI_RecursiveChats_slim/AI_13_Spiral_5_Hero.md:16460-16470
flags: []
tags: [layer/operators, domain/operational, stable, definition, time, "type/DF", "concept/ontology-of-change"]
---
# Time kernel — compressing recent history into the specious present
## Claim (formal)
Define the specious present by convolving recent history with a causal, normalized kernel \(K_\tau(k)\):
```math
\bar{x}_t = \sum_{k=0}^{\infty} K_\tau(k)\, x_{t-k}, \qquad K_\tau(k) \ge 0,\; \sum_k K_\tau(k) = 1,\; \operatorname{supp}(K_\tau) \approx \tau.
```
The kernel \(K_\tau\) shapes the perceived “thickness” of now and sets how rapidly the field integrates past inputs into the current moment.

## Philosophical Translation (of formal claim)
“Now” is a weighted blur of the recent past; the kernel makes that blur explicit and tunable.

## Philosophical Justification
- [[S-DF-prm-temporal-ops]] requires depth-aware smoothing; the time kernel instantiates it for experiential integration.
- Making the kernel explicit lets us audit how “now” is constructed and how it interacts with breath/broadcast.

## Clarifications / Further Context
- Choice of \(\tau\) and kernel shape depends on task/agent; must be declared for comparability.
- Feeds global broadcast and memory trace integration.

## Next Steps in Chain
- suggest: [[S-DF-global-broadcast]]
- suggest: integrate kernel settings into audit cards.

## Tags
#type/DF #layer/operators #domain/operational #definition #time #concept/ontology-of-change #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-global-broadcast]]
- [[01_Statements/Definition/S-DF-reflection-operator]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-ontology-of-change]]
- Parents: [[01_Statements/Definition/S-DF-prm-temporal-ops]]
- Dependencies: [[01_Statements/Definition/S-DF-prm-temporal-ops]]
- Successors: [[01_Statements/Definition/S-DF-global-broadcast]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

