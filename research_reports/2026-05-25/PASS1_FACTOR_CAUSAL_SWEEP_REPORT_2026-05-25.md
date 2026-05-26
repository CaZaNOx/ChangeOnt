# Pass-1 Factor / Causal Sweep — 2026-05-25

## Claim boundary

Diagnostic factor sweep only. Counterfactual shapes/readout parameters are not canonical, not tuned outputs, and not evidence for publication claims. The goal is causal understanding: which generic factors explain current CO behavior and where performance deficits remain after plausible factor variation.

## What varied

- kernel mechanism toggles: dynamic shape, quotient, scheduler, sequence, all recent core off;
- dynamic-shape update rate;
- counterfactual public shape profiles;
- generic readout resolver gate permissive/conservative settings;
- repo-available baselines/STOA references per family.

## Main comparison table

| family/mode | metric | canonical CO | best baseline | best baseline mean | best CO variant | best CO variant mean | canonical-best baseline | best CO-best baseline | best variant improvement |
|---|---|---:|---|---:|---|---:|---:|---:|---:|
| bandit/easy_public_bandit | final_cumulative_regret (lower_is_better) | 9.3000 | ts | 1.9000 | co_shape_flat_mid | 5.2000 | 7.4000 | 3.3000 | 4.1000 |
| renewal/noisy_renewal | mean_reward (higher_is_better) | 0.5000 | phase | 0.9167 | co_shape_local_fast | 0.6250 | -0.4167 | -0.2917 | 0.1250 |

## Factor interpretation

### bandit/easy_public_bandit

- Canonical CO vs best baseline delta: `7.4000`.
- Best CO variant: `co_shape_flat_mid`; delta vs best baseline: `3.3000`.
- `canonical` range: `0.0000`, best within group: `co_canonical`.
- `dynamic_alpha` range: `8.8000`, best within group: `co_dynamic_alpha_high`.
- `mechanism_ablation` range: `7.5000`, best within group: `co_no_quotient`.
- `readout_gate` range: `0.0000`, best within group: `co_readout_resolver_conservative`.
- `shape_counterfactual` range: `11.6000`, best within group: `co_shape_flat_mid`.

### renewal/noisy_renewal

- Canonical CO vs best baseline delta: `-0.4167`.
- Best CO variant: `co_shape_local_fast`; delta vs best baseline: `-0.2917`.
- `canonical` range: `0.0000`, best within group: `co_canonical`.
- `dynamic_alpha` range: `0.0417`, best within group: `co_dynamic_alpha_low`.
- `mechanism_ablation` range: `0.1250`, best within group: `co_static_shape`.
- `readout_gate` range: `0.0417`, best within group: `co_readout_resolver_conservative`.
- `shape_counterfactual` range: `0.5833`, best within group: `co_shape_local_fast`.

## Cold interpretation

If a counterfactual shape or readout variant improves CO but still remains below the best baseline, the deficit is not explained by that factor alone. If disabling recent mechanisms improves CO, the new mechanism may be misweighted or harmful in that family. If all variants remain far below baseline, the likely cause is deeper adapter/readout/objective mismatch or that the classical baseline is well matched to the family.

## Full JSON summary

```json
{
  "aggregates": {
    "bandit/easy_public_bandit/co_canonical": {
      "agent": "co_canonical",
      "agent_kind": "co_variant",
      "family": "bandit",
      "mean_metric_value": 9.299999999999999,
      "metric_direction": "lower_is_better",
      "metric_name": "final_cumulative_regret",
      "mode": "easy_public_bandit",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        9.299999999999999
      ]
    },
    "bandit/easy_public_bandit/co_dynamic_alpha_high": {
      "agent": "co_dynamic_alpha_high",
      "agent_kind": "co_variant",
      "family": "bandit",
      "mean_metric_value": 8.0,
      "metric_direction": "lower_is_better",
      "metric_name": "final_cumulative_regret",
      "mode": "easy_public_bandit",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        8.0
      ]
    },
    "bandit/easy_public_bandit/co_dynamic_alpha_low": {
      "agent": "co_dynamic_alpha_low",
      "agent_kind": "co_variant",
      "family": "bandit",
      "mean_metric_value": 16.799999999999994,
      "metric_direction": "lower_is_better",
      "metric_name": "final_cumulative_regret",
      "mode": "easy_public_bandit",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        16.799999999999994
      ]
    },
    "bandit/easy_public_bandit/co_minimal_recent_core": {
      "agent": "co_minimal_recent_core",
      "agent_kind": "co_variant",
      "family": "bandit",
      "mean_metric_value": 16.799999999999994,
      "metric_direction": "lower_is_better",
      "metric_name": "final_cumulative_regret",
      "mode": "easy_public_bandit",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        16.799999999999994
      ]
    },
    "bandit/easy_public_bandit/co_no_quotient": {
      "agent": "co_no_quotient",
      "agent_kind": "co_variant",
      "family": "bandit",
      "mean_metric_value": 9.299999999999999,
      "metric_direction": "lower_is_better",
      "metric_name": "final_cumulative_regret",
      "mode": "easy_public_bandit",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        9.299999999999999
      ]
    },
    "bandit/easy_public_bandit/co_no_scheduler": {
      "agent": "co_no_scheduler",
      "agent_kind": "co_variant",
      "family": "bandit",
      "mean_metric_value": 16.799999999999994,
      "metric_direction": "lower_is_better",
      "metric_name": "final_cumulative_regret",
      "mode": "easy_public_bandit",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        16.799999999999994
      ]
    },
    "bandit/easy_public_bandit/co_no_sequence": {
      "agent": "co_no_sequence",
      "agent_kind": "co_variant",
      "family": "bandit",
      "mean_metric_value": 9.299999999999999,
      "metric_direction": "lower_is_better",
      "metric_name": "final_cumulative_regret",
      "mode": "easy_public_bandit",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        9.299999999999999
      ]
    },
    "bandit/easy_public_bandit/co_readout_resolver_conservative": {
      "agent": "co_readout_resolver_conservative",
      "agent_kind": "co_variant",
      "family": "bandit",
      "mean_metric_value": 9.299999999999999,
      "metric_direction": "lower_is_better",
      "metric_name": "final_cumulative_regret",
      "mode": "easy_public_bandit",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        9.299999999999999
      ]
    },
    "bandit/easy_public_bandit/co_readout_resolver_permissive": {
      "agent": "co_readout_resolver_permissive",
      "agent_kind": "co_variant",
      "family": "bandit",
      "mean_metric_value": 9.299999999999999,
      "metric_direction": "lower_is_better",
      "metric_name": "final_cumulative_regret",
      "mode": "easy_public_bandit",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        9.299999999999999
      ]
    },
    "bandit/easy_public_bandit/co_shape_flat_mid": {
      "agent": "co_shape_flat_mid",
      "agent_kind": "co_variant",
      "family": "bandit",
      "mean_metric_value": 5.200000000000001,
      "metric_direction": "lower_is_better",
      "metric_name": "final_cumulative_regret",
      "mode": "easy_public_bandit",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        5.200000000000001
      ]
    },
    "bandit/easy_public_bandit/co_shape_hidden_long": {
      "agent": "co_shape_hidden_long",
      "agent_kind": "co_variant",
      "family": "bandit",
      "mean_metric_value": 7.8000000000000025,
      "metric_direction": "lower_is_better",
      "metric_name": "final_cumulative_regret",
      "mode": "easy_public_bandit",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        7.8000000000000025
      ]
    },
    "bandit/easy_public_bandit/co_shape_local_fast": {
      "agent": "co_shape_local_fast",
      "agent_kind": "co_variant",
      "family": "bandit",
      "mean_metric_value": 16.799999999999994,
      "metric_direction": "lower_is_better",
      "metric_name": "final_cumulative_regret",
      "mode": "easy_public_bandit",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        16.799999999999994
      ]
    },
    "bandit/easy_public_bandit/co_shape_rigid_topology": {
      "agent": "co_shape_rigid_topology",
      "agent_kind": "co_variant",
      "family": "bandit",
      "mean_metric_value": 6.5,
      "metric_direction": "lower_is_better",
      "metric_name": "final_cumulative_regret",
      "mode": "easy_public_bandit",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        6.5
      ]
    },
    "bandit/easy_public_bandit/co_static_shape": {
      "agent": "co_static_shape",
      "agent_kind": "co_variant",
      "family": "bandit",
      "mean_metric_value": 16.799999999999994,
      "metric_direction": "lower_is_better",
      "metric_name": "final_cumulative_regret",
      "mode": "easy_public_bandit",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        16.799999999999994
      ]
    },
    "bandit/easy_public_bandit/epsgreedy": {
      "agent": "epsgreedy",
      "agent_kind": "baseline",
      "family": "bandit",
      "mean_metric_value": 16.799999999999994,
      "metric_direction": "lower_is_better",
      "metric_name": "final_cumulative_regret",
      "mode": "easy_public_bandit",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        16.799999999999994
      ]
    },
    "bandit/easy_public_bandit/kl_ucb": {
      "agent": "kl_ucb",
      "agent_kind": "baseline",
      "family": "bandit",
      "mean_metric_value": 2.6000000000000005,
      "metric_direction": "lower_is_better",
      "metric_name": "final_cumulative_regret",
      "mode": "easy_public_bandit",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        2.6000000000000005
      ]
    },
    "bandit/easy_public_bandit/ts": {
      "agent": "ts",
      "agent_kind": "baseline",
      "family": "bandit",
      "mean_metric_value": 1.9000000000000004,
      "metric_direction": "lower_is_better",
      "metric_name": "final_cumulative_regret",
      "mode": "easy_public_bandit",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        1.9000000000000004
      ]
    },
    "bandit/easy_public_bandit/ucb1": {
      "agent": "ucb1",
      "agent_kind": "baseline",
      "family": "bandit",
      "mean_metric_value": 5.200000000000001,
      "metric_direction": "lower_is_better",
      "metric_name": "final_cumulative_regret",
      "mode": "easy_public_bandit",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        5.200000000000001
      ]
    },
    "maze/static_visible_5x5/co_canonical": {
      "agent": "co_canonical",
      "agent_kind": "co_variant",
      "family": "maze",
      "mean_metric_value": -7.0,
      "metric_direction": "higher_is_better",
      "metric_name": "episode_return",
      "mode": "static_visible_5x5",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        -7.0
      ]
    },
    "renewal/noisy_renewal/co_canonical": {
      "agent": "co_canonical",
      "agent_kind": "co_variant",
      "family": "renewal",
      "mean_metric_value": 0.5,
      "metric_direction": "higher_is_better",
      "metric_name": "mean_reward",
      "mode": "noisy_renewal",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        0.5
      ]
    },
    "renewal/noisy_renewal/co_dynamic_alpha_high": {
      "agent": "co_dynamic_alpha_high",
      "agent_kind": "co_variant",
      "family": "renewal",
      "mean_metric_value": 0.4583333333333333,
      "metric_direction": "higher_is_better",
      "metric_name": "mean_reward",
      "mode": "noisy_renewal",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        0.4583333333333333
      ]
    },
    "renewal/noisy_renewal/co_dynamic_alpha_low": {
      "agent": "co_dynamic_alpha_low",
      "agent_kind": "co_variant",
      "family": "renewal",
      "mean_metric_value": 0.5,
      "metric_direction": "higher_is_better",
      "metric_name": "mean_reward",
      "mode": "noisy_renewal",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        0.5
      ]
    },
    "renewal/noisy_renewal/co_minimal_recent_core": {
      "agent": "co_minimal_recent_core",
      "agent_kind": "co_variant",
      "family": "renewal",
      "mean_metric_value": 0.5416666666666666,
      "metric_direction": "higher_is_better",
      "metric_name": "mean_reward",
      "mode": "noisy_renewal",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        0.5416666666666666
      ]
    },
    "renewal/noisy_renewal/co_no_quotient": {
      "agent": "co_no_quotient",
      "agent_kind": "co_variant",
      "family": "renewal",
      "mean_metric_value": 0.5,
      "metric_direction": "higher_is_better",
      "metric_name": "mean_reward",
      "mode": "noisy_renewal",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        0.5
      ]
    },
    "renewal/noisy_renewal/co_no_scheduler": {
      "agent": "co_no_scheduler",
      "agent_kind": "co_variant",
      "family": "renewal",
      "mean_metric_value": 0.5,
      "metric_direction": "higher_is_better",
      "metric_name": "mean_reward",
      "mode": "noisy_renewal",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        0.5
      ]
    },
    "renewal/noisy_renewal/co_no_sequence": {
      "agent": "co_no_sequence",
      "agent_kind": "co_variant",
      "family": "renewal",
      "mean_metric_value": 0.5,
      "metric_direction": "higher_is_better",
      "metric_name": "mean_reward",
      "mode": "noisy_renewal",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        0.5
      ]
    },
    "renewal/noisy_renewal/co_readout_resolver_conservative": {
      "agent": "co_readout_resolver_conservative",
      "agent_kind": "co_variant",
      "family": "renewal",
      "mean_metric_value": 0.5833333333333334,
      "metric_direction": "higher_is_better",
      "metric_name": "mean_reward",
      "mode": "noisy_renewal",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        0.5833333333333334
      ]
    },
    "renewal/noisy_renewal/co_readout_resolver_permissive": {
      "agent": "co_readout_resolver_permissive",
      "agent_kind": "co_variant",
      "family": "renewal",
      "mean_metric_value": 0.5416666666666666,
      "metric_direction": "higher_is_better",
      "metric_name": "mean_reward",
      "mode": "noisy_renewal",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        0.5416666666666666
      ]
    },
    "renewal/noisy_renewal/co_shape_flat_mid": {
      "agent": "co_shape_flat_mid",
      "agent_kind": "co_variant",
      "family": "renewal",
      "mean_metric_value": 0.4583333333333333,
      "metric_direction": "higher_is_better",
      "metric_name": "mean_reward",
      "mode": "noisy_renewal",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        0.4583333333333333
      ]
    },
    "renewal/noisy_renewal/co_shape_hidden_long": {
      "agent": "co_shape_hidden_long",
      "agent_kind": "co_variant",
      "family": "renewal",
      "mean_metric_value": 0.041666666666666664,
      "metric_direction": "higher_is_better",
      "metric_name": "mean_reward",
      "mode": "noisy_renewal",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        0.041666666666666664
      ]
    },
    "renewal/noisy_renewal/co_shape_local_fast": {
      "agent": "co_shape_local_fast",
      "agent_kind": "co_variant",
      "family": "renewal",
      "mean_metric_value": 0.625,
      "metric_direction": "higher_is_better",
      "metric_name": "mean_reward",
      "mode": "noisy_renewal",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        0.625
      ]
    },
    "renewal/noisy_renewal/co_shape_rigid_topology": {
      "agent": "co_shape_rigid_topology",
      "agent_kind": "co_variant",
      "family": "renewal",
      "mean_metric_value": 0.4583333333333333,
      "metric_direction": "higher_is_better",
      "metric_name": "mean_reward",
      "mode": "noisy_renewal",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        0.4583333333333333
      ]
    },
    "renewal/noisy_renewal/co_static_shape": {
      "agent": "co_static_shape",
      "agent_kind": "co_variant",
      "family": "renewal",
      "mean_metric_value": 0.625,
      "metric_direction": "higher_is_better",
      "metric_name": "mean_reward",
      "mode": "noisy_renewal",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        0.625
      ]
    },
    "renewal/noisy_renewal/last": {
      "agent": "last",
      "agent_kind": "baseline",
      "family": "renewal",
      "mean_metric_value": 0.3333333333333333,
      "metric_direction": "higher_is_better",
      "metric_name": "mean_reward",
      "mode": "noisy_renewal",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        0.3333333333333333
      ]
    },
    "renewal/noisy_renewal/ngram": {
      "agent": "ngram",
      "agent_kind": "baseline",
      "family": "renewal",
      "mean_metric_value": 0.25,
      "metric_direction": "higher_is_better",
      "metric_name": "mean_reward",
      "mode": "noisy_renewal",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        0.25
      ]
    },
    "renewal/noisy_renewal/phase": {
      "agent": "phase",
      "agent_kind": "baseline",
      "family": "renewal",
      "mean_metric_value": 0.9166666666666666,
      "metric_direction": "higher_is_better",
      "metric_name": "mean_reward",
      "mode": "noisy_renewal",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        0.9166666666666666
      ]
    },
    "renewal/noisy_renewal/vom": {
      "agent": "vom",
      "agent_kind": "baseline",
      "family": "renewal",
      "mean_metric_value": 0.25,
      "metric_direction": "higher_is_better",
      "metric_name": "mean_reward",
      "mode": "noisy_renewal",
      "runs": 1,
      "std_population": 0.0,
      "values": [
        0.25
      ]
    }
  },
  "claim_boundary": "Diagnostic factor sweep only. Counterfactual shapes/readout parameters are not canonical, not tuned outputs, and not evidence for publication claims. The goal is causal understanding: which generic factors explain current CO behavior and where performance deficits remain after plausible factor variation.",
  "comparisons": {
    "bandit/easy_public_bandit": {
      "best_baseline_agent": "ts",
      "best_baseline_mean": 1.9000000000000004,
      "best_co_variant_agent": "co_shape_flat_mid",
      "best_co_variant_mean": 5.200000000000001,
      "best_co_variant_minus_best_baseline": 3.3000000000000007,
      "best_variant_improvement_over_canonical": 4.099999999999998,
      "canonical_co_mean": 9.299999999999999,
      "canonical_minus_best_baseline": 7.399999999999999,
      "factor_group_effects": {
        "canonical": {
          "agents": [
            "co_canonical"
          ],
          "best_agent": "co_canonical",
          "max": 9.299999999999999,
          "min": 9.299999999999999,
          "range": 0.0
        },
        "dynamic_alpha": {
          "agents": [
            "co_dynamic_alpha_high",
            "co_dynamic_alpha_low"
          ],
          "best_agent": "co_dynamic_alpha_high",
          "max": 16.799999999999994,
          "min": 8.0,
          "range": 8.799999999999994
        },
        "mechanism_ablation": {
          "agents": [
            "co_minimal_recent_core",
            "co_no_quotient",
            "co_no_scheduler",
            "co_no_sequence",
            "co_static_shape"
          ],
          "best_agent": "co_no_quotient",
          "max": 16.799999999999994,
          "min": 9.299999999999999,
          "range": 7.499999999999995
        },
        "readout_gate": {
          "agents": [
            "co_readout_resolver_conservative",
            "co_readout_resolver_permissive"
          ],
          "best_agent": "co_readout_resolver_conservative",
          "max": 9.299999999999999,
          "min": 9.299999999999999,
          "range": 0.0
        },
        "shape_counterfactual": {
          "agents": [
            "co_shape_flat_mid",
            "co_shape_hidden_long",
            "co_shape_local_fast",
            "co_shape_rigid_topology"
          ],
          "best_agent": "co_shape_flat_mid",
          "max": 16.799999999999994,
          "min": 5.200000000000001,
          "range": 11.599999999999993
        }
      },
      "metric_direction": "lower_is_better",
      "metric_name": "final_cumulative_regret"
    },
    "renewal/noisy_renewal": {
      "best_baseline_agent": "phase",
      "best_baseline_mean": 0.9166666666666666,
      "best_co_variant_agent": "co_shape_local_fast",
      "best_co_variant_mean": 0.625,
      "best_co_variant_minus_best_baseline": -0.29166666666666663,
      "best_variant_improvement_over_canonical": 0.125,
      "canonical_co_mean": 0.5,
      "canonical_minus_best_baseline": -0.41666666666666663,
      "factor_group_effects": {
        "canonical": {
          "agents": [
            "co_canonical"
          ],
          "best_agent": "co_canonical",
          "max": 0.5,
          "min": 0.5,
          "range": 0.0
        },
        "dynamic_alpha": {
          "agents": [
            "co_dynamic_alpha_high",
            "co_dynamic_alpha_low"
          ],
          "best_agent": "co_dynamic_alpha_low",
          "max": 0.5,
          "min": 0.4583333333333333,
          "range": 0.041666666666666685
        },
        "mechanism_ablation": {
          "agents": [
            "co_minimal_recent_core",
            "co_no_quotient",
            "co_no_scheduler",
            "co_no_sequence",
            "co_static_shape"
          ],
          "best_agent": "co_static_shape",
          "max": 0.625,
          "min": 0.5,
          "range": 0.125
        },
        "readout_gate": {
          "agents": [
            "co_readout_resolver_conservative",
            "co_readout_resolver_permissive"
          ],
          "best_agent": "co_readout_resolver_conservative",
          "max": 0.5833333333333334,
          "min": 0.5416666666666666,
          "range": 0.04166666666666674
        },
        "shape_counterfactual": {
          "agents": [
            "co_shape_flat_mid",
            "co_shape_hidden_long",
            "co_shape_local_fast",
            "co_shape_rigid_topology"
          ],
          "best_agent": "co_shape_local_fast",
          "max": 0.625,
          "min": 0.041666666666666664,
          "range": 0.5833333333333334
        }
      },
      "metric_direction": "higher_is_better",
      "metric_name": "mean_reward"
    }
  },
  "completed_at": "2026-05-25T14:28:30.324424+00:00",
  "factor_groups": {
    "canonical": [
      "co_canonical"
    ],
    "dynamic_alpha": [
      "co_dynamic_alpha_low",
      "co_dynamic_alpha_high"
    ],
    "mechanism_ablation": [
      "co_static_shape",
      "co_no_quotient",
      "co_no_scheduler",
      "co_no_sequence",
      "co_minimal_recent_core"
    ],
    "readout_gate": [
      "co_readout_resolver_permissive",
      "co_readout_resolver_conservative"
    ],
    "shape_counterfactual": [
      "co_shape_flat_mid",
      "co_shape_local_fast",
      "co_shape_hidden_long",
      "co_shape_rigid_topology"
    ]
  },
  "non_claims": [
    "Counterfactual shape/readout variants are not canonical.",
    "Do not tune constants from this result.",
    "This sweep is small-N and bounded; it explains behavior, it does not establish final empirical evidence."
  ],
  "outputs": {
    "report_md": "research_reports/2026-05-25/PASS1_FACTOR_CAUSAL_SWEEP_REPORT_2026-05-25.md",
    "runs_jsonl": "outputs/pass1_factor_causal_sweep_v1/runs.jsonl",
    "shape_reports_json": "outputs/pass1_factor_causal_sweep_v1/shape_factor_reports.json",
    "steps_jsonl": "outputs/pass1_factor_causal_sweep_v1/steps.jsonl",
    "summary_json": "outputs/pass1_factor_causal_sweep_v1/summary.json"
  },
  "rows": 37,
  "run_settings": {
    "bandit_horizon": 24,
    "latent_max_steps": 8,
    "maintenance_native_horizons": "regime defaults",
    "maze_max_steps": 32,
    "renewal_horizon": 24
  },
  "seeds": [
    0
  ],
  "skipped_rows": 0,
  "status": "executed_family_by_family_timeout_safe",
  "step_summaries": {
    "bandit/easy_public_bandit/co_canonical": {
      "actions": {
        "0": 9,
        "1": 5,
        "2": 10
      },
      "avg_quotient_rows": 0.0,
      "avg_recursion_demand": 0.16814685268455204,
      "avg_sequence_active_rows": 0.125,
      "commitment_modes": {
        "dominance": 16,
        "reopen_or_sample": 6,
        "stable_continuation": 2
      },
      "dynamic_shape_applied_steps": 24,
      "shape_gauged_resolver_steps": 4,
      "steps": 24
    },
    "bandit/easy_public_bandit/co_dynamic_alpha_high": {
      "actions": {
        "0": 8,
        "1": 4,
        "2": 12
      },
      "avg_quotient_rows": 0.0,
      "avg_recursion_demand": 0.16742942427806423,
      "avg_sequence_active_rows": 0.041666666666666664,
      "commitment_modes": {
        "dominance": 18,
        "reopen_or_sample": 6
      },
      "dynamic_shape_applied_steps": 24,
      "shape_gauged_resolver_steps": 4,
      "steps": 24
    },
    "bandit/easy_public_bandit/co_dynamic_alpha_low": {
      "actions": {
        "0": 24
      },
      "avg_quotient_rows": 0.0,
      "avg_recursion_demand": 0.19341482695635495,
      "avg_sequence_active_rows": 0.0,
      "commitment_modes": {
        "dominance": 23,
        "reopen_or_sample": 1
      },
      "dynamic_shape_applied_steps": 24,
      "shape_gauged_resolver_steps": 0,
      "steps": 24
    },
    "bandit/easy_public_bandit/co_minimal_recent_core": {
      "actions": {
        "0": 24
      },
      "avg_quotient_rows": 0.0,
      "avg_recursion_demand": 0.0,
      "avg_sequence_active_rows": 0.0,
      "commitment_modes": {
        "dominance": 23,
        "reopen_or_sample": 1
      },
      "dynamic_shape_applied_steps": 0,
      "shape_gauged_resolver_steps": 0,
      "steps": 24
    },
    "bandit/easy_public_bandit/co_no_quotient": {
      "actions": {
        "0": 9,
        "1": 5,
        "2": 10
      },
      "avg_quotient_rows": 0.0,
      "avg_recursion_demand": 0.16814685268455204,
      "avg_sequence_active_rows": 0.125,
      "commitment_modes": {
        "dominance": 16,
        "reopen_or_sample": 6,
        "stable_continuation": 2
      },
      "dynamic_shape_applied_steps": 24,
      "shape_gauged_resolver_steps": 4,
      "steps": 24
    },
    "bandit/easy_public_bandit/co_no_scheduler": {
      "actions": {
        "0": 24
      },
      "avg_quotient_rows": 0.0,
      "avg_recursion_demand": 0.0,
      "avg_sequence_active_rows": 0.0,
      "commitment_modes": {
        "dominance": 23,
        "reopen_or_sample": 1
      },
      "dynamic_shape_applied_steps": 24,
      "shape_gauged_resolver_steps": 0,
      "steps": 24
    },
    "bandit/easy_public_bandit/co_no_sequence": {
      "actions": {
        "0": 9,
        "1": 5,
        "2": 10
      },
      "avg_quotient_rows": 0.0,
      "avg_recursion_demand": 0.16814685268455204,
      "avg_sequence_active_rows": 0.0,
      "commitment_modes": {
        "dominance": 16,
        "reopen_or_sample": 6,
        "stable_continuation": 2
      },
      "dynamic_shape_applied_steps": 24,
      "shape_gauged_resolver_steps": 4,
      "steps": 24
    },
    "bandit/easy_public_bandit/co_readout_resolver_conservative": {
      "actions": {
        "0": 9,
        "1": 5,
        "2": 10
      },
      "avg_quotient_rows": 0.0,
      "avg_recursion_demand": 0.16781150425071875,
      "avg_sequence_active_rows": 0.16666666666666666,
      "commitment_modes": {
        "dominance": 16,
        "reopen_or_sample": 6,
        "stable_continuation": 2
      },
      "dynamic_shape_applied_steps": 24,
      "shape_gauged_resolver_steps": 4,
      "steps": 24
    },
    "bandit/easy_public_bandit/co_readout_resolver_permissive": {
      "actions": {
        "0": 9,
        "1": 5,
        "2": 10
      },
      "avg_quotient_rows": 0.0,
      "avg_recursion_demand": 0.16852754155883065,
      "avg_sequence_active_rows": 0.08333333333333333,
      "commitment_modes": {
        "dominance": 16,
        "reopen_or_sample": 6,
        "stable_continuation": 2
      },
      "dynamic_shape_applied_steps": 24,
      "shape_gauged_resolver_steps": 4,
      "steps": 24
    },
    "bandit/easy_public_bandit/co_shape_flat_mid": {
      "actions": {
        "0": 4,
        "1": 4,
        "2": 16
      },
      "avg_quotient_rows": 0.0,
      "avg_recursion_demand": 0.17214773570552733,
      "avg_sequence_active_rows": 0.0,
      "commitment_modes": {
        "dominance": 15,
        "reopen_or_sample": 9
      },
      "dynamic_shape_applied_steps": 24,
      "shape_gauged_resolver_steps": 6,
      "steps": 24
    },
    "bandit/easy_public_bandit/co_shape_hidden_long": {
      "actions": {
        "0": 6,
        "1": 6,
        "2": 12
      },
      "avg_quotient_rows": 0.0,
      "avg_recursion_demand": 0.21349897196531856,
      "avg_sequence_active_rows": 0.041666666666666664,
      "commitment_modes": {
        "dominance": 10,
        "reopen_or_sample": 14
      },
      "dynamic_shape_applied_steps": 24,
      "shape_gauged_resolver_steps": 2,
      "steps": 24
    },
    "bandit/easy_public_bandit/co_shape_local_fast": {
      "actions": {
        "0": 24
      },
      "avg_quotient_rows": 0.0,
      "avg_recursion_demand": 0.19026575482159458,
      "avg_sequence_active_rows": 0.0,
      "commitment_modes": {
        "dominance": 23,
        "reopen_or_sample": 1
      },
      "dynamic_shape_applied_steps": 24,
      "shape_gauged_resolver_steps": 0,
      "steps": 24
    },
    "bandit/easy_public_bandit/co_shape_rigid_topology": {
      "actions": {
        "0": 5,
        "1": 5,
        "2": 14
      },
      "avg_quotient_rows": 0.0,
      "avg_recursion_demand": 0.1830120152288807,
      "avg_sequence_active_rows": 0.0,
      "commitment_modes": {
        "dominance": 14,
        "reopen_or_sample": 10
      },
      "dynamic_shape_applied_steps": 24,
      "shape_gauged_resolver_steps": 7,
      "steps": 24
    },
    "bandit/easy_public_bandit/co_static_shape": {
      "actions": {
        "0": 24
      },
      "avg_quotient_rows": 0.0,
      "avg_recursion_demand": 0.19101998885663032,
      "avg_sequence_active_rows": 0.0,
      "commitment_modes": {
        "dominance": 23,
        "reopen_or_sample": 1
      },
      "dynamic_shape_applied_steps": 0,
      "shape_gauged_resolver_steps": 0,
      "steps": 24
    },
    "maze/static_visible_5x5/co_canonical": {
      "actions": {
        "DOWN": 4,
        "RIGHT": 4
      },
      "avg_quotient_rows": 0.5,
      "avg_recursion_demand": 0.041907065638041384,
      "avg_sequence_active_rows": 1.125,
      "commitment_modes": {
        "dominance": 6,
        "stable_continuation": 2
      },
      "dynamic_shape_applied_steps": 8,
      "shape_gauged_resolver_steps": 0,
      "steps": 8
    },
    "renewal/noisy_renewal/co_canonical": {
      "actions": {
        "0": 3,
        "2": 1,
        "3": 20
      },
      "avg_quotient_rows": 0.0,
      "avg_recursion_demand": 0.1472357795232805,
      "avg_sequence_active_rows": 0.4583333333333333,
      "commitment_modes": {
        "dominance": 18,
        "reopen_or_sample": 4,
        "stable_continuation": 2
      },
      "dynamic_shape_applied_steps": 24,
      "shape_gauged_resolver_steps": 1,
      "steps": 24
    },
    "renewal/noisy_renewal/co_dynamic_alpha_high": {
      "actions": {
        "0": 3,
        "1": 1,
        "2": 1,
        "3": 19
      },
      "avg_quotient_rows": 0.0,
      "avg_recursion_demand": 0.14722246335990768,
      "avg_sequence_active_rows": 0.4583333333333333,
      "commitment_modes": {
        "dominance": 18,
        "reopen_or_sample": 5,
        "stable_continuation": 1
      },
      "dynamic_shape_applied_steps": 24,
      "shape_gauged_resolver_steps": 1,
      "steps": 24
    },
    "renewal/noisy_renewal/co_dynamic_alpha_low": {
      "actions": {
        "0": 3,
        "2": 1,
        "3": 20
      },
      "avg_quotient_rows": 0.0,
      "avg_recursion_demand": 0.14703026340697237,
      "avg_sequence_active_rows": 0.4583333333333333,
      "commitment_modes": {
        "dominance": 18,
        "reopen_or_sample": 4,
        "stable_continuation": 2
      },
      "dynamic_shape_applied_steps": 24,
      "shape_gauged_resolver_steps": 1,
      "steps": 24
    },
    "renewal/noisy_renewal/co_minimal_recent_core": {
      "actions": {
        "0": 3,
        "3": 21
      },
      "avg_quotient_rows": 0.0,
      "avg_recursion_demand": 0.0,
      "avg_sequence_active_rows": 0.0,
      "commitment_modes": {
        "dominance": 19,
        "reopen_or_sample": 3,
        "stable_continuation": 2
      },
      "dynamic_shape_applied_steps": 0,
      "shape_gauged_resolver_steps": 0,
      "steps": 24
    },
    "renewal/noisy_renewal/co_no_quotient": {
      "actions": {
        "0": 3,
        "2": 1,
        "3": 20
      },
      "avg_quotient_rows": 0.0,
      "avg_recursion_demand": 0.1472357795232805,
      "avg_sequence_active_rows": 0.4583333333333333,
      "commitment_modes": {
        "dominance": 18,
        "reopen_or_sample": 4,
        "stable_continuation": 2
      },
      "dynamic_shape_applied_steps": 24,
      "shape_gauged_resolver_steps": 1,
      "steps": 24
    },
    "renewal/noisy_renewal/co_no_scheduler": {
      "actions": {
        "0": 3,
        "2": 1,
        "3": 20
      },
      "avg_quotient_rows": 0.0,
      "avg_recursion_demand": 0.0,
      "avg_sequence_active_rows": 0.4583333333333333,
      "commitment_modes": {
        "dominance": 18,
        "reopen_or_sample": 4,
        "stable_continuation": 2
      },
      "dynamic_shape_applied_steps": 24,
      "shape_gauged_resolver_steps": 1,
      "steps": 24
    },
    "renewal/noisy_renewal/co_no_sequence": {
      "actions": {
        "0": 3,
        "2": 1,
        "3": 20
      },
      "avg_quotient_rows": 0.0,
      "avg_recursion_demand": 0.1472357795232805,
      "avg_sequence_active_rows": 0.0,
      "commitment_modes": {
        "dominance": 18,
        "reopen_or_sample": 4,
        "stable_continuation": 2
      },
      "dynamic_shape_applied_steps": 24,
      "shape_gauged_resolver_steps": 1,
      "steps": 24
    },
    "renewal/noisy_renewal/co_readout_resolver_conservative": {
      "actions": {
        "0": 3,
        "2": 1,
        "3": 20
      },
      "avg_quotient_rows": 0.0,
      "avg_recursion_demand": 0.1473246025977751,
      "avg_sequence_active_rows": 0.4583333333333333,
      "commitment_modes": {
        "dominance": 18,
        "reopen_or_sample": 4,
        "stable_continuation": 2
      },
      "dynamic_shape_applied_steps": 24,
      "shape_gauged_resolver_steps": 1,
      "steps": 24
    },
    "renewal/noisy_renewal/co_readout_resolver_permissive": {
      "actions": {
        "0": 3,
        "3": 21
      },
      "avg_quotient_rows": 0.0,
      "avg_recursion_demand": 0.1473246025977751,
      "avg_sequence_active_rows": 0.4583333333333333,
      "commitment_modes": {
        "dominance": 19,
        "reopen_or_sample": 3,
        "stable_continuation": 2
      },
      "dynamic_shape_applied_steps": 24,
      "shape_gauged_resolver_steps": 0,
      "steps": 24
    },
    "renewal/noisy_renewal/co_shape_flat_mid": {
      "actions": {
        "0": 3,
        "1": 2,
        "2": 2,
        "3": 17
      },
      "avg_quotient_rows": 0.0,
      "avg_recursion_demand": 0.15574250866835807,
      "avg_sequence_active_rows": 0.25,
      "commitment_modes": {
        "dominance": 12,
        "reopen_or_sample": 6,
        "stable_continuation": 6
      },
      "dynamic_shape_applied_steps": 24,
      "shape_gauged_resolver_steps": 2,
      "steps": 24
    },
    "renewal/noisy_renewal/co_shape_hidden_long": {
      "actions": {
        "0": 12,
        "1": 11,
        "2": 1
      },
      "avg_quotient_rows": 0.0,
      "avg_recursion_demand": 0.20663976574357343,
      "avg_sequence_active_rows": 0.5416666666666666,
      "commitment_modes": {
        "reopen_or_sample": 24
      },
      "dynamic_shape_applied_steps": 24,
      "shape_gauged_resolver_steps": 0,
      "steps": 24
    },
    "renewal/noisy_renewal/co_shape_local_fast": {
      "actions": {
        "0": 1,
        "3": 23
      },
      "avg_quotient_rows": 0.0,
      "avg_recursion_demand": 0.14742714663283343,
      "avg_sequence_active_rows": 0.375,
      "commitment_modes": {
        "dominance": 21,
        "reopen_or_sample": 1,
        "stable_continuation": 2
      },
      "dynamic_shape_applied_steps": 24,
      "shape_gauged_resolver_steps": 0,
      "steps": 24
    },
    "renewal/noisy_renewal/co_shape_rigid_topology": {
      "actions": {
        "0": 3,
        "1": 2,
        "2": 2,
        "3": 17
      },
      "avg_quotient_rows": 0.0,
      "avg_recursion_demand": 0.16757939572303843,
      "avg_sequence_active_rows": 0.25,
      "commitment_modes": {
        "dominance": 12,
        "reopen_or_sample": 6,
        "stable_continuation": 6
      },
      "dynamic_shape_applied_steps": 24,
      "shape_gauged_resolver_steps": 2,
      "steps": 24
    },
    "renewal/noisy_renewal/co_static_shape": {
      "actions": {
        "0": 1,
        "3": 23
      },
      "avg_quotient_rows": 0.0,
      "avg_recursion_demand": 0.14742714663283343,
      "avg_sequence_active_rows": 0.375,
      "commitment_modes": {
        "dominance": 20,
        "reopen_or_sample": 1,
        "stable_continuation": 3
      },
      "dynamic_shape_applied_steps": 0,
      "shape_gauged_resolver_steps": 0,
      "steps": 24
    }
  },
  "study": "pass1_factor_causal_sweep_v1",
  "variants": {
    "co_canonical": {},
    "co_dynamic_alpha_high": {
      "candidate_surface": {
        "dynamic_shape_alpha": 0.7
      }
    },
    "co_dynamic_alpha_low": {
      "candidate_surface": {
        "dynamic_shape_alpha": 0.12
      }
    },
    "co_minimal_recent_core": {
      "candidate_surface": {
        "dynamic_shape_enabled": false,
        "quotient_enabled": false,
        "recursion_scheduler_enabled": false,
        "sequence_composition_enabled": false
      }
    },
    "co_no_quotient": {
      "candidate_surface": {
        "quotient_enabled": false
      }
    },
    "co_no_scheduler": {
      "candidate_surface": {
        "recursion_scheduler_enabled": false
      }
    },
    "co_no_sequence": {
      "candidate_surface": {
        "sequence_composition_enabled": false
      }
    },
    "co_readout_resolver_conservative": {
      "commitment_formula_params": {
        "preblocking_carrier_pressure_base": 0.78,
        "preblocking_carrier_pressure_floor": 0.5,
        "preblocking_resolver_support_base": 0.16,
        "preblocking_resolver_support_floor": 0.14,
        "preblocking_score_margin_base": 0.075,
        "preblocking_support_margin_base": 0.145,
        "resolver_support_scaled_base": 0.11,
        "resolver_support_threshold": 0.11
      }
    },
    "co_readout_resolver_permissive": {
      "commitment_formula_params": {
        "preblocking_carrier_pressure_base": 0.62,
        "preblocking_carrier_pressure_floor": 0.34,
        "preblocking_resolver_support_base": 0.08,
        "preblocking_resolver_support_floor": 0.06,
        "preblocking_score_margin_base": 0.04,
        "preblocking_support_margin_base": 0.08,
        "resolver_support_scaled_base": 0.055,
        "resolver_support_threshold": 0.055
      }
    },
    "co_shape_flat_mid": {
      "shape_axes": {
        "consequence_span": 0.5,
        "hidden_decisiveness": 0.5,
        "local_cue_reliability": 0.5,
        "reshapeability": 0.5,
        "revision_cost": 0.5,
        "topology_constraint": 0.5
      }
    },
    "co_shape_hidden_long": {
      "shape_axes": {
        "consequence_span": 1.0,
        "hidden_decisiveness": 1.0,
        "local_cue_reliability": 0.25,
        "reshapeability": 0.75,
        "revision_cost": 1.0,
        "topology_constraint": 0.5
      }
    },
    "co_shape_local_fast": {
      "shape_axes": {
        "consequence_span": 0.0,
        "hidden_decisiveness": 0.0,
        "local_cue_reliability": 1.0,
        "reshapeability": 0.25,
        "revision_cost": 0.0,
        "topology_constraint": 0.25
      }
    },
    "co_shape_rigid_topology": {
      "shape_axes": {
        "consequence_span": 0.75,
        "hidden_decisiveness": 0.5,
        "local_cue_reliability": 0.75,
        "reshapeability": 0.0,
        "revision_cost": 0.75,
        "topology_constraint": 1.0
      }
    },
    "co_static_shape": {
      "candidate_surface": {
        "dynamic_shape_enabled": false
      }
    }
  }
}
```
