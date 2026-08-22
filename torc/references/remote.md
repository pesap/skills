# Torc remote workers

Use Torc's remote-worker commands for SSH-accessible machines. Do not replace
them with a custom SSH loop unless the task is explicitly a manual fallback.

## Preconditions

- Torc is installed at compatible versions on the server and workers;
- passwordless SSH works without prompts;
- workers can reach the Torc server and required workflow paths; and
- the workflow has been created or submitted and has a workflow ID.

## Native worker flow

```bash
torc create workflow.yaml
torc remote add-workers <workflow-id> user@host1 user@host2
torc remote list-workers <workflow-id>
torc remote run <workflow-id>
torc remote status <workflow-id>
torc remote collect-logs <workflow-id> \
  --local-output-dir ./logs
```

Use `torc remote stop` after an intentional stop. Use
`torc remote delete-logs` only when remote logs are no longer needed; collecting
logs does not clean worker binaries or repository state.

If workers disappear immediately, inspect `torc remote status`, worker logs,
server reachability, SSH startup, and version compatibility before debugging
the workflow payload. `--skip-version-check` is a temporary diagnostic escape
hatch, not a permanent fix.

## API URL

Use the full Torc API base path, for example:

```bash
export TORC_API_URL=http://torc.example.org:8080/torc-service/v1
torc status <workflow-id>
```

Verify the URL from the same network context used by the workers. A local
client reaching the server does not prove that workers can reach it.

## Environment setup

Use the workflow's `invocation_script` for modules, conda, and site-specific
variables. Avoid relying on an interactive login shell on a worker. Test the
script with a small command and record the resolved Torc version and module
list.

## Manual fallback

Use `skills/torc/scripts/run-remote.sh` only for a non-Torc command that
must run in an already prepared remote workdir:

```bash
skills/torc/scripts/run-remote.sh \
  --host user@cluster \
  --remote-root /scratch/$USER/torc-runs \
  --workdir /projects/repo/exact-worktree \
  --command 'bash scripts/check.sh' \
  --out-dir ./artifacts \
  --fetch output/summary.json \
  --fetch output/summary_time_series
```

When the fetched output is an R2X system, request the JSON entrypoint and its
adjacent `<stem>_time_series/` directory as a pair. Do not collect only the
entrypoint.

The helper creates run state, waits for an exit code, and fetches requested
paths/logs. It does not sync the repository, create a worktree, install Torc,
or run solver/build payloads on a login node. Prepare the exact worktree first;
use [versioned-runs.md](./versioned-runs.md) for that workflow.
