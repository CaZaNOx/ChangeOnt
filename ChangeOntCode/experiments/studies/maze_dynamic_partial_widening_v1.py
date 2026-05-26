from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml  # type: ignore
except Exception as exc:  # pragma: no cover
    raise RuntimeError("PyYAML is required to load CO agent config") from exc

from environments.maze1.env import GridMazeEnv, MazeSpec
from agents.stoa.maze.replanning_visible_astar import visible_replanning_astar_action
from agents.co.integration.core_builder import build_co_core
from agents.co.adapters.maze_adapter import COAdapterMaze


DEFAULT_SEEDS = list(range(10)) + [19, 33]


def _load_co_full_params() -> Dict[str, Any]:
    cfg_path = Path("experiments/configs/co_agents/co_agents_selection.yaml")
    payload = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    for agent in list(payload.get("co_agents", [])):
        if str(agent.get("name")) == "CO_canonical_core":
            return dict(agent.get("params", {}))
    raise RuntimeError("CO_canonical_core config not found in experiments/configs/co_agents/co_agents_selection.yaml")


def _run_visible_astar(spec: MazeSpec, unknown_penalty: float = 0.0) -> Dict[str, Any]:
    env = GridMazeEnv(spec=spec)
    steps = 0
    trace: List[str] = []
    while steps < 500 and env.pos != env.goal:
        act = visible_replanning_astar_action(
            env.get_observation(),
            optimistic_unknown=True,
            unknown_penalty=float(unknown_penalty),
        )
        if act not in ("UP", "DOWN", "LEFT", "RIGHT"):
            act = "RIGHT"
        _, reward, done, _info = env.step(act)
        trace.append(act)
        steps += 1
        if done:
            break
    return {
        "steps": int(steps),
        "solved": bool(env.pos == env.goal),
        "return": float(-max(0, steps - 1) if env.pos == env.goal else -steps),
        "trace_prefix": trace[:20],
    }


def _run_co(spec: MazeSpec, co_params: Dict[str, Any]) -> Dict[str, Any]:
    env = GridMazeEnv(spec=spec)
    core = build_co_core(co_params)
    agent = COAdapterMaze(core=core, name="CO_canonical_core")
    steps = 0
    trace: List[str] = []
    while steps < 500 and env.pos != env.goal:
        obs = {"family": "maze", "t": steps, "episode": 0, **env.get_observation()}
        sel = agent.select(obs)
        act = sel.get("action") if isinstance(sel, dict) else sel
        if act not in ("UP", "DOWN", "LEFT", "RIGHT"):
            act = "RIGHT"
        _, reward, done, _info = env.step(act)
        agent.update({
            "observation": tuple(env.pos),
            "reward": reward,
            "done": done,
            "action": act,
        })
        trace.append(act)
        steps += 1
        if done:
            break
    return {
        "steps": int(steps),
        "solved": bool(env.pos == env.goal),
        "return": float(-max(0, steps - 1) if env.pos == env.goal else -steps),
        "trace_prefix": trace[:20],
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Widen dynamic/partial maze on fair discovered-map baselines.")
    ap.add_argument("--out", type=str, default="outputs/maze_dynamic_partial_widening_v1.json")
    ap.add_argument("--seeds", type=int, nargs="*", default=DEFAULT_SEEDS)
    ap.add_argument("--width", type=int, default=9)
    ap.add_argument("--height", type=int, default=9)
    ap.add_argument("--view-radius", type=int, default=1)
    ap.add_argument("--wall-flip-prob", type=float, default=0.12)
    ap.add_argument("--max-flips-per-step", type=int, default=1)
    args = ap.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    co_params = _load_co_full_params()

    rows: List[Dict[str, Any]] = []
    for seed in list(args.seeds):
        spec = MazeSpec(
            width=int(args.width),
            height=int(args.height),
            seed=int(seed),
            partial_observability=True,
            view_radius=int(args.view_radius),
            dynamic_walls=True,
            wall_flip_prob=float(args.wall_flip_prob),
            max_flips_per_step=int(args.max_flips_per_step),
        )
        baseline = _run_visible_astar(spec, unknown_penalty=0.0)
        baseline_pen = _run_visible_astar(spec, unknown_penalty=0.35)
        co = _run_co(spec, co_params)
        rows.append({
            "seed": int(seed),
            "visible_astar": baseline,
            "visible_astar_unknown_penalty": baseline_pen,
            "co_full": co,
            "co_minus_visible_astar_steps": int(co["steps"] - baseline["steps"]),
            "co_minus_visible_astar_unknown_penalty_steps": int(co["steps"] - baseline_pen["steps"]),
        })

    solved_all = {
        "visible_astar": all(bool(r["visible_astar"]["solved"]) for r in rows),
        "visible_astar_unknown_penalty": all(bool(r["visible_astar_unknown_penalty"]["solved"]) for r in rows),
        "co_full": all(bool(r["co_full"]["solved"]) for r in rows),
    }
    payload = {
        "study": "maze_dynamic_partial_widening_v1",
        "status": "executed",
        "environment": {
            "family": "maze",
            "width": int(args.width),
            "height": int(args.height),
            "partial_observability": True,
            "view_radius": int(args.view_radius),
            "dynamic_walls": True,
            "wall_flip_prob": float(args.wall_flip_prob),
            "max_flips_per_step": int(args.max_flips_per_step),
            "fairness_boundary": [
                "CO sees only discovered/visible grid with unknown cells = -1",
                "fair baselines replan from the same discovered grid each step",
                "no hidden full-map shortest path is given to CO or discovered-map baselines",
                "dynamic flips are accepted only when the environment preserves a path from current position to goal",
            ],
        },
        "agents": ["CO_canonical_core", "visible_astar", "visible_astar_unknown_penalty"],
        "seeds": list(args.seeds),
        "results": rows,
        "summary": {
            "solved_all": solved_all,
            "mean_co_minus_visible_astar_steps": sum(r["co_minus_visible_astar_steps"] for r in rows) / max(1, len(rows)),
            "mean_co_minus_visible_astar_unknown_penalty_steps": sum(r["co_minus_visible_astar_unknown_penalty_steps"] for r in rows) / max(1, len(rows)),
            "max_co_minus_visible_astar_steps": max(r["co_minus_visible_astar_steps"] for r in rows),
            "min_co_minus_visible_astar_steps": min(r["co_minus_visible_astar_steps"] for r in rows),
        },
        "interpretation_guardrails": [
            "This study validates restored machinery and a first widened comparison only.",
            "It does not establish broad dynamic/partial maze closure.",
            "Any stronger maze claim should widen beyond this seed block and inspect bad-seed traces.",
        ],
    }
    out_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
