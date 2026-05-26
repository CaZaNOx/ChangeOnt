from __future__ import annotations

"""Structural ablation probe v1.

This diagnostic is not a reward benchmark. It asks whether the current
public-effect path changes RCF/certificate/readout telemetry for structurally
separable reasons:

- full: original adapter public_effects;
- no_public_effects: removes all public_effects;
- weak_competition_only: keeps only procedural decision-slot facts;
- no_weak_competition: removes decision-slot facts, keeps burden/effect facts;
- branch_internal_only_unique_scope: keeps burden/effect facts but uniquifies
  burden/scope labels per candidate so cross-branch relations are suppressed.

The diagnostic is intentionally conservative. It records action/mode changes,
score deltas, relation counts, and certificate gate changes; it does not claim
performance or novelty.
"""

import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping

from agents.co.tests.relation_path_trace_diagnostics import _case_candidates, _run_candidate_commitment

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "structural_ablation_probe_v1.json"
DECISION_SLOT_OPS = {"decision_slot", "single_decision_slot"}


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
            expr = str(cand.get("candidate_id", cand.get("action", "candidate")))
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
        else:
            raise ValueError(f"unknown ablation variant: {variant}")
        out.append(cand)
    return out


def _round_assessment(assessment: Mapping[str, Any]) -> Dict[str, float]:
    keys = (
        "dominance_score",
        "sampling_score",
        "continuation_score",
        "collapse_certificate_blocker_pressure",
        "collapse_certificate_recursion_demand",
        "certificate_gate_open",
        "certificate_blocks_dominance",
        "collapse_blocked",
    )
    out: Dict[str, float] = {}
    for key in keys:
        try:
            out[key] = round(float(assessment.get(key, 0.0)), 6)
        except Exception:
            out[key] = 0.0
    return out


def _run_variant(family: str, candidates: List[Dict[str, Any]], variant: str) -> Dict[str, Any]:
    rows, commit = _run_candidate_commitment(_mutate_effects(candidates, variant), f"{family}:{variant}")
    telemetry = dict(rows[0].get("relation_surface_telemetry", {}) or {}) if rows else {}
    assessment = dict(commit.get("canonical_commitment_assessment", {}) or {})
    action = str(commit.get("action"))
    ranking = []
    for act, rec in assessment.items():
        ranking.append({"action": act, **_round_assessment(rec)})
    ranking.sort(key=lambda rec: rec.get("dominance_score", 0.0), reverse=True)
    return {
        "variant": variant,
        "action": commit.get("action"),
        "mode": commit.get("canonical_commitment_mode"),
        "reason": commit.get("canonical_commitment_reason"),
        "relations_by_type": dict(telemetry.get("relations_by_type", {}) or {}),
        "relations_total": int(telemetry.get("relations_total", 0) or 0),
        "branch_internal_operation_rows": int(telemetry.get("branch_internal_operation_rows", 0) or 0),
        "rows_with_public_effects": int(telemetry.get("rows_with_public_effects", 0) or 0),
        "selected_assessment": _round_assessment(assessment.get(action, {})),
        "dominance_ranking": ranking,
    }


def _delta(full: Mapping[str, Any], other: Mapping[str, Any]) -> Dict[str, Any]:
    keys = set(full.get("selected_assessment", {})) | set(other.get("selected_assessment", {}))
    return {
        "action_changed_vs_full": bool(full.get("action") != other.get("action")),
        "mode_changed_vs_full": bool(full.get("mode") != other.get("mode")),
        "selected_assessment_delta_vs_full": {
            k: round(float(full.get("selected_assessment", {}).get(k, 0.0)) - float(other.get("selected_assessment", {}).get(k, 0.0)), 6)
            for k in sorted(keys)
        },
    }


def main() -> Dict[str, Any]:
    variants = [
        "full",
        "no_public_effects",
        "weak_competition_only",
        "no_weak_competition",
        "branch_internal_only_unique_scope",
    ]
    cases = []
    aggregate = {
        "cases": 0,
        "full_vs_no_public_action_changes": 0,
        "full_vs_no_public_mode_changes": 0,
        "full_vs_weak_only_action_changes": 0,
        "full_vs_weak_only_mode_changes": 0,
        "weak_only_branch_internal_rows": 0,
    }
    for family, candidates in _case_candidates().items():
        records = [_run_variant(family, list(candidates), variant) for variant in variants]
        by_variant = {r["variant"]: r for r in records}
        full = by_variant["full"]
        comparisons = {v: _delta(full, by_variant[v]) for v in variants if v != "full"}
        aggregate["cases"] += 1
        aggregate["full_vs_no_public_action_changes"] += int(comparisons["no_public_effects"]["action_changed_vs_full"])
        aggregate["full_vs_no_public_mode_changes"] += int(comparisons["no_public_effects"]["mode_changed_vs_full"])
        aggregate["full_vs_weak_only_action_changes"] += int(comparisons["weak_competition_only"]["action_changed_vs_full"])
        aggregate["full_vs_weak_only_mode_changes"] += int(comparisons["weak_competition_only"]["mode_changed_vs_full"])
        aggregate["weak_only_branch_internal_rows"] += int(by_variant["weak_competition_only"].get("branch_internal_operation_rows", 0))
        cases.append({"family": family, "variants": records, "comparisons_vs_full": comparisons})
    result = {
        "study": "structural_ablation_probe_v1",
        "claim_boundary": "structural ablation only; not reward evidence and not novelty proof",
        "aggregate": aggregate,
        "cases": cases,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    return result


if __name__ == "__main__":
    data = main()
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "aggregate": data["aggregate"]}, indent=2, sort_keys=True))
