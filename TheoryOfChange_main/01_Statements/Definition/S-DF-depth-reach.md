---
id: stmt.depth-reach
type: DF
aliases: ["FND_4.Depth"]
title: Depth — minimal reach distance to Now
concepts: ["[[02_Concepts/C-prior-pointer-reach]]"]
dependencies: ["[[01_Statements/02_Outer_Formation/006_S-DF-reach-relation]]", "[[01_Statements/02_Outer_Formation/008_S-DF-asymmetric-local-contribution]]"]
parents: ["[[01_Statements/02_Outer_Formation/008_S-DF-asymmetric-local-contribution]]"]
successors: []
symbols_used: []
sources:
  - path: TheoryOfChange/02_Foundations/FND_4_ReachingAndDepth.md:1
flags: []
tags: [layer/foundations, domain/logical, foundations, stable, "type/DF", "concept/prior-pointer-reach"]
---
# Depth — minimal reach distance to Now
## Claim (formal)
Depth(p; Now) := minimal length of Reach path from p to Now; provides a partial order for priors and supports neighborhood layering.

## Philosophical Translation (of formal claim)
Some priors are “closer” than others — depth makes that precise without a clock.

## Philosophical Justification
- [[S-DF-reach-relation]] defines adjacency; layering those adjacencies gives a neutral order without external time.
- Asymmetric local contribution ([[S-DF-asymmetric-local-contribution]]) provides the weaker local asymmetry needed for nearby anchors to matter more directly; depth is the constructive mechanism.
- SE/noise thresholds need a principled notion of “distance” so audits are not arbitrary.

## Derivation (Philosophical)
- Fix LocalReach and admissible path metric (cost, hop count, breath-weighted).
- Define Depth(p) = min_{paths p→Now} length(path).
- Show this induces nested neighborhoods used for thresholds and pointer stability.

## Clarifications / Further Context
- Depth works with LocalReach; can inform thresholds, SE windows, and pointer stability.
- Declare the path family/locality constraints used to compute depth; otherwise comparisons are ambiguous.
- Depth is frame- and window-dependent; Tx changes may alter computed depth.
- If multiple minimal paths exist, specify tie-break rules or treat depth as a set-valued relation.

## Next Steps in Chain
- suggest: [[S-DF-prm-depth-breadth-flip]]
- suggest: [[S-CL-time-noise-thresholds]]

## Explanation (informal)
Depth turns mere reachability into an ordered neighborhood structure. It does not assume clock time; it measures how many admissible continuation steps, or how much admissible cost, separates a prior from the present.

## Derivation (Formal/Logical/Mathematical)
```text
Depth(p; Now) := min { Length(π) | π is an admissible Reach-path from p to Now }
Neighborhood_k(Now) := { p | Depth(p; Now) ≤ k }
```
If admissible path length is cost-weighted rather than hop-counted, replace `Length(π)` with the declared cost functional.

## Tags
#type/DF #layer/foundations #domain/logical #concept/prior-pointer-reach #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Clarification/S-CL-time-noise-thresholds]]
- [[01_Statements/Definition/S-DF-prm-depth-breadth-flip]]
- [[01_Statements/Definition/S-DF-prm-temporal-ops]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-prior-pointer-reach]]
- Parents: [[01_Statements/02_Outer_Formation/008_S-DF-asymmetric-local-contribution]]
- Dependencies: [[01_Statements/02_Outer_Formation/006_S-DF-reach-relation]]; [[01_Statements/02_Outer_Formation/008_S-DF-asymmetric-local-contribution]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

