# Pass-1 All-Problem CO vs STOA/Baseline Comparison — 2026-05-25

## Claim boundary

Pass-1 bounded diagnostic comparison only: current active problem families, small seed count, capped horizons, no post-result tuning, public baselines labelled. This is not proof of CO usefulness, not novelty evidence, and not publication-grade SOTA evidence.

## Procedure

- Derived six-question shape reports from each adapter's public `problem_contract` before scoring results.
- Ran CO through the canonical current kernel manifest.
- Ran explicit repo-available public baselines/STOA-style baselines per active family/mode.
- Used small seed count and capped horizons to avoid timeouts; this is diagnostic, not publication-grade evidence.
- Finite-horizon DP is skipped outside direct public health observation to avoid hidden-state oracle leakage.

## CO vs best public baseline summary

| family/mode | metric | direction | CO mean | best baseline | best mean | CO-best | favorable? |
|---|---:|---|---:|---|---:|---:|---|
| bandit/easy_public_bandit | final_cumulative_regret | lower_is_better | 56.8667 | ts | 6.1667 | 50.7000 | False |
| renewal/noisy_renewal | mean_reward | higher_is_better | 0.4115 | phase | 0.8568 | -0.4453 | False |

## Interpretation

This comparison is a first bounded pass over current active problem families. It should be used to identify failure modes and where CO is or is not competitive under the current rough kernel. It must not be used to tune coefficients or claim proof of CO.

## Full JSON summary

```json
{
  "aggregates": {
    "bandit/easy_public_bandit/co": {
      "agent": "co",
      "baseline_type": "co",
      "family": "bandit",
      "mean_metric_value": 56.86666666666668,
      "mean_runtime_seconds": 3.9642978870003085,
      "metric_direction": "lower_is_better",
      "metric_name": "final_cumulative_regret",
      "mode": "easy_public_bandit",
      "runs": 3,
      "std_population": 33.66504946610886,
      "values": [
        9.299999999999999,
        82.40000000000008,
        78.89999999999996
      ]
    },
    "bandit/easy_public_bandit/epsgreedy": {
      "agent": "epsgreedy",
      "baseline_type": "public_stoa_baseline",
      "family": "bandit",
      "mean_metric_value": 18.899999999999995,
      "mean_runtime_seconds": 0.0003665153332500874,
      "metric_direction": "lower_is_better",
      "metric_name": "final_cumulative_regret",
      "mode": "easy_public_bandit",
      "runs": 3,
      "std_population": 7.537019746999912,
      "values": [
        28.99999999999999,
        16.799999999999994,
        10.899999999999999
      ]
    },
    "bandit/easy_public_bandit/kl_ucb": {
      "agent": "kl_ucb",
      "baseline_type": "public_stoa_baseline",
      "family": "bandit",
      "mean_metric_value": 8.1,
      "mean_runtime_seconds": 0.008679867332830327,
      "metric_direction": "lower_is_better",
      "metric_name": "final_cumulative_regret",
      "mode": "easy_public_bandit",
      "runs": 3,
      "std_population": 1.2027745701779131,
      "values": [
        8.899999999999999,
        9.0,
        6.400000000000002
      ]
    },
    "bandit/easy_public_bandit/ts": {
      "agent": "ts",
      "baseline_type": "public_stoa_baseline",
      "family": "bandit",
      "mean_metric_value": 6.166666666666667,
      "mean_runtime_seconds": 0.001214386666106293,
      "metric_direction": "lower_is_better",
      "metric_name": "final_cumulative_regret",
      "mode": "easy_public_bandit",
      "runs": 3,
      "std_population": 0.97410927974683,
      "values": [
        5.200000000000001,
        5.800000000000001,
        7.5
      ]
    },
    "bandit/easy_public_bandit/ucb1": {
      "agent": "ucb1",
      "baseline_type": "public_stoa_baseline",
      "family": "bandit",
      "mean_metric_value": 13.33333333333333,
      "mean_runtime_seconds": 0.0005589833326666849,
      "metric_direction": "lower_is_better",
      "metric_name": "final_cumulative_regret",
      "mode": "easy_public_bandit",
      "runs": 3,
      "std_population": 1.065624490876384,
      "values": [
        12.899999999999999,
        14.799999999999995,
        12.299999999999999
      ]
    },
    "renewal/noisy_renewal/co": {
      "agent": "co",
      "baseline_type": "co",
      "family": "renewal",
      "mean_metric_value": 0.4114583333333333,
      "mean_runtime_seconds": 4.639578456333766,
      "metric_direction": "higher_is_better",
      "metric_name": "mean_reward",
      "mode": "noisy_renewal",
      "runs": 3,
      "std_population": 0.049547649975105336,
      "values": [
        0.4609375,
        0.34375,
        0.4296875
      ]
    },
    "renewal/noisy_renewal/last": {
      "agent": "last",
      "baseline_type": "public_stoa_baseline",
      "family": "renewal",
      "mean_metric_value": 0.2526041666666667,
      "mean_runtime_seconds": 0.0002533063337371762,
      "metric_direction": "higher_is_better",
      "metric_name": "mean_reward",
      "mode": "noisy_renewal",
      "runs": 3,
      "std_population": 0.07663509879980292,
      "values": [
        0.2578125,
        0.15625,
        0.34375
      ]
    },
    "renewal/noisy_renewal/ngram": {
      "agent": "ngram",
      "baseline_type": "public_stoa_baseline",
      "family": "renewal",
      "mean_metric_value": 0.2552083333333333,
      "mean_runtime_seconds": 0.00037957999969269923,
      "metric_direction": "higher_is_better",
      "metric_name": "mean_reward",
      "mode": "noisy_renewal",
      "runs": 3,
      "std_population": 0.04830009633070679,
      "values": [
        0.28125,
        0.1875,
        0.296875
      ]
    },
    "renewal/noisy_renewal/phase": {
      "agent": "phase",
      "baseline_type": "public_stoa_baseline",
      "family": "renewal",
      "mean_metric_value": 0.8567708333333334,
      "mean_runtime_seconds": 0.0002558383330324432,
      "metric_direction": "higher_is_better",
      "metric_name": "mean_reward",
      "mode": "noisy_renewal",
      "runs": 3,
      "std_population": 0.03513212907091678,
      "values": [
        0.90625,
        0.8359375,
        0.828125
      ]
    },
    "renewal/noisy_renewal/vom": {
      "agent": "vom",
      "baseline_type": "public_stoa_baseline",
      "family": "renewal",
      "mean_metric_value": 0.2552083333333333,
      "mean_runtime_seconds": 0.0007803070002410095,
      "metric_direction": "higher_is_better",
      "metric_name": "mean_reward",
      "mode": "noisy_renewal",
      "runs": 3,
      "std_population": 0.04830009633070679,
      "values": [
        0.28125,
        0.1875,
        0.296875
      ]
    }
  },
  "bounded_run_settings": {
    "bandit_horizon": 128,
    "latent_max_steps": 64,
    "maintenance_native_horizons": "regime defaults: 60/80/100",
    "maze_max_steps": 96,
    "renewal_horizon": 128
  },
  "claim_boundary": "Pass-1 bounded diagnostic comparison only: current active problem families, small seed count, capped horizons, no post-result tuning, public baselines labelled. This is not proof of CO usefulness, not novelty evidence, and not publication-grade SOTA evidence.",
  "co_vs_best_baseline": {
    "bandit/easy_public_bandit": {
      "best_baseline_agent": "ts",
      "best_baseline_mean": 6.166666666666667,
      "claim_boundary": "small-N bounded diagnostic only; do not tune constants from this comparison",
      "co_favorable_vs_best_baseline": false,
      "co_mean": 56.86666666666668,
      "co_minus_best_baseline": 50.70000000000002,
      "metric_direction": "lower_is_better",
      "metric_name": "final_cumulative_regret"
    },
    "renewal/noisy_renewal": {
      "best_baseline_agent": "phase",
      "best_baseline_mean": 0.8567708333333334,
      "claim_boundary": "small-N bounded diagnostic only; do not tune constants from this comparison",
      "co_favorable_vs_best_baseline": false,
      "co_mean": 0.4114583333333333,
      "co_minus_best_baseline": -0.44531250000000006,
      "metric_direction": "higher_is_better",
      "metric_name": "mean_reward"
    }
  },
  "completed_at": "2026-05-25T14:28:15.597648+00:00",
  "errors": [],
  "execution_note": "Default execution uses one subprocess per family to avoid timeout/state accumulation in this environment. The same family run functions are used; results are appended to one JSONL file and aggregated after all families complete.",
  "families": [
    "bandit",
    "renewal"
  ],
  "modes": [
    "bandit/easy_public_bandit",
    "renewal/noisy_renewal"
  ],
  "non_claims": [
    "Not a publication-grade SOTA suite.",
    "Not broad empirical proof.",
    "Do not tune constants from this result.",
    "Some baselines are strong public baselines, some are simple public heuristics; labels must be preserved."
  ],
  "outputs": {
    "report_md": "research_reports/2026-05-25/PASS1_ALL_PROBLEM_STOA_COMPARISON_REPORT_2026-05-25.md",
    "runs_jsonl": "outputs/pass1_all_problem_stoa_comparison_v1/runs.jsonl",
    "shape_reports_json": "outputs/pass1_all_problem_stoa_comparison_v1/shape_reports.json",
    "summary_json": "outputs/pass1_all_problem_stoa_comparison_v1/summary.json"
  },
  "performance_rows": 30,
  "raw_rows": 30,
  "seeds": [
    0,
    1,
    2
  ],
  "shape_report_count": 8,
  "skipped_rows": 0,
  "started_at": "family-by-family subprocess execution; see row runtime_seconds",
  "status": "executed_family_by_family_timeout_safe",
  "study": "pass1_all_problem_stoa_comparison_v1"
}
```
