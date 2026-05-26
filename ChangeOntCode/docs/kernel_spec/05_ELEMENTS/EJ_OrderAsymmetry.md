# EJ: Order Asymmetry
Current classification: **Investigatory**

Asymmetry is foundational, but EJ as a separate canonical bundle remains under test.

## Purpose
EJ enforces **order sensitivity** where the continuation space is non-commutative: doing A→B is not equal to B→A.

## Element Role
EJ is an element because it bundles order-related primitives and applies them as constraints/penalties on candidate continuations.

## Intended Primitive Dependencies
- P15_OrderAsymmetry (when fully realized)
- P5_TemporalOps (for sequencing context)
- P8_Loopiness (optional) for loop/order interactions

## Intended Semantic Combinators
- gated penalties
- non-commutative sequence scoring

## Outputs
Typed roles:
- **ordering constraint / penalty**

Signals (canonical):
- `EJ_Order.order_score`
- `EJ_Order.asymmetry`

## State Mutation
- none beyond optional internal EMA.

## Why this element exists
CO derives temporal/ordering structure from change, and does not assume symmetry. EJ operationalizes this as explicit order constraints.

## Element Charter
### Domain
- `history/trace`
- `probes` (order-related diagnostics)

### Codomain
- emits per-candidate order penalties or constraints.

### Invariants
- **Neutrality**: if evidence indicates order symmetry, penalties must be near zero.
- **Directionality**: if order asymmetry is present, EJ must change candidate ranking.
- **Boundedness**: penalties bounded and stable.

### Falsifiers
- EJ changes decisions in contexts where order cannot matter.
- EJ fails to matter when order asymmetry is explicitly present.

### Interaction expectations
- With **EI**: EJ constrains EI’s compositions.
- With **EC**: rupture may increase order sensitivity if identity is sequence-defined.

## Forbidden
- Must not use future information.