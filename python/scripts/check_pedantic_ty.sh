#!/usr/bin/env bash
# Run from the target project through its configured environment runner.
# Requires installed ty. Enforce configured rules and fail on warnings.
set -euo pipefail

if (( $# == 0 )); then
  set -- .
fi

exec ty check --error-on-warning --output-format full -- "$@"
