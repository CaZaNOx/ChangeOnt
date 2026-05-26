# Structural Microcase Probe Report — 2026-05-16

## Scope

This report documents targeted synthetic structural microcases. They are not reward benchmarks, not broad family studies, and not evidence that CO works empirically.

The probe lives at:

```text
ChangeOntCode/experiments/studies/structural_microcase_probe_v1.py
ChangeOntCode/agents/co/tests/structural_microcase_probe_invariants.py
ChangeOntCode/outputs/structural_microcase_probe_v1.json
```

## What was tested

The probe constructs controlled candidate rows with public effects so the current kernel can be checked against small known structural expectations:

```text
neutral_no_effects_equal
weak_decision_slot_only
hiddenness_without_exposure
exposure_resolves_hiddenness_equal_evidence
relief_resolves_burden_equal_evidence
cancellation_resolves_burden_equal_evidence
quotient_equivalent_pressure_equal_evidence
```

The tested path is:

```text
candidate rows
→ public_effects
→ RelationSurface
→ branch-internal burden carriers
→ RecursiveContinuationField
→ CollapseCertificate
→ CommitmentSurface
```

## Latest result summary after certificate-aware continuation correction

```json
{
  "cases": 7,
  "passed": 7,
  "passed_with_watchpoints": 0,
  "failed": 0,
  "cases_with_field_delta": 5,
  "selected_blocked_stable_continuation_watchpoints": 0
}
```

## Positive findings

- Weak decision-slot competition is logged as weak/procedural competition and does not count as a branch-internal burden operation.
- Hiddenness carried without exposure creates unresolved hiddenness burden and blocks dominance-style collapse.
- Comparable hiddenness-blocked stable continuation is redirected to an unblocked alternative after the certificate-aware correction.
- Exposure, relief, cancellation, and equivalence are recognized as structural relations/carriers.
- Under equal local evidence, resolver branches outrank burden-carrying branches in the exposure, relief, and cancellation microcases.
- Equivalent pressure signatures produce quotient/equivalence support without generating false unresolved rivalry.

## Relation to continuation-gating probe

The earlier microcase watchpoint has been moved into the explicit second-stage diagnostic:

```text
STRUCTURAL_CONTINUATION_GATING_PROBE_REPORT_2026-05-16.md
```

That diagnostic now checks both:

```text
1. comparable unblocked alternatives displace blocked stable continuations;
2. overwhelming-support blocked continuations may still continue under unresolved burden.
```

## Claim boundary

These results support only this limited claim:

```text
The current relation/certificate path recognizes the intended structural classes
in synthetic controlled cases and affects field/certificate/readout telemetry for
non-decorative reasons.
```

They do not establish:

```text
- reward performance;
- generality across real family distributions;
- RCF novelty;
- formula correctness;
- consciousness/meaning claims.
```

## Required follow-up

The next relevant work is not more broad rewriting. It is trace inspection of real adapter cases after the certificate-aware correction, followed by formula-ledger entries for the new continuation-gating margins.
