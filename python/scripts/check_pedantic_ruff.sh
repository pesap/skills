#!/usr/bin/env bash
# Run from the target project through its configured environment runner.
# Requires installed Ruff. Preview/ALL findings are diagnostic, not policy.
set -euo pipefail

if (( $# == 0 )); then
  set -- .
fi

exec ruff check --preview --select ALL --no-fix --no-fix-only --no-unsafe-fixes \
  --output-format full -- "$@"
