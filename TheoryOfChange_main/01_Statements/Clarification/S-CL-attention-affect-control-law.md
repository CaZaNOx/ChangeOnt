---
id: stmt.cl-attention-affect-control-law
type: CL
title: Attention and affect act as measurable control laws with falsifiers
dependencies:
- '[[01_Statements/FoundationalTruth/S-FT-immediate-datum]]'
- '[[01_Statements/Definition/S-DF-structure-of-experience]]'
- '[[01_Statements/Definition/S-DF-prm-temporal-ops]]'
concepts:
- '[[02_Concepts/C-ontology-of-change]]'
- '[[02_Concepts/C-subject-awareness-experience]]'
parents:
- '[[01_Statements/Clarification/S-CL-change-core-axiom]]'
successors: []
symbols_used: []
sources:
- path: TheoryOfChange/00_Meta/AI_RecursiveChats_slim/AI_13_Spiral_5_Hero.md:27150-27190
flags: []
tags:
- attention
- emotion
- experiment
- stable
- type/CL
- status/stable
---

# Attention and affect act as measurable control laws with falsifiers

AI_13 makes the attention story testable: define the allocation \(A_n = \arg\max_{a\in\mathcal A} \mathbb E[\Delta \text{Stability}(R) + \lambda\,\text{InfoGain}(R) - \mu\,\text{Cost}(a)]\). Surprise drives \(\lambda\) up (exploration), mastery drives the stability term, and \(\mu\) encodes effort/switch penalties. Experimental falsifier: perturb surprise/uncertainty in a trial-by-trial prediction task, fit the three weights, and reject the model if attention/learning-rate shifts fail to match the sign predictions. The same passage operationalises “emotions” as control signals: reported affect intensity modulates meta-parameters of the update rule \(U\) (learning rates, credit assignment, exploration policy). Positive surprise should accelerate reinforcement-weighted features; frustration should accelerate error-correcting features and widen sampling. A two-armed drifting bandit—with logged prediction errors, self-reports, and fitted meta-parameters—provides the falsifier: if intensity and subsequent \(\Delta\)learning-rate are unrelated after controlling for payoffs, the coupling story dies. This keeps talk of “attention” and “emotion” on measurable levers rather than mystical states.

## Philosophical Justification
- Treating attention/affect as control laws grounds phenomenology in operational levers; aligns with structure-of-experience and temporal ops (specious present, updates).
- Falsifiers ensure the model is not rhetorical: signs must match under perturbations.

## Clarifications / Further Context
- Parameters: stability term, info gain weight λ, cost weight μ; affect modulates meta-parameters of update rule U.
- Falsifier design: drifting bandit with prediction errors, self-reports, fitted meta-parameters; reject if affect–ΔLR coupling fails after payoff controls.
- Attention/affect are measurable; avoid mystification by insisting on estimators and sign tests.

## Next Steps in Chain
- suggest: specify estimators for λ, μ, and affect–meta-parameter coupling.
- suggest: integrate with temporal ops (specious present) and broadcast nodes for end-to-end tests.

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By

<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-ontology-of-change]]; [[02_Concepts/C-subject-awareness-experience]]
- Parents: [[01_Statements/Clarification/S-CL-change-core-axiom]]
- Dependencies: [[01_Statements/FoundationalTruth/S-FT-immediate-datum]]; [[01_Statements/Definition/S-DF-structure-of-experience]]; [[01_Statements/Definition/S-DF-prm-temporal-ops]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

