---
id: stmt.descriptor-guided-predictive-deformation
type: DF
aliases:
- DescriptorGuidedDeformation
- PredictiveCrossoverProtocol
title: Descriptor-guided predictive deformation — problem movement should predict configuration crossover
concepts:
- '[[02_Concepts/C-recursive-truth]]'
- '[[02_Concepts/C-ontology-of-change]]'
dependencies:
- '[[01_Statements/Definition/S-DF-change-benchmark-protocol]]'
- '[[01_Statements/Definition/S-DF-hdr-meta]]'
- '[[01_Statements/Definition/S-DF-hdr-common]]'
- '[[01_Statements/Definition/S-DF-stabilization-target-scope]]'
parents:
- '[[01_Statements/Definition/S-DF-stabilization-target-scope]]'
- '[[01_Statements/Definition/S-DF-change-benchmark-protocol]]'
successors:
- '[[01_Statements/Definition/S-DF-candidate-surface]]'
- '[[01_Statements/Definition/S-DF-commitment-surface]]'
symbols_used: []
sources:
- path: TheoryOfChange_main/00_Meta/THEORY_TO_EXPERIMENT_GATE_PASS87L.md
- path: ChangeOntCode/docs/kernel_spec/44_CANONICAL_CANDIDATE_SURFACE.md
- path: chat/2026-04-08 clarification that a general regime-space claim must predict ranking reversals under controlled problem deformation rather than merely narrating benchmark differences after the fact
flags: []
tags:
- layer/operators
- domain/operational
- type/DF
- status/stable
- bridge
- experiment
- prediction
chain_status_band: bridge-provisional
chain_status_note: The predictive-deformation requirement is the correct experimental consequence of a general descriptor law, but the actual descriptor axes and executable mapping remain provisional.
---
# Descriptor-guided predictive deformation — problem movement should predict configuration crossover
## Claim (formal)
If a general descriptor law is real, then controlled deformation of a problem should move the problem's descriptor position in a predictable way, and that movement should predict a corresponding change in which kernel posture or configuration performs better. A descriptor law that only explains outcomes after the run has not yet earned its status.

## Philosophical Translation (of formal claim)
A genuine regime description should do more than rename known benchmarks. It should let us say in advance: this problem sits here, this configuration is shaped for that region, and if we deform the problem along this structural axis, the favored configuration should shift accordingly.

## Philosophical Justification
[[01_Statements/Definition/S-DF-change-benchmark-protocol]] already requires that benchmarking remain honest and not collapse into theater. [[01_Statements/Definition/S-DF-hdr-meta]] and [[01_Statements/Definition/S-DF-hdr-common]] justify that local problems arise inside inherited structural priors while still requiring live regime estimation. [[01_Statements/Definition/S-DF-stabilization-target-scope]] adds that what is being stabilized can differ in kind. If these doctrines are to amount to a genuine problem-agnostic law rather than a family glossary, then they must support counterfactual prediction under controlled deformation. Otherwise the descriptor layer would merely redescribe solved cases rather than constrain future behavior.

## Explanation (informal)
Suppose two kernel postures differ: one hardens early and reopens reluctantly; the other stays tentative longer and reopens more easily. A descriptor law should let us predict where each posture should win. If we then make the problem more confusable, more rapidly deforming, or more costly to mis-harden, the predicted advantage should move. That ranking shift is the real evidence that the descriptor means something.

## Derivation (Philosophical)
- A general descriptor law claims to classify problems by structural regime rather than by benchmark name.
- Such a classification is meaningful only if it constrains expected solver behavior.
- Controlled deformation changes the local problem structure while preserving comparability.
- Therefore a real descriptor law should predict how configuration advantage shifts under such deformation.
- If no such pre-run prediction is possible, the purported descriptor remains classificatory rhetoric rather than an earned law.

## Derivation (Formal/Logical/Mathematical)
```text
Given problem P with descriptor D(P) and configurations C1, C2,
if D(P) predicts rank(C1, C2 | P),
and deformation τ moves P to P' with descriptor D(P'),
then the law should predict whether rank(C1, C2 | P') is preserved, weakened, or reversed.

Minimal earned case:
  D(P1) ⇒ C1 > C2
  τ(P1)=P2 and D(P2) shifts along a stated axis
  D(P2) ⇒ C2 > C1
```

## Clarifications / Further Context
- This file does **not** claim the current repo already has the right descriptor space.
- It states the minimum experimental consequence that any serious candidate descriptor law must satisfy.
- The relevant configurations are kernel postures over a shared skeleton, not unrelated benchmark-specialized algorithms.
- The deformation should be structural and parity-honest, not answer-bearing or hand-curated to rescue a preferred configuration.

## Next Steps in Chain
- suggest: [[01_Statements/Definition/S-DF-candidate-surface]]
- suggest: [[01_Statements/Definition/S-DF-commitment-surface]]

## Active-chain status
Band: bridge-provisional.
The predictive requirement is strong and necessary, but the present repository still has to earn it by specifying descriptor axes and running controlled deformation tests.

## Tags
#type/DF #layer/operators #domain/operational #bridge #experiment #prediction #status/stable
