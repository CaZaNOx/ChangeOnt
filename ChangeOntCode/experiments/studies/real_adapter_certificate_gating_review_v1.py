from __future__ import annotations

"""Real-adapter certificate-gating review v1.

This diagnostic is not a reward benchmark. It asks whether the
certificate-aware stable-continuation rule introduced for controlled
microcases actually activates on real adapter candidate rows, and whether
blocked selections that bypass that rule through ``reopen_or_sample`` are
structurally justified by exposure/reduction/cancellation effects.

Scope:
- standard relation-path sample cases used by existing structural diagnostics;
- a conservative maintenance and latent-mechanism sweep over public observations
  likely to produce blocked continuations or unblocked exposure alternatives.

Claim boundary: structural readout review only; no performance, novelty, or
benchmark claim.
"""

import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Tuple

from agents.co.adapters.latent_mechanism_adapter import COAdapterLatentMechanism
from agents.co.adapters.maintenance_replacement_adapter import COAdapterMaintenanceReplacement
from agents.co.tests.relation_path_trace_diagnostics import (
    DummyCore,
    TraceHeader,
    TraceHeaderState,
    _case_candidates,
    _run_candidate_commitment,
)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "real_adapter_certificate_gating_review_v1.json"

RESOLVER_OPS = {"reduce", "reveal", "reset", "cancel", "cancellation", "buffer", "absorb", "expose"}
CARRIER_ONLY_OPS = {"carry", "mask", "postpone", "defer"}
DECISION_SLOT_OPS = {"decision_slot", "single_decision_slot"}


def _action_key(x: Any) -> str:
    return str(x)


def _effects_for_action(candidates: Iterable[Mapping[str, Any]], action: Any) -> List[Dict[str, Any]]:
    key = _action_key(action)
    for cand in candidates:
        if _action_key(cand.get("candidate_id", cand.get("action"))) == key:
            return [dict(e) for e in cand.get("public_effects", []) if isinstance(e, Mapping)]
    return []


def _ops(effects: Iterable[Mapping[str, Any]]) -> List[str]:
    return [str(e.get("operation", e.get("op", ""))).strip().lower() for e in effects]


def _has_resolver(effects: Iterable[Mapping[str, Any]]) -> bool:
    return any(op in RESOLVER_OPS for op in _ops(effects))


def _has_only_carrier_or_slot(effects: Iterable[Mapping[str, Any]]) -> bool:
    relevant = [op for op in _ops(effects) if op not in DECISION_SLOT_OPS]
    return bool(relevant) and all(op in CARRIER_ONLY_OPS for op in relevant)


def _blocked(assessment: Mapping[str, Any], controls: Mapping[str, Any]) -> bool:
    collapse = float(controls.get("collapse_admissibility", 0.45) or 0.45)
    return bool(
        float(assessment.get("certificate_blocks_dominance", 0.0) or 0.0) >= 0.5
        or (float(assessment.get("collapse_blocked", 0.0) or 0.0) >= 0.55 and collapse < 0.75)
    )


def _review_case(name: str, candidates: List[Dict[str, Any]], source: str) -> Dict[str, Any]:
    rows, commit = _run_candidate_commitment(list(candidates), name)
    assessments = {str(k): dict(v) for k, v in dict(commit.get("canonical_commitment_assessment", {}) or {}).items()}
    controls = dict(commit.get("direct_controls_used", {}) or {})
    selected = commit.get("action")
    selected_key = _action_key(selected)
    mode = str(commit.get("canonical_commitment_mode"))
    reason = str(commit.get("canonical_commitment_reason"))
    applied = bool(commit.get("certificate_aware_stable_continuation_applied", False))
    selected_assessment = assessments.get(selected_key, {})
    selected_blocked = bool(selected_assessment and _blocked(selected_assessment, controls))

    ordered_cont = sorted(
        assessments.items(),
        key=lambda kv: float(kv[1].get("continuation_score", 0.0) or 0.0),
        reverse=True,
    )
    top_cont_action = ordered_cont[0][0] if ordered_cont else None
    top_cont_assessment = ordered_cont[0][1] if ordered_cont else {}
    top_cont_blocked = bool(top_cont_assessment and _blocked(top_cont_assessment, controls))
    unblocked = [(a, ass) for a, ass in ordered_cont if not _blocked(ass, controls)]
    best_unblocked_action = unblocked[0][0] if unblocked else None
    best_unblocked_assessment = unblocked[0][1] if unblocked else {}
    unblocked_resolvers = [(a, ass) for a, ass in unblocked if float(ass.get("resolver_support", 0.0) or 0.0) >= 0.08]
    best_unblocked_resolver_action = unblocked_resolvers[0][0] if unblocked_resolvers else None
    best_unblocked_resolver_assessment = unblocked_resolvers[0][1] if unblocked_resolvers else {}
    has_unblocked_alt = best_unblocked_action is not None

    top_gap_vs_unblocked = None
    top_support_gap_vs_unblocked = None
    if top_cont_action is not None and best_unblocked_action is not None:
        top_gap_vs_unblocked = float(top_cont_assessment.get("continuation_score", 0.0) or 0.0) - float(best_unblocked_assessment.get("continuation_score", 0.0) or 0.0)
        top_support_gap_vs_unblocked = float(top_cont_assessment.get("support", 0.0) or 0.0) - float(best_unblocked_assessment.get("support", 0.0) or 0.0)

    selected_effects = _effects_for_action(candidates, selected)
    selected_ops = _ops(selected_effects)
    selected_has_resolver = _has_resolver(selected_effects)
    selected_only_carries = _has_only_carrier_or_slot(selected_effects)

    watchpoints: List[str] = []
    notes: List[str] = []
    if mode == "stable_continuation" and selected_blocked and has_unblocked_alt and not applied:
        watchpoints.append("stable_selected_blocked_despite_unblocked_alternative_without_certificate_aware_switch")
    if top_cont_blocked and has_unblocked_alt and mode != "stable_continuation":
        notes.append("blocked_top_continuation_bypassed_by_prior_readout_mode")
    if mode == "reopen_or_sample" and selected_blocked and not selected_has_resolver:
        if best_unblocked_resolver_action is not None:
            watchpoints.append("reopen_or_sample_selected_blocked_branch_despite_unblocked_resolver_alternative")
            if selected_only_carries:
                watchpoints.append("reopen_or_sample_selected_carrier_only_blocked_branch_despite_unblocked_resolver")
        else:
            notes.append("reopen_or_sample_selected_blocked_without_unblocked_resolver_alternative")
    if mode == "reopen_or_sample" and selected_blocked and selected_has_resolver:
        notes.append("blocked_sampling_selection_has_public_resolver_effect")
    if bool(commit.get("certificate_aware_reopen_or_sample_applied", False)):
        notes.append("certificate_aware_reopen_or_sample_applied")
    if applied:
        notes.append("certificate_aware_stable_continuation_applied")

    return {
        "name": name,
        "source": source,
        "candidate_rows": len(rows),
        "selected_action": selected,
        "selected_mode": mode,
        "selected_reason": reason,
        "selected_blocked": selected_blocked,
        "selected_ops": selected_ops,
        "selected_has_resolver_effect": selected_has_resolver,
        "certificate_aware_stable_continuation_applied": applied,
        "certificate_aware_alternative": commit.get("certificate_aware_stable_continuation_alternative"),
        "certificate_aware_reopen_or_sample_applied": bool(commit.get("certificate_aware_reopen_or_sample_applied", False)),
        "certificate_aware_reopen_or_sample_original": commit.get("certificate_aware_reopen_or_sample_original"),
        "certificate_aware_reopen_or_sample_alternative": commit.get("certificate_aware_reopen_or_sample_alternative"),
        "top_continuation_action": top_cont_action,
        "top_continuation_blocked": top_cont_blocked,
        "best_unblocked_continuation_action": best_unblocked_action,
        "best_unblocked_resolver_action": best_unblocked_resolver_action,
        "best_unblocked_resolver_assessment": _round_assessment(best_unblocked_resolver_assessment),
        "top_continuation_gap_vs_best_unblocked": None if top_gap_vs_unblocked is None else round(top_gap_vs_unblocked, 6),
        "top_support_gap_vs_best_unblocked": None if top_support_gap_vs_unblocked is None else round(top_support_gap_vs_unblocked, 6),
        "selected_assessment": _round_assessment(selected_assessment),
        "top_continuation_assessment": _round_assessment(top_cont_assessment),
        "best_unblocked_assessment": _round_assessment(best_unblocked_assessment),
        "notes": notes,
        "watchpoints": watchpoints,
    }


def _round_assessment(assessment: Mapping[str, Any]) -> Dict[str, float]:
    keys = (
        "support",
        "burden",
        "stability",
        "dominance_score",
        "sampling_score",
        "continuation_score",
        "collapse_blocked",
        "certificate_gate_open",
        "certificate_blocks_dominance",
        "collapse_certificate_blocker_pressure",
        "collapse_certificate_recursion_demand",
    )
    out: Dict[str, float] = {}
    for key in keys:
        try:
            out[key] = round(float(assessment.get(key, 0.0) or 0.0), 6)
        except Exception:
            out[key] = 0.0
    return out


def _standard_cases() -> List[Tuple[str, List[Dict[str, Any]], str]]:
    return [(name, list(candidates), "standard_trace_sample") for name, candidates in _case_candidates().items()]


def _maintenance_sweep() -> List[Tuple[str, List[Dict[str, Any]], str]]:
    out: List[Tuple[str, List[Dict[str, Any]], str]] = []
    idx = 0
    for mode in ["direct", "partial", "hidden"]:
        for health in [None, 0, 1, 2, 3, 4]:
            for degradation in [0.05, 0.20, 0.45, 0.70]:
                for noise in [0.10, 0.40, 0.70]:
                    obs = {
                        "observed_health": health,
                        "max_health": 4,
                        "health_observed": health is not None,
                        "degradation_prob_public": degradation,
                        "wait_recovery_prob_public": 0.0,
                        "repair_cost_public": 0.80,
                        "replace_cost_public": 2.0,
                        "failure_penalty_public": 8.0,
                        "observe_health_mode": mode,
                        "observation_noise_public": noise,
                    }
                    try:
                        candidates = COAdapterMaintenanceReplacement(DummyCore())._derive(obs)["candidates"]
                    except Exception:
                        idx += 1
                        continue
                    name = f"maintenance_sweep_{idx}_{mode}_health_{health}_deg_{degradation}_noise_{noise}"
                    out.append((name, list(candidates), "maintenance_public_observation_sweep"))
                    idx += 1
    return out


def _latent_sweep() -> List[Tuple[str, List[Dict[str, Any]], str]]:
    out: List[Tuple[str, List[Dict[str, Any]], str]] = []
    idx = 0
    for hiddenness in [0.0, 0.20, 0.40, 0.60, 0.80, 1.0]:
        for deceptiveness in [0.0, 0.30, 0.70]:
            for pos in [(0, 0), (0, 1), (1, 0), (1, 1), (2, 1)]:
                obs = {
                    "pos": pos,
                    "goal": (2, 2),
                    "door": (1, 1),
                    "switches": [(0, 1)],
                    "decoys": [(1, 0)],
                    "legal_actions": ["UP", "DOWN", "LEFT", "RIGHT", "INTERACT"],
                    "door_open": False,
                    "hiddenness": hiddenness,
                    "rewrite_harshness": 0.40,
                    "local_deceptiveness": deceptiveness,
                }
                try:
                    candidates = COAdapterLatentMechanism(DummyCore())._derive(obs)["candidates"]
                except Exception:
                    idx += 1
                    continue
                name = f"latent_sweep_{idx}_hidden_{hiddenness}_decept_{deceptiveness}_pos_{pos}"
                out.append((name, list(candidates), "latent_public_observation_sweep"))
                idx += 1
    return out


def _summarize(cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    modes = Counter(str(c.get("selected_mode")) for c in cases)
    sources = Counter(str(c.get("source")) for c in cases)
    watch = Counter(w for c in cases for w in c.get("watchpoints", []))
    notes = Counter(n for c in cases for n in c.get("notes", []))
    return {
        "cases": len(cases),
        "sources": dict(sorted(sources.items())),
        "modes": dict(sorted(modes.items())),
        "certificate_aware_stable_continuation_applied_cases": sum(1 for c in cases if c.get("certificate_aware_stable_continuation_applied")),
        "certificate_aware_reopen_or_sample_applied_cases": sum(1 for c in cases if c.get("certificate_aware_reopen_or_sample_applied")),
        "stable_selected_blocked_with_unblocked_alternative_without_switch": sum(1 for c in cases if "stable_selected_blocked_despite_unblocked_alternative_without_certificate_aware_switch" in c.get("watchpoints", [])),
        "blocked_top_continuation_with_unblocked_alt_bypassed_by_prior_mode": sum(1 for c in cases if "blocked_top_continuation_bypassed_by_prior_readout_mode" in c.get("notes", [])),
        "reopen_or_sample_selected_blocked_cases": sum(1 for c in cases if c.get("selected_mode") == "reopen_or_sample" and c.get("selected_blocked")),
        "reopen_or_sample_selected_blocked_with_resolver_effect": sum(1 for c in cases if c.get("selected_mode") == "reopen_or_sample" and c.get("selected_blocked") and c.get("selected_has_resolver_effect")),
        "reopen_or_sample_selected_blocked_without_unblocked_resolver_note": sum(1 for c in cases if "reopen_or_sample_selected_blocked_without_unblocked_resolver_alternative" in c.get("notes", [])),
        "reopen_or_sample_selected_blocked_despite_unblocked_resolver_watchpoints": sum(1 for c in cases if "reopen_or_sample_selected_blocked_branch_despite_unblocked_resolver_alternative" in c.get("watchpoints", [])),
        "watchpoints_by_type": dict(sorted(watch.items())),
        "notes_by_type": dict(sorted(notes.items())),
    }


def main() -> Dict[str, Any]:
    all_inputs = _standard_cases() + _maintenance_sweep() + _latent_sweep()
    cases = [_review_case(name, candidates, source) for name, candidates, source in all_inputs]
    standard_cases = [c for c in cases if c["source"] == "standard_trace_sample"]
    sweep_cases = [c for c in cases if c["source"] != "standard_trace_sample"]
    watchpoint_cases = [c for c in cases if c.get("watchpoints")]
    notable_cases = [
        c for c in cases
        if c.get("certificate_aware_stable_continuation_applied")
        or c.get("top_continuation_blocked") and c.get("best_unblocked_continuation_action") is not None
        or c.get("watchpoints")
    ]
    result = {
        "study": "real_adapter_certificate_gating_review_v1",
        "claim_boundary": "structural real-adapter readout review only; not reward evidence, not novelty proof, not broad benchmark evidence",
        "summary": _summarize(cases),
        "standard_sample_summary": _summarize(standard_cases),
        "sweep_summary": _summarize(sweep_cases),
        "notable_cases": notable_cases[:80],
        "watchpoint_cases": watchpoint_cases[:80],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    return result


if __name__ == "__main__":
    payload = main()
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "summary": payload["summary"], "standard_sample_summary": payload["standard_sample_summary"]}, indent=2, sort_keys=True))
