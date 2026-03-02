# docs/code_reference/environments/README.md

# Environments Folder

## Purpose

`environments/` contains the executable task-family environments used by runners.

---

## Why it exists

The harness requires concrete worlds/tasks to execute against.

These environments are the source of:
- initial observations,
- transition results,
- feedback,
- success/failure conditions,
- task-local legality and dynamics.

---

## Runtime role

The runner constructs an environment, then repeatedly:

1. obtains initial/current local information,
2. asks a STOA or CO path for an action,
3. applies the action to the environment,
4. receives feedback,
5. continues until the run ends.

---

## Contracts

Environments must have clearly documented:
- reset semantics,
- step semantics,
- returned observation/feedback shape,
- terminal conditions,
- task-local legality constraints.

For CO runs, the translator/adapters layer decides what part of environment-local information becomes kernel-relevant path-space update structure.

---

## Documentation requirement

Each environment family should document:
- what it models,
- how reset/step work,
- what outputs are available to the runner,
- what is exposed to translators,
- what is intentionally task-local and not part of the CO internal representation.