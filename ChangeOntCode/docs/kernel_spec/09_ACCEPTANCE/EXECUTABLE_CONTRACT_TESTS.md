# Executable Contract Tests

This folder defines **acceptance gates** that enforce that code reflects the docs.

CO is treated as a **truth-claim** framework; therefore the primary acceptance gates are:
- **coherence / law / invariant tests** (not just performance)
- **parity honesty checks**
- **no silent fallback** in strict mode

## Tests

### Primitive law/invariant tests

Run:

```bash
cd ChangeOntCode
python -m agents.co.tests.law_invariants
```

These enforce the Primitive Charters for core primitives (v1):
- P1 BendMetric
- P2 Gauge
- P11 Residuation

### Element invariant tests

Run:

```bash
cd ChangeOntCode
python -m agents.co.tests.element_invariants
```

These enforce the Element Charters for core elements (v1):
- EA (monotone response to change pressure; bounded novelty)
- EC (continuity decreases with mismatch; bounds)
- EB (no free birth under low pressure / non-positive MDL gain)

## Strictness

By default tests are strict (fail nonzero).

- `CO_STRICT_LAWS=0` prints failures but exits 0.
- `CO_STRICT_ELEMENTS=0` prints failures but exits 0.

Strict mode is intended for CI and for “docs-first” development.
