# docs/code_reference/agents/co/combos.md

# CO Combos

## Purpose

`combos/` contains combo/kernel-configuration artifacts.

These represent grouped kernel variant definitions or older combination artifacts.

---

## Why it exists

The project needs a way to define:
- full stacks,
- reduced stacks,
- and possibly targeted variant combinations.

This area can serve that purpose if it is kept aligned with the canonical config grammar.

---

## Documentation requirement

Every combo artifact should be documented as one of:

- active canonical variant definition
- optional canonical variant artifact
- experimental variant artifact
- legacy / historical artifact

---

## Important rule

**Binding**

Combo files must not silently compete with the active canonical config path.

If `experiments/configs/co_agents/...` is the canonical active variant definition path, then `combos/` must either:
- be aligned and documented,
- or be marked historical/experimental.

---

## Misalignment examples

This area is misaligned if:
- combos imply one variant grammar while active runtime uses another,
- combo names and actual runtime behavior diverge,
- or historical combo artifacts remain undocumented as such.