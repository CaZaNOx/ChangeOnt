# docs/code_reference/agents/co/core/elements.md

# CO Elements

## Purpose

Elements are mechanism families built from primitives, combinators, and weights.

They are not just feature collectors.  
They are structured mechanism forms that emit typed structural contribution packets.

---

## Why they exist

Elements let the kernel take multiple distinct stances toward unfolding.

Examples:
- adaptive fit
- residual/tension interpretation
- persistence-through-change
- density/precision
- compressibility
- breadth vs depth
- routing/regime interpretation
- change-operator interpretation
- order asymmetry interpretation

---

## General contract

**Binding**

Every element should have:
- a clear conceptual role,
- documented primitive dependencies,
- documented runtime status,
- and an honest contribution packet behavior.

If an element exists in docs/configs but cannot be meaningfully exercised in runtime, that is a misalignment.

---

## Element files and intended meanings

### `EA_HAQ.py`
#### Meaning
Adaptive-fit / gauge-like adjustment mechanism.

#### Why needed
Interprets local structural fit and mismatch reduction.

#### Status guidance
- likely **core canonical**
- parameter fidelity must be real if EA sweeps are to be honest

---

### `EB_GHVC.py`
#### Meaning
Residual/tension/pressure-sensitive mechanism.

#### Why needed
Interprets unresolved structural inconsistency, pressure, or residual deformation.

#### Status guidance
- likely **core canonical**
- should not be starved of the signals it conceptually depends on

---

### `EC_Identity.py`
#### Meaning
Persistence-through-change / identity-across-deformation mechanism.

#### Why needed
Tracks stabilized continuity without assuming static identity as primitive.

#### Status guidance
- likely **core canonical**

---

### `EG_DensityPrecision.py`
#### Meaning
Local packedness / revisitation / precision-of-local-structure mechanism.

#### Why needed
Useful for local path-space crowding and spatial recurrence.

#### Status guidance
- likely part of the core baseline set in at least one density/precision form

---

### `EE_Compressibility.py`
#### Meaning
Compressibility / pattern economy interpretation at the element level.

#### Why needed
Supports stronger explicit compressibility-sensitive mechanism forms.

#### Status guidance
- **canonical optional extension** unless promoted further

---

### `EF_Router.py`
#### Meaning
Routing/regime-sensitive mechanism, possibly probe-sensitive.

#### Why needed
Useful for richer regime selection or mechanism routing.

#### Status guidance
- **canonical optional extension** unless promoted further

---

### `EH_BreadthDepth.py`
#### Meaning
Tradeoff between widening exploration and deepening continuation.

#### Why needed
Supports path-space branch management and continuation strategy control.

#### Status guidance
- **canonical optional extension**

---

### `EI_ChangeOps.py`
#### Meaning
Higher-order interpretation of change-operator structure.

#### Why needed
Supports reasoning about change composition itself.

#### Status guidance
- **canonical optional extension**

---

### `EJ_OrderAsymmetry.py`
#### Meaning
Explicit asymmetry-sensitive mechanism.

#### Why needed
Supports directional/path-sensitive judgments.

#### Status guidance
- may remain **canonical optional extension**
- asymmetry itself remains foundational independent of this element

---

### `ED_GaugeWarp.py`
#### Meaning
Warp-like gauge reinterpretation mechanism.

#### Why needed
Potentially richer metric/warp adaptation.

#### Status guidance
- **experimental** unless fully integrated and contract-clean

---

### `E0_VoteBridge.py`
#### Meaning
Bridge from local mechanism outputs into shared continuation-vote space.

#### Why needed
Lets element-level structure become part of higher-level decision/fusion processing.

#### Status guidance
- likely **core canonical support mechanism**

---

### `action_head.py`
#### Meaning
Final continuation/fusion head.

#### Why needed
Produces the final internal continuation surface before translator-side collapse into task action.

#### Status guidance
- **core canonical**
- must faithfully implement documented fusion and classical collapse semantics

---

## Packet rule reminder

**Binding**

Elements are expected to emit typed structural contribution packets.

They must not all be reduced to “return one float” if that destroys their actual role.

---

## Misalignment examples

Element documentation is incomplete or code is misaligned if:
- element names exist but their conceptual role is unclear,
- element packets are not honest or are flattened incorrectly,
- an element is configured but starved of required structure,
- or an experimental element appears in baseline `CO_full` without justification.