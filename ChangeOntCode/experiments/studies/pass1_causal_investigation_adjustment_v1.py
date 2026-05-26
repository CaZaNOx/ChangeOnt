from __future__ import annotations

"""Pass-1 causal investigation + generic adjustment audit.

This study records the first non-problem-specific adjustment made after the
all-problem STOA comparison/factor sweep: public problem-contract vocabulary
normalization for shape derivation.  It also guards against treating the factor
sweep as permission to tune readout or shapes from performance.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Mapping, List

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "pass1_causal_investigation_adjustment_v1.json"
REPORT = ROOT.parent / "PASS1_CAUSAL_INVESTIGATION_ADJUSTMENT_REPORT_2026-05-25.md"

from experiments.studies.pass1_factor_causal_sweep_v1 import _shape_reports
from agents.co.placement.shape_prior6 import derive_shape_prior6
from agents.co.core.contracts.problem_contract import normalize_problem_contract


def _json_safe(x: Any) -> Any:
    if isinstance(x, Mapping):
        return {str(k): _json_safe(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_json_safe(v) for v in x]
    if isinstance(x, (str, int, float, bool)) or x is None:
        return x
    return str(x)


def _read_json(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _legacy_contract(problem: Mapping[str, Any]) -> Dict[str, Any]:
    # Emulate the prior failure mode: drift=none and commitment_cost=medium_to_high
    # were not accepted vocabulary and collapsed to unknown before shape derivation.
    p = json.loads(json.dumps(problem))
    ts = p.get("timescale_profile", {}) if isinstance(p.get("timescale_profile"), Mapping) else {}
    rv = p.get("reversibility_profile", {}) if isinstance(p.get("reversibility_profile"), Mapping) else {}
    if ts.get("drift") == "none":
        ts["drift"] = "unknown"
    if rv.get("commitment_cost") == "medium_to_high":
        rv["commitment_cost"] = "unknown"
    return p


def _axis_delta(a: Mapping[str, float], b: Mapping[str, float]) -> Dict[str, float]:
    keys = sorted(set(a.keys()) | set(b.keys()))
    return {k: float(a.get(k, 0.0)) - float(b.get(k, 0.0)) for k in keys}


def build_summary() -> Dict[str, Any]:
    shape_payload = _shape_reports()
    reports = list(shape_payload.get("canonical_derived_shape_reports", []))
    affected: List[Dict[str, Any]] = []
    for r in reports:
        pc = r.get("problem_contract", {}) if isinstance(r.get("problem_contract"), Mapping) else {}
        new_shape = derive_shape_prior6(pc)
        old_shape = derive_shape_prior6(_legacy_contract(pc))
        d = _axis_delta(new_shape.get("axes", {}), old_shape.get("axes", {}))
        raw_d = _axis_delta(new_shape.get("raw_axes_before_quantization", {}), old_shape.get("raw_axes_before_quantization", {}))
        if any(abs(v) > 1e-9 for v in d.values()) or any(abs(v) > 1e-9 for v in raw_d.values()):
            affected.append({
                "family": r.get("family"),
                "mode": r.get("mode"),
                "contract_timescale": pc.get("timescale_profile", {}),
                "contract_reversibility": pc.get("reversibility_profile", {}),
                "legacy_axes": old_shape.get("axes", {}),
                "new_axes": new_shape.get("axes", {}),
                "axis_delta_new_minus_legacy": d,
                "raw_axis_delta_new_minus_legacy": raw_d,
            })

    factor_summary = _read_json(ROOT / "outputs" / "pass1_factor_causal_sweep_v1" / "summary.json") or {}
    comparison_summary = _read_json(ROOT / "outputs" / "pass1_all_problem_stoa_comparison_v1" / "summary.json") or {}
    payload = {
        "study": "pass1_causal_investigation_adjustment_v1",
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "adjustment_applied": {
            "kind": "public_contract_vocabulary_normalization",
            "files": [
                "ChangeOntCode/agents/co/core/contracts/_common.py",
                "ChangeOntCode/agents/co/core/contracts/problem_contract.py",
                "ChangeOntCode/agents/co/placement/shape_prior6.py",
            ],
            "details": [
                "drift uses a dedicated public drift vocabulary including 'none' instead of reusing horizon-fixity vocabulary",
                "commitment_cost accepts ordinal public categories low_to_medium and medium_to_high",
                "shape_prior6 maps drift=none to zero drift pressure and medium_to_high to elevated but non-maximal commitment pressure",
            ],
            "guardrails": [
                "no family names used in kernel shape code",
                "no action-name bonuses",
                "no hidden state, DP values, baseline values, or reward hindsight",
                "no canonical shape selected from performance results",
                "no readout coefficient tuning in this pass",
            ],
        },
        "affected_shape_reports": affected,
        "affected_shape_report_count": len(affected),
        "factor_sweep_rows_available_after_adjustment": factor_summary.get("rows"),
        "factor_sweep_comparisons_available_after_adjustment": factor_summary.get("comparisons", {}),
        "all_problem_comparison_rows_available_after_adjustment": comparison_summary.get("raw_rows"),
        "all_problem_comparison_available_after_adjustment": comparison_summary.get("co_vs_best_baseline", {}),
        "diagnosis": {
            "single_cause_found": False,
            "safe_generic_fix_found": True,
            "safe_generic_fix_scope": "public contract/shape vocabulary only",
            "performance_tuning_justified": False,
            "new_kernel_mechanism_justified": False,
            "main_remaining_causes": [
                "bandit: generic CO update/exploration is less efficient than posterior/UCB-style baselines",
                "renewal: compact phase/period structure is under-extracted compared with phase FSM",
                "maintenance: middle/renewal-like regimes still expose readout/gate timing and regime-placement issues over longer horizons",
                "latent: short capped runs remain inconclusive; shape vocabulary fix changes latent placement but does not establish performance",
            ],
        },
    }
    return payload


def write_report(summary: Mapping[str, Any]) -> None:
    lines = [
        "# Pass-1 Causal Investigation + Generic Adjustment — 2026-05-25",
        "",
        "## Claim boundary",
        "",
        "This is a causal investigation and one conservative generic adjustment. It is not a performance tuning pass, not a new CO mechanism, and not publication evidence.",
        "",
        "## Adjustment applied",
        "",
        "The public problem-contract vocabulary feeding shape derivation was too coarse. Legitimate public values such as `drift=none` and `commitment_cost=medium_to_high` were previously normalized to `unknown`, distorting shape before the kernel saw the problem.",
        "",
        "Files changed:",
        "",
    ]
    for f in summary.get("adjustment_applied", {}).get("files", []):
        lines.append(f"- `{f}`")
    lines += ["", "Guardrails:", ""]
    for g in summary.get("adjustment_applied", {}).get("guardrails", []):
        lines.append(f"- {g}")
    lines += ["", "## Affected shape reports", ""]
    affected = list(summary.get("affected_shape_reports", []))
    if not affected:
        lines.append("No canonical shape reports changed under the vocabulary correction.")
    else:
        for row in affected:
            lines.append(f"### {row.get('family')}/{row.get('mode')}")
            lines.append("")
            lines.append(f"- Legacy axes: `{row.get('legacy_axes')}`")
            lines.append(f"- New axes: `{row.get('new_axes')}`")
            lines.append(f"- Delta new-minus-legacy: `{row.get('axis_delta_new_minus_legacy')}`")
            lines.append("")
    lines += [
        "## Causal interpretation",
        "",
        "The factor sweep still does not support one universal non-problem-specific performance fix. Shape/readout variants change behavior in some families but do not close the gap to strong baselines. Therefore this pass deliberately did not tune readout coefficients or choose counterfactual shapes based on results.",
        "",
        "Remaining cause clusters:",
        "",
    ]
    for item in summary.get("diagnosis", {}).get("main_remaining_causes", []):
        lines.append(f"- {item}")
    lines += [
        "",
        "## Verdict",
        "",
        "A real generic bug was fixed: public regime vocabulary should not collapse to `unknown`. But the performance deficits remain multi-causal. The next safe investigation is not benchmark tuning; it is targeted, context-conditioned analysis of (1) bandit exploration/update cadence, (2) renewal phase extraction, and (3) maintenance longer-horizon gate/readout timing.",
        "",
        "## Full JSON",
        "",
        "```json",
        json.dumps(_json_safe(summary), indent=2, sort_keys=True),
        "```",
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> Dict[str, Any]:
    summary = build_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(_json_safe(summary), indent=2, sort_keys=True), encoding="utf-8")
    write_report(summary)
    print(json.dumps({"study": summary["study"], "affected_shape_report_count": summary["affected_shape_report_count"]}, indent=2, sort_keys=True))
    return dict(summary)


if __name__ == "__main__":
    main()
