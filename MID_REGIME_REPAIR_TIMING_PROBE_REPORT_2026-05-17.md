# Mid-Regime Repair-Timing Probe — 2026-05-17

## Scope

This probe follows the focused maintenance failure analysis. It does not tune the kernel and does not claim reward evidence. It asks a narrow structural question:

```text
When observed health is moderately degraded, when should CO continue RUN-through-carrier-burden and when should it prefer REPAIR as an adequate resolver?
```

Two probe families were run:

1. adapter-public observations at `observed_health = 2`, varying public degradation, public failure penalty, repair cost, and observation noise;
2. hand-built synthetic cases varying RUN carrier pressure, REPAIR resolver magnitude, and REPAIR local visible support.

## Adapter-public sweep summary

```json
{
  "cases": 252,
  "high_risk_run_case_count": 0,
  "sample_high_risk_run_cases": [],
  "selected_actions": {
    "INSPECT": 208,
    "REPAIR": 20,
    "RUN": 24
  },
  "selected_actions_by_degradation": {
    "0.05": {
      "INSPECT": 24,
      "RUN": 12
    },
    "0.10": {
      "INSPECT": 24,
      "RUN": 12
    },
    "0.20": {
      "INSPECT": 32,
      "REPAIR": 4
    },
    "0.30": {
      "INSPECT": 32,
      "REPAIR": 4
    },
    "0.45": {
      "INSPECT": 32,
      "REPAIR": 4
    },
    "0.60": {
      "INSPECT": 32,
      "REPAIR": 4
    },
    "0.75": {
      "INSPECT": 32,
      "REPAIR": 4
    }
  },
  "selected_actions_by_failure_penalty": {
    "12.0": {
      "INSPECT": 52,
      "REPAIR": 5,
      "RUN": 6
    },
    "2.0": {
      "INSPECT": 52,
      "REPAIR": 5,
      "RUN": 6
    },
    "5.0": {
      "INSPECT": 52,
      "REPAIR": 5,
      "RUN": 6
    },
    "8.0": {
      "INSPECT": 52,
      "REPAIR": 5,
      "RUN": 6
    }
  },
  "selected_actions_by_repair_cost": {
    "0.40": {
      "INSPECT": 56,
      "REPAIR": 20,
      "RUN": 8
    },
    "0.80": {
      "INSPECT": 76,
      "RUN": 8
    },
    "1.20": {
      "INSPECT": 76,
      "RUN": 8
    }
  }
}
```

## Synthetic pressure-matrix summary

```json
{
  "cases": 144,
  "first_repair_resolver_magnitude_by_carrier_and_repair_visible": {
    "carrier=0.20;repair_visible=0.40": null,
    "carrier=0.20;repair_visible=0.48": null,
    "carrier=0.20;repair_visible=0.56": null,
    "carrier=0.20;repair_visible=0.64": null,
    "carrier=0.35;repair_visible=0.40": null,
    "carrier=0.35;repair_visible=0.48": null,
    "carrier=0.35;repair_visible=0.56": null,
    "carrier=0.35;repair_visible=0.64": 0.08,
    "carrier=0.50;repair_visible=0.40": 0.35,
    "carrier=0.50;repair_visible=0.48": 0.35,
    "carrier=0.50;repair_visible=0.56": 0.35,
    "carrier=0.50;repair_visible=0.64": 0.08,
    "carrier=0.65;repair_visible=0.40": 0.35,
    "carrier=0.65;repair_visible=0.48": 0.35,
    "carrier=0.65;repair_visible=0.56": 0.08,
    "carrier=0.65;repair_visible=0.64": 0.08,
    "carrier=0.80;repair_visible=0.40": 0.35,
    "carrier=0.80;repair_visible=0.48": 0.35,
    "carrier=0.80;repair_visible=0.56": 0.08,
    "carrier=0.80;repair_visible=0.64": 0.08,
    "carrier=1.00;repair_visible=0.40": 0.5,
    "carrier=1.00;repair_visible=0.48": 0.5,
    "carrier=1.00;repair_visible=0.56": 0.08,
    "carrier=1.00;repair_visible=0.64": 0.08
  },
  "sample_strong_pressure_nonrepair_cases": [],
  "selected_actions": {
    "REPAIR": 73,
    "RUN": 71
  },
  "selected_actions_by_carrier_and_repair_visible": {
    "carrier=0.20;repair_visible=0.40": {
      "RUN": 6
    },
    "carrier=0.20;repair_visible=0.48": {
      "RUN": 6
    },
    "carrier=0.20;repair_visible=0.56": {
      "RUN": 6
    },
    "carrier=0.20;repair_visible=0.64": {
      "RUN": 6
    },
    "carrier=0.35;repair_visible=0.40": {
      "RUN": 6
    },
    "carrier=0.35;repair_visible=0.48": {
      "RUN": 6
    },
    "carrier=0.35;repair_visible=0.56": {
      "RUN": 6
    },
    "carrier=0.35;repair_visible=0.64": {
      "REPAIR": 6
    },
    "carrier=0.50;repair_visible=0.40": {
      "REPAIR": 3,
      "RUN": 3
    },
    "carrier=0.50;repair_visible=0.48": {
      "REPAIR": 3,
      "RUN": 3
    },
    "carrier=0.50;repair_visible=0.56": {
      "REPAIR": 3,
      "RUN": 3
    },
    "carrier=0.50;repair_visible=0.64": {
      "REPAIR": 6
    },
    "carrier=0.65;repair_visible=0.40": {
      "REPAIR": 3,
      "RUN": 3
    },
    "carrier=0.65;repair_visible=0.48": {
      "REPAIR": 3,
      "RUN": 3
    },
    "carrier=0.65;repair_visible=0.56": {
      "REPAIR": 6
    },
    "carrier=0.65;repair_visible=0.64": {
      "REPAIR": 6
    },
    "carrier=0.80;repair_visible=0.40": {
      "REPAIR": 3,
      "RUN": 3
    },
    "carrier=0.80;repair_visible=0.48": {
      "REPAIR": 3,
      "RUN": 3
    },
    "carrier=0.80;repair_visible=0.56": {
      "REPAIR": 6
    },
    "carrier=0.80;repair_visible=0.64": {
      "REPAIR": 6
    },
    "carrier=1.00;repair_visible=0.40": {
      "REPAIR": 2,
      "RUN": 4
    },
    "carrier=1.00;repair_visible=0.48": {
      "REPAIR": 2,
      "RUN": 4
    },
    "carrier=1.00;repair_visible=0.56": {
      "REPAIR": 6
    },
    "carrier=1.00;repair_visible=0.64": {
      "REPAIR": 6
    }
  },
  "strong_pressure_nonrepair_case_count": 0
}
```

## Interpretation

This probe now serves as a regression check for the generic shape-gauged resolver-timing law.  The earlier version exposed high-risk RUN-through-carrier-burden cases.  The current runtime no longer treats formal certificate blocking as the only way a resolver can matter: sufficiently urgent public shape plus carried burden plus an adequate resolver relation can bend commitment before blockage.

This is not a maintenance threshold rule.  The runtime does not read `observed_health <= 2` and does not prefer the native action name `REPAIR`.  It reads generic public structure:

```text
carrier-only pressure
resolver support
local problem-shape gauge
support/score gap
```

The synthetic matrix is retained to ensure the rule is not a universal resolver bonus: both RUN-through-burden and REPAIR-as-resolver choices must remain possible depending on pressure, adequacy, and gauge.

## Current watchpoint

```text
The shape-gauged timing constants are behavior-affecting provisional coefficients.
They are now documented formula-ledger items and must remain frozen for empirical tests.
```
