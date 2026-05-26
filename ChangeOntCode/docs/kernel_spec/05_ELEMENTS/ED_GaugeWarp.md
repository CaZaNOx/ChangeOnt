# ED: GaugeWarp
Current classification: **Provisional**

Plausible doctrine-level warp element, but not part of the strongest canonical kernel slice.

## Purpose
ED applies **local transport/metric warping** to the continuation field using gauge/alignment structure.

ED exists to separate:
- **EA**: detect/learn change-pressure and frame misalignment (salience/gradient)
- **ED**: *apply* a transport warp to candidate evaluation based on current alignment.

## Element Role
ED is an **element** (not a primitive) because it bundles multiple primitives into one doctrine-level warp operator.

## Intended Primitive Dependencies
- P2_Gauge (alignment / transport gain)
- P1_BendMetric (optional) for warp intensity under deformation
- P5_TemporalOps (optional) for smoothing

## Intended Semantic Combinators
- multiplicative coupling: apply gain as warp
- gated blend: warp should be neutral when alignment is stable

## Outputs
Typed roles:
- **transport/gauge warp** (primary)

Signals (canonical):
- `ED_GaugeWarp.gain`
- `ED_GaugeWarp.warp_strength`

## State Mutation
- May update internal gauge state (through P2 state).
- Must not mutate environment topology.

## Why this element exists
CO claims continuation is evaluated in a **local frame** and that alignment/transport matters. ED operationalizes this as a warp on candidate evaluation.

## Element Charter
### Domain
Consumes standard packet fields:
- `signals` (z_PE, z_gain, var_resid) when provided
- `memory_view` (family summaries)

### Codomain
Emits a **transport warp** deformation that modulates candidate scores.

### Invariants
- **Neutrality**: if alignment is stable (low z_PE) then warp strength should be near neutral.
- **Monotonicity**: higher misalignment (z_PE) should not reduce warp strength (unless gated off explicitly).
- **Boundedness**: warp strength must be finite and clampable.

### Falsifiers
- ED changes rankings under stable alignment with no evidence of drift.
- ED produces unbounded warps or NaNs.

### Interaction expectations
- With **EC**: continuity should gate warp aggressiveness (high continuity => gentler warp).
- With **EA**: ED should not duplicate EA’s salience; it should apply transport after EA detects pressure.

## Forbidden
- Must not choose final actions.
- Must not peek hidden simulator state.