from __future__ import annotations

"""Trace-level analysis for the first focused frozen maintenance benchmark.

This study reads the frozen benchmark outputs. It does not rerun, retune, or
modify CO constants. Its purpose is diagnostic: explain where CO diverges from
public baselines in maintenance/replacement and identify structural failure
hypotheses for the next probe.
"""

import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, pstdev
from typing import Any, Dict, Iterable, List, Mapping, Tuple

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "outputs" / "focused_frozen_empirical_mini_benchmark_v1"
RUNS_DIR = OUT_DIR / "runs"
ANALYSIS_DIR = ROOT / "outputs" / "focused_maintenance_failure_analysis_v1"
SUMMARY_JSON = ANALYSIS_DIR / "summary.json"
DETAILS_JSONL = ANALYSIS_DIR / "details.jsonl"
REPORT_MD = ROOT.parent / "FOCUSED_MAINTENANCE_FAILURE_ANALYSIS_2026-05-17.md"

MODES = ("bandit_like", "middle", "renewal_like")
SEEDS = (0, 1, 2)
ACTIONS = ("RUN", "INSPECT", "REPAIR", "REPLACE", "WAIT")


def _read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _write_jsonl(path: Path, rows: Iterable[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(dict(row), sort_keys=True) + "\n")


def _trace(mode: str, agent: str, seed: int) -> List[Dict[str, Any]]:
    return _read_jsonl(RUNS_DIR / f"maintenance_{mode}_{agent}_s{seed}" / "trace.jsonl")


def _total(rows: List[Mapping[str, Any]]) -> float:
    return float(sum(float(r.get("reward", 0.0)) for r in rows))


def _obs_key(r: Mapping[str, Any]) -> str:
    h = (r.get("obs") or {}).get("observed_health")
    return "unknown" if h is None else str(h)


def _mode_key(r: Mapping[str, Any]) -> str:
    sel = r.get("co_selection") or {}
    return str(sel.get("canonical_commitment_mode", ""))


def _ass(r: Mapping[str, Any], action: str) -> Dict[str, float]:
    sel = r.get("co_selection") or {}
    raw = ((sel.get("canonical_commitment_assessment") or {}).get(action) or {})
    out: Dict[str, float] = {}
    for k, v in raw.items():
        if isinstance(v, (int, float)):
            out[k] = float(v)
    return out


def _agent_summary(mode: str, agent: str) -> Dict[str, Any]:
    totals: List[float] = []
    action_counts: Counter[str] = Counter()
    event_counts: Counter[str] = Counter()
    failure_counts: List[int] = []
    obs_action: Dict[str, Counter[str]] = defaultdict(Counter)
    obs_mode: Dict[str, Counter[str]] = defaultdict(Counter)
    obs_action_rewards: Dict[Tuple[str, str], List[float]] = defaultdict(list)
    for seed in SEEDS:
        p = RUNS_DIR / f"maintenance_{mode}_{agent}_s{seed}" / "trace.jsonl"
        if not p.exists():
            continue
        rows = _read_jsonl(p)
        totals.append(_total(rows))
        failures = 0
        for r in rows:
            action = str(r.get("action"))
            event = str((r.get("info") or {}).get("last_event"))
            obs = _obs_key(r)
            action_counts[action] += 1
            event_counts[event] += 1
            failures += int("failure" in event)
            obs_action[obs][action] += 1
            obs_action_rewards[(obs, action)].append(float(r.get("reward", 0.0)))
            if agent == "co":
                obs_mode[obs][_mode_key(r)] += 1
        failure_counts.append(failures)
    return {
        "agent": agent,
        "mode": mode,
        "runs": len(totals),
        "mean_total_reward": mean(totals) if totals else None,
        "std_total_reward_population": pstdev(totals) if len(totals) > 1 else 0.0,
        "values": totals,
        "action_counts": dict(action_counts),
        "event_counts": dict(event_counts),
        "failure_counts_by_seed": failure_counts,
        "actions_by_observed_health": {k: dict(v) for k, v in sorted(obs_action.items())},
        "co_modes_by_observed_health": {k: dict(v) for k, v in sorted(obs_mode.items())},
        "mean_reward_by_observed_health_action": {
            f"{k[0]}::{k[1]}": mean(v) for k, v in sorted(obs_action_rewards.items())
        },
    }


def _middle_obs2_co_metrics() -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    for seed in SEEDS:
        for r in _trace("middle", "co", seed):
            if (r.get("obs") or {}).get("observed_health") == 2:
                rows.append(r)
    actions = ("RUN", "REPAIR", "INSPECT", "WAIT", "REPLACE")
    keys = (
        "support", "field_score", "burden", "carrier_only_pressure", "resolver_support",
        "dominance_score", "continuation_score", "sampling_score",
        "collapse_certificate_score", "certificate_gate_open",
        "certificate_blocks_dominance", "collapse_certificate_blocker_pressure",
        "collapse_certificate_recursion_demand",
    )
    metrics: Dict[str, Dict[str, float]] = {}
    for action in actions:
        vals: Dict[str, List[float]] = {k: [] for k in keys}
        for r in rows:
            ass = _ass(r, action)
            for k in keys:
                vals[k].append(float(ass.get(k, 0.0)))
        metrics[action] = {f"mean_{k}": mean(v) if v else 0.0 for k, v in vals.items()}
        metrics[action].update({f"min_{k}": min(v) if v else 0.0 for k, v in vals.items()})
        metrics[action].update({f"max_{k}": max(v) if v else 0.0 for k, v in vals.items()})
    return {
        "n_middle_co_observed_health_2_rows": len(rows),
        "selected_action_counts": dict(Counter(str(r.get("action")) for r in rows)),
        "commitment_mode_counts": dict(Counter(_mode_key(r) for r in rows)),
        "metrics_by_action": metrics,
    }


def _divergence_summary(mode: str, co_agent: str = "co", baseline_agent: str = "threshold") -> Dict[str, Any]:
    divergence_rows: List[Dict[str, Any]] = []
    total_divergent_steps = 0
    for seed in SEEDS:
        co = _trace(mode, co_agent, seed)
        base = _trace(mode, baseline_agent, seed)
        for t, (c, b) in enumerate(zip(co, base)):
            if c.get("action") != b.get("action"):
                total_divergent_steps += 1
                if len(divergence_rows) < 30:
                    divergence_rows.append({
                        "mode": mode,
                        "seed": seed,
                        "t": t,
                        "co_action": c.get("action"),
                        "baseline_action": b.get("action"),
                        "co_reward": c.get("reward"),
                        "baseline_reward": b.get("reward"),
                        "co_observed_health": (c.get("obs") or {}).get("observed_health"),
                        "baseline_observed_health": (b.get("obs") or {}).get("observed_health"),
                        "co_true_health_after": (c.get("info") or {}).get("health_true"),
                        "baseline_true_health_after": (b.get("info") or {}).get("health_true"),
                        "co_event": (c.get("info") or {}).get("last_event"),
                        "baseline_event": (b.get("info") or {}).get("last_event"),
                        "co_commitment_mode": _mode_key(c),
                        "co_commitment_reason": (c.get("co_selection") or {}).get("canonical_commitment_reason"),
                    })
    return {"mode": mode, "baseline_agent": baseline_agent, "total_divergent_steps": total_divergent_steps, "sample_divergences": divergence_rows}


def _make_report(summary: Mapping[str, Any]) -> str:
    middle = summary["agent_summaries"]["middle"]
    obs2 = summary["middle_observed_health_2_co_metrics"]
    co_mid = middle["co"]
    th_mid = middle["threshold"]
    ren = summary["agent_summaries"]["renewal_like"]
    return f"""# Focused Maintenance Failure Analysis — 2026-05-17

## Scope

This report analyzes the already-frozen `focused_frozen_empirical_mini_benchmark_v1` outputs. It does not retune constants, rerun policy search, or change the kernel. Its purpose is diagnostic: explain why CO underperformed in the `middle` maintenance regime and why the `renewal_like` result looked favorable against the simple public thresholds.

## Main finding

The `middle` loss is not primarily an inspection problem. CO never inspects in `middle`; the public threshold baseline also never inspects. The difference is repair timing:

```json
{json.dumps({
    'middle_co_mean': co_mid['mean_total_reward'],
    'middle_threshold_mean': th_mid['mean_total_reward'],
    'co_action_counts': co_mid['action_counts'],
    'threshold_action_counts': th_mid['action_counts'],
    'co_failure_counts_by_seed': co_mid['failure_counts_by_seed'],
    'threshold_failure_counts_by_seed': th_mid['failure_counts_by_seed'],
}, indent=2, sort_keys=True)}
```

The threshold baseline repairs whenever public observed health is `2` or lower. CO repairs mostly at observed health `0` or `1`, and continues `RUN` at observed health `2`:

```json
{json.dumps({
    'co_actions_by_observed_health': co_mid['actions_by_observed_health'],
    'threshold_actions_by_observed_health': th_mid['actions_by_observed_health'],
    'co_modes_by_observed_health': co_mid['co_modes_by_observed_health'],
}, indent=2, sort_keys=True)}
```

## Structural diagnosis of observed-health = 2

At observed health `2`, CO selects `RUN` in all sampled rows. Internally, `REPAIR` is recognized as a strong resolver (`resolver_support ≈ 0.50`), but `RUN` still wins because its local support/field score and dominance/continuation scores remain higher. `RUN` carries substantial branch-internal pressure, but that pressure is not currently enough to block dominance or force a resolver preference.

```json
{json.dumps(obs2, indent=2, sort_keys=True)}
```

In short:

```text
CO sees REPAIR as a resolver, but not as urgent enough at public health 2.
RUN is treated as a still-viable high-support continuation despite carrier-only pressure.
```

That is a formula/readout issue, not evidence that RelationSurface or resolver recognition is absent.

## Why renewal_like looked favorable

The `renewal_like` result is favorable only against simple public threshold baselines. CO avoids failures by repeatedly inspecting under hidden observation; the threshold baselines inspect only initially and then run into failure resets.

```json
{json.dumps({
    'renewal_like_co': ren['co'],
    'renewal_like_threshold': ren['threshold'],
}, indent=2, sort_keys=True)}
```

This is a positive structural signal for hiddenness/exposure sensitivity, but it is not a strong benchmark result. It may also indicate over-conservatism: CO earns safety mostly through very frequent inspection, not through a sophisticated repair/replacement cycle.

## Divergence samples

The first sample divergences against the public threshold baseline are stored in:

- `ChangeOntCode/outputs/focused_maintenance_failure_analysis_v1/details.jsonl`

## Current issue

The specific unresolved issue is:

```text
The current CommitmentSurface does not treat moderate carrier-only pressure at public health 2 as sufficient reason to prefer a strong resolver branch when RUN still has high support.
```

Possible explanations:

1. `carrier_only_pressure` is underweighted in dominance/collapse gating.
2. `collapse_blocked` thresholds are too high for mid-regime public health risk.
3. `resolver adequacy` is currently used mainly when a branch is already blocked, so it does not help enough when `RUN` is merely risky-but-not-blocked.
4. The six-question/direct-control projection for `middle` may be too collapse/local-support permissive.
5. The maintenance adapter may publish adequate resolver facts, but insufficient consequence-span / risk-of-delay facts.

## What not to conclude

Do not conclude that CO fails globally. Do not conclude that CO works. Do not tune thresholds directly to make `middle` match the public threshold baseline.

## Recommended next probe

Create a targeted mid-regime repair-timing microcase and real-trace counterfactual probe:

```text
public observed health = 2
RUN has high immediate support but carries degradation/failure pressure
REPAIR has lower immediate support but strong resolver support
vary failure penalty, degradation probability, observation noise, and horizon/consequence span
```

Expected purpose:

```text
Determine when CO should allow RUN-through-burden and when it should prefer REPAIR as an adequate resolver.
```

This is the right next probe because it targets the actual failure mechanism without performance tuning or family-specific policy insertion.
"""


def main() -> None:
    if not OUT_DIR.exists():
        raise RuntimeError(f"missing benchmark outputs: {OUT_DIR}")
    details: List[Dict[str, Any]] = []
    agent_summaries: Dict[str, Dict[str, Any]] = {}
    for mode in MODES:
        agent_summaries[mode] = {}
        for agent in ("co", "threshold", "threshold_opt", "finite_horizon_dp"):
            if any((RUNS_DIR / f"maintenance_{mode}_{agent}_s{s}" / "trace.jsonl").exists() for s in SEEDS):
                agent_summaries[mode][agent] = _agent_summary(mode, agent)
        details.append(_divergence_summary(mode, baseline_agent="threshold"))
    summary: Dict[str, Any] = {
        "study": "focused_maintenance_failure_analysis_v1",
        "source_outputs": str(OUT_DIR.relative_to(ROOT)),
        "claim_boundary": "Diagnostic trace analysis only; no retuning and no broad benchmark claim.",
        "agent_summaries": agent_summaries,
        "middle_observed_health_2_co_metrics": _middle_obs2_co_metrics(),
        "divergence_summaries": details,
        "conclusion": {
            "middle_loss_primary_mechanism": "CO repairs later than public threshold baseline; it runs at observed_health=2 where threshold repairs.",
            "renewal_like_gain_primary_mechanism": "CO repeatedly inspects under hiddenness and avoids failure resets suffered by threshold baselines.",
            "next_probe": "mid_regime_repair_timing_microcase_and_counterfactual_probe",
        },
    }
    _write_json(SUMMARY_JSON, summary)
    _write_jsonl(DETAILS_JSONL, details)
    REPORT_MD.write_text(_make_report(summary), encoding="utf-8")
    print(json.dumps({
        "study": summary["study"],
        "middle_co_mean": agent_summaries["middle"]["co"]["mean_total_reward"],
        "middle_threshold_mean": agent_summaries["middle"]["threshold"]["mean_total_reward"],
        "middle_co_actions": agent_summaries["middle"]["co"]["action_counts"],
        "middle_threshold_actions": agent_summaries["middle"]["threshold"]["action_counts"],
        "middle_co_obs2_actions": agent_summaries["middle"]["co"]["actions_by_observed_health"].get("2"),
        "renewal_co_actions": agent_summaries["renewal_like"]["co"]["action_counts"],
        "renewal_threshold_failures": agent_summaries["renewal_like"]["threshold"]["failure_counts_by_seed"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
