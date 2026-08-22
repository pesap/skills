# Torc and Slurm

Use this reference for scheduler selection, self-contained Slurm specs, and
submission from a cluster login node.

## Login-node boundary

Login nodes are for lightweight orchestration only:

- inspect `torc`, `sbatch`, `squeue`, `sacct`, and paths;
- detect the HPC profile and inspect partitions;
- create Git refs/worktrees;
- generate or validate workflow specs; and
- submit Torc workflows.

Run `uv`, builds, dependency installation, R2X, PLEXOS, solver, and benchmark
payloads inside Torc jobs and their Slurm allocations.

Prefer the site's load-balanced login hostname. For NLR Kestrel, use
`kestrel.hpc.nlr.gov`, not `kl1`, `kl2`, or `kl3` unless explicitly requested.

## Discover the site

```bash
torc hpc detect
torc hpc partitions <profile>
```

Check the site's module setup and account policy before generating schedulers.
Use an invocation script to initialize modules in compute-node shells.

## Choose a scheduler path

### Self-contained source spec

Use this for a durable workflow modeled on `reeds_r2x.yaml`. The source YAML
contains `resource_requirements`, `slurm_schedulers`, and `schedule_nodes`
actions, so it can be dry-run locally and submitted directly:

```bash
torc create --dry-run reeds_r2x.yaml
torc submit --no-prompts \
  -o /scratch/$USER/torc-output \
  reeds_r2x.yaml
```

Set the account variable once in the spec. Use explicit `on_jobs_ready` or
`on_workflow_start` actions according to when allocations should be claimed;
use `on_workflow_complete` for scoped cleanup. Confirm the action is armed and
the workflow is schedulable with `torc create --dry-run` before submission.

For sequential parser stages that share node-local `TMPDIR`, use one scheduler
allocation for the chain and make later jobs depend on the first job's durable
output. Keep durable outputs on shared `/scratch` or `/projects`, not only in
node-local temporary storage.

### Generated site-specific spec

Use this when the source workflow intentionally has no site scheduler policy:

```bash
torc slurm generate \
  --account <account> \
  --profile <profile> \
  workflow.yaml \
  -o /tmp/workflow-slurm.yaml

torc create --dry-run /tmp/workflow-slurm.yaml
torc submit --no-prompts \
  -o /scratch/$USER/torc-output \
  /tmp/workflow-slurm.yaml
```

Keep `/tmp/workflow-slurm.yaml` separate from the source. The generated file
is disposable site configuration; the source remains the portable workflow.
Select generation options deliberately:

- `--group-by resource-requirements` when distinct resource profiles need
  separate scheduler allocations;
- `--group-by partition` when grouping by partition reduces allocations;
- `--single-allocation` only when all nodes must be reserved together; and
- `--walltime-strategy` and `--walltime-multiplier` when queue time versus
  allocation reuse is a deliberate trade-off.

For scripts, the direct pipeline is also supported:

```bash
torc slurm generate --account <account> workflow.yaml | \
  torc submit --no-prompts -o /scratch/$USER/torc-output -
```

Use the pipeline only when the generated spec does not need review or reuse.
Save the generated file when debugging scheduler mapping or preserving
submission evidence.

## Submission evidence

Record:

- `torc --version`;
- source commit and workflow path;
- account, profile, partition, and scheduler settings;
- `TORC_API_URL` when using a shared server;
- `torc submit` output directory and workflow ID; and
- generated workflow spec, if one was produced.

A successful `sbatch` or completed Slurm allocation is not a successful Torc
payload. Inspect Torc jobs/results and `job_stdio` logs before declaring the
workflow complete.

## Remote or tunneled server

When the Torc server is reachable from the submitting machine, use local Torc
commands with the full API base URL:

```bash
export TORC_API_URL=http://<host>:<port>/torc-service/v1
torc status <workflow-id>
torc workflows list
```

Do not SSH merely to run Torc status commands. Use SSH for cluster-local
scheduler state, remote worktrees, or logs that Torc does not expose.
