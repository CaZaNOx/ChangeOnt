"""Runtime wiring invariants for the maintenance/replacement runner default.

Run:
    python -m agents.co.tests.maintenance_replacement_runtime_wiring_invariants
"""
from __future__ import annotations

from environments.maintenance_replacement.env import ACTIONS, MaintenanceReplacementEnv
from experiments.runners.maintenance_replacement_runner import build_agent, spec_from_name
from agents.co.placement.shape_prior6 import SHAPE_PRIOR6_AXES, shape_prior6_to_direct_controls


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def main() -> None:
    spec = spec_from_name("bandit_like", 0)
    env = MaintenanceReplacementEnv(spec)
    obs, _, done, _ = env.reset(seed=0)
    agent = build_agent("co", 0, spec=spec)

    sel = agent.select(obs)
    action = str(sel.get("action"))
    _assert(action in ACTIONS, f"runner-default CO action outside maintenance action set: {action}")
    _assert(int(sel.get("signal_bus_votes", 0) or 0) > 0, "runner-default CO must enable CandidateEvidenceSurface before CommitmentSurface")
    next_obs, reward, done, info = env.step(action)
    agent.update({"action": action, "reward": float(reward), "done": bool(done), "info": dict(info)})

    st = getattr(agent.core.header, "state", None)
    _assert(st is not None, "runner-default CO header state missing after update")
    _assert(
        float(getattr(st, "local_authority", 0.5)) != 0.5
        or float(getattr(st, "nonlocal_authority", 0.5)) != 0.5,
        "runner-default CO must let packet problem_contract drive non-default six-question controls",
    )

    _assert(int(getattr(st, "update_count", 0)) > 0, "adapter feedback pass must drive core/header update_count")


def _uncertainty_by_mode() -> None:
    hidden = spec_from_name("renewal_like", 0)
    env = MaintenanceReplacementEnv(hidden)
    obs, _, done, _ = env.reset(seed=0)
    agent = build_agent("co", 0, spec=hidden)
    d0 = agent._derive(obs)
    _assert(float(d0["residuals"]["uncertainty"]) >= 0.80, "hidden uninspected health must be high-uncertainty, not treated as known")
    obs, _, done, info = env.step("INSPECT")
    d1 = agent._derive(obs)
    _assert(float(d1["residuals"]["uncertainty"]) <= 0.20, "fresh hidden inspection should be low-uncertainty public evidence")
    obs, _, done, info = env.step("RUN")
    d2 = agent._derive(obs)
    _assert(float(d2["residuals"]["uncertainty"]) > float(d1["residuals"]["uncertainty"]), "hidden inspected health must become more uncertain when it grows stale")

    direct = spec_from_name("bandit_like", 0)
    denv = MaintenanceReplacementEnv(direct)
    dobs, _, _, _ = denv.reset(seed=0)
    dagent = build_agent("co", 0, spec=direct)
    dd = dagent._derive(dobs)
    inspect = next(c for c in dd["candidates"] if c["candidate_id"] == "INSPECT")
    run = next(c for c in dd["candidates"] if c["candidate_id"] == "RUN")
    _assert(float(inspect["goal_relation"]) < 0.05, "direct health observation should not publish INSPECT as a useful information action")
    _assert(float(run["goal_relation"]) > float(inspect["goal_relation"]), "RUN must dominate useless INSPECT under direct high-health public observation")


def _shape_override_reaches_header() -> None:
    spec = spec_from_name("middle", 0)
    env = MaintenanceReplacementEnv(spec)
    obs, _, _, _ = env.reset(seed=0)
    override_axes = {k: 1.0 for k in SHAPE_PRIOR6_AXES}
    agent = build_agent("co", 0, spec=spec, co_params={"shape_prior6_override": {"axes": override_axes, "source": "study_override"}})
    sel = agent.select(obs)
    keys = set(sel.get("problem_packet_keys", []))
    _assert("shape_prior6" in keys, "study-only wrong-shape override must be placed on the public packet")
    action = str(sel.get("action"))
    next_obs, reward, done, info = env.step(action)
    agent.update({"action": action, "reward": float(reward), "done": bool(done), "info": dict(info)})
    expected = shape_prior6_to_direct_controls({"axes": override_axes})["axes"]
    st = getattr(agent.core.header, "state", None)
    _assert(st is not None, "header state missing under shape override")
    _assert(abs(float(getattr(st, "nonlocal_authority", -1.0)) - float(expected["nonlocal_authority"])) < 1e-9, "shape override did not drive header direct controls")


if __name__ == "__main__":
    main()
    _uncertainty_by_mode()
    _shape_override_reaches_header()
