# Local Torc execution

Use local execution to validate specification expansion, wrappers, paths, and
small payloads before consuming HPC allocations.

## Preflight

From the repository root:

```bash
torc --version
torc create --dry-run workflow.yaml
torc -f json create --dry-run workflow.yaml
```

The dry run validates the graph and reports expanded jobs/files. It does not
run R2X, build software, solve a model, or create durable model artifacts.

## Standalone smoke test

Use a unique output directory and constrain concurrency:

```bash
torc -s --in-memory run workflow.yaml \
  --max-parallel-jobs 1 \
  --output-dir /tmp/torc-smoke-$(date +%Y%m%d-%H%M%S)
```

Use `--num-cpus`, `--memory-gb`, `--num-gpus`, or `--time-limit` when the local
machine needs explicit limits. Do not write a smoke test into canonical
`artifacts/` or a shared materialized-data directory.

For R2X, start with the smallest meaningful stage graph, such as archive
materialization plus parsing. Add translation, export, and validation only
after the previous boundary produces the expected durable file bundle.

## Invocation scripts

Use an invocation script when the job needs modules, conda, or a controlled
shell. Keep it short and make it execute the command it receives:

```bash
#!/usr/bin/env bash
set -euo pipefail
source /etc/profile.d/modules.sh 2>/dev/null || true
module load <module>
source <conda-hook-if-needed>
conda activate <environment>
exec "$@"
```

Test the wrapper with a harmless command before attaching it to a full workflow.
Do not hide workflow dependencies or artifact copying in the wrapper.

## Installation

If Torc is missing and a user-managed binary is allowed, use the bundled
installer rather than hand-writing a download flow:

```bash
skills/torc/scripts/install-latest-torc.sh \
  --install-dir "$HOME/.local/bin" --print-path
export PATH="$HOME/.local/bin:$PATH"
torc --version
```

Prefer a site-provided module or package manager when cluster policy requires
one. The installer writes only the selected `torc` executable.

## Inspecting a completed local run

Use the output directory printed by Torc. If standalone mode used an in-memory
database, it snapshots state at shutdown; retain the database and job logs when
the run is evidence. Check the workflow status and result records before
opening payload logs.

If a local smoke test fails, classify it as graph expansion, environment
bootstrap, missing input, or payload failure. Do not jump directly to Slurm
until the smallest local reproducer is understood.
