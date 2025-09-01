# CO_RECURSION_PROTOCOL — How to extend without drift

When adding/changing anything:

1. **Chain mapping:** Show ID→eventlets→paths→δ→bends→τ→equivalence→Q→gauge→decision for your change.
2. **No oracles:** Explicitly certify no plant internals are read.
3. **Equivalence closure:** Identity arises from τ-equivalence; use infimum-lift; pass congruence test.
4. **Two-time-scale:** Document step-size schedule and mixing assumptions; include drift guard + sample floor.
5. **Anti-thrash:** Hysteresis/cooldowns or curvature control; bounded-regret fallback if mis-specified.
6. **Falsifier shelf:** At least one decisive falsifier per mechanism; preregister constants and pass/fail gates.
7. **Budget parity:** Match resources; count quotient bookkeeping.
8. **Stress finitude knobs:** Prove qualitative invariants persist under 0.5×/2× caps.
9. **Traceability:** Update the traceability table (Spec ID → File/Line → Test → Metric).
