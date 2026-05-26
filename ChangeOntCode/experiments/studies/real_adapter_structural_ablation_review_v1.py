from __future__ import annotations

"""Real-adapter structural ablation review v1.

This diagnostic extends the small structural ablation probe from the five
standard trace cases to the broader public-observation sweep used by the
certificate-gating review. It is not a reward benchmark. It asks whether the
currently active runtime decisions depend on lawful public-effect structure
rather than only on scalar candidate support.

Variants:
- full: adapter candidate rows unchanged;
- no_public_effects: removes all public_effects/burden effects;
- weak_competition_only: keeps only procedural decision-slot facts;
- no_weak_competition: removes decision-slot facts but keeps burden/effect facts;
- branch_internal_only_unique_scope: keeps burden/effect facts but breaks shared
  burden scopes so cross-branch relation topology is suppressed;
- no_resolver_ops: removes exposure/reduction/cancellation/buffer/transform facts;
- carrier_only_no_resolver: keeps carry/mask/postpone/defer and decision-slot facts.

Claim boundary: structural mechanism-causality review only; no performance,
novelty, or empirical success claim.
"""

import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Tuple

from agents.co.tests.relation_path_trace_diagnostics import _run_candidate_commitment
from experiments.studies.real_adapter_certificate_gating_review_v1 import (
    _latent_sweep,
    _maintenance_sweep,
    _standard_cases,
)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "real_adapter_structural_ablation_review_v1.json"

DECISION_SLOT_OPS = {"decision_slot", "single_decision_slot"}
RESOLVER_OPS = {"reduce", "reveal", "reset", "cancel", "cancellation", "buffer", "absorb", "expose", "transform"}
CARRIER_OPS = {"carry", "mask", "postpone", "defer"}


def _op(effect: Mapping[str, Any]) -> str:
    return str(effect.get("operation", effect.get("op", ""))).strip().lower()


def _mutate_effects(candidates: Iterable[Mapping[str, Any]], variant: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for raw in candidates:
        cand = dict(deepcopy(raw))
        effects = [dict(e) for e in cand.get("public_effects", []) if isinstance(e, Mapping)]
        if variant == "full":
            pass
        elif variant == "no_public_effects":
            cand.pop("public_effects", None)
            cand.pop("burden_effects", None)
            cand.pop("effect_facts", None)
        elif variant == "weak_competition_only":
            cand["public_effects"] = [e for e in effects if _op(e) in DECISION_SLOT_OPS]
        elif variant == "no_weak_competition":
            cand["public_effects"] = [e for e in effects if _op(e) not in DECISION_SLOT_OPS]
        elif variant == "branch_internal_only_unique_scope":
            expr = str(cand.get("continuation_id", cand.get("branch_id", cand.get("candidate_id", cand.get("action", "candidate")))))
            unique_effects = []
            for effect in effects:
                if _op(effect) in DECISION_SLOT_OPS:
                    continue
                e = dict(effect)
                for key in ("burden_type", "relation_scope", "scope", "resource", "resource_type"):
                    if e.get(key):
                        e[key] = f"{e[key]}__{expr}"
                unique_effects.append(e)
            cand["public_effects"] = unique_effects
        elif variant == "no_resolver_ops":
            cand["public_effects"] = [e for e in effects if _op(e) not in RESOLVER_OPS]
        elif variant == "carrier_only_no_resolver":
            cand["public_effects"] = [e for e in effects if _op(e) in CARRIER_OPS or _op(e) in DECISION_SLOT_OPS]
        else:
            raise ValueError(f"unknown ablation variant: {variant}")
        out.append(cand)
    return out


def _blocked(assessment: Mapping[str, Any], controls: Mapping[str, Any]) -> bool:
    collapse = float(controls.get("collapse_admissibility", 0.45) or 0.45)
    return bool(
        float(assessment.get("certificate_blocks_dominance", 0.0) or 0.0) >= 0.5
        or (float(assessment.get("collapse_blocked", 0.0) or 0.0) >= 0.55 and collapse < 0.75)
    )


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
        "resolver_support",
        "carrier_only_pressure",
    )
    out: Dict[str, float] = {}
    for key in keys:
        try:
            out[key] = round(float(assessment.get(key, 0.0) or 0.0), 6)
        except Exception:
            out[key] = 0.0
    return out


def _run_variant(name: str, candidates: List[Dict[str, Any]], variant: str) -> Dict[str, Any]:
    mutated = _mutate_effects(candidates, variant)
    rows, commit = _run_candidate_commitment(mutated, f"{name}:{variant}")
    telemetry = dict(rows[0].get("relation_surface_telemetry", {}) or {}) if rows else {}
    assessments = {str(k): dict(v) for k, v in dict(commit.get("canonical_commitment_assessment", {}) or {}).items()}
    controls = dict(commit.get("direct_controls_used", {}) or {})
    selected = str(commit.get("action"))
    selected_ass = assessments.get(selected, {})
    blocked_actions = [a for a, ass in assessments.items() if _blocked(ass, controls)]
    resolver_actions = [a for a, ass in assessments.items() if float(ass.get("resolver_support", 0.0) or 0.0) >= 0.08]
    carrier_actions = [a for a, ass in assessments.items() if float(ass.get("carrier_only_pressure", 0.0) or 0.0) >= 0.08]
    return {
        "variant": variant,
        "action": commit.get("action"),
        "mode": commit.get("canonical_commitment_mode"),
        "reason": commit.get("canonical_commitment_reason"),
        "selected_blocked": bool(selected_ass and _blocked(selected_ass, controls)),
        "blocked_actions": blocked_actions,
        "resolver_actions": resolver_actions,
        "carrier_actions": carrier_actions,
        "certificate_aware_stable_continuation_applied": bool(commit.get("certificate_aware_stable_continuation_applied", False)),
        "certificate_aware_reopen_or_sample_applied": bool(commit.get("certificate_aware_reopen_or_sample_applied", False)),
        "relations_by_type": dict(telemetry.get("relations_by_type", {}) or {}),
        "relations_total": int(telemetry.get("relations_total", 0) or 0),
        "structural_relations": int(sum(int(v) for k, v in dict(telemetry.get("relations_by_type", {}) or {}).items() if k not in {"decision_slot_competition", "rivalry"})),
        "branch_internal_operation_rows": int(telemetry.get("branch_internal_operation_rows", 0) or 0),
        "rows_with_public_effects": int(telemetry.get("rows_with_public_effects", 0) or 0),
        "selected_assessment": _round_assessment(selected_ass),
    }


def _compare(full: Mapping[str, Any], other: Mapping[str, Any]) -> Dict[str, Any]:
    full_ass = dict(full.get("selected_assessment", {}) or {})
    other_ass = dict(other.get("selected_assessment", {}) or {})
    keys = sorted(set(full_ass) | set(other_ass))
    return {
        "action_changed": bool(full.get("action") != other.get("action")),
        "mode_changed": bool(full.get("mode") != other.get("mode")),
        "reason_changed": bool(full.get("reason") != other.get("reason")),
        "selected_blocked_changed": bool(full.get("selected_blocked") != other.get("selected_blocked")),
        "certificate_aware_reopen_changed": bool(full.get("certificate_aware_reopen_or_sample_applied") != other.get("certificate_aware_reopen_or_sample_applied")),
        "certificate_aware_stable_changed": bool(full.get("certificate_aware_stable_continuation_applied") != other.get("certificate_aware_stable_continuation_applied")),
        "relations_total_delta": int(full.get("relations_total", 0) or 0) - int(other.get("relations_total", 0) or 0),
        "structural_relations_delta": int(full.get("structural_relations", 0) or 0) - int(other.get("structural_relations", 0) or 0),
        "branch_internal_rows_delta": int(full.get("branch_internal_operation_rows", 0) or 0) - int(other.get("branch_internal_operation_rows", 0) or 0),
        "selected_assessment_delta": {k: round(float(full_ass.get(k, 0.0)) - float(other_ass.get(k, 0.0)), 6) for k in keys},
    }


def _all_inputs() -> List[Tuple[str, List[Dict[str, Any]], str]]:
    return _standard_cases() + _maintenance_sweep() + _latent_sweep()


def _summarize_cases(cases: List[Dict[str, Any]], variants: List[str]) -> Dict[str, Any]:
    by_source = Counter(str(c.get("source")) for c in cases)
    full_modes = Counter(str(c["variants_by_name"]["full"].get("mode")) for c in cases)
    full_actions = Counter(str(c["variants_by_name"]["full"].get("action")) for c in cases)
    comparisons_summary: Dict[str, Dict[str, Any]] = {}
    for variant in variants:
        if variant == "full":
            continue
        comps = [c["comparisons_vs_full"][variant] for c in cases]
        comparisons_summary[variant] = {
            "action_changes": sum(1 for x in comps if x["action_changed"]),
            "mode_changes": sum(1 for x in comps if x["mode_changed"]),
            "reason_changes": sum(1 for x in comps if x["reason_changed"]),
            "selected_blocked_changes": sum(1 for x in comps if x["selected_blocked_changed"]),
            "certificate_aware_reopen_changes": sum(1 for x in comps if x["certificate_aware_reopen_changed"]),
            "certificate_aware_stable_changes": sum(1 for x in comps if x["certificate_aware_stable_changed"]),
            "positive_structural_relation_delta_cases": sum(1 for x in comps if x["structural_relations_delta"] > 0),
            "positive_branch_internal_delta_cases": sum(1 for x in comps if x["branch_internal_rows_delta"] > 0),
        }
    return {
        "cases": len(cases),
        "sources": dict(sorted(by_source.items())),
        "full_modes": dict(sorted(full_modes.items())),
        "full_actions_top10": dict(full_actions.most_common(10)),
        "full_certificate_aware_reopen_cases": sum(1 for c in cases if c["variants_by_name"]["full"].get("certificate_aware_reopen_or_sample_applied")),
        "full_certificate_aware_stable_cases": sum(1 for c in cases if c["variants_by_name"]["full"].get("certificate_aware_stable_continuation_applied")),
        "comparisons_vs_full": comparisons_summary,
    }


def main() -> Dict[str, Any]:
    variants = [
        "full",
        "no_public_effects",
        "weak_competition_only",
        "no_weak_competition",
        "branch_internal_only_unique_scope",
        "no_resolver_ops",
        "carrier_only_no_resolver",
    ]
    cases: List[Dict[str, Any]] = []
    for name, candidates, source in _all_inputs():
        records = [_run_variant(name, list(candidates), variant) for variant in variants]
        by_name = {r["variant"]: r for r in records}
        comparisons = {variant: _compare(by_name["full"], by_name[variant]) for variant in variants if variant != "full"}
        cases.append({
            "name": name,
            "source": source,
            "variants": records,
            "variants_by_name": by_name,
            "comparisons_vs_full": comparisons,
        })
    summary = _summarize_cases(cases, variants)
    # Keep output reviewable: store all summaries but only detailed cases where
    # at least one ablation changes action/mode/certificate-aware behavior.
    notable = []
    for c in cases:
        if any(
            comp.get("action_changed")
            or comp.get("mode_changed")
            or comp.get("certificate_aware_reopen_changed")
            or comp.get("certificate_aware_stable_changed")
            for comp in c["comparisons_vs_full"].values()
        ):
            compact = {
                "name": c["name"],
                "source": c["source"],
                "full": c["variants_by_name"]["full"],
                "comparisons_vs_full": c["comparisons_vs_full"],
            }
            for v in variants:
                if v != "full" and (
                    c["comparisons_vs_full"][v].get("action_changed")
                    or c["comparisons_vs_full"][v].get("mode_changed")
                    or c["comparisons_vs_full"][v].get("certificate_aware_reopen_changed")
                    or c["comparisons_vs_full"][v].get("certificate_aware_stable_changed")
                ):
                    compact[v] = c["variants_by_name"][v]
            notable.append(compact)
    result = {
        "study": "real_adapter_structural_ablation_review_v1",
        "claim_boundary": "structural mechanism-causality review only; not reward evidence, novelty proof, or benchmark evidence",
        "summary": summary,
        "notable_cases": notable[:120],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    return result


if __name__ == "__main__":
    payload = main()
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "summary": payload["summary"]}, indent=2, sort_keys=True))
