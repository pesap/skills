---
name: github
description: >
  Operate GitHub from the terminal with `gh`: inspect or update pull requests,
  review threads, issues, and workflow runs; debug or optimize GitHub
  Actions, caches, artifacts, matrices, concurrency, and runners. Use for
  requests such as "check this PR", "why did CI fail", or "reply to review".
  Do not use for GitLab or GitHub App/OAuth implementation.
license: MIT
---

# GitHub

Resolve the repository and target first, then gather remote evidence with `gh`
before proposing or making changes. When outside a repository, pass
`--repo owner/repo` or use a URL.

## Task router

Open only the reference whose trigger matches the task:

- [Pull requests](references/prs.md) — PR state, checks, review-thread replies,
  creation, and verification.
- [Issues](references/issues.md) — issue creation, triage, labels, and
  parent/child relationships.
- [Workflow runs](references/runs.md) — failed-run and job-log investigation.
- [GitHub Actions](references/actions.md) — workflow YAML, caching, matrices,
  artifacts, concurrency, runners, and CI performance.
- [API patterns](references/api-patterns.md) — `gh api`, GraphQL, `--json`, and
  `--jq` when standard subcommands do not expose enough data.

Use trigger evals only when tuning recognition and `evals/evals.json` only when
grading output quality; do not load eval files during normal GitHub work.

## Core workflow

1. Confirm repository, PR/issue/run target, and desired outcome.
2. Read the matching task reference and inspect repository guidance or workflow
   files that govern the target.
3. Gather current state with structured `gh` output where available.
4. Diagnose from concrete PR state, review threads, checks, logs, artifacts,
   labels, issue context, or workflow YAML.
5. Take the smallest high-impact action: reply in-thread, update metadata,
   rerun, patch workflow configuration, or create the requested artifact.
6. Verify the remote result with a follow-up `gh` query. Do not infer success
   from a mutation command alone.

## Critical policies

- Reply to reviewer comments in their existing thread; use a general PR comment
  only when no thread exists.
- Before creating a PR, check for an open PR with the same head branch.
- Build PR bodies explicitly. Use a repository template when present, otherwise
  use [pr-template.md](pr-template.md).
- Add `Closes #N` only when the durable source issue is resolved from explicit
  instruction, an issue-numbered branch, session context, or forge evidence.
- Before claiming PR success, verify its base, commits, signature state, body,
  close marker, and checks on the remote.

## Output

Report key `gh` evidence, findings or actions, workflow changes where relevant,
verification status, and remaining risks or follow-up work.
