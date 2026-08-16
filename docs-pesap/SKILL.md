---
name: docs-pesap
description:
  Create or revise accurate, task-oriented READMEs, API documentation,
  tutorials, how-to guides, explanations, setup, troubleshooting, migration,
  release notes, and GitHub Markdown. Use when documentation must be grounded
  in repository code and runnable commands rather than marketing copy.
license: MIT
---

# Documentation

Write the shortest complete path that lets the intended reader achieve a real
outcome and verify it. Treat implementation, public APIs, configuration, tests,
CI, and established project terminology as the source of truth.

## Choose the document shape

| Reader need | Shape | Keep it focused on |
|---|---|---|
| Learn by completing a guided example | Tutorial | A narrow path to a working result |
| Accomplish a known task | How-to | Prerequisites, actions, verification, recovery |
| Look up exact behavior | Reference | Contracts, options, defaults, errors, compatibility |
| Understand concepts or trade-offs | Explanation | Rationale, architecture, and behavior |

Split conflicting modes into linked pages instead of making one page serve all
four.

## Core workflow

1. Identify the reader, desired outcome, document shape, and success check.
2. Inspect the implementation, public contract, configuration, scripts, tests,
   CI, existing terminology, and related docs before writing.
3. Verify every command, flag, path, version, output, and behavior claimed.
4. Write prerequisites before actions and place validation immediately after
   the action it verifies. Include recovery where failure is plausible.
5. Use typed, copy-pasteable examples with realistic placeholders. Do not invent
   APIs or filenames; prefix expected shell output with `#` when it shares a
   command block.
6. Validate links, anchors, examples, commands, generated references, rendering,
   and repository documentation checks where available.

Label unverifiable assumptions or omit them. Never present stale or uncertain
instructions as authoritative.

## Reference router

Open only the reference whose trigger matches the task:

- [README guidance](references/readmes.md) — project entry points, quickstarts,
  success checks, and the learning ladder.
- [API documentation](references/api-docs.md) — public contracts, errors,
  side effects, limits, and generated references.
- [GitHub Markdown](references/github-markdown.md) — headings, links, alerts,
  collapsed sections, tables, diagrams, badges, and accessible rendering.
- [Documentation testing](references/documentation-testing.md) — executable
  examples, vocabulary guards, fixtures, and docs CI.

## Completion gate

Confirm that the reader can complete the task in one pass; claims and examples
match source truth; prerequisites, permissions, side effects, and recovery are
explicit; links and rendering validate; and no filler, marketing claims, hidden
steps, or unsupported certainty remain.

## Output

Report files and sections changed, reader/outcome/document shape, source-of-truth
files consulted, validation commands and results, and any remaining assumptions
or documentation gaps.
