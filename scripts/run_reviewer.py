#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
from pathlib import Path

from run_developer import select_developer_task
from shared.artifact_paths import (
    analysis_path,
    developer_handoff_path,
    developer_implementation_path,
    generated_tasks_dir,
    reviewer_report_path,
)
from shared.task_utils import extract_section, extract_task_code, find_latest_task

PUSHED_COMMIT_RE = re.compile(r"Pushed commit hash:\s*`([^`]+)`")
COMMIT_HASH_RE = re.compile(r"^[0-9a-fA-F]{7,40}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a local reviewer report for a selected backlog task."
    )
    parser.add_argument(
        "goal",
        nargs="?",
        help="Human goal used to locate the matching planner task. If omitted, the next eligible backlog task is selected automatically.",
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Target repository path. Defaults to current repository.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the reviewer report without writing files.",
    )
    return parser.parse_args()


def read_if_exists(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def extract_pushed_commit_hash(handoff_text: str) -> str | None:
    match = PUSHED_COMMIT_RE.search(handoff_text)
    if match is None:
        return None
    value = match.group(1).strip()
    if not value or value == "pending":
        return None
    return value


def select_reviewer_task(
    *,
    repo_root: Path,
    goal: str | None,
    workspace_root: Path,
    target_name: str,
    planned_task: tuple[Path, str] | None = None,
) -> tuple[Path, str]:
    try:
        return select_developer_task(
            repo_root=repo_root,
            goal=goal,
            workspace_root=workspace_root,
            target_name=target_name,
            planned_task=planned_task,
        )
    except FileNotFoundError:
        if planned_task is not None or goal:
            raise

    candidate_dirs = [generated_tasks_dir(workspace_root, target_name), workspace_root / "backlog" / "tasks"]
    for task_dir in candidate_dirs:
        latest_task = find_latest_task(task_dir)
        if latest_task is not None:
            return latest_task, latest_task.read_text(encoding="utf-8")

    raise FileNotFoundError("Reviewer phase requires at least one backlog task to inspect.")


def inspect_pushed_commit(target_repo_root: Path, pushed_commit_hash: str | None) -> tuple[bool, str]:
    if not pushed_commit_hash:
        return (
            False,
            "Pushed-commit evidence is missing from the developer handoff; review findings cannot be grounded in an inspectable pushed task result.",
        )

    if COMMIT_HASH_RE.fullmatch(pushed_commit_hash) is None:
        return (
            False,
            f"Pushed commit hash `{pushed_commit_hash}` is malformed, so the reviewer could not inspect it in the target repository.",
        )

    try:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", f"{pushed_commit_hash}^{{commit}}"],
            cwd=target_repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        return (
            False,
            f"Pushed commit `{pushed_commit_hash}` could not be inspected in the target repository because git inspection failed: {exc}.",
        )

    if result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip() or "git rev-parse returned a non-zero exit status."
        return (
            False,
            f"Pushed commit `{pushed_commit_hash}` could not be inspected in the target repository: {stderr}",
        )

    resolved_hash = result.stdout.strip()
    return (
        True,
        f"Review findings are grounded in inspecting pushed commit `{resolved_hash}` in the target repository rather than only the local worktree or task artifacts.",
    )


def build_inputs_reviewed(workspace_root: Path, target_name: str, task_path: Path) -> list[Path]:
    task_code = extract_task_code(task_path).lower()
    candidates = [
        analysis_path(workspace_root, target_name),
        task_path,
        developer_handoff_path(workspace_root, target_name, task_code),
        developer_implementation_path(workspace_root, target_name, task_code),
    ]
    return [path for path in candidates if path.exists()]


def section_items(markdown: str, heading: str) -> list[str]:
    content = extract_section(markdown, heading)
    if not content:
        return []

    items: list[str] = []
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("- "):
            items.append(stripped[2:].strip())
        else:
            items.append(stripped)
    return items


def detect_missing_plan_details(implementation_text: str, task_text: str) -> list[str]:
    missing: list[str] = []
    plan_steps = section_items(implementation_text, "Step-by-Step Implementation Plan")
    likely_files = section_items(implementation_text, "Exact Files Likely To Change")
    acceptance = section_items(implementation_text, "Exact Acceptance Criteria")
    task_status = extract_section(task_text, "Status").lower()

    if not plan_steps:
        missing.append("The implementation artifact does not include a step-by-step plan.")
    if not likely_files:
        missing.append("The implementation artifact does not identify likely files to change.")
    if not acceptance:
        missing.append("The implementation artifact does not restate acceptance criteria.")
    if task_status != "done":
        missing.append(
            f"The selected task is still `{task_status}`, so implementation completion and verification are not yet evident."
        )

    return missing


def analyze_risks(
    task_text: str,
    implementation_text: str,
    handoff_text: str,
    pushed_commit_hash: str | None,
    commit_is_inspectable: bool,
    commit_evidence_note: str,
) -> list[str]:
    risks: list[str] = []
    likely_files = section_items(implementation_text, "Exact Files Likely To Change")

    if not handoff_text:
        risks.append("Developer handoff is missing, so reviewer context is incomplete.")
    if not implementation_text:
        risks.append("Developer implementation artifact is missing, so the implementation plan cannot be fully reviewed.")
    if extract_section(task_text, "Status").lower() == "done" and not pushed_commit_hash:
        risks.append("Task is marked done, but the developer handoff does not record a pushed commit hash for review.")
    if pushed_commit_hash and not commit_is_inspectable:
        risks.append(commit_evidence_note)
    if any(path.endswith(".py`") or path.endswith(".py") for path in likely_files):
        risks.append("Proposed script changes could affect local runner behavior and should be checked with dry-run verification.")
    if any("docs/" in path for path in likely_files):
        risks.append("Documentation changes may drift from actual runner behavior if the workflow scripts change again.")
    if task_text and handoff_text and task_text not in handoff_text:
        risks.append("The developer handoff appears stale relative to the current task file and may need regeneration.")
    if task_text and implementation_text and task_text not in implementation_text:
        risks.append("The implementation artifact appears stale relative to the current task file and may need regeneration.")

    if not risks:
        risks.append("No immediate structural risk was identified from the available developer artifacts.")

    return risks


def build_suggested_improvements(
    task_text: str,
    missing_details: list[str],
    risks: list[str],
    pushed_commit_hash: str | None,
    commit_is_inspectable: bool,
) -> list[str]:
    suggestions: list[str] = []

    if missing_details:
        suggestions.append("Regenerate or update the developer implementation artifact so the plan, likely files, and acceptance criteria are explicit.")
    if extract_section(task_text, "Status").lower() != "done":
        suggestions.append("Do not approve review until the task file is updated to `done` or explicitly `blocked` with explanation.")
    if not pushed_commit_hash:
        suggestions.append("Require the developer handoff to include the pushed commit hash so review can inspect a concrete repository snapshot.")
    elif not commit_is_inspectable:
        suggestions.append("Ask the developer to confirm the pushed commit is available in the target repository before review proceeds.")
    if not suggestions:
        suggestions.append("Proceed with normal code and acceptance-criteria review against the referenced pushed commit.")

    return suggestions


def build_reviewer_report(
    *,
    repo_root: Path,
    workspace_root: Path,
    target_name: str,
    task_path: Path,
    task_text: str,
    implementation_text: str,
    handoff_text: str,
) -> str:
    pushed_commit_hash = extract_pushed_commit_hash(handoff_text)
    commit_is_inspectable, commit_evidence_note = inspect_pushed_commit(repo_root, pushed_commit_hash)
    missing_details = detect_missing_plan_details(implementation_text, task_text)
    risks = analyze_risks(
        task_text=task_text,
        implementation_text=implementation_text,
        handoff_text=handoff_text,
        pushed_commit_hash=pushed_commit_hash,
        commit_is_inspectable=commit_is_inspectable,
        commit_evidence_note=commit_evidence_note,
    )
    suggestions = build_suggested_improvements(
        task_text=task_text,
        missing_details=missing_details,
        risks=risks,
        pushed_commit_hash=pushed_commit_hash,
        commit_is_inspectable=commit_is_inspectable,
    )
    inputs_reviewed = build_inputs_reviewed(workspace_root, target_name, task_path)

    inputs_text = "\n".join(f"- `{path.relative_to(repo_root).as_posix()}`" for path in inputs_reviewed) or "- None found"
    missing_text = "\n".join(f"- {item}" for item in missing_details) or "- None noted"
    risks_text = "\n".join(f"- {item}" for item in risks) or "- None noted"
    suggestions_text = "\n".join(f"- {item}" for item in suggestions) or "- None noted"

    return (
        f"# Reviewer Report\n\n"
        f"## Date\n{dt.datetime.now(dt.timezone.utc).isoformat()}\n\n"
        f"## Task\n- Code: {extract_task_code(task_path)}\n- File: `{task_path.relative_to(repo_root).as_posix()}`\n\n"
        f"## Inputs Reviewed\n{inputs_text}\n\n"
        f"## Pushed Commit Evidence\n- Recorded pushed commit hash: `{pushed_commit_hash or 'missing'}`\n"
        f"- Inspectable in target repository: {'yes' if commit_is_inspectable else 'no'}\n"
        f"- Evidence note: {commit_evidence_note}\n\n"
        f"## Missing Plan Details\n{missing_text}\n\n"
        f"## Risks\n{risks_text}\n\n"
        f"## Suggested Improvements\n{suggestions_text}\n"
    )


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo).resolve()
    workspace_root = repo_root / "agents"
    target_name = repo_root.name

    planner_task_dir = generated_tasks_dir(workspace_root, target_name)
    planned_task = None
    try:
        planned_task_path, planned_task_content = select_developer_task(
            repo_root=repo_root,
            goal=args.goal,
            workspace_root=workspace_root,
            target_name=target_name,
        )
        planned_task = (planned_task_path, planned_task_content)
    except FileNotFoundError:
        planned_task = None

    task_path, task_text = select_reviewer_task(
        repo_root=repo_root,
        goal=args.goal,
        workspace_root=workspace_root,
        target_name=target_name,
        planned_task=planned_task,
    )

    task_code = extract_task_code(task_path).lower()
    implementation_path = developer_implementation_path(workspace_root, target_name, task_code)
    handoff_path = developer_handoff_path(workspace_root, target_name, task_code)
    report_path = reviewer_report_path(workspace_root, target_name, task_code)

    implementation_text = read_if_exists(implementation_path)
    handoff_text = read_if_exists(handoff_path)

    report_text = build_reviewer_report(
        repo_root=repo_root,
        workspace_root=workspace_root,
        target_name=target_name,
        task_path=task_path,
        task_text=task_text,
        implementation_text=implementation_text,
        handoff_text=handoff_text,
    )

    if args.dry_run:
        print(report_text.rstrip())
        return 0

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_text, encoding="utf-8")
    print(f"Wrote reviewer report: {report_path.relative_to(repo_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
