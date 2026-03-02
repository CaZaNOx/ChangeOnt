# Architecture Runtime

This file describes the canonical target-state runtime architecture.

## 1. Canonical runtime backbone

The target-state runtime backbone is:

1. suite config is loaded
2. jobs are expanded
3. environment family runner is selected
4. runner constructs environment
5. runner constructs either:
   - STOA path
   - or CO path
6. select → act → feedback → update loop executes
7. required run artifacts are written
8. mode/family/suite summaries and plots are generated

## 2. CO runtime backbone

The canonical CO runtime backbone is:

1. meta-header provides prior regime frame
2. translator converts task-local input into a CO path-space update
3. current path-space fragment is assembled
4. header evaluates runtime regime
5. primitives read the fragment
6. elements emit typed structural contribution packets
7. packets fuse into group outputs
8. groups fuse with:
   - header contribution
   - meta-header contribution
   - explicit classical/STOA continuation stream
9. final CO continuation surface is produced
10. translator maps continuation surface into concrete task action
11. runner executes action
12. environment feedback is translated back into kernel update form
13. fragment updates asymmetrically
14. loop repeats

## 3. STOA runtime backbone

The canonical STOA runtime backbone is simpler:

1. runner constructs environment
2. runner constructs family-local STOA algorithm
3. runner obtains action/prediction from STOA logic
4. runner applies action to environment
5. runner updates STOA model/state
6. runner writes required artifacts

## 4. Canonical internal representation

The CO kernel must not be modeled as a flat time-indexed state vector.

The canonical internal representation is:

> a time-free, asymmetry-preserving, k-local weighted directional path-space fragment

This is the kernel-native situation model.

## 5. Boundary layers

### Environment
Defines the task-local world.

### Runner
Owns family-local execution.

### Adapter
Bridges runner-facing execution and the CO kernel path.

### Translator
Converts:
- task-local input into kernel-relevant path-space updates
- kernel continuation surfaces into concrete task actions
- task feedback back into kernel update structure

### Kernel
Operates on the internal path-space fragment.

## 6. Header and meta-header

The runtime must distinguish:

### Meta-header
Prior regime frame:
- rule stability
- prior classicality
- prior expected staticity/dynamism

### Header
Live runtime regime modulation:
- sensitivity
- reevaluation pressure
- structural cadence
- local classicality modulation
- reopening of stabilized assumptions

These are not the same thing.

## 7. Classicality

Classicality is not a primitive global truth source.

It is a regime judgment about how strongly a local domain behaves like a fixed-rule, fixed-identity, highly stabilized space.

In highly classical regimes, the final fusion may collapse strongly toward the classical/STOA continuation stream.

## 8. Asymmetry

Asymmetry is foundational.

It must be preserved in:
- internal representation
- update semantics
- at least some fusion/composition behavior

Symmetry may appear only as a local or derived special case.

## 9. Time

External time is not primitive in the kernel.

The kernel must privilege:
- order
- precedence
- path relation
- reach
- structural spacing
- deformation
- recurrence

Time-like quantities may be derived later but must not be assumed primitive.

## 10. Runtime misalignment examples

The runtime architecture is misaligned if:
- the code has multiple competing active runtime paths
- translators are bypassed or reduced to trivial state passthroughs
- the kernel is forced to think directly in final task actions
- meta-header and header are collapsed together
- classicality is treated as a global constant
- time is treated as a primitive kernel coordinate