# docs/code_reference/coverage_checklist.md

# Documentation Coverage Checklist

This checklist is used to determine whether the documentation is complete enough to support the docs → code pipeline.

The standard is:

> The docs must capture the target state clearly enough that code misalignments can be detected and implementation can proceed against the documented should-state.

---

## A. Top-level target state

### A1. Project-level target state
- [ ] final desired state of the repo is explicitly documented
- [ ] current broken/prototype state is distinguished from target state
- [ ] `CO_full` is defined clearly
- [ ] the repo’s role as both benchmark harness and mechanism investigation harness is explicit
- [ ] extensibility target is explicit

### A2. Documentation status vocabulary
- [ ] Binding is defined
- [ ] Recommended starting point is defined
- [ ] Open design space is defined
- [ ] Experimental is defined
- [ ] Legacy / inactive is defined

---

## B. Harness and execution

### B1. Scheduler contract
- [ ] family/mode/run parallel target state is documented
- [ ] barrier behavior is documented
- [ ] allowed implementation strategies are documented

### B2. Run/mode/family/suite artifact contract
- [ ] required run artifacts documented
- [ ] required mode artifacts documented
- [ ] required family artifacts documented
- [ ] required suite artifacts documented

### B3. Plot contract
- [ ] plots required at all relevant levels documented
- [ ] semantic plot rules documented
- [ ] CO-only vs STOA-vs-CO distinction documented

### B4. Manifest/config resolution contract
- [ ] CO manifest resolution behavior documented
- [ ] no-silent-drop expectation documented

---

## C. Kernel architecture

### C1. Internal representation
- [ ] path-based internal representation documented
- [ ] time-free rule documented
- [ ] asymmetry foundational rule documented
- [ ] branch-space explicitness documented
- [ ] path-space fragment schema documented at least structurally

### C2. Header / meta-header
- [ ] distinction documented
- [ ] meta-header role documented
- [ ] header role documented
- [ ] classicality role documented
- [ ] reopening rule documented
- [ ] cadence semantics documented

### C3. Primitive/element composition
- [ ] primitive reuse rule documented
- [ ] relation-form importance documented
- [ ] weight layering documented
- [ ] group composition documented

### C4. Element output contract
- [ ] typed contribution packet documented
- [ ] mandatory fields documented
- [ ] optional fields documented
- [ ] branch-vote optionality documented

### C5. Fusion / classical collapse
- [ ] hierarchical staged fusion documented
- [ ] allowed local fusion laws documented
- [ ] classical collapse documented
- [ ] low-background monitoring documented
- [ ] reopening conditions documented

### C6. Translator boundary
- [ ] input translation documented
- [ ] output translation documented
- [ ] feedback translation documented
- [ ] bus vs final task-action distinction documented

### C7. Component classification
- [ ] core canonical kernel set documented
- [ ] canonical optional extension set documented
- [ ] experimental set documented
- [ ] legacy/inactive rule documented

---

## D. Code-reference coverage

### D1. Repo map
- [ ] top-level repo map exists

### D2. Agents
- [ ] `agents/` documented
- [ ] `agents/co/` documented
- [ ] `agents/stoa/` documented

### D3. CO subareas
- [ ] adapters documented
- [ ] translators documented
- [ ] core README documented
- [ ] engine/pipeline documented
- [ ] primitives documented
- [ ] elements documented
- [ ] combinators documented
- [ ] contracts/context documented
- [ ] logic documented
- [ ] headers documented
- [ ] integration documented
- [ ] registries documented
- [ ] combos documented
- [ ] tests documented
- [ ] utils documented

### D4. Environments
- [ ] common environment contract documented
- [ ] bandit environment docs exist
- [ ] maze environment docs exist
- [ ] renewal environment docs exist

### D5. Experiments
- [ ] experiments README documented
- [ ] suite_cli documented
- [ ] configs documented
- [ ] runners documented
- [ ] logging documented
- [ ] plotting documented

### D6. Outputs
- [ ] outputs README documented
- [ ] run artifacts documented
- [ ] summaries and plots documented

### D7. STOA details
- [ ] STOA bandit docs exist
- [ ] STOA maze docs exist
- [ ] STOA renewal docs exist
- [ ] STOA shared support docs exist

---

## E. Misalignment visibility

### E1. Detectability rule
- [ ] docs are strong enough to detect missing implementation
- [ ] docs are strong enough to detect incorrect implementation
- [ ] docs are strong enough to detect legacy drift
- [ ] docs are strong enough to detect missing artifacts/plots

### E2. Experimental boundary
- [ ] docs make it clear what may differ without counting as code misalignment
- [ ] docs make it clear what is not yet frozen

---

## F. Practical readiness

### F1. Implementation readiness
- [ ] a developer could rebuild the intended kernel loop from the docs
- [ ] a developer could rebuild the intended harness behavior from the docs
- [ ] a developer could identify whether code is aligned or not from the docs

### F2. Honest-claim readiness
- [ ] docs are strong enough to justify the phrase “CO-honest implementation” once code aligns
- [ ] docs are strong enough to justify the phrase “honest STOA comparison” once code aligns

---

## Final pass rule

The docs are complete enough for the docs → code pipeline only when all sections above are either:
- checked off,
- or explicitly documented as open design space with a deliberate status label.