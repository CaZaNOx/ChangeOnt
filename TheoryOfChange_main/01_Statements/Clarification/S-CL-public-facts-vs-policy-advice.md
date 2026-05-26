---
id: stmt.public-facts-vs-policy-advice
type: CL
aliases:
- S-CL-public-facts-vs-policy-advice
- PublicFactPolicyBoundary
- PublicTransitionGrammar
title: Public facts versus policy advice
concepts:
- '[[02_Concepts/C-boundary]]'
dependencies:
- '[[01_Statements/02_Outer_Formation/012_S-DF-continuation-admissibility.md]]'
- '[[01_Statements/02_Outer_Formation/014_S-DF-remaining-transformation-burden.md]]'
parents:
- '[[01_Statements/02_Outer_Formation/012_S-DF-continuation-admissibility.md]]'
successors:
- '[[../ChangeOntCode/docs/kernel_spec/16_TRANSLATOR_BOUNDARY_CONTRACT.md]]'
- '[[../ChangeOntCode/docs/kernel_spec/77_PUBLIC_BURDEN_EFFECT_SCHEMA.md]]'
- '[[../ChangeOntCode/docs/kernel_spec/80_KERNEL_SIDE_RELATION_SURFACE_CONTRACT.md]]'
symbols_used: []
flags:
- leakage-boundary
tags:
- layer/foundations
- domain/operational
- type/CL
- concept/translator-boundary
- concept/public-fact
- concept/kernel-bridge
status: canonical-scaffold
---
# Public facts versus policy advice

## Claim
A public fact describes the lawful transformation grammar or observable effect structure of a problem. Policy advice ranks or selects continuations by expected success, hidden value, optimality, or future reward.

The kernel may use public facts to derive burden/effect relations. It may not receive policy advice through the translator or adapter and then call it CO reasoning.

## Allowed public facts
Allowed facts include:

- a legal move exists or is prohibited;
- a wall blocks a transition;
- sampling can reduce uncertainty about the sampled option;
- inspection can reduce hiddenness;
- repair can reduce degradation under public dynamics;
- replacement resets a public state class;
- an action consumes a public resource or time budget;
- an observation is stale or fresh under public history.

These facts describe transformation grammar or observable effect structure.

## Forbidden policy advice
Forbidden facts include:

- this action is optimal now;
- this action has highest DP value;
- this route is shortest using hidden map information;
- repair is correct because hidden health is below threshold;
- sample this arm because it is the true best arm;
- replace now because the benchmark baseline would do so.

These are strategic rankings or hidden-state evaluations.

## Boundary rule
Adapters may publish public transition/effect facts. The kernel-side RelationSurface derives continuation identities and relations from those facts. Adapters should not publish final branch-relation conclusions when those conclusions depend on strategic evaluation rather than public grammar.

## Grey zone
Some facts are public but still strategically useful. That is allowed. A fact becomes forbidden only when it encodes an optimality verdict, hidden-state read, baseline policy, or future reward ranking rather than a lawful effect relation.

## Tags
#type/CL #layer/foundations #domain/operational #concept/translator-boundary #concept/public-fact #concept/kernel-bridge #status/canonical-scaffold
