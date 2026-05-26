# Architecture Acceptance Audits — 2026-05-06

## Status

**Architecture acceptance status: ACCEPTANCE_WATCHPOINTS_REMAIN.**

This audit does not test reward performance. It checks whether the current kernel path is clean enough to present as an architecture to a serious critic.

Current answer:

```text
The public-effect → RelationSurface → RCF → CollapseCertificate path exists,
and the immediate hard failures from the first audit were reduced to watchpoints.
Relation quality, branch identity trace quality, certificate reasons, public-effect
formula grounding, and formula-ledger completeness are still not critic-ready.
```

The current executable audit is:

```bash
cd ChangeOntCode
python -m experiments.studies.architecture_acceptance_audit_v1
```

Current verified output:

```json
{
  "status": "ACCEPTANCE_WATCHPOINTS_REMAIN",
  "relations_total": 80,
  "rivalry_ratio": 0.0,
  "formula_coefficient_lines": 231,
  "summary": {
    "adapter_public_effect_leakage": "PASS_WITH_WATCHPOINTS",
    "relation_noise": "PASS_WITH_WATCHPOINTS",
    "collapse_certificate_reason_quality": "PASS_WITH_WATCHPOINTS",
    "branch_identity_trace_quality": "PASS_WITH_WATCHPOINTS",
    "formula_grounding": "PASS_WITH_WATCHPOINTS"
  }
}
```

This is architecture/trace status only. It is not reward evidence.

---

## 1. Adapter public-effect leakage audit

### Current result

```text
PASS_WITH_WATCHPOINTS
```

No sampled `public_effect` contains forbidden leakage labels such as `oracle`, `optimal_policy`, `dp_value`, `best_action`, or `hidden_policy`. Accepted sampled public bases are within the allowed public bases.

### Remaining watchpoints

This pass checks public/leakage form. It does not yet prove every magnitude formula is conceptually grounded.

Examples requiring formula-ledger scrutiny:

```text
maintenance: degradation/maintenance_need magnitudes
maze: visible_goal_distance local improvement
latent mechanism: visible_route_distance / mechanism_hiddenness magnitudes
bandit/renewal: uncertainty-carry and uncertainty-reduction magnitudes
```

Acceptance still requires a per-effect table:

```text
effect emitted
public source
why public grammar
why not policy advice
hidden state used? no/yes
formula status
```

---

## 2. RelationSurface noise audit

### Current result

```text
PASS_WITH_WATCHPOINTS
```

Current relation path distinguishes weak decision-slot competition from strong continuation rivalry. In the current audit output, strong rivalry ratio is zero in the sampled cases, while weak decision-slot competition remains frequent and separately logged.

### Remaining watchpoints

```text
- weak decision-slot competition can dominate raw relation counts;
- relation quality still needs broader traces beyond the five representative cases;
- sparse structural relations must remain typed and public-basis grounded;
- relation-derived field deltas must keep traceable reasons.
```

Acceptance still depends on showing that relation topology is not just action-set bookkeeping.

---

## 3. Collapse-certificate reason audit

### Current result

```text
PASS_WITH_WATCHPOINTS
```

CollapseCertificate now separates weak procedural competition from unresolved structural rivalry and exposes certificate gates consumed by CommitmentSurface.

### Remaining watchpoints

```text
- certificate reason quality is still minimal-v1;
- blocker pressure and resolver support coefficients remain provisional;
- mode/action changes must be explained by certificate reasons, not scalar dominance alone;
- non-ready certificates with active blockers/recursion must continue to block dominance-style earned collapse.
```

A certificate is not critic-ready merely because it changes readout. It must preserve a reason structure that survives manual trace review.

---

## 4. Branch identity trace audit

### Current result

```text
PASS_WITH_WATCHPOINTS
```

Branch identity uses the intended precedence:

```text
continuation_id → branch_id → candidate_id → action
```

Continuation signatures include coarse burden-regime bands rather than raw magnitude identity.

### Remaining watchpoints

```text
- multi-step continuation identity is still open;
- same native action in materially different pressure regimes must continue to split when warranted;
- small within-band numeric jitter must not create identity explosion;
- action labels must remain last-resort interface aliases, not primary continuation identity.
```

---

## 5. Formula-level grounding audit

### Current result

```text
PASS_WITH_WATCHPOINTS
```

Static audit still finds many formula coefficient lines across active surfaces. This does not mean the formulas are wrong. It means they are not final derived laws and are not paper-claim safe without ledger coverage.

Formula-ledger work remains required for:

```text
candidate publication formulas;
RelationSurface weights/bands;
RCF debt, relief, grey, recursion, readiness, viability;
CollapseCertificate blocker/resolver/gate formulas;
CommitmentSurface dominance, sampling, and stable-continuation formulas;
adapter public-effect magnitudes.
```

---

## 6. What changed in the acceptance-fix follow-up

The corrective pass recorded in `93_ARCHITECTURE_ACCEPTANCE_FIXES.md` changed the first hard-failure audit interpretation into watchpoints.

Material changes:

```text
- Weak decision-slot competition is separated from strong continuation rivalry.
- `decision_slot_competition` is logged but does not count as an unresolved-rival blocker.
- Continuation signatures include coarse burden-regime bands, not raw magnitudes.
- CollapseCertificate exposes weak decision competition separately from unresolved rivals.
- CommitmentSurface respects certificate gates.
- Initial formula-ledger rows exist for acceptance-critical readout formulas.
```

What remains watchpoint-level:

```text
- Weak decision-slot competition can still be frequent, though no longer collapse-blocking.
- Full formula-ledger coverage for all remaining behavior-affecting scalar formulas is incomplete.
- Public-effect magnitudes still require broader formula grounding before final paper claims.
- Broader real-trace behavior still needs structural validation before performance claims.
```

---

## 7. Claim boundary

This audit supports only the following bounded claim:

```text
The current architecture path is wired and inspectable enough for controlled structural diagnostics and ablations.
```

It does not support:

```text
benchmark success;
RCF novelty;
final formula grounding;
final quotient/recursion formalization;
consciousness or subjectivity claims.
```
