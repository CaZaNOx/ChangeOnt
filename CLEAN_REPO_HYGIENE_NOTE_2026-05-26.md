# Clean Repo Hygiene Note — 2026-05-26

This package is a root-hygiene cleanup of `ChangeOnt_domain_relative_coarseness_field_2026-05-25.zip`.

No theory, kernel behavior, tests, adapters, or experiment logic were intentionally changed in this cleanup pass.

## What changed

- Dated audit/probe/review/update artifacts were moved out of the repository root into `research_reports/<date>/`.
- `research_reports/INDEX.md` and per-date indexes were added.
- `README.md` and `NEXT_AI_START_HERE.md` were updated to point to the report archive and current snapshot name.
- Build/cache artifacts were checked and no `__pycache__`, `.pytest_cache`, or `.pyc` artifacts were retained.

## Root policy

The repository root should contain only:

- onboarding/navigation files,
- current ledgers/maps,
- package metadata,
- high-level project control files.

New dated audit reports should go under:

```text
research_reports/<YYYY-MM-DD>/
```

and `research_reports/INDEX.md` should be updated.
