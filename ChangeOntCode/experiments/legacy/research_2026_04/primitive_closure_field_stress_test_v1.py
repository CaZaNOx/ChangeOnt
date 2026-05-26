from __future__ import annotations

from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

"""Docs-aligned primitive closure field stress test.

This is intentionally a contract/measurement-level study, not a benchmark-performance study.
It operationalizes the first three watchlist pairs from docs/kernel_spec/44_... using
synthetic-but-auditable observable-class contrasts.

Important limitations:
- It does not claim runtime doctrinal realization.
- It does not consume Tier C adapter semantics.
- It stress-tests the current documented assignment rules for separability.
"""

from dataclasses import dataclass
import json
from typing import Dict, Mapping, Any, List, Tuple

from agents.co.placement.legacy.basis_protocol import derive_direct_modulation

PRIMITIVE_FIELDS = [
    "observed_support_coverage",
    "hidden_decisive_dependence",
    "closure_rigidity",
    "correction_irreversibility",
    "local_cue_fidelity",
    "carrier_persistence",
    "payload_volatility",
    "cross_actor_reactivity",
    "consequence_propagation_span",
    "intervention_branching_freedom",
    "anchor_explicitness",
    "anchor_drift",
]


def clip01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def mean(vals: List[float], default: float = 0.5) -> float:
    return sum(vals) / len(vals) if vals else default


def band(x: float) -> str:
    x = clip01(x)
    if x < 0.2:
        return "VL"
    if x < 0.4:
        return "L"
    if x < 0.6:
        return "M"
    if x < 0.8:
        return "H"
    return "VH"


def bin05(x: float) -> int:
    x = clip01(x)
    if x < 0.15:
        return 0
    if x < 0.35:
        return 1
    if x < 0.55:
        return 2
    if x < 0.75:
        return 3
    return 4


@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    pair_id: str
    reference_family: str
    description: str
    declared: Dict[str, float]
    measured: Dict[str, float]
    expectations: Dict[str, str]


DEFAULT_DECLARED = {
    "D1_observability_scope": 0.5,
    "D2_admissibility_rigidity": 0.5,
    "D3_intervention_branching": 0.5,
    "D4_anchor_contract": 0.7,
    "D5_external_reactivity": 0.1,
    "D6_consequence_horizon": 0.5,
    "D7_carrier_rule_stability": 0.8,
}

DEFAULT_MEASURED = {
    "M1_revealed_coverage": 0.5,
    "M2_hidden_overturn_rate": 0.2,
    "M3_correction_loss": 0.5,
    "M4_cue_success_alignment": 0.5,
    "M5_carrier_break_rate": 0.1,
    "M6_payload_drift_rate": 0.2,
    "M7_realized_bypass": 0.5,
    "M8_anchor_shift_rate": 0.1,
    "M9_reactive_divergence": 0.1,
    "M10_delayed_consequence_revelation": 0.5,
}


def mk_scenario(
    scenario_id: str,
    pair_id: str,
    family: str,
    description: str,
    declared_updates: Dict[str, float],
    measured_updates: Dict[str, float],
    expectations: Dict[str, str],
) -> Scenario:
    d = dict(DEFAULT_DECLARED)
    d.update(declared_updates)
    m = dict(DEFAULT_MEASURED)
    m.update(measured_updates)
    return Scenario(scenario_id, pair_id, family, description, d, m, expectations)


SCENARIOS: List[Scenario] = [
    mk_scenario(
        "pair1_A_low_coverage_low_hidden_decisive",
        "pair1",
        "latent_mechanism",
        "Much remains unrevealed, but newly revealed structure rarely overturns the best local continuation.",
        {"D1_observability_scope": 0.2, "D6_consequence_horizon": 0.2},
        {"M1_revealed_coverage": 0.2, "M2_hidden_overturn_rate": 0.15, "M10_delayed_consequence_revelation": 0.2},
        {"observed_support_coverage": "low", "hidden_decisive_dependence": "low"},
    ),
    mk_scenario(
        "pair1_B_high_coverage_high_hidden_decisive",
        "pair1",
        "latent_mechanism",
        "Most visible structure is exposed, but a small hidden factor can still flip the correct continuation.",
        {"D1_observability_scope": 0.8, "D6_consequence_horizon": 0.8},
        {"M1_revealed_coverage": 0.8, "M2_hidden_overturn_rate": 0.85, "M10_delayed_consequence_revelation": 0.8},
        {"observed_support_coverage": "high", "hidden_decisive_dependence": "high"},
    ),
    mk_scenario(
        "pair2_A_many_alternatives_hard_correction",
        "pair2",
        "maze",
        "Many lawful alternatives remain, but late correction still leaves significant debt.",
        {"D2_admissibility_rigidity": 0.2, "D3_intervention_branching": 0.85, "D6_consequence_horizon": 0.8},
        {"M7_realized_bypass": 0.85, "M3_correction_loss": 0.8, "M10_delayed_consequence_revelation": 0.7},
        {"closure_rigidity": "low", "intervention_branching_freedom": "high"},
    ),
    mk_scenario(
        "pair2_B_few_alternatives_cheap_correction",
        "pair2",
        "maze",
        "Local continuation is funnelled through narrow choices, but wrong local choices can be corrected with limited residual debt.",
        {"D2_admissibility_rigidity": 0.85, "D3_intervention_branching": 0.2, "D6_consequence_horizon": 0.2},
        {"M7_realized_bypass": 0.15, "M3_correction_loss": 0.2, "M10_delayed_consequence_revelation": 0.2},
        {"closure_rigidity": "high", "intervention_branching_freedom": "low"},
    ),
    mk_scenario(
        "pair3_A_long_horizon_good_local_cues",
        "pair3",
        "renewal",
        "Local cues track the good continuation reliably, but decisive effects propagate across many later steps.",
        {"D4_anchor_contract": 0.85, "D6_consequence_horizon": 0.85},
        {"M4_cue_success_alignment": 0.8, "M10_delayed_consequence_revelation": 0.85},
        {"local_cue_fidelity": "high", "consequence_propagation_span": "high"},
    ),
    mk_scenario(
        "pair3_B_short_horizon_bad_local_cues",
        "pair3",
        "renewal",
        "Effects resolve quickly, but local cues are noisy or deceptive.",
        {"D4_anchor_contract": 0.75, "D6_consequence_horizon": 0.2},
        {"M4_cue_success_alignment": 0.2, "M10_delayed_consequence_revelation": 0.15},
        {"local_cue_fidelity": "low", "consequence_propagation_span": "low"},
    ),
]


def field_records_from_observables(declared: Mapping[str, float], measured: Mapping[str, float]) -> Dict[str, Dict[str, Any]]:
    d = lambda k, default=0.5: clip01(float(declared.get(k, default)))
    m = lambda k, default=0.5: clip01(float(measured.get(k, default)))

    declared_centers = {
        "observed_support_coverage": d("D1_observability_scope"),
        "hidden_decisive_dependence": mean([1.0 - d("D1_observability_scope"), d("D6_consequence_horizon")]),
        "closure_rigidity": mean([d("D2_admissibility_rigidity"), 1.0 - d("D3_intervention_branching")]),
        "correction_irreversibility": d("D6_consequence_horizon"),
        "local_cue_fidelity": mean([d("D4_anchor_contract"), 1.0 - 0.40 * d("D6_consequence_horizon")]),
        "carrier_persistence": d("D7_carrier_rule_stability"),
        "payload_volatility": mean([0.20, 0.50 * d("D5_external_reactivity")]),
        "cross_actor_reactivity": d("D5_external_reactivity"),
        "consequence_propagation_span": d("D6_consequence_horizon"),
        "intervention_branching_freedom": mean([d("D3_intervention_branching"), 1.0 - 0.30 * d("D2_admissibility_rigidity")]),
        "anchor_explicitness": d("D4_anchor_contract"),
        "anchor_drift": 1.0 - d("D4_anchor_contract"),
    }

    measured_centers = {
        "observed_support_coverage": m("M1_revealed_coverage"),
        "hidden_decisive_dependence": mean([m("M2_hidden_overturn_rate"), m("M10_delayed_consequence_revelation")]),
        "closure_rigidity": 1.0 - m("M7_realized_bypass"),
        "correction_irreversibility": mean([m("M3_correction_loss"), m("M10_delayed_consequence_revelation")]),
        "local_cue_fidelity": m("M4_cue_success_alignment"),
        "carrier_persistence": 1.0 - m("M5_carrier_break_rate"),
        "payload_volatility": mean([m("M6_payload_drift_rate"), m("M8_anchor_shift_rate"), m("M9_reactive_divergence")]),
        "cross_actor_reactivity": m("M9_reactive_divergence"),
        "consequence_propagation_span": m("M10_delayed_consequence_revelation"),
        "intervention_branching_freedom": m("M7_realized_bypass"),
        "anchor_explicitness": declared_centers["anchor_explicitness"],
        "anchor_drift": m("M8_anchor_shift_rate"),
    }

    out: Dict[str, Dict[str, Any]] = {}
    for field in PRIMITIVE_FIELDS:
        dc = clip01(declared_centers[field])
        mc = clip01(measured_centers[field])
        declared_conf = 0.8 if field != "anchor_explicitness" else 0.95
        measured_conf = 0.8 if field != "anchor_explicitness" else 0.2
        measured_maturity = 0.7 if field != "anchor_explicitness" else 0.1
        dw = declared_conf * (1.0 - measured_maturity)
        mw = measured_conf * measured_maturity
        center = clip01((dw * dc + mw * mc) / max(1e-9, dw + mw))
        disagreement = abs(dc - mc)
        confidence = clip01(max(0.15, 0.9 - 0.6 * disagreement))
        width = 0.10 + 0.20 * disagreement
        lower = clip01(center - width)
        upper = clip01(center + width)
        out[field] = {
            "declared_center": round(dc, 4),
            "measured_center": round(mc, 4),
            "center": round(center, 4),
            "lower": round(lower, 4),
            "upper": round(upper, 4),
            "confidence": round(confidence, 4),
            "band": band(center),
            "disagreement": round(disagreement, 4),
        }
    return out


def basis_from_fields(fields: Mapping[str, Mapping[str, Any]]) -> Tuple[Dict[str, float], Dict[str, int], Dict[str, float]]:
    get = lambda k: float(fields[k]["center"])
    axis_center = {
        "coverage_adequacy": get("observed_support_coverage"),
        "hidden_structure_dependence": get("hidden_decisive_dependence"),
        "revision_harshness": clip01(mean([get("closure_rigidity"), get("correction_irreversibility")])),
        "local_progress_reliability": get("local_cue_fidelity"),
        "scaffold_stability": get("carrier_persistence"),
        "payload_rewrite_intensity": get("payload_volatility"),
        "strategic_coupling": get("cross_actor_reactivity"),
        "consequence_depth": get("consequence_propagation_span"),
        "action_topology": clip01(1.0 - get("intervention_branching_freedom")),
        "anchor_stability": clip01(mean([get("anchor_explicitness"), 1.0 - get("anchor_drift") ])),
    }
    axis_bins = {k: bin05(v) for k, v in axis_center.items()}
    controls = {k: round(v, 4) for k, v in derive_direct_modulation(axis_bins).as_dict().items()}
    return ({k: round(v, 4) for k, v in axis_center.items()}, axis_bins, controls)


def evaluate_pair(pair_id: str, scenario_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_id = {r["scenario_id"]: r for r in scenario_rows}
    if pair_id == "pair1":
        a = by_id["pair1_A_low_coverage_low_hidden_decisive"]
        b = by_id["pair1_B_high_coverage_high_hidden_decisive"]
        cov_a = a["fields"]["observed_support_coverage"]["center"]
        hid_a = a["fields"]["hidden_decisive_dependence"]["center"]
        cov_b = b["fields"]["observed_support_coverage"]["center"]
        hid_b = b["fields"]["hidden_decisive_dependence"]["center"]
        success = cov_a <= 0.35 and hid_a <= 0.40 and cov_b >= 0.65 and hid_b >= 0.65
        return {
            "pair_id": pair_id,
            "status": "separated" if success else "watchlist_failure",
            "criteria": {"A_low_cov": cov_a, "A_low_hidden": hid_a, "B_high_cov": cov_b, "B_high_hidden": hid_b},
            "note": "Pair 1 survives this first pass only if low exposure can remain low-hidden and high hidden decisiveness can coexist with high exposure.",
        }
    if pair_id == "pair2":
        a = by_id["pair2_A_many_alternatives_hard_correction"]
        b = by_id["pair2_B_few_alternatives_cheap_correction"]
        rig_a = a["fields"]["closure_rigidity"]["center"]
        br_a = a["fields"]["intervention_branching_freedom"]["center"]
        rig_b = b["fields"]["closure_rigidity"]["center"]
        br_b = b["fields"]["intervention_branching_freedom"]["center"]
        topo_a = a["axes"]["action_topology"]
        topo_b = b["axes"]["action_topology"]
        success = br_a >= 0.65 and rig_a <= 0.40 and rig_b >= 0.65 and br_b <= 0.35 and topo_b > topo_a
        return {
            "pair_id": pair_id,
            "status": "separated" if success else "watchlist_failure",
            "criteria": {"A_rigidity": rig_a, "A_branching": br_a, "B_rigidity": rig_b, "B_branching": br_b, "A_action_topology": topo_a, "B_action_topology": topo_b},
            "note": "Pair 2 survives only if branching freedom and rigidity can move in opposite directions and change action topology/control downstream.",
        }
    if pair_id == "pair3":
        a = by_id["pair3_A_long_horizon_good_local_cues"]
        b = by_id["pair3_B_short_horizon_bad_local_cues"]
        cue_a = a["fields"]["local_cue_fidelity"]["center"]
        span_a = a["fields"]["consequence_propagation_span"]["center"]
        cue_b = b["fields"]["local_cue_fidelity"]["center"]
        span_b = b["fields"]["consequence_propagation_span"]["center"]
        nonlocal_a = a["controls"]["nonlocal_authority"]
        nonlocal_b = b["controls"]["nonlocal_authority"]
        success = cue_a >= 0.65 and span_a >= 0.65 and cue_b <= 0.35 and span_b <= 0.35 and nonlocal_a > nonlocal_b
        return {
            "pair_id": pair_id,
            "status": "separated" if success else "watchlist_failure",
            "criteria": {"A_cue": cue_a, "A_span": span_a, "B_cue": cue_b, "B_span": span_b, "A_nonlocal_authority": nonlocal_a, "B_nonlocal_authority": nonlocal_b},
            "note": "Pair 3 survives this first pass only if long-range consequences can remain high without forcing cue fidelity low.",
        }
    raise KeyError(pair_id)


def main(out_path: str = "outputs/primitive_closure_field_stress_test_v1.json") -> None:
    rows: List[Dict[str, Any]] = []
    for scenario in SCENARIOS:
        fields = field_records_from_observables(scenario.declared, scenario.measured)
        axes, axis_bins, controls = basis_from_fields(fields)
        rows.append({
            "scenario_id": scenario.scenario_id,
            "pair_id": scenario.pair_id,
            "reference_family": scenario.reference_family,
            "description": scenario.description,
            "declared_observables": scenario.declared,
            "measured_observables": scenario.measured,
            "expectations": scenario.expectations,
            "fields": fields,
            "axes": axes,
            "axis_bins": axis_bins,
            "controls": controls,
        })
    pair_summaries = {pid: evaluate_pair(pid, [r for r in rows if r["pair_id"] == pid]) for pid in ["pair1", "pair2", "pair3"]}
    payload = {
        "study": "primitive_closure_field_stress_test_v1",
        "status": "docs_aligned_synthetic_probe",
        "limitations": [
            "This is not runtime doctrinal realization.",
            "This uses synthetic observable-class contrasts rather than family performance outcomes.",
            "This is a first-pass separability probe for the documented assignment rules.",
        ],
        "rows": rows,
        "pair_summaries": pair_summaries,
    }
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
