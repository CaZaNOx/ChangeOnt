from **future** import annotations  
from typing import Dict, Any, List, Optional

from agents.co.core.compliance.anti_oracle import AntiOracle  
from agents.co.core.compliance.budget_parity import BudgetMeter

def run_pre_run_checklist(agent_name: str,  
seeds: Dict[str, int],  
precision: str,  
class_cap: int,  
context_cap: Optional[int],  
anti_oracle: AntiOracle,  
budget: BudgetMeter) -> Dict[str, Any]:  
"""  
Lightweight pre-run checklist. Returns dict with 'ok': bool and 'issues': [str].  
"""  
issues: List[str] = []

```
# Seeds present
for k in ("base", "per_episode_base", "agent_init"):
    if k not in seeds:
        issues.append(f"missing_seed:{k}")

# Precision
if precision.lower() not in ("float32", "fp32"):
    issues.append(f"precision_not_float32:{precision}")

# Caps
if class_cap > 64:
    issues.append(f"class_cap_exceeds_64:{class_cap}")
if context_cap is not None and context_cap > 64 and "transformer" in agent_name.lower():
    # parity cap for lite baseline; HAQ may not use ctx window but keep note
    issues.append(f"context_cap_exceeds_64:{context_cap}")

# Anti-oracle
if not anti_oracle.ok():
    issues.append(f"anti_oracle_violation:{anti_oracle.report()}")

# Budget sanity
b = budget.as_dict()
if b["param_bits"] <= 0 and "fsm" not in agent_name.lower():
    issues.append("params_zero_but_nontrivial_agent")
if b["flops_per_step_mean"] < 0.0:
    issues.append("negative_flops_mean")

return {"ok": len(issues) == 0, "issues": issues, "budget": b}