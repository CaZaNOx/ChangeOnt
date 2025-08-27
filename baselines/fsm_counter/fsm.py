# Baseline FSM counter with a tolerant API matching the runner

class FSMCounter:
    def __init__(self, A: int, interval: int = 12, **kwargs):
        # Runner passes period=env_cfg.k; accept it as an alias
        if 'period' in kwargs and kwargs['period'] is not None:
            interval = kwargs.pop('period')
        self.A = int(A)
        self.interval = int(interval)

        # --- interface fields expected by the runner/loggers ---
        self.just_flipped = False      # set True only on a mode flip (FSM never flips)
        self.mode = "STATIC"           # for logs; HAQ uses EXPLORE/EXPLOIT
        self.flips = []                # timestamps of flips (empty for FSM)
        self.loop_score_ema = 0.0      # placeholder so loggers don’t choke
        self.collapsed = False         # header flag parity
        # -------------------------------------------------------

        self.count = 0

    def reset(self):
        self.count = 0
        self.just_flipped = False
        self.mode = "STATIC"
        self.flips.clear()
        self.loop_score_ema = 0.0
        self.collapsed = False

    # Some runners call begin/end hooks; make them no-ops
    def begin_episode(self, **kwargs):
        self.reset()

    def end_episode(self, **kwargs):
        pass

    # Standardized agent API: accept t_global and ignore extra kwargs
    def act(self, obs, t_global=None, **kwargs) -> int:
        # FSM never flips modes
        self.just_flipped = False
        self.count += 1
        # Simple heuristic baseline: exit every fixed interval
        return 1 if (self.count % self.interval == 0) else 0