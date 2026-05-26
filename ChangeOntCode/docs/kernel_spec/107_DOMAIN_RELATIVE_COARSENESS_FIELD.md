# 107 — Domain-Relative Coarseness Field

## Status
First-pass contract / implemented as bounded telemetry in `DynamicShapeField`.

## Purpose
The earlier scalar `coarseness_radius` was a useful first-pass compression, but it is conceptually too thin. CO-space is not resolved equally along every active invariant. The kernel should therefore preserve a bounded domain-relative coarseness profile where domains are earned by public relation/burden evidence.

## Required distinction

- Global coarseness: fallback coarseness when no domain-specific evidence exists.
- Domain coarseness: retained resolution for an active public relation/burden domain.

Domain coarseness is not a problem-specific feature vector. Allowed domain sources include only:

- `relation_field_domain`;
- public burden type;
- public relation scope;
- hiddenness/exposure domain;
- admissibility/sequence domains if surfaced as public relation/burden facts.

Forbidden sources:

- family name;
- native action name;
- hidden state;
- reward hindsight;
- DP/baseline values;
- post-hoc performance success.

## Runtime contract
`DynamicShapeField` may expose:

- `coarseness_radius` — global fallback;
- `coarseness_by_domain` — bounded active public-domain map;
- row telemetry `dynamic_shape_domain_coarseness`;
- effective-control summaries `dynamic_shape_domain_coarseness_avg`, `dynamic_shape_domain_coarseness_min`, `dynamic_shape_domain_coarseness_count`.

The field must not choose an action. It may only affect subsequent gauge/control interpretation and telemetry.

## Expected behavior

1. If two domains carry different public ambiguity/burden profiles, their coarseness values may diverge.
2. Function-like concentrated domains may become coarser, if collapse is otherwise lawful.
3. Ambiguous, high-burden, hidden, or grey domains should become finer / less collapsed.
4. If no public domain exists, only the global fallback is used.
5. The domain map remains bounded to observed public domains; it must not accumulate arbitrary dimensions.

## Evidence status
This is a first-pass implementation of a conceptually required refinement. It is not a final metric theory and should be tested in configuration/causal audits before being used for performance claims.
