from future import annotations
from typing import Callable, Dict, Any, Tuple
import random

def paired_mc_delta_regret(
    rollout_fn: Callable[[int, str], float],
    horizon: int = 40,
    n_pairs: int = 8,
    seed: int = 1729,
    ) -> Tuple[float, Dict[str, Any]]:
    """
    Monte-Carlo paired rollouts with shared RNG streams.
    rollout_fn(step_seed, mode) -> cumulative regret over 'horizon' (caller handles horizon).
    Modes are "EXPLORE" and "EXPLOIT".
    Returns (ΔReg = Reg_stay - Reg_flip, aux_logs)
    """
    rng = random.Random(seed)
    deltas = []
    logs = {"pairs": []}
    for i in range(n_pairs):
        s = rng.randrange(1 << 30)
        reg_explore = rollout_fn(s, "EXPLORE")
        reg_exploit = rollout_fn(s, "EXPLOIT")
        delta = float(reg_explore - reg_exploit)
        deltas.append(delta)
        logs["pairs"].append({"seed": s, "reg_explore": reg_explore, "reg_exploit": reg_exploit, "delta": delta})
        mean_delta = float(sum(deltas) / max(1, len(deltas)))
    return mean_delta, logs


from **future** import annotations  
from typing import Callable, Tuple  
import random

def paired_mc_debt(simulate: Callable[[str, int, int], float],  
horizon: int = 40,  
n_pairs: int = 8,  
base_seed: int = 1729,  
delta_reg_min: float = 0.05) -> Tuple[bool, float]:  
"""  
Monte-Carlo debt test with paired RNG:  
simulate(mode, seed, horizon) -> cumulative regret for the horizon under 'mode' in {"EXPLORE","EXPLOIT"}.  
Returns (ok, delta_reg) where delta_reg = Reg_explore - Reg_exploit.  
ok if delta_reg >= delta_reg_min.  
"""  
rng = random.Random(base_seed)  
diffs = []  
for i in range(n_pairs):  
s = rng.randint(0, 2**31 - 1)  
reg_explore = simulate("EXPLORE", s, horizon)  
reg_exploit = simulate("EXPLOIT", s, horizon)  
diffs.append(reg_explore - reg_exploit)  
delta_reg = sum(diffs) / max(1, len(diffs))  
return (delta_reg >= float(delta_reg_min), float(delta_reg))