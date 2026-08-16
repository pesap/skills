---
name: uv
description:
  Run standalone Python scripts reproducibly with `uv run`, PEP 723 inline
  dependencies, `uv init --script`, `uv add --script`, and `uv lock --script`.
  Use when replacing `pip`/manual-venv script flows, adding script dependencies,
  locking a script, or making it executable. For package projects, follow the
  repository's existing project and package-manager conventions instead.
license: MIT
---

# uv scripts

First distinguish a standalone script from a package project. Preserve an
existing project's configured package manager and lockfile unless migration is
explicitly requested.

## Core workflow

1. Run a script with `uv run`; add `--no-project` when the script must not use or
   install the surrounding project.
2. For a repeatable standalone script, initialize PEP 723 metadata with
   `uv init --script` and add dependencies with `uv add --script`.
3. Use `uv run --with ...` only for disposable, one-off dependencies.
4. Lock repeatable resolution with `uv lock --script`; use
   `tool.uv.exclude-newer` only when the reproducibility policy requires it.
5. For an executable script, use `#!/usr/bin/env -S uv run --script`.
6. Run the script and report the Python version, project interaction, dependency
   assumptions, lock behavior, and exact result.

## Command router

Open only the command reference needed for the task:

- [`uv run`](run.md) — execution, project interaction, inline metadata, and
  temporary dependencies.
- [`uv init --script`](init-script.md) — create a standalone metadata-bearing
  script.
- [`uv add --script`](add-script.md) — add or remove inline dependencies.
- [`uv lock --script`](lock-script.md) — create and use a script lockfile.

Use `evals/trigger-prompts.json` only when tuning recognition.

## Output

Report standalone-versus-project context, commands used, validation result, and
remaining blockers or reproducibility caveats.
