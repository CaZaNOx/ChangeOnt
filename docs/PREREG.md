# Preregistration: falsifiers & thresholds

**HAQ / (a):** On the renewal / counting-gate family: phase-flip sharpness ≥ 0.85; FDR_windowed ≤ 0.20; AUReg ≤ baseline − 0.10 (absolute). Fail if any gate is missed.

**Spawn / (b):** Spawn accepted only if ΔBIC ≤ −10 and AUReg gain ≥ 0.05; otherwise falsified.

**κ / (c):** Δκ ≥ +0.10 without AUReg loss; else falsified.

**Edge-of-chaos / (d):** Keep diversity in [0.25, 0.35]; median band error ≤ 0.10; else falsified.

**Potential / (e):** Turning on warp reduces time-to-stable-loop ≥ 25% on CA/maze; else falsified.

**LLN / (f):** Drift guard satisfied for 3 windows; frequencies stabilize; else falsified.

**Density header / (g):** Must not worsen AUReg by > 0.02 in classical regime; else falsified.

**Meta-flip / (h):** Reduce median escape-time after hole by ≥ 30% without >5% thrash; else falsified.

**Complex turn / (i):** Beat straight EMA steering by ≥ 0.03 AUReg on mixed regimes; else falsified.

**Collapse header:** Mis-spec (false rigidity/flexibility) must not cause unbounded regret (bounded-regret fallback).
