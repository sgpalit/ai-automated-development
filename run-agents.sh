#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

if [ "$#" -eq 0 ]; then
  cat <<'EOF'
Usage:
  ./run-agents.sh "Your goal here" [--phase analyst|planner] [--repo PATH] [--dry-run]

Examples:
  ./run-agents.sh "Improve onboarding documentation"
  ./run-agents.sh "Improve onboarding documentation" --phase analyst
  ./run-agents.sh "Improve onboarding documentation" --dry-run
EOF
  exit 1
fi

exec python3 "$SCRIPT_DIR/scripts/run_cycle.py" "$@"
