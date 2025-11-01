from __future__ import annotations
from typing import Dict, Any

def _clip01(x: float) -> float:
    return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)

class ArisalTension:
    """
    P0_ArisalTension
    ----------------
    Compute a unit-scale signal for "change-in-the-now" as *tension* and its
    positive increment as *arise*, using light deltas from existing bus signals.

    Inputs (from inputs.get("signals", {})):
      - EA_HAQ.novelty                     in [0,1]   (if present)
      - EE_Compressibility.mdl or P3.mdl   arbitrary  (we delta & relu)
      - P1.bend                            arbitrary  (we delta & relu)
      - P8.loopiness                       in [0,1]   (soft cue)
      - z_PE                               arbitrary  (prediction error; squashed)
      - EG_DensityPrecision.visit_density  in [0,1]   (penalty; we invert)

    Params (configure):
      - alpha: float        EMA smoothing on tension (default 0.3)
      - weights: dict       per-feature weights (see defaults below)
      - squash_k: float     logistic sharpness for z_PE (default 1.0)
      - clip: (lo,hi)       clamp bounds (default (0.0, 1.0))

    Outputs (added to returned dict):
      - "P0_ArisalTension.tension" : float in [0,1]
      - "P0_ArisalTension.arise"   : float in [0,1]
      - also flat aliases:
          "tension", "arise"
    """

    def __init__(self, **params: Any):
        self.params: Dict[str, Any] = {
            "alpha": 0.3,
            "weights": {
                "novelty": 0.35,
                "mdl_d":   0.20,
                "bend_d":  0.15,
                "loop":    0.10,
                "surp":    0.10,
                "anti_density": 0.10,  # uses (1 - visit_density)
            },
            "squash_k": 1.0,
            "clip": (0.0, 1.0),
        }
        self.params.update(params or {})
        self._state = {
            "last_tension": 0.0,
            "last_arise":   0.0,
            "mdl_prev":     None,
            "bend_prev":    None,
        }

    # keep uniform primitive surface
    def configure(self, params: Dict[str, Any], context: Dict[str, Any]):
        if params:
            # shallow merge; caller can pass partial 'weights'
            if "weights" in params and isinstance(params["weights"], dict):
                w = dict(self.params.get("weights", {}))
                w.update(params["weights"])
                p = dict(params)
                p["weights"] = w
                self.params.update(p)
            else:
                self.params.update(params)
        return self

    def fit(self, stream_or_env_view=None):
        return self

    def _squash(self, x: float) -> float:
        # gentle logistic for unbounded surprise
        k = float(self.params.get("squash_k", 1.0))
        try:
            # 1 / (1 + exp(-k x)) mapped to [0,1]
            import math
            return 1.0 / (1.0 + math.exp(-k * float(x)))
        except Exception:
            return 0.5

    def step(self, inputs: Dict[str, Any]) -> Dict[str, float]:
        sig = inputs.get("signals", {}) or {}

        novelty   = float(sig.get("EA_HAQ.novelty", 0.0))
        mdl_now   = float(sig.get("EE_Compressibility.mdl", sig.get("P3.mdl", 0.0)))
        bend_now  = float(sig.get("P1.bend", 0.0))
        loopiness = float(sig.get("P8.loopiness", 0.0))
        surprise  = self._squash(float(sig.get("z_PE", 0.0)))
        density   = float(sig.get("EG_DensityPrecision.visit_density", 0.0))
        anti_density = 1.0 - _clip01(density)

        # safe deltas (positive part only)
        mdl_prev  = self._state["mdl_prev"]
        bend_prev = self._state["bend_prev"]
        mdl_d  = max(0.0, (mdl_now  - (0.0 if mdl_prev  is None else mdl_prev)))
        bend_d = max(0.0, (bend_now - (0.0 if bend_prev is None else bend_prev)))

        # weighted mixture → normalize by sum(weights)
        w = self.params["weights"]
        raw = (
            w["novelty"]      * _clip01(novelty) +
            w["mdl_d"]        * mdl_d +
            w["bend_d"]       * bend_d +
            w["loop"]         * _clip01(loopiness) +
            w["surp"]         * _clip01(surprise) +
            w["anti_density"] * _clip01(anti_density)
        )
        denom = sum(float(v) for v in w.values()) or 1.0
        score = raw / denom
        score = _clip01(score)

        # EMA smoothing → tension; positive increment → arise
        alpha    = float(self.params.get("alpha", 0.3))
        prev_ten = float(self._state["last_tension"])
        tension  = _clip01(alpha * score + (1.0 - alpha) * prev_ten)
        arise    = _clip01(max(0.0, tension - prev_ten))

        # persist
        self._state["mdl_prev"]     = mdl_now
        self._state["bend_prev"]    = bend_now
        self._state["last_tension"] = tension
        self._state["last_arise"]   = arise

        lo, hi = self.params.get("clip", (0.0, 1.0))
        tension = min(hi, max(lo, tension))
        arise   = min(hi, max(lo, arise))

        # publish both namespaced and flat keys
        out = {
            "P0_ArisalTension.tension": tension,
            "P0_ArisalTension.arise":   arise,
            "tension": tension,
            "arise":   arise,
        }
        return out

    def report(self) -> Dict[str, float]:
        return {
            "tension": float(self._state["last_tension"]),
            "arise":   float(self._state["last_arise"]),
        }