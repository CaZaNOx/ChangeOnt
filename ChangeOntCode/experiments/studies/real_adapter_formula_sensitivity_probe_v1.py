from __future__ import annotations

"""Real-adapter formula/coefficient sensitivity probe v1.

This diagnostic is part of the formula-ledger integrity gate, not performance
optimization. It perturbs the behavior-affecting CommitmentSurface coefficients
introduced by certificate-aware stable continuation and resolver-aware
reopen/sample selection, then measures how many real-adapter trace decisions
change relative to the certified defaults.

The goal is to classify coefficients as currently stable, sensitive, or brittle
so they can be grounded or demoted honestly before empirical reward claims.
"""

import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Tuple

from agents.co.runtime.surfaces.candidate_surface import CandidateEvidenceSurface
from agents.co.runtime.surfaces.commitment_surface import CommitmentSurface
from agents.co.tests.relation_path_trace_diagnostics import TraceBus, TraceHeader, TraceHeaderState
from experiments.studies.real_adapter_certificate_gating_review_v1 import (
    _latent_sweep,
    _maintenance_sweep,
    _standard_cases,
)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "real_adapter_formula_sensitivity_probe_v1.json"

BASELINE_PARAMS: Dict[str, float] = {}

PARAM_PROFILES: Dict[str, Dict[str, float]] = {
    "baseline": BASELINE_PARAMS,
    # Narrow comparability: blocked branches need only a small lead to keep
    # selection.  If many decisions change against baseline, the current gate is
    # highly dependent on permissive unblocked-alternative preference.
    "strict_comparability_narrow_margins": {
        "continuation_gate_margin_floor": 0.02,
        "continuation_gate_margin_cap": 0.09,
        "continuation_gate_margin_base": 0.025,
        "support_advantage_limit_floor": 0.07,
        "support_advantage_limit_cap": 0.17,
        "support_advantage_limit_base": 0.09,
        "sampling_gate_margin_floor": 0.03,
        "sampling_gate_margin_cap": 0.11,
        "sampling_gate_margin_base": 0.035,
        "sampling_support_advantage_floor": 0.06,
        "sampling_support_advantage_cap": 0.18,
        "sampling_support_advantage_base": 0.08,
    },
    # Wide comparability: unblocked/resolver alternatives may replace blocked
    # branches across wider support gaps.  Large changes here warn that the
    # gate could become a hidden conservative policy if left ungrounded.
    "permissive_comparability_wide_margins": {
        "continuation_gate_margin_floor": 0.08,
        "continuation_gate_margin_cap": 0.24,
        "continuation_gate_margin_base": 0.075,
        "support_advantage_limit_floor": 0.18,
        "support_advantage_limit_cap": 0.40,
        "support_advantage_limit_base": 0.23,
        "sampling_gate_margin_floor": 0.09,
        "sampling_gate_margin_cap": 0.27,
        "sampling_gate_margin_base": 0.090,
        "sampling_support_advantage_floor": 0.18,
        "sampling_support_advantage_cap": 0.42,
        "sampling_support_advantage_base": 0.22,
    },
    # Treat weaker branch-internal reducer/exposer facts as resolver candidates.
    "low_resolver_threshold": {
        "resolver_support_threshold": 0.04,
    },
    # Require stronger resolver facts before a branch can displace a blocked
    # carrier-only selection.
    "high_resolver_threshold": {
        "resolver_support_threshold": 0.14,
    },

    # Disable the comparable-alternative gates by forcing zero margins. This is
    # a falsification control: many changes here mean the certificate-aware
    # rules are behavior-causal rather than decorative.
    "zero_comparability_margins": {
        "continuation_gate_margin_floor": 0.0,
        "continuation_gate_margin_cap": 0.0,
        "continuation_gate_margin_base": 0.0,
        "support_advantage_limit_floor": 0.0,
        "support_advantage_limit_cap": 0.0,
        "support_advantage_limit_base": 0.0,
        "sampling_gate_margin_floor": 0.0,
        "sampling_gate_margin_cap": 0.0,
        "sampling_gate_margin_base": 0.0,
        "sampling_support_advantage_floor": 0.0,
        "sampling_support_advantage_cap": 0.0,
        "sampling_support_advantage_base": 0.0,
    },

    # Remove burden-scaled adequacy and use the base resolver floor only.
    # If this changes many cases, the scaled adequacy law is behavior-causal.
    "resolver_adequacy_unscaled_floor_only": {
        "resolver_support_carrier_weight": 0.0,
        "resolver_support_blocker_weight": 0.0,
        "resolver_support_scaled_base": 0.08,
    },
    # Require stronger resolver adequacy relative to carrier/blocker pressure.
    # Large action changes here would warn that resolver adequacy is a brittle
    # hidden policy knob rather than a stable structural guard.
    "strict_resolver_adequacy_scaling": {
        "resolver_support_carrier_weight": 0.24,
        "resolver_support_blocker_weight": 0.08,
        "resolver_support_scaled_cap": 0.50,
    },
    # Make resolver recognition nearly impossible. This tests whether the
    # resolver threshold is structurally active in the real sweep.
    "resolver_threshold_nearly_disabled": {
        "resolver_support_threshold": 0.95,
    },
    # Remove adaptive widening from blocker pressure.  If this matches baseline
    # closely, the current blocker-pressure terms may be nonessential in these
    # cases; if not, they are behavior-critical and need stronger grounding.
    "flat_blocker_terms": {
        "continuation_gate_margin_blocker_weight": 0.0,
        "support_advantage_limit_blocker_weight": 0.0,
        "sampling_gate_margin_blocker_weight": 0.0,
        "sampling_support_advantage_blocker_weight": 0.0,
    },
}


def _obs_from_candidates(candidates: List[Dict[str, Any]], family: str) -> Dict[str, Any]:
    actions = [c.get("candidate_id") for c in candidates if c.get("candidate_id") is not None and bool(c.get("legal", True))]
    return {
        "family": family,
        "t": 5,
        "action_space": actions,
        "problem_contract": {
            "task_anchor": {"kind": "formula_sensitivity_probe", "provided_externally": True},
            "actions": {"count": len(actions), "native_type": "adapter_candidates"},
            "observability_profile": {"state": "public_trace", "constraints": "public_trace"},
        },
        "candidates": candidates,
    }


def _run_candidate_commitment_with_params(
    candidates: List[Dict[str, Any]],
    family: str,
    params: Mapping[str, float],
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    obs = _obs_from_candidates(candidates, family)
    bus = TraceBus()
    prims: Dict[str, Any] = {"signal_bus": bus}
    header = TraceHeader(TraceHeaderState())
    CandidateEvidenceSurface().step(obs, prims, header, None)
    rows = [dict(r) for r in prims.get("__candidate_publication_rows__", [])]
    out = CommitmentSurface(collapse_enabled=False, commitment_formula_params=dict(params)).step(obs, prims, header, None)
    return rows, dict(out or {})


def _all_inputs() -> List[Tuple[str, List[Dict[str, Any]], str]]:
    return _standard_cases() + _maintenance_sweep() + _latent_sweep()


def _selected_assessment(commit: Mapping[str, Any]) -> Dict[str, float]:
    action = str(commit.get("action"))
    ass = dict(dict(commit.get("canonical_commitment_assessment", {}) or {}).get(action, {}) or {})
    out: Dict[str, float] = {}
    for key in (
        "support",
        "burden",
        "dominance_score",
        "sampling_score",
        "continuation_score",
        "resolver_support",
        "carrier_only_pressure",
        "collapse_blocked",
        "certificate_gate_open",
        "certificate_blocks_dominance",
    ):
        try:
            out[key] = round(float(ass.get(key, 0.0) or 0.0), 6)
        except Exception:
            out[key] = 0.0
    return out


def _commit_record(name: str, source: str, profile: str, commit: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "name": name,
        "source": source,
        "profile": profile,
        "action": commit.get("action"),
        "mode": commit.get("canonical_commitment_mode"),
        "reason": commit.get("canonical_commitment_reason"),
        "certificate_aware_reopen_or_sample_applied": bool(commit.get("certificate_aware_reopen_or_sample_applied", False)),
        "certificate_aware_stable_continuation_applied": bool(commit.get("certificate_aware_stable_continuation_applied", False)),
        "sampling_gate_margin": round(float(commit.get("sampling_gate_margin", 0.0) or 0.0), 6),
        "sampling_support_advantage_limit": round(float(commit.get("sampling_support_advantage_limit", 0.0) or 0.0), 6),
        "continuation_gate_margin": round(float(commit.get("continuation_gate_margin", 0.0) or 0.0), 6),
        "support_advantage_limit": round(float(commit.get("support_advantage_limit", 0.0) or 0.0), 6),
        "required_resolver_support": round(float(commit.get("required_resolver_support", 0.0) or 0.0), 6),
        "selected_assessment": _selected_assessment(commit),
    }


def main() -> Dict[str, Any]:
    cases: List[Dict[str, Any]] = []
    for name, candidates, source in _all_inputs():
        profile_records: Dict[str, Dict[str, Any]] = {}
        for profile, params in PARAM_PROFILES.items():
            _rows, commit = _run_candidate_commitment_with_params(list(candidates), f"{name}:{profile}", params)
            profile_records[profile] = _commit_record(name, source, profile, commit)
        baseline = profile_records["baseline"]
        comparisons: Dict[str, Dict[str, Any]] = {}
        for profile, record in profile_records.items():
            if profile == "baseline":
                continue
            comparisons[profile] = {
                "action_changed": bool(record["action"] != baseline["action"]),
                "mode_changed": bool(record["mode"] != baseline["mode"]),
                "reason_changed": bool(record["reason"] != baseline["reason"]),
                "certificate_aware_reopen_changed": bool(record["certificate_aware_reopen_or_sample_applied"] != baseline["certificate_aware_reopen_or_sample_applied"]),
                "certificate_aware_stable_changed": bool(record["certificate_aware_stable_continuation_applied"] != baseline["certificate_aware_stable_continuation_applied"]),
            }
        cases.append({
            "name": name,
            "source": source,
            "profiles": profile_records,
            "comparisons_vs_baseline": comparisons,
        })

    by_source = Counter(str(c["source"]) for c in cases)
    profile_summary: Dict[str, Dict[str, Any]] = {}
    for profile in PARAM_PROFILES:
        records = [c["profiles"][profile] for c in cases]
        if profile == "baseline":
            profile_summary[profile] = {
                "actions": dict(Counter(str(r["action"]) for r in records).most_common(10)),
                "modes": dict(Counter(str(r["mode"]) for r in records)),
                "certificate_aware_reopen_cases": sum(1 for r in records if r["certificate_aware_reopen_or_sample_applied"]),
                "certificate_aware_stable_cases": sum(1 for r in records if r["certificate_aware_stable_continuation_applied"]),
            }
        else:
            comps = [c["comparisons_vs_baseline"][profile] for c in cases]
            profile_summary[profile] = {
                "action_changes": sum(1 for x in comps if x["action_changed"]),
                "mode_changes": sum(1 for x in comps if x["mode_changed"]),
                "reason_changes": sum(1 for x in comps if x["reason_changed"]),
                "certificate_aware_reopen_changes": sum(1 for x in comps if x["certificate_aware_reopen_changed"]),
                "certificate_aware_stable_changes": sum(1 for x in comps if x["certificate_aware_stable_changed"]),
                "actions": dict(Counter(str(r["action"]) for r in records).most_common(10)),
                "modes": dict(Counter(str(r["mode"]) for r in records)),
            }

    notable: List[Dict[str, Any]] = []
    for c in cases:
        if any(any(v for v in comp.values()) for comp in c["comparisons_vs_baseline"].values()):
            notable.append(c)

    result = {
        "study": "real_adapter_formula_sensitivity_probe_v1",
        "claim_boundary": "coefficient/formula sensitivity only; not tuning, reward evidence, novelty proof, or benchmark evidence",
        "parameter_profiles": PARAM_PROFILES,
        "summary": {
            "cases": len(cases),
            "sources": dict(sorted(by_source.items())),
            "profiles": profile_summary,
            "notable_case_count": len(notable),
        },
        "notable_cases": notable[:120],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    return result


if __name__ == "__main__":
    payload = main()
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "summary": payload["summary"]}, indent=2, sort_keys=True))
