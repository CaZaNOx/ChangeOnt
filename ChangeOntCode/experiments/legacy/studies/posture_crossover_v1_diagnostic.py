from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List

from environments.bandit.bandit import BernoulliBanditEnv
from agents.co.adapters.bandit_adapter import COAdapterBandit
from agents.co.integration.core_builder import build_co_core
from agents.co.runtime.surfaces.candidate_surface import _header_scales

OUT_PATH = Path("outputs/posture_crossover_v1_diagnostic.json")

COMMON_PARAMS: Dict[str, Any] = {
    "header": {"mode": "SSI"},
    "elements": {
        "haq": {"enabled": True, "history_len": 64, "ema_alpha": 0.2},
        "EC_Identity": {"enabled": True},
        "density": {"enabled": True, "rounding": 2},
        "change_ops": {"enabled": True, "k": 4, "mdl_select": False},
        "candidate_surface": {"enabled": True},
        "commitment_surface": {
            "enabled": True,
            "prefer_bus_if_present": True,
            "use_translator": True,
            "blend_mode": "co_only",
            "use_classical_proposal": False,
            "allow_classical_fallback": False,
            "allow_policy_rescue": False,
            "co_weight_override": None,
            "eps_on_cycle": 0.10,
            "ngram_order": 2,
            "greedy_explore_bias": 0.10,
        },
    },
    "primitives": {
        "signal_bus": {},
        "kernel_substrate": {},
        "P0": {},
        "P1": {},
        "P2": {},
        "P4": {"epsilon": 0.2, "window": 5},
        "P7": {},
        "P16": {},
        "p10": {},
        "p12": {},
        "id_mem": {},
        "bandit_stats": {},
        "ngram_model": {},
    },
    "combinator": {"order": ["haq", "EC_Identity", "density", "change_ops", "candidate_surface", "commitment_surface"]},
}

POSTURES: Dict[str, Dict[str, Any]] = {
    "early_hardening": {
        "name": "early_hardening",
        "axes": {
            "hardening_bias": 0.85,
            "reopen_bias": 0.25,
            "persistence_depth": 0.60,
            "contradiction_tolerance": 0.35,
            "collapse_readiness": 0.55,
        },
    },
    "late_hardening": {
        "name": "late_hardening",
        "axes": {
            "hardening_bias": 0.20,
            "reopen_bias": 0.80,
            "persistence_depth": 0.40,
            "contradiction_tolerance": 0.35,
            "collapse_readiness": 0.20,
        },
    },
}


def _make_agent(posture_cfg: Dict[str, Any]) -> COAdapterBandit:
    params = dict(COMMON_PARAMS)
    params["descriptor_hypothesis"] = {
        "target_scope": "hypothesis_over_anchor",
        "axes": {
            "evidence_discriminability": 0.22,
            "persistence_reliability": 0.85,
            "revision_cost": 0.80,
            "deformation_rate": 0.05,
        },
    }
    params["kernel_posture"] = dict(posture_cfg)
    params["prediction_protocol"] = {
        "base_problem": {"name": "P_confusable_stationary"},
        "predicted_ordering_before": ["late_hardening", "early_hardening"],
        "status": "declared",
    }
    core = build_co_core(params)
    return COAdapterBandit(core=core, name=str(posture_cfg.get("name", "CO")), n_arms=3)


def _packet(agent: COAdapterBandit, t: int) -> Dict[str, Any]:
    obs = {"family": "bandit", "t": t, "n_arms": 3}
    visible = agent._derive_from_visible_history(obs, t)
    from agents.co.boundary.problem_packet import make_problem_packet

    return make_problem_packet(
        family="bandit",
        step_idx=t,
        action_space=list(range(agent.n_arms)),
        current_observation={"n_arms": agent.n_arms, **obs},
        history=list(agent._history[-64:]),
        trace=list(agent._trace[-64:]),
        feedback=dict(agent._last_feedback or {}),
        residuals=visible["residuals"],
        probes=visible["probes"],
        signals=visible["signals"],
        constraints={},
        family_payload={"n_arms": agent.n_arms},
        memory_view=visible["memory_view"],
        classical_proposal=visible["classical_proposal"],
        candidates=visible["candidates"],
        goal_field=visible["goal_field"],
        field_update=dict(agent._last_field_update or {}),
        dyn_hint=visible["dyn_hint"],
        co_conf_hint=visible["co_conf_hint"],
        support_evidence=visible.get("support_evidence"),
    )


def _scope_aggregate(votes: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
    agg: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for vote in votes:
        agg[str(vote.get("scope", "base"))][str(vote.get("action"))] += float(vote.get("weight", 0.0) or 0.0)
    return {scope: dict(vals) for scope, vals in agg.items()}


def _rounded(d: Dict[str, Any], nd: int = 6) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for k, v in d.items():
        if isinstance(v, dict):
            out[k] = _rounded(v, nd)
        elif isinstance(v, float):
            out[k] = round(v, nd)
        else:
            out[k] = v
    return out


def main() -> None:
    env = BernoulliBanditEnv([0.46, 0.50, 0.54], horizon=12)
    seed = 2
    inspect_t = 4
    result: Dict[str, Any] = {
        "study": "posture_crossover_v1_diagnostic",
        "seed": seed,
        "inspect_after_updates": inspect_t,
        "postures": {},
        "comparison": {},
    }

    per_posture: Dict[str, Dict[str, Any]] = {}
    for name, posture in POSTURES.items():
        env.reset(seed=seed)
        agent = _make_agent(posture)
        core = agent.core
        for t in range(inspect_t):
            sel = agent.select({"family": "bandit", "t": t, "n_arms": 3})
            action = int(sel["action"])
            _, reward, done, _ = env.step(action)
            agent.update({"action": action, "reward": float(reward), "done": bool(done)})

        packet = _packet(agent, inspect_t)
        votes = _bandit_votes(packet, core.primitives, core.header)
        scoped = _scope_aggregate(votes)
        head = next(e for e in core.elements if e.__class__.__name__.lower().endswith("actionhead"))
        fused = head._typed_fuse_scoped(scoped, head._signal_snapshot(core.primitives))
        header_state = core.header.state
        signals = core.primitives["signal_bus"].signals()

        per_posture[name] = {
            "header": {
                "posture_name": str(header_state.posture_name),
                "posture_applied": bool(header_state.posture_applied),
                "identity_support_threshold": float(header_state.identity_support_threshold),
                "fracture_tolerance": float(header_state.fracture_tolerance),
                "retention_depth": float(header_state.retention_depth),
                "collapse_permission": float(header_state.collapse_permission),
                "evidence_gate": float(header_state.evidence_gate),
                "support_evidence": float(header_state.support_evidence),
            },
            "header_scales": _header_scales(core.header),
            "signals": {
                "continuity_conf": float(signals.get("EC_Identity.continuity_conf", 0.0)),
                "fracture_pressure": float(signals.get("EC_Identity.fracture_pressure", 0.0)),
                "incumbent_contradiction": float(signals.get("EC_Identity.incumbent_contradiction", 0.0)),
                "takeover_potential": float(signals.get("EC_Identity.takeover_potential", 0.0)),
            },
            "scoped_votes": scoped,
            "fused_scores": {str(k): float(v) for k, v in fused.items()},
        }
    result["postures"] = _rounded(per_posture)

    early = per_posture["early_hardening"]
    late = per_posture["late_hardening"]
    result["comparison"] = _rounded({
        "posture_surface_live": bool(early["header"]["posture_applied"] and late["header"]["posture_applied"]),
        "threshold_gap": float(late["header"]["identity_support_threshold"] - early["header"]["identity_support_threshold"]),
        "evidence_gate_equal": abs(early["header"]["evidence_gate"] - late["header"]["evidence_gate"]) < 1e-9,
        "evidence_gate_value": float(early["header"]["evidence_gate"]),
        "fused_scores_equal": all(abs(float(early["fused_scores"].get(str(a), 0.0)) - float(late["fused_scores"].get(str(a), 0.0))) < 1e-9 for a in range(3)),
        "notes": [
            "Runtime posture is active in the adapter path after the adapter/core.step fix.",
            "In the inspected confusable bandit state, evidence_gate saturates at 0.0 for both postures.",
            "The remaining posture effect only rescales whole vote scopes uniformly.",
            "CommitmentSurface._typed_fuse_scoped normalizes each scope independently, so uniform per-scope rescaling is erased before action selection.",
        ],
    })

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
