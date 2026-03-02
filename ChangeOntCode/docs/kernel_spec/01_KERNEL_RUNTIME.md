# Kernel Runtime

This file describes the canonical target-state runtime behavior of the CO kernel itself.

It should be read together with:
- `01A_ARCHITECTURE_DOCTRINE.md`
- `03_WIRING_MAP.md`
- `11_INTERNAL_REPRESENTATION.md`
- `12_HEADER_AND_METAHEADER_CONTRACT.md`
- `14_ELEMENT_CONTRIBUTION_PACKET.md`
- `15_FUSION_AND_CLASSICAL_COLLAPSE.md`
- `16_TRANSLATOR_BOUNDARY_CONTRACT.md`

## 1. Runtime principle

The CO kernel is not a flat policy function over static state.

The runtime must preserve:

- change-first interpretation
- path-based internal structure
- time-free ordered unfolding
- asymmetry
- staged contribution and fusion behavior
- explicit translator boundaries

## 2. Canonical runtime object

The kernel’s native runtime object is:

> a **k-local weighted directional path-space fragment**

This fragment is:
- time-free
- order-based
- asymmetry-preserving
- branch-space-aware
- structurally profiled

It is the kernel’s internal “situation” object.

## 3. Canonical runtime stages

The canonical runtime stages are:

1. **meta-header prior frame exists**
2. **translator supplies path-space update**
3. **current fragment is assembled**
4. **header evaluates live regime**
5. **primitives read the fragment**
6. **elements emit typed structural contribution packets**
7. **element packets fuse into group outputs**
8. **group outputs fuse with**:
   - header contribution
   - meta-header contribution
   - explicit classical/STOA continuation stream
9. **final continuation surface is produced**
10. **translator collapses continuation surface into task action**
11. **environment feedback is translated back into update form**
12. **fragment updates asymmetrically**
13. **loop repeats**

## 4. Runtime separation of concerns

### Meta-header
Provides prior regime information:
- rule stability
- prior classicality
- prior expected dynamism/staticity

### Header
Provides live local regime interpretation:
- sensitivity
- reevaluation pressure
- cadence
- local classicality modulation
- reopening of stabilized assumptions

### Primitives
Read structural aspects of the fragment.

### Elements
Emit typed structural contribution packets.

### Groups
Fuse multiple elements into higher-order mechanism outputs.

### Final fusion
Combines groups with header/meta-header/classical stream.

### Translator
Maps between task-local structure and kernel-internal structure.

## 5. Continuation surface

The kernel’s final internal runtime output is not yet a concrete task action.

It is a **continuation surface**:
- weighted continuation preferences
- branch-local constraints
- confidence
- partial preselection where relevant
- residual ambiguity where relevant

The translator is the legitimate collapse point into concrete task action.

## 6. Select/update rule

**Binding**

The runtime must preserve a real distinction between:

### Select path
Produces continuation/action-relevant structure.

### Update path
Integrates feedback and changes internal state without pretending to be another select pass.

This is especially important for:
- avoiding double mutation
- keeping cadence and regime interpretation honest
- preventing hidden semantic drift

## 7. Asymmetry rule

**Binding**

Asymmetry is fundamental in runtime behavior.

This means:
- prior remains prior
- current grows from prior
- update is directional
- return is not identical to reversal
- order-sensitive composition is allowed where justified

A runtime that treats the kernel as fundamentally symmetric is misaligned.

## 8. Time rule

**Binding**

External time is not primitive in kernel runtime.

The runtime should track:
- order rank
- precedence
- path depth
- reach
- structural separation
- recurrence span
- stabilization persistence

but not treat elapsed time as a primitive kernel axis.

## 9. Classical collapse in runtime

**Binding**

The runtime must allow:
- strong classical collapse in highly classical/frozen regimes
- but also low-background monitoring for shifts

So the runtime must support both:
- near-total classical dominance when justified
- and reopening of CO influence when deformation/tension/instability rises

## 10. Runtime misalignment examples

The kernel runtime is misaligned if:
- it is effectively a flat task-state policy
- translators are bypassed or trivialized
- contribution packets are flattened into one forced scalar too early
- select and update are not really separated
- asymmetry is erased
- time is treated as primitive
- classicality is global instead of regime-conditioned
- the continuation surface is bypassed and replaced with raw final task tokens inside the kernel