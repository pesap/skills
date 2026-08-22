---
name: torc
description: >
  Design, preflight, run, debug, install, and operate Torc workflows across
  local, remote-worker, and Slurm/HPC modes. Use for Torc YAML/KDL/JSON5,
  FileSpecs, job dependencies, workflow actions, resource requirements,
  parameterized R2X pipelines, invocation scripts, Slurm submission, remote
  workers, TORC_API_URL, logs/artifacts, exact-SHA remote runs, Git/LFS,
  modules, or solver workflows such as PLEXOS. Do not use for generic Slurm,
  SSH, Git, or solver/model questions without a Torc workflow.
---

# Torc

Use Torc as the graph and scheduler boundary. Prefer the smallest workflow that
solves the current problem, then add control in layers:

```text
local smoke test -> portable HPC workflow -> self-contained Slurm workflow -> exact-SHA run
```

Read only the reference for the selected mode:

| Task | Read |
|---|---|
| Design a graph or review FileSpecs/actions | `references/workflow-design.md` |
| Local run or cross-platform local workflow | `references/local.md` |
| ReEDS/R2X/PLEXOS workflow | `references/r2x.md` |
| Slurm detection, generation, or submission | `references/slurm.md` |
| SSH workers or API tunnel | `references/remote.md` |
| Exact commit, remote worktree, cleanup, or Git LFS | `references/versioned-runs.md` |
| Failure diagnosis | `references/failure-signatures.md` |

## Operating loop

1. **Identify the mode.** Choose local direct execution, self-contained Slurm,
   generated Slurm, remote workers, manual remote fallback, or an exact-SHA
   remote run. Keep payload/model debugging separate from orchestration.
2. **Inspect before editing.** Read the workflow, project instructions,
   installed Torc help, relevant references, and existing scripts.
3. **Design durable boundaries.** Name inputs, intermediate files, final
   artifacts, resources, and cleanup scope. Prefer FileSpec edges over hidden
   shell ordering. For R2X, preserve JSON plus `_time_series` sidecars.
4. **Preflight.** Run:

   ```bash
   torc create --dry-run workflow.yaml
   torc -f json create --dry-run workflow.yaml
   ```

   Check expanded counts, job names, file names, scheduler actions, and warnings.
5. **Smoke test locally.** Use a unique temporary output directory:

   ```bash
   torc -s --in-memory run workflow.yaml \
     --max-parallel-jobs 1 \
     --output-dir <unique-temporary-directory>
   ```

   Do not use canonical artifacts or shared materialized data for a smoke test.
6. **Submit only from an HPC login node.** Use `torc hpc detect` and
   `torc hpc partitions <profile>` for discovery. Use `torc submit` directly
   when the source already has `slurm_schedulers` and `schedule_nodes`; otherwise
   use `torc slurm generate` and submit the generated spec.
7. **Inspect native state first.** Check Torc status, jobs, results, resource
   data, `job_stdio`, runner logs, and scheduler records before SSH diagnostics.
8. **Report evidence.** State the mode, exact commands, files/jobs/resources/
   actions, environment, outputs/logs, and any blocker. Never claim payload
   success from dry-run or `sbatch` success alone.

## Hard boundaries

- Do not run builds, installs, R2X, PLEXOS, solvers, or workload smoke tests on
  login nodes. Login nodes are for inspection, Git/worktree setup, module
  discovery, Torc preflight, and submission.
- Keep modules, conda, site bootstrap, and dynamic interpreter selection in an
  `invocation_script` or job prologue. End wrappers with `exec "$@"`.
- Workflow `variables` use `{name}` substitution. Workflow `env` values are
  literal strings; they do not run `$(...)`, `$TMPDIR`, or other shell logic.
- Quote paths. Do not use `${VAR:-default}` in workflow commands or env values.
  For cross-platform local specs, use concrete forward-slash paths and tools
  available on the target OS; avoid Bash-only cleanup and heredocs.
- Use native command boundaries (`r2x -i/-o`), not live pipes or conversion
  wrappers. Validators read artifacts and never repair or rewrite them.
- Move code to HPC by Git commit/ref and isolated worktree, not rsyncing the
  whole repository or datasets. Keep large data on explicit remote paths.
- Prefer load-balanced login hosts. For NLR Kestrel use `kestrel.hpc.nlr.gov`,
  not `kl1`/`kl2`/`kl3`, unless the user requests otherwise.
- Treat `run-remote.sh` as a fallback command runner for an existing remote
  workdir, not as repository synchronization.
- Do not create a helper script for trivial one-command setup. Prefer a Torc
  action or direct job command; add a script only when setup is fragile,
  repeated, or needs independent testing.
- Use `--skip-version-check` only as a temporary diagnosis for mismatched Torc
  versions; fix the installation instead.

## Mode boundaries

### Local

A local-only workflow normally needs no `resource_requirements`,
`execution_config`, `slurm_schedulers`, or `schedule_nodes`. Use a Torc
workflow-start action only for trivial setup such as untarring. Actions are not
job dependency edges: if setup failure must block downstream work, use a
materialize job and a completion marker instead. See `references/local.md` and
`references/r2x.md`.

### Self-contained Slurm

Keep `resource_requirements`, `slurm_schedulers`, and matching `schedule_nodes`
in the source spec. Prefer `on_jobs_ready` tied to the allocation's root jobs;
use `on_workflow_complete` for narrowly scoped cleanup. Submit the source
spec directly after dry-run validation.

### Generated Slurm

For a portable workflow without site policy:

```bash
torc slurm generate --account <account> --profile <profile> \
  workflow.yaml -o <generated>.yaml
torc create --dry-run <generated>.yaml
torc submit --no-prompts -o /scratch/$USER/torc-output <generated>.yaml
```

Keep generated and source specs separate. Use the direct pipe only when the
scheduler output does not need review or reuse.

### Remote workers

Use Torc-native `torc remote add-workers`, `list-workers`, `run`, `status`,
and `collect-logs`. Verify worker Torc versions and the full
`TORC_API_URL` from the workers' network context before debugging payloads.

### Exact-SHA remote runs

Use the bundled scripts in this order when applicable:

1. `setup-hpc-git-remote.sh` for a bare transport repo;
2. `git push hpc ...` for the exact run ref;
3. `prepare-git-run.sh` for an isolated worktree;
4. `deploy-git-torc-slurm.sh` for direct exact-SHA submission; and
5. `cleanup-worktree.sh` after outputs are safe.

Keep logs, outputs, and metadata; remove only temporary worktrees and prune
metadata. Delete run refs only with explicit intent. Read
`references/versioned-runs.md` for commands and failure recovery.

## Bundled tooling

Use these scripts instead of rewriting their behavior:

- `doctor.sh` / `doctor.cmd` — local and optional remote preflight;
- `install-latest-torc.sh` — user-local Torc installation;
- `setup-hpc-git-remote.sh` — configure a bare Git transport remote;
- `prepare-git-run.sh` — materialize an exact-SHA worktree;
- `deploy-git-torc-slurm.sh` — submit from an exact-SHA worktree;
- `push-run-cleanup.sh` — push, prepare, orchestrate, fetch, and clean;
- `run-remote.sh` / `.cmd` — manual fallback for an existing remote workdir;
- `cleanup-worktree.sh` / `.cmd` — safe worktree cleanup.

Use the installed Torc CLI's `--help` as authoritative when this skill and
site version differ. Do not preload every reference or inspect every helper.
