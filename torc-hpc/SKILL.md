---
name: torc-hpc
description: >
  Design, run, debug, install, and operate Torc workflows across local,
  remote-worker, and Slurm/HPC modes. Use when a user asks about Torc workflow
  YAML, explicit files/jobs/dependencies/resources/scheduler actions, local
  smoke tests, Slurm submission, remote workers, invocation scripts,
  TORC_API_URL, logs/artifacts, exact-SHA remote runs, or HPC Git/LFS/module
  failures.
---

# torc-hpc

Use Torc as the workflow graph and scheduler boundary. Prefer a declarative
workflow whose durable files make every stage, dependency, and output visible.
For R2X-style work, the normal shape is:

```text
archive/input -> materialize -> parse -> transform -> translate -> export -> validate
```

Keep each durable system boundary as a named Torc `FileSpec`; an R2X JSON
entrypoint and its adjacent `_time_series` directory are one artifact bundle.
Put resource profiles in `resource_requirements`, scheduler policy in
`slurm_schedulers`, and allocation/cleanup behavior in `actions`. This is the
preferred pattern for reproducibility, local smoke tests, and Slurm runs.

## Choose the execution path

| Need | Path | Read next |
|---|---|---|
| Design or review a declarative workflow | Explicit file/job graph, parameters, resources, actions | [workflow-design.md](./references/workflow-design.md) |
| Install or refresh Torc | User-managed binary or site-approved installation | [local.md](./references/local.md) |
| Syntax or wrapper smoke test | `torc create --dry-run`, then standalone `torc run` | [local.md](./references/local.md) |
| Submit a self-contained Slurm workflow | Source already declares `slurm_schedulers` and `schedule_nodes` | [slurm.md](./references/slurm.md) |
| Add site-specific Slurm policy | `torc slurm generate ...` then `torc submit` | [slurm.md](./references/slurm.md) |
| Run workers over SSH | `torc remote ...` | [remote.md](./references/remote.md) |
| Run an exact code revision remotely | Git bare remote plus isolated worktree | [versioned-runs.md](./references/versioned-runs.md) |
| Clean an exact-SHA run | Temporary worktree/ref cleanup | [versioned-runs.md](./references/versioned-runs.md) |
| Diagnose a failed run | Torc state first, then scheduler and payload logs | [failure-signatures.md](./references/failure-signatures.md) |

Do not preload every reference. Read the design reference before authoring a
workflow; otherwise load only the reference for the selected mode or failure.

## Standard operating sequence

1. **Scope the mode and boundary.** Decide whether this is local execution,
   self-contained Slurm, generated Slurm, remote workers, or an exact-SHA run.
   Keep model/solver debugging separate from Torc orchestration.
2. **Design the graph before running it.** Name inputs, intermediate states,
   final artifacts, resource profiles, and cleanup scope. Use file edges rather
   than hidden ordering or live pipes.
3. **Preflight the graph.** Run `torc create --dry-run workflow.yaml`; use
   `torc -f json create --dry-run workflow.yaml` when the expanded plan needs
   machine-readable inspection. Confirm parameter expansion and job/file edges.
4. **Smoke test cheaply.** Use a unique temporary output directory and
   `torc -s --in-memory run ... --max-parallel-jobs 1` before allocating HPC
   resources. Do not use canonical artifact directories for a smoke test.
5. **Submit through Torc.** For a source spec without scheduler policy, use
   `torc slurm generate ... | torc submit --no-prompts -`. For a self-contained
   spec with explicit scheduler actions, use `torc submit --no-prompts` on the
   source spec directly and pass an explicit output directory.
6. **Inspect native state first.** Check workflow/job status, results, resource
   data, and Torc output before SSHing for cluster details. A completed Slurm
   allocation does not prove the payload succeeded.
7. **Preserve evidence and clean narrowly.** Keep logs, metadata, and requested
   outputs. Remove only run-scoped materialized data or temporary worktrees;
   never delete durable outputs as a generic cleanup step.

## Non-negotiable boundaries

- Do not run builds, dependency installs, solvers, or workload smoke tests on
  login nodes. Use login nodes for lightweight checks, Git/worktree preparation,
  and Torc/Slurm submission only.
- Keep module, conda, and site setup in an `invocation_script` or job prologue;
  do not repeat it in every command.
- Do not rely on shell forms such as `${VAR:-default}` inside workflow
  `command` or `env`. Use Torc parameters, concrete paths, or a pre-rendered
  file.
- Use durable `input_files`/`output_files` edges. For R2X, use native `-i` and
  `-o` JSON boundaries; do not add a conversion or live-pipe layer.
- Move code by Git commit/ref, not by rsyncing a whole repository. Keep large
  data on the remote filesystem and run from an exact-SHA worktree.
- Prefer site load-balanced login entrypoints. Do not hardcode a direct login
  node unless the user explicitly requests it.
- Treat helper scripts as narrow tools: `run-remote.sh` runs a command in an
  existing remote workdir; it does not synchronize or materialize a repository.

## Output

Report:

- selected Torc mode and workflow boundary;
- files/jobs/resources/actions changed or invoked;
- exact commands and relevant environment values;
- preflight or smoke-test evidence;
- blocking environment or scheduler gaps; and
- output, log, metadata, and cleanup locations.
