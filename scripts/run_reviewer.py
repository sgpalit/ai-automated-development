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
    reviewer_report_path,
)
from shared.task_utils import extract_section, extract_task_code

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
    commit_is_inspectable: bool,
) -> list[str]:
    suggestions: list[str] = []
    task_status = extract_section(task_text, "Status").lower()

    if task_status != "done":
        suggestions.append(
            f"Complete implementation verification and move the task from `{task_status}` to `done` only after the acceptance criteria are satisfied."
        )
    if not commit_is_inspectable:
        suggestions.append("Add a usable pushed commit hash to the developer handoff and ensure the commit is locally inspectable in the target repository before requesting approval-ready review.")
    if any("stale" in item.lower() for item in risks):
        suggestions.append("Regenerate the developer handoff and implementation prompt so they match the current task definition.")
    if missing_details:
        suggestions.append("Fill the missing implementation details before final review to reduce ambiguity for follow-up work.")

    if not suggestions:
        suggestions.append("The developer artifacts are reviewable as-is; proceed to final verification and completion reporting.")

    return suggestions


def decide_review(
    task_text: str,
    missing_details: list[str],
    risks: list[str],
    commit_is_inspectable: bool,
) -> str:
    task_status = extract_section(task_text, "Status").lower()
    if task_status != "done":
        return "needs-changes"
    if not commit_is_inspectable:
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
    commit_is_inspectable, commit_evidence_note = inspect_pushed_commit(target_repo_root, pushed_commit_hash)
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
        pushed_commit_hash=pushed_commit_hash,
        commit_is_inspectable=commit_is_inspectable,
        commit_evidence_note=commit_evidence_note,
    )
    suggestions = build_suggested_improvements(
        task_text=task_text,
        missing_details=missing_details,
        risks=risks,
        commit_is_inspectable=commit_is_inspectable,
    )
    decision = decide_review(
        task_text=task_text,
        missing_details=missing_details,
        risks=risks,
        commit_is_inspectable=commit_is_inspectable,
    )

    inputs_text = "\n".join(f"- `{path.relative_to(workspace_root)}`" for path in inputs_reviewed) or "- None"
    missing_text = "\n".join(f"- {item}" for item in missing_details) or "- No major detail gaps detected in the implementation artifact."
    risks_text = "\n".join(f"- {item}" for item in risks)
    suggestions_text = "\n".join(f"- {item}" for item in suggestions)
    analysis_note = (
        "- The current analysis artifact was reviewed for continuity with the selected goal."
        if analysis_text
        else "- No planner analysis artifact was available for this review."
    )
    commit_summary = pushed_commit_hash if pushed_commit_hash else "missing"
    commit_findings_text = "\n".join(
        [
            f"- Reported pushed commit hash: `{commit_summary}`",
            f"- Inspection status: {'inspectable' if commit_is_inspectable else 'not inspectable'}",
            f"- Evidence: {commit_evidence_note}",
        ]
    )

    return "\n".join(
        [
            f"# Reviewer Report — {task_code}",
            "",
            "## Context",
            f"- Goal: {goal}",
            f"- Review date: {review_date}",
            f"- Target repository: `{target_repo_root}`",
            f"- Task file: `{task_path.relative_to(workspace_root)}`",
            f"- Objective: {objective or 'Not provided.'}",
            "",
            "## Decisions",
            f"- Decision: `{decision}`",
            f"- Summary: Reviewer decision is based on the selected task artifacts and pushed-commit inspection evidence.",
            "",
            "## Artifacts",
            "### Inputs Reviewed",
            inputs_text,
            analysis_note,
            "",
            "### Pushed Commit Verification",
            commit_findings_text,
            "",
            "### Missing Details",
            missing_text,
            "",
            "### Risks",
            risks_text,
            "",
            "## Open Questions / Risks",
            risks_text,
            "",
            "## Recommended Next Step",
            suggestions_text,
            "",
        ]
    )


def main() -> int:
    args = parse_args()
    target_repo_root = Path(args.repo).resolve()
    workspace_root = Path(__file__).resolve().parent.parent
    goal = args.goal or ""
    selection = select_developer_task(goal=goal, repo_root=target_repo_root, workspace_root=workspace_root)
    target_name = selection.target_name
    task_path = selection.task_path
    task_code = extract_task_code(task_path).lower()

    task_text = task_path.read_text(encoding="utf-8")
    analysis_text = read_if_exists(analysis_path(workspace_root, target_name))
    handoff_text = read_if_exists(developer_handoff_path(workspace_root, target_name, task_code))
    implementation_text = read_if_exists(developer_implementation_path(workspace_root, target_name, task_code))

    report = build_reviewer_report(
        goal=goal or selection.goal,
        workspace_root=workspace_root,
        target_name=target_name,
        target_repo_root=target_repo_root,
        task_path=task_path,
        task_text=task_text,
        analysis_text=analysis_text,
        handoff_text=handoff_text,
        implementation_text=implementation_text,
    )

    if args.dry_run:
        print(report)
        return 0

    output_path = reviewer_report_path(workspace_root, target_name, task_code)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Wrote reviewer report to {output_path.relative_to(workspace_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
