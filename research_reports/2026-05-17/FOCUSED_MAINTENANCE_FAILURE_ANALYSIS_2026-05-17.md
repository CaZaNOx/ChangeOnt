# Focused Maintenance Failure Analysis — 2026-05-17

## Scope

This report analyzes the already-frozen `focused_frozen_empirical_mini_benchmark_v1` outputs. It does not retune constants, rerun policy search, or change the kernel. Its purpose is diagnostic: explain why CO underperformed in the `middle` maintenance regime and why the `renewal_like` result looked favorable against the simple public thresholds.

## Main finding

The `middle` loss is not primarily an inspection problem. CO never inspects in `middle`; the public threshold baseline also never inspects. The difference is repair timing:

```json
{
  "co_action_counts": {
    "REPAIR": 16,
    "RUN": 224
  },
  "co_failure_counts_by_seed": [
    1,
    0,
    0
  ],
  "middle_co_mean": 44.9,
  "middle_threshold_mean": 60.3,
  "threshold_action_counts": {
    "REPAIR": 22,
    "RUN": 218
  },
  "threshold_failure_counts_by_seed": [
    0,
    0,
    0
  ]
}
```

The threshold baseline repairs whenever public observed health is `2` or lower. CO repairs mostly at observed health `0` or `1`, and continues `RUN` at observed health `2`:

```json
{
  "co_actions_by_observed_health": {
    "0": {
      "REPAIR": 3
    },
    "1": {
      "REPAIR": 13
    },
    "2": {
      "RUN": 97
    },
    "3": {
      "RUN": 82
    },
    "4": {
      "RUN": 45
    }
  },
  "co_modes_by_observed_health": {
    "0": {
      "dominance": 3
    },
    "1": {
      "dominance": 13
    },
    "2": {
      "dominance": 38,
      "stable_continuation": 59
    },
    "3": {
      "dominance": 81,
      "stable_continuation": 1
    },
    "4": {
      "dominance": 45
    }
  },
  "threshold_actions_by_observed_health": {
    "2": {
      "REPAIR": 22
    },
    "3": {
      "RUN": 85
    },
    "4": {
      "RUN": 133
    }
  }
}
```

## Structural diagnosis of observed-health = 2

At observed health `2`, CO selects `RUN` in all sampled rows. Internally, `REPAIR` is recognized as a strong resolver (`resolver_support ≈ 0.50`), but `RUN` still wins because its local support/field score and dominance/continuation scores remain higher. `RUN` carries substantial branch-internal pressure, but that pressure is not currently enough to block dominance or force a resolver preference.

```json
{
  "commitment_mode_counts": {
    "dominance": 38,
    "stable_continuation": 59
  },
  "metrics_by_action": {
    "INSPECT": {
      "max_burden": 0.060599736865816024,
      "max_carrier_only_pressure": 0.0,
      "max_certificate_blocks_dominance": 0.0,
      "max_certificate_gate_open": 1.0,
      "max_collapse_certificate_blocker_pressure": 0.011482455164906584,
      "max_collapse_certificate_recursion_demand": 0.03918777629126939,
      "max_collapse_certificate_score": 0.46629293139715094,
      "max_continuation_score": 0.47993844275190145,
      "max_dominance_score": 0.6427156702215855,
      "max_field_score": 0.8312213588965949,
      "max_resolver_support": 0.218,
      "max_sampling_score": 0.0990045818946666,
      "max_support": 0.4297185129395617,
      "mean_burden": 0.060432920733153116,
      "mean_carrier_only_pressure": 0.0,
      "mean_certificate_blocks_dominance": 0.0,
      "mean_certificate_gate_open": 1.0,
      "mean_collapse_certificate_blocker_pressure": 0.011460062932812917,
      "mean_collapse_certificate_recursion_demand": 0.03908591199502401,
      "mean_collapse_certificate_score": 0.4662432997263311,
      "mean_continuation_score": 0.4717945493291869,
      "mean_dominance_score": 0.6312353172106802,
      "mean_field_score": 0.7816259939241216,
      "mean_resolver_support": 0.218,
      "mean_sampling_score": 0.09805867599865503,
      "mean_support": 0.42178037761403014,
      "min_burden": 0.06012265900251287,
      "min_carrier_only_pressure": 0.0,
      "min_certificate_blocks_dominance": 0.0,
      "min_certificate_gate_open": 1.0,
      "min_collapse_certificate_blocker_pressure": 0.011413077708653668,
      "min_collapse_certificate_recursion_demand": 0.0388531830774102,
      "min_collapse_certificate_score": 0.4662270840290239,
      "min_continuation_score": 0.46832295101544275,
      "min_dominance_score": 0.62737855494862,
      "min_field_score": 0.7526468840846104,
      "min_resolver_support": 0.218,
      "min_sampling_score": 0.09632944532202076,
      "min_support": 0.41759017329527426
    },
    "REPAIR": {
      "max_burden": 0.08028371201551392,
      "max_carrier_only_pressure": 0.0,
      "max_certificate_blocks_dominance": 0.0,
      "max_certificate_gate_open": 1.0,
      "max_collapse_certificate_blocker_pressure": 0.010276824791541201,
      "max_collapse_certificate_recursion_demand": 0.04313823674448435,
      "max_collapse_certificate_score": 0.5242012650511209,
      "max_continuation_score": 0.49739632644849885,
      "max_dominance_score": 0.6822212332930131,
      "max_field_score": 0.8278730096900992,
      "max_resolver_support": 0.5,
      "max_sampling_score": 0.0971229900365468,
      "max_support": 0.4734282072438126,
      "mean_burden": 0.06917678035930547,
      "mean_carrier_only_pressure": 0.0,
      "mean_certificate_blocks_dominance": 0.0,
      "mean_certificate_gate_open": 1.0,
      "mean_collapse_certificate_blocker_pressure": 0.006517380070482117,
      "mean_collapse_certificate_recursion_demand": 0.039142520641585764,
      "mean_collapse_certificate_score": 0.5192512630859056,
      "mean_continuation_score": 0.4737950334838676,
      "mean_dominance_score": 0.6483388857769601,
      "mean_field_score": 0.7301102398503064,
      "mean_resolver_support": 0.5,
      "mean_sampling_score": 0.09104817801046006,
      "mean_support": 0.44609848951708847,
      "min_burden": 0.06603922423161268,
      "min_carrier_only_pressure": 0.0,
      "min_certificate_blocks_dominance": 0.0,
      "min_certificate_gate_open": 1.0,
      "min_collapse_certificate_blocker_pressure": 0.005693365854676705,
      "min_collapse_certificate_recursion_demand": 0.03758516739657837,
      "min_collapse_certificate_score": 0.5137507171484301,
      "min_continuation_score": 0.4509838146506922,
      "min_dominance_score": 0.6186429387754353,
      "min_field_score": 0.6691166094508102,
      "min_resolver_support": 0.5,
      "min_sampling_score": 0.0784502496006226,
      "min_support": 0.429714048922086
    },
    "REPLACE": {
      "max_burden": 0.10356579861222175,
      "max_carrier_only_pressure": 0.0,
      "max_certificate_blocks_dominance": 0.0,
      "max_certificate_gate_open": 1.0,
      "max_collapse_certificate_blocker_pressure": 0.013570285555480153,
      "max_collapse_certificate_recursion_demand": 0.04906735309691767,
      "max_collapse_certificate_score": 0.5326953937578347,
      "max_continuation_score": 0.32000979822828124,
      "max_dominance_score": 0.43890568195629975,
      "max_field_score": 0.0,
      "max_resolver_support": 0.40399999999999997,
      "max_sampling_score": 0.10604840441839551,
      "max_support": 0.27882610379997386,
      "mean_burden": 0.09458823620480963,
      "mean_carrier_only_pressure": 0.0,
      "mean_certificate_blocks_dominance": 0.0,
      "mean_certificate_gate_open": 1.0,
      "mean_collapse_certificate_blocker_pressure": 0.009630120798920986,
      "mean_collapse_certificate_recursion_demand": 0.04555918205458638,
      "mean_collapse_certificate_score": 0.5313506529561914,
      "mean_continuation_score": 0.3152550354970868,
      "mean_dominance_score": 0.4314346997930343,
      "mean_field_score": 0.0,
      "mean_resolver_support": 0.40399999999999997,
      "mean_sampling_score": 0.10371809678049991,
      "mean_support": 0.27708760911449526,
      "min_burden": 0.09248293102809187,
      "min_carrier_only_pressure": 0.0,
      "min_certificate_blocks_dominance": 0.0,
      "min_certificate_gate_open": 1.0,
      "min_collapse_certificate_blocker_pressure": 0.008829726215537048,
      "min_collapse_certificate_recursion_demand": 0.04447081253010936,
      "min_collapse_certificate_score": 0.5254661764482325,
      "min_continuation_score": 0.3043950099827879,
      "min_dominance_score": 0.4200581487355518,
      "min_field_score": 0.0,
      "min_resolver_support": 0.40399999999999997,
      "min_sampling_score": 0.1020233466103238,
      "min_support": 0.27313152343835617
    },
    "RUN": {
      "max_burden": 0.11974519302592328,
      "max_carrier_only_pressure": 0.5823333333333334,
      "max_certificate_blocks_dominance": 0.0,
      "max_certificate_gate_open": 1.0,
      "max_collapse_certificate_blocker_pressure": 0.07797499529285586,
      "max_collapse_certificate_recursion_demand": 0.1382847460651485,
      "max_collapse_certificate_score": 0.4773981937820242,
      "max_continuation_score": 0.5262727029804628,
      "max_dominance_score": 0.7550284914682887,
      "max_field_score": 1.0,
      "max_resolver_support": 0.0,
      "max_sampling_score": 0.06785435005400403,
      "max_support": 0.5651105583041489,
      "mean_burden": 0.11274076271370125,
      "mean_carrier_only_pressure": 0.5823333333333334,
      "mean_certificate_blocks_dominance": 0.0,
      "mean_certificate_gate_open": 1.0,
      "mean_collapse_certificate_blocker_pressure": 0.07538778829714235,
      "mean_collapse_certificate_recursion_demand": 0.13771837231416914,
      "mean_collapse_certificate_score": 0.4756066157474857,
      "mean_continuation_score": 0.52125339099363,
      "mean_dominance_score": 0.7432168649317702,
      "mean_field_score": 1.0,
      "mean_resolver_support": 0.0,
      "mean_sampling_score": 0.05648280024361333,
      "mean_support": 0.55948260371912,
      "min_burden": 0.10820610609040564,
      "min_carrier_only_pressure": 0.5823333333333334,
      "min_certificate_blocks_dominance": 0.0,
      "min_certificate_gate_open": 1.0,
      "min_collapse_certificate_blocker_pressure": 0.07465442915295191,
      "min_collapse_certificate_recursion_demand": 0.13738585340622933,
      "min_collapse_certificate_score": 0.47107731934898456,
      "min_continuation_score": 0.5139765962317088,
      "min_dominance_score": 0.728548860123922,
      "min_field_score": 1.0,
      "min_resolver_support": 0.0,
      "min_sampling_score": 0.05309260166465543,
      "min_support": 0.5456423964399366
    },
    "WAIT": {
      "max_burden": 0.06948316469511655,
      "max_carrier_only_pressure": 0.0,
      "max_certificate_blocks_dominance": 0.0,
      "max_certificate_gate_open": 1.0,
      "max_collapse_certificate_blocker_pressure": 0.009993620989119082,
      "max_collapse_certificate_recursion_demand": 0.03894849131540589,
      "max_collapse_certificate_score": 0.48166920066447094,
      "max_continuation_score": 0.38772336178288985,
      "max_dominance_score": 0.5156031057024961,
      "max_field_score": 0.3664541792772666,
      "max_resolver_support": 0.05,
      "max_sampling_score": 0.1030804039588045,
      "max_support": 0.32521389726525746,
      "mean_burden": 0.0692856417666506,
      "mean_carrier_only_pressure": 0.0,
      "mean_certificate_blocks_dominance": 0.0,
      "mean_certificate_gate_open": 1.0,
      "mean_collapse_certificate_blocker_pressure": 0.009986550734489742,
      "mean_collapse_certificate_recursion_demand": 0.03884081570423758,
      "mean_collapse_certificate_score": 0.4816355259453488,
      "mean_continuation_score": 0.383195729918274,
      "mean_dominance_score": 0.5076812213220937,
      "mean_field_score": 0.34709522445331326,
      "mean_resolver_support": 0.05,
      "mean_sampling_score": 0.10226627945965484,
      "mean_support": 0.32168022010677716,
      "min_burden": 0.06891622806602127,
      "min_carrier_only_pressure": 0.0,
      "min_certificate_blocks_dominance": 0.0,
      "min_certificate_gate_open": 1.0,
      "min_collapse_certificate_blocker_pressure": 0.009966346630313113,
      "min_collapse_certificate_recursion_demand": 0.03863060096094622,
      "min_collapse_certificate_score": 0.48162280185095585,
      "min_continuation_score": 0.3814954132694288,
      "min_dominance_score": 0.5049716402509287,
      "min_field_score": 0.33821257592860526,
      "min_resolver_support": 0.05,
      "min_sampling_score": 0.10034711950309706,
      "min_support": 0.3201756136930711
    }
  },
  "n_middle_co_observed_health_2_rows": 97,
  "selected_action_counts": {
    "RUN": 97
  }
}
```

In short:

```text
CO sees REPAIR as a resolver, but not as urgent enough at public health 2.
RUN is treated as a still-viable high-support continuation despite carrier-only pressure.
```

That is a formula/readout issue, not evidence that RelationSurface or resolver recognition is absent.

## Why renewal_like looked favorable

The `renewal_like` result is favorable only against simple public threshold baselines. CO avoids failures by repeatedly inspecting under hidden observation; the threshold baselines inspect only initially and then run into failure resets.

```json
{
  "renewal_like_co": {
    "action_counts": {
      "INSPECT": 284,
      "RUN": 16
    },
    "actions_by_observed_health": {
      "2": {
        "INSPECT": 274
      },
      "3": {
        "INSPECT": 4,
        "RUN": 4
      },
      "4": {
        "INSPECT": 3,
        "RUN": 12
      },
      "unknown": {
        "INSPECT": 3
      }
    },
    "agent": "co",
    "co_modes_by_observed_health": {
      "2": {
        "stable_continuation": 274
      },
      "3": {
        "stable_continuation": 8
      },
      "4": {
        "stable_continuation": 15
      },
      "unknown": {
        "reopen_or_sample": 3
      }
    },
    "event_counts": {
      "inspect": 284,
      "run": 10,
      "run_degraded": 6
    },
    "failure_counts_by_seed": [
      0,
      0,
      0
    ],
    "mean_reward_by_observed_health_action": {
      "2::INSPECT": -0.1,
      "3::INSPECT": -0.1,
      "3::RUN": 0.75,
      "4::INSPECT": -0.1,
      "4::RUN": 0.9166666666666666,
      "unknown::INSPECT": -0.1
    },
    "mean_total_reward": -4.800000000000001,
    "mode": "renewal_like",
    "runs": 3,
    "std_total_reward_population": 1.849774761063267,
    "values": [
      -2.2000000000000006,
      -6.3500000000000005,
      -5.8500000000000005
    ]
  },
  "renewal_like_threshold": {
    "action_counts": {
      "INSPECT": 3,
      "RUN": 297
    },
    "actions_by_observed_health": {
      "4": {
        "RUN": 297
      },
      "unknown": {
        "INSPECT": 3
      }
    },
    "agent": "threshold",
    "co_modes_by_observed_health": {},
    "event_counts": {
      "failure_reset": 24,
      "inspect": 3,
      "run": 196,
      "run_degraded": 77
    },
    "failure_counts_by_seed": [
      7,
      9,
      8
    ],
    "mean_reward_by_observed_health_action": {
      "4::RUN": -0.3560606060606061,
      "unknown::INSPECT": -0.1
    },
    "mean_total_reward": -35.35,
    "mode": "renewal_like",
    "runs": 3,
    "std_total_reward_population": 10.142731387550397,
    "values": [
      -22.35,
      -47.1,
      -36.6
    ]
  }
}
```

This is a positive structural signal for hiddenness/exposure sensitivity, but it is not a strong benchmark result. It may also indicate over-conservatism: CO earns safety mostly through very frequent inspection, not through a sophisticated repair/replacement cycle.

## Divergence samples

The first sample divergences against the public threshold baseline are stored in:

- `ChangeOntCode/outputs/focused_maintenance_failure_analysis_v1/details.jsonl`

## Current issue

The specific unresolved issue is:

```text
The current CommitmentSurface does not treat moderate carrier-only pressure at public health 2 as sufficient reason to prefer a strong resolver branch when RUN still has high support.
```

Possible explanations:

1. `carrier_only_pressure` is underweighted in dominance/collapse gating.
2. `collapse_blocked` thresholds are too high for mid-regime public health risk.
3. `resolver adequacy` is currently used mainly when a branch is already blocked, so it does not help enough when `RUN` is merely risky-but-not-blocked.
4. The six-question/direct-control projection for `middle` may be too collapse/local-support permissive.
5. The maintenance adapter may publish adequate resolver facts, but insufficient consequence-span / risk-of-delay facts.

## What not to conclude

Do not conclude that CO fails globally. Do not conclude that CO works. Do not tune thresholds directly to make `middle` match the public threshold baseline.

## Recommended next probe

Create a targeted mid-regime repair-timing microcase and real-trace counterfactual probe:

```text
public observed health = 2
RUN has high immediate support but carries degradation/failure pressure
REPAIR has lower immediate support but strong resolver support
vary failure penalty, degradation probability, observation noise, and horizon/consequence span
```

Expected purpose:

```text
Determine when CO should allow RUN-through-burden and when it should prefer REPAIR as an adequate resolver.
```

This is the right next probe because it targets the actual failure mechanism without performance tuning or family-specific policy insertion.

## Post-analysis status update — shape-gauged resolver timing

This failure analysis diagnosed the prior baseline before the 2026-05-17 shape-gauged pre-blocking resolver-timing update.  The diagnosis remains useful as the cause of the update, but its episode counts/actions should not be treated as current-runtime behavior until the focused benchmark is rerun under the new baseline.
