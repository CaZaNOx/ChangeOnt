"""
Run a tiny CO bandit loop with a real built core to check wiring.
python -m agents.co.tests.smoke_co_runner
"""
from agents.co.integration.core_builder import build_co_core
from agents.co.adapters.bandit_adapter import COAdapterBandit


def main():
    params = {
        "header": {"type": "SSI"},
        "elements": {
            "haq": {"enabled": True, "history_len": 8, "ema_alpha": 0.2},
            "candidate_surface": {"enabled": True},
            "router": {"enabled": True},
            "commitment_surface": {"enabled": True, "eps_on_cycle": 0.02, "ngram_order": 0},
        },
        "combinator": {"order": ["haq", "candidate_surface", "router", "commitment_surface"]},
        "primitives": {"bandit_stats": {}, "signal_bus": {}, "P2": {}},
    }
    core = build_co_core(params)
    agent = COAdapterBandit(core=core, name="CO_SMOKE", n_arms=3)
    for t in range(20):
        sel = agent.select({"family": "bandit", "t": t, "n_arms": 3})
        action = int(sel["action"]) if isinstance(sel, dict) and "action" in sel else 0
        reward = 1.0 if action == 2 else 0.0
        agent.update({"action": action, "reward": reward, "done": False})


if __name__ == "__main__":
    main()
