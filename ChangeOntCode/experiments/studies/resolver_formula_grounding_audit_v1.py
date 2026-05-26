from __future__ import annotations

"""Resolver formula grounding audit v1.

This diagnostic follows resolver recognition from public adapter facts through
RelationSurface branch-internal operation summaries, RCF/certificate rows, and
CommitmentSurface readout. It is a structural grounding check only: it does not
measure reward, tune coefficients, or claim novelty.
"""

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Tuple

from agents.co.adapters.common import public_effect, single_decision_slot_effect
from experiments.studies.real_adapter_formula_sensitivity_probe_v1 import (
    _all_inputs,
    _run_candidate_commitment_with_params,
)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "resolver_formula_grounding_audit_v1.json"

RELIEF_OPS = {"reduce", "relieve", "prevent"}
CANCEL_OPS = {"reset", "cancel"}
EXPOSURE_OPS = {"reveal", "expose", "reduce_hiddenness"}
BUFFER_OPS = {"buffer", "absorb"}
RESOLVER_OPS = RELIEF_OPS | CANCEL_OPS | EXPOSURE_OPS | BUFFER_OPS
CARRIER_OPS = {"carry", "increase", "amplify", "consume", "require", "mask", "postpone", "hide", "threshold", "phase_shift"}
TRANSFORM_OPS = {"transform", "transfer"}
DECISION_SLOT_OPS = {"decision_slot", "single_decision_slot"}
RESOLVER_THRESHOLD = 0.08


def _op(raw: Mapping[str, Any]) -> str:
    return str(raw.get("operation", raw.get("op", raw.get("effect", "")))).strip().lower()


def _effects(cand: Mapping[str, Any]) -> List[Dict[str, Any]]:
    value = cand.get("public_effects", cand.get("burden_effects", cand.get("effect_facts", [])))
    if isinstance(value, Mapping):
        return [dict(value)]
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
        return [dict(v) for v in value if isinstance(v, Mapping)]
    return []


def _ops_for_candidate(cand: Mapping[str, Any]) -> List[str]:
    return [_op(e) for e in _effects(cand)]


def _resolver_op_groups(ops: Iterable[str]) -> List[str]:
    groups: List[str] = []
    s = set(ops)
    if s & RELIEF_OPS:
        groups.append("relief_or_reduce")
    if s & CANCEL_OPS:
        groups.append("cancellation_or_reset")
    if s & EXPOSURE_OPS:
        groups.append("exposure_or_reveal")
    if s & BUFFER_OPS:
        groups.append("buffer_or_absorb")
    if s & TRANSFORM_OPS:
        groups.append("transform_or_transfer_nonresolver")
    if s & CARRIER_OPS:
        groups.append("carrier_or_masking")
    if s and not (s - DECISION_SLOT_OPS):
        groups.append("decision_slot_only")
    return groups


def _row_by_action(rows: Iterable[Mapping[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {str(r.get("action")): dict(r) for r in rows if r.get("action") is not None}


def _cand_by_action(candidates: Iterable[Mapping[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {str(c.get("candidate_id", c.get("action"))): dict(c) for c in candidates if c.get("candidate_id", c.get("action")) is not None}


def _assessment(commit: Mapping[str, Any], action: str) -> Dict[str, Any]:
    return dict(dict(commit.get("canonical_commitment_assessment", {}) or {}).get(str(action), {}) or {})


def _f(row: Mapping[str, Any], key: str) -> float:
    try:
        return float(row.get(key, 0.0) or 0.0)
    except Exception:
        return 0.0


def _round_fields(row: Mapping[str, Any], fields: Iterable[str]) -> Dict[str, float]:
    return {k: round(_f(row, k), 6) for k in fields}


def _review_real_case(name: str, candidates: List[Dict[str, Any]], source: str) -> Dict[str, Any]:
    rows, commit = _run_candidate_commitment_with_params(list(candidates), f"resolver_audit:{name}", {})
    rb = _row_by_action(rows)
    cb = _cand_by_action(candidates)
    selected = str(commit.get("action"))
    candidate_records: List[Dict[str, Any]] = []
    watchpoints: List[str] = []
    notes: List[str] = []

    for action, cand in cb.items():
        ops = _ops_for_candidate(cand)
        row = rb.get(action, {})
        ass = _assessment(commit, action)
        resolver_by_ops = bool(set(ops) & RESOLVER_OPS)
        transform_only = bool(set(ops) & TRANSFORM_OPS) and not resolver_by_ops and not bool(set(ops) & CARRIER_OPS)
        resolver_support = max(
            _f(row, "branch_internal_resolver_support"),
            _f(row, "branch_internal_exposure_support"),
            _f(row, "branch_internal_relief_support"),
            _f(row, "branch_internal_cancellation_support"),
            _f(row, "branch_internal_buffering_support"),
            _f(ass, "resolver_support"),
        )
        transform_pressure = _f(row, "branch_internal_transform_pressure")
        if resolver_by_ops and resolver_support <= 0.0:
            watchpoints.append("resolver_public_op_not_recognized")
        if not resolver_by_ops and resolver_support >= RESOLVER_THRESHOLD:
            watchpoints.append("resolver_support_without_resolver_public_op")
        if transform_only and resolver_support >= RESOLVER_THRESHOLD:
            watchpoints.append("transform_only_counted_as_resolver")
        if transform_pressure > 0.0 and resolver_support < RESOLVER_THRESHOLD:
            notes.append("transform_pressure_kept_nonresolver")
        candidate_records.append({
            "action": action,
            "ops": ops,
            "resolver_op_groups": _resolver_op_groups(ops),
            "resolver_by_public_ops": resolver_by_ops,
            "transform_only": transform_only,
            "row_resolver_fields": _round_fields(row, (
                "branch_internal_resolver_support",
                "branch_internal_relief_support",
                "branch_internal_cancellation_support",
                "branch_internal_exposure_support",
                "branch_internal_buffering_support",
                "branch_internal_transform_pressure",
                "branch_internal_unresolved_pressure",
                "branch_internal_hiddenness_pressure",
            )),
            "assessment": _round_fields(ass, (
                "resolver_support",
                "carrier_only_pressure",
                "collapse_blocked",
                "certificate_blocks_dominance",
                "sampling_score",
                "continuation_score",
                "dominance_score",
                "support",
            )),
        })

    return {
        "name": name,
        "source": source,
        "selected_action": selected,
        "selected_mode": commit.get("canonical_commitment_mode"),
        "selected_reason": commit.get("canonical_commitment_reason"),
        "certificate_aware_reopen_or_sample_applied": bool(commit.get("certificate_aware_reopen_or_sample_applied", False)),
        "certificate_aware_reopen_or_sample_original": commit.get("certificate_aware_reopen_or_sample_original"),
        "certificate_aware_reopen_or_sample_alternative": commit.get("certificate_aware_reopen_or_sample_alternative"),
        "candidate_records": candidate_records,
        "watchpoints": sorted(set(watchpoints)),
        "notes": sorted(set(notes)),
    }


def _spoof_candidates(resolver_action: str, carrier_action: str, *, resolver_op: str = "reduce") -> List[Dict[str, Any]]:
    return [
        {
            "candidate_id": resolver_action,
            "legal": True,
            "visible_delta": 0.64,
            "line_support": 0.64,
            "uncertainty_hint": 0.40,
            "coverage_adequacy": 0.50,
            "tested_hint": 0.50,
            "reversibility_hint": 0.50,
            "public_effects": [
                public_effect(resolver_op, "degradation", magnitude=0.70, scope="machine_health", public_basis="declared_transition_rule", direction="relieve", coupling="health_continuation"),
                single_decision_slot_effect(),
            ],
        },
        {
            "candidate_id": carrier_action,
            "legal": True,
            "visible_delta": 0.68,
            "line_support": 0.68,
            "uncertainty_hint": 0.55,
            "coverage_adequacy": 0.45,
            "tested_hint": 0.40,
            "reversibility_hint": 0.50,
            "contradiction_hint": 0.20,
            "public_effects": [
                public_effect("carry", "degradation", magnitude=0.80, scope="machine_health", public_basis="declared_transition_rule", direction="postpone", coupling="health_continuation"),
                public_effect("carry", "hiddenness", magnitude=0.70, scope="health_observability", kind="uncertainty", public_basis="visible_observation", direction="mask_or_postpone", coupling="health_continuation"),
                single_decision_slot_effect(),
            ],
        },
    ]


def _transform_only_candidates() -> List[Dict[str, Any]]:
    return [
        {
            "candidate_id": "TRANSFORM_ONLY",
            "legal": True,
            "visible_delta": 0.64,
            "line_support": 0.64,
            "uncertainty_hint": 0.52,
            "coverage_adequacy": 0.46,
            "tested_hint": 0.42,
            "reversibility_hint": 0.48,
            "public_effects": [
                public_effect("transform", "mechanism_hiddenness", magnitude=0.75, scope="mechanism", public_basis="declared_transition_rule", direction="rewrite", coupling="door_mechanism"),
                single_decision_slot_effect(),
            ],
        },
        {
            "candidate_id": "CARRIER_ONLY",
            "legal": True,
            "visible_delta": 0.64,
            "line_support": 0.64,
            "uncertainty_hint": 0.52,
            "coverage_adequacy": 0.46,
            "tested_hint": 0.42,
            "reversibility_hint": 0.48,
            "public_effects": [
                public_effect("carry", "mechanism_hiddenness", magnitude=0.75, scope="mechanism", kind="uncertainty", public_basis="visible_observation", direction="unresolved", coupling="door_mechanism"),
                single_decision_slot_effect(),
            ],
        },
    ]


def _microcase_record(name: str, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    rows, commit = _run_candidate_commitment_with_params(candidates, f"resolver_microcase:{name}", {})
    rb = _row_by_action(rows)
    records = []
    for cand in candidates:
        action = str(cand["candidate_id"])
        row = rb.get(action, {})
        ass = _assessment(commit, action)
        records.append({
            "action": action,
            "ops": _ops_for_candidate(cand),
            "resolver_op_groups": _resolver_op_groups(_ops_for_candidate(cand)),
            "row_resolver_fields": _round_fields(row, (
                "branch_internal_resolver_support",
                "branch_internal_relief_support",
                "branch_internal_cancellation_support",
                "branch_internal_exposure_support",
                "branch_internal_buffering_support",
                "branch_internal_transform_pressure",
                "branch_internal_unresolved_pressure",
                "branch_internal_hiddenness_pressure",
            )),
            "assessment": _round_fields(ass, (
                "resolver_support",
                "carrier_only_pressure",
                "collapse_blocked",
                "certificate_blocks_dominance",
                "dominance_score",
                "sampling_score",
                "continuation_score",
                "support",
            )),
        })
    return {
        "name": name,
        "selected_action": commit.get("action"),
        "selected_mode": commit.get("canonical_commitment_mode"),
        "selected_reason": commit.get("canonical_commitment_reason"),
        "records": records,
    }


def _summarize(cases: List[Dict[str, Any]], microcases: List[Dict[str, Any]]) -> Dict[str, Any]:
    source_counts = Counter(c["source"] for c in cases)
    op_counts: Counter = Counter()
    group_counts: Counter = Counter()
    row_watchpoints: Counter = Counter(w for c in cases for w in c["watchpoints"])
    notes = Counter(n for c in cases for n in c["notes"])
    rows = 0
    resolver_rows = 0
    transform_pressure_rows = 0
    transform_only_resolver_rows = 0
    selected_resolver_rows = 0
    selected_transform_only_resolver_rows = 0
    certificate_reopen_by_alt_group: Counter = Counter()
    for c in cases:
        selected = str(c["selected_action"])
        alt = c.get("certificate_aware_reopen_or_sample_alternative")
        for rec in c["candidate_records"]:
            rows += 1
            ops = list(rec["ops"])
            op_counts.update(op for op in ops if op)
            group_counts.update(rec["resolver_op_groups"])
            ass = rec["assessment"]
            is_resolver = float(ass.get("resolver_support", 0.0) or 0.0) >= RESOLVER_THRESHOLD
            if is_resolver:
                resolver_rows += 1
            if rec["row_resolver_fields"].get("branch_internal_transform_pressure", 0.0) > 0.0:
                transform_pressure_rows += 1
            if rec["transform_only"] and is_resolver:
                transform_only_resolver_rows += 1
            if rec["action"] == selected and is_resolver:
                selected_resolver_rows += 1
            if rec["action"] == selected and rec["transform_only"] and is_resolver:
                selected_transform_only_resolver_rows += 1
            if alt is not None and rec["action"] == str(alt):
                certificate_reopen_by_alt_group.update(rec["resolver_op_groups"])
    spoof_checks = {}
    for m in microcases:
        by_action = {r["action"]: r for r in m["records"]}
        if m["name"] == "resolver_action_name_spoof_run_reduces_repair_carries":
            spoof_checks["run_named_resolver_recognized"] = by_action["RUN"]["assessment"]["resolver_support"] >= RESOLVER_THRESHOLD
            spoof_checks["repair_named_carrier_not_resolver"] = by_action["REPAIR"]["assessment"]["resolver_support"] < RESOLVER_THRESHOLD
        if m["name"] == "resolver_action_name_spoof_repair_reduces_run_carries":
            spoof_checks["repair_named_resolver_recognized"] = by_action["REPAIR"]["assessment"]["resolver_support"] >= RESOLVER_THRESHOLD
            spoof_checks["run_named_carrier_not_resolver"] = by_action["RUN"]["assessment"]["resolver_support"] < RESOLVER_THRESHOLD
        if m["name"] == "transform_only_is_not_resolver":
            spoof_checks["transform_only_not_resolver"] = by_action["TRANSFORM_ONLY"]["assessment"]["resolver_support"] < RESOLVER_THRESHOLD
            spoof_checks["transform_pressure_recorded"] = by_action["TRANSFORM_ONLY"]["row_resolver_fields"]["branch_internal_transform_pressure"] > 0.0
    return {
        "cases": len(cases),
        "candidate_rows_reviewed": rows,
        "sources": dict(sorted(source_counts.items())),
        "public_effect_operation_counts": dict(op_counts.most_common()),
        "operation_group_counts": dict(group_counts.most_common()),
        "resolver_rows_at_threshold": resolver_rows,
        "transform_pressure_rows": transform_pressure_rows,
        "transform_only_rows_counted_as_resolver": transform_only_resolver_rows,
        "selected_resolver_rows_at_threshold": selected_resolver_rows,
        "selected_transform_only_rows_counted_as_resolver": selected_transform_only_resolver_rows,
        "certificate_aware_reopen_alternative_groups": dict(certificate_reopen_by_alt_group.most_common()),
        "watchpoints_by_type": dict(sorted(row_watchpoints.items())),
        "notes_by_type": dict(sorted(notes.items())),
        "microcase_checks": spoof_checks,
    }


def main() -> Dict[str, Any]:
    cases = [_review_real_case(name, list(candidates), source) for name, candidates, source in _all_inputs()]
    microcases = [
        _microcase_record("resolver_action_name_spoof_run_reduces_repair_carries", _spoof_candidates("RUN", "REPAIR", resolver_op="reduce")),
        _microcase_record("resolver_action_name_spoof_repair_reduces_run_carries", _spoof_candidates("REPAIR", "RUN", resolver_op="reduce")),
        _microcase_record("exposure_action_name_spoof_interact_reveals_run_carries", _spoof_candidates("INTERACT", "RUN", resolver_op="reveal")),
        _microcase_record("cancellation_action_name_spoof_replace_resets_run_carries", _spoof_candidates("REPLACE", "RUN", resolver_op="reset")),
        _microcase_record("buffer_action_name_spoof_wait_buffers_run_carries", _spoof_candidates("WAIT", "RUN", resolver_op="buffer")),
        _microcase_record("transform_only_is_not_resolver", _transform_only_candidates()),
    ]
    summary = _summarize(cases, microcases)
    watchpoint_cases = [c for c in cases if c["watchpoints"]]
    notable = [
        c for c in cases
        if c.get("certificate_aware_reopen_or_sample_applied")
        or c.get("watchpoints")
        or "transform_pressure_kept_nonresolver" in c.get("notes", [])
    ]
    result = {
        "study": "resolver_formula_grounding_audit_v1",
        "claim_boundary": "structural resolver-formula grounding only; not reward evidence, not parameter tuning, not novelty proof",
        "resolver_definition": {
            "resolver_ops": sorted(RESOLVER_OPS),
            "carrier_ops": sorted(CARRIER_OPS),
            "transform_ops_nonresolver_without_explicit_reduce_reveal_reset_buffer": sorted(TRANSFORM_OPS),
            "resolver_threshold": RESOLVER_THRESHOLD,
        },
        "summary": summary,
        "microcases": microcases,
        "watchpoint_cases": watchpoint_cases[:80],
        "notable_cases": notable[:100],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    return result


if __name__ == "__main__":
    payload = main()
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "summary": payload["summary"]}, indent=2, sort_keys=True))
