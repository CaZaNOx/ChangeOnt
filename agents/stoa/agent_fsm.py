# agents/stoa/agent_fsm.py
from __future__ import annotations

class LastFSM:
    """
    Deterministic Mealy FSM baseline:
      state = last observed symbol (finite set {0..A-1})
      λ(q, x) = x   (predict next == current obs)
      δ(q, x) = x
    """
    def __init__(self, A: int):
        self.A = int(A); self.state = 0
    def reset(self, init_obs: int) -> None:
        self.state = int(init_obs)
    def act(self, obs: int) -> int:
        self.state = int(obs); return self.state
    def transition(self, q: int, x: int) -> int: return int(x)
    def output(self, q: int, x: int) -> int: return int(x)
    def budget_row(self) -> dict:
        return {"params_bits": self.A, "flops_per_step": 1, "memory_bytes": self.A}

class PhaseFSM:
    """
    Finite Mealy FSM for length-L cycles.
    State = phase ∈ {0..L-1}. Transition: phase ← (phase+1) mod L.
    Output: Code[(phase+1) mod L]. Learning: Code[phase] ← obs (one-step online).
    The full (explicit) finite state space is (phase, Code[0..L-1]) with A^L states.
    """
    def __init__(self, A: int, L_win: int):
        self.A = int(A)
        self.L = int(L_win)
        self.phase = 0
        self.code = [0 for _ in range(self.L)]

    def reset(self, init_obs: int):
        self.phase = 0
        v = int(init_obs)
        self.code = [v for _ in range(self.L)]

    def act(self, obs: int) -> int:
        pred = self.code[(self.phase + 1) % self.L]
        self.code[self.phase] = int(obs)           # learn mapping
        self.phase = (self.phase + 1) % self.L     # advance
        return int(pred)

    def budget_row(self) -> dict:
        # tiny, explicit finite footprint
        return {"params_bits": self.L, "flops_per_step": 4, "memory_bytes": self.L}

class NGramFSM:
    """
    Finite Mealy FSM with order-k context (k=L-1 typical).
    State = tuple(last k symbols) ⇒ |Σ|^k finite states.
    Transition: shift in current obs.
    Output: argmax over counts[next | state] with Laplace smoothing (finite tables).
    """
    def __init__(self, A: int, k: int):
        self.A = int(A)
        self.k = int(k)
        self.ctx = tuple([0]*self.k) if self.k > 0 else tuple()
        self.counts = {}  # dict[ctx -> dict[next->count]]

    def reset(self, init_obs: int):
        if self.k > 0:
            v = int(init_obs)
            self.ctx = tuple([v]*self.k)
        else:
            self.ctx = tuple()
        self.counts.clear()

    def _predict_from_ctx(self, ctx):
        c = self.counts.get(ctx)
        if not c:
            return 0  # deterministic tie-break
        best_y, best_v = 0, -1
        for y in range(self.A):
            v = c.get(y, 0) + 1  # Laplace smoothing
            if v > best_v:
                best_v, best_y = v, y
        return best_y

    def act(self, obs: int) -> int:
        ctx = self.ctx
        pred = self._predict_from_ctx(ctx)
        # learn: update next-symbol count for current context
        c = self.counts.get(ctx)
        if c is None:
            c = {}
            self.counts[ctx] = c
        y = int(obs)
        c[y] = c.get(y, 0) + 1
        # transition context
        if self.k > 0:
            if self.k == 1:
                self.ctx = (y,)
            else:
                lst = list(ctx)[1:] + [y]
                self.ctx = tuple(lst)
        return int(pred)

    def budget_row(self) -> dict:
        # finite upper bound footprint; explicit for audit
        return {"params_bits": self.A * max(1, self.k), "flops_per_step": self.A + self.k, "memory_bytes": self.A * max(1, self.k)}
