---
id: stmt.cl-classical-limit-falsifier
type: CL
title: Classical limit and falsifier conditions for CO agents
concepts:
- '[[02_Concepts/C-math-structures]]'
- '[[02_Concepts/C-ontology-of-change]]'
dependencies:
- '[[01_Statements/Derivation/S-DR-quantale-boolean-flattening-proof]]'
- '[[01_Statements/Definition/S-DF-prm-bend-metric]]'
- '[[01_Statements/Definition/S-DF-prm-gauge]]'
parents:
- '[[01_Statements/Definition/S-DF-prm-gauge]]'
successors: []
symbols_used:
- '[[01_Statements/SYMBOLS/Tau]]'
sources:
- path: TheoryOfChange_main/00_Meta/Context/AI_13_leads_master.txt:21
- path: TheoryOfChange_main/00_Meta/Context/AI_13_leads_master.txt:23
- path: TheoryOfChange_main/00_Meta/Context/AI_13_leads_master.txt:27
flags: []
tags:
- formal
- validation
- stable
- type/CL
- concept/math-structures
- concept/ontology-of-change
- status/stable
---

# Classical limit and falsifier conditions for CO agents

## Claim (formal)
Change Ontology agents must reduce to classical shortest-path/MDP behavior when tolerance τ → 0, gauge is flat, and base costs are stationary; failure to do so falsifies the claimed generalization. Conversely, gauge-warped behavior must exhibit the predicted phase-flip and black-hole basins when bend concentration grows; if measured exit costs do not diverge relative to entry costs under the stated inequalities, the gauge dynamics are invalid.

## Practical falsifiers / tests
- Classical reproduction: set τ≈0, flat gauge g_t≡g_∞, stationary c_0; the agent’s path choices must match Dijkstra/shortest-path or the equivalent MDP optimum. Any deviation under these settings falsifies the CO generalization claim.
- Gauge flip / basin test: place a long loop with tempting exits; track Δ_t and basin depth ρ. A finite-time sign change in Δ_t with growing ρ must appear as gauge concentrates; absence falsifies the flip mechanism.
- Black-hole construction: measure exit vs inward costs as gauge tightens; exit costs must diverge relative to inward costs. If not, update rate η or tolerance schedule is insufficient.
- Regret bound audit: for stationary costs and flat gauge, regret should match the declared bound (e.g., O(√(T log T)) + 3εT); higher regret undercuts the advantage claim.

## Next Steps in Chain
- suggest: link to [[S-DF-prm-gauge]] audit cards for test configs.
- suggest: record falsifier runs in the audit trail with τ/gauge settings.

## Tags
#type/CL #layer/validation #domain/formal #concept/math-structures #concept/ontology-of-change

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Derivation/S-DR-core-from-immediate-datum]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-math-structures]]; [[02_Concepts/C-ontology-of-change]]
- Parents: [[01_Statements/Definition/S-DF-prm-gauge]]
- Dependencies: [[01_Statements/Derivation/S-DR-quantale-boolean-flattening-proof]]; [[01_Statements/Definition/S-DF-prm-bend-metric]]; [[01_Statements/Definition/S-DF-prm-gauge]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

