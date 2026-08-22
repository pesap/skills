# Exact-SHA remote runs

Use Git to move code to HPC and keep data on the remote filesystem. Run jobs
from an isolated worktree for one exact commit; never run from the receiving
bare repository or a shared mutable checkout.

## Configure the bare remote

Use the site's load-balanced login hostname:

```bash
skills/torc/scripts/setup-hpc-git-remote.sh \
  --host user@kestrel.hpc.nlr.gov \
  --remote-git-dir /scratch/$USER/git/myrepo.git \
  --remote-name hpc
```

The receiving repository is bare. It is transport, not a job checkout.

## Prepare a run

Publish an exact revision and create a run-scoped worktree:

```bash
git push hpc HEAD:refs/heads/runs/<run-id>
SHA=$(git rev-parse HEAD)

skills/torc/scripts/prepare-git-run.sh \
  --host user@kestrel.hpc.nlr.gov \
  --remote-git-dir /scratch/$USER/git/myrepo.git \
  --sha "$SHA" \
  --run-root /scratch/$USER/torc-runs/<run-id>
```

The run directory contains:

```text
src/             # exact-SHA worktree
out/             # intended outputs
logs/            # intended logs
metadata.env     # resolved run metadata
```

Keep large inputs at explicit remote paths such as `/scratch/$USER/data/...` or
`/projects/team/data/...`; do not rsync the whole repository or datasets.

## Submit an exact-SHA Torc workflow

If the commit is already present in the remote bare repository, use the bundled
wrapper:

```bash
skills/torc/scripts/deploy-git-torc-slurm.sh \
  --host user@kestrel.hpc.nlr.gov \
  --remote-git-dir /scratch/$USER/git/myrepo.git \
  --sha "$SHA" \
  --run-id <run-id> \
  --workflow workflows/run.slurm.yaml \
  --torc-api-url http://torc.hpc.nrel.gov:8080/torc-service/v1 \
  --modules 'gams/51.3.0 xpressmp/9.7.0 conda/2024.06.1' \
  --remote-torc-bin /scratch/$USER/torc/0.30.3/torc
```

The wrapper verifies the worktree SHA and workflow path, checks `torc` and
`sbatch`, exports `TORC_API_URL`, and submits from the exact worktree. It does
not commit, push, install dependencies, build, or run solver payloads on a
login node.

Use `--module` repeatedly when possible. Use `--remote-torc-bin` when Torc is
not on the remote `PATH`; use `--remote-path-prefix` only for a deliberate
PATH setup.

For a lightweight repository script that submits Torc and fetches selected
artifacts in one local command, use:

```bash
skills/torc/scripts/push-run-cleanup.sh \
  --host user@kestrel.hpc.nlr.gov \
  --remote-git-dir /scratch/$USER/git/myrepo.git \
  --script scripts/submit_torc.sh \
  --out-dir ./artifacts \
  --fetch out \
  -- --workflow workflows/run.slurm.yaml
```

Use this only for orchestration. The called script must submit work to Torc;
it must not build, install, solve, or benchmark on the login node.

## Cleanup

Clean only temporary worktrees and metadata after outputs are safe. Preview
first:

```bash
skills/torc/scripts/cleanup-worktree.sh \
  --host user@kestrel.hpc.nlr.gov \
  --remote-git-dir /scratch/$USER/git/myrepo.git \
  --run-root /scratch/$USER/torc-runs \
  --run-id failed-run-1 \
  --keep current-run
```

Execute only after reviewing the dry-run output:

```bash
skills/torc/scripts/cleanup-worktree.sh \
  --host user@kestrel.hpc.nlr.gov \
  --remote-git-dir /scratch/$USER/git/myrepo.git \
  --run-root /scratch/$USER/torc-runs \
  --run-id failed-run-1 \
  --keep current-run \
  --execute
```

The helper removes only the temporary `src` worktree by default and prunes
stale worktree metadata. Keep logs, outputs, and `metadata.env`. Delete a
temporary `refs/heads/runs/...` ref only with explicit `--delete-ref` after the
run no longer needs it.

If a run fails before cleanup, remove the worktree with
`git worktree remove --force`, run `git worktree prune`, and inspect the run
metadata before deleting its ref. Do not use broad `rm -rf` against the run
parent.

## Git LFS

A plain SSH bare repository does not provide `git-lfs-authenticate`. For a
small run-critical artifact only, a narrow `.gitattributes` override can store
that path as a normal Git blob and the push can use `GIT_LFS_SKIP_PUSH=1`.
Do not broadly disable LFS for large datasets; keep those datasets remote.
