# Focused Frozen Empirical Mini-Benchmark Report — 2026-05-17

## Empirical question

With the structural baseline and constants frozen, does the current CO kernel execute reproducibly against explicit public baselines in burden/hiddenness-sensitive settings while preserving structural telemetry and without hidden fallback or post-result tuning?

## Claim boundary

Focused frozen empirical mini-benchmark only: preliminary, small-N, no post-result tuning, explicit public baselines, structural telemetry required. It is not broad benchmark evidence, not CO proof, not novelty evidence, and not grounds for coefficient adjustment.

## Scope

This is the first small frozen benchmark-shaped run after structural/formula gates. It focuses on the maintenance/replacement family because its direct, partial, and hidden regimes directly exercise hiddenness, burden carrying, exposure, and resolver behavior. It remains too small for broad empirical claims.

## Outputs

- `ChangeOntCode/outputs/focused_frozen_empirical_mini_benchmark_v1/runs.jsonl`
- `ChangeOntCode/outputs/focused_frozen_empirical_mini_benchmark_v1/structural_telemetry.jsonl`
- `ChangeOntCode/outputs/focused_frozen_empirical_mini_benchmark_v1/summary.json`
- `ChangeOntCode/outputs/focused_frozen_empirical_mini_benchmark_v1/suite_manifest.json`

## Preliminary finding

Across three frozen seeds, CO underperforms the best public baseline in `bandit_like` and `middle` maintenance regimes, but outperforms the simple public threshold baselines in the hidden `renewal_like` regime. This is a diagnostic pattern, not a success claim: it suggests CO's current structure may be most relevant when hiddenness/renewal pressure is active, while direct/partial regimes still expose weakness against simple public control-limit policies.

Do not tune constants from this result. The next task is trace-level failure analysis: why does CO lose in `middle`, why does it do well in `renewal_like`, and which structural mechanisms are responsible?

## Summary

```json
{
  "aggregate": {
    "maintenance_replacement/bandit_like/co": {
      "baseline_type": "co",
      "mean_metric_value": 52.583333333333336,
      "metric_direction": "higher_is_better",
      "metric_name": "total_reward",
      "parity_label": "same_episode_seed_public_observation; finite_horizon_dp only used for direct-observation regime",
      "runs": 3,
      "std_population": 5.253305837491496,
      "values": [
        49.25,
        48.5,
        60.0
      ]
    },
    "maintenance_replacement/bandit_like/finite_horizon_dp": {
      "baseline_type": "public_known_model_baseline",
      "mean_metric_value": 57.5,
      "metric_direction": "higher_is_better",
      "metric_name": "total_reward",
      "parity_label": "same_episode_seed_public_observation; finite_horizon_dp only used for direct-observation regime",
      "runs": 3,
      "std_population": 2.041241452319315,
      "values": [
        55.0,
        57.5,
        60.0
      ]
    },
    "maintenance_replacement/bandit_like/threshold": {
      "baseline_type": "public_baseline",
      "mean_metric_value": 54.916666666666664,
      "metric_direction": "higher_is_better",
      "metric_name": "total_reward",
      "parity_label": "same_episode_seed_public_observation; finite_horizon_dp only used for direct-observation regime",
      "runs": 3,
      "std_population": 4.788585966186214,
      "values": [
        56.25,
        48.5,
        60.0
      ]
    },
    "maintenance_replacement/middle/co": {
      "baseline_type": "co",
      "mean_metric_value": 44.900000000000006,
      "metric_direction": "higher_is_better",
      "metric_name": "total_reward",
      "parity_label": "same_episode_seed_public_observation; finite_horizon_dp only used for direct-observation regime",
      "runs": 3,
      "std_population": 3.40024508920558,
      "values": [
        42.25000000000001,
        49.7,
        42.75
      ]
    },
    "maintenance_replacement/middle/threshold": {
      "baseline_type": "public_baseline",
      "mean_metric_value": 60.30000000000001,
      "metric_direction": "higher_is_better",
      "metric_name": "total_reward",
      "parity_label": "same_episode_seed_public_observation; finite_horizon_dp only used for direct-observation regime",
      "runs": 3,
      "std_population": 0.8031189202104548,
      "values": [
        61.350000000000016,
        60.150000000000006,
        59.400000000000006
      ]
    },
    "maintenance_replacement/middle/threshold_opt": {
      "baseline_type": "public_baseline",
      "mean_metric_value": 60.30000000000001,
      "metric_direction": "higher_is_better",
      "metric_name": "total_reward",
      "parity_label": "same_episode_seed_public_observation; finite_horizon_dp only used for direct-observation regime",
      "runs": 3,
      "std_population": 0.8031189202104548,
      "values": [
        61.350000000000016,
        60.150000000000006,
        59.400000000000006
      ]
    },
    "maintenance_replacement/renewal_like/co": {
      "baseline_type": "co",
      "mean_metric_value": -4.799999999999995,
      "metric_direction": "higher_is_better",
      "metric_name": "total_reward",
      "parity_label": "same_episode_seed_public_observation; finite_horizon_dp only used for direct-observation regime",
      "runs": 3,
      "std_population": 1.8497747610632687,
      "values": [
        -2.1999999999999935,
        -6.349999999999996,
        -5.849999999999998
      ]
    },
    "maintenance_replacement/renewal_like/threshold": {
      "baseline_type": "public_baseline",
      "mean_metric_value": -35.35,
      "metric_direction": "higher_is_better",
      "metric_name": "total_reward",
      "parity_label": "same_episode_seed_public_observation; finite_horizon_dp only used for direct-observation regime",
      "runs": 3,
      "std_population": 10.142731387550397,
      "values": [
        -22.35,
        -47.1,
        -36.6
      ]
    },
    "maintenance_replacement/renewal_like/threshold_opt": {
      "baseline_type": "public_baseline",
      "mean_metric_value": -35.35,
      "metric_direction": "higher_is_better",
      "metric_name": "total_reward",
      "parity_label": "same_episode_seed_public_observation; finite_horizon_dp only used for direct-observation regime",
      "runs": 3,
      "std_population": 10.142731387550397,
      "values": [
        -22.35,
        -47.1,
        -36.6
      ]
    }
  },
  "baseline_runs": 18,
  "claim_boundary": "Focused frozen empirical mini-benchmark only: preliminary, small-N, no post-result tuning, explicit public baselines, structural telemetry required. It is not broad benchmark evidence, not CO proof, not novelty evidence, and not grounds for coefficient adjustment.",
  "co_runs": 9,
  "co_vs_best_public_baseline": {
    "maintenance_replacement/bandit_like": {
      "best_public_baseline_agent": "finite_horizon_dp",
      "best_public_baseline_mean": 57.5,
      "co_favorable_vs_best_public_baseline": false,
      "co_mean": 52.583333333333336,
      "co_minus_best_public_baseline": -4.916666666666664,
      "interpretation_boundary": "small-N preliminary only; do not tune constants from this comparison",
      "metric_direction": "higher_is_better"
    },
    "maintenance_replacement/middle": {
      "best_public_baseline_agent": "threshold",
      "best_public_baseline_mean": 60.30000000000001,
      "co_favorable_vs_best_public_baseline": false,
      "co_mean": 44.900000000000006,
      "co_minus_best_public_baseline": -15.400000000000006,
      "interpretation_boundary": "small-N preliminary only; do not tune constants from this comparison",
      "metric_direction": "higher_is_better"
    },
    "maintenance_replacement/renewal_like": {
      "best_public_baseline_agent": "threshold",
      "best_public_baseline_mean": -35.35,
      "co_favorable_vs_best_public_baseline": true,
      "co_mean": -4.799999999999995,
      "co_minus_best_public_baseline": 30.550000000000004,
      "interpretation_boundary": "small-N preliminary only; do not tune constants from this comparison",
      "metric_direction": "higher_is_better"
    }
  },
  "completed_at": "2026-05-17T14:19:54.430929+00:00",
  "empirical_question": "With the structural baseline and constants frozen, does the current CO kernel execute reproducibly against explicit public baselines in burden/hiddenness-sensitive settings while preserving structural telemetry and without hidden fallback or post-result tuning?",
  "families": [
    "maintenance_replacement"
  ],
  "outputs": {
    "runs_jsonl": "outputs/focused_frozen_empirical_mini_benchmark_v1/runs.jsonl",
    "structural_telemetry_jsonl": "outputs/focused_frozen_empirical_mini_benchmark_v1/structural_telemetry.jsonl",
    "suite_manifest": "outputs/focused_frozen_empirical_mini_benchmark_v1/suite_manifest.json"
  },
  "runs": 27,
  "seeds": [
    0,
    1,
    2
  ],
  "structural_telemetry": {
    "canonical_modes": {
      "dominance": 360,
      "reopen_or_sample": 3,
      "stable_continuation": 357
    },
    "certificate_aware_reopen_or_sample_records": 3,
    "certificate_aware_stable_continuation_records": 0,
    "records": 720,
    "records_by_family": {
      "maintenance_replacement": 720
    },
    "structural_step_records_missing_basic_co_fields": 0
  },
  "study": "focused_frozen_empirical_mini_benchmark_v1"
}
```

## Interpretation boundary

Use this result to find failures, logging defects, or gross regressions. Do not use it to tune constants or claim CO superiority.

## Post-report status update — shape-gauged resolver timing

This report was generated before the 2026-05-17 shape-gauged pre-blocking resolver-timing update.  Its results are retained as historical diagnostic evidence for the prior baseline only.  They must not be cited as current-baseline empirical evidence.

Current next action: rerun a focused frozen mini-benchmark only after the shape-gauged timing update is accepted as part of the frozen baseline and its formula constants are frozen.
