# Frozen Empirical Sanity Smoke — 2026-05-16

Status: **small runtime sanity only, not benchmark evidence**.

Study: `ChangeOntCode/experiments/studies/frozen_empirical_sanity_smoke_v1.py`

This smoke was run only after structural/microcase/manual trace checks. Constants were frozen before execution. No tuning was performed in response to these results.

## Maintenance/replacement smoke

Summary: `{'co': {'errors': [], 'mean_total_reward': 30.19166666666667, 'runs': 6}, 'random': {'errors': [], 'mean_total_reward': -44.48333333333333, 'runs': 6}, 'threshold': {'errors': [], 'mean_total_reward': 26.133333333333336, 'runs': 6}}`

Scope: 3 regimes (`bandit_like`, `middle`, `renewal_like`) × 3 agents (`random`, `threshold`, `co`) × 2 seeds.

## Latent-mechanism smoke

Summary: `{'co': {'errors': [], 'mean_reward': 0.26249999999999996, 'runs': 1, 'success_rate': 1.0}, 'heuristic': {'errors': [], 'mean_reward': -1.7600000000000002, 'runs': 1, 'success_rate': 0.0}, 'random': {'errors': [], 'mean_reward': -1.0, 'runs': 1, 'success_rate': 0.0}}`

Scope: one `easy_visible` max-20-step smoke for random, heuristic, and CO.

## Interpretation boundary

This only shows that the frozen runtime executes without invalid-action rescue or catastrophic wiring failure on a small sanity sample. It is not a performance claim. The maintenance CO mean and latent CO success in this smoke must not be cited as evidence for CO effectiveness without larger frozen-seed, fair-baseline studies.

## Defect found during this step

`experiments/runners/maintenance_replacement_runner.py` still contained an invalid-action rescue to `RUN`. That was removed and replaced with fail-closed behavior. A regression invariant now protects it.
