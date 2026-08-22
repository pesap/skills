# R2X workflow patterns

Use this reference when a Torc workflow parses ReEDS, translates to PLEXOS, exports XML,
or runs PLEXOS.

## Choose the smallest level

| Need                 | Workflow shape                                                                   | Keep out                                             |
| -------------------- | -------------------------------------------------------------------------------- | ---------------------------------------------------- |
| Local XML smoke test | `untar action -> parse -> translate -> export`                                   | Slurm, resource profiles, `execution_config`, solver |
| Local year matrix    | Same graph with `parameters` and parameterized FileSpecs/jobs                    | PLEXOS solver and HPC policy                         |
| HPC XML generation   | Same graph plus resources, scheduler, `schedule_nodes`, and invocation scripts   | Solver unless requested                              |
| HPC solve            | XML generation -> separate PLEXOS job and allocation                             | Login-node solver execution                          |
| Experiment platform  | Parameterized systems, validation, provenance, retries, and explicit allocations | Controls that are not wired to a job                 |

Start with the local single-case workflow. Add parameter expansion only after one case
runs. Keep the same durable boundaries as the workflow grows.

## Artifact contracts

Treat these as bundles, not isolated paths:

- R2X JSON plus its adjacent `<stem>_time_series/` directory;
- PLEXOS XML plus its adjacent `Data/` directory; and
- PLEXOS solution directory plus its run log and completion marker.

A JSON FileSpec establishes a Torc dependency, but it does not make the sidecar part of
Torc's file validation. Validators, remote fetches, and cleanup must preserve the bundle.
Use native R2X `-i` and `-o` boundaries; do not pipe or convert systems between jobs.

## Local workflow rules

A local-only workflow normally needs no `resource_requirements`, `execution_config`,
`slurm_schedulers`, or `schedule_nodes`. Use:

```bash
torc create --dry-run workflow.yaml
torc -s --in-memory run workflow.yaml --max-parallel-jobs 1 \
  --output-dir <unique-temporary-directory>
```

A dry run validates expansion only. It does not untar the archive or exercise R2X.
Use a unique temporary output directory for the real smoke test. Torc local
workflow actions run from Torc's output directory, so use absolute paths in
setup actions and create the target directory before `tar -C`.

For a simple local archive, a workflow-start action is acceptable:

```yaml
actions:
  - trigger_type: on_workflow_start
    action_type: run_commands
    commands:
      - 'mkdir -p "{tmpdir}"'
      - 'tar -xzf "{raw_archive}" -C "{tmpdir}"'
```

The action runs before jobs, but it is not a FileSpec dependency edge. If extraction
must be independently verified and must block parsing on failure, use a materialize job
that produces a marker as its final output instead. Do not assume an action failure will
prevent unrelated ready jobs from starting.

Use absolute `raw_archive` and `tmpdir` values in actions. Actions run from Torc's
output directory, not necessarily the workflow submission directory. Torc workflow
variables use `{name}` substitution; they do not evaluate `$TMPDIR` or command
substitution. Set platform-specific concrete paths, for example:

```yaml
variables:
  raw_archive: /path/to/repo/data/artifacts/reeds-input.tar.gz
  tmpdir: /tmp/reeds-r2x
```

or:

```yaml
variables:
  raw_archive: C:/path/to/repo/data/artifacts/reeds-input.tar.gz
  tmpdir: C:/Users/user/AppData/Local/Temp/reeds-r2x
```

Windows 10+ includes `tar`. Keep commands to tools available on both platforms;
avoid `rm -rf`, Bash-only heredocs, and shell-specific environment syntax in a
cross-platform local workflow.

## Year matrices

Use workflow parameters for every value that changes a path or command:

```yaml
parameters:
  solve_year: [2029, 2050]
  weather_year: [2012, 2018]

files:
  - name: parsed_{solve_year}_{weather_year}
    path: artifacts/parsed_{solve_year}_{weather_year}.json
    use_parameters: [solve_year, weather_year]
```

Give every expanded job and FileSpec a unique name and path. Use the same parameters
in `use_parameters` for the job and its files. Check the source archive's available
solve years before choosing a matrix; ReEDS parser inputs commonly reject years not
listed in `inputs_case/modeledyears.csv`.

Keep local matrix concurrency low (`--max-parallel-jobs 1`) until memory and temporary
storage use are known. A matrix dry run should report the expected expanded job/file
counts before payload execution.

## Environment and invocation scripts

Workflow `env` values are literal strings. Do not write shell commands there:

```yaml
# Wrong: command substitution is not evaluated.
env:
  R2X_PYTHON: "$(r2x python path)"
```

Use an `invocation_script` for dynamic setup and make it execute the job command:

```bash
#!/usr/bin/env bash
set -euo pipefail
export R2X_PYTHON="$(r2x python path)"
exec "$@"
```

Use the same R2X-managed interpreter for validators that read R2X System JSON. Do not
let `uv run --script` silently create a second environment with incompatible R2X or
infrasys versions.

For HPC module setup, source the site's module initialization, purge/load the required
module, and `exec "$@"`. Keep credentials out of YAML, commands, logs, and Git.

## PLEXOS boundary

Run PLEXOS only in a scheduler allocation. A PLEXOS job should consume the exported
XML and `Data/` directory, load the site module through an invocation script, write to
a run-scoped solution directory, capture a log, and create a completion marker only
after the executable exits successfully. Inspect Torc job results and payload logs;
`sbatch` success alone is not a successful PLEXOS run.
