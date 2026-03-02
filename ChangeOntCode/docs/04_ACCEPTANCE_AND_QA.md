# Acceptance and QA

This file defines what counts as acceptable target-state behavior.

## 1. Acceptance scope

Acceptance is not only about:
- “it runs”

Acceptance must also include:
- semantic correctness
- required artifacts
- correct plotting
- correct summary semantics
- honest CO wiring
- honest STOA comparison
- documentation completeness sufficient for docs → code implementation

## 2. Run acceptance

A run is acceptable only if:
- it terminates or reaches its documented stopping condition
- required run artifacts are present
- run status reflects reality
- metrics are family-appropriate
- quick plot exists
- manifests/provenance are coherent

## 3. Mode acceptance

A mode summary is acceptable only if:
- all required runs for the mode are complete
- mode summary CSV exists
- mode plot(s) exist
- labels are correct
- summary semantics are honest

## 4. Family acceptance

A family summary is acceptable only if:
- all required modes are complete
- combined summary exists
- family plot(s) exist
- family-level aggregation semantics are correct

## 5. Suite acceptance

A suite is acceptable only if:
- all intended families are complete
- suite summary files exist
- suite plot(s) exist
- CO-only outputs exclude STOA rows
- STOA-vs-CO outputs use compatible metrics
- agent identity normalization is consistent
- provenance/failure outputs exist or are explicitly accounted for

## 6. CO-honesty acceptance

The implementation should not be called a CO-honest implementation unless:
- the internal representation is path-based and time-free
- translators are first-class and real
- header/meta-header roles are real
- elements and primitives are wired honestly
- classicality is treated as regime-conditioned collapse
- decorative parameters and dead config surfaces are removed or documented
- summary outputs do not misrepresent CO behavior

## 7. Smoke acceptance

A canonical smoke path should:
- complete quickly
- not hang indefinitely
- include at least one representative CO run
- include at least one representative STOA run
- produce required artifacts

If the nominal demo suite hangs, it is not an acceptable smoke path.

## 8. Documentation completeness acceptance

Documentation is acceptable only if:
- the target-state contracts are explicit
- status labels are used honestly
- the docs support misalignment detection
- the code-reference layer covers all major folders/subsystems
- the kernel-spec layer captures the actual intended should-state

## 9. QA priorities

The highest-priority QA checks are:
1. no indefinite hangs in canonical smoke paths
2. required artifacts at every level
3. semantically correct suite summaries
4. honest CO manifest resolution
5. honest header/classicality behavior
6. consistent identity normalization