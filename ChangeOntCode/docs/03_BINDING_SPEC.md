# Binding Spec (Code Contracts)

This page defines binding contracts for the canonical runtime (adapters → pipeline → ActionHead). Keep it unambiguous and in sync with code.

## 1) Observation envelope (adapter → kernel)
All CO adapters must provide an observation dict with these **required keys**:
- `family: str` — lower-case family name (`"bandit"`, `"maze"`, `"renewal"`)
- `t: int` — step index within the episode/run

Standard optional keys (use when available):
- `episode: int` — episode index
- `feedback: dict` — outcome feedback (reward, done, etc.)
- `translator_mask: list` — blocklist of forbidden actions (if provided by runner)
- `residuals: dict`, `probes: dict` — diagnostics for GHVC / change detection
- `history: list`, `trace: list` — short action/observation traces for identity

**Rule:** adapters must not inject hidden env state beyond what the runner already exposes.

### Current implementation detail (per-family fields)
Per-family observation fields are defined by translator expectations and runners, not by this contract. For current expectations, see:
- `agents/co/integration/translators/bandit_translator.py`
- `agents/co/integration/translators/maze_translator.py`
- `agents/co/integration/translators/renewal_translator.py`

## 2) Mask contract (translator → ActionHead)
- Translators return a `translator_mask` **blocklist** (set of forbidden actions).
- ActionHead removes any masked actions **from CO scores** before blending.
- ActionHead does **not** currently apply the mask to classical scores. If you need a hard blocklist across all paths, update ActionHead accordingly.

## 3) Vote bus vs scalar signal contract
- **Votes:** elements publish votes to `co_bus.push(family, action, weight, ...)`.
  - ActionHead drains votes once per decision via `co_bus.drain(family)`.
- **Scalar signals:** elements publish scalar telemetry to `co_bus.set(key, value)` (or `bus[key] = value`).
  - Naming convention: `ElementName.field`, e.g., `EC_Identity.last_d`, `EB_GHVC.pressure`.

## 4) Header update ownership
- Decision pass (`C_Pipeline.run`) must **not** update header state.
- Learning pass (`C_Pipeline.run_update`) owns `header.update(...)` and uses feedback.

## 5) Required telemetry keys (QA-aligned)
QA reads `metrics.jsonl` and expects these fields when present:

Signals dict keys:
- `signals["EC_Identity.same"]`
- `signals["EC_Identity.last_d"]`
- `signals["EB_GHVC.pressure"]`
- `signals["EB_GHVC.mdl_gain"]`
- `signals["EB_GHVC.birth_suggest"]`

Other keys (if present in records):
- `header_update_count`
- `header_update_source`
- `mask_mode`
- `translator_mask`
- `birth_count`

## 6) No alternate runtime semantics
There must be exactly one canonical runtime semantics: adapters → `C_Pipeline.run/run_update`. Do not create alternate runtime loops or bypass ActionHead.

