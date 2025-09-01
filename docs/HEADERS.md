# Headers (regime detectors & schedulers)

## Collapse-to-classical
- Condition: $H(y\mid [x])\le 0.10$ bits and variance ratio ≤5% over W=200.
- Action: freeze gauge/merges; use a cheap classical solver; continue monitoring and auto un-freeze when breach persists twice.

## Density of change
- Breadth $b$: normalized out-degree on Q over last 200 steps.
- Depth $d$: 1 − revisit ratio; optionally cross-check with loop occupancy or mean return time. If $b\ge 0.60$ and $b\ge 1.5\,d$: loosen τ (explore). If $d\ge 0.60$ and $d\ge 1.5\,b$: tighten τ (exploit). Else mix.

## Depth↔Breadth meta-flip
- EMA on $(b-d)$ with β=0.9; trigger if $|Δ|\ge 0.20$; hysteresis 0.10; min-hold 15; cooldown 20; ≤1 flip/50 steps.

## Complex turn (continuous steering)
- Maintain a vector $z$ in the breadth–depth plane; update with step η=0.25 and momentum 0.80; snap angle to $\{0, \pi/2, \pi, 3\pi/2\}$ minimizing short-horizon regret (H=20); clip $\|z\|\le 1$.

