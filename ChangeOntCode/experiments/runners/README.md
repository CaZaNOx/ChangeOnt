# experiments/runners/

Canonical role: parity-preserving execution, logging, and evaluation orchestration.

Runners should not contain family-local help for CO beyond admitted interfaces.


## Maintenance/replacement runner

`maintenance_replacement_runner.py` supports:

```text
--agent random
--agent threshold
--agent threshold_opt
--agent finite_horizon_dp
--agent q_learning
--agent co
```

`finite_horizon_dp` is intentionally restricted to direct public health observation. It is not valid as a hidden-health comparator unless explicitly recast as an oracle upper bound.
