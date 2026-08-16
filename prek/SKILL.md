---
name: prek
description:
  Run, debug, optimize, or migrate Git hook and CI lint automation with `prek`,
  the Rust replacement for pre-commit. Use for hook installation, execution,
  updates, skip/include behavior, cache performance, migration from
  `pre-commit`, or CI wiring, even when users say only "pre-commit", "hooks",
  or "lint checks". Do not use for one-off lint/test commands with no hook
  orchestration or repository hook configuration.
license: MIT
---

# prek

Preserve hook coverage and behavior before optimizing runner performance.

## Defaults

- Prefer `prek run --all-files` in CI over `pre-commit run --all-files`.
- Keep hook definitions in existing `.pre-commit-config.yaml` unless migration
  requested.
- Use `SKIP=hook1,hook2` for temporary CI partitioning.
- Preserve behavior first when migrating from `pre-commit`; optimize only after
  matching hook coverage.

## Workflow

1. Confirm the hook entrypoint and scope: local git hooks, CI job, migration, or
   flaky hook investigation.
2. Read existing hook config and nearby CI definitions before changing commands.
3. Determine whether the task is behavioral parity, performance improvement, or
   failure diagnosis.
4. Prefer the smallest reliable change: command swap, cache fix, install step,
   or hook selection change.
5. Validate with the narrowest useful command (`prek run <hook> --all-files`
   before full runs when possible).
6. Report any intentional behavior differences from `pre-commit`.

## Common gotchas

- `prek` is a drop-in replacement for many flows, but surrounding install/cache
  steps may still be Python- or language-specific.
- CI slowdowns often come from repeated environment setup, duplicate hook runs,
  or path-agnostic jobs rather than from the hook runner itself.
- Temporary `SKIP=` usage is fine for partitioning, but leaving it baked into CI
  can silently reduce coverage.
- Migration requests should preserve existing hook semantics unless the user
  explicitly asks to prune or redesign hooks.

## Quick reference

```bash
# Install git hooks
prek install -f --install-hooks

# Run all hooks
prek run --all-files

# Run one hook
prek run ruff-check --all-files

# Skip specific hooks for one run
SKIP=julia-format,julia-lint prek run --all-files

# Update hook revisions
prek auto-update

# Validate updates in CI without rewriting files
prek auto-update --check
```

## CI guidance

- Keep hook pipeline simple: install deps once, then run `prek`.
- Split language-heavy hooks into dedicated jobs with path-based rules.
- Avoid duplicate hook execution across parallel jobs.
- Prefer read-mostly caches and a single writer job.
