# Current Kernel Diagnostic Map v1 — 2026-05-22

## Claim boundary

First-pass diagnostic map only. It tests whether recent generic kernel mechanisms are behavior/telemetry visible across existing problem families. It is not a benchmark, not CO proof, not novelty evidence, and not a reason to tune coefficients post hoc.

## Scope

Runs attempted: 48; succeeded: 48; failed: 0.

Variants: `full_current`, `static_shape`, `no_quotient`, `no_scheduler`, `no_sequence`, `minimal_recent_core`.

## Per-run map

| family | mode | seed | variant | metric | actions | dyn steps | seq steps | avg seq rows | avg quotient rows | avg recursion demand | max recursion demand | avg blockers | modes |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| bandit | easy_public_bandit | 0 | full_current | 4.000 | 3 | 16 | 1 | 0.062 | 0.000 | 0.190 | 0.234 | 0.000 | `{"dominance": 11, "reopen_or_sample": 3, "stable_continuation": 2}` |
| bandit | easy_public_bandit | 0 | minimal_recent_core | 0.000 | 1 | 0 | 0 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | `{"dominance": 15, "reopen_or_sample": 1}` |
| bandit | easy_public_bandit | 0 | no_quotient | 4.000 | 3 | 16 | 1 | 0.062 | 0.000 | 0.190 | 0.234 | 0.000 | `{"dominance": 11, "reopen_or_sample": 3, "stable_continuation": 2}` |
| bandit | easy_public_bandit | 0 | no_scheduler | 0.000 | 1 | 16 | 0 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | `{"dominance": 15, "reopen_or_sample": 1}` |
| bandit | easy_public_bandit | 0 | no_sequence | 4.000 | 3 | 16 | 0 | 0.000 | 0.000 | 0.190 | 0.234 | 0.000 | `{"dominance": 11, "reopen_or_sample": 3, "stable_continuation": 2}` |
| bandit | easy_public_bandit | 0 | static_shape | 0.000 | 1 | 0 | 0 | 0.000 | 0.000 | 0.198 | 0.234 | 0.000 | `{"dominance": 15, "reopen_or_sample": 1}` |
| latent_mechanism | easy_visible | 0 | full_current | 6.200 | 5 | 14 | 0 | 0.000 | 2.143 | 0.108 | 0.378 | 0.000 | `{"dominance": 9, "stable_continuation": 5}` |
| latent_mechanism | easy_visible | 0 | minimal_recent_core | -15.800 | 5 | 0 | 0 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | `{"dominance": 9, "stable_continuation": 7}` |
| latent_mechanism | easy_visible | 0 | no_quotient | -15.800 | 5 | 16 | 0 | 0.000 | 0.000 | 0.155 | 0.386 | 0.000 | `{"dominance": 9, "stable_continuation": 7}` |
| latent_mechanism | easy_visible | 0 | no_scheduler | 6.200 | 5 | 14 | 0 | 0.000 | 2.143 | 0.000 | 0.000 | 0.000 | `{"dominance": 9, "stable_continuation": 5}` |
| latent_mechanism | easy_visible | 0 | no_sequence | 6.200 | 5 | 14 | 0 | 0.000 | 2.143 | 0.108 | 0.378 | 0.000 | `{"dominance": 9, "stable_continuation": 5}` |
| latent_mechanism | easy_visible | 0 | static_shape | 4.200 | 5 | 0 | 0 | 0.000 | 2.188 | 0.100 | 0.342 | 0.000 | `{"dominance": 10, "stable_continuation": 6}` |
| latent_mechanism | hidden_depth2 | 0 | full_current | -14.400 | 5 | 16 | 13 | 0.938 | 1.500 | 0.370 | 0.593 | 0.941 | `{"reopen_or_sample": 16}` |
| latent_mechanism | hidden_depth2 | 0 | minimal_recent_core | -16.000 | 2 | 0 | 0 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | `{"reopen_or_sample": 16}` |
| latent_mechanism | hidden_depth2 | 0 | no_quotient | -15.400 | 5 | 16 | 13 | 0.875 | 0.000 | 0.401 | 0.595 | 0.928 | `{"reopen_or_sample": 16}` |
| latent_mechanism | hidden_depth2 | 0 | no_scheduler | -16.000 | 4 | 16 | 12 | 0.812 | 1.375 | 0.000 | 0.000 | 0.944 | `{"reopen_or_sample": 16}` |
| latent_mechanism | hidden_depth2 | 0 | no_sequence | -14.400 | 5 | 16 | 0 | 0.000 | 1.500 | 0.370 | 0.593 | 0.941 | `{"reopen_or_sample": 16}` |
| latent_mechanism | hidden_depth2 | 0 | static_shape | -16.000 | 2 | 0 | 12 | 0.750 | 0.500 | 0.353 | 0.360 | 1.000 | `{"reopen_or_sample": 16}` |
| maintenance_replacement | bandit_like | 0 | full_current | 18.000 | 1 | 18 | 18 | 3.000 | 2.000 | 0.006 | 0.066 | 0.000 | `{"dominance": 18}` |
| maintenance_replacement | bandit_like | 0 | minimal_recent_core | 18.000 | 1 | 0 | 0 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | `{"dominance": 18}` |
| maintenance_replacement | bandit_like | 0 | no_quotient | 18.000 | 1 | 18 | 18 | 3.000 | 0.000 | 0.010 | 0.066 | 0.000 | `{"dominance": 18}` |
| maintenance_replacement | bandit_like | 0 | no_scheduler | 18.000 | 1 | 18 | 18 | 3.000 | 2.000 | 0.000 | 0.000 | 0.000 | `{"dominance": 18}` |
| maintenance_replacement | bandit_like | 0 | no_sequence | 18.000 | 1 | 18 | 0 | 0.000 | 2.000 | 0.006 | 0.066 | 0.000 | `{"dominance": 18}` |
| maintenance_replacement | bandit_like | 0 | static_shape | 18.000 | 1 | 0 | 18 | 3.000 | 2.000 | 0.005 | 0.073 | 0.000 | `{"dominance": 18}` |
| maintenance_replacement | middle | 0 | full_current | 16.750 | 1 | 18 | 18 | 3.278 | 0.000 | 0.092 | 0.172 | 0.000 | `{"dominance": 18}` |
| maintenance_replacement | middle | 0 | minimal_recent_core | 16.750 | 1 | 0 | 0 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | `{"dominance": 17, "stable_continuation": 1}` |
| maintenance_replacement | middle | 0 | no_quotient | 16.750 | 1 | 18 | 18 | 3.278 | 0.000 | 0.092 | 0.172 | 0.000 | `{"dominance": 18}` |
| maintenance_replacement | middle | 0 | no_scheduler | 16.750 | 1 | 18 | 18 | 3.278 | 0.000 | 0.000 | 0.000 | 0.000 | `{"dominance": 18}` |
| maintenance_replacement | middle | 0 | no_sequence | 16.750 | 1 | 18 | 0 | 0.000 | 0.000 | 0.092 | 0.172 | 0.000 | `{"dominance": 18}` |
| maintenance_replacement | middle | 0 | static_shape | 16.750 | 1 | 0 | 18 | 3.278 | 0.000 | 0.074 | 0.180 | 0.000 | `{"dominance": 17, "stable_continuation": 1}` |
| maintenance_replacement | renewal_like | 0 | full_current | 3.450 | 2 | 18 | 14 | 1.944 | 0.000 | 0.111 | 0.340 | 0.011 | `{"reopen_or_sample": 1, "stable_continuation": 17}` |
| maintenance_replacement | renewal_like | 0 | minimal_recent_core | 3.450 | 2 | 0 | 0 | 0.000 | 0.000 | 0.000 | 0.000 | 0.011 | `{"reopen_or_sample": 1, "stable_continuation": 17}` |
| maintenance_replacement | renewal_like | 0 | no_quotient | 3.450 | 2 | 18 | 14 | 1.944 | 0.000 | 0.111 | 0.340 | 0.011 | `{"reopen_or_sample": 1, "stable_continuation": 17}` |
| maintenance_replacement | renewal_like | 0 | no_scheduler | 3.450 | 2 | 18 | 14 | 1.944 | 0.000 | 0.000 | 0.000 | 0.011 | `{"reopen_or_sample": 1, "stable_continuation": 17}` |
| maintenance_replacement | renewal_like | 0 | no_sequence | 3.450 | 2 | 18 | 0 | 0.000 | 0.000 | 0.112 | 0.340 | 0.011 | `{"reopen_or_sample": 1, "stable_continuation": 17}` |
| maintenance_replacement | renewal_like | 0 | static_shape | 3.450 | 2 | 0 | 14 | 1.944 | 0.000 | 0.096 | 0.348 | 0.011 | `{"reopen_or_sample": 1, "stable_continuation": 17}` |
| maze | static_visible_5x5 | 0 | full_current | -7.000 | 2 | 8 | 7 | 1.125 | 0.500 | 0.042 | 0.068 | 0.000 | `{"dominance": 6, "stable_continuation": 2}` |
| maze | static_visible_5x5 | 0 | minimal_recent_core | -9.000 | 3 | 0 | 0 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | `{"dominance": 6, "stable_continuation": 4}` |
| maze | static_visible_5x5 | 0 | no_quotient | -7.000 | 2 | 8 | 7 | 1.125 | 0.000 | 0.048 | 0.068 | 0.000 | `{"dominance": 6, "stable_continuation": 2}` |
| maze | static_visible_5x5 | 0 | no_scheduler | -7.000 | 2 | 8 | 7 | 1.125 | 0.500 | 0.000 | 0.000 | 0.000 | `{"dominance": 6, "stable_continuation": 2}` |
| maze | static_visible_5x5 | 0 | no_sequence | -9.000 | 3 | 10 | 0 | 0.000 | 0.800 | 0.038 | 0.070 | 0.000 | `{"dominance": 6, "stable_continuation": 4}` |
| maze | static_visible_5x5 | 0 | static_shape | -7.000 | 2 | 0 | 7 | 1.125 | 0.500 | 0.034 | 0.067 | 0.000 | `{"dominance": 6, "stable_continuation": 2}` |
| renewal | noisy_renewal | 0 | full_current | 8.000 | 2 | 16 | 3 | 0.188 | 0.000 | 0.162 | 0.267 | 0.000 | `{"dominance": 11, "reopen_or_sample": 3, "stable_continuation": 2}` |
| renewal | noisy_renewal | 0 | minimal_recent_core | 8.000 | 2 | 0 | 0 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | `{"dominance": 11, "reopen_or_sample": 3, "stable_continuation": 2}` |
| renewal | noisy_renewal | 0 | no_quotient | 8.000 | 2 | 16 | 3 | 0.188 | 0.000 | 0.162 | 0.267 | 0.000 | `{"dominance": 11, "reopen_or_sample": 3, "stable_continuation": 2}` |
| renewal | noisy_renewal | 0 | no_scheduler | 8.000 | 2 | 16 | 3 | 0.188 | 0.000 | 0.000 | 0.000 | 0.000 | `{"dominance": 11, "reopen_or_sample": 3, "stable_continuation": 2}` |
| renewal | noisy_renewal | 0 | no_sequence | 8.000 | 2 | 16 | 0 | 0.000 | 0.000 | 0.162 | 0.267 | 0.000 | `{"dominance": 11, "reopen_or_sample": 3, "stable_continuation": 2}` |
| renewal | noisy_renewal | 0 | static_shape | 10.000 | 2 | 0 | 1 | 0.062 | 0.000 | 0.162 | 0.279 | 0.000 | `{"dominance": 12, "reopen_or_sample": 1, "stable_continuation": 3}` |

## Full-current versus ablation deltas

| family | mode | seed | ablation | metric Δ | prefix action diffs | dyn-step Δ | avg recursion Δ | avg quotient-row Δ |
|---|---|---:|---|---:|---:|---:|---:|---:|
| bandit | easy_public_bandit | 0 | minimal_recent_core | -4.000 | 7 | -16 | -0.190 | 0.000 |
| bandit | easy_public_bandit | 0 | no_quotient | 0.000 | 0 | 0 | 0.000 | 0.000 |
| bandit | easy_public_bandit | 0 | no_scheduler | -4.000 | 7 | 0 | -0.190 | 0.000 |
| bandit | easy_public_bandit | 0 | no_sequence | 0.000 | 0 | 0 | 0.000 | 0.000 |
| bandit | easy_public_bandit | 0 | static_shape | -4.000 | 7 | -16 | 0.008 | 0.000 |
| latent_mechanism | easy_visible | 0 | minimal_recent_core | -22.000 | 11 | -14 | -0.108 | -2.143 |
| latent_mechanism | easy_visible | 0 | no_quotient | -22.000 | 11 | 2 | 0.047 | -2.143 |
| latent_mechanism | easy_visible | 0 | no_scheduler | 0.000 | 0 | 0 | -0.108 | 0.000 |
| latent_mechanism | easy_visible | 0 | no_sequence | 0.000 | 0 | 0 | 0.000 | 0.000 |
| latent_mechanism | easy_visible | 0 | static_shape | -2.000 | 10 | -14 | -0.009 | 0.045 |
| latent_mechanism | hidden_depth2 | 0 | minimal_recent_core | -1.600 | 9 | -16 | -0.370 | -1.500 |
| latent_mechanism | hidden_depth2 | 0 | no_quotient | -1.000 | 11 | 0 | 0.032 | -1.500 |
| latent_mechanism | hidden_depth2 | 0 | no_scheduler | -1.600 | 10 | 0 | -0.370 | -0.125 |
| latent_mechanism | hidden_depth2 | 0 | no_sequence | 0.000 | 0 | 0 | -0.000 | 0.000 |
| latent_mechanism | hidden_depth2 | 0 | static_shape | -1.600 | 9 | -16 | -0.017 | -1.000 |
| maintenance_replacement | bandit_like | 0 | minimal_recent_core | 0.000 | 0 | -18 | -0.006 | -2.000 |
| maintenance_replacement | bandit_like | 0 | no_quotient | 0.000 | 0 | 0 | 0.004 | -2.000 |
| maintenance_replacement | bandit_like | 0 | no_scheduler | 0.000 | 0 | 0 | -0.006 | 0.000 |
| maintenance_replacement | bandit_like | 0 | no_sequence | 0.000 | 0 | 0 | 0.000 | 0.000 |
| maintenance_replacement | bandit_like | 0 | static_shape | 0.000 | 0 | -18 | -0.002 | 0.000 |
| maintenance_replacement | middle | 0 | minimal_recent_core | 0.000 | 0 | -18 | -0.092 | 0.000 |
| maintenance_replacement | middle | 0 | no_quotient | 0.000 | 0 | 0 | 0.000 | 0.000 |
| maintenance_replacement | middle | 0 | no_scheduler | 0.000 | 0 | 0 | -0.092 | 0.000 |
| maintenance_replacement | middle | 0 | no_sequence | 0.000 | 0 | 0 | 0.000 | 0.000 |
| maintenance_replacement | middle | 0 | static_shape | 0.000 | 0 | -18 | -0.018 | 0.000 |
| maintenance_replacement | renewal_like | 0 | minimal_recent_core | 0.000 | 0 | -18 | -0.111 | 0.000 |
| maintenance_replacement | renewal_like | 0 | no_quotient | 0.000 | 0 | 0 | 0.000 | 0.000 |
| maintenance_replacement | renewal_like | 0 | no_scheduler | 0.000 | 0 | 0 | -0.111 | 0.000 |
| maintenance_replacement | renewal_like | 0 | no_sequence | 0.000 | 0 | 0 | 0.000 | 0.000 |
| maintenance_replacement | renewal_like | 0 | static_shape | 0.000 | 0 | -18 | -0.015 | 0.000 |
| maze | static_visible_5x5 | 0 | minimal_recent_core | -2.000 | 5 | -8 | -0.042 | -0.500 |
| maze | static_visible_5x5 | 0 | no_quotient | 0.000 | 0 | 0 | 0.006 | -0.500 |
| maze | static_visible_5x5 | 0 | no_scheduler | 0.000 | 0 | 0 | -0.042 | 0.000 |
| maze | static_visible_5x5 | 0 | no_sequence | -2.000 | 5 | 2 | -0.004 | 0.300 |
| maze | static_visible_5x5 | 0 | static_shape | 0.000 | 0 | -8 | -0.008 | 0.000 |
| renewal | noisy_renewal | 0 | minimal_recent_core | 0.000 | 0 | -16 | -0.162 | 0.000 |
| renewal | noisy_renewal | 0 | no_quotient | 0.000 | 0 | 0 | 0.000 | 0.000 |
| renewal | noisy_renewal | 0 | no_scheduler | 0.000 | 0 | 0 | -0.162 | 0.000 |
| renewal | noisy_renewal | 0 | no_sequence | 0.000 | 0 | 0 | 0.000 | 0.000 |
| renewal | noisy_renewal | 0 | static_shape | 2.000 | 2 | -16 | -0.000 | 0.000 |

## Interpretation boundary

This map is useful only for first-pass diagnosis: mechanism visibility, rough behavioral sensitivity, and failure discovery. It should not be cited as benchmark evidence or as evidence that CO is useful/novel.
