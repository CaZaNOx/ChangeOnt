# Structural Trace and Formula Hotspot Review — 2026-05-06

## Scope

This pass followed the validation pack by manually reviewing the remaining structural trace watchpoints and formula-ledger hot spots. It did not run broad reward benchmarks and did not tune reward performance.

## Checks performed

1. Reviewed representative structural traces for:
   - `bandit_initial`
   - `maintenance_partial_midhealth`
   - `maze_visible_local`
   - `latent_mechanism_visible`
   - `renewal_initial`
2. Checked whether field deltas were scalar-field changes or topology/count changes.
3. Checked whether weak decision-slot competition was still acting like strong rivalry.
4. Checked whether non-ready collapse certificates could still permit dominance-style commitment.
5. Reviewed formula-hotspot scan and updated the formula ledger for new certificate-gate formulas.

## Fixes made

### 1. CommitmentSurface now respects non-ready certificates as dominance gates

Finding: in `latent_mechanism_visible`, relation/certificate structure made the selected `RIGHT` branch certificate-not-ready with substantial recursion demand, but readout still used `dominance` mode. This violated the certified docs requirement that CommitmentSurface respect certificate gates.

Fix:

- Added `certificate_gate_open` telemetry.
- Added `certificate_blocks_dominance` gate.
- Dominance-style earned collapse is now blocked when a certificate is non-ready and recursion/blocker pressure or explicit blockers indicate unresolved structure.

Result:

- `latent_mechanism_visible` now shifts from `dominance` to `stable_continuation`, while keeping the same action. This means the action may remain stable, but the readout no longer claims earned dominance collapse under a non-ready certificate.

### 2. Structural trace diagnostics now separate scalar deltas from topology/count deltas

Finding: previous diagnostics over-counted topology/count changes such as `quotient_share_count` as generic field deltas.

Fix:

- Added `scalar_field_delta_l1` / `scalar_field_delta_max`.
- Added `topology_count_delta_l1` / `topology_count_delta_max`.

Result:

- Maze topology/count shifts are no longer confused with scalar field instability.

### 3. Weak decision-slot competition no longer creates false watchpoints when branch-internal carriers are present

Finding: weak competition dominates relation counts in some families because every immediate action competes for one readout slot. This is not strong rivalry and is no longer collapse-blocking.

Fix:

- Weak competition dominance is now an informational note when branch-internal burden operations are present.
- It remains a warning only if no structural carrier exists.

### 4. Formula ledger expanded for certificate-gate fields

Added formula-ledger rows for:

- `certificate_gate_open`
- `certificate_blocks_dominance`

These are classified as canonical-constrained proxies, not final derived laws.

## Updated structural trace summary

```json
{
  "cases": 5,
  "candidate_rows": 20,
  "relations_total": 80,
  "structural_relations": 16,
  "weak_decision_competition_relations": 64,
  "branch_internal_operation_rows": 20,
  "field_delta_positive_cases": 5,
  "commitment_changed_cases": 1,
  "cases_with_watchpoints": 0
}
```

## Case interpretation

### Bandit

- No cross-branch structural relations.
- Branch-internal uncertainty operations are active.
- Mode remains `reopen_or_sample`, which is appropriate under unresolved sampling/uncertainty pressure.

### Maintenance

- Selected action remains `INSPECT` in `stable_continuation` mode.
- Public effects alter field state, but no per-branch scalar delta is large enough to require action change.
- This is currently interpreted as stable readout under exposure/hiddenness handling, not a failure.

### Maze

- Selected action remains `RIGHT` in `dominance` mode.
- `RIGHT` has earned-collapse-ready certificate and relief support.
- Topology/count deltas reflect quotient/relations, not destabilizing scalar deltas.

### Latent mechanism

- Selected action remains `RIGHT`, but mode changes from `dominance` to `stable_continuation` after certificate-gate fix.
- This is the correct architecture outcome: the same action may remain selected, but the kernel no longer claims dominance-style earned collapse while hiddenness/recursion structure is unresolved.

### Renewal

- No cross-branch structural relations.
- Branch-internal recurrence/uncertainty operations are active.
- Mode remains `reopen_or_sample`, which is consistent with unresolved sequence/phase uncertainty.

## Remaining watchpoints

No current structural trace case has a hard watchpoint after this pass. Remaining limitations are broader validation/research items:

1. Full formula ledger is still incomplete.
2. Exact quotient/equivalence tolerance remains target-specified, not calibrated.
3. Recursion scheduler/budget remains target-specified, not deeply validated.
4. Multi-step continuation identity remains under-audited.
5. These diagnostics are still architecture/trace validation, not reward evidence.
