# Kernel Spec Index

## Table of Contents
1. `01_KERNEL_RUNTIME.md`
2. `02_DATA_CONTRACTS.md`
3. `03_WIRING_MAP.md`
4. `04_PRIMITIVES/`
5. `05_ELEMENTS/`
6. `06_HEADERS/`
7. `07_COMBINATORS/`
8. `08_TRANSLATORS/`
9. `09_ACCEPTANCE/`

## Docs -> Code Rule
- These kernel specs are **binding** and must match the runtime implemented under `ChangeOntCode/agents/co/` and `ChangeOntCode/experiments/`.
- If a spec conflicts with code, update code to comply or add a TODO in `09_ACCEPTANCE/SPEC_GAPS.md` describing the mismatch and required decision.

## Implementation Order (Recommended)
1. `07_COMBINATORS/C_Pipeline.md` (defines canonical runtime and update semantics)
2. `02_DATA_CONTRACTS.md` (observation/mask/signal contracts)
3. `05_ELEMENTS/ActionHead.md` (final action + telemetry surface)
4. `05_ELEMENTS/EC_Identity.md` and `05_ELEMENTS/EB_GHVC.md` (required signals)
5. `04_PRIMITIVES/P1_BendMetric.md`, `P12_ClosureQuotient.md`, `P10_ChangeOpsCore.md` (support identity + GHVC state)
6. `08_TRANSLATORS/*` (family-specific scoring and masks)
7. Remaining elements/primitives/headers

