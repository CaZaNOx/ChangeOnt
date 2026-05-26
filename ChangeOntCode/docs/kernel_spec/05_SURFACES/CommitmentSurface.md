# CommitmentSurface

CommitmentSurface is the canonical readout surface. It expresses an earned collapse as a native action. It is not a policy head and must not choose by score-maximum selection, first-legal rescue, greedy reward, or baseline-policy rescue.

Inputs: collapse certificates, RCF field state, candidate rows, masks, and native action expression mapping.

Output: native action expression only when commitment is evidence-bearing under the current contract; otherwise a contract violation / non-evidential state must be logged.

Primary docs: `43_CANONICAL_COMMITMENT_RULE.md`, `42_CANONICAL_READOUT_AND_ACTION_SELECTION_RULE.md`, `91_EARNED_COLLAPSE_CERTIFICATE_IMPLEMENTATION.md`, `78_RUNTIME_SAFETY_AND_FALLBACK_CONTRACT.md`.
