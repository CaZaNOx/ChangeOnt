# 93. Architecture Acceptance Fixes: Rivalry, Branch Regimes, Certificate Reasons, Formula Ledger

Status: active contract / implementation alignment target.

This file records the corrective contract following `92_ARCHITECTURE_ACCEPTANCE_AUDITS.md`. It is not a new doctrine layer. It narrows four audit failures into exact implementation requirements.

---

## 1. Weak decision-slot competition is not strong continuation rivalry

A candidate set normally competes for one immediate readout slot. That fact is public and legal, but it is weak procedural competition, not by itself an unresolved continuation rivalry.

```text
weak decision-slot competition:
  only one expression can be selected at this decision moment

strong continuation rivalry:
  committing to one continuation blocks, consumes, invalidates, or destabilizes another continuation condition
```

RelationSurface must therefore separate:

```text
decision_slot_competition
```

from:

```text
rivalry
```

Only strong `rivalry` may act as an earned-collapse blocker. `decision_slot_competition` may be logged and may affect ordinary readout awareness, but it must not inflate unresolved non-equivalent rival counts.

Acceptance condition:

```text
generic single-action-slot facts must not dominate relation topology or collapse certificates.
```

---

## 2. Continuation identity must include burden regime, not raw action and not raw magnitude

A branch is a retained continuation-pressure signature. It must distinguish materially different pressure regimes while avoiding identity explosion.

Therefore a public-effect-derived continuation signature may include coarse regime bands such as:

```text
none / low / medium / high / critical
```

but must not use raw continuous magnitudes as identity keys.

Example:

```text
RUN with low degradation carry
  ≠ RUN with critical degradation carry
```

but:

```text
RUN with 0.61 degradation and RUN with 0.63 degradation
```

should usually remain the same pressure-regime branch unless a documented threshold is crossed.

Acceptance condition:

```text
same action + materially different burden regime → different pressure signature;
same action + tiny magnitude perturbation within band → same pressure signature.
```

---

## 3. Collapse certificates must preserve reason quality

CollapseCertificate must distinguish blockers/resolvers by relation quality:

```text
strong unresolved rivalry → possible blocker
weak decision-slot competition → not a blocker by itself
quotient/equivalence → rival resolution / collapse support
relief/cancellation/buffering → burden resolution support
operative grey/proximity/recursion → possible blocker when active
```

The certificate must expose structured reasons, not only a score:

```text
collapse_blockers
collapse_certificate_reason_flags
unresolved_rival_count
weak_decision_competition_count
quotient_resolved_rival_count
relief_out_count
cancellation_out_count
buffering_relation_count
recursion_relation_count
```

Acceptance condition:

```text
A branch must not be blocked merely because it competes for the same immediate decision slot.
```

---

## 4. Formula ledger minimum before architecture acceptance

Formula grounding is still not complete, but the active architecture must include an initial ledger for the formulas now capable of changing readout.

At minimum the ledger must cover:

```text
RelationSurface relation weights
RelationSurface pressure-regime banding
CollapseCertificate blocker_pressure
CollapseCertificate resolver_support
CollapseCertificate earnedness
CollapseCertificate recursion_demand
CommitmentSurface collapse_blocked
CommitmentSurface relation_ready_bonus
CommitmentSurface dominance_score
CommitmentSurface sampling_score
CommitmentSurface continuation_score
```

For each formula, the ledger must state:

```text
status class
allowed inputs
forbidden inputs
monotonic commitments
family-tuning risk
paper-claim status
```

Acceptance condition:

```text
No readout-affecting scalar may remain undocumented as an anonymous heuristic.
```
