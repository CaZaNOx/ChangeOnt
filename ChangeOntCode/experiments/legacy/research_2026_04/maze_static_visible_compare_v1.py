from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

import yaml  # type: ignore

from environments.maze1.env import GridMazeEnv, MazeSpec
from agents.stoa.maze.replanning_visible_astar import visible_replanning_astar_action
from agents.co.integration.core_builder import build_co_core
from agents.co.adapters.maze_adapter import COAdapterMaze

SIZES = [(5,5),(7,7),(9,9),(13,13)]
SEEDS = list(range(10))


def _load_co_full_params() -> Dict[str, Any]:
    cfg_path = Path("experiments/configs/co_agents/co_agents_selection.yaml")
    payload = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    for agent in list(payload.get("co_agents", [])):
        if str(agent.get("name")) == "CO_canonical_core":
            return dict(agent.get("params", {}))
    raise RuntimeError("CO_canonical_core config not found")


def _run_visible_astar(spec: MazeSpec) -> Dict[str, Any]:
    env = GridMazeEnv(spec=spec)
    steps = 0
    while steps < 500 and env.pos != env.goal:
        act = visible_replanning_astar_action(env.get_observation(), optimistic_unknown=True, unknown_penalty=0.0)
        if act not in ("UP", "DOWN", "LEFT", "RIGHT"):
            act = "RIGHT"
        _, _, done, _ = env.step(act)
        steps += 1
        if done:
            break
    return {"steps": int(steps), "solved": bool(env.pos == env.goal)}


def _run_co(spec: MazeSpec, params: Dict[str, Any]) -> Dict[str, Any]:
    env = GridMazeEnv(spec=spec)
    core = build_co_core(params)
    agent = COAdapterMaze(core=core, name="CO_canonical_core")
    steps = 0
    while steps < 500 and env.pos != env.goal:
        obs = {"family": "maze", "t": steps, "episode": 0, **env.get_observation()}
        sel = agent.select(obs)
        act = sel.get("action") if isinstance(sel, dict) else sel
        if act not in ("UP", "DOWN", "LEFT", "RIGHT"):
            act = "RIGHT"
        _, reward, done, _ = env.step(act)
        agent.update({"observation": tuple(env.pos), "reward": reward, "done": done, "action": act})
        steps += 1
        if done:
            break
    return {"steps": int(steps), "solved": bool(env.pos == env.goal)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, default="outputs/maze_static_visible_compare_v1.json")
    args = ap.parse_args()
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    params = _load_co_full_params()
    rows: List[Dict[str, Any]] = []
    for width, height in SIZES:
        for seed in SEEDS:
            spec = MazeSpec(width=width, height=height, seed=seed, partial_observability=False, dynamic_walls=False)
            astar = _run_visible_astar(spec)
            co = _run_co(spec, params)
            rows.append({"width": width, "height": height, "seed": seed, "visible_astar": astar, "co": co, "co_minus_astar": int(co["steps"])-int(astar["steps"])})
    out = {
        "study": "maze_static_visible_compare_v1",
        "rows": rows,
        "summary": {
            "all_solved": all(r["co"]["solved"] and r["visible_astar"]["solved"] for r in rows),
            "exact_matches": sum(1 for r in rows if r["co_minus_astar"] == 0),
            "total": len(rows),
            "mean_co_minus_astar": sum(r["co_minus_astar"] for r in rows) / float(len(rows) or 1),
            "max_abs_gap": max(abs(r["co_minus_astar"]) for r in rows) if rows else 0,
        },
    }
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
