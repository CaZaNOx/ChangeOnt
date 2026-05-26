from __future__ import annotations

"""Current-kernel diagnostic map v1.

First-pass diagnostic, not an empirical proof suite.  The study runs the current
CO kernel across the existing active problem families with generic mechanism
ablations:

- full_current: DynamicShapeField + quotient/equivalence + recursion scheduler + sequence composition;
- static_shape: DynamicShapeField disabled only;
- no_quotient: quotient/equivalence disabled only;
- no_scheduler: recursion scheduler disabled only;
- no_sequence: sequence composition disabled only;
- minimal_recent_core: recent mechanisms disabled.

The purpose is to map what the rough first-pass kernel actually does across
families, and to catch cases where a mechanism is inert, overactive, or causing
unexplained behavior.  It is intentionally small and claim-bounded.
"""

import json
import os
import sys
from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, List, Mapping, Tuple

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.studies._co_eval_common import load_co_manifest_params
from agents.co.integration.core_builder import build_co_core
from environments.bandit.bandit import BernoulliBanditEnv
from agents.co.adapters.bandit_adapter import COAdapterBandit
from environments.renewal.env import CodebookRenewalEnvW, EnvCfg
from agents.co.adapters.renewal_adapter import COAdapterRenewal
from environments.maze1.env import GridMazeEnv, MazeSpec
from agents.co.adapters.maze_adapter import COAdapterMaze
from environments.latent_mechanism.env import LatentMechanismDoorWorld, MechanismSpec
from agents.co.adapters.latent_mechanism_adapter import COAdapterLatentMechanism
from experiments.runners.maintenance_replacement_runner import spec_from_name
from environments.maintenance_replacement.env import MaintenanceReplacementEnv, ACTIONS as MAINT_ACTIONS
from agents.co.adapters.maintenance_replacement_adapter import COAdapterMaintenanceReplacement

OUT_DIR = ROOT / "outputs" / "current_kernel_diagnostic_map_v1"
RUNS_JSONL = OUT_DIR / "runs.jsonl"
STEPS_JSONL = OUT_DIR / "steps.jsonl"
SUMMARY_JSON = OUT_DIR / "summary.json"
REPORT_MD = ROOT.parent / "CURRENT_KERNEL_DIAGNOSTIC_MAP_REPORT_2026-05-22.md"

SEEDS = [0]
VARIANTS: Dict[str, Dict[str, bool]] = {
    "full_current": {"dynamic_shape_enabled": True, "quotient_enabled": True, "recursion_scheduler_enabled": True, "sequence_composition_enabled": True},
    "static_shape": {"dynamic_shape_enabled": False, "quotient_enabled": True, "recursion_scheduler_enabled": True, "sequence_composition_enabled": True},
    "no_quotient": {"dynamic_shape_enabled": True, "quotient_enabled": False, "recursion_scheduler_enabled": True, "sequence_composition_enabled": True},
    "no_scheduler": {"dynamic_shape_enabled": True, "quotient_enabled": True, "recursion_scheduler_enabled": False, "sequence_composition_enabled": True},
    "no_sequence": {"dynamic_shape_enabled": True, "quotient_enabled": True, "recursion_scheduler_enabled": True, "sequence_composition_enabled": False},
    "minimal_recent_core": {"dynamic_shape_enabled": False, "quotient_enabled": False, "recursion_scheduler_enabled": False, "sequence_composition_enabled": False},
}

CLAIM_BOUNDARY = (
    "First-pass diagnostic map only. It tests whether recent generic kernel mechanisms are behavior/telemetry visible "
    "across existing problem families. It is not a benchmark, not CO proof, not novelty evidence, and not a reason "
    "to tune coefficients post hoc."
)


def _json_safe(x: Any) -> Any:
    if isinstance(x, Mapping):
        return {str(k): _json_safe(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_json_safe(v) for v in x]
    if isinstance(x, (str, int, float, bool)) or x is None:
        return x
    return str(x)


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_json_safe(data), indent=2, sort_keys=True), encoding="utf-8")


def _append_jsonl(path: Path, row: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(_json_safe(dict(row)), sort_keys=True) + "\n")


def _load_base_params() -> Dict[str, Any]:
    return load_co_manifest_params(ROOT / "experiments" / "configs" / "co_agents" / "co_agents_canonical_core.yaml")


def _params_for_variant(base: Mapping[str, Any], variant: str) -> Dict[str, Any]:
    params = deepcopy(dict(base))
    elements = dict(params.get("elements", {}) or {})
    cand = dict(elements.get("candidate_surface", {}) or {})
    cand.setdefault("enabled", True)
    cand.update(VARIANTS[variant])
    elements["candidate_surface"] = cand
    params["elements"] = elements
    return params


def _core_agent(adapter_cls: Any, base_params: Mapping[str, Any], variant: str, *args: Any, **kwargs: Any) -> Any:
    core = build_co_core(_params_for_variant(base_params, variant))
    return adapter_cls(core=core, *args, **kwargs)


def _rows_from_agent(agent: Any) -> List[Dict[str, Any]]:
    core = getattr(agent, "core", None)
    prims = getattr(core, "primitives", {}) if core is not None else {}
    rows = prims.get("__candidate_publication_rows__", []) if isinstance(prims, dict) else []
    return [dict(r) for r in rows if isinstance(r, dict)]


def _relation_telemetry(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    for row in rows:
        tel = row.get("relation_surface_telemetry")
        if isinstance(tel, dict):
            return dict(tel)
    return {}


def _avg(rows: Iterable[Mapping[str, Any]], key: str) -> float:
    vals: List[float] = []
    for r in rows:
        try:
            vals.append(float(r.get(key, 0.0) or 0.0))
        except Exception:
            pass
    return float(mean(vals)) if vals else 0.0


def _max(rows: Iterable[Mapping[str, Any]], key: str) -> float:
    vals: List[float] = []
    for r in rows:
        try:
            vals.append(float(r.get(key, 0.0) or 0.0))
        except Exception:
            pass
    return max(vals) if vals else 0.0


def _row_trace_sample(rows: List[Dict[str, Any]], limit: int = 6) -> List[Dict[str, Any]]:
    """Return compact row-level trace for mechanism provenance audits."""
    keys = (
        "action", "continuation_id", "branch_id", "continuation_memory_id",
        "support_mass", "decision_state", "burden_pressure", "field_debt",
        "field_grey_pressure", "field_recursion_budget", "field_recursion_budget_before_scheduler",
        "recursion_scheduler_demand", "recursion_scheduler_structural_channel",
        "recursion_scheduler_sampling_uncertainty_channel", "recursion_scheduler_weak_procedural_channel",
        "recursion_scheduler_mode", "collapse_certificate_status", "collapse_blockers",
        "quotient_id", "quotient_share_count", "relation_surface_quotient_profile",
        "relation_surface_quotient_profile_accepted", "relation_surface_quotient_profile_reason",
        "relation_surface_quotient_profile_entries", "dynamic_shape_controls_active",
        "continuation_phase", "sequence_composition_active", "sequence_composition_id",
        "sequence_continuation_id", "ordered_continuation_id", "sequence_phase_transition",
        "sequence_previous_phase", "sequence_domain_compatibility", "sequence_composition_support",
        "sequence_composition_reason",
    )
    out: List[Dict[str, Any]] = []
    for r in rows[:limit]:
        item = {k: _json_safe(r.get(k)) for k in keys if k in r}
        eff = r.get("dynamic_shape_effective_controls")
        if isinstance(eff, dict):
            item["dynamic_shape_effective_controls"] = {
                k: _json_safe(eff.get(k))
                for k in (
                    "local_authority", "nonlocal_authority", "path_sensitivity",
                    "revision_permissibility", "collapse_admissibility",
                    "low_evidence_sampling", "dynamic_shape_urgency",
                    "dynamic_shape_coarsening", "dynamic_shape_projection_horizon",
                    "dynamic_shape_gauge_confidence",
                ) if k in eff
            }
        out.append(item)
    return out


def _step_summary(*, family: str, mode: str, seed: int, variant: str, t: int, action: Any, reward: float, sel: Mapping[str, Any], rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    rel_tel = _relation_telemetry(rows)
    dyn_updates = [r.get("dynamic_shape_update") for r in rows if isinstance(r.get("dynamic_shape_update"), dict)]
    dyn_applied = any(bool(u.get("applied")) for u in dyn_updates if isinstance(u, dict))
    quotient_rows = sum(1 for r in rows if float(r.get("quotient_share_count", 1) or 1) > 1)
    scheduler_disabled = any(bool(r.get("recursion_scheduler_disabled")) for r in rows)
    sequence_rows = sum(1 for r in rows if bool(r.get("sequence_composition_active")))
    sequence_disabled = any(bool(r.get("sequence_composition_disabled")) for r in rows)
    direct_controls = dict(sel.get("direct_controls_used", {}) or {}) if isinstance(sel.get("direct_controls_used", {}), dict) else {}
    assessment = sel.get("canonical_commitment_assessment", {}) if isinstance(sel.get("canonical_commitment_assessment", {}), dict) else {}
    return {
        "family": family,
        "mode": mode,
        "seed": int(seed),
        "variant": variant,
        "t": int(t),
        "action": action,
        "reward": float(reward),
        "canonical_commitment_mode": sel.get("canonical_commitment_mode"),
        "canonical_commitment_reason": sel.get("canonical_commitment_reason"),
        "shape_gauged_resolver_timing_applied": bool(sel.get("shape_gauged_resolver_timing_applied", False)),
        "certificate_aware_stable_continuation_applied": bool(sel.get("certificate_aware_stable_continuation_applied", False)),
        "certificate_aware_reopen_or_sample_applied": bool(sel.get("certificate_aware_reopen_or_sample_applied", False)),
        "candidate_rows": len(rows),
        "relations_total": int(rel_tel.get("relations_total", 0) or 0),
        "relations_by_type": dict(rel_tel.get("relations_by_type", {}) or {}),
        "rows_with_relations": int(rel_tel.get("rows_with_relations", 0) or 0),
        "quotient_rows": int(quotient_rows),
        "quotient_disabled": bool(rel_tel.get("quotient_equivalence_disabled", 0)),
        "quotient_profiles_accepted": int(rel_tel.get("quotient_profiles_accepted", 0) or 0),
        "quotient_profiles_rejected": dict(rel_tel.get("quotient_profiles_rejected", {}) or {}),
        "quotient_buckets_with_multiple_members": int(rel_tel.get("quotient_buckets_with_multiple_members", 0) or 0),
        "quotient_profile_summaries_sample": list(rel_tel.get("quotient_profile_summaries", []) or [])[:8],
        "dynamic_shape_applied": dyn_applied,
        "dynamic_shape_update_count": int((dyn_updates[-1] or {}).get("state_after", {}).get("update_count", 0) if dyn_updates else 0),
        "avg_recursion_scheduler_demand": _avg(rows, "recursion_scheduler_demand"),
        "max_recursion_scheduler_demand": _max(rows, "recursion_scheduler_demand"),
        "avg_recursion_scheduler_structural_channel": _avg(rows, "recursion_scheduler_structural_channel"),
        "max_recursion_scheduler_structural_channel": _max(rows, "recursion_scheduler_structural_channel"),
        "avg_recursion_scheduler_sampling_uncertainty_channel": _avg(rows, "recursion_scheduler_sampling_uncertainty_channel"),
        "avg_recursion_scheduler_weak_procedural_channel": _avg(rows, "recursion_scheduler_weak_procedural_channel"),
        "avg_field_recursion_budget": _avg(rows, "field_recursion_budget"),
        "avg_field_recursion_budget_before_scheduler": _avg(rows, "field_recursion_budget_before_scheduler"),
        "max_field_grey_pressure": _max(rows, "field_grey_pressure"),
        "avg_field_debt": _avg(rows, "field_debt"),
        "avg_collapse_blockers": _avg(rows, "collapse_blocker_count"),
        "scheduler_disabled": scheduler_disabled,
        "sequence_rows": int(sequence_rows),
        "sequence_disabled": bool(sequence_disabled),
        "max_sequence_composition_support": _max(rows, "sequence_composition_support"),
        "dynamic_shape_controls_applied_in_commitment": bool(direct_controls.get("dynamic_shape_controls_applied", 0.0)),
        "direct_controls_used": _json_safe(direct_controls),
        "local_shape_gauge": _json_safe(sel.get("local_shape_gauge", {})),
        "canonical_commitment_assessment_summary": _json_safe(assessment),
        "row_trace_sample": _row_trace_sample(rows),
        "co_evidence_valid_for_step": bool(sel.get("co_evidence_valid_for_step", False)),
    }


def _run_bandit(base_params: Mapping[str, Any], variant: str, seed: int) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    horizon = 16
    env = BernoulliBanditEnv([0.10, 0.20, 0.80], horizon=horizon)
    env.reset(seed=seed)
    agent = _core_agent(COAdapterBandit, base_params, variant, name="CO_diag", n_arms=env.n_arms)
    total_reward = 0.0
    steps: List[Dict[str, Any]] = []
    done = False
    t = 0
    while not done and t < horizon:
        sel = agent.select({"family": "bandit", "t": t, "n_arms": env.n_arms})
        action = int(sel["action"])
        _, reward, done, _ = env.step(action)
        rows = _rows_from_agent(agent)
        steps.append(_step_summary(family="bandit", mode="easy_public_bandit", seed=seed, variant=variant, t=t, action=action, reward=float(reward), sel=sel, rows=rows))
        agent.update({"action": action, "reward": float(reward), "done": bool(done)})
        total_reward += float(reward)
        t += 1
    return {"metric_name": "total_reward", "metric_value": total_reward, "metric_direction": "higher_is_better", "steps": t}, steps


def _run_renewal(base_params: Mapping[str, Any], variant: str, seed: int) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    horizon = 16
    cfg = EnvCfg(A=4, L_win=3, p_ren=0.04, p_noise=0.02, T_max=horizon)
    env = CodebookRenewalEnvW(cfg, seed=seed)
    obs, _, done, _ = env.reset()
    agent = _core_agent(COAdapterRenewal, base_params, variant, name="CO_diag")
    total_reward = 0.0
    steps: List[Dict[str, Any]] = []
    for t in range(horizon):
        sel = agent.select({"family": "renewal", "obs": int(obs), "t": t, "A": cfg.A, "L_win": cfg.L_win})
        action = int(sel["action"])
        obs, reward, done, _ = env.step(action)
        rows = _rows_from_agent(agent)
        steps.append(_step_summary(family="renewal", mode="noisy_renewal", seed=seed, variant=variant, t=t, action=action, reward=float(reward), sel=sel, rows=rows))
        agent.update({"observation": int(obs), "reward": float(reward), "done": bool(done), "action": int(action)})
        total_reward += float(reward)
        if done:
            break
    return {"metric_name": "total_reward", "metric_value": total_reward, "metric_direction": "higher_is_better", "steps": len(steps)}, steps


def _run_maze(base_params: Mapping[str, Any], variant: str, seed: int) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    horizon = 16
    env = GridMazeEnv(spec=MazeSpec(width=5, height=5, seed=seed, partial_observability=False))
    env.reset(seed=seed)
    agent = _core_agent(COAdapterMaze, base_params, variant, name="CO_diag")
    total_reward = 0.0
    steps: List[Dict[str, Any]] = []
    done = False
    for t in range(horizon):
        obs = env.get_observation()
        obs.update({"family": "maze", "t": t})
        sel = agent.select(obs)
        action = str(sel["action"])
        _, reward, done, _ = env.step(action)
        rows = _rows_from_agent(agent)
        steps.append(_step_summary(family="maze", mode="static_visible_5x5", seed=seed, variant=variant, t=t, action=action, reward=float(reward), sel=sel, rows=rows))
        agent.update({"observation": tuple(env.pos), "reward": float(reward), "done": bool(done), "action": action})
        total_reward += float(reward)
        if done:
            break
    return {"metric_name": "episode_return", "metric_value": total_reward, "metric_direction": "higher_is_better", "steps": len(steps), "done": bool(done)}, steps


def _latent_spec(mode: str, seed: int, horizon: int) -> MechanismSpec:
    spec = MechanismSpec.easy_visible(seed=seed) if mode == "easy_visible" else MechanismSpec.hidden_depth2(seed=seed)
    spec.max_steps = int(horizon)
    return spec


def _run_latent(base_params: Mapping[str, Any], variant: str, seed: int, mode: str) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    horizon = 16
    env = LatentMechanismDoorWorld(_latent_spec(mode, seed, horizon))
    obs, _, done, info = env.reset(seed=seed)
    agent = _core_agent(COAdapterLatentMechanism, base_params, variant, name="CO_diag")
    total_reward = 0.0
    steps: List[Dict[str, Any]] = []
    success = False
    for t in range(horizon):
        sel = agent.select(obs)
        action = str(sel["action"])
        next_obs, reward, done, info = env.step(action)
        rows = _rows_from_agent(agent)
        steps.append(_step_summary(family="latent_mechanism", mode=mode, seed=seed, variant=variant, t=t, action=action, reward=float(reward), sel=sel, rows=rows))
        agent.update({"observation": tuple(next_obs.get("pos") or (0, 0)), "reward": float(reward), "done": bool(done), "action": action})
        total_reward += float(reward)
        obs = next_obs
        if done:
            success = tuple(obs.get("pos") or (0, 0)) == tuple(obs.get("goal") or (999, 999))
            break
    return {"metric_name": "episode_return", "metric_value": total_reward, "metric_direction": "higher_is_better", "steps": len(steps), "success": int(success), "wrong_count": int(info.get("wrong_count", 0) or 0)}, steps


def _run_maintenance(base_params: Mapping[str, Any], variant: str, seed: int, regime: str) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    spec = spec_from_name(regime, seed)
    # Diagnostic cap: keep this first-pass map fast enough to run in a cold takeover.
    spec.horizon = min(int(spec.horizon), 18)
    env = MaintenanceReplacementEnv(spec)
    obs, _, done, info = env.reset(seed=seed)
    agent = _core_agent(COAdapterMaintenanceReplacement, base_params, variant, name="CO_diag")
    total_reward = 0.0
    steps: List[Dict[str, Any]] = []
    t = 0
    while not done:
        sel = agent.select(obs)
        action = str(sel["action"])
        if action not in MAINT_ACTIONS:
            raise RuntimeError(f"invalid maintenance CO action {action!r}")
        next_obs, reward, done, info = env.step(action)
        rows = _rows_from_agent(agent)
        steps.append(_step_summary(family="maintenance_replacement", mode=regime, seed=seed, variant=variant, t=t, action=action, reward=float(reward), sel=sel, rows=rows))
        agent.update({"action": action, "reward": float(reward), "done": bool(done), "info": dict(info)})
        total_reward += float(reward)
        obs = next_obs
        t += 1
    return {"metric_name": "total_reward", "metric_value": total_reward, "metric_direction": "higher_is_better", "steps": len(steps), "observation_mode": spec.observe_health}, steps


TASKS = [
    ("bandit", "easy_public_bandit"),
    ("renewal", "noisy_renewal"),
    ("maze", "static_visible_5x5"),
    ("latent_mechanism", "easy_visible"),
    ("latent_mechanism", "hidden_depth2"),
    ("maintenance_replacement", "bandit_like"),
    ("maintenance_replacement", "middle"),
    ("maintenance_replacement", "renewal_like"),
]


def _run_task(base_params: Mapping[str, Any], family: str, mode: str, variant: str, seed: int) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    if family == "bandit":
        return _run_bandit(base_params, variant, seed)
    if family == "renewal":
        return _run_renewal(base_params, variant, seed)
    if family == "maze":
        return _run_maze(base_params, variant, seed)
    if family == "latent_mechanism":
        return _run_latent(base_params, variant, seed, mode)
    if family == "maintenance_replacement":
        return _run_maintenance(base_params, variant, seed, mode)
    raise ValueError(f"unknown task {family}:{mode}")


def _summarize_run_steps(steps: List[Dict[str, Any]]) -> Dict[str, Any]:
    modes = Counter(str(s.get("canonical_commitment_mode", "")) for s in steps)
    reasons = Counter(str(s.get("canonical_commitment_reason", "")) for s in steps)
    actions = [str(s.get("action")) for s in steps]
    return {
        "steps_logged": len(steps),
        "unique_actions": len(set(actions)),
        "action_trace_prefix": actions[:16],
        "commitment_modes": dict(modes),
        "top_commitment_reasons": dict(reasons.most_common(5)),
        "shape_gauged_resolver_steps": sum(1 for s in steps if s.get("shape_gauged_resolver_timing_applied")),
        "certificate_stable_continuation_steps": sum(1 for s in steps if s.get("certificate_aware_stable_continuation_applied")),
        "certificate_reopen_steps": sum(1 for s in steps if s.get("certificate_aware_reopen_or_sample_applied")),
        "avg_relations_total": _avg(steps, "relations_total"),
        "avg_quotient_rows": _avg(steps, "quotient_rows"),
        "avg_sequence_rows": _avg(steps, "sequence_rows"),
        "sequence_active_steps": sum(1 for s in steps if int(s.get("sequence_rows", 0) or 0) > 0),
        "dynamic_shape_applied_steps": sum(1 for s in steps if s.get("dynamic_shape_applied")),
        "avg_recursion_scheduler_demand": _avg(steps, "avg_recursion_scheduler_demand"),
        "max_recursion_scheduler_demand": _max(steps, "max_recursion_scheduler_demand"),
        "avg_field_recursion_budget": _avg(steps, "avg_field_recursion_budget"),
        "avg_collapse_blockers": _avg(steps, "avg_collapse_blockers"),
        "co_invalid_steps": sum(1 for s in steps if not s.get("co_evidence_valid_for_step")),
    }


def main() -> Dict[str, Any]:
    os.environ["CO_STRICT_ERRORS"] = "1"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for p in (RUNS_JSONL, STEPS_JSONL, SUMMARY_JSON):
        if p.exists():
            p.unlink()
    base = _load_base_params()
    runs: List[Dict[str, Any]] = []
    failures: List[Dict[str, Any]] = []
    for family, mode in TASKS:
        for seed in SEEDS:
            for variant in VARIANTS:
                run_id = f"{family}__{mode}__{variant}__s{seed}"
                try:
                    metrics, steps = _run_task(base, family, mode, variant, seed)
                    for step in steps:
                        step["run_id"] = run_id
                        _append_jsonl(STEPS_JSONL, step)
                    row = {
                        "run_id": run_id,
                        "family": family,
                        "mode": mode,
                        "seed": int(seed),
                        "variant": variant,
                        "mechanism_flags": dict(VARIANTS[variant]),
                        **metrics,
                        **_summarize_run_steps(steps),
                    }
                    runs.append(row)
                    _append_jsonl(RUNS_JSONL, row)
                except Exception as exc:
                    fail = {"run_id": run_id, "family": family, "mode": mode, "seed": int(seed), "variant": variant, "error": f"{type(exc).__name__}: {exc}"}
                    failures.append(fail)
                    _append_jsonl(RUNS_JSONL, {**fail, "status": "failed"})
    # Compare full_current against ablations per family/mode/seed.
    by_key: Dict[Tuple[str, str, int], Dict[str, Dict[str, Any]]] = defaultdict(dict)
    for row in runs:
        by_key[(row["family"], row["mode"], int(row["seed"]))][row["variant"]] = row
    comparisons: List[Dict[str, Any]] = []
    for (family, mode, seed), vmap in sorted(by_key.items()):
        full = vmap.get("full_current")
        if not full:
            continue
        full_prefix = list(full.get("action_trace_prefix", []))
        for variant, row in sorted(vmap.items()):
            if variant == "full_current":
                continue
            prefix = list(row.get("action_trace_prefix", []))
            n = min(len(full_prefix), len(prefix))
            diff = sum(1 for i in range(n) if full_prefix[i] != prefix[i]) + abs(len(full_prefix) - len(prefix))
            comparisons.append({
                "family": family,
                "mode": mode,
                "seed": seed,
                "ablation": variant,
                "metric_delta_vs_full": (float(row.get("metric_value", 0.0) or 0.0) - float(full.get("metric_value", 0.0) or 0.0)),
                "prefix_action_differences_vs_full": int(diff),
                "dynamic_shape_step_delta_vs_full": int(row.get("dynamic_shape_applied_steps", 0) or 0) - int(full.get("dynamic_shape_applied_steps", 0) or 0),
                "avg_recursion_demand_delta_vs_full": float(row.get("avg_recursion_scheduler_demand", 0.0) or 0.0) - float(full.get("avg_recursion_scheduler_demand", 0.0) or 0.0),
                "avg_quotient_rows_delta_vs_full": float(row.get("avg_quotient_rows", 0.0) or 0.0) - float(full.get("avg_quotient_rows", 0.0) or 0.0),
                "sequence_active_step_delta_vs_full": int(row.get("sequence_active_steps", 0) or 0) - int(full.get("sequence_active_steps", 0) or 0),
                "avg_sequence_rows_delta_vs_full": float(row.get("avg_sequence_rows", 0.0) or 0.0) - float(full.get("avg_sequence_rows", 0.0) or 0.0),
            })
    summary = {
        "study": "current_kernel_diagnostic_map_v1",
        "claim_boundary": CLAIM_BOUNDARY,
        "tasks": [{"family": f, "mode": m} for f, m in TASKS],
        "variants": VARIANTS,
        "seeds": SEEDS,
        "runs_attempted": len(TASKS) * len(SEEDS) * len(VARIANTS),
        "runs_succeeded": len(runs),
        "runs_failed": len(failures),
        "failures": failures,
        "comparisons": comparisons,
        "output_files": {"runs_jsonl": str(RUNS_JSONL.relative_to(ROOT)), "steps_jsonl": str(STEPS_JSONL.relative_to(ROOT))},
    }
    _write_json(SUMMARY_JSON, summary)
    _write_report(runs, summary)
    return summary


def _fmt_float(x: Any) -> str:
    try:
        return f"{float(x):.3f}"
    except Exception:
        return "n/a"


def _write_report(runs: List[Dict[str, Any]], summary: Dict[str, Any]) -> None:
    lines: List[str] = []
    lines.append("# Current Kernel Diagnostic Map v1 — 2026-05-22")
    lines.append("")
    lines.append("## Claim boundary")
    lines.append("")
    lines.append(CLAIM_BOUNDARY)
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(f"Runs attempted: {summary['runs_attempted']}; succeeded: {summary['runs_succeeded']}; failed: {summary['runs_failed']}.")
    lines.append("")
    lines.append("Variants: `full_current`, `static_shape`, `no_quotient`, `no_scheduler`, `no_sequence`, `minimal_recent_core`.")
    lines.append("")
    if summary.get("failures"):
        lines.append("## Failures")
        lines.append("")
        for f in summary["failures"]:
            lines.append(f"- `{f['run_id']}`: {f['error']}")
        lines.append("")
    lines.append("## Per-run map")
    lines.append("")
    lines.append("| family | mode | seed | variant | metric | actions | dyn steps | seq steps | avg seq rows | avg quotient rows | avg recursion demand | max recursion demand | avg blockers | modes |")
    lines.append("|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    for r in sorted(runs, key=lambda x: (x["family"], x["mode"], x["seed"], x["variant"])):
        lines.append(
            "| {family} | {mode} | {seed} | {variant} | {metric} | {actions} | {dyn} | {seq_steps} | {seq_rows} | {quot} | {rec} | {recmax} | {block} | `{modes}` |".format(
                family=r.get("family"),
                mode=r.get("mode"),
                seed=r.get("seed"),
                variant=r.get("variant"),
                metric=_fmt_float(r.get("metric_value")),
                actions=r.get("unique_actions"),
                dyn=r.get("dynamic_shape_applied_steps"),
                seq_steps=r.get("sequence_active_steps", 0),
                seq_rows=_fmt_float(r.get("avg_sequence_rows", 0.0)),
                quot=_fmt_float(r.get("avg_quotient_rows")),
                rec=_fmt_float(r.get("avg_recursion_scheduler_demand")),
                recmax=_fmt_float(r.get("max_recursion_scheduler_demand")),
                block=_fmt_float(r.get("avg_collapse_blockers")),
                modes=json.dumps(r.get("commitment_modes", {}), sort_keys=True),
            )
        )
    lines.append("")
    lines.append("## Full-current versus ablation deltas")
    lines.append("")
    lines.append("| family | mode | seed | ablation | metric Δ | prefix action diffs | dyn-step Δ | avg recursion Δ | avg quotient-row Δ |")
    lines.append("|---|---|---:|---|---:|---:|---:|---:|---:|")
    for c in summary.get("comparisons", []):
        lines.append(
            f"| {c['family']} | {c['mode']} | {c['seed']} | {c['ablation']} | {_fmt_float(c['metric_delta_vs_full'])} | {c['prefix_action_differences_vs_full']} | {c['dynamic_shape_step_delta_vs_full']} | {_fmt_float(c['avg_recursion_demand_delta_vs_full'])} | {_fmt_float(c['avg_quotient_rows_delta_vs_full'])} |"
        )
    lines.append("")
    lines.append("## Interpretation boundary")
    lines.append("")
    lines.append("This map is useful only for first-pass diagnosis: mechanism visibility, rough behavioral sensitivity, and failure discovery. It should not be cited as benchmark evidence or as evidence that CO is useful/novel.")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
