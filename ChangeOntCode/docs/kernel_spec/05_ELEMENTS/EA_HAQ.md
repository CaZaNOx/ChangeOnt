# EA_HAQ
Current classification: **Provisional**

Meaningful active element on the default path, but still depends on evolving upstream theory anchors.

## What this element is
EA_HAQ is the kernel’s history-adaptive gauge modulation element. Its role is to modulate continuation preference by combining:
- present change pressure,
- gauge adaptation,
- bounded history,
- and local defect/warp signals.

It is not just “novelty detection.” It is the element that asks whether the local field should be read as needing stronger adaptation, stronger warping, or stronger caution.

## Why this element exists
A change-first kernel cannot treat all local deviations as equal. Some deviations indicate:
- harmless fluctuation,
- some indicate build-up of deformation pressure,
- some indicate that the current local gauge is itself misfitted.

EA_HAQ exists to coordinate those factors into one modulation surface.

## What EA_HAQ is not
EA_HAQ is not:
- a primitive,
- the final action chooser,
- or a hidden family-specific solver.

It is a doctrine-level modulation element built from lower-level signals.

## Intended upstream support
Primary:
- P2 Gauge

Secondary/supporting:
- P1 BendMetric or equivalent surprise source
- P5 TemporalOps or equivalent history shaping
- bounded visible history support from the translated packet

## Inputs
Typical packet inputs include:
- `history`
- `trace`
- `signals.z_PE`
- `signals.z_gain`
- `signals.var_resid`
- gauge state from P2

## Outputs
Typical bus outputs include:
- `EA_HAQ.novelty`
- `EA_HAQ.holonomy_defect`
- `EA_HAQ.gauge_gain`
- `EA_HAQ.modulated_pe`
- `EA_HAQ.modulated_gain`
- `EA_HAQ.warp_strength`

The element should affect later continuation preference, but it should not directly choose the final task action.

## Why the doc stresses this
Earlier versions of the project let HAQ collapse into “one novelty scalar.” That underdescribed its role. The current description is meant to preserve the stronger idea: HAQ is a change-sensitive modulation surface, not a log of surprise.

## Current status
Real runtime component with a meaningful role. Still depends on some evolving upstream theory anchors, but content-wise the element is clear enough to explain and implement honestly.