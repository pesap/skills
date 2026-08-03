#!/usr/bin/env python3
"""Run pytest doctests found in Markdown documentation.

Copy this script into a repository's scripts/ directory and pass the
repository's documentation paths. The default path is docs/.
"""

from __future__ import annotations

import argparse
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run pytest doctests collected from Markdown files."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["docs"],
        help="Documentation files or directories to test (default: docs)",
    )
    args = parser.parse_args()

    command = [
        sys.executable,
        "-m",
        "pytest",
        "--doctest-glob=*.md",
        *args.paths,
    ]
    return subprocess.run(command, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
