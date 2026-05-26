from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SUMMARY = ROOT / "outputs" / "pass1_all_problem_stoa_comparison_v1" / "summary.json"
SHAPES = ROOT / "outputs" / "pass1_all_problem_stoa_comparison_v1" / "shape_reports.json"


def main() -> None:
    if not SUMMARY.exists():
        raise AssertionError("missing pass1 all-problem STOA comparison summary; run the study first")
    if not SHAPES.exists():
        raise AssertionError("missing shape reports")
    data = json.loads(SUMMARY.read_text(encoding="utf-8"))
    shape = json.loads(SHAPES.read_text(encoding="utf-8"))
    required_modes = {
        "bandit/easy_public_bandit",
        "renewal/noisy_renewal",
        "maze/static_visible_5x5",
        "latent_mechanism/easy_visible",
        "latent_mechanism/hidden_depth2",
        "maintenance_replacement/bandit_like",
        "maintenance_replacement/middle",
        "maintenance_replacement/renewal_like",
    }
    modes = set(data.get("modes", []))
    missing = required_modes - modes
    if missing:
        raise AssertionError(f"missing active problem modes from comparison: {sorted(missing)}")
    if int(data.get("shape_report_count", 0)) < len(required_modes):
        raise AssertionError("shape reports were not produced for all active modes")
    if len(shape.get("shape_reports", [])) < len(required_modes):
        raise AssertionError("shape report file too small")
    comparisons = dict(data.get("co_vs_best_baseline", {}))
    for mode in required_modes:
        if mode not in comparisons:
            raise AssertionError(f"missing CO-vs-best-baseline comparison for {mode}")
    if data.get("status") not in {"executed", "executed_with_errors", "executed_family_by_family_timeout_safe"}:
        raise AssertionError(f"unexpected status {data.get('status')}")
    if int(data.get("performance_rows", 0)) <= 0:
        raise AssertionError("no performance rows")
    print(json.dumps({"pass1_all_problem_stoa_comparison_invariants": "passed", "modes": sorted(modes), "status": data.get("status")}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
