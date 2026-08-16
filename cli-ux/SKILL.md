---
name: cli-ux
description:
  Design, review, or improve command-line interfaces for strong UX,
  accessibility, composability, and automation. Use for command trees, flags,
  help, onboarding, errors, streams, exit codes, progress, color, completions,
  non-interactive modes, screen readers, and CLI best practices. Do not use for
  full-screen TUI design or shell implementation with no CLI surface change.
license: MIT
---

# CLI UX

Treat arguments, streams, output formats, errors, and exit codes as a public
interface for both people and automation.

## Core contract

1. Start from the terminal user journey: install, discover command name,
   tab-complete, run first command, ask for help, then compose/automate.
2. Optimize time-to-value: show likely first commands, concise examples, and
   next steps before exhaustive docs.
3. Provide `-h`/`--help` on the main command and subcommands; keep help fast,
   predictable, searchable, and example-rich.
4. Use familiar names and a consistent command tree so users can guess commands
   from prior commands.
5. Treat CLI arguments as a public API: avoid breaking changes; document
   unstable human output versus stable machine/porcelain output.
6. Validate input early and make errors human-readable: what happened, why,
   likely owner, how to fix, and where to get details.
7. Use streams correctly: data on stdout, diagnostics on stderr, accept stdin
   where useful, and return meaningful exit codes.
8. Keep non-interactive mode first-class. Interactive prompts can guide humans,
   but must not replace flags/config for automation.
9. Make output accessible by default: boring, linear, grepable,
   screen-reader-friendly, and useful when redirected.
10. Gate visual affordances: color only on TTY and never when `NO_COLOR`; no
    animation/spinners when not TTY, `TERM=dumb`, CI, or `--no-animation`.
11. Prefer structured output flags (`--json`, `--yaml`, or stable line formats)
    for parsing and assistive tooling.
12. For destructive operations, include dry-run/preview and explicit
    confirmation controls.

## Reference router

- Read [CLI UX principles](references/cli-ux-principles.md) when source-derived
  principles or trade-offs need more detail.
- Use `evals/trigger-prompts.json` only when tuning recognition and
  `evals/evals.json` only when grading review quality.

## Output

- CLI UX verdict.
- User journey risks and accessibility risks.
- Recommended command/help/output/error changes.
- Automation contract: streams, exit codes, structured output, non-interactive
  behavior.
- Validation plan: examples, golden output, accessibility/plain-mode checks, and
  backwards-compatibility checks.
