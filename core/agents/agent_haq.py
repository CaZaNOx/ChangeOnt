from typing import Optional, Dict

from core.loops.edge_costs import TransitionModel
from core.loops.loop_score import loop_score


class HAQAgent:
    """
    Minimal HAQ agent (CO-pure):
      - learns token→token transitions from observations only (no oracles),
      - base cost δ(u→v) = 1 − P(v|u) with Dirichlet(α) smoothing,
      - perceived cost c_G(u→v) = δ(u→v) − 0.5(G[u] + G[v]),
      - loop_score s = (C_leave − C_stay) / (|C_leave| + |C_stay| + ε),
      - EXPLORE↔EXPLOIT with hysteresis + cooldown + min-hold,
      - new: flip is armed only if (i) loop advantage has margin and (ii) recent novelty is high.
    """

    def __init__(self, A: int, seed: int = 31415):
        self.A = int(A)
        self.seed = int(seed)

        # Empirical transition model on observed tokens
        self._tm = TransitionModel(A=self.A, alpha=0.3)

        # Endogenous attention/gauge G (token -> [0,1])
        self.g: Dict[int, float] = {}

        # Previous observation for updating counts and novelty
        self.prev_obs: Optional[int] = None

        # Loop score smoothing (EMA)
        self.loop_score_ema = 0.0
        self.gamma = 0.97  # slower EMA to avoid twitch

        # Flip logic + timers
        self.mode = "EXPLORE"
        self.cooldown_left = 0
        self.COOLDOWN = 10
        self.min_hold = 30
        self.hold_left = 0
        self.theta_on = 0.25
        self.theta_off = 0.15
        self.margin_on = 0.06  # require c_stay - c_leave >= margin for arm

        # Novelty EMA (CO-pure): EMA of 1 − P(obs | prev_obs)
        self.n_ema = 0.0
        self.n_gamma = 0.95
        self.n_thresh = 0.15

        # Flip bookkeeping
        self.flips = []
        self.just_flipped = False

        # Collapse flag placeholder (unused in this minimal shim)
        self.collapsed = False

    # -------- lifecycle --------

    def reset(self):
        self._tm = TransitionModel(A=self.A, alpha=0.3)
        # persist gauge across episodes (CO design); comment next line to clear per-ep
        # self.g.clear()
        self.prev_obs = None
        self.loop_score_ema = 0.0
        self.mode = "EXPLORE"
        self.cooldown_left = 0
        self.min_hold = 30
        self.hold_left = 0
        self.n_ema = 0.0
        self.flips = []
        self.just_flipped = False
        self.collapsed = False

    # -------- policy --------

    def act(self, obs, t_global: Optional[int] = None, **kwargs) -> int:
        """
        CO-pure: only uses observed tokens and learned transition stats.
        Returns action: 0=continue, 1=exit (when exploiting and leaving is cheaper).
        """

        # 1) Learn transitions from last->current observation
        if self.prev_obs is not None:
            self._tm.update(self.prev_obs, obs)

        # 2) Ensure this token has a gauge entry
        if obs not in self.g:
            self.g[obs] = 0.0

        # 3) Perceived costs & loop score
        c_stay, c_leave = self._tm.stay_leave_costs(obs, self.g)
        s_raw = loop_score(c_leave, c_stay, eps=1e-6)
        self.loop_score_ema = self.gamma * self.loop_score_ema + (1.0 - self.gamma) * s_raw

        # 4) Novelty EMA (from token stream only)
        nov = 0.0
        if self.prev_obs is not None:
            p_row = self._tm.probs_row(self.prev_obs)
            nov = 1.0 - p_row.get(obs, 0.0)
        self.n_ema = self.n_gamma * self.n_ema + (1.0 - self.n_gamma) * nov

        # 5) Gauge update (Robbins–Monro; CO-pure proxies for PE/EU)
        pe = 0.0
        if self.prev_obs is not None:
            pe = 1.0 - self._tm.prob(self.prev_obs, obs)  # misprediction rate
        eu = s_raw if s_raw > 0.0 else 0.0               # advantage to staying (bounded by loop score)
        eta = 1.0 / (1.0 + (t_global or 0) + 50.0) ** 0.6
        self.g[obs] = max(0.0, min(1.0, self.g[obs] + eta * (1.0 * pe - 0.8 * eu - 0.001 * self.g[obs])))

        # 6) Flip logic with margin + novelty gates
        margin = (c_stay - c_leave)  # positive when staying is cheaper than leaving

        self.just_flipped = False
        if self.cooldown_left > 0:
            self.cooldown_left -= 1
        if self.hold_left > 0:
            self.hold_left -= 1

        arm_ok = (self.loop_score_ema >= self.theta_on) and (margin >= self.margin_on) and (self.n_ema >= self.n_thresh)
        disarm_ok = (self.loop_score_ema <= self.theta_off)

        if self.cooldown_left == 0 and self.hold_left == 0:
            if self.mode == "EXPLORE" and arm_ok:
                self.mode = "EXPLOIT"
                self.flips.append(t_global if t_global is not None else 0)
                self.cooldown_left = self.COOLDOWN
                self.hold_left = self.min_hold
                self.just_flipped = True
            elif self.mode == "EXPLOIT" and disarm_ok:
                self.mode = "EXPLORE"
                self.flips.append(t_global if t_global is not None else 0)
                self.cooldown_left = self.COOLDOWN
                self.hold_left = self.min_hold
                self.just_flipped = True

        # 7) Remember current obs for next update
        self.prev_obs = obs

        # 8) Action: in EXPLOIT, exit iff leaving is cheaper than staying (no oracle)
        if self.mode == "EXPLOIT":
            return 1 if (c_leave < c_stay) else 0
        else:
            return 0