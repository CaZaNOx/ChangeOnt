
# Translator Boundary Contract

## Purpose

The translator exposes the public lawful problem specification in a generic form the kernel can consume.
It does **not** solve the problem and it does **not** derive the shape prior.

## The translator may provide only public/parity-honest information
Allowed examples:
- start state / task anchor / win condition
- legal actions
- prohibited actions
- public transition rules
- public exceptions
- public rewards/costs if the environment exposes them
- visible updates after each step

The translator may use only information that a parity-honest STOA baseline could also receive
from the same environment.

## The translator may not provide
Forbidden examples:
- best-next-step hints
- shortest-path rankings
- arm rankings
- hidden simulator internals unavailable to baselines
- family-private strategy labels disguised as public fields
- near-final policy advice under the name of translation

## Relationship to shape derivation
The translator is not the regime-analysis layer.
It publishes the lawful/public problem facts; the placement layer separately derives the
six-question shape prior from those public facts and the visible stream.
