#!/usr/bin/env sh
set -eu

TASK_DIR="backlog/tasks"
FAIL=0

if [ ! -d "$TASK_DIR" ]; then
  echo "ERROR: $TASK_DIR not found"
  exit 1
fi

for file in "$TASK_DIR"/*.md; do
  base=$(basename "$file")

  case "$base" in
    TASK-TEMPLATE.md) ;;
    TASK-[0-9][0-9][0-9]-*.md) ;;
    *)
      echo "ERROR: invalid task filename: $base"
      FAIL=1
      ;;
  esac

  for heading in Status Priority Objective Scope "Out of Scope" "Acceptance Criteria" Dependencies; do
    if ! rg -q "^## ${heading}$" "$file"; then
      echo "ERROR: $base is missing heading: $heading"
      FAIL=1
    fi
  done
done

if [ "$FAIL" -ne 0 ]; then
  echo "Backlog checks failed."
  exit 1
fi

echo "Backlog checks passed."
