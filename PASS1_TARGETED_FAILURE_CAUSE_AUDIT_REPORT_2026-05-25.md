# Pass-1 Targeted Failure-Cause Audit — 2026-05-25

**Claim boundary:** Targeted causal audit only.  This is not a tuning run, not a performance claim, and not evidence of CO superiority/inferiority by itself.  It identifies which mechanism layer plausibly explains current weak STOA comparisons.

## Bottom line

The weak CO-vs-STOA comparison is not caused by a single missing toggle. The targeted audit separates three cause clusters:

1. **Bandit:** weak posterior-like evidence accumulation / exploration cadence.
2. **Renewal:** weak compact recurrence/phase extraction compared with PhaseFSM.
3. **Maintenance:** longer-horizon phase transition is wrong: middle-like traces often shift from RUN into repeated INSPECT/exposure, but do not progress generically to relief/stabilization; this is sequence/readout phase-consumption failure, not a repair-specific missing rule.

No new kernel mechanism or problem-specific adjustment was made in this pass.

## Bounded run settings

- Seeds: `[0, 1]`
- Bandit horizon: `48`
- Renewal horizon: `48`
- Maintenance horizon cap: `48`
- Q-learning was skipped in this targeted pass to avoid timeouts; q-learning remains covered by the prior all-problem STOA comparison.

## Bandit

- CO mean regret: `20.0000`
- Thompson Sampling mean regret: `3.5000`
- CO late best-arm pull rate: `0.5000`
- TS late best-arm pull rate: `0.9375`

**Diagnosis:** CO has public uncertainty/burden signals, but it does not maintain or consume a compact posterior-like evidence state. When early feedback misleads, support/stability can lock in more slowly or wrongly than Thompson Sampling.

## Renewal

- CO mean reward: `0.5208`
- PhaseFSM mean reward: `0.8646`
- CO/Phase action alignment: `0.5833`
- CO period-3 repeat score: `0.7556`
- PhaseFSM period-3 repeat score: `0.8667`

**Diagnosis:** CO sequence composition is local and does not yet form a compact, retained recurrence-phase variable. PhaseFSM directly represents the relevant cycle; CO currently under-extracts it.

## Maintenance

### bandit_like

- CO mean total reward: `41.3750`
- Threshold mean total reward: `41.8750`
- Q-learning mean total reward: `skipped here`
- CO RUN rate: `1.0000`
- CO maintenance-action rate: `0.0000`
- Carrier/resolver cases: `52`
- Shape-gauged resolver triggers: `0`
- High-debt RUN cases: `50`
- Carrier/resolver → maintenance selection rate: `0.0000`
- CO mean INSPECT count: `0.00`
- CO mean REPAIR/REPLACE count: `0.00`
- INSPECT followed by relief within 3 steps: `0.0000`
- Mean max INSPECT streak: `0.00`

### middle

- CO mean total reward: `9.3000`
- Threshold mean total reward: `40.3750`
- Q-learning mean total reward: `skipped here`
- CO RUN rate: `0.2812`
- CO maintenance-action rate: `0.7188`
- Carrier/resolver cases: `96`
- Shape-gauged resolver triggers: `0`
- High-debt RUN cases: `27`
- Carrier/resolver → maintenance selection rate: `0.7188`
- CO mean INSPECT count: `34.50`
- CO mean REPAIR/REPLACE count: `0.00`
- INSPECT followed by relief within 3 steps: `0.0000`
- Mean max INSPECT streak: `34.50`

### renewal_like

- CO mean total reward: `0.9250`
- Threshold mean total reward: `-23.8500`
- Q-learning mean total reward: `skipped here`
- CO RUN rate: `0.1250`
- CO maintenance-action rate: `0.8750`
- Carrier/resolver cases: `96`
- Shape-gauged resolver triggers: `7`
- High-debt RUN cases: `12`
- Carrier/resolver → maintenance selection rate: `0.8750`
- CO mean INSPECT count: `42.00`
- CO mean REPAIR/REPLACE count: `0.00`
- INSPECT followed by relief within 3 steps: `0.0000`
- Mean max INSPECT streak: `13.50`

## Cause summary

The current Pass-1 kernel detects many relevant structures, but each weak family exposes a different missing strength:

- bandit requires stronger generic statistical evidence accumulation, not sequence/quotient machinery;
- renewal requires a generic recurrence/phase-retention abstraction, not simply local sequence rows;
- maintenance requires stronger generic phase-transition consumption (expose/reveal → relieve/reduce → stabilize) over longer horizons, not a repair-specific rule.

## Recommended next steps

1. Do not add task-specific fixes.
2. Decide whether CO should include a generic recurrent-regime/phase-retention element. This may be a real missing concept, but it must pass the concept-admission gate.
3. Audit whether bandit/posterior-style evidence should remain a weakness CO accepts, or whether generic evidence-state retention belongs inside the kernel.
4. For maintenance, run a generic gate/readout adequacy redesign only if context-conditioned traces show strong carrier/resolver/phase expectation with repeated non-selection.

## Outputs

- `outputs/pass1_targeted_failure_cause_audit_v1/summary.json`
- `outputs/pass1_targeted_failure_cause_audit_v1/bandit_steps.jsonl`
- `outputs/pass1_targeted_failure_cause_audit_v1/renewal_steps.jsonl`
- `outputs/pass1_targeted_failure_cause_audit_v1/maintenance_steps.jsonl`

