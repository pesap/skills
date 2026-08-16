# GitLab pipelines

Use this reference for pipeline/job failures, `.gitlab-ci.yml`, variables,
`rules`, `needs`, caches, artifacts, matrices, and performance work.

## Contents

- [Triage loop](#triage-loop)
- [Pipeline graph](#pipeline-graph)
- [Artifacts and cache](#artifacts-and-cache)
- [Parallel variants](#parallel-variants)
- [Variables and safety](#variables-and-safety)

## Triage loop

1. Identify the pipeline, ref, source, failed job, and expected behavior.
2. Inspect status and bounded logs before editing YAML.
3. Separate runner/environment failures from job-command and pipeline-graph
   failures.
4. Make the smallest correction, lint the configuration, and rerun only the
   necessary job or pipeline when possible.
5. Verify the new remote state and preserve the failing evidence in the report.

```bash
glab ci status
glab ci list
glab ci get
glab ci trace <job-id>
glab ci retry <job-id>
glab ci lint
glab ci run
```

Run `glab ci <command> --help` for version-specific flags. Prefer structured or
bounded output when available; avoid loading every job log by default.

## Pipeline graph

- `stages` orders stages; jobs in a stage can run in parallel.
- `needs` expresses the real DAG and can start jobs before prior stages finish.
- `rules` decides whether a job exists and when it runs; check
  `CI_PIPELINE_SOURCE`, branch/tag conditions, and `changes` together.
- `include` and CI components can hide effective configuration. Inspect merged
  configuration before assuming the root file owns a job.
- Add `interruptible` or workflow-level cancellation where obsolete pipelines
  should stop.
- Add job timeouts and keep cheap, high-signal checks early.

## Artifacts and cache

Use artifacts for outputs consumed by later jobs or humans. Use cache for
reusable dependencies that are safe to regenerate.

```yaml
build:
  script: make build
  artifacts:
    paths: [dist/]
    expire_in: 1 hour

test:
  needs: [build]
  script: make test
```

For caches, key from the dependency inputs and separate incompatible platforms
or toolchains. `cache:key:files` accepts at most two files; use `prefix` for
additional context. Avoid broad branch-only keys when dependency files can
provide deterministic invalidation.

```yaml
test:
  cache:
    key:
      files: [package-lock.json]
      prefix: node
    paths: [node_modules/]
  script:
    - npm ci
    - npm test
```

Do not cache credentials, mutable deployment state, or artifacts whose stale
reuse can hide correctness failures.

## Parallel variants

```yaml
test:
  parallel:
    matrix:
      - PYTHON: ["3.10", "3.11", "3.12"]
  image: python:$PYTHON
  script: pytest
```

Keep the matrix limited to compatibility dimensions that provide distinct
signal. Use path or rules-based selection for expensive language-specific jobs,
and avoid running the same lint or test coverage in multiple jobs.

## Variables and safety

Common context includes `CI_COMMIT_BRANCH`, `CI_COMMIT_SHA`,
`CI_PIPELINE_SOURCE`, `CI_PROJECT_NAME`, `CI_JOB_TOKEN`, and
`GITLAB_USER_LOGIN`. Confirm availability for the current pipeline source;
protected variables are not necessarily exposed to merge-request pipelines.
Never echo secrets or place them in artifacts or caches.

Canonical references: <https://docs.gitlab.com/ci/> and
<https://docs.gitlab.com/ci/yaml/>.
