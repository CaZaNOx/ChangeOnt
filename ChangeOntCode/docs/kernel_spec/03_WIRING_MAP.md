# Wiring Map

This file shows the target-state wiring of the kernel and harness boundaries.

## 1. High-level wiring

### Environment side
Environment provides task-local state, legality, and feedback.

### Runner side
Runner owns family-local execution loop.

### Adapter side
Adapter bridges runner execution and CO kernel entry/update paths.

### Translator side
Translator maps:
- task-local input → path-space update
- continuation surface → concrete task action
- feedback → path-space update

### Kernel side
Kernel operates on:
- path-space fragment
- headers/meta-header
- primitives
- elements
- groups
- final fusion

---

## 2. Canonical CO wiring

1. meta-header supplies prior regime frame
2. translator produces path-space update
3. path-space fragment is assembled
4. header evaluates local runtime regime
5. primitives read the fragment
6. elements emit typed contribution packets
7. packets fuse into group outputs
8. groups fuse with:
   - header
   - meta-header
   - classical/STOA continuation stream
9. final continuation surface is produced
10. translator maps continuation surface to task action
11. runner executes action
12. feedback is translated back into kernel update form

## 3. Internal representation placement

The path-space fragment is internal to the kernel.

The translator is the boundary where:
- task-local structure enters
- and task-local action form exits

## 4. Classical stream placement

The classical/STOA continuation stream is part of the final fusion stage.

It must be explicit, not hidden in undocumented shortcuts.

## 5. Important wiring rule

The bus or continuation surface is richer than the final task action.

The kernel should not be forced to think natively in final task actions.

## 6. Misalignment examples

The wiring is misaligned if:
- translators are bypassed
- the bus is treated as the final task-action bus
- classical influence is hidden rather than explicit
- there are competing active kernel paths with no documented status