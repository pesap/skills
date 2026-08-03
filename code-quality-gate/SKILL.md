---
name: code-quality-gate
description:
  Check changed code against repository guidance and canonical quality commands
  before review. Use when users ask for a quality check, conformance check,
  pre-review gate, lint/type/test validation, or whether a change follows the
  project's coding guidelines. Do not use for broad bug-finding, severity
  ranking, architecture review, or merge recommendation; use pi-review.
license: MIT
compatibility: pi
---

# Code Quality Gate

This is a conformance and validation gate, not a substitute for code review.
Determine the rules that apply to the change, run the project's authoritative
checks, and report concrete pass/fail evidence.

## Rule precedence

Apply guidance in this order:

1. Explicit user requirements for this change.
2. Repository and directory-scoped instructions (`AGENTS.md`, `CLAUDE.md`,
   contributor guides, and equivalent files).
3. Project configuration and canonical commands (formatter, linter, type
   checker, tests, build, CI configuration).
4. Relevant ADRs, domain references, and language-specific project guidance.
5. [The fallback baseline](references/baseline.md) only where applicable
   project guidance is absent.

If two authoritative sources conflict, report the conflict and do not silently
choose a rule. Treat missing guidance as a gap, not as permission to invent a
project convention.

## Workflow

1. **Scope the change.** Inspect the diff, changed files, nearby tests, and the
   repository root. Check for nested instructions that govern touched paths.
2. **Discover guidance.** Read the applicable instruction files and identify the
   project's canonical validation commands. Do not assume a generic command
   when the repository defines another one.
3. **Build a check matrix.** Record each rule or command as `pass`, `fail`,
   `not-run`, or `not-applicable`, with its source.
4. **Run deterministic checks.** Prefer the narrowest relevant formatter,
   linter, type checker, test, build, and generated-file checks. Expand to the
   project-mandated suite when required.
5. **Inspect conformance.** Check the changed code against the discovered rules,
   acceptance criteria, public contracts, and local patterns. Do not turn this
   into a broad search for unrelated bugs or design opinions.
6. **Report honestly.** Distinguish a failed check, a skipped check, an
   unavailable tool, and an ambiguous or missing rule. Never claim a pass from
   an unrun command.

## Boundary with review

- Use the repository's separate review mechanism for correctness findings,
  severity, architecture, security review, and merge recommendations.
- Apply comment-cleanup rules only for an explicit comment request or when they
  are a stated project requirement.
- Apply NASA/JPL rules only when safety-oriented discipline is explicitly
  requested.

## Output

```text
## Quality Gate: Pass | Needs fixes | Blocked

### Guidance applied
- Source: rule or convention
- Scope: files/directories covered

### Checks
- [pass|fail|not-run|not-applicable] Rule or command
  Evidence: ...

### Unresolved guidance
- Missing, conflicting, or unavailable project information

### Validation
- Command: ...
- Result: ...
```

`Needs fixes` means an applicable rule or required check failed. `Blocked` means
required guidance, tooling, credentials, or environment state prevented a
meaningful check. Do not use severity labels.
