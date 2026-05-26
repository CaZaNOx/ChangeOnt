from __future__ import annotations

"""Mid-regime repair-timing probe v1.

This diagnostic isolates the issue found in the focused maintenance failure
analysis: in the middle maintenance regime, public observed health = 2 caused
CO to keep selecting RUN while the public threshold baseline repaired.  The
probe is structural, not a reward benchmark and not a tuning pass.

It asks whether the current runtime has a principled switch point from
RUN-through-carrier-burden to REPAIR-as-resolver when only public maintenance
facts change: degradation probability, failure penalty, repair cost, and
observation noise.  It also includes hand-built microcases that vary carrier
pressure and resolver adequacy directly.
"""

import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

from agents.co.adapters.maintenance_replacement_adapter import COAdapterMaintenanceReplacement
from agents.co.tests.relation_path_trace_diagnostics import DummyCore, _run_candidate_commitment
from experiments.studies.real_adapter_formula_sensitivity_probe_v1 import _run_candidate_commitment_with_params

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "mid_regime_repair_timing_probe_v1.json"
REPORT = ROOT.parent / "MID_REGIME_REPAIR_TIMING_PROBE_REPORT_2026-05-17.md"

DEGRADATIONS = [0.05, 0.10, 0.20, 0.30, 0.45, 0.60, 0.75]
FAILURE_PENALTIES = [2.0, 5.0, 8.0, 12.0]
REPAIR_COSTS = [0.40, 0.80, 1.20]
NOISES = [0.10, 0.40, 0.70]

CARRIER_MAGNITUDES = [0.20, 0.35, 0.50, 0.65, 0.80, 1.00]
RESOLVER_MAGNITUDES = [0.08, 0.12, 0.20, 0.35, 0.50, 0.75]
REPAIR_VISIBLES = [0.40, 0.48, 0.56, 0.64]

ASSESSMENT_KEYS = (
    "support",
    "field_score",
    "burden",
    "carrier_only_pressure",
    "resolver_support",
    "dominance_score",
    "continuation_score",
    "sampling_score",
    "collapse_blocked",
    "collapse_certificate_blocker_pressure",
    "collapse_certificate_recursion_demand",
    "certificate_gate_open",
    "certificate_blocks_dominance",
)


def _assessment(commit: Mapping[str, Any], action: str) -> Dict[str, float]:
    raw = dict(dict(commit.get("canonical_commitment_assessment", {}) or {}).get(action, {}) or {})
    out: Dict[str, float] = {}
    for key in ASSESSMENT_KEYS:
        try:
            out[key] = round(float(raw.get(key, 0.0) or 0.0), 6)
        except Exception:
            out[key] = 0.0
    return out


def _effect(operation: str, burden_type: str, magnitude: float, *, kind: str = "burden") -> Dict[str, Any]:
    return {
        "operation": operation,
        "kind": kind,
        "burden_type": burden_type,
        "scope": "candidate",
        "magnitude": float(magnitude),
        "relation_scope": burden_type,
        "public_basis": "visible_observation",
        "leakage_status": "public",
    }


def _candidate(candidate_id: str, visible: float, effects: Sequence[Mapping[str, Any]], *, uncertainty: float = 0.35) -> Dict[str, Any]:
    return {
        "candidate_id": candidate_id,
        "legal": True,
        "visible_delta": float(visible),
        "goal_relation": float(visible),
        "line_support": float(0.25 + 0.50 * visible),
        "support_depth": 0.62,
        "paired_depth": 0.62,
        "coverage_adequacy": float(max(0.05, 1.0 - uncertainty)),
        "tested_hint": 0.45,
        "uncertainty_hint": float(uncertainty),
        "reversibility_hint": 0.55,
        "continuity_support": float(max(0.05, 0.35 + 0.45 * visible)),
        "public_effects": [dict(e) for e in effects],
    }


def _commit_summary(commit: Mapping[str, Any]) -> Dict[str, Any]:
    selected = str(commit.get("action"))
    run = _assessment(commit, "RUN")
    repair = _assessment(commit, "REPAIR")
    return {
        "selected_action": selected,
        "selected_mode": commit.get("canonical_commitment_mode"),
        "selected_reason": commit.get("canonical_commitment_reason"),
        "certificate_aware_reopen_or_sample_applied": bool(commit.get("certificate_aware_reopen_or_sample_applied", False)),
        "certificate_aware_stable_continuation_applied": bool(commit.get("certificate_aware_stable_continuation_applied", False)),
        "required_resolver_support": round(float(commit.get("required_resolver_support", 0.0) or 0.0), 6),
        "run": run,
        "repair": repair,
        "run_minus_repair": {
            "support": round(run.get("support", 0.0) - repair.get("support", 0.0), 6),
            "dominance_score": round(run.get("dominance_score", 0.0) - repair.get("dominance_score", 0.0), 6),
            "continuation_score": round(run.get("continuation_score", 0.0) - repair.get("continuation_score", 0.0), 6),
            "sampling_score": round(run.get("sampling_score", 0.0) - repair.get("sampling_score", 0.0), 6),
        },
    }


def _adapter_case(degradation: float, failure_penalty: float, repair_cost: float, noise: float) -> Dict[str, Any]:
    obs = {
        "observed_health": 2,
        "max_health": 4,
        "health_observed": True,
        "degradation_prob_public": float(degradation),
        "wait_recovery_prob_public": 0.0,
        "repair_cost_public": float(repair_cost),
        "replace_cost_public": 2.0,
        "failure_penalty_public": float(failure_penalty),
        "observe_health_mode": "partial",
        "observation_noise_public": float(noise),
    }
    candidates = COAdapterMaintenanceReplacement(DummyCore())._derive(obs)["candidates"]
    rows, commit = _run_candidate_commitment(list(candidates), f"mid_repair_adapter:d{degradation}:p{failure_penalty}:c{repair_cost}:n{noise}")
    effects = {str(c.get("candidate_id")): list(c.get("public_effects", []) or []) for c in candidates}
    return {
        "case_type": "adapter_public_observation",
        "observed_health": 2,
        "degradation": float(degradation),
        "failure_penalty": float(failure_penalty),
        "repair_cost": float(repair_cost),
        "noise": float(noise),
        "run_effects": effects.get("RUN", []),
        "repair_effects": effects.get("REPAIR", []),
        "row_count": len(rows),
        **_commit_summary(commit),
    }


def _synthetic_case(carrier_mag: float, resolver_mag: float, repair_visible: float, *, run_visible: float = 0.70) -> Dict[str, Any]:
    candidates = [
        _candidate("RUN", run_visible, [_effect("carry", "degradation", carrier_mag)], uncertainty=0.35),
        _candidate("REPAIR", repair_visible, [_effect("reduce", "degradation", resolver_mag)], uncertainty=0.35),
        _candidate("INSPECT", 0.20, [_effect("reveal", "hiddenness", 0.10, kind="evidence")], uncertainty=0.35),
        _candidate("WAIT", 0.10, [_effect("carry", "degradation", 0.20)], uncertainty=0.35),
        _candidate("REPLACE", 0.25, [_effect("reset", "degradation", resolver_mag * 0.80)], uncertainty=0.35),
    ]
    _rows, commit = _run_candidate_commitment_with_params(
        list(candidates),
        f"mid_repair_synthetic:c{carrier_mag}:r{resolver_mag}:rv{repair_visible}",
        {},
    )
    out = {
        "case_type": "synthetic_pressure_matrix",
        "carrier_magnitude": float(carrier_mag),
        "resolver_magnitude": float(resolver_mag),
        "run_visible": float(run_visible),
        "repair_visible": float(repair_visible),
    }
    out.update(_commit_summary(commit))
    return out


def _aggregate_adapter(cases: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    actions = Counter(str(c.get("selected_action")) for c in cases)
    by_deg: Dict[str, Counter[str]] = defaultdict(Counter)
    by_penalty: Dict[str, Counter[str]] = defaultdict(Counter)
    by_cost: Dict[str, Counter[str]] = defaultdict(Counter)
    high_risk_run_cases: List[Mapping[str, Any]] = []
    for c in cases:
        by_deg[f"{float(c['degradation']):.2f}"][str(c.get("selected_action"))] += 1
        by_penalty[f"{float(c['failure_penalty']):.1f}"][str(c.get("selected_action"))] += 1
        by_cost[f"{float(c['repair_cost']):.2f}"][str(c.get("selected_action"))] += 1
        run = c.get("run", {}) or {}
        repair = c.get("repair", {}) or {}
        if (
            c.get("selected_action") == "RUN"
            and float(c.get("degradation", 0.0)) >= 0.30
            and float(c.get("failure_penalty", 0.0)) >= 8.0
            and float(run.get("carrier_only_pressure", 0.0)) >= 0.45
            and float(repair.get("resolver_support", 0.0)) >= 0.35
        ):
            high_risk_run_cases.append(c)
    return {
        "cases": len(cases),
        "selected_actions": dict(actions),
        "selected_actions_by_degradation": {k: dict(v) for k, v in sorted(by_deg.items())},
        "selected_actions_by_failure_penalty": {k: dict(v) for k, v in sorted(by_penalty.items())},
        "selected_actions_by_repair_cost": {k: dict(v) for k, v in sorted(by_cost.items())},
        "high_risk_run_case_count": len(high_risk_run_cases),
        "sample_high_risk_run_cases": [
            {
                "degradation": c["degradation"],
                "failure_penalty": c["failure_penalty"],
                "repair_cost": c["repair_cost"],
                "noise": c["noise"],
                "selected_action": c.get("selected_action"),
                "selected_mode": c.get("selected_mode"),
                "selected_reason": c.get("selected_reason"),
                "run": c.get("run"),
                "repair": c.get("repair"),
                "run_minus_repair": c.get("run_minus_repair"),
            }
            for c in high_risk_run_cases[:8]
        ],
    }


def _aggregate_synthetic(cases: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    by_carrier: Dict[str, Counter[str]] = defaultdict(Counter)
    first_repair_by_carrier_visible: Dict[str, float | None] = {}
    for c in cases:
        key = f"carrier={float(c['carrier_magnitude']):.2f};repair_visible={float(c['repair_visible']):.2f}"
        by_carrier[key][str(c.get("selected_action"))] += 1
    for carrier in CARRIER_MAGNITUDES:
        for repair_visible in REPAIR_VISIBLES:
            rows = [c for c in cases if abs(float(c["carrier_magnitude"]) - carrier) < 1e-9 and abs(float(c["repair_visible"]) - repair_visible) < 1e-9]
            selected = [float(c["resolver_magnitude"]) for c in rows if c.get("selected_action") == "REPAIR"]
            first_repair_by_carrier_visible[f"carrier={carrier:.2f};repair_visible={repair_visible:.2f}"] = min(selected) if selected else None
    pressure_without_repair = [
        c for c in cases
        if float(c["carrier_magnitude"]) >= 0.65
        and float(c["resolver_magnitude"]) >= 0.50
        and float(c["repair_visible"]) >= 0.56
        and c.get("selected_action") != "REPAIR"
    ]
    return {
        "cases": len(cases),
        "selected_actions": dict(Counter(str(c.get("selected_action")) for c in cases)),
        "selected_actions_by_carrier_and_repair_visible": {k: dict(v) for k, v in sorted(by_carrier.items())},
        "first_repair_resolver_magnitude_by_carrier_and_repair_visible": first_repair_by_carrier_visible,
        "strong_pressure_nonrepair_case_count": len(pressure_without_repair),
        "sample_strong_pressure_nonrepair_cases": [
            {
                "carrier_magnitude": c["carrier_magnitude"],
                "resolver_magnitude": c["resolver_magnitude"],
                "repair_visible": c["repair_visible"],
                "selected_action": c.get("selected_action"),
                "selected_mode": c.get("selected_mode"),
                "run": c.get("run"),
                "repair": c.get("repair"),
                "run_minus_repair": c.get("run_minus_repair"),
            }
            for c in pressure_without_repair[:8]
        ],
    }


def _make_report(result: Mapping[str, Any]) -> str:
    adapter = result["summary"]["adapter_sweep"]
    synth = result["summary"]["synthetic_pressure_matrix"]
    return f"""# Mid-Regime Repair-Timing Probe — 2026-05-17

## Scope

This probe follows the focused maintenance failure analysis. It does not tune the kernel and does not claim reward evidence. It asks a narrow structural question:

```text
When observed health is moderately degraded, when should CO continue RUN-through-carrier-burden and when should it prefer REPAIR as an adequate resolver?
```

Two probe families were run:

1. adapter-public observations at `observed_health = 2`, varying public degradation, public failure penalty, repair cost, and observation noise;
2. hand-built synthetic cases varying RUN carrier pressure, REPAIR resolver magnitude, and REPAIR local visible support.

## Adapter-public sweep summary

```json
{json.dumps(adapter, indent=2, sort_keys=True)}
```

## Synthetic pressure-matrix summary

```json
{json.dumps(synth, indent=2, sort_keys=True)}
```

## Interpretation

This probe now serves as a regression check for the generic shape-gauged resolver-timing law.  The earlier version exposed high-risk RUN-through-carrier-burden cases.  The current runtime no longer treats formal certificate blocking as the only way a resolver can matter: sufficiently urgent public shape plus carried burden plus an adequate resolver relation can bend commitment before blockage.

This is not a maintenance threshold rule.  The runtime does not read `observed_health <= 2` and does not prefer the native action name `REPAIR`.  It reads generic public structure:

```text
carrier-only pressure
resolver support
local problem-shape gauge
support/score gap
```

The synthetic matrix is retained to ensure the rule is not a universal resolver bonus: both RUN-through-burden and REPAIR-as-resolver choices must remain possible depending on pressure, adequacy, and gauge.

## Current watchpoint

```text
The shape-gauged timing constants are behavior-affecting provisional coefficients.
They are now documented formula-ledger items and must remain frozen for empirical tests.
```
"""


def main() -> Dict[str, Any]:
    adapter_cases: List[Dict[str, Any]] = []
    for d in DEGRADATIONS:
        for p in FAILURE_PENALTIES:
            for c in REPAIR_COSTS:
                for n in NOISES:
                    adapter_cases.append(_adapter_case(d, p, c, n))

    synthetic_cases: List[Dict[str, Any]] = []
    for carrier in CARRIER_MAGNITUDES:
        for resolver in RESOLVER_MAGNITUDES:
            for repair_visible in REPAIR_VISIBLES:
                synthetic_cases.append(_synthetic_case(carrier, resolver, repair_visible))

    adapter_summary = _aggregate_adapter(adapter_cases)
    synthetic_summary = _aggregate_synthetic(synthetic_cases)
    result: Dict[str, Any] = {
        "study": "mid_regime_repair_timing_probe_v1",
        "claim_boundary": "structural repair-timing diagnostic only; not reward evidence, not coefficient tuning, not CO proof",
        "summary": {
            "adapter_sweep": adapter_summary,
            "synthetic_pressure_matrix": synthetic_summary,
            "watchpoint": "shape-gauged pre-blocking resolver timing is active; constants remain provisional",
            "next_question": "whether the shape-gauged timing law remains structurally sane across real-family traces and frozen empirical tests",
        },
        "adapter_cases": adapter_cases,
        "synthetic_cases": synthetic_cases,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    REPORT.write_text(_make_report(result), encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(main()["summary"], indent=2, sort_keys=True))
