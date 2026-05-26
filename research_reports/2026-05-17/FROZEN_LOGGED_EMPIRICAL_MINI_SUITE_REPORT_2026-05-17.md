# Frozen Logged Empirical Mini-Suite Report — 2026-05-17

## Claim boundary

Frozen logged empirical mini-suite only: checks execution, logging, explicit public baselines, and structural telemetry preservation. It is not benchmark evidence, not tuning evidence, not CO proof, and not an RCF novelty claim.

## Scope

This suite runs fixed small episodes/seeds across the active families with explicit public baselines and CO.
It is the first frozen logged mini-suite after structural/formula gates, not a reward benchmark.

## Outputs

- `ChangeOntCode/outputs/frozen_logged_empirical_mini_suite_v1/runs.jsonl`
- `ChangeOntCode/outputs/frozen_logged_empirical_mini_suite_v1/structural_telemetry.jsonl`
- `ChangeOntCode/outputs/frozen_logged_empirical_mini_suite_v1/summary.json`
- `ChangeOntCode/outputs/frozen_logged_empirical_mini_suite_v1/suite_manifest.json`

## Summary

```json
{
  "aggregate": {
    "bandit/easy/CO_canonical_core": {
      "mean_metric_value": 16.799999999999994,
      "metric_name": "final_cumulative_regret",
      "runs": 1,
      "values": [
        16.799999999999994
      ]
    },
    "bandit/easy/kl_ucb": {
      "mean_metric_value": 2.6000000000000005,
      "metric_name": "final_cumulative_regret",
      "runs": 1,
      "values": [
        2.6000000000000005
      ]
    },
    "bandit/easy/ucb1": {
      "mean_metric_value": 5.200000000000001,
      "metric_name": "final_cumulative_regret",
      "runs": 1,
      "values": [
        5.200000000000001
      ]
    },
    "latent_mechanism/easy_visible/CO_canonical_core": {
      "mean_metric_value": 1.0,
      "metric_name": "success",
      "runs": 1,
      "values": [
        1.0
      ]
    },
    "latent_mechanism/easy_visible/heuristic": {
      "mean_metric_value": 0.0,
      "metric_name": "success",
      "runs": 1,
      "values": [
        0.0
      ]
    },
    "latent_mechanism/easy_visible/random": {
      "mean_metric_value": 0.0,
      "metric_name": "success",
      "runs": 1,
      "values": [
        0.0
      ]
    },
    "latent_mechanism/hidden_depth2/CO_canonical_core": {
      "mean_metric_value": 0.0,
      "metric_name": "success",
      "runs": 1,
      "values": [
        0.0
      ]
    },
    "latent_mechanism/hidden_depth2/heuristic": {
      "mean_metric_value": 0.0,
      "metric_name": "success",
      "runs": 1,
      "values": [
        0.0
      ]
    },
    "latent_mechanism/hidden_depth2/random": {
      "mean_metric_value": 0.0,
      "metric_name": "success",
      "runs": 1,
      "values": [
        0.0
      ]
    },
    "maintenance_replacement/bandit_like/co": {
      "mean_metric_value": 49.25,
      "metric_name": "total_reward",
      "runs": 1,
      "values": [
        49.25
      ]
    },
    "maintenance_replacement/bandit_like/finite_horizon_dp": {
      "mean_metric_value": 55.0,
      "metric_name": "total_reward",
      "runs": 1,
      "values": [
        55.0
      ]
    },
    "maintenance_replacement/bandit_like/random": {
      "mean_metric_value": -43.70000000000001,
      "metric_name": "total_reward",
      "runs": 1,
      "values": [
        -43.70000000000001
      ]
    },
    "maintenance_replacement/bandit_like/threshold": {
      "mean_metric_value": 56.25,
      "metric_name": "total_reward",
      "runs": 1,
      "values": [
        56.25
      ]
    },
    "maintenance_replacement/middle/co": {
      "mean_metric_value": 42.25000000000001,
      "metric_name": "total_reward",
      "runs": 1,
      "values": [
        42.25000000000001
      ]
    },
    "maintenance_replacement/middle/random": {
      "mean_metric_value": -30.800000000000033,
      "metric_name": "total_reward",
      "runs": 1,
      "values": [
        -30.800000000000033
      ]
    },
    "maintenance_replacement/middle/threshold": {
      "mean_metric_value": 61.350000000000016,
      "metric_name": "total_reward",
      "runs": 1,
      "values": [
        61.350000000000016
      ]
    },
    "maze/maze_5x5/CO_canonical_core": {
      "mean_metric_value": -9.0,
      "metric_name": "episode_return",
      "runs": 1,
      "values": [
        -9.0
      ]
    },
    "maze/maze_5x5/astar": {
      "mean_metric_value": -7.0,
      "metric_name": "episode_return",
      "runs": 1,
      "values": [
        -7.0
      ]
    },
    "maze/maze_5x5/bfs": {
      "mean_metric_value": -7.0,
      "metric_name": "episode_return",
      "runs": 1,
      "values": [
        -7.0
      ]
    },
    "renewal/clean/CO_canonical_core": {
      "mean_metric_value": 15.0,
      "metric_name": "final_cum_reward",
      "runs": 1,
      "values": [
        15.0
      ]
    },
    "renewal/clean/last": {
      "mean_metric_value": 7.0,
      "metric_name": "final_cum_reward",
      "runs": 1,
      "values": [
        7.0
      ]
    },
    "renewal/clean/phase": {
      "mean_metric_value": 22.0,
      "metric_name": "final_cum_reward",
      "runs": 1,
      "values": [
        22.0
      ]
    },
    "renewal/clean/vom": {
      "mean_metric_value": 6.0,
      "metric_name": "final_cum_reward",
      "runs": 1,
      "values": [
        6.0
      ]
    }
  },
  "baseline_runs": 16,
  "claim_boundary": "Frozen logged empirical mini-suite only: checks execution, logging, explicit public baselines, and structural telemetry preservation. It is not benchmark evidence, not tuning evidence, not CO proof, and not an RCF novelty claim.",
  "co_runs": 7,
  "completed_at": "2026-05-17T13:40:27.703939+00:00",
  "families": [
    "bandit",
    "latent_mechanism",
    "maintenance_replacement",
    "maze",
    "renewal"
  ],
  "outputs": {
    "runs_jsonl": "outputs/frozen_logged_empirical_mini_suite_v1/runs.jsonl",
    "structural_telemetry_jsonl": "outputs/frozen_logged_empirical_mini_suite_v1/structural_telemetry.jsonl",
    "suite_manifest": "outputs/frozen_logged_empirical_mini_suite_v1/suite_manifest.json"
  },
  "runs": 23,
  "structural_telemetry": {
    "canonical_modes": {
      "dominance": 182,
      "reopen_or_sample": 26,
      "stable_continuation": 30
    },
    "records": 238,
    "records_by_family": {
      "bandit": 24,
      "latent_mechanism": 40,
      "maintenance_replacement": 140,
      "maze": 10,
      "renewal": 24
    },
    "structural_step_records_missing_basic_co_fields": 0
  },
  "study": "frozen_logged_empirical_mini_suite_v1"
}
```

## Interpretation boundary

These numbers only show that the frozen runtime executes, logs, and can be compared against explicit public baselines without tuning. Broad empirical or novelty claims remain disallowed.
