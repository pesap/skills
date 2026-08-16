# Torc workflow design

Use this reference before authoring or materially changing a workflow. The
objective is a reviewable, reproducible graph rather than a long shell script.

## Declare the graph in dependency order

Keep the specification easy to scan in this order:

1. `name`, `description`, and `project`;
2. `variables` or `parameters`;
3. `enable_ro_crate` and `execution_config` when needed;
4. durable `files`;
5. `resource_requirements`;
6. `jobs`; and
7. Slurm schedulers and lifecycle `actions`.

A reviewer should be able to trace every job from an input file to a durable
output without reading command implementation details.

## Prefer durable FileSpecs

Give each input, marker, intermediate state, and final artifact a stable file
name. Connect jobs with matching `input_files` and `output_files`; do not hide
dependencies in shell ordering.

```yaml
files:
  - name: raw_archive
    path: data/artifacts/input.tar.gz
  - name: input_ready
    path: data/materialized/.input-ready.json
  - name: parsed_system
    path: artifacts/run/parsed-system.json
  - name: exported_xml
    path: artifacts/run/model/model.xml
```

For an R2X `System`, the JSON file and adjacent
`<stem>_time_series/` directory form one co-located bundle. Declare the JSON
entrypoint as the Torc `FileSpec`, but treat the sidecar as part of the same
output contract:

- the producer must create both paths under the same parent and stem;
- every downstream job, remote worktree, and artifact collection must move or
  fetch the JSON and sidecar together;
- validators must check the entrypoint and sidecar contents, not just JSON
  existence; and
- cleanup may remove the sidecar only when it removes the whole run-scoped
  bundle after durable outputs are preserved.

The FileSpec is the dependency edge; it is not permission to omit the sidecar.
For example, a remote collection should request both
`parsed-system.json` and `parsed-system_time_series/` rather than fetching only
the entrypoint.

Use parameters for matrix rows and include the parameters that affect a
FileSpec or command:

```yaml
parameters:
  scenario: [A1, A2, A3]
  solve_year: [2050]

files:
  - name: parsed_{scenario}_{solve_year}
    path: artifacts/{scenario}/{solve_year}/parsed-system.json
    use_parameters: [scenario, solve_year]
```

Use one durable marker only when a side effect needs an explicit completion
edge, such as archive materialization. A marker must be created last, after
verification succeeds.

## Make each stage a job

A job should have one concern and one reviewable boundary. Typical R2X stages
are materialize, parse, apply defaults, disaggregate, translate, export, and
read-only validate. Name stages with the domain operation, not generic
`step1`/`step2` labels.

```yaml
jobs:
  - name: parse_reeds
    command: >-
      r2x run r2x-reeds.reeds-parser
      -o "${files.output.parsed_system}"
      path="{materialized_dir}"
      solve_year=2050
      weather_year=2012
      case_name=geothermal
      scenario=base
    input_files:
      - input_ready
    output_files:
      - parsed_system
    resource_requirements: parse

  - name: validate
    command: >-
      uv run --script scripts/validate_files.py
      --output "artifacts/run"
    input_files:
      - parsed_system
      - exported_xml
    resource_requirements: validation
```

For R2X, pass durable JSON between jobs with the plugin's native `-i`/`-o`
arguments. Do not use a live pipe, temporary conversion format, or a wrapper
that copies a system bundle without preserving its time-series sidecar.
Validation jobs must read artifacts and report failures; they must not repair,
rewrite, or silently replace them.

Keep commands deterministic:

- quote paths containing parameters or spaces;
- use explicit flags and values instead of relying on shell defaults;
- make cleanup paths narrowly scoped; and
- keep environment setup in `invocation_script` or a job prologue.

## Separate portable resources from site scheduling

Declare portable job needs once:

```yaml
resource_requirements:
  - name: parse
    num_cpus: 4
    num_gpus: 0
    num_nodes: 1
    memory: 16g
    runtime: PT2H
  - name: validation
    num_cpus: 2
    num_gpus: 0
    num_nodes: 1
    memory: 8g
    runtime: PT1H
```

Use `slurm_schedulers` for account, node, memory, and walltime policy. Do not
repeat scheduler details in every job command. Select a scheduler by the
workflow's scheduling action and keep resource requirements on the jobs.

## Use direct execution for explicit HPC specs

For a workflow that already knows its scheduler policy, keep direct execution
and lifecycle actions in the same source spec:

```yaml
execution_config:
  mode: direct
  limit_resources: true
  termination_signal: SIGTERM
  sigterm_lead_seconds: 30

slurm_schedulers:
  - name: parser_scheduler
    account: "{hpc_account}"
    nodes: 1
    mem: 16G
    walltime: "02:30:00"

actions:
  - trigger_type: on_jobs_ready
    action_type: schedule_nodes
    jobs:
      - parse_reeds
    scheduler: parser_scheduler
    scheduler_type: slurm
    num_allocations: 1
```

The important design is that the source spec contains both the scheduler and
the action, so it can run locally for a dry run and be submitted directly on a
login node.

For sequential stages that must share node-local `TMPDIR`, schedule the first
job of the chain with an allocation sized for the chain, then connect later
stages with file dependencies. Confirm the resulting plan with
`torc create --dry-run` and inspect generated scheduler output before a costly
run. Use separate allocations when stages need different resources or can run
independently.

Use `on_jobs_ready` when an allocation should be created as a selected stage
becomes ready. Use `on_workflow_start` for work that must reserve capacity at
workflow start, and `on_workflow_complete` for scoped cleanup. A workflow needs
at least one `schedule_nodes` action to be schedulable; validate the exact
trigger and job selectors with the installed Torc version.

## Make cleanup part of the graph

Materialize data into a run-scoped directory, not beside durable artifacts:

```yaml
variables:
  materialized_dir: $TMPDIR/2026_06_18_USA_defaults

actions:
  - trigger_type: on_workflow_start
    action_type: run_commands
    commands:
      - 'rm -rf -- "{materialized_dir}"'
      - 'mkdir -p -- "{materialized_dir}"'
  - trigger_type: on_workflow_complete
    action_type: run_commands
    commands:
      - 'rm -rf -- "{materialized_dir}"'
```

Only remove a path that is fully derived from the current run and cannot point
at a shared output directory. Preserve durable JSON, sidecars, XML, logs, and
RO-Crate metadata. If cleanup must happen after failure as well as success,
verify the installed Torc action semantics; do not assume a shell `trap` runs
inside a different job allocation.

## Put site setup in an invocation script

```bash
#!/usr/bin/env bash
set -euo pipefail
source /etc/profile.d/modules.sh
source /nopt/nrel/apps/env.sh
module purge
module load gams/51.3.0 xpressmp/9.7.0 conda/2024.06.1
exec "$@"
```

```yaml
jobs:
  - name: parse_reeds
    command: r2x run r2x-reeds.reeds-parser ...
    invocation_script: bash scripts/invocation.sh
```

Use the site's module initialization inside the job shell. A successful module
load on a login node does not prove that a non-login compute-node shell has the
same `MODULEPATH`.

## Provenance and validation

- Set `enable_ro_crate: true` when file/job provenance is part of the result.
- Validate parameter expansion with `torc create --dry-run` before execution.
- Use read-only validators for files, component counts, domain rules, and
  exported XML.
- Record code SHA, Torc version, R2X package versions, source archive checksum,
  scheduler/account, and output directory for reproducible runs.
- Keep the source workflow and generated Slurm workflow distinct when using
  `torc slurm generate`; never overwrite the only source spec. Preserve each
  R2X JSON entrypoint and its sidecar together in the retained artifact set.
