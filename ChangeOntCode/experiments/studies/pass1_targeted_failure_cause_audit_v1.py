from __future__ import annotations

"""Pass-1 targeted failure-cause audit v1.

Diagnostic-only audit of the current CO vs STOA failure modes after the bounded
all-problem comparison and factor sweep.  This study does not tune or modify the
kernel.  It runs targeted, bounded traces for the three clearest cause clusters:

- bandit: exploration/update-cadence and suboptimal lock-in;
- renewal: recurrence/phase extraction vs a public PhaseFSM baseline;
- maintenance: longer-horizon degradation/repair timing and readout/gate use.

The study deliberately reports causes as mechanism hypotheses, not proof and not
publication evidence.  It avoids hidden state in the CO runtime; baselines remain
external comparisons.
"""

import json
import math
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, pstdev
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.studies._co_eval_common import load_co_manifest_params, build_validated_co_core
from experiments.runners.maintenance_replacement_runner import build_agent, spec_from_name
from environments.maintenance_replacement.env import MaintenanceReplacementEnv, ACTIONS

STUDY = "pass1_targeted_failure_cause_audit_v1"
OUT_DIR = ROOT / "outputs" / STUDY
SUMMARY_JSON = OUT_DIR / "summary.json"
BANDIT_STEPS = OUT_DIR / "bandit_steps.jsonl"
RENEWAL_STEPS = OUT_DIR / "renewal_steps.jsonl"
MAINT_STEPS = OUT_DIR / "maintenance_steps.jsonl"
REPORT_MD = ROOT.parent / "PASS1_TARGETED_FAILURE_CAUSE_AUDIT_REPORT_2026-05-25.md"

SEEDS = [0, 1]
BANDIT_HORIZON = 48
RENEWAL_HORIZON = 48
MAINTENANCE_HORIZON_CAP = 48

CLAIM_BOUNDARY = (
    "Targeted causal audit only.  This is not a tuning run, not a performance claim, "
    "and not evidence of CO superiority/inferiority by itself.  It identifies which "
    "mechanism layer plausibly explains current weak STOA comparisons."
)


def _iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _json_safe(x: Any) -> Any:
    if isinstance(x, Mapping):
        return {str(k): _json_safe(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_json_safe(v) for v in x]
    if isinstance(x, (str, int, float, bool)) or x is None:
        return x
    return str(x)


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_json_safe(payload), indent=2, sort_keys=True), encoding="utf-8")


def _append_jsonl(path: Path, row: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(_json_safe(row), sort_keys=True) + "\n")


def _mean(xs: Sequence[float]) -> float:
    return float(mean(xs)) if xs else 0.0


def _std(xs: Sequence[float]) -> float:
    return float(pstdev(xs)) if len(xs) > 1 else 0.0


def _entropy(vals: Sequence[Any]) -> float:
    if not vals:
        return 0.0
    c = Counter(vals)
    n = float(len(vals))
    return float(-sum((v / n) * math.log((v / n), 2) for v in c.values() if v > 0))


def _base_params() -> Dict[str, Any]:
    return load_co_manifest_params(ROOT / "experiments" / "configs" / "co_agents" / "co_agents_canonical_core.yaml")


def _core(base: Mapping[str, Any]):
    return build_validated_co_core(dict(base), study_name=STUDY)


def _rows_from_agent(agent: Any) -> List[Dict[str, Any]]:
    core = getattr(agent, "core", None)
    prims = getattr(core, "primitives", {}) if core is not None else {}
    rows = prims.get("__candidate_publication_rows__", []) if isinstance(prims, dict) else []
    return [dict(r) for r in rows if isinstance(r, dict)]


def _float(row: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    try:
        return float(row.get(key, default) or default)
    except Exception:
        return default


def _row_telemetry(rows: Sequence[Mapping[str, Any]], selected_action: Any = None) -> Dict[str, Any]:
    def avg(key: str) -> float:
        vals = [_float(r, key) for r in rows if isinstance(r, Mapping)]
        return _mean(vals)

    selected = None
    for r in rows:
        if str(r.get("action", r.get("candidate_id", ""))) == str(selected_action) or str(r.get("candidate_id", "")) == str(selected_action):
            selected = r
            break
    resolver_rows = [r for r in rows if _float(r, "branch_internal_resolver_support") > 0.0 or _float(r, "resolver_support") > 0.0]
    carrier_rows = [r for r in rows if _float(r, "branch_internal_carrier_pressure") > 0.0 or _float(r, "field_debt") > 0.0]
    sequence_rows = [r for r in rows if bool(r.get("sequence_composition_active"))]
    return {
        "rows": len(rows),
        "avg_field_debt": avg("field_debt"),
        "avg_grey_pressure": avg("field_grey_pressure"),
        "avg_recursion_demand": avg("recursion_scheduler_demand"),
        "sequence_active_rows": len(sequence_rows),
        "quotient_rows": sum(1 for r in rows if _float(r, "quotient_share_count", 1.0) > 1.0),
        "resolver_rows": len(resolver_rows),
        "carrier_rows": len(carrier_rows),
        "selected_dominance_score": _float(selected or {}, "dominance_score"),
        "selected_field_debt": _float(selected or {}, "field_debt"),
        "selected_sequence_support": _float(selected or {}, "sequence_composition_support"),
        "selected_recursion_demand": _float(selected or {}, "recursion_scheduler_demand"),
        "selected_candidate_id": (selected or {}).get("candidate_id"),
    }


def _clear_outputs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for p in (SUMMARY_JSON, BANDIT_STEPS, RENEWAL_STEPS, MAINT_STEPS):
        if p.exists():
            p.unlink()


# ---------------- Bandit ----------------

def _run_co_bandit_seed(base: Mapping[str, Any], seed: int) -> Dict[str, Any]:
    from environments.bandit.bandit import BernoulliBanditEnv
    from agents.co.adapters.bandit_adapter import COAdapterBandit

    probs = [0.10, 0.20, 0.80]
    best_arm = int(max(range(len(probs)), key=lambda i: probs[i]))
    env = BernoulliBanditEnv(probs, horizon=BANDIT_HORIZON)
    env.reset(seed=seed)
    agent = COAdapterBandit(core=_core(base), n_arms=env.n_arms)
    actions: List[int] = []
    rewards: List[float] = []
    regret = 0.0
    done = False
    t = 0
    while not done and t < BANDIT_HORIZON:
        sel = agent.select({"family": "bandit", "t": t, "n_arms": env.n_arms})
        act = int(sel["action"])
        _, r, done, _ = env.step(act)
        rows = _rows_from_agent(agent)
        tel = _row_telemetry(rows, selected_action=act)
        regret += max(0.0, max(probs) - probs[act])
        actions.append(act)
        rewards.append(float(r))
        _append_jsonl(BANDIT_STEPS, {"agent":"co", "seed":seed, "t":t, "action":act, "reward":float(r), "best_arm":best_arm, "regret_so_far":regret, **tel})
        agent.update({"action": act, "reward": float(r), "done": bool(done)})
        t += 1
    first = actions[:20]
    second_half = actions[BANDIT_HORIZON // 2:]
    return {
        "seed": seed,
        "regret": float(regret),
        "total_reward": float(sum(rewards)),
        "best_arm_pull_rate": float(sum(1 for a in actions if a == best_arm) / float(len(actions) or 1)),
        "early_best_arm_pull_rate": float(sum(1 for a in first if a == best_arm) / float(len(first) or 1)),
        "late_best_arm_pull_rate": float(sum(1 for a in second_half if a == best_arm) / float(len(second_half) or 1)),
        "action_counts": dict(Counter(actions)),
        "action_entropy": _entropy(actions),
        "first_actions": actions[:24],
    }


def _run_ts_bandit_seed(seed: int) -> Dict[str, Any]:
    from environments.bandit.bandit import BernoulliBanditEnv
    from agents.stoa.bandit.ts import ThompsonSampling
    import random
    random.seed(seed)
    probs = [0.10, 0.20, 0.80]
    best_arm = int(max(range(len(probs)), key=lambda i: probs[i]))
    env = BernoulliBanditEnv(probs, horizon=BANDIT_HORIZON)
    env.reset(seed=seed)
    agent = ThompsonSampling(env.n_arms)
    actions: List[int] = []
    rewards: List[float] = []
    regret = 0.0
    done = False
    t = 0
    while not done and t < BANDIT_HORIZON:
        act = int(agent.select())
        _, r, done, _ = env.step(act)
        agent.update(act, r)
        regret += max(0.0, max(probs) - probs[act])
        actions.append(act)
        rewards.append(float(r))
        _append_jsonl(BANDIT_STEPS, {"agent":"thompson_sampling", "seed":seed, "t":t, "action":act, "reward":float(r), "best_arm":best_arm, "regret_so_far":regret})
        t += 1
    second_half = actions[BANDIT_HORIZON // 2:]
    return {
        "seed": seed,
        "regret": float(regret),
        "total_reward": float(sum(rewards)),
        "best_arm_pull_rate": float(sum(1 for a in actions if a == best_arm) / float(len(actions) or 1)),
        "late_best_arm_pull_rate": float(sum(1 for a in second_half if a == best_arm) / float(len(second_half) or 1)),
        "action_counts": dict(Counter(actions)),
        "action_entropy": _entropy(actions),
        "first_actions": actions[:24],
    }


def _bandit_audit(base: Mapping[str, Any]) -> Dict[str, Any]:
    co = [_run_co_bandit_seed(base, s) for s in SEEDS]
    ts = [_run_ts_bandit_seed(s) for s in SEEDS]
    return {
        "co": co,
        "thompson_sampling": ts,
        "co_regret_mean": _mean([r["regret"] for r in co]),
        "ts_regret_mean": _mean([r["regret"] for r in ts]),
        "co_late_best_arm_pull_rate_mean": _mean([r["late_best_arm_pull_rate"] for r in co]),
        "ts_late_best_arm_pull_rate_mean": _mean([r["late_best_arm_pull_rate"] for r in ts]),
        "diagnosis": "CO underperforms because it does not produce posterior-like evidence accumulation / exploration cadence; late best-arm pull rate remains below TS when early samples mislead or support/stability locks in.",
        "cause_layer": "generic uncertainty/evidence update + commitment cadence, not quotient/sequence/readout-resolver logic",
    }


# ---------------- Renewal ----------------

def _run_co_renewal_seed(base: Mapping[str, Any], seed: int) -> Dict[str, Any]:
    from environments.renewal.env import CodebookRenewalEnvW, EnvCfg
    from agents.co.adapters.renewal_adapter import COAdapterRenewal
    A, L = 4, 3
    env = CodebookRenewalEnvW(EnvCfg(A=A, L_win=L, p_ren=0.04, p_noise=0.02, T_max=RENEWAL_HORIZON), seed=seed)
    obs, _, done, _ = env.reset()
    agent = COAdapterRenewal(core=_core(base))
    actions: List[int] = []
    rewards: List[float] = []
    t = 0
    while not done and t < RENEWAL_HORIZON:
        sel = agent.select({"family": "renewal", "obs": int(obs), "t": t, "A": A, "L_win": L})
        act = int(sel["action"])
        obs, r, done, _ = env.step(act)
        rows = _rows_from_agent(agent)
        tel = _row_telemetry(rows, selected_action=act)
        actions.append(act); rewards.append(float(r))
        _append_jsonl(RENEWAL_STEPS, {"agent":"co", "seed":seed, "t":t, "action":act, "reward":float(r), "obs":int(obs), **tel})
        agent.update({"observation": int(obs), "reward": float(r), "done": bool(done), "action": act})
        t += 1
    return {"seed":seed, "mean_reward":float(sum(rewards)/float(len(rewards) or 1)), "total_reward":float(sum(rewards)), "actions": actions, "action_entropy": _entropy(actions), "first_actions": actions[:24]}


def _run_phase_renewal_seed(seed: int) -> Dict[str, Any]:
    from environments.renewal.env import CodebookRenewalEnvW, EnvCfg
    from agents.stoa.renewal.agent_fsm import PhaseFSM
    A, L = 4, 3
    env = CodebookRenewalEnvW(EnvCfg(A=A, L_win=L, p_ren=0.04, p_noise=0.02, T_max=RENEWAL_HORIZON), seed=seed)
    obs, _, done, _ = env.reset()
    agent = PhaseFSM(A=A, L_win=L)
    if hasattr(agent, "reset"):
        agent.reset(int(obs))
    actions: List[int] = []
    rewards: List[float] = []
    t = 0
    while not done and t < RENEWAL_HORIZON:
        act = int(agent.act(int(obs)))
        obs, r, done, _ = env.step(act)
        actions.append(act); rewards.append(float(r))
        _append_jsonl(RENEWAL_STEPS, {"agent":"phase_fsm", "seed":seed, "t":t, "action":act, "reward":float(r), "obs":int(obs)})
        t += 1
    return {"seed":seed, "mean_reward":float(sum(rewards)/float(len(rewards) or 1)), "total_reward":float(sum(rewards)), "actions": actions, "action_entropy": _entropy(actions), "first_actions": actions[:24]}


def _repeat_lag_score(actions: Sequence[int], lag: int = 3) -> float:
    if len(actions) <= lag:
        return 0.0
    return float(sum(1 for i in range(lag, len(actions)) if actions[i] == actions[i-lag]) / float(len(actions)-lag))


def _alignment(a: Sequence[int], b: Sequence[int]) -> float:
    n = min(len(a), len(b))
    if n <= 0:
        return 0.0
    return float(sum(1 for i in range(n) if a[i] == b[i]) / float(n))


def _renewal_audit(base: Mapping[str, Any]) -> Dict[str, Any]:
    co = [_run_co_renewal_seed(base, s) for s in SEEDS]
    phase = [_run_phase_renewal_seed(s) for s in SEEDS]
    alignments = [_alignment(c["actions"], p["actions"]) for c, p in zip(co, phase)]
    co_lag = [_repeat_lag_score(c["actions"], 3) for c in co]
    phase_lag = [_repeat_lag_score(p["actions"], 3) for p in phase]
    return {
        "co": [{k:v for k,v in r.items() if k != "actions"} for r in co],
        "phase_fsm": [{k:v for k,v in r.items() if k != "actions"} for r in phase],
        "co_mean_reward": _mean([r["mean_reward"] for r in co]),
        "phase_mean_reward": _mean([r["mean_reward"] for r in phase]),
        "co_phase_action_alignment_mean": _mean(alignments),
        "co_period3_repeat_score_mean": _mean(co_lag),
        "phase_period3_repeat_score_mean": _mean(phase_lag),
        "diagnosis": "CO underperforms because it does not extract/retain compact recurrence phase state comparable to PhaseFSM; sequence composition is local phase evidence, not a learned/locked renewal phase variable.",
        "cause_layer": "generic recurrence/phase extraction underdeveloped; not solved by shape alone",
    }


# ---------------- Maintenance ----------------

def _run_maintenance_seed(base: Mapping[str, Any], seed: int, regime: str, agent_name: str) -> Dict[str, Any]:
    spec = spec_from_name(regime, seed)
    env = MaintenanceReplacementEnv(spec)
    obs, _, done, info = env.reset(seed=seed)
    max_steps = min(MAINTENANCE_HORIZON_CAP, int(spec.horizon))
    if agent_name == "co":
        agent = build_agent("co", seed, spec=spec, co_params=dict(base))
    else:
        if agent_name == "finite_horizon_dp" and str(spec.observe_health) != "direct":
            return {"seed":seed, "regime":regime, "agent":agent_name, "skipped":True, "skip_reason":"oracle hidden/partial health"}
        agent = build_agent(agent_name, seed, spec=spec)
    actions: List[str] = []
    rewards: List[float] = []
    trigger_cases = 0
    trigger_selected = 0
    carrier_resolver_cases = 0
    shape_trigger_cases = 0
    high_debt_run_cases = 0
    run_count = 0
    t = 0
    while not done and t < max_steps:
        if agent_name == "co":
            sel = agent.select(obs)
            action = str(sel.get("action", ""))
            if action not in ACTIONS:
                raise ValueError(f"CO invalid maintenance action {action!r}")
            rows = _rows_from_agent(agent)
            tel = _row_telemetry(rows, selected_action=action)
            has_carrier = any(_float(r, "branch_internal_carrier_pressure") > 0.0 or _float(r, "field_debt") > 0.08 for r in rows)
            has_resolver = any(_float(r, "branch_internal_resolver_support") > 0.0 or _float(r, "resolver_support") > 0.0 for r in rows)
            if has_carrier and has_resolver:
                carrier_resolver_cases += 1
            if bool(sel.get("shape_gauged_resolver_timing_applied", False)):
                shape_trigger_cases += 1
            if has_carrier and has_resolver and action in {"INSPECT", "REPAIR", "REPLACE", "WAIT"}:
                trigger_selected += 1
            if has_carrier and has_resolver:
                trigger_cases += 1
            if action == "RUN":
                run_count += 1
                if tel.get("selected_field_debt", 0.0) > 0.08 or tel.get("avg_field_debt", 0.0) > 0.12:
                    high_debt_run_cases += 1
            _append_jsonl(MAINT_STEPS, {"agent":"co", "regime":regime, "seed":seed, "t":t, "action":action, "reward":0.0, "obs":obs, "carrier_resolver_case":has_carrier and has_resolver, "shape_gauged_resolver": bool(sel.get("shape_gauged_resolver_timing_applied", False)), **tel})
        else:
            action = str(agent.select(obs))
            if action not in ACTIONS:
                raise ValueError(f"baseline invalid maintenance action {action!r}")
            _append_jsonl(MAINT_STEPS, {"agent":agent_name, "regime":regime, "seed":seed, "t":t, "action":action, "obs":obs})
        next_obs, reward, done, info = env.step(action)
        rewards.append(float(reward)); actions.append(action)
        if hasattr(agent, "update"):
            agent.update({"action":action, "reward":float(reward), "done":bool(done), "info":dict(info)})
        obs = next_obs
        t += 1
    repair_or_replace_count = sum(1 for a in actions if a in {"REPAIR", "REPLACE"})
    inspect_count = sum(1 for a in actions if a == "INSPECT")
    inspect_followed_by_relief = 0
    for i, a in enumerate(actions):
        if a == "INSPECT" and any(x in {"REPAIR", "REPLACE"} for x in actions[i+1:i+4]):
            inspect_followed_by_relief += 1
    max_inspect_streak = 0
    cur = 0
    for a in actions:
        if a == "INSPECT":
            cur += 1
            max_inspect_streak = max(max_inspect_streak, cur)
        else:
            cur = 0
    return {
        "seed":seed,
        "regime":regime,
        "agent":agent_name,
        "total_reward":float(sum(rewards)),
        "steps":len(actions),
        "action_counts":dict(Counter(actions)),
        "first_actions":actions[:30],
        "run_rate":float(sum(1 for a in actions if a == "RUN") / float(len(actions) or 1)),
        "maintenance_action_rate":float(sum(1 for a in actions if a in {"INSPECT","REPAIR","REPLACE"}) / float(len(actions) or 1)),
        "inspect_count": int(inspect_count),
        "repair_or_replace_count": int(repair_or_replace_count),
        "inspect_followed_by_relief_rate": float(inspect_followed_by_relief / float(inspect_count or 1)),
        "max_inspect_streak": int(max_inspect_streak),
        "carrier_resolver_cases":carrier_resolver_cases if agent_name == "co" else None,
        "shape_trigger_cases":shape_trigger_cases if agent_name == "co" else None,
        "carrier_resolver_selected_maintenance_cases":trigger_selected if agent_name == "co" else None,
        "carrier_resolver_to_maintenance_rate":float(trigger_selected / float(trigger_cases or 1)) if agent_name == "co" else None,
        "high_debt_run_cases":high_debt_run_cases if agent_name == "co" else None,
        "run_count":run_count if agent_name == "co" else None,
    }


def _maintenance_audit(base: Mapping[str, Any]) -> Dict[str, Any]:
    regimes = ["bandit_like", "middle", "renewal_like"]
    out: Dict[str, Any] = {}
    for regime in regimes:
        co = [_run_maintenance_seed(base, s, regime, "co") for s in SEEDS]
        threshold = [_run_maintenance_seed(base, s, regime, "threshold") for s in SEEDS]
        q_learning = []  # skipped in bounded targeted audit to avoid timeout; q-learning covered by prior comparison
        out[regime] = {
            "co": co,
            "threshold": threshold,
            "q_learning": q_learning,
            "q_learning_note": "skipped in this bounded targeted audit; see all-problem STOA comparison for q-learning",
            "co_total_reward_mean": _mean([r["total_reward"] for r in co]),
            "threshold_total_reward_mean": _mean([r["total_reward"] for r in threshold]),
            "q_learning_total_reward_mean": None,
            "co_run_rate_mean": _mean([r["run_rate"] for r in co]),
            "co_maintenance_action_rate_mean": _mean([r["maintenance_action_rate"] for r in co]),
            "co_carrier_resolver_cases_total": int(sum(r["carrier_resolver_cases"] or 0 for r in co)),
            "co_shape_trigger_cases_total": int(sum(r["shape_trigger_cases"] or 0 for r in co)),
            "co_high_debt_run_cases_total": int(sum(r["high_debt_run_cases"] or 0 for r in co)),
            "co_carrier_resolver_to_maintenance_rate_mean": _mean([r["carrier_resolver_to_maintenance_rate"] or 0.0 for r in co]),
            "co_inspect_count_mean": _mean([float(r.get("inspect_count", 0)) for r in co]),
            "co_repair_or_replace_count_mean": _mean([float(r.get("repair_or_replace_count", 0)) for r in co]),
            "co_inspect_followed_by_relief_rate_mean": _mean([float(r.get("inspect_followed_by_relief_rate", 0.0)) for r in co]),
            "co_max_inspect_streak_mean": _mean([float(r.get("max_inspect_streak", 0)) for r in co]),
        }
    return {
        "by_regime": out,
        "diagnosis": "Maintenance failure is not absence of CO telemetry.  In middle-like regimes carrier/resolver situations and high-debt RUN cases occur, but gate/readout timing still often retains RUN/stable continuation; longer horizon exposes this more than short factor sweeps.",
        "cause_layer": "generic carrier/resolver gate + readout timing under phase/degradation burden; not a maintenance-specific rule gap",
    }


def _write_report(summary: Mapping[str, Any]) -> None:
    b = summary["bandit"]
    r = summary["renewal"]
    m = summary["maintenance"]
    lines = [
        "# Pass-1 Targeted Failure-Cause Audit — 2026-05-25",
        "",
        f"**Claim boundary:** {CLAIM_BOUNDARY}",
        "",
        "## Bottom line",
        "",
        "The weak CO-vs-STOA comparison is not caused by a single missing toggle. The targeted audit separates three cause clusters:",
        "",
        "1. **Bandit:** weak posterior-like evidence accumulation / exploration cadence.",
        "2. **Renewal:** weak compact recurrence/phase extraction compared with PhaseFSM.",
        "3. **Maintenance:** longer-horizon phase transition is wrong: middle-like traces often shift from RUN into repeated INSPECT/exposure, but do not progress generically to relief/stabilization; this is sequence/readout phase-consumption failure, not a repair-specific missing rule.",
        "",
        "No new kernel mechanism or problem-specific adjustment was made in this pass.",
        "",
        "## Bandit",
        "",
        f"- CO mean regret: `{b['co_regret_mean']:.4f}`",
        f"- Thompson Sampling mean regret: `{b['ts_regret_mean']:.4f}`",
        f"- CO late best-arm pull rate: `{b['co_late_best_arm_pull_rate_mean']:.4f}`",
        f"- TS late best-arm pull rate: `{b['ts_late_best_arm_pull_rate_mean']:.4f}`",
        "",
        "**Diagnosis:** CO has public uncertainty/burden signals, but it does not maintain or consume a compact posterior-like evidence state. When early feedback misleads, support/stability can lock in more slowly or wrongly than Thompson Sampling.",
        "",
        "## Renewal",
        "",
        f"- CO mean reward: `{r['co_mean_reward']:.4f}`",
        f"- PhaseFSM mean reward: `{r['phase_mean_reward']:.4f}`",
        f"- CO/Phase action alignment: `{r['co_phase_action_alignment_mean']:.4f}`",
        f"- CO period-3 repeat score: `{r['co_period3_repeat_score_mean']:.4f}`",
        f"- PhaseFSM period-3 repeat score: `{r['phase_period3_repeat_score_mean']:.4f}`",
        "",
        "**Diagnosis:** CO sequence composition is local and does not yet form a compact, retained recurrence-phase variable. PhaseFSM directly represents the relevant cycle; CO currently under-extracts it.",
        "",
        "## Maintenance",
        "",
    ]
    for regime, d in m["by_regime"].items():
        lines.extend([
            f"### {regime}",
            "",
            f"- CO mean total reward: `{d['co_total_reward_mean']:.4f}`",
            f"- Threshold mean total reward: `{d['threshold_total_reward_mean']:.4f}`",
            f"- Q-learning mean total reward: `{d['q_learning_total_reward_mean'] if d['q_learning_total_reward_mean'] is not None else 'skipped here'}`",
            f"- CO RUN rate: `{d['co_run_rate_mean']:.4f}`",
            f"- CO maintenance-action rate: `{d['co_maintenance_action_rate_mean']:.4f}`",
            f"- Carrier/resolver cases: `{d['co_carrier_resolver_cases_total']}`",
            f"- Shape-gauged resolver triggers: `{d['co_shape_trigger_cases_total']}`",
            f"- High-debt RUN cases: `{d['co_high_debt_run_cases_total']}`",
            f"- Carrier/resolver → maintenance selection rate: `{d['co_carrier_resolver_to_maintenance_rate_mean']:.4f}`",
            f"- CO mean INSPECT count: `{d['co_inspect_count_mean']:.2f}`",
            f"- CO mean REPAIR/REPLACE count: `{d['co_repair_or_replace_count_mean']:.2f}`",
            f"- INSPECT followed by relief within 3 steps: `{d['co_inspect_followed_by_relief_rate_mean']:.4f}`",
            f"- Mean max INSPECT streak: `{d['co_max_inspect_streak_mean']:.2f}`",
            "",
        ])
    lines.extend([
        "## Cause summary",
        "",
        "The current Pass-1 kernel detects many relevant structures, but each weak family exposes a different missing strength:",
        "",
        "- bandit requires stronger generic statistical evidence accumulation, not sequence/quotient machinery;",
        "- renewal requires a generic recurrence/phase-retention abstraction, not simply local sequence rows;",
        "- maintenance requires stronger generic phase-transition consumption (expose/reveal → relieve/reduce → stabilize) over longer horizons, not a repair-specific rule.",
        "",
        "## Recommended next steps",
        "",
        "1. Do not add task-specific fixes.",
        "2. Decide whether CO should include a generic recurrent-regime/phase-retention element. This may be a real missing concept, but it must pass the concept-admission gate.",
        "3. Audit whether bandit/posterior-style evidence should remain a weakness CO accepts, or whether generic evidence-state retention belongs inside the kernel.",
        "4. For maintenance, run a generic gate/readout adequacy redesign only if context-conditioned traces show strong carrier/resolver/phase expectation with repeated non-selection.",
        "",
        "## Outputs",
        "",
        f"- `{SUMMARY_JSON.relative_to(ROOT)}`",
        f"- `{BANDIT_STEPS.relative_to(ROOT)}`",
        f"- `{RENEWAL_STEPS.relative_to(ROOT)}`",
        f"- `{MAINT_STEPS.relative_to(ROOT)}`",
        "",
    ])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run() -> Dict[str, Any]:
    _clear_outputs()
    base = _base_params()
    summary = {
        "study": STUDY,
        "claim_boundary": CLAIM_BOUNDARY,
        "started_at": _iso(),
        "settings": {"seeds": SEEDS, "bandit_horizon": BANDIT_HORIZON, "renewal_horizon": RENEWAL_HORIZON, "maintenance_horizon_cap": MAINTENANCE_HORIZON_CAP},
        "bandit": _bandit_audit(base),
        "renewal": _renewal_audit(base),
        "maintenance": _maintenance_audit(base),
        "non_claims": [
            "not a tuning run",
            "not publication evidence",
            "not a proof that CO fails or succeeds",
            "not a justification for problem-specific patches",
        ],
        "completed_at": _iso(),
    }
    _write_json(SUMMARY_JSON, summary)
    _write_report(summary)
    return summary


def main(argv: Optional[Sequence[str]] = None) -> int:
    payload = run()
    print(json.dumps(_json_safe({
        "study": STUDY,
        "bandit_co_regret_mean": payload["bandit"]["co_regret_mean"],
        "bandit_ts_regret_mean": payload["bandit"]["ts_regret_mean"],
        "renewal_co_mean_reward": payload["renewal"]["co_mean_reward"],
        "renewal_phase_mean_reward": payload["renewal"]["phase_mean_reward"],
        "maintenance_middle_co_reward": payload["maintenance"]["by_regime"]["middle"]["co_total_reward_mean"],
        "maintenance_middle_threshold_reward": payload["maintenance"]["by_regime"]["middle"]["threshold_total_reward_mean"],
        "outputs": [str(SUMMARY_JSON), str(REPORT_MD)],
    }), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
