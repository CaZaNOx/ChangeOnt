# Canonical Translator / Adapter Contract

This folder states the active boundary/adapter contract for the current kernel phase. The contract is problem-family agnostic.

## Target state

A boundary / adapter may expose only lawful public structure:

- current public observation;
- legal native actions or candidate expressions;
- task / continuation anchor;
- public hiddenness or visibility status;
- public burden/effect facts such as `reduces_hiddenness`, `carries_degradation`, `blocks_transition`, `resets_condition`, or `reduces_uncertainty`;
- public admissibility constraints and masks when they are part of the native problem grammar.

The adapter must not expose policy conclusions:

- no optimal-action labels;
- no baseline value or DP/Q estimates;
- no shortest-path answer in hidden or partial settings;
- no hidden-state action hints;
- no first-legal, uniform, greedy, or family-local rescue path.

If public structure is missing or malformed, the canonical CO path must fail closed under `78_RUNTIME_SAFETY_AND_FALLBACK_CONTRACT.md`. It must not invent scores or select a native action.

## Relation to kernel

The adapter publishes public facts. The kernel derives continuation identities, burden operations, relations, field state, collapse certificates, and readout.

Primary references: `16_TRANSLATOR_BOUNDARY_CONTRACT.md`, `77_PUBLIC_BURDEN_EFFECT_SCHEMA.md`, `88_ADAPTER_PUBLIC_EFFECT_RELATION_COVERAGE.md`, and `95_KERNEL_STRUCTURE_CARRIER_ALIGNMENT.md`.
