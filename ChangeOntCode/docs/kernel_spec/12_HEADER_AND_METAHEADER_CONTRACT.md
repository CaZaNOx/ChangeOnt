# docs/kernel_spec/12_HEADER_AND_METAHEADER_CONTRACT.md

# Header and Meta-Header Contract

## Status
- **Binding**: distinction between meta-header and header
- **Recommended starting point**: meta-header as prior regime frame, header as live regime modulation
- **Open design space**: exact threshold values, exact internal state schema
- **Experimental**: additional header families beyond canonical baseline

---

## 1. Principle

The kernel distinguishes between:

- **meta-header**
- **header**

These are not the same thing.

---

## 2. Meta-header

### Role
**Binding**

The meta-header represents **prior regime information** justified by the task or environment class.

Examples:
- fixed board size,
- fixed action schema,
- fixed game rules,
- known high classicality,
- known strong stabilization of identities/rules.

### What it does
**Binding**

The meta-header may provide:
- prior classicality expectations,
- prior rule-stability expectations,
- prior dynamism/staticity expectations,
- prior ceilings or floors on collapse toward classical handling.

### What it must not do
**Binding**

The meta-header must not be confused with:
- live local regime detection,
- per-step runtime instability response,
- or purely local dynamic modulation.

Those belong to the header.

---

## 3. Header

### Role
**Binding**

The header is the **live runtime regime interpreter**.

It evaluates:
- whether current local structure appears stable or shifting,
- whether local assumptions remain trustworthy,
- how sensitive the kernel should be,
- how often reevaluation should happen,
- how justified local classical collapse is right now.

### What it controls
**Recommended starting point**

The header may control:
- local classicality modulation,
- reevaluation pressure,
- structural cadence,
- local regime labels,
- gating or attenuation of certain fusion pathways.

### What it must not assume
**Binding**

The header must not smuggle external time as primitive cadence.

Cadence must be structural:
- every advance,
- every k advances,
- instability-triggered,
- shift-triggered,
- closure-break-triggered,
- or similar structurally justified rules.

---

## 4. Distinction summary

**Binding**

Meta-header:
- prior regime frame

Header:
- live local regime modulation

Meta-header is not a substitute for header.
Header is not a substitute for meta-header.

---

## 5. Classicality

**Binding**

Classicality is a regime judgment, not a primitive global truth.

A domain or local fragment may justify strong classical handling when:
- rules are fixed,
- identities are stable,
- branch-space is strongly constrained,
- deformation is low,
- reevaluation pressure is low.

In such regimes, the header and meta-header may jointly allow strong collapse toward classical/STOA handling.

---

## 6. Reopening rule

**Binding**

A previously stabilized local regime must be reopenable when structural evidence changes.

Examples of reopening signals:
- rising reeval pressure,
- loss of closure,
- rising tension,
- unexpected asymmetry,
- meaningful branch-space deformation,
- local identity instability.

---

## 7. Misalignment examples

Code is misaligned with this spec if:
- meta-header and header are collapsed into one vague controller,
- header uses external time as primitive cadence,
- classicality is treated as a global constant,
- or stabilized assumptions cannot be reopened under structural shifts.