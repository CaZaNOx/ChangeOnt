# 03C. Implementation Fidelity Status

Status: current code-vs-target status document.  
Last consolidated: 2026-05-06.  
This is not a conceptual definition; it reports how the current implementation appears to match the target docs.

Primary target docs:

```text
01B_TARGET_ARCHITECTURE_CONTRACT.md
95_KERNEL_STRUCTURE_CARRIER_ALIGNMENT.md
96_CONCEPTUAL_CLOSURE_LEDGER.md
102_DOCS_CONSOLIDATION_AND_IMPLEMENTATION_AUDIT_GATE.md
```

## Status labels

```text
faithful:
  runtime behavior substantially matches the target contract.

aligned-watchpoint:
  core path exists and passes first diagnostics, but needs deeper trace/formula validation.

partial:
  some implementation exists but important carriers or tests remain incomplete.

investigatory:
  retained for comparison or future work, not active canonical evidence.

inactive/deprecated:
  historical path or alias, not authoritative for the active target.
```

## Current status summary

| Component / layer | Status | Note |
|---|---:|---|
| Boundary / adapter public-effect publication | aligned-watchpoint | Adapters publish public_effects and sampled leakage audit did not show obvious hidden policy; magnitudes/formulas still need grounding. |
| No non-CO rescue selector / fail-closed rule | faithful | Silent first-legal/uniform/baseline-policy rescue paths were removed or fail-closed in the audited active path. Continue auditing. |
| CandidateSurface | aligned-watchpoint | Candidate rows exist as intake carriers; formula/source fields still require ledger coverage. |
| Continuation identity | aligned-watchpoint | `continuation_id -> branch_id -> candidate_id -> action` precedence exists; first-pass continuation memory can now persist across action expressions by public burden-domain key, but generic sequence-level composition now has a first-pass implementation; behavioral sufficiency remains open. |
| Branch-internal burden operations | aligned-watchpoint | Public effects now survive as branch-internal operation summaries even without cross-branch relations. |
| RelationSurface | aligned-watchpoint | Kernel-side relation derivation exists; weak decision-slot competition is separated from strong rivalry. Relation quality still needs broader trace validation. |
| RecursiveContinuationField | aligned-watchpoint | RCF consumes internal operations and relations and produces field deltas in structural traces. Formula grounding and semantic distinctness still require work. |
| CollapseCertificate | aligned-watchpoint | First-class certificate exists and affects readout. Reason quality and formula/gate grounding remain watchpoints. |
| CommitmentSurface / Readout | aligned-watchpoint | Consumes certificate fields and no longer uses non-CO rescue selector in active audited paths. Needs more fixed-score/certificate-causal tests. |
| Shape prior / gauge controls | partial | Active six-question basis exists and can set controls; minimality/sufficiency and axis independence remain open. |
| Formula ledger | partial | Initial ledger exists; full coverage for readout-affecting scalars is incomplete. |
| Quotient/equivalence tolerance | partial | First-pass public residual-profile helper now derives conservative equivalence relations and rejects same-score/action/weak-slot false quotients; final tolerance and real-trace false/missed quotient diagnostics remain incomplete. |
| Recursion demand | first-pass partial | `recursion_scheduler.py` now derives bounded public structural recursion demand from relation topology, grey/debt/hiddenness/threshold pressure, and shape controls before CollapseCertificate. It does not expand hidden futures or choose actions. Real-trace calibration and actual multi-layer unfolding remain open. |
| RCF vs known algorithms | investigatory | Minimum diagnostic criterion documented; full comparison to MCTS/DP/BP/active inference/options/SR/search remains open. |
| Consciousness/meaning bridge | investigatory | Motivation and continuation-relevance bridge documented; not part of current evidence-bearing kernel claim. |

## Interpretation

The active architecture is no longer blocked by the earlier hard failures:

```text
relation-starved RCF;
action-as-branch precedence;
first-pass action-expression-only continuation memory;
weak competition as collapse-blocking rivalry;
missing certificate-aware readout;
non-CO rescue selector;
branch-internal operations disappearing without cross-branch relations.
```

However, the implementation is not final or paper-ready. Current status is:

```text
architecture target is coherent enough for systematic implementation audit;
runtime path is aligned enough for structural diagnostics;
benchmark/performance claims remain premature.
```

## Next code-vs-doc audit priorities

```text
1. Verify every adapter public_effect against public-fact rules and formula status.
2. Verify every branch-internal operation carrier and relation carrier has tests.
2a. Extend first-pass sequence-composition tests into broader multi-stage sequence traces and sequence on/off ablations.
3. Extend quotient/equivalence validation beyond first-pass synthetic invariants into real-trace false/missed quotient audits.
3a. Extend recursion-scheduler validation into real traces and distinguish justified structural unfolding demand from ordinary lookahead/search.
4. Verify CollapseCertificate gates cause behavior changes for structural reasons.
5. Complete formula-ledger entries for every readout-affecting scalar.
6. Produce cross-family structural trace packs before reward benchmarking.
```

## 2026-05-22 quotient / maintenance audit status

Two audit-only passes now refine the remaining hardening watchpoints:

- `quotient_accept_reject_audit_v1.py` adds/uses quotient profile accept/reject provenance in relation telemetry and row traces. It found no duplicate-signature missed-quotient bug in the capped current-family diagnostic, but confirms that quotienting remains conservative and mostly singleton outside matched residual profiles.
- `maintenance_action_insensitivity_audit_v1.py` confirms maintenance middle/renewal_like action-prefix insensitivity under recent-mechanism ablations. The current trace evidence points to generic readout dominance / stable-continuation swamping and incomplete generic pre-blocking resolver timing, not a maintenance-specific rule.

Fidelity consequence: quotient/equivalence remains partial, but is now auditable. Maintenance behavior must not be tuned directly; next code work should add generic dominance/readout-swamping and cross-family pre-blocking resolver microcases before any commitment-formula change.


## 2026-05-22 kernel Pass-1 closure candidate

Generic sequence-level continuation composition has been implemented and wired. See `KERNEL_PASS1_CLOSURE_CANDIDATE_REPORT_2026-05-22.md`, `SEQUENCE_COMPOSITION_MICROCASE_PROBE_REPORT_2026-05-22.md`, and the updated sequence/readout audits.

Current status: the known rough kernel mechanism set is now present as a Pass-1 closure candidate, not a final kernel. Next work should freeze/evaluate rather than add mechanisms: sequence on/off diagnostics, adapter-boundary tests, coefficient sensitivity, quotient false/missed quotient audit, and a current-family failure map. Robot/sim expansion remains premature until this evaluation is complete.
