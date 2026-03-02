# docs/kernel_spec/15_FUSION_AND_CLASSICAL_COLLAPSE.md

# Fusion and Classical Collapse

## Status
- **Binding**: hierarchical staged fusion
- **Recommended starting point**: additive, gated, and order-sensitive local fusion laws
- **Open design space**: exact thresholds and exact operator parametrization

---

## 1. Principle

The kernel does not use one universal flat fusion law.

The canonical architecture is **hierarchical staged fusion**.

Within that hierarchy, a small family of local fusion laws is allowed.

---

## 2. Canonical fusion skeleton

**Binding**

The kernel must fuse in stages:

1. primitive-derived information contributes to element packets;
2. element packets fuse into group outputs;
3. group outputs fuse with:
   - header contribution,
   - meta-header contribution,
   - explicit classical/STOA continuation stream;
4. the result is a CO-internal continuation surface;
5. the translator maps that continuation surface into task action.

---

## 3. Allowed local fusion laws

**Recommended starting point**

The canonical family of local fusion laws should be:

- **weighted additive**
- **gated selective**
- **order-sensitive sequential**

### Weighted additive
Useful in sufficiently classical or near-linear local regimes.

### Gated selective
Useful when some contributions should only matter under certain structural/regime conditions.

### Order-sensitive sequential
Useful when composition order matters and asymmetry must be preserved.

---

## 4. Classicality

**Binding**

Classicality is a regime judgment about how strongly a domain or local fragment behaves like:
- a fixed-rule,
- fixed-identity,
- highly stabilized,
- strongly classical space.

This may justify collapse toward:
- classical assumptions,
- STOA continuation streams,
- or very low CO influence.

---

## 5. Classical collapse rule

**Binding**

The kernel may collapse strongly toward classical/STOA handling when:
- meta-header prior classicality is high,
- runtime stability is high,
- reeval pressure is low,
- tension is low,
- branch-space deformation is low,
- identities/rules remain strongly stabilized.

---

## 6. Background monitoring rule

**Binding**

Even under strong classical collapse, CO should retain low-background monitoring for:
- shift alerts,
- rising tension,
- branch-space deformation,
- loss of closure,
- rising asymmetry,
- identity instability.

CO influence must be able to reopen when justified by structural change.

---

## 7. Misalignment examples

Code is misaligned with this spec if:
- all fusion is forced into one additive law,
- classicality is treated as a global constant,
- classical collapse cannot reopen,
- or final fusion omits the explicit classical/STOA continuation stream.