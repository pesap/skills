---
name: gitlab
description: >
  Operate GitLab from the terminal with `glab`: inspect or update merge
  requests, issues, pipelines, jobs, and releases; create or debug
  `.gitlab-ci.yml`; and improve variables, rules, caches, artifacts, and CI
  performance. Use for requests such as "check this MR" or "why did the
  pipeline fail". Do not use for GitHub or deep Kubernetes-agent work.
license: MIT
---

# GitLab

Resolve the project and target first, then gather remote evidence with `glab`
before proposing or making changes.

## Task router

Open only the reference whose trigger matches the task:

- [GitLab commands](references/commands.md) — authentication, merge requests,
  issues, releases, repository operations, environment, and mutation safety.
- [Pipelines](references/pipelines.md) — run and job triage, `.gitlab-ci.yml`,
  `rules`, `needs`, cache, artifacts, matrices, and CI performance.

## Core workflow

1. Confirm project/group, MR/issue/pipeline/release target, and desired outcome.
2. Read the matching reference and inspect repository guidance or CI files that
   govern the target.
3. Gather current state with `glab` list, view, status, or API output.
4. Diagnose from concrete MR state, discussion threads, jobs, logs, artifacts,
   variables, rules, or pipeline configuration.
5. Apply the smallest reliable action or configuration change.
6. Verify with follow-up `glab` inspection or a pipeline rerun when appropriate;
   do not infer success from a mutation command alone.

## Output

Report key `glab` evidence, findings or actions, pipeline/configuration changes,
verification status, and remaining risks or next steps.
