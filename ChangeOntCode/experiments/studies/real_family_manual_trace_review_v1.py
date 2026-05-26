from __future__ import annotations

"""Manual real-family structural trace review v1.

This is not a reward benchmark. It selects representative public-observation
cases from each active family and records the theory-to-runtime chain:

native/public observation -> candidate/public effects -> RelationSurface/RCF
telemetry -> CollapseCertificate/readout assessment -> commitment.

The review is meant to answer whether each family is structurally alive, thin at
the adapter boundary, and free from obvious hidden-solver/fallback behavior.
"""

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Tuple

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agents.co.adapters.bandit_adapter import COAdapterBandit
from agents.co.adapters.latent_mechanism_adapter import COAdapterLatentMechanism
from agents.co.adapters.maintenance_replacement_adapter import COAdapterMaintenanceReplacement
from agents.co.adapters.maze_adapter import COAdapterMaze
from agents.co.adapters.renewal_adapter import COAdapterRenewal
from agents.co.tests.relation_path_trace_diagnostics import DummyCore, _run_candidate_commitment

OUT = ROOT / "outputs" / "real_family_manual_trace_review_v1.json"

FORBIDDEN_TERMS = ("optimal", "best_action", "oracle", "hidden_policy", "dp_value", "q_value", "shortest_path")
RESOLVER_OPS = {"reduce", "relieve", "prevent", "reveal", "expose", "reset", "cancel", "buffer", "absorb"}
CARRIER_OPS = {"carry", "increase", "amplify", "mask", "postpone", "hide", "consume", "require"}
WEAK_OPS = {"decision_slot", "single_decision_slot"}


class _Stats:
    def __init__(self, means: List[float], counts: List[int]) -> None:
        self.means = list(means)
        self.counts = list(counts)
    def ensure(self, n: int) -> None:
        if len(self.means) < n:
            self.means += [0.0] * (n - len(self.means))
        if len(self.counts) < n:
            self.counts += [0] * (n - len(self.counts))


def _op(effect: Mapping[str, Any]) -> str:
    return str(effect.get("operation", effect.get("op", ""))).strip().lower()


def _candidate_key(c: Mapping[str, Any]) -> str:
    return str(c.get("candidate_id", c.get("action", "candidate")))


def _derive_bandit_cases() -> List[Tuple[str, str, Dict[str, Any], List[Dict[str, Any]]]]:
    cases = []
    specs = [
        ("bandit_initial_no_history", [0.0, 0.0, 0.0], [0, 0, 0], [], []),
        ("bandit_sparse_asymmetric_history", [0.40, 0.70, 0.0], [10, 2, 0], [0, 0, 1, 0, 1, 0], [{"action": 0, "reward": 0.0}, {"action": 1, "reward": 1.0}]),
        ("bandit_covered_close_means", [0.60, 0.55, 0.50], [12, 12, 12], [0, 1, 2, 0, 1, 2], [{"action": 0, "reward": 1.0}, {"action": 1, "reward": 1.0}, {"action": 2, "reward": 0.0}]),
    ]
    for name, means, counts, trace, hist in specs:
        core = DummyCore()
        core.primitives["bandit_stats"] = _Stats(means, counts)
        adapter = COAdapterBandit(core, n_arms=len(means))
        adapter._trace = list(trace)
        adapter._history = list(hist)
        obs = {"family": "bandit", "t": len(trace), "n_arms": len(means)}
        derived = adapter._derive_from_visible_history(obs, step_idx=len(trace))
        cases.append(("bandit", name, obs, list(derived.get("candidates", []))))
    return cases


def _derive_renewal_cases() -> List[Tuple[str, str, Dict[str, Any], List[Dict[str, Any]]]]:
    cases = []
    specs = [
        ("renewal_initial_no_history", {"A": 4, "obs": 0}, [], [], []),
        ("renewal_repeating_context", {"A": 4, "obs": 1}, [0, 1, 0, 1, 0, 1, 0, 1], [1, 1, 1, 1], [1.0, 1.0, 0.0, 1.0]),
        ("renewal_diffuse_miss_history", {"A": 4, "obs": 2}, [0, 2, 1, 3, 0, 2, 1, 3], [0, 1, 2, 3], [0.0, 0.0, 1.0, 0.0]),
    ]
    for name, obs, history, actions, rewards in specs:
        core = DummyCore()
        adapter = COAdapterRenewal(core)
        adapter._history = list(history)
        adapter._action_history = list(actions)
        adapter._reward_history = list(rewards)
        derived = adapter._derive_from_visible_history(dict(obs))
        cases.append(("renewal", name, dict(obs), list(derived.get("candidates", []))))
    return cases


def _derive_maze_cases() -> List[Tuple[str, str, Dict[str, Any], List[Dict[str, Any]]]]:
    cases = []
    specs = [
        ("maze_visible_open_corridor", {"pos": (1, 1), "goal": (1, 3), "grid": [[0,0,0,0],[0,0,0,0],[0,0,0,0]], "height": 3, "width": 4}),
        ("maze_visible_wall_constraint", {"pos": (1, 1), "goal": (0, 2), "grid": [[0,0,0],[0,0,1],[0,0,0]], "height": 3, "width": 3}),
        ("maze_partial_unknown_topology", {"pos": (1, 1), "goal": (1, 3), "grid": [[0,-1,0,0],[0,0,-1,0],[0,0,0,0]], "height": 3, "width": 4, "partial_observability": True}),
    ]
    for name, obs in specs:
        derived = COAdapterMaze(DummyCore())._derive(dict(obs))
        cases.append(("maze", name, dict(obs), list(derived.get("candidates", []))))
    return cases


def _derive_maintenance_cases() -> List[Tuple[str, str, Dict[str, Any], List[Dict[str, Any]]]]:
    cases = []
    specs = [
        ("maintenance_partial_midhealth", {"observed_health": 2, "max_health": 4, "health_observed": True, "degradation_prob_public": 0.20, "wait_recovery_prob_public": 0.0, "repair_cost_public": 0.80, "replace_cost_public": 2.0, "failure_penalty_public": 8.0, "observe_health_mode": "partial", "observation_noise_public": 0.20}),
        ("maintenance_hidden_high_degradation", {"observed_health": None, "max_health": 4, "health_observed": False, "degradation_prob_public": 0.70, "wait_recovery_prob_public": 0.0, "repair_cost_public": 0.80, "replace_cost_public": 2.0, "failure_penalty_public": 8.0, "observe_health_mode": "hidden", "observation_noise_public": 0.70}),
        ("maintenance_direct_low_health", {"observed_health": 0, "max_health": 4, "health_observed": True, "degradation_prob_public": 0.45, "wait_recovery_prob_public": 0.0, "repair_cost_public": 0.80, "replace_cost_public": 2.0, "failure_penalty_public": 8.0, "observe_health_mode": "direct", "observation_noise_public": 0.10}),
    ]
    for name, obs in specs:
        derived = COAdapterMaintenanceReplacement(DummyCore())._derive(dict(obs))
        cases.append(("maintenance", name, dict(obs), list(derived.get("candidates", []))))
    return cases


def _derive_latent_cases() -> List[Tuple[str, str, Dict[str, Any], List[Dict[str, Any]]]]:
    cases = []
    specs = [
        ("latent_visible_switch_nearby", {"pos": (0,0), "goal": (2,2), "door": (1,1), "switches": [(0,1)], "decoys": [(1,0)], "legal_actions": ["UP","DOWN","LEFT","RIGHT","INTERACT"], "door_open": False, "hiddenness": 0.20, "rewrite_harshness": 0.40, "local_deceptiveness": 0.00}),
        ("latent_hidden_deceptive_start", {"pos": (0,0), "goal": (2,2), "door": (1,1), "switches": [(0,1)], "decoys": [(1,0)], "legal_actions": ["UP","DOWN","LEFT","RIGHT","INTERACT"], "door_open": False, "hiddenness": 0.80, "rewrite_harshness": 0.40, "local_deceptiveness": 0.70}),
        ("latent_at_switch", {"pos": (0,1), "goal": (2,2), "door": (1,1), "switches": [(0,1)], "decoys": [(1,0)], "legal_actions": ["UP","DOWN","LEFT","RIGHT","INTERACT"], "door_open": False, "hiddenness": 0.60, "rewrite_harshness": 0.40, "local_deceptiveness": 0.30}),
    ]
    for name, obs in specs:
        derived = COAdapterLatentMechanism(DummyCore())._derive(dict(obs))
        cases.append(("latent_mechanism", name, dict(obs), list(derived.get("candidates", []))))
    return cases


def _summarize_candidates(candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = []
    for c in candidates:
        effects = [e for e in c.get("public_effects", []) if isinstance(e, Mapping)]
        ops = [_op(e) for e in effects]
        row = {
            "candidate": _candidate_key(c),
            "legal": bool(c.get("legal", True)),
            "ops": sorted(set(ops)),
            "resolver_ops": sorted(set(op for op in ops if op in RESOLVER_OPS)),
            "carrier_ops": sorted(set(op for op in ops if op in CARRIER_OPS)),
            "weak_slot_only": bool(ops and all(op in WEAK_OPS for op in ops)),
            "public_effect_count": len(effects),
            "leakage_terms_found": [term for term in FORBIDDEN_TERMS if term in json.dumps(c, sort_keys=True).lower()],
        }
        for k in ("goal_relation", "support_depth", "uncertainty_hint", "obstruction_hint", "contradiction_hint", "continuity_support"):
            if k in c:
                try:
                    row[k] = round(float(c.get(k)), 6)
                except Exception:
                    pass
        rows.append(row)
    return rows


def _round_assessment(assessment: Mapping[str, Any]) -> Dict[str, float]:
    keys = (
        "support", "burden", "stability", "dominance_score", "sampling_score", "continuation_score",
        "collapse_blocked", "certificate_gate_open", "certificate_blocks_dominance",
        "collapse_certificate_blocker_pressure", "collapse_certificate_recursion_demand",
        "resolver_support", "carrier_only_pressure",
    )
    out: Dict[str, float] = {}
    for key in keys:
        try:
            out[key] = round(float(assessment.get(key, 0.0) or 0.0), 6)
        except Exception:
            out[key] = 0.0
    return out


def _review_case(family: str, name: str, obs: Dict[str, Any], candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    rows, commit = _run_candidate_commitment(list(candidates), f"manual_trace:{family}:{name}")
    telemetry = dict(rows[0].get("relation_surface_telemetry", {}) or {}) if rows else {}
    assessments = {str(k): dict(v) for k, v in dict(commit.get("canonical_commitment_assessment", {}) or {}).items()}
    selected = str(commit.get("action"))
    selected_assessment = assessments.get(selected, {})
    selected_candidate = next((c for c in candidates if _candidate_key(c) == selected), {})
    selected_ops = [_op(e) for e in selected_candidate.get("public_effects", []) if isinstance(e, Mapping)] if selected_candidate else []
    forbidden = []
    for c in candidates:
        dump = json.dumps(c, sort_keys=True).lower()
        forbidden += [term for term in FORBIDDEN_TERMS if term in dump]
    structural_relations = 0
    relations_by_type = dict(telemetry.get("relations_by_type", {}) or {})
    for k, v in relations_by_type.items():
        if k not in {"decision_slot_competition", "rivalry"}:
            try:
                structural_relations += int(v)
            except Exception:
                pass
    notes: List[str] = []
    watchpoints: List[str] = []
    if forbidden:
        watchpoints.append("forbidden_leakage_term_in_candidate_payload")
    if int(telemetry.get("rows_with_public_effects", 0) or 0) <= 0:
        watchpoints.append("no_public_effect_rows")
    if family in {"maintenance", "latent_mechanism", "maze"} and structural_relations <= 0:
        notes.append("no_structural_cross_branch_relations_in_this_case")
    if bool(commit.get("certificate_aware_reopen_or_sample_applied", False)):
        notes.append("resolver_aware_reopen_or_sample_applied")
    if bool(commit.get("certificate_aware_stable_continuation_applied", False)):
        notes.append("certificate_aware_stable_continuation_applied")
    return {
        "family": family,
        "name": name,
        "public_observation_excerpt": {k: obs[k] for k in list(obs)[:12]},
        "candidate_count": len(candidates),
        "candidate_summaries": _summarize_candidates(candidates),
        "relation_telemetry": {
            "relations_total": int(telemetry.get("relations_total", 0) or 0),
            "relations_by_type": relations_by_type,
            "structural_relations": structural_relations,
            "branch_internal_operation_rows": int(telemetry.get("branch_internal_operation_rows", 0) or 0),
            "rows_with_public_effects": int(telemetry.get("rows_with_public_effects", 0) or 0),
        },
        "selected_action": commit.get("action"),
        "selected_mode": commit.get("canonical_commitment_mode"),
        "selected_reason": commit.get("canonical_commitment_reason"),
        "selected_ops": sorted(set(selected_ops)),
        "selected_assessment": _round_assessment(selected_assessment),
        "certificate_aware_reopen_or_sample_applied": bool(commit.get("certificate_aware_reopen_or_sample_applied", False)),
        "certificate_aware_stable_continuation_applied": bool(commit.get("certificate_aware_stable_continuation_applied", False)),
        "direct_controls_used": dict(commit.get("direct_controls_used", {}) or {}),
        "notes": notes,
        "watchpoints": watchpoints,
    }


def _all_cases() -> List[Tuple[str, str, Dict[str, Any], List[Dict[str, Any]]]]:
    return (
        _derive_bandit_cases()
        + _derive_renewal_cases()
        + _derive_maze_cases()
        + _derive_maintenance_cases()
        + _derive_latent_cases()
    )


def main() -> Dict[str, Any]:
    cases = [_review_case(family, name, obs, candidates) for family, name, obs, candidates in _all_cases()]
    by_family = Counter(c["family"] for c in cases)
    watchpoints = Counter(w for c in cases for w in c.get("watchpoints", []))
    modes = Counter(str(c.get("selected_mode")) for c in cases)
    relation_alive = Counter(c["family"] for c in cases if c["relation_telemetry"].get("relations_total", 0) > 0)
    structural_relation_alive = Counter(c["family"] for c in cases if c["relation_telemetry"].get("structural_relations", 0) > 0)
    result = {
        "study": "real_family_manual_trace_review_v1",
        "claim_boundary": "manual structural trace review only; not reward evidence, tuning evidence, or novelty proof",
        "summary": {
            "cases": len(cases),
            "cases_by_family": dict(sorted(by_family.items())),
            "selected_modes": dict(sorted(modes.items())),
            "families_with_relation_telemetry": dict(sorted(relation_alive.items())),
            "families_with_structural_cross_branch_relations": dict(sorted(structural_relation_alive.items())),
            "watchpoints_by_type": dict(sorted(watchpoints.items())),
            "certificate_aware_reopen_cases": sum(1 for c in cases if c.get("certificate_aware_reopen_or_sample_applied")),
            "certificate_aware_stable_cases": sum(1 for c in cases if c.get("certificate_aware_stable_continuation_applied")),
        },
        "cases": cases,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    return result


if __name__ == "__main__":
    payload = main()
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "summary": payload["summary"]}, indent=2, sort_keys=True))
