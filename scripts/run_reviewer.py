#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path

from run_developer import select_developer_task
from shared.artifact_paths import (
    analysis_path,
    developer_handoff_path,
    developer_implementation_path,
    reviewer_report_path,
)
from shared.task_utils import extract_section, extract_task_code

PUSHED_COMMIT_RE = re.compile(r"Pushed commit hash:\s*`([^`]+)`")


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


def analyze_risks(task_text: str, implementation_text: str, handoff_text: str) -> list[str]:
    risks: list[str] = []
    likely_files = section_items(implementation_text, "Exact Files Likely To Change")
    pushed_commit_hash = extract_pushed_commit_hash(handoff_text)

    if not handoff_text:
        risks.append("Developer handoff is missing, so reviewer context is incomplete.")
    if not implementation_text:
        risks.append("Developer implementation artifact is missing, so the implementation plan cannot be fully reviewed.")
    if extract_section(task_text, "Status").lower() == "done" and not pushed_commit_hash:
        risks.append("Task is marked done, but the developer handoff does not record a pushed commit hash for review.")
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


def build_suggested_improvements(task_text: str, missing_details: list[str], risks: list[str]) -> list[str]:
    suggestions: list[str] = []
    task_status = extract_section(task_text, "Status").lower()

    if task_status != "done":
        suggestions.append(
            f"Complete implementation verification and move the task from `{task_status}` to `done` only after the acceptance criteria are satisfied."
        )
    if any("stale" in item.lower() for item in risks):
        suggestions.append("Regenerate the developer handoff and implementation prompt so they match the current task definition.")
    if missing_details:
        suggestions.append("Fill the missing implementation details before final review to reduce ambiguity for follow-up work.")

    if not suggestions:
        suggestions.append("The developer artifacts are reviewable as-is; proceed to final verification and completion reporting.")

    return suggestions


def decide_review(task_text: str, missing_details: list[str], risks: list[str]) -> str:
    task_status = extract_section(task_text, "Status").lower()
    if task_status != "done":
        return "needs-changes"
    if missing_details:
        return "needs-changes"
    if any("stale" in item.lower() for item in risks):
        return "needs-changes"
    return "approved"


def build_reviewer_report(
    goal: str,
    workspace_root: Path,
    target_name: str,
    target_repo_root: Path,
    task_path: Path,
    task_text: str,
    analysis_text: str,
    handoff_text: str,
    implementation_text: str,
) -> str:
    review_date = dt.date.today().isoformat()
    task_code = extract_task_code(task_path)
    pushed_commit_hash = extract_pushed_commit_hash(handoff_text)
    inputs_reviewed = build_inputs_reviewed(
        workspace_root=workspace_root,
        target_name=target_name,
        task_path=task_path,
    )
    objective = extract_section(task_text, "Objective")
    missing_details = detect_missing_plan_details(implementation_text=implementation_text, task_text=task_text)
    risks = analyze_risks(
        task_text=task_text,
        implementation_text=implementation_text,
        handoff_text=handoff_text,
    )
    suggestions = build_suggested_improvements(
        task_text=task_text,
        missing_details=missing_details,
        risks=risks,
    )
    decision = decide_review(task_text=task_text, missing_details=missing_details, risks=risks)

    inputs_text = "\n".join(f"- `{path.relative_to(workspace_root)}`" for path in inputs_reviewed) or "- None"
    missing_text = "\n".join(f"- {item}" for item in missing_details) or "- No major detail gaps detected in the implementation artifact."
    risks_text = "\n".join(f"- {item}" for item in risks)
    suggestions_text = "\n".join(f"- {item}" for item in suggestions)
    analysis_note = (
        "- The current analysis artifact was available and supports the onboarding/documentation framing."
        if analysis_text
        else "- No analysis artifact was available during review."
    )
    notes = [
        "Reviewer did not modify repository code.",
        f"Current task status is `{extract_section(task_text, 'Status').lower()}`.",
        "Re-run reviewer after implementation artifacts and task state are synchronized if developer output changes.",
    ]
    notes_text = "\n".join(f"- {item}" for item in notes)

    return f"""# Reviewer Report

## Context
- Goal: {goal}
- Task ID: `{task_code}`
- Repository Path: `{target_repo_root}`
- Review Date: {review_date}

## Inputs Reviewed
{inputs_text}

## Task Summary
- {objective}
{analysis_note}

## Implementation Plan Evaluation
- Implementation artifact present: {"yes" if implementation_text else "no"}
- Developer handoff present: {"yes" if handoff_text else "no"}
- Developer pushed commit hash: {f"`{pushed_commit_hash}`" if pushed_commit_hash else "not provided"}
{missing_text}

## Risk Analysis
{risks_text}

## Suggested Improvements
{suggestions_text}

## Decision
{decision}

## Notes
{notes_text}
"""


def run_reviewer_phase(
    goal: str | None,
    repo_root: Path,
    workspace_root: Path,
    target_name: str,
    dry_run: bool,
    planned_task: tuple[Path, str] | None = None,
) -> Path:
    task_path, task_text = select_developer_task(
        repo_root=repo_root,
        goal=goal,
        workspace_root=workspace_root,
        target_name=target_name,
        planned_task=planned_task,
    )
    task_code = extract_task_code(task_path).lower()
    report_path = reviewer_report_path(workspace_root, target_name, task_code)
    report_dir = report_path.parent
    analysis_text = read_if_exists(analysis_path(workspace_root, target_name))
    handoff_text = read_if_exists(developer_handoff_path(workspace_root, target_name, task_code))
    implementation_text = read_if_exists(developer_implementation_path(workspace_root, target_name, task_code))
    report = build_reviewer_report(
        goal=goal or extract_section(task_text, "Objective") or task_code,
        workspace_root=workspace_root,
        target_name=target_name,
        target_repo_root=repo_root,
        task_path=task_path,
        task_text=task_text,
        analysis_text=analysis_text,
        handoff_text=handoff_text,
        implementation_text=implementation_text,
    )

    print(f"Reviewer selected task: {task_path}")

    if dry_run:
        print(f"[dry-run] Would write reviewer report: {report_path}")
        print(report)
        return report_path

    report_dir.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")
    print(f"Reviewer report written: {report_path}")
    return report_path


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo).resolve()
    workspace_root = Path(".").resolve()
    target_name = repo_root.name
    run_reviewer_phase(
        goal=args.goal,
        repo_root=repo_root,
        workspace_root=workspace_root,
        target_name=target_name,
        dry_run=args.dry_run,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
