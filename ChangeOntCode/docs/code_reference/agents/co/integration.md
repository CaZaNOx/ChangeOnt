# docs/code_reference/agents/co/integration.md

# CO Integration

## Purpose

`integration/` contains the assembly layer that connects:
- config,
- kernel construction,
- translators,
- adapters,
- and runner-facing execution.

---

## Why it exists

The kernel should not be constructed ad hoc inside many unrelated files.

Integration provides the controlled path from:
- configuration
to
- active runnable kernel.

---

## Main files

### `core_builder.py`
#### Role
Primary builder for active kernel assembly.

#### Why needed
Constructs the kernel from documented config/variant choices.

#### Target-state requirement
Must:
- build headers/meta-header correctly,
- build primitives/elements honestly,
- respect the real config surface,
- and avoid decorative parameters.

---

### `loader.py`
#### Role
Loader support for CO artifacts/configs.

#### Why needed
Encapsulates loading behavior instead of scattering it.

---

### `runner_shim.py`
#### Role
Runner-side bridge/shim into CO execution.

#### Why needed
Potential integration support when runners need a narrow interfacing surface.

---

### `suite_hooks.py`
#### Role
Suite-side integration hooks.

#### Important note
Must be clearly documented as:
- canonical active support,
- optional support,
- or stale/legacy if not aligned with the active suite path.

---

### `translators/`
#### Role
Boundary translation layer between task-local structures and CO kernel structures.

#### Why needed
The kernel’s internal representation is not task-local state.

Translators are the legitimate boundary operators.

---

## Translator subarea

Expected translator files include:
- bandit translator
- maze translator
- renewal translator

Each translator should document:
- what task-local inputs it reads,
- what path-space updates it emits,
- how it maps continuation surfaces back into task actions,
- and how feedback is translated back into kernel update structure.

---

## Misalignment examples

This area is misaligned if:
- builders ignore documented params,
- translators silently reduce CO to flat task-state features,
- suite hooks or alternate builders drift from the active runtime path,
- or integration files compete as hidden second runtime architectures.