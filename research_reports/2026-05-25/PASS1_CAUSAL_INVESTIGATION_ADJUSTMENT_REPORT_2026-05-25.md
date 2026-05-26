# Pass-1 Causal Investigation + Generic Adjustment — 2026-05-25

## Claim boundary

This is a causal investigation and one conservative generic adjustment. It is not a performance tuning pass, not a new CO mechanism, and not publication evidence.

## Adjustment applied

The public problem-contract vocabulary feeding shape derivation was too coarse. Legitimate public values such as `drift=none` and `commitment_cost=medium_to_high` were previously normalized to `unknown`, distorting shape before the kernel saw the problem.

Files changed:

- `ChangeOntCode/agents/co/core/contracts/_common.py`
- `ChangeOntCode/agents/co/core/contracts/problem_contract.py`
- `ChangeOntCode/agents/co/placement/shape_prior6.py`

Guardrails:

- no family names used in kernel shape code
- no action-name bonuses
- no hidden state, DP values, baseline values, or reward hindsight
- no canonical shape selected from performance results
- no readout coefficient tuning in this pass

## Affected shape reports

### latent_mechanism/easy_visible

- Legacy axes: `{'hidden_decisiveness': 0.0, 'reshapeability': 0.5, 'local_cue_reliability': 0.75, 'revision_cost': 0.5, 'consequence_span': 0.5, 'topology_constraint': 0.5}`
- New axes: `{'hidden_decisiveness': 0.0, 'reshapeability': 0.25, 'local_cue_reliability': 0.75, 'revision_cost': 0.5, 'consequence_span': 0.75, 'topology_constraint': 0.5}`
- Delta new-minus-legacy: `{'consequence_span': 0.25, 'hidden_decisiveness': 0.0, 'local_cue_reliability': 0.0, 'reshapeability': -0.25, 'revision_cost': 0.0, 'topology_constraint': 0.0}`

### latent_mechanism/hidden_depth2

- Legacy axes: `{'hidden_decisiveness': 0.0, 'reshapeability': 0.5, 'local_cue_reliability': 0.75, 'revision_cost': 0.5, 'consequence_span': 0.5, 'topology_constraint': 0.5}`
- New axes: `{'hidden_decisiveness': 0.0, 'reshapeability': 0.25, 'local_cue_reliability': 0.75, 'revision_cost': 0.5, 'consequence_span': 0.75, 'topology_constraint': 0.5}`
- Delta new-minus-legacy: `{'consequence_span': 0.25, 'hidden_decisiveness': 0.0, 'local_cue_reliability': 0.0, 'reshapeability': -0.25, 'revision_cost': 0.0, 'topology_constraint': 0.0}`

## Causal interpretation

The factor sweep still does not support one universal non-problem-specific performance fix. Shape/readout variants change behavior in some families but do not close the gap to strong baselines. Therefore this pass deliberately did not tune readout coefficients or choose counterfactual shapes based on results.

Remaining cause clusters:

- bandit: generic CO update/exploration is less efficient than posterior/UCB-style baselines
- renewal: compact phase/period structure is under-extracted compared with phase FSM
- maintenance: middle/renewal-like regimes still expose readout/gate timing and regime-placement issues over longer horizons
- latent: short capped runs remain inconclusive; shape vocabulary fix changes latent placement but does not establish performance

## Verdict

A real generic bug was fixed: public regime vocabulary should not collapse to `unknown`. But the performance deficits remain multi-causal. The next safe investigation is not benchmark tuning; it is targeted, context-conditioned analysis of (1) bandit exploration/update cadence, (2) renewal phase extraction, and (3) maintenance longer-horizon gate/readout timing.

## Full JSON

```json
{
  "adjustment_applied": {
    "details": [
      "drift uses a dedicated public drift vocabulary including 'none' instead of reusing horizon-fixity vocabulary",
      "commitment_cost accepts ordinal public categories low_to_medium and medium_to_high",
      "shape_prior6 maps drift=none to zero drift pressure and medium_to_high to elevated but non-maximal commitment pressure"
    ],
    "files": [
      "ChangeOntCode/agents/co/core/contracts/_common.py",
      "ChangeOntCode/agents/co/core/contracts/problem_contract.py",
      "ChangeOntCode/agents/co/placement/shape_prior6.py"
    ],
    "guardrails": [
      "no family names used in kernel shape code",
      "no action-name bonuses",
      "no hidden state, DP values, baseline values, or reward hindsight",
      "no canonical shape selected from performance results",
      "no readout coefficient tuning in this pass"
    ],
    "kind": "public_contract_vocabulary_normalization"
  },
  "affected_shape_report_count": 2,
  "affected_shape_reports": [
    {
      "axis_delta_new_minus_legacy": {
        "consequence_span": 0.25,
        "hidden_decisiveness": 0.0,
        "local_cue_reliability": 0.0,
        "reshapeability": -0.25,
        "revision_cost": 0.0,
        "topology_constraint": 0.0
      },
      "contract_reversibility": {
        "action_reversibility": "partly_reversible",
        "commitment_cost": "medium_to_high",
        "notes": "wrong interaction can reset or delay mechanism progress"
      },
      "contract_timescale": {
        "drift": "none",
        "horizon_fixity": "fixed",
        "notes": "semantic rewrite is endogenous, induced by interaction history"
      },
      "family": "latent_mechanism",
      "legacy_axes": {
        "consequence_span": 0.5,
        "hidden_decisiveness": 0.0,
        "local_cue_reliability": 0.75,
        "reshapeability": 0.5,
        "revision_cost": 0.5,
        "topology_constraint": 0.5
      },
      "mode": "easy_visible",
      "new_axes": {
        "consequence_span": 0.75,
        "hidden_decisiveness": 0.0,
        "local_cue_reliability": 0.75,
        "reshapeability": 0.25,
        "revision_cost": 0.5,
        "topology_constraint": 0.5
      },
      "raw_axis_delta_new_minus_legacy": {
        "consequence_span": 0.0504,
        "hidden_decisiveness": 0.0,
        "local_cue_reliability": 0.0,
        "reshapeability": -0.22500000000000003,
        "revision_cost": 0.09900000000000009,
        "topology_constraint": 0.0
      }
    },
    {
      "axis_delta_new_minus_legacy": {
        "consequence_span": 0.25,
        "hidden_decisiveness": 0.0,
        "local_cue_reliability": 0.0,
        "reshapeability": -0.25,
        "revision_cost": 0.0,
        "topology_constraint": 0.0
      },
      "contract_reversibility": {
        "action_reversibility": "partly_reversible",
        "commitment_cost": "medium_to_high",
        "notes": "wrong interaction can reset or delay mechanism progress"
      },
      "contract_timescale": {
        "drift": "none",
        "horizon_fixity": "fixed",
        "notes": "semantic rewrite is endogenous, induced by interaction history"
      },
      "family": "latent_mechanism",
      "legacy_axes": {
        "consequence_span": 0.5,
        "hidden_decisiveness": 0.0,
        "local_cue_reliability": 0.75,
        "reshapeability": 0.5,
        "revision_cost": 0.5,
        "topology_constraint": 0.5
      },
      "mode": "hidden_depth2",
      "new_axes": {
        "consequence_span": 0.75,
        "hidden_decisiveness": 0.0,
        "local_cue_reliability": 0.75,
        "reshapeability": 0.25,
        "revision_cost": 0.5,
        "topology_constraint": 0.5
      },
      "raw_axis_delta_new_minus_legacy": {
        "consequence_span": 0.0504,
        "hidden_decisiveness": 0.0,
        "local_cue_reliability": 0.0,
        "reshapeability": -0.22500000000000003,
        "revision_cost": 0.09900000000000009,
        "topology_constraint": 0.0
      }
    }
  ],
  "all_problem_comparison_available_after_adjustment": {
    "bandit/easy_public_bandit": {
      "best_baseline_agent": "ts",
      "best_baseline_mean": 5.533333333333334,
      "claim_boundary": "small-N bounded diagnostic only; do not tune constants from this comparison",
      "co_favorable_vs_best_baseline": false,
      "co_mean": 56.86666666666668,
      "co_minus_best_baseline": 51.33333333333335,
      "metric_direction": "lower_is_better",
      "metric_name": "final_cumulative_regret"
    },
    "latent_mechanism/easy_visible": {
      "best_baseline_agent": "heuristic",
      "best_baseline_mean": 0.0,
      "claim_boundary": "small-N bounded diagnostic only; do not tune constants from this comparison",
      "co_favorable_vs_best_baseline": true,
      "co_mean": 0.3333333333333333,
      "co_minus_best_baseline": 0.3333333333333333,
      "metric_direction": "higher_is_better",
      "metric_name": "success"
    },
    "latent_mechanism/hidden_depth2": {
      "best_baseline_agent": "heuristic",
      "best_baseline_mean": 0.0,
      "claim_boundary": "small-N bounded diagnostic only; do not tune constants from this comparison",
      "co_favorable_vs_best_baseline": true,
      "co_mean": 0.0,
      "co_minus_best_baseline": 0.0,
      "metric_direction": "higher_is_better",
      "metric_name": "success"
    },
    "maintenance_replacement/bandit_like": {
      "best_baseline_agent": "finite_horizon_dp",
      "best_baseline_mean": 57.5,
      "claim_boundary": "small-N bounded diagnostic only; do not tune constants from this comparison",
      "co_favorable_vs_best_baseline": false,
      "co_mean": 52.583333333333336,
      "co_minus_best_baseline": -4.916666666666664,
      "metric_direction": "higher_is_better",
      "metric_name": "total_reward"
    },
    "maintenance_replacement/middle": {
      "best_baseline_agent": "threshold",
      "best_baseline_mean": 60.30000000000001,
      "claim_boundary": "small-N bounded diagnostic only; do not tune constants from this comparison",
      "co_favorable_vs_best_baseline": false,
      "co_mean": 5.700000000000016,
      "co_minus_best_baseline": -54.599999999999994,
      "metric_direction": "higher_is_better",
      "metric_name": "total_reward"
    },
    "maintenance_replacement/renewal_like": {
      "best_baseline_agent": "q_learning",
      "best_baseline_mean": 24.016666666666666,
      "claim_boundary": "small-N bounded diagnostic only; do not tune constants from this comparison",
      "co_favorable_vs_best_baseline": false,
      "co_mean": -4.799999999999999,
      "co_minus_best_baseline": -28.816666666666663,
      "metric_direction": "higher_is_better",
      "metric_name": "total_reward"
    },
    "maze/static_visible_5x5": {
      "best_baseline_agent": "astar_full_grid",
      "best_baseline_mean": -7.0,
      "claim_boundary": "small-N bounded diagnostic only; do not tune constants from this comparison",
      "co_favorable_vs_best_baseline": false,
      "co_mean": -7.666666666666667,
      "co_minus_best_baseline": -0.666666666666667,
      "metric_direction": "higher_is_better",
      "metric_name": "episode_return"
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
  "all_problem_comparison_rows_available_after_adjustment": 114,
  "completed_at": "2026-05-25T14:31:27.362804+00:00",
  "diagnosis": {
    "main_remaining_causes": [
      "bandit: generic CO update/exploration is less efficient than posterior/UCB-style baselines",
      "renewal: compact phase/period structure is under-extracted compared with phase FSM",
      "maintenance: middle/renewal-like regimes still expose readout/gate timing and regime-placement issues over longer horizons",
      "latent: short capped runs remain inconclusive; shape vocabulary fix changes latent placement but does not establish performance"
    ],
    "new_kernel_mechanism_justified": false,
    "performance_tuning_justified": false,
    "safe_generic_fix_found": true,
    "safe_generic_fix_scope": "public contract/shape vocabulary only",
    "single_cause_found": false
  },
  "factor_sweep_comparisons_available_after_adjustment": {
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
    "latent_mechanism/easy_visible": {
      "best_baseline_agent": "heuristic",
      "best_baseline_mean": 0.0,
      "best_co_variant_agent": "co_canonical",
      "best_co_variant_mean": 0.0,
      "best_co_variant_minus_best_baseline": 0.0,
      "best_variant_improvement_over_canonical": 0.0,
      "canonical_co_mean": 0.0,
      "canonical_minus_best_baseline": 0.0,
      "factor_group_effects": {
        "canonical": {
          "agents": [
            "co_canonical"
          ],
          "best_agent": "co_canonical",
          "max": 0.0,
          "min": 0.0,
          "range": 0.0
        },
        "dynamic_alpha": {
          "agents": [
            "co_dynamic_alpha_high",
            "co_dynamic_alpha_low"
          ],
          "best_agent": "co_dynamic_alpha_high",
          "max": 0.0,
          "min": 0.0,
          "range": 0.0
        },
        "mechanism_ablation": {
          "agents": [
            "co_minimal_recent_core",
            "co_no_quotient",
            "co_no_scheduler",
            "co_no_sequence",
            "co_static_shape"
          ],
          "best_agent": "co_minimal_recent_core",
          "max": 0.0,
          "min": 0.0,
          "range": 0.0
        },
        "readout_gate": {
          "agents": [
            "co_readout_resolver_conservative",
            "co_readout_resolver_permissive"
          ],
          "best_agent": "co_readout_resolver_conservative",
          "max": 0.0,
          "min": 0.0,
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
          "max": 0.0,
          "min": 0.0,
          "range": 0.0
        }
      },
      "metric_direction": "higher_is_better",
      "metric_name": "success"
    },
    "latent_mechanism/hidden_depth2": {
      "best_baseline_agent": "heuristic",
      "best_baseline_mean": 0.0,
      "best_co_variant_agent": "co_canonical",
      "best_co_variant_mean": 0.0,
      "best_co_variant_minus_best_baseline": 0.0,
      "best_variant_improvement_over_canonical": 0.0,
      "canonical_co_mean": 0.0,
      "canonical_minus_best_baseline": 0.0,
      "factor_group_effects": {
        "canonical": {
          "agents": [
            "co_canonical"
          ],
          "best_agent": "co_canonical",
          "max": 0.0,
          "min": 0.0,
          "range": 0.0
        },
        "dynamic_alpha": {
          "agents": [
            "co_dynamic_alpha_high",
            "co_dynamic_alpha_low"
          ],
          "best_agent": "co_dynamic_alpha_high",
          "max": 0.0,
          "min": 0.0,
          "range": 0.0
        },
        "mechanism_ablation": {
          "agents": [
            "co_minimal_recent_core",
            "co_no_quotient",
            "co_no_scheduler",
            "co_no_sequence",
            "co_static_shape"
          ],
          "best_agent": "co_minimal_recent_core",
          "max": 0.0,
          "min": 0.0,
          "range": 0.0
        },
        "readout_gate": {
          "agents": [
            "co_readout_resolver_conservative",
            "co_readout_resolver_permissive"
          ],
          "best_agent": "co_readout_resolver_conservative",
          "max": 0.0,
          "min": 0.0,
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
          "max": 0.0,
          "min": 0.0,
          "range": 0.0
        }
      },
      "metric_direction": "higher_is_better",
      "metric_name": "success"
    },
    "maintenance_replacement/bandit_like": {
      "best_baseline_agent": "finite_horizon_dp",
      "best_baseline_mean": 16.0,
      "best_co_variant_agent": "co_canonical",
      "best_co_variant_mean": 16.0,
      "best_co_variant_minus_best_baseline": 0.0,
      "best_variant_improvement_over_canonical": 0.0,
      "canonical_co_mean": 16.0,
      "canonical_minus_best_baseline": 0.0,
      "factor_group_effects": {
        "canonical": {
          "agents": [
            "co_canonical"
          ],
          "best_agent": "co_canonical",
          "max": 16.0,
          "min": 16.0,
          "range": 0.0
        },
        "dynamic_alpha": {
          "agents": [
            "co_dynamic_alpha_high",
            "co_dynamic_alpha_low"
          ],
          "best_agent": "co_dynamic_alpha_high",
          "max": 16.0,
          "min": 16.0,
          "range": 0.0
        },
        "mechanism_ablation": {
          "agents": [
            "co_minimal_recent_core",
            "co_no_quotient",
            "co_no_scheduler",
            "co_no_sequence",
            "co_static_shape"
          ],
          "best_agent": "co_minimal_recent_core",
          "max": 16.0,
          "min": 16.0,
          "range": 0.0
        },
        "readout_gate": {
          "agents": [
            "co_readout_resolver_conservative",
            "co_readout_resolver_permissive"
          ],
          "best_agent": "co_readout_resolver_conservative",
          "max": 16.0,
          "min": 16.0,
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
          "max": 16.0,
          "min": 16.0,
          "range": 0.0
        }
      },
      "metric_direction": "higher_is_better",
      "metric_name": "truncated_total_reward_32"
    },
    "maintenance_replacement/middle": {
      "best_baseline_agent": "q_learning",
      "best_baseline_mean": 15.25,
      "best_co_variant_agent": "co_canonical",
      "best_co_variant_mean": 15.25,
      "best_co_variant_minus_best_baseline": 0.0,
      "best_variant_improvement_over_canonical": 0.0,
      "canonical_co_mean": 15.25,
      "canonical_minus_best_baseline": 0.0,
      "factor_group_effects": {
        "canonical": {
          "agents": [
            "co_canonical"
          ],
          "best_agent": "co_canonical",
          "max": 15.25,
          "min": 15.25,
          "range": 0.0
        },
        "dynamic_alpha": {
          "agents": [
            "co_dynamic_alpha_high",
            "co_dynamic_alpha_low"
          ],
          "best_agent": "co_dynamic_alpha_high",
          "max": 15.25,
          "min": 15.25,
          "range": 0.0
        },
        "mechanism_ablation": {
          "agents": [
            "co_minimal_recent_core",
            "co_no_quotient",
            "co_no_scheduler",
            "co_no_sequence",
            "co_static_shape"
          ],
          "best_agent": "co_minimal_recent_core",
          "max": 15.25,
          "min": 15.25,
          "range": 0.0
        },
        "readout_gate": {
          "agents": [
            "co_readout_resolver_conservative",
            "co_readout_resolver_permissive"
          ],
          "best_agent": "co_readout_resolver_conservative",
          "max": 15.25,
          "min": 15.25,
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
          "max": 15.25,
          "min": -4.8999999999999995,
          "range": 20.15
        }
      },
      "metric_direction": "higher_is_better",
      "metric_name": "truncated_total_reward_32"
    },
    "maintenance_replacement/renewal_like": {
      "best_baseline_agent": "threshold",
      "best_baseline_mean": 9.9,
      "best_co_variant_agent": "co_shape_local_fast",
      "best_co_variant_mean": 6.200000000000001,
      "best_co_variant_minus_best_baseline": -3.6999999999999993,
      "best_variant_improvement_over_canonical": 3.4000000000000017,
      "canonical_co_mean": 2.7999999999999994,
      "canonical_minus_best_baseline": -7.100000000000001,
      "factor_group_effects": {
        "canonical": {
          "agents": [
            "co_canonical"
          ],
          "best_agent": "co_canonical",
          "max": 2.7999999999999994,
          "min": 2.7999999999999994,
          "range": 0.0
        },
        "dynamic_alpha": {
          "agents": [
            "co_dynamic_alpha_high",
            "co_dynamic_alpha_low"
          ],
          "best_agent": "co_dynamic_alpha_high",
          "max": 2.7999999999999994,
          "min": 2.7999999999999994,
          "range": 0.0
        },
        "mechanism_ablation": {
          "agents": [
            "co_minimal_recent_core",
            "co_no_quotient",
            "co_no_scheduler",
            "co_no_sequence",
            "co_static_shape"
          ],
          "best_agent": "co_minimal_recent_core",
          "max": 2.7999999999999994,
          "min": 2.7999999999999994,
          "range": 0.0
        },
        "readout_gate": {
          "agents": [
            "co_readout_resolver_conservative",
            "co_readout_resolver_permissive"
          ],
          "best_agent": "co_readout_resolver_conservative",
          "max": 3.649999999999999,
          "min": 2.7999999999999994,
          "range": 0.8499999999999996
        },
        "shape_counterfactual": {
          "agents": [
            "co_shape_flat_mid",
            "co_shape_hidden_long",
            "co_shape_local_fast",
            "co_shape_rigid_topology"
          ],
          "best_agent": "co_shape_local_fast",
          "max": 6.200000000000001,
          "min": -6.3,
          "range": 12.5
        }
      },
      "metric_direction": "higher_is_better",
      "metric_name": "truncated_total_reward_32"
    },
    "maze/static_visible_5x5": {
      "best_baseline_agent": "astar_full_grid",
      "best_baseline_mean": -7.0,
      "best_co_variant_agent": "co_canonical",
      "best_co_variant_mean": -7.0,
      "best_co_variant_minus_best_baseline": 0.0,
      "best_variant_improvement_over_canonical": 0.0,
      "canonical_co_mean": -7.0,
      "canonical_minus_best_baseline": 0.0,
      "factor_group_effects": {
        "canonical": {
          "agents": [
            "co_canonical"
          ],
          "best_agent": "co_canonical",
          "max": -7.0,
          "min": -7.0,
          "range": 0.0
        },
        "dynamic_alpha": {
          "agents": [
            "co_dynamic_alpha_high",
            "co_dynamic_alpha_low"
          ],
          "best_agent": "co_dynamic_alpha_high",
          "max": -7.0,
          "min": -7.0,
          "range": 0.0
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
          "max": -7.0,
          "min": -9.0,
          "range": 2.0
        },
        "readout_gate": {
          "agents": [
            "co_readout_resolver_conservative",
            "co_readout_resolver_permissive"
          ],
          "best_agent": "co_readout_resolver_conservative",
          "max": -7.0,
          "min": -7.0,
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
          "max": -7.0,
          "min": -7.0,
          "range": 0.0
        }
      },
      "metric_direction": "higher_is_better",
      "metric_name": "episode_return"
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
  "factor_sweep_rows_available_after_adjustment": 142,
  "study": "pass1_causal_investigation_adjustment_v1"
}
```
