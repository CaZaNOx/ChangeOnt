from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any
import random

Action = str
ACTIONS: List[Action] = ["UP", "DOWN", "LEFT", "RIGHT", "INTERACT"]
DIRS = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}


@dataclass
class MechanismSpec:
    width: int = 9
    height: int = 7
    mechanism_depth: int = 2
    hiddenness: float = 1.0
    rewrite_harshness: float = 0.6
    local_deceptiveness: float = 0.0
    seed: int = 0
    max_steps: int = 120
    observe_progress: bool = False
    reset_on_wrong: bool = True
    start: Tuple[int, int] = (3, 1)
    goal: Tuple[int, int] = (3, 7)
    door: Tuple[int, int] = (3, 4)
    switches: List[Tuple[int, int]] = field(default_factory=lambda: [(1, 2), (5, 2), (3, 2)])
    decoys: List[Tuple[int, int]] = field(default_factory=lambda: [(1, 6), (5, 6)])

    @staticmethod
    def easy_visible(seed: int = 0) -> "MechanismSpec":
        return MechanismSpec(
            mechanism_depth=1,
            hiddenness=0.0,
            rewrite_harshness=0.2,
            local_deceptiveness=0.0,
            observe_progress=True,
            reset_on_wrong=False,
            seed=seed,
            max_steps=80,
        )

    @staticmethod
    def hidden_depth2(seed: int = 0) -> "MechanismSpec":
        return MechanismSpec(
            mechanism_depth=2,
            hiddenness=1.0,
            rewrite_harshness=0.6,
            local_deceptiveness=0.2,
            observe_progress=False,
            reset_on_wrong=True,
            seed=seed,
            max_steps=120,
        )

    @staticmethod
    def deceptive_depth3(seed: int = 0) -> "MechanismSpec":
        return MechanismSpec(
            mechanism_depth=3,
            hiddenness=1.0,
            rewrite_harshness=0.85,
            local_deceptiveness=0.6,
            observe_progress=False,
            reset_on_wrong=True,
            seed=seed,
            max_steps=180,
        )


class LatentMechanismDoorWorld:
    def __init__(self, spec: MechanismSpec):
        self.spec = spec
        self.rng = random.Random(spec.seed)
        self.reset(seed=spec.seed)

    def _sample_sequence(self) -> List[Tuple[int, int]]:
        pool = list(self.spec.switches)
        self.rng.shuffle(pool)
        return pool[: max(1, min(self.spec.mechanism_depth, len(pool)))]

    def reset(self, seed: Optional[int] = None):
        if seed is not None:
            self.rng = random.Random(int(seed))
        self.pos = tuple(self.spec.start)
        self.steps = 0
        self.done = False
        self.unlock_seq = self._sample_sequence()
        self.progress = 0
        self.wrong_count = 0
        self.attempted: Dict[Tuple[int, int], int] = {}
        self.path: List[Tuple[int, int]] = [self.pos]
        self.last_action: Optional[str] = None
        self.last_event: str = "start"
        self._sync_door_state()
        return self.get_observation(), 0.0, False, self._info()

    def _sync_door_state(self) -> None:
        self.door_open = self.progress >= len(self.unlock_seq)

    def _in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.spec.height and 0 <= c < self.spec.width

    def _is_border(self, r: int, c: int) -> bool:
        return r == 0 or c == 0 or r == self.spec.height - 1 or c == self.spec.width - 1

    def _is_wall(self, r: int, c: int) -> bool:
        if not self._in_bounds(r, c):
            return True
        if self._is_border(r, c):
            return True
        if c == self.spec.door[1] and r != self.spec.door[0]:
            return True
        if (r, c) == self.spec.door and not self.door_open:
            return True
        return False

    def _tile_kind(self, r: int, c: int) -> str:
        if (r, c) == self.pos:
            return "agent"
        if (r, c) == self.spec.goal:
            return "goal"
        if (r, c) == self.spec.door:
            return "door_open" if self.door_open else "door_closed"
        if (r, c) in self.spec.switches:
            return "switch"
        if (r, c) in self.spec.decoys:
            return "decoy"
        if self._is_wall(r, c):
            return "wall"
        return "free"

    def _grid_obs(self) -> List[List[int]]:
        out: List[List[int]] = []
        for r in range(self.spec.height):
            row: List[int] = []
            for c in range(self.spec.width):
                k = self._tile_kind(r, c)
                row.append({
                    "free": 0, "wall": 1, "switch": 2, "decoy": 3,
                    "door_closed": 4, "door_open": 0, "goal": 5, "agent": 6,
                }[k])
            out.append(row)
        return out

    def _legal(self, action: str) -> bool:
        if action == "INTERACT":
            return self.pos in self.spec.switches or self.pos in self.spec.decoys
        drdc = DIRS.get(action)
        if drdc is None:
            return False
        nr = self.pos[0] + drdc[0]
        nc = self.pos[1] + drdc[1]
        return not self._is_wall(nr, nc)

    def legal_actions(self) -> List[str]:
        return [a for a in ACTIONS if self._legal(a)]

    def step(self, action: Action):
        if self.done:
            return self.get_observation(), 0.0, True, self._info()
        self.steps += 1
        reward = -1.0
        self.last_action = action
        self.last_event = "noop"
        if action in DIRS:
            if self._legal(action):
                dr, dc = DIRS[action]
                self.pos = (self.pos[0] + dr, self.pos[1] + dc)
                self.last_event = "move"
            else:
                reward -= 1.0
                self.last_event = "blocked"
        elif action == "INTERACT":
            tile = self.pos
            self.attempted[tile] = self.attempted.get(tile, 0) + 1
            if tile in self.unlock_seq and self.progress < len(self.unlock_seq) and tile == self.unlock_seq[self.progress]:
                self.progress += 1
                reward += 1.0
                self.last_event = "mechanism_progress"
            elif tile in self.spec.decoys or tile in self.spec.switches:
                self.wrong_count += 1
                self.last_event = "wrong_interact"
                reward -= 1.0 - 1.0 * min(1.0, self.spec.rewrite_harshness)
                if self.spec.reset_on_wrong:
                    self.progress = 0
            else:
                reward -= 0.5
                self.last_event = "idle_interact"
            self._sync_door_state()
        if self.pos == self.spec.goal:
            reward += 20.0
            self.done = True
            self.last_event = "goal"
        if self.steps >= self.spec.max_steps:
            self.done = True
        self.path.append(self.pos)
        return self.get_observation(), reward, self.done, self._info()

    def _info(self) -> Dict[str, Any]:
        return {
            "door_open": bool(self.door_open),
            "progress": int(self.progress),
            "mechanism_depth": int(len(self.unlock_seq)),
            "wrong_count": int(self.wrong_count),
            "last_event": self.last_event,
            "unlock_seq": [list(x) for x in self.unlock_seq],
        }

    def get_observation(self) -> Dict[str, Any]:
        door_visible = 1.0 if self.door_open else 0.0
        progress_signal = float(self.progress) / float(max(1, len(self.unlock_seq)))
        progress_obs = progress_signal if (self.spec.hiddenness < 1.0 or self.spec.observe_progress) else None
        door_shortcut_bias = float(max(0.0, min(1.0, 1.0 - abs(self.pos[0] - self.spec.door[0]) / float(max(1, self.spec.height - 2)))))
        active_hint = None
        if self.progress < len(self.unlock_seq) and (self.spec.hiddenness < 0.25 or self.spec.observe_progress):
            try:
                active_hint = list(self.unlock_seq[self.progress])
            except Exception:
                active_hint = None
        return {
            "family": "latent_mechanism",
            "t": int(self.steps),
            "pos": list(self.pos),
            "goal": list(self.spec.goal),
            "door": list(self.spec.door),
            "door_open": bool(self.door_open),
            "door_visible_state": door_visible,
            "progress_obs": progress_obs,
            "progress_true": progress_signal,
            "height": int(self.spec.height),
            "width": int(self.spec.width),
            "grid": self._grid_obs(),
            "mechanism_depth": int(len(self.unlock_seq)),
            "hiddenness": float(self.spec.hiddenness),
            "rewrite_harshness": float(self.spec.rewrite_harshness),
            "local_deceptiveness": float(self.spec.local_deceptiveness),
            "legal_actions": self.legal_actions(),
            "recent_path": [list(p) for p in self.path[-8:]],
            "door_shortcut_bias": float(self.spec.local_deceptiveness * door_shortcut_bias),
            "switches": [list(s) for s in self.spec.switches],
            "decoys": [list(d) for d in self.spec.decoys],
            "active_switch_hint": active_hint,
            "last_event": self.last_event,
        }
