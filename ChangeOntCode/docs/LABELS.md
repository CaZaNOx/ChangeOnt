# LABELS — SpecCard IDs and Legacy Mapping

SpecCard ID Schema
CO.<Tier>.<Area>.<Name>@vX.Y
Examples
• CO.K1.Identity.Rtau@v0.2
• CO.K2.Lift.Witness@v0.2
• CO.K3.Headers.Collapse@v0.2

Tiers
• K* — Kernel (contract).
• E* — Extensions (hypotheses until promoted).

Legacy Mapping (to be completed as you finalize)
Old label → SpecCard ID
• core a  → CO.K1.Identity.Rtau@v0.2          (detectability, tolerance, closure start)
• core b  → CO.K1.Identity.Closure@v0.2       (deterministic closure with witnesses)
• core c  → CO.K2.Lift.Witness@v0.2           (infimum-lift with chaining)
• core d  → CO.K3.Headers.Collapse@v0.2       (collapse to classical)
• core e  → CO.K3.Headers.LoopEMA@v0.2        (loop score EMA)
• core f  → CO.K3.Headers.Hysteresis@v0.2     (flip gate with cooldown)
• core g  → CO.K4.Gauge.RM@v0.2               (Robbins–Monro gauge update)
• core h  → CO.K5.Logic.Base@v0.2             (3-valued logic tables over Q)
• core i  → CO.E.Headers.Harm@v0.1-HYP        (harm-legitimated edits; extension)

Note
If your historical a…i differ, adjust the mapping table here without changing the SpecCard schema.
