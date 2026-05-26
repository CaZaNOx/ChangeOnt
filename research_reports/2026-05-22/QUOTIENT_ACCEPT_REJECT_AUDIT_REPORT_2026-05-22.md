# Quotient Accept/Reject Audit v1 — 2026-05-22

## Claim boundary

Quotient accept/reject audit only. It checks provenance visibility and obvious first-pass quotient pathologies. It is not a final quotient law, not state abstraction/bisimulation evidence, not benchmark evidence, and not a CO proof.

## Main verdict

Quotient provenance is now visible enough for first-pass audit. The capped diagnostic did not show an obvious duplicate-signature missed-quotient bug. The main remaining issue is not a detected false quotient; it is that quotienting is deliberately conservative and mostly singleton outside matched public residual profiles.

## Findings

### QAR1_PROVENANCE_NOW_VISIBLE — resolved-watchpoint

**Finding:** Quotient accept/reject reasons are now visible at relation telemetry and row-trace level.

**Evidence:** 605 accepted profiles observed across 144 full-current diagnostic steps; rejected reasons are counted as {}.

**Next action:** Keep this logging; use it during real-trace false/missed quotient calibration.

### QAR2_NO_DUPLICATE_SIGNATURE_MISSED_QUOTIENT_FOUND — passed-check

**Finding:** No obvious duplicate-profile signature with quotient_share_count=1 was found in the capped diagnostic.

**Evidence:** duplicate_signature_bug_count=0.

**Next action:** If this becomes nonzero, fix quotient grouping before any calibration.

### QAR3_CONSERVATIVE_SINGLETONS_DOMINATE — medium

**Finding:** Most accepted profiles are singleton residual profiles rather than multi-member quotient buckets. This is conservative but means quotienting is mostly a trace annotation outside the few matched-profile cases.

**Evidence:** accepted_singletons_in_trace_sample=495; possible_calibration_site_count=82.

**Next action:** Do not loosen quotienting yet; first design false-quotient/missed-quotient microcases and compare to state-abstraction/bisimulation analogues.

## Task summary

| family | mode | steps | accepted profiles | quotient rows | multi-bucket steps | rejected reasons |
|---|---|---:|---:|---:|---:|---|
| bandit | easy_public_bandit | 16 | 48 | 0 | 0 | `{}` |
| latent_mechanism | easy_visible | 14 | 52 | 30 | 12 | `{}` |
| latent_mechanism | hidden_depth2 | 16 | 55 | 24 | 10 | `{}` |
| maintenance_replacement | bandit_like | 24 | 120 | 48 | 24 | `{}` |
| maintenance_replacement | middle | 24 | 120 | 0 | 0 | `{}` |
| maintenance_replacement | renewal_like | 24 | 120 | 0 | 0 | `{}` |
| maze | static_visible_5x5 | 10 | 26 | 8 | 4 | `{}` |
| renewal | noisy_renewal | 16 | 64 | 0 | 0 | `{}` |

## Interpretation

A singleton accepted profile is not a bug: it means the branch has an auditable public residual profile, but no other current branch shares that full profile under the conservative gauge. Future work should add explicit false-quotient and missed-quotient cases before loosening bands or equivalence tolerance.
