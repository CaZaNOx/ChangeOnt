# H_ID

## Purpose

H_ID is the **identity-biased header**.

Its role is to provide a control mode in which persistence / sameness / stable identity criteria are weighted more strongly in runtime deployment.

---

## Header Role

H_ID is a **header**, not:
- a primitive
- a semantic combinator
- an element
- a translator

It belongs to the control/deployment layer.

Its role is to bias control toward stronger identity-preserving interpretation where appropriate.

---

## Inputs

H_ID may consume:
- identity-related canonical signals
- bounded internal state
- update-pass observation/feedback context

Typical relevant signals may include:
- `EC_Identity.same`
- `EC_Identity.last_d`
- closure/group-related hints if explicitly wired

---

## Outputs

H_ID may expose:
- identity-sensitive control settings
- effective thresholds or control weights
- conservative sameness-biased runtime posture

These outputs affect deployment and blending, not direct action semantics.

---

## State Mutation

H_ID may mutate only on the **update pass**.

This is binding.

---

## Why this header exists

Different task situations may call for different control emphases.

Some local regimes plausibly benefit from stronger identity-preserving interpretation, for example when:
- continuity matters more than novelty
- stable regime exploitation is favored
- reinterpretation should be dampened

H_ID is the explicit control mode for that posture.

---

## What H_ID is not

H_ID is not:
- the identity primitive itself
- the identity element itself
- a translator rule
- a direct action chooser

It is an internal control emphasis.

---

## Forbidden

H_ID must not:
- update on decision pass
- directly choose actions
- silently redefine `EC_Identity`
- contain hidden task-specific logic

---

## Telemetry

H_ID may influence:
- header debug fields
- control-mode traces
- effective identity-sensitive control state if logged

---

## Current Status

H_ID is a valid header class even if its exact formula remains provisional.

Its architectural role is stable:
- identity-sensitive internal control header