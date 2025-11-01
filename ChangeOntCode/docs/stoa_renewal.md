<!-- docs/stoa_renewal.md -->
# STOA: Renewal Prediction (Phase / N-gram)

**Anchors**
- Renewal theory: age \(a\), hazard \(h(a)\), residual life.
- Phase predictor approximates \( \Pr(\text{renewal at } t+1 \mid a_t) = h(a_t) \).
- N-gram HMM surrogate captures limited memory; breaks when dependencies exceed its order.

**Expectation**
- Phase predictor accuracy vs. age tracks hazard; beats n-gram on long memory.
- Deterministic; bookkeeping invariant holds: reward==1 iff act==obs.

**Acceptance**
- Mismatch count 0.
- Accuracy curve consistent with configured hazard (qualitative overlay).
