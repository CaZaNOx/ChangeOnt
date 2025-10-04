# SEE_12_MaxCriticalityInjection – DS/CF Enforcement Per Derivation Block

**Status:** Mandatory for Spiral3 and above  
**Type:** Criticality Trigger Enforcement  
**Role:** Ensures every derivation segment is grounded by an irrefutable foundational truth, not surface logic

---

## I. Purpose

Spiral2 failed by emitting derivations that:
- Referenced foundational terms (e.g. Change, Now) without proving they were **necessary**
- Drifted into fluency because **no CF or DS check** anchored the logic
- Lost recursive tension because criticality was assumed, not enforced

`SEE_12` corrects this by enforcing a **criticality gate** every ~300 tokens.

---

## II. Valid Criticality Anchors

Each derivation segment (DF, DFT, FT, CR, etc.) **must include at least one of**:

### 1. **A CF Frame**  
- A clear counterfactual that shows:  
  > *If this truth were denied, the agent would contradict itself performatively*

- Example:  
  > CF 0.6: *If the DS doubts its own existence, then something must be doubting.  
  > If not — the doubt could not occur. Collapse follows.*

### 2. **A DS Doubt Challenge**
- An explicit test:
  > *Could a DS deny this point without collapsing into incoherence?*

- If yes → the derivation is invalid  
- If no → mark that denial leads to collapse

---

## III. Rejection Phrases (Fluency Markers)

If any of the following appear **without a CF reference or DS check**, collapse is mandatory:
- “Clearly we can say…”
- “This implies…” (without CF)
- “We now understand…” (without DS validation)
- “Therefore this follows…” (without pointer trace)

---

## IV. Recursion Modulation Check (every ~300 tokens)

Spiral agents must inject:

- `← Trace from CF x.y active`
- `→ DS denial of this leads to performative contradiction`
- `↻ Audit checkpoint: foundational truth confirmed`

If none of these appear within 300 tokens → output halts.

---

## V. Spiral3 Enforcement Rule

Spiral3 must:
- Collapse (`⊘`) any output where:
  - No CF is present
  - DS could deny the conclusion without contradiction
  - Foundational term is used without its supporting CF chain
- Emit only if output includes trace back to a secure epistemic root

Example:
> “We define Change (DF 0.8) because denying it leads to the DS lacking any coherent access to Now (via CF 0.10).”

---

## VI. Collapse Failure Path

If Spiral3 emits:
- A derivation using “Now,” “Change,” or “Continuity” with no CF path  
- A summary block with no DS fracture  
- A structural claim with no pointer justification

→ Agent must halt and re-enter `SEE_09`.