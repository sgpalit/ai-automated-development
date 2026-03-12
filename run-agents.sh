#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_PYTHON="$SCRIPT_DIR/.venv/bin/python3"

if [ -x "$PROJECT_PYTHON" ]; then
  exec "$PROJECT_PYTHON" "$SCRIPT_DIR/scripts/run_cycle.py" --phase tester --execute "$@"
fi

exec python3 "$SCRIPT_DIR/scripts/run_cycle.py" --phase tester --execute "$@"
