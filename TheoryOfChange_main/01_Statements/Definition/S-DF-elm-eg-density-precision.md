---
id: stmt.elm-eg-density-precision
type: DF
aliases: ["ELM.EG.DensityPrecision"]
title: Element — EG — Density/Precision (r′ scheduler)
concepts: ["[[02_Concepts/C-ontology-of-change]]"]
dependencies: ["[[01_Statements/Definition/S-DF-prm-precision-density]]", "[[01_Statements/Definition/S-DF-prm-temporal-ops]]"]
parents: ["[[01_Statements/Definition/S-DF-prm-precision-density]]"]
successors: []
symbols_used: []
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:5628
flags: []
tags: [layer/operators, domain/operational, element, control, precision, "type/DF", "concept/ontology-of-change"]
---
# Element — EG — Density/Precision (r′ scheduler)
## Claim (formal)
Emit r′ (effective precision) from surprise/phase schedule with depth‑aware smoothing; provides a knob for information density.

## Philosophical Translation (of formal claim)
Tighten or loosen your grip when it helps most.

## Philosophical Justification
Information is not free: higher precision costs attention and risks over‑fitting to noise; lower precision saves resources but can miss signal. Surprise and breath phase provide natural cues for scheduling r′, making precision adaptive to context.

## Derivation (Philosophical)
- Surprise and phase do not merely affect belief; they affect how finely the field should be sampled.
- Precision/density is the primitive knob.
- EG is the element that turns that knob into an explicit scheduling policy.

## Derivation (Formal/Logical/Mathematical)
```text
r'_t := schedule(surprise_t, phase_t; EMA)
```
with EMA smoothing to prevent jitter.

## Explanation (informal)
EG is the element that tightens or loosens how finely the kernel resolves structure. It is the practical face of precision scheduling.

## Clarifications / Further Context
- Couple to attention maps so precision is applied where it matters.
- Decay parameters should align with breath and depth to avoid thrash.

## Next Steps in Chain
- Validate schedules on benchmark tasks; measure SNR and outcome quality.

## Tags
#type/DF #layer/operators #domain/operational #element #control #precision #concept/ontology-of-change

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-prm-precision-density]]
- [[01_Statements/Definition/S-DF-prm-temporal-ops]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-ontology-of-change]]
- Parents: [[01_Statements/Definition/S-DF-prm-precision-density]]
- Dependencies: [[01_Statements/Definition/S-DF-prm-precision-density]]; [[01_Statements/Definition/S-DF-prm-temporal-ops]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

