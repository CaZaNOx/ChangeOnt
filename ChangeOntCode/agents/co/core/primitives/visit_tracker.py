# agents/co/core/primitives/visit_tracker.py
from __future__ import annotations
from typing import Dict, Tuple, Set, Optional

Dir = str
Pos = Tuple[int, int]

class VisitTracker:
    """
    Maze helper: remembers last (pos, action) → if pos didn't change next step,
    mark that action as blocked at that pos. Also counts visits to avoid cycles.
    """
    def __init__(self, horizon: int = 512) -> None:
        self.horizon = int(horizon)
        self.last_pos: Optional[Pos] = None
        self.last_action: Optional[Dir] = None
        self.blocked: Dict[Pos, Set[Dir]] = {}
        self.visits: Dict[Pos, int] = {}

    def note_visit(self, pos: Pos) -> None:
        c = self.visits.get(pos, 0) + 1
        self.visits[pos] = c
        # (Optional) decimate very old counts
        if c > self.horizon:
            self.visits[pos] = self.horizon

    def is_blocked(self, pos: Pos, direction: Dir) -> bool:
        return direction in self.blocked.get(pos, set())

    def record_action(self, pos: Pos, action: Dir) -> None:
        self.last_pos = pos
        self.last_action = action

    def on_feedback(self, feedback: Dict) -> None:
        # We expect runner/adapter to include current pos after the step.
        curr = feedback.get("observation")
        if curr is None:
            curr = feedback.get("pos")
        if not isinstance(curr, (tuple, list)) or len(curr) != 2:
            return
        curr_pos: Pos = (int(curr[0]), int(curr[1]))
        # If we attempted an action last step and position did not change,
        # mark that action as blocked at the last position.
        if self.last_pos is not None and self.last_action is not None:
            if curr_pos == self.last_pos:
                self.blocked.setdefault(self.last_pos, set()).add(self.last_action)
        # Always count visit
        self.note_visit(curr_pos)
        # Update last_pos to what we just observed
        self.last_pos = curr_pos