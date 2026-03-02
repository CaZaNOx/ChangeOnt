# docs/kernel_spec/16_TRANSLATOR_BOUNDARY_CONTRACT.md

# Translator Boundary Contract

## Status
- **Binding**: translators are first-class boundary operators
- **Recommended starting point**: translators map task-local input into path-space updates and path-space continuation surfaces into task actions
- **Open design space**: exact translator helper structure and family-specific optimization details

---

## 1. Principle

Translators are not trivial formatting helpers.

Translators are the boundary operators between:
- problem-local task structures,
- and the CO kernel’s problem-agnostic internal representation.

---

## 2. Input-side translator role

**Binding**

Translators must convert task-local observations/feedback into CO-facing updates to the path-space fragment.

This includes translating task-local structures into kernel-relevant forms such as:
- realized transitions,
- branch-space candidates,
- constraints,
- structural shifts,
- stabilization/destabilization signals,
- closure/opening shifts,
- confidence or precision relevant signals.

---

## 3. Output-side translator role

**Binding**

Translators must convert the CO-internal continuation surface into a concrete task action.

This is where task-local legality and action semantics are applied.

Examples:
- maze action index or move direction,
- bandit arm choice,
- renewal symbol/action class.

---

## 4. Feedback translation rule

**Binding**

Translators must also translate environment feedback back into CO-relevant update structure.

The kernel should not rely only on raw reward or raw next-state payloads.

---

## 5. Bus rule

**Binding**

The bus or fused continuation surface is richer than the final task action.

Translators are the legitimate collapse point into concrete task action space.

The kernel must not be forced to think natively in final task action tokens.

---

## 6. Misalignment examples

Code is misaligned with this spec if:
- translators only pass flat state features through unchanged,
- the kernel is forced to emit final task actions as its deepest native output,
- or feedback is not translated back into kernel-relevant structural update form.