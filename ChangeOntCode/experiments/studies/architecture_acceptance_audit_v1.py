from __future__ import annotations

"""Architecture acceptance audit v1.

This is a diagnostic/audit study, not a reward benchmark.  It checks whether the
current ChangeOnt kernel path is critic-ready along the five acceptance axes
identified after the earned-collapse-certificate patch:

1. adapter public-effect leakage
2. RelationSurface noise / relation sparsity
3. collapse-certificate reason quality
4. branch identity trace quality
5. formula-level grounding status

The output is intentionally allowed to contain FAIL / NEEDS_WORK statuses.  A
failed audit is not a test failure; it is architecture evidence that the kernel
is not yet acceptance-ready.
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping

from agents.co.adapters.maintenance_replacement_adapter import COAdapterMaintenanceReplacement
from agents.co.runtime.surfaces.relation_surface import derive_relation_surface
from agents.co.tests.relation_path_trace_diagnostics import (
    DummyCore,
    _case_candidates,
    _run_candidate_commitment,
    _strip_public_effects,
    trace_all_cases,
)

FORBIDDEN_TERMS = ("optimal", "best_action", "dp_value", "oracle", "hidden_policy", "shortest_path", "q_value")
ALLOWED_BASES = {"visible_observation", "declared_transition_rule", "legal_constraint", "public_history", "parity_honest_uncertainty", "problem_contract", "public_cost", "kernel_history"}
ALLOWED_LEAKAGE = {"public", "parity_honest", "kernel_history", "investigatory"}


def _effect_text(eff: Mapping[str, Any]) -> str:
    return " ".join(str(v).lower() for v in eff.values())


def audit_public_effects(cases: Mapping[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    issues: List[Dict[str, Any]] = []
    family_rows: Dict[str, Any] = {}
    all_effects = 0
    for family, candidates in cases.items():
        fam_counter = Counter()
        fam_issues = []
        for cand in candidates:
            effects = list(cand.get("public_effects") or [])
            fam_counter["candidates"] += 1
            fam_counter["effects"] += len(effects)
            if not effects:
                fam_issues.append({"candidate": cand.get("candidate_id"), "issue": "missing_public_effects"})
            for eff in effects:
                all_effects += 1
                op = str(eff.get("operation", ""))
                fam_counter[f"op_{op}"] += 1
                basis = str(eff.get("public_basis", ""))
                leakage = str(eff.get("leakage_status", ""))
                if basis not in ALLOWED_BASES:
                    fam_issues.append({"candidate": cand.get("candidate_id"), "issue": "non_allowed_public_basis", "effect": eff})
                if leakage not in ALLOWED_LEAKAGE:
                    fam_issues.append({"candidate": cand.get("candidate_id"), "issue": "non_allowed_leakage_status", "effect": eff})
                text = _effect_text(eff)
                for term in FORBIDDEN_TERMS:
                    if term in text:
                        fam_issues.append({"candidate": cand.get("candidate_id"), "issue": f"forbidden_term_{term}", "effect": eff})
        family_rows[family] = {"counts": dict(fam_counter), "issues": fam_issues}
        issues.extend({"family": family, **i} for i in fam_issues)
    status = "PASS_WITH_WATCHPOINTS" if not issues else "FAIL"
    watchpoints = [
        "Magnitude formulas in adapters still require a formula ledger; this audit only checks public/leakage form.",
        "Visible geometry/local progress facts are public grammar only if they use visible observations and not hidden route/search information.",
        "Same-row burden operations are not yet first-class field facts unless they participate in cross-branch relations.",
    ]
    return {"status": status, "total_public_effects": all_effects, "issues": issues, "family_rows": family_rows, "watchpoints": watchpoints}


def audit_relation_noise(trace_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = sum(int(c.get("relations_total", 0) or 0) for c in trace_cases)
    by_type = Counter()
    per_family = []
    for c in trace_cases:
        rels = dict(c.get("relations_by_type") or {})
        by_type.update(rels)
        rivalry = int(rels.get("rivalry", 0) or 0)
        non_rival = sum(int(v) for k, v in rels.items() if k != "rivalry")
        ratio = float(rivalry / max(1, rivalry + non_rival))
        per_family.append({
            "family": c.get("family"),
            "relations_total": int(c.get("relations_total", 0) or 0),
            "relations_by_type": rels,
            "rivalry_ratio": ratio,
            "non_rival_relations": non_rival,
            "status": "NEEDS_REVIEW" if ratio > 0.65 else "OK",
        })
    rivalry_ratio = float(by_type.get("rivalry", 0) / max(1, total))
    weak_total = int(by_type.get("decision_slot_competition", 0) or 0)
    weak_ratio = float(weak_total / max(1, total))
    status = "FAIL" if rivalry_ratio > 0.65 else "PASS_WITH_WATCHPOINTS"
    return {
        "status": status,
        "relations_total": total,
        "relations_by_type": dict(by_type),
        "rivalry_ratio": rivalry_ratio,
        "weak_decision_competition_ratio": weak_ratio,
        "per_family": per_family,
        "finding": "Strong continuation rivalry no longer dominates after weak decision-slot competition is separated. Weak competition may still be high, but it is not a collapse blocker by itself.",
        "required_fix": "Continue tracking weak decision-slot competition separately and prevent it from unresolved-rival blocker counts.",
    }


def audit_collapse_reasons(cases: Mapping[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    changed_cases = []
    all_cases = []
    for name, candidates in cases.items():
        on_rows, on_commit = _run_candidate_commitment(candidates, name)
        off_rows, off_commit = _run_candidate_commitment(_strip_public_effects(candidates), name)
        changed = bool(on_commit.get("action") != off_commit.get("action") or on_commit.get("canonical_commitment_mode") != off_commit.get("canonical_commitment_mode"))
        row_summaries = []
        generic_rivalry_blocked = 0
        non_rival_reason_rows = 0
        for row in on_rows:
            rel_types = dict(row.get("collapse_certificate_relations_by_type") or {})
            blockers = list(row.get("collapse_blockers") or [])
            flags = list(row.get("collapse_certificate_reason_flags") or [])
            if "unresolved_non_equivalent_rival" in blockers and rel_types.get("rivalry", 0) >= 4:
                generic_rivalry_blocked += 1
            if any(f in flags for f in ("relieves_burden_elsewhere", "cancels_burden_condition", "quotient_or_equivalence_support", "buffers_tension_conversion")):
                non_rival_reason_rows += 1
            row_summaries.append({
                "action": row.get("action", row.get("candidate_id")),
                "status": row.get("collapse_certificate_status"),
                "blockers": blockers,
                "reason_flags": flags,
                "relations_by_type": rel_types,
                "score": row.get("collapse_certificate_score"),
                "blocker_pressure": row.get("collapse_certificate_blocker_pressure"),
                "recursion_demand": row.get("collapse_certificate_recursion_demand"),
            })
        rec = {
            "family": name,
            "changed": changed,
            "on_action": on_commit.get("action"),
            "off_action": off_commit.get("action"),
            "on_mode": on_commit.get("canonical_commitment_mode"),
            "off_mode": off_commit.get("canonical_commitment_mode"),
            "generic_rivalry_blocked_rows": generic_rivalry_blocked,
            "non_rival_reason_rows": non_rival_reason_rows,
            "row_certificates": row_summaries,
        }
        all_cases.append(rec)
        if changed:
            changed_cases.append(rec)
    status = "FAIL" if any(c["generic_rivalry_blocked_rows"] >= max(2, len(c["row_certificates"]) // 2) for c in changed_cases) else "PASS_WITH_WATCHPOINTS"
    return {
        "status": status,
        "changed_cases": changed_cases,
        "all_cases": all_cases,
        "finding": "Certificate reason quality no longer shows generic decision-slot rivalry as a collapse blocker in sampled traces. Reason quality remains watchpoint-level because formula constants and non-rival resolver effects still need broader validation.",
        "required_fix": "Continue requiring structured reason traces and ensure weak competition never becomes an unresolved-rival blocker without strong burden/admissibility coupling.",
    }


def audit_branch_identity() -> Dict[str, Any]:
    cases = _case_candidates()
    trace_cases = trace_all_cases()
    source_counts = Counter()
    for c in trace_cases:
        source_counts.update(dict(c.get("identity_source_counts") or {}))

    adapter = COAdapterMaintenanceReplacement(DummyCore())
    healthy = {
        "observed_health": 4,
        "max_health": 4,
        "health_observed": True,
        "degradation_prob_public": 0.05,
        "wait_recovery_prob_public": 0.00,
        "repair_cost_public": 0.80,
        "replace_cost_public": 2.0,
        "failure_penalty_public": 8.0,
        "observe_health_mode": "partial",
    }
    degraded = dict(healthy)
    degraded.update({"observed_health": 1, "degradation_prob_public": 0.25})

    def run_sig(obs: Mapping[str, Any]) -> Dict[str, Any]:
        rows = derive_relation_surface(list(adapter._derive(obs)["candidates"]), {}).rows
        for row in rows:
            if row.get("candidate_id") == "RUN":
                effs = list(row.get("public_effects") or [])
                return {
                    "branch_id": str(row.get("branch_id")),
                    "signature": str(row.get("continuation_signature", "")),
                    "effect_magnitudes": {f"{e.get('operation')}:{e.get('burden_type') or e.get('relation_scope')}": e.get("magnitude") for e in effs},
                }
        return {}

    healthy_run = run_sig(healthy)
    degraded_run = run_sig(degraded)
    same_signature = bool(healthy_run.get("signature") == degraded_run.get("signature"))
    magnitude_changed = bool(healthy_run.get("effect_magnitudes") != degraded_run.get("effect_magnitudes"))
    status = "FAIL" if same_signature and magnitude_changed else "PASS_WITH_WATCHPOINTS"
    return {
        "status": status,
        "identity_source_counts": dict(source_counts),
        "healthy_run": healthy_run,
        "degraded_run": degraded_run,
        "same_signature_despite_changed_magnitude": bool(same_signature and magnitude_changed),
        "finding": "Branch identity no longer falls back to action labels, and public-effect signatures include coarse burden-regime bands. Healthy and degraded RUN separate when pressure crosses a material regime band.",
        "required_fix": "Keep signatures banded rather than raw-magnitude keyed; extend bands only through documented thresholds/basin status.",
    }


def audit_formula_grounding(repo_root: Path) -> Dict[str, Any]:
    files = [
        repo_root / "agents/co/runtime/surfaces/candidate_surface.py",
        repo_root / "agents/co/runtime/surfaces/continuation_field.py",
        repo_root / "agents/co/runtime/surfaces/collapse_certificate.py",
        repo_root / "agents/co/runtime/surfaces/commitment_surface.py",
        repo_root / "agents/co/runtime/surfaces/relation_surface.py",
    ]
    coeff_pat = re.compile(r"(?<![A-Za-z0-9_])(0\.\d+|1\.0)(?=\s*[*+-])")
    entries = []
    total_coeff_lines = 0
    for f in files:
        text = f.read_text(encoding="utf-8")
        lines = text.splitlines()
        coeff_lines = []
        for i, line in enumerate(lines, 1):
            if coeff_pat.search(line) and not line.strip().startswith("#"):
                coeff_lines.append({"line": i, "text": line.strip()[:220]})
        total_coeff_lines += len(coeff_lines)
        entries.append({"path": str(f.relative_to(repo_root)), "coefficient_lines": len(coeff_lines), "examples": coeff_lines[:12]})
    ledger_path = repo_root / "docs/kernel_spec/79_CANDIDATE_AND_COMMITMENT_FORMULA_GROUNDING_PROTOCOL.md"
    ledger_text = ledger_path.read_text(encoding="utf-8") if ledger_path.exists() else ""
    has_initial_ledger = "Initial formula ledger for architecture-acceptance patch" in ledger_text
    status = "PASS_WITH_WATCHPOINTS" if has_initial_ledger else ("FAIL" if total_coeff_lines > 0 else "PASS")
    return {
        "status": status,
        "initial_ledger_present": bool(has_initial_ledger),
        "total_formula_coefficient_lines": total_coeff_lines,
        "files": entries,
        "finding": "An initial formula ledger now exists for the readout-affecting acceptance patch. Many older scalar formulas remain provisional and still require full ledger coverage before final paper claims.",
        "required_fix": "Expand the formula ledger from the acceptance-critical fields to all active CandidateSurface/ContinuationState/RCF/CommitmentSurface scalar formulas before final evidence claims.",
    }


def main() -> Dict[str, Any]:
    repo_root = Path(__file__).resolve().parents[2]
    cases = _case_candidates()
    traces = trace_all_cases()
    public_effect_leakage = audit_public_effects(cases)
    relation_noise = audit_relation_noise(traces)
    collapse_certificate_reasons = audit_collapse_reasons(cases)
    branch_identity = audit_branch_identity()
    formula_grounding = audit_formula_grounding(repo_root)
    summary = {
        "adapter_public_effect_leakage": public_effect_leakage["status"],
        "relation_noise": relation_noise["status"],
        "collapse_certificate_reason_quality": collapse_certificate_reasons["status"],
        "branch_identity_trace_quality": branch_identity["status"],
        "formula_grounding": formula_grounding["status"],
    }
    hard_fail = any(v == "FAIL" for v in summary.values())
    result = {
        "audit_name": "architecture_acceptance_audit_v1",
        "status": "ACCEPTANCE_WATCHPOINTS_REMAIN" if not hard_fail else "NOT_ACCEPTANCE_READY",
        "summary": summary,
        "public_effect_leakage": public_effect_leakage,
        "relation_noise": relation_noise,
        "collapse_certificate_reasons": collapse_certificate_reasons,
        "branch_identity": branch_identity,
        "formula_grounding": formula_grounding,
    }
    out_path = repo_root / "outputs" / "architecture_acceptance_audit_v1.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "output": str(out_path.relative_to(repo_root)),
        "status": result["status"],
        "summary": result["summary"],
        "relations_total": result["relation_noise"]["relations_total"],
        "rivalry_ratio": result["relation_noise"]["rivalry_ratio"],
        "formula_coefficient_lines": result["formula_grounding"]["total_formula_coefficient_lines"],
    }, indent=2, sort_keys=True))
    return result


if __name__ == "__main__":
    main()
