# 91 — Earned-Collapse Certificate Implementation

Date: 2026-05-06
Status: minimal runtime implementation / diagnostic bridge
Claim boundary: this is not reward evidence and not a final collapse theory.

## Purpose

The previous RelationSurface/RCF wiring established that public burden/effect
facts can produce relation topology and that those relations can alter RCF field
outputs. The remaining readout gap was that `CommitmentSurface` consumed those
relation effects mostly after they had been flattened into scalar proxy fields.

This file records the first minimal implementation of a structured earned-
collapse certificate.

## Runtime path

```text
CandidateSurface
→ RelationSurface
→ RecursiveContinuationField
→ CollapseCertificate
→ CommitmentSurface
```

The certificate stage is implemented in:

```text
agents/co/runtime/surfaces/collapse_certificate.py
```

and is applied inside candidate publication after RCF field deformation and
before rows are exposed to CommitmentSurface.

## What the certificate preserves

The certificate preserves relation/collapse reasons that should not disappear
into scalar field mutation:

```text
collapse_certificate_status
collapse_certificate_ready
collapse_certificate_score / earnedness
collapse_certificate_blocker_pressure
collapse_certificate_recursion_demand
collapse_blockers
unresolved_rival_count
quotient_resolved_rival_count
relations_by_type
```

It is deliberately generic. It reads anonymous branch ids, relation types, RCF
field outputs, and direct controls. It must not inspect family names, action
labels, reward values, hidden state, shortest paths, DP values, or other policy
information.

## Certificate logic, minimal v1

A branch is more collapse-ready when:

```text
- field collapse readiness is high;
- debt and grey pressure are low/bounded;
- quotient/equivalence or cancellation resolves rivals;
- relief/cancellation/buffering relations support burden resolution;
- no non-equivalent rival remains operative;
- recursion demand is not active.
```

A branch is blocked when:

```text
- unresolved non-equivalent rivals remain;
- operative grey difference remains;
- burden remains unresolved without relief/cancellation/buffering;
- relation topology still demands recursion.
```

The certificate is not a policy selector. It is a collapse-readiness and
collapse-blocker record. CommitmentSurface still performs readout, but it now
uses certificate fields as first-class evidence.

## Why this matters

The kernel claim is not that relations merely perturb internal fields. The claim
is that relation topology can affect whether collapse is earned. Therefore the
readout must be able to distinguish:

```text
unresolved rival → preserve grey / recurse / block collapse
quotient-equivalent rival → collapse may proceed
relief/cancellation → burden can be reduced or condition removed
raw relation telemetry → not policy evidence by itself
```

This patch moves the implementation from:

```text
relation-influenced scalar proxy readout
```

toward:

```text
relation-certified earned-collapse readout
```

## Diagnostics added

```text
agents/co/tests/collapse_certificate_readout_invariants.py
agents/co/tests/commitment_surface_relation_awareness_diagnostics.py
experiments/studies/relation_path_trace_v1.py
```

The relation-path trace now reports not only whether relations alter RCF fields,
but also whether the certificate-aware readout changes commitment mode/action in
sampled real adapter cases.

Current relation-path diagnostic result verified in this working tree:

```json
{
  "cases": 5,
  "candidate_rows": 20,
  "relations_total": 80,
  "non_rival_relations": 16,
  "field_delta_positive_cases": 5,
  "commitment_action_changed_cases": 0,
  "commitment_mode_changed_cases": 1
}
```

Interpretation:

```text
Relation topology reaches RCF.
RCF field outputs change in all sampled cases.
Certificate-aware readout changes commitment mode in one sampled case while the native action remains unchanged.
This is mechanism/trace evidence only, not reward-performance evidence.
```

## Remaining caveats

1. The certificate rules are minimal v1 rules, not a final earned-collapse
   algebra.
2. Relation noise remains possible, especially if weak decision-slot competition is misread as structural rivalry.
3. Formula-level grounding is still required for certificate weights and gates.
4. Real benchmark reward remains uninterpreted until leakage, relation quality,
   and collapse behavior are audited.
5. This implementation should be tested with RelationSurface-on/off and
   fixed-score/different-topology diagnostics before broad performance claims.

---

## Acceptance correction: certificate reason quality

A collapse certificate must distinguish weak procedural competition from strong unresolved rivalry.

```text
decision_slot_competition:
  counted as weak competition telemetry;
  not a collapse blocker by itself.

rivalry:
  counted as unresolved rival pressure only when it expresses continuation-level incompatibility.
```

The certificate must expose `weak_decision_competition_count` separately from `unresolved_rival_count`. A branch should not be blocked merely because it appears in the same immediate action set as other branches.


## Carrier alignment correction

See `95_KERNEL_STRUCTURE_CARRIER_ALIGNMENT.md`. Public burden/effect facts must not disappear when they do not form a cross-branch relation. Branch-internal operations are first-class kernel carriers, while weak decision-slot competition remains procedural telemetry rather than strong rivalry or a collapse blocker.
