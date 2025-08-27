from dataclasses import dataclass
import random

@dataclass
class EnvCfg:
    A:int; Lwin:int; p_ren:float; p_merge:float; p_split:float
    p_noise:float; p_adv:float; Tmax:int; k:int
    # new (optional) loopiness knobs; default off if not provided
    p_loop: float = 0.0          # probability to repeat last observed token
    p_loop_marker: float = 0.0   # while looping, probability to set marker = that token

class CodebookRenewalEnvW:
    """
    Renewal-with-codebook toy plant, now with optional "loopiness":
      - with prob p_loop, repeat last observed token (creates real self-loops),
      - occasionally pins the event marker to the looping token (p_loop_marker).
    This remains CO-pure: agent only sees tokens, not flags or counters.
    """
    def __init__(self, cfg:EnvCfg, seed:int):
        self.cfg = cfg
        self.rng = random.Random(seed)
        self.t = 0
        self.done = False
        self.latents = list(range(cfg.A))
        self.marker = 0
        self.visit = 0
        self._last_obs = None

    def reset(self):
        self.t = 0; self.done = False
        self.latents = list(range(self.cfg.A))
        self.rng.shuffle(self.latents)
        self.marker = self.rng.randrange(self.cfg.A)
        self.visit = 0
        self._last_obs = None
        obs = self._emit()
        return obs, 0.0, False, {"renewal":False,"kth_opportunity":False}

    def step(self, action:int):
        if self.done: raise StopIteration
        self.t += 1
        renewal = False; kth = False

        # Renewal?
        if self.rng.random() < self.cfg.p_ren:
            self._renew(); renewal = True

        # Merge/split?
        r = self.rng.random()
        if r < self.cfg.p_merge:
            self._merge()
        elif r < self.cfg.p_merge + self.cfg.p_split:
            self._split()

        # Emit observation with optional loopiness
        obs = self._emit()

        # Count opportunities at the level of latents-as-observed (toy)
        if self._latent_for(obs) == self.marker:
            self.visit += 1
            if self.visit == self.cfg.k:
                kth = True

        # Reward only if exiting exactly on k-th opportunity
        reward = 1.0 if (action==1 and kth) else 0.0
        if action==1:  # episode ends on exit attempt
            self.done = True
        if self.t >= self.cfg.Tmax:
            self.done = True

        return obs, reward, self.done, {"renewal":renewal,"kth_opportunity":kth}

    def _emit(self):
        # With probability p_loop, repeat last observed token
        tok = None
        if (self._last_obs is not None) and (self.rng.random() < getattr(self.cfg, "p_loop", 0.0)):
            tok = self._last_obs
            # While in a loop, occasionally set marker to this token (ties events to loops)
            if self.rng.random() < getattr(self.cfg, "p_loop_marker", 0.0):
                self.marker = self._latent_for(tok)
        else:
            tok = self.latents[self.rng.randrange(self.cfg.A)]

        # Noise
        if self.rng.random() < self.cfg.p_noise:
            tok = self.rng.randrange(self.cfg.A)

        self._last_obs = tok
        return tok

    def _renew(self):
        self.rng.shuffle(self.latents)
        self.marker = self.rng.randrange(self.cfg.A)
        self.visit = 0

    def _merge(self):
        i, j = self.rng.sample(range(self.cfg.A), 2)
        self.latents[j] = self.latents[i]

    def _split(self):
        j = self.rng.randrange(self.cfg.A)
        self.latents[j] = self.rng.randrange(self.cfg.A)

    def _latent_for(self, tok):
        # inverse is ambiguous when many latents map to same tok; ok for toy probe
        return tok