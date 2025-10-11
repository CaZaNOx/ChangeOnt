# agents/co/tests/smoke_co_runner.py
"""
Run a toy 'maze' loop with synthetic observations to check wiring.
python -m agents.co.tests.smoke_co_runner
"""
import random
from agents.co.registries.factories import load_registry, get_adapter_class
from pathlib import Path
import yaml

def load_combo(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    reg = load_registry("agents/co/registries/registry.yaml")
    combo = load_combo("agents/co/combos/R6_router_full.yaml")
    Adapter = get_adapter_class(reg, combo["env_adapter"])
    agent = Adapter(combo, registry_path="agents/co/registries/registry.yaml")
    agent.reset(0)
    # toy stream
    state = 0
    for t in range(50):
        obs = {
            "state_token": f"s{state}",
            "valid_actions": ["L","R","U","D"],
            "base_costs": {"L":1.0,"R":1.0,"U":1.0,"D":1.0},
            "signals": {"z_PE": 0.3 if t%7==0 else 0.05, "z_gain": 0.2, "var_resid": 0.1},
        }
        a = agent.act(obs)
        # fake reward
        r = 1.0 if a in ("R","U") else 0.0
        agent.learn({"reward": r})
        state = (state + (1 if a in ("R","U") else -1)) % 7
    print("FINAL METRICS:", agent.finalize())

if __name__ == "__main__":
    main()
