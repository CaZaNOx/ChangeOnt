# Data Contracts

This file defines the target-state data contracts that connect the kernel runtime layers.

The purpose is to make explicit:
- what kinds of structures exist,
- what each layer may emit or consume,
- and where code misalignment should be detectable.

It should be read together with:
- `11_INTERNAL_REPRESENTATION.md`
- `14_ELEMENT_CONTRIBUTION_PACKET.md`
- `16_TRANSLATOR_BOUNDARY_CONTRACT.md`

## 1. Principle

The kernel should not rely on ad hoc undocumented dict shapes.

The project must converge toward explicit data contracts for:
- path-space fragments
- element contribution packets
- continuation surfaces
- translator input/output/update structures
- run/suite artifact shapes

## 2. Canonical internal kernel data object

The kernel’s canonical internal runtime object is the:

> **k-local weighted directional path-space fragment**

### Required structural areas
The fragment should contain, at minimum:

#### Anchoring/order
- `now_ref`
- `anchor_id`
- `prior_refs`
- `k_window`
- `path_depth`

#### Realized local segment
- `realized_segment`

Each realized entry should include:
- `from_ref`
- `to_ref`
- `action_ref` if relevant
- `order_rank`
- `transition_weight`
- `bend_local`
- `delta_signature`

#### Local branch-space
- `branch_space`

Each branch candidate should include:
- `candidate_ref`
- `parent_ref`
- `branch_weight`
- `selection_bias`
- `constraint_status`

#### Structural profiles
- `bend_profile`
- `loop_profile`
- `closure_profile`
- `density_profile`
- `asymmetry_profile`
- `compressibility_profile`
- `gauge_profile`
- `tension_profile`
- `stabilization_profile`

#### Regime-control profiles
- `meta_regime_prior`
- `runtime_regime_profile`
- `classicality_profile`
- `reeval_pressure`
- `cadence_profile`

#### Decision-side profiles
- `continuation_surface`
- `constraint_surface`
- `confidence_profile`

## 3. Element contribution packet contract

Every element should emit a typed structural contribution packet.

### Mandatory fields
- `element_id`
- `scope_ref`
- `contribution_kind`
- `confidence`
- `diagnostics`

### Optional canonical fields
- `branch_vote_surface`
- `regime_contribution`
- `cadence_contribution`
- `weight_hint`
- `bus_updates`

### Important rule
Not every element must emit a branch vote.

Some elements may primarily emit:
- regime contributions
- cadence contributions
- structural diagnostics

## 4. Group output contract

A group output is the fused higher-order result of one or more element packets.

A group output should preserve enough structure to participate honestly in final fusion.

### Recommended minimum structure
- `group_id`
- `scope_ref`
- `group_contribution_kind`
- `group_branch_surface` if applicable
- `group_regime_contribution` if applicable
- `group_confidence`
- `group_diagnostics`

## 5. Continuation surface contract

The continuation surface is the final kernel-internal decision structure before translator-side collapse.

### It may contain
- branch candidate weights
- preference ordering
- soft constraints
- hard masks
- confidence
- residual ambiguity
- partial preselection

### It must not be
- already the final task action token
- or a hidden task-local action object pretending to be generic kernel output

## 6. Translator input/output/update contracts

### Translator input contract
Translators receive task-local information and must emit path-space relevant update structure.

### Translator output contract
Translators receive the continuation surface and must emit a concrete legal task action.

### Translator feedback contract
Translators receive task-local feedback/result and must emit update-relevant kernel structure.

## 7. Run artifact contracts

At the run level, the required data artifacts are:
- `metrics.jsonl`
- `budget.csv`
- `run_manifest.json`
- `job_state.json`
- `quick_plot.png`

These are part of the overall data contract of the harness.

## 8. Summary data contracts

At higher levels, the harness must produce:
- mode summary CSVs
- family summary CSVs
- suite summary CSVs
- plots

These outputs must be semantically clean:
- CO-only outputs exclude STOA
- STOA-vs-CO outputs use compatible metrics
- identity normalization is consistent

## 9. Misalignment examples

Data contracts are misaligned if:
- packet shapes are undocumented
- translators and kernel assume incompatible structures
- branch-space vanishes silently before the kernel
- contribution packets are flattened inconsistently
- continuation surfaces are secretly task-local action objects
- or summary CSVs mix incompatible semantics while looking valid