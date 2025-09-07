# tests/test_headers.py
from __future__ import annotations

from core.headers.meta_flip import HysteresisFlip, FlipConfig
from core.headers.collapse import CollapseHeader, CollapseConfig

def test_hysteresis_cooldown_bounds():
    cfg = FlipConfig(beta=0.5, theta_on=0.6, theta_off=0.4, cooldown_steps=5)
    hf = HysteresisFlip(cfg)
    flips = 0
    # oscillating loop_score; cooldown should cap flips
    for t in range(50):
        s = 0.8 if (t % 7 == 0) else 0.1
        prev = hf.mode
        hf.step(s)
        if hf.mode != prev:
            flips += 1
    assert flips <= 50 // cfg.cooldown_steps

def test_collapse_freeze_unfreeze():
    cfg = CollapseConfig(window=20, entropy_bits_thresh=0.2, var_rel_thresh=0.2, unfreeze_violations=2)
    c = CollapseHeader(cfg)
    # feed a stable window (all same class)
    frozen, *_ = c.update([0] * cfg.window)
    assert frozen is True
    # now inject violations; need 2 consecutive to unfreeze
    f1 = c.update([1])[0]
    f2 = c.update([0])[0]
    f3 = c.update([1])[0]
    # after sufficient violations, should unfreeze
    assert f3 is False
