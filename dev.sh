#!/usr/bin/env bash

set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$project_root"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is required to run this project. Install uv first, then rerun ./dev.sh." >&2
  exit 1
fi

echo "Syncing project dependencies with uv..."
uv sync --locked

echo "Starting the Flask development server on http://127.0.0.1:5000 ..."
uv run flask --app run --debug run
