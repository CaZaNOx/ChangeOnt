# agents/co/adapters/maze_adapter.py
from typing import Any, Dict, List
import random
from ..registries.factories import load_registry, build_header, build_elements
from ..core.combinators.C_pipeline import Pipeline
from .probes import ProbesAggregator
from ..core.primitives.budget import BudgetLedger
from ..core.primitives.calibrators import RMState, rm_update

class COAgentMaze:
    def __init__(self, combo_cfg: Dict, registry_path: str = "agents/co/registries/registry.yaml"):
        self.combo = combo_cfg
        self.reg = load_registry(registry_path)
        # Header
        hname = combo_cfg["header"]["name"]
        family = combo_cfg["header"].get("static", {}).get("family", "maze")
        overrides = combo_cfg["header"].get("static", {})
        hb = build_header(self.reg, hname, family, overrides=overrides if hname != "CS" else None)
        self.header_name = hb.name
        self.math_context = hb.math_context
        self.header_state = hb.header_state
        self.guards = hb.guards

        # Elements
        elems_cfg = combo_cfg.get("elements", [])
        self.elements = build_elements(self.reg, elems_cfg)
        self.pipeline = Pipeline(self.elements)

        # Logs & utilities
        self.history: List[Any] = []
        self.alpha_series: List[float] = []
        self.metrics: Dict[str, Any] = {}
        self.probes = ProbesAggregator(window=64)
        self.budget = BudgetLedger()
        # Calibrators registry: name -> callable(theta, signal) -> (new_theta, state)
        self.rm_gamma_state = RMState(theta_min=0.0, theta_max=1.0, base_lr=0.2)
        self.rm_lambda_state = RMState(theta_min=0.0, theta_max=0.1, base_lr=0.1)
        self._last_action = None

    def reset(self, seed: int | None = None):
        if seed is not None:
            random.seed(seed)
        self.history.clear()
        self.alpha_series.clear()
        self.metrics.clear()
        self.probes = ProbesAggregator(window=64)
        self.budget = BudgetLedger()
        self.rm_gamma_state = RMState(theta_min=0.0, theta_max=1.0, base_lr=0.2)
        self.rm_lambda_state = RMState(theta_min=0.0, theta_max=0.1, base_lr=0.1)
        self._last_action = None

    def _state_in(self, observation: Dict) -> Dict:
        calibrators = {
            "gamma_rm": lambda theta, sig: rm_update(theta, sig, self.rm_gamma_state),
            "lambda_rm": lambda theta, sig: rm_update(theta, sig, self.rm_lambda_state),
        }
        self.budget.tick()
        return {
            "header_state": self.header_state,
            "math_context": self.math_context,
            "guards": self.guards,
            "history": tuple(x for x in self.history if x is not None),
            "base_costs": observation.get("base_costs", {}),
            "signals": observation.get("signals", {}),
            "probes": self.probes.probes(),
            "residuals": observation.get("residuals", {}),
            "budget": self.budget,
            "calibrators": calibrators,
        }

    def act(self, observation: Any) -> Any:
        self.history.append(observation.get("state_token"))
        self.probes.update(state_token=observation.get("state_token"))
        st = self._state_in(observation)
        out = self.pipeline.run(st)
        alpha = out.get("alpha")
        if alpha is not None: self.alpha_series.append(alpha)
        actions = observation.get("valid_actions", [])
        if not actions:
            self._last_action = None
            return None
        warped = out.get("warped_costs", observation.get("base_costs", {}))
        best = min(warped.keys(), key=lambda k: warped[k])
        self._last_action = best
        return best

    def select(self, *args, **kwargs):
        """Compatibility wrapper for runners expecting select()."""
        return self.act(*args, **kwargs)

    def learn(self, feedback: Dict):
        r = feedback.get("reward")
        if r is not None:
            self.probes.update(reward=float(r))
            # credit some budget if reward positive
            if r > 0:
                self.budget.credit(0.05)

    def finalize(self) -> Dict:
        self.metrics["alpha_series"] = list(self.alpha_series)
        self.metrics["tau"] = float(getattr(self.header_state, "tau_eff", 0.0))
        self.metrics["eps"] = float(getattr(self.header_state, "eps_eff", 0.0))
        self.metrics["header"] = self.header_name
        self.metrics["math_context"] = self.math_context.to_dict()
        self.metrics["dyn"] = float(getattr(self.header_state, "dyn", 0.0))
        self.metrics["tag"] = str(getattr(self.header_state, "tag", "CS"))
        return self.metrics
    
# ---- Back-compat aliases (legacy runner names) ----
COMazeAgent = COAgentMaze
COMazeCfg = dict  # runners may expect a cfg class; dict works as a placeholder

