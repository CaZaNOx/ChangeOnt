# agents/co/core/primitives/P15_order_arisal.py

from __future__ import annotations
from collections import deque, defaultdict
from typing import Any, Dict, Iterable, Hashable, Optional

class OrderArisal:
    """
    P15: order-asymmetry + arisal/tension primitive (env-agnostic).

    Interface:
      - update(action=None, state_token=None): call AFTER a step to feed history/visits
      - penalty_for_actions(actions, observation=None) -> {action: penalty in [0,1]}
      - metrics() -> {"arisal":..., "loopiness":..., "osc_recent":...}

    Notes:
      - Backtrack detection uses an 'inverse_map' if provided by observation;
        otherwise it falls back to common maze labels or 2-cycle patterns.
      - Arisal is 1 on first visit of a state_token, then decays ~ 1/count;
        'tension' is exposed as EMA of arisal (you can read 'arisal' as a proxy).
    """

    def __init__(self,
                 window: int = 8,
                 ema_alpha: float = 0.2,
                 w_back: float = 0.6,
                 w_cycle: float = 0.3,
                 w_osc: float = 0.1):
        self.window    = int(max(1, window))
        self.ema_alpha = float(ema_alpha)
        self.w_back    = float(w_back)
        self.w_cycle   = float(w_cycle)
        self.w_osc     = float(w_osc)

        self.history      = deque(maxlen=self.window)         # recent actions
        self.state_counts = defaultdict(int)                  # visits per state_token
        self.arisal_ema   = 0.0
        self.loopiness_ema= 0.0
        self._last_metrics: Dict[str, float] = {}

    def reset(self) -> None:
        self.history.clear()
        self.state_counts.clear()
        self.arisal_ema = 0.0
        self.loopiness_ema = 0.0
        self._last_metrics.clear()

    @staticmethod
    def _clip01(x: float) -> float:
        return 0.0 if x < 0.0 else 1.0 if x > 1.0 else x

    def _inverse_of(self, a: Any, inverse_map: Optional[Dict[Any, Any]]) -> Optional[Any]:
        if inverse_map and a in inverse_map:
            return inverse_map[a]
        # common maze tokens
        if a == "UP": return "DOWN"
        if a == "DOWN": return "UP"
        if a == "LEFT": return "RIGHT"
        if a == "RIGHT": return "LEFT"
        return None

    def _oscillation_score(self) -> float:
        n = len(self.history)
        if n < 3:
            return 0.0
        # repetitiveness in window
        uniq = len(set(self.history))
        rep  = 1.0 - (uniq / float(n))
        # tail A,B,A pattern
        A = self.history[-3] if n >= 3 else None
        B = self.history[-2] if n >= 2 else None
        C = self.history[-1] if n >= 1 else None
        two_cycle = 1.0 if (A is not None and B is not None and C is not None and A == C and A != B) else 0.0
        return self._clip01(0.5 * rep + 0.5 * two_cycle)

    # ---- public API ---------------------------------------------------------

    def update(self, action: Optional[Any] = None, state_token: Optional[Hashable] = None) -> None:
        """Feed AFTER a step: the action you took and a hashable state token."""
        if action is not None:
            self.history.append(action)

        if state_token is not None:
            self.state_counts[state_token] += 1
            # instantaneous arisal: first time -> 1.0, then decays as 1/count
            count  = self.state_counts[state_token]
            arisal = 1.0 / float(count)
            self.arisal_ema = (1.0 - self.ema_alpha) * self.arisal_ema + self.ema_alpha * arisal

        osc = self._oscillation_score()
        self.loopiness_ema = (1.0 - self.ema_alpha) * self.loopiness_ema + self.ema_alpha * osc

        self._last_metrics = {
            "arisal":   self._clip01(self.arisal_ema),
            "loopiness":self._clip01(self.loopiness_ema),
        }

    def penalty_for_actions(self,
                            actions: Iterable[Any],
                            observation: Optional[Dict[str, Any]] = None) -> Dict[Any, float]:
        """
        Return per-action penalties in [0,1] for order asymmetry.
        observation may include:
          - 'inverse_map': dict action->inverse (optional)
          - 'family': e.g. 'maze'|'bandit'|'renewal' (optional)
        """
        inv_map = None
        family  = None
        try:
            inv_map = observation.get("inverse_map")
            family  = observation.get("family")
        except Exception:
            pass

        last = self.history[-1] if self.history else None
        prev = self.history[-2] if len(self.history) >= 2 else None

        osc = self._oscillation_score()
        out: Dict[Any, float] = {}

        for a in actions:
            # (1) backtrack (use inverse_map if present; else common maze tokens)
            back = 0.0
            inv  = self._inverse_of(last, inv_map) if last is not None else None
            if inv is not None and a == inv:
                back = 1.0

            # fallback for bandit-like: A,B then choosing A again (switch-back)
            if back == 0.0 and family in ("bandit", "renewal") and prev is not None and last is not None:
                if a == prev and a != last:
                    back = 0.7

            # (2) would this create A,B,A? then it's a 2-cycle
            cycle2 = 0.0
            if prev is not None and last is not None and a == prev and a != last:
                cycle2 = 1.0

            # (3) soft window oscillation prior
            out[a] = self._clip01(self.w_back * back + self.w_cycle * cycle2 + self.w_osc * osc)

        return out

    def metrics(self) -> Dict[str, float]:
        m = dict(self._last_metrics)
        m["osc_recent"] = self._oscillation_score()
        return m