# Real-Family Manual Trace Review — 2026-05-16

Status: **manual structural trace review, not reward evidence**.

Study: `ChangeOntCode/experiments/studies/real_family_manual_trace_review_v1.py`

## Coverage

- Total cases: 15
- Cases by family: `{'bandit': 3, 'latent_mechanism': 3, 'maintenance': 3, 'maze': 3, 'renewal': 3}`
- Selected modes: `{'dominance': 3, 'reopen_or_sample': 7, 'stable_continuation': 5}`
- Families with relation telemetry: `{'bandit': 3, 'latent_mechanism': 3, 'maintenance': 3, 'maze': 3, 'renewal': 3}`
- Families with structural cross-branch relations: `{'latent_mechanism': 3, 'maintenance': 3, 'maze': 3}`
- Certificate-aware reopen cases: 2
- Certificate-aware stable-continuation cases: 0
- Watchpoints: `{}`

## Judgment

The manual trace review did not find hard watchpoints in the representative public-observation cases. Every active family produced relation telemetry. Structural cross-branch relations appeared in maze, maintenance, and latent-mechanism cases; bandit and renewal mostly operate through branch-internal sampling/uncertainty carriers in these representative cases.

This is sufficient for a small frozen empirical sanity smoke, but not for broad benchmark claims.

## Where to inspect details

Full case-level trace records are in:

```text
ChangeOntCode/outputs/real_family_manual_trace_review_v1.json
```
