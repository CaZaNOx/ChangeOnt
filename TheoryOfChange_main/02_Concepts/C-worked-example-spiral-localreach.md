---
id: concept.worked-example.spiral-localreach
title: Worked Example — Spiral Adjacency in LocalReach
tags: [worked-example, spiral, LocalReach]
status: example
---
# Worked Example — Spiral Adjacency in LocalReach

Setup
- Consider a 2D lattice with LocalReach defined as Manhattan distance ≤ 1 from Now.
- Define a discrete spiral path P that winds outward one unit per full turn.

Observation
- Successive points on P (arms k and k+1) remain within small depth bands from Now over short windows; many are adjacent (distance 1), hence in LocalReach.

Implication
- Spiral adjacency provides contextual continuity: validation and identity checks can reference prior arms without long jumps.

Links
- [[01_Statements/Definition/S-DF-localreach-topology]]; [[01_Statements/Definition/S-DF-depth-reach]]; [[01_Statements/Definition/S-DF-breath-field-global-integrator]]; [[01_Statements/Corollary/S-CR-spiral-context-continuity]]

Note
- This is illustrative; continuous variants follow by taking finer lattices/metrics.















































<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

<!-- END:AUTOGEN:RELATIONSHIPS -->













































