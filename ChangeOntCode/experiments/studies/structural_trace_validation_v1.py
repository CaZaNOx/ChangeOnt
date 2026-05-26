from __future__ import annotations

"""Structural trace validation v1.

This study is not a reward benchmark.  It validates whether the current
public-effect -> RelationSurface -> RCF -> CollapseCertificate -> Commitment
path produces traceable structural reasons across real adapter sample rows.

It extends architecture_acceptance_audit_v1 by reporting row-level traces,
relation on/off causal deltas, changed/unchanged commitment explanations, and
formula-ledger coverage watchpoints.
"""

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping

from agents.co.tests.relation_path_trace_diagnostics import (
    FIELD_KEYS,
    _case_candidates,
    _field_delta,
    _relation_telemetry,
    _run_candidate_commitment,
    _strip_public_effects,
)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "structural_trace_validation_v1.json"

KEY_FORMULA_FILES = [
    "agents/co/adapters/bandit_adapter.py",
    "agents/co/adapters/maintenance_replacement_adapter.py",
    "agents/co/adapters/maze_adapter.py",
    "agents/co/adapters/renewal_adapter.py",
    "agents/co/adapters/latent_mechanism_adapter.py",
    "agents/co/runtime/surfaces/candidate_surface.py",
    "agents/co/runtime/surfaces/relation_surface.py",
    "agents/co/runtime/surfaces/continuation_field.py",
    "agents/co/runtime/surfaces/collapse_certificate.py",
    "agents/co/runtime/surfaces/commitment_surface.py",
]

COEFF_RE = re.compile(r"(?<![A-Za-z0-9_])(?:0\.[0-9]+|1\.0|[2-9]\.[0-9]+)\s*\*")

LEDGER_FIELDS = [
    "relation_weight",
    "burden_regime_band",
    "decision_slot_competition",
    "collapse_blocker_pressure",
    "resolver_support",
    "earnedness",
    "recursion_demand",
    "collapse_blocked",
    "relation_ready_bonus",
    "dominance_score",
    "sampling_score",
    "continuation_score",
]


def _as_float(x: Any, default: float = 0.0) -> float:
    try:
        return float(x)
    except Exception:
        return float(default)


def _rows_by_action(rows: Iterable[Mapping[str, Any]]) -> Dict[str, Mapping[str, Any]]:
    return {str(r.get("action")): r for r in rows if r.get("action") is not None}


def _public_effect_summary(rows: List[Mapping[str, Any]]) -> Dict[str, Any]:
    by_op = Counter()
    by_type = Counter()
    by_basis = Counter()
    by_leakage = Counter()
    examples: List[Dict[str, Any]] = []
    for row in rows:
        for eff in row.get("public_effects") or []:
            if not isinstance(eff, Mapping):
                continue
            op = str(eff.get("operation", eff.get("op", "unknown")))
            typ = str(eff.get("burden_type", eff.get("effect_type", "")) or "none")
            by_op[op] += 1
            by_type[typ] += 1
            by_basis[str(eff.get("public_basis", "missing"))] += 1
            by_leakage[str(eff.get("leakage_status", "missing"))] += 1
            if len(examples) < 10:
                examples.append({
                    "candidate": row.get("candidate_id", row.get("action")),
                    "operation": op,
                    "burden_type": typ,
                    "magnitude": eff.get("magnitude", eff.get("weight")),
                    "public_basis": eff.get("public_basis"),
                    "leakage_status": eff.get("leakage_status"),
                })
    return {
        "operations": dict(by_op),
        "burden_types": dict(by_type),
        "public_basis": dict(by_basis),
        "leakage_status": dict(by_leakage),
        "examples": examples,
    }


def _row_structural_summary(row: Mapping[str, Any], assessment: Mapping[str, Any] | None = None) -> Dict[str, Any]:
    rel_types = dict(row.get("collapse_certificate_relations_by_type") or {})
    flags = list(row.get("collapse_certificate_reason_flags") or [])
    blockers = list(row.get("collapse_blockers") or [])
    cert = dict(row.get("collapse_certificate") or {})
    structural_relation_count = sum(int(v) for k, v in rel_types.items() if k not in {"decision_slot_competition"})
    weak_comp = int(rel_types.get("decision_slot_competition", 0) or 0)
    return {
        "action": row.get("action", row.get("candidate_id")),
        "candidate_id": row.get("candidate_id"),
        "branch_id": str(row.get("branch_id", ""))[:260],
        "continuation_signature": str(row.get("continuation_signature", row.get("relation_surface_effect_signature", "")))[:260],
        "identity_source": row.get("relation_surface_identity_source"),
        "public_effect_count": int(row.get("relation_surface_public_effect_count", 0) or 0),
        "branch_internal": {
            "operation_count": int(row.get("branch_internal_operation_count", 0) or 0),
            "operation_counts": dict(row.get("branch_internal_operation_counts", {}) or {}),
            "burden_types": list(row.get("branch_internal_burden_types", []) or []),
            "unresolved_pressure": row.get("branch_internal_unresolved_pressure"),
            "hiddenness_pressure": row.get("branch_internal_hiddenness_pressure"),
            "resolver_support": row.get("branch_internal_resolver_support"),
            "exposure_support": row.get("branch_internal_exposure_support"),
            "buffering_support": row.get("branch_internal_buffering_support"),
            "masking_pressure": row.get("branch_internal_masking_pressure"),
            "threshold_pressure": row.get("branch_internal_threshold_pressure"),
        },
        "relation_count": int(row.get("relation_surface_relation_count", 0) or row.get("field_relation_count", 0) or 0),
        "relations_by_type": rel_types,
        "weak_decision_competition_count": weak_comp,
        "structural_relation_count": int(structural_relation_count),
        "field": {key: row.get(key) for key in FIELD_KEYS if key in row},
        "certificate": {
            "status": row.get("collapse_certificate_status", cert.get("status")),
            "ready": row.get("collapse_certificate_ready", cert.get("ready")),
            "score": row.get("collapse_certificate_score", cert.get("score")),
            "blocker_pressure": row.get("collapse_certificate_blocker_pressure", cert.get("blocker_pressure")),
            "recursion_demand": row.get("collapse_certificate_recursion_demand", cert.get("recursion_demand")),
            "blockers": blockers,
            "reason_flags": flags,
        },
        "commitment_assessment": dict(assessment or {}),
    }


def _case_trace(name: str, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    on_rows, on_commit = _run_candidate_commitment(candidates, name)
    off_rows, off_commit = _run_candidate_commitment(_strip_public_effects(candidates), name)
    telemetry = _relation_telemetry(on_rows)
    delta = _field_delta(on_rows, off_rows)
    on_by_action = _rows_by_action(on_rows)
    off_by_action = _rows_by_action(off_rows)
    on_assess = dict(on_commit.get("canonical_commitment_assessment") or {})
    off_assess = dict(off_commit.get("canonical_commitment_assessment") or {})
    on_action = str(on_commit.get("action"))
    off_action = str(off_commit.get("action"))
    action_changed = on_commit.get("action") != off_commit.get("action")
    mode_changed = on_commit.get("canonical_commitment_mode") != off_commit.get("canonical_commitment_mode")
    selected_on = on_by_action.get(on_action, {})
    selected_off = off_by_action.get(off_action, {})
    selected_on_structural = _row_structural_summary(selected_on, on_assess.get(on_action, {})) if selected_on else {}
    selected_off_structural = _row_structural_summary(selected_off, off_assess.get(off_action, {})) if selected_off else {}
    structural_relations = sum(int(v) for k, v in dict(telemetry.get("relations_by_type") or {}).items() if k != "decision_slot_competition")
    weak_comp = int(dict(telemetry.get("relations_by_type") or {}).get("decision_slot_competition", 0) or 0)
    branch_internal_rows = int(telemetry.get("branch_internal_operation_rows", 0) or 0)
    rows = [_row_structural_summary(r, on_assess.get(str(r.get("action")), {})) for r in on_rows]

    warnings: List[str] = []
    notes: List[str] = []
    if structural_relations == 0 and branch_internal_rows == 0:
        warnings.append("no_structural_relations_or_branch_internal_operations")
    if weak_comp > 0 and weak_comp / max(1, int(telemetry.get("relations_total", 0) or 0)) > 0.75:
        # Weak decision-slot competition is expected in single-action readout spaces.
        # It is a warning only when it is the sole structural carrier.  If
        # branch-internal burden operations are present, keep it as an info note
        # so relation counts are not mistaken for strong rivalry.
        if branch_internal_rows == 0 and structural_relations == 0:
            warnings.append("weak_decision_competition_without_structural_carrier")
        else:
            notes.append("weak_decision_competition_dominates_relation_counts_but_is_nonblocking")
    if action_changed and not selected_on_structural.get("certificate", {}).get("reason_flags"):
        warnings.append("action_changed_without_visible_certificate_reason_flags")
    if action_changed and selected_on_structural.get("structural_relation_count", 0) == 0 and branch_internal_rows == 0:
        warnings.append("action_changed_to_row_without_structural_carrier")
    if (
        not action_changed
        and not mode_changed
        and structural_relations > 0
        and delta.get("scalar_field_delta_max", 0.0) > 0.25
    ):
        warnings.append("large_per_branch_scalar_field_delta_without_commitment_change_requires_manual_review")
    elif (
        not action_changed
        and not mode_changed
        and structural_relations > 0
        and delta.get("scalar_field_delta_l1", delta.get("field_delta_l1", 0.0)) > 0.50
    ):
        notes.append("distributed_scalar_field_delta_without_commitment_change_reviewed_as_stability_case")
    if (not action_changed and not mode_changed and structural_relations > 0 and delta.get("topology_count_delta_l1", 0.0) > 0.0):
        notes.append("topology_count_delta_without_commitment_change_reviewed_separately")

    if warnings:
        status = "WATCHPOINTS"
    elif notes:
        status = "OK_WITH_NOTES"
    else:
        status = "OK"

    return {
        "family": name,
        "status": status,
        "warnings": warnings,
        "notes": notes,
        "candidate_rows": len(on_rows),
        "public_effect_summary": _public_effect_summary(candidates),
        "relations_total": int(telemetry.get("relations_total", 0) or 0),
        "relations_by_type": dict(telemetry.get("relations_by_type", {}) or {}),
        "structural_relations": int(structural_relations),
        "weak_decision_competition_relations": int(weak_comp),
        "branch_internal_operation_rows": int(branch_internal_rows),
        "branch_internal_unresolved_pressure_total": float(telemetry.get("branch_internal_unresolved_pressure_total", 0.0) or 0.0),
        "branch_internal_hiddenness_pressure_total": float(telemetry.get("branch_internal_hiddenness_pressure_total", 0.0) or 0.0),
        "branch_internal_resolver_support_total": float(telemetry.get("branch_internal_resolver_support_total", 0.0) or 0.0),
        "identity_source_counts": dict(telemetry.get("identity_source_counts", {}) or {}),
        "field_delta": delta,
        "commitment": {
            "on_action": on_commit.get("action"),
            "off_action": off_commit.get("action"),
            "on_mode": on_commit.get("canonical_commitment_mode"),
            "off_mode": off_commit.get("canonical_commitment_mode"),
            "on_reason": on_commit.get("canonical_commitment_reason"),
            "off_reason": off_commit.get("canonical_commitment_reason"),
            "action_changed": bool(action_changed),
            "mode_changed": bool(mode_changed),
            "selected_on": selected_on_structural,
            "selected_off": selected_off_structural,
        },
        "rows": rows,
    }


def _formula_scan() -> Dict[str, Any]:
    files: List[Dict[str, Any]] = []
    total = 0
    for rel in KEY_FORMULA_FILES:
        path = ROOT / rel
        if not path.exists():
            files.append({"path": rel, "missing": True, "coefficient_lines": 0, "examples": []})
            continue
        examples: List[Dict[str, Any]] = []
        count = 0
        for idx, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            if COEFF_RE.search(line):
                count += 1
                if len(examples) < 12:
                    examples.append({"line": idx, "text": line.strip()})
        total += count
        files.append({"path": rel, "coefficient_lines": count, "examples": examples})
    ledger = (ROOT / "docs/kernel_spec/79_CANDIDATE_AND_COMMITMENT_FORMULA_GROUNDING_PROTOCOL.md").read_text(encoding="utf-8", errors="ignore")
    covered = {field: (field in ledger) for field in LEDGER_FIELDS}
    missing = [field for field, ok in covered.items() if not ok]
    return {
        "status": "PASS_WITH_WATCHPOINTS" if not missing else "NEEDS_LEDGER_EXPANSION",
        "formula_coefficient_lines": total,
        "files": files,
        "ledger_fields_checked": covered,
        "missing_ledger_fields": missing,
        "finding": "Formula ledger covers the initial certificate/readout critical fields, but many coefficient lines remain provisional-global proxies rather than paper-final laws.",
    }


def main() -> None:
    cases = _case_candidates()
    traces = [_case_trace(name, cand) for name, cand in cases.items()]
    changed = [c for c in traces if c["commitment"]["action_changed"] or c["commitment"]["mode_changed"]]
    warnings = [c for c in traces if c["warnings"]]
    formula = _formula_scan()
    result = {
        "study": "structural_trace_validation_v1",
        "status": "PASS_WITH_WATCHPOINTS" if not any("action_changed_without_visible" in w for c in traces for w in c["warnings"]) else "NEEDS_REVIEW",
        "summary": {
            "cases": len(traces),
            "candidate_rows": sum(c["candidate_rows"] for c in traces),
            "relations_total": sum(c["relations_total"] for c in traces),
            "structural_relations": sum(c["structural_relations"] for c in traces),
            "weak_decision_competition_relations": sum(c["weak_decision_competition_relations"] for c in traces),
            "branch_internal_operation_rows": sum(c["branch_internal_operation_rows"] for c in traces),
            "field_delta_positive_cases": sum(1 for c in traces if c["field_delta"]["field_delta_l1"] > 0.0),
            "commitment_changed_cases": len(changed),
            "cases_with_watchpoints": len(warnings),
        },
        "case_traces": traces,
        "formula_grounding": formula,
        "interpretation": [
            "This is mechanism/trace validation, not reward evidence.",
            "The relation path is structurally live if field deltas and certificate/readout changes have explicit relation/certificate reasons.",
            "Weak decision-slot competition remains logged but should not be treated as strong rivalry or collapse blockage.",
            "Branch-internal burden operations are now reported separately from cross-branch relation topology.",
            "Formula coefficients remain provisional unless ledger entries, invariants, and ablations justify them.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "status": result["status"], "summary": result["summary"], "formula_lines": formula["formula_coefficient_lines"]}, indent=2))


if __name__ == "__main__":
    main()
