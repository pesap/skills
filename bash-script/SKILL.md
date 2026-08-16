---
name: bash-script
description:
  Write, review, or harden Bash scripts for reliable team, CI, deploy, setup,
  and operator workflows. Use for strict mode, arguments, quoting, traps,
  idempotency, hostile filenames, ShellCheck fixes, or terminal UX. Do not use
  for POSIX sh, interactive shell configuration, or data-heavy automation that
  should move to a general-purpose language.
license: MIT
---

# Bash scripts

Prefer the smallest reliable script that preserves the repository's existing
shell, command, and output contracts. Decide whether Bash is still suitable
before expanding a long-lived or data-heavy script.

## Core workflow

1. Inspect the script, callers, target environments, repository guidance, and
   existing lint or test commands.
2. Identify the input, output, exit-code, side-effect, cleanup, and
   interactive/non-interactive contracts.
3. Reproduce failures before editing when practical.
4. Apply the smallest root-cause change; keep behavior idempotent where repeated
   execution is plausible.
5. Validate narrowly with `bash -n`, ShellCheck when available, and a bounded
   dry run or repository test. Exercise cleanup and failure paths when changed.

## Guardrails

- Use `#!/usr/bin/env bash` for Bash scripts. Add `set -euo pipefail` to
  non-trivial scripts, but still handle critical failures explicitly; strict
  mode is not a substitute for reasoning about command status.
- Bind positional and function arguments to named variables immediately. Quote
  expansions by default and use arrays instead of space-delimited command
  strings.
- Treat filenames as hostile data: do not parse `ls` or raw `find` output. Use
  globs, `find -exec`, or NUL-delimited input, and protect leading dashes with
  `--` or safe path prefixes.
- Use `if command; then` for command status, `[[ ... ]]` for Bash string and
  pattern tests, and `(( ... ))` for arithmetic after validating untrusted
  numeric input.
- Prefer `$(...)`, `printf`, small named functions, and lowercase locals;
  reserve uppercase names for exported environment variables.
- Use traps for temporary resources. Preserve the original exit code and make
  cleanup tolerant of partially created state.
- Send diagnostics to stderr. Gate tracing, color, animation, and prompts;
  honor TTY state, `CI`, and `NO_COLOR`, and provide flags for automation.
- Do not parse structured JSON/YAML with ad hoc text processing, read and write
  the same file in one pipeline, or use `cmd1 && cmd2 || cmd3` as general
  control flow.
- Keep privileged writes explicit; remember that `sudo cmd > file` does not
  elevate the shell redirection.
- Recommend Python or another language when the script accumulates complex data
  structures, business logic, deep control flow, or fragile quoting.

## Reference router

Open only the reference whose trigger matches the task:

- [Modern Bash](references/modern-bash.md) — strict mode, cleanup, logging,
  operator UX, and deciding when to stop using Bash.
- [Bash pitfalls](references/bash-pitfalls.md) — filename handling, quoting,
  tests, pipelines, arrays, arithmetic, `sudo`, `find`, and `xargs`.
- [Bash cheatsheet](references/bash-cheatsheet.md) — function structure,
  redirection, heredocs, and debugging patterns.

Use `evals/trigger-prompts.json` for trigger tuning and `evals/evals.json` for
output-quality evaluation; do not load them during normal script work.

## Output

Report Bash suitability, the contract and safety choices that mattered, files
changed, validation commands and results, interactive/CI behavior, and any
remaining reason to migrate away from Bash.
