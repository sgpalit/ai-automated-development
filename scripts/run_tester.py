#!/usr/bin/env python3
"""Generate a local tester handoff artifact for the selected backlog task."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from run_developer import select_developer_task
from shared.artifact_paths import (
    analysis_path,
    developer_handoff_path,
    developer_implementation_path,
    reviewer_report_path,
    tester_report_path,
)
from shared.task_utils import extract_task_code


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write a tester validation report for the selected backlog task."
    )
    parser.add_argument(
        "goal",
        nargs="?",
        help="Optional human goal for the tester phase.",
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Target repository path. Defaults to current repository.",
    )
    parser.add_argument(
        "--task",
        help="Optional explicit backlog task file. If omitted, the current in-progress task is used.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the tester report without writing files.",
    )
    return parser.parse_args()


@dataclass(frozen=True)
class TesterInputs:
    task_path: Path
    task_content: str
    developer_artifact: Path | None
    implementation_artifact: Path | None
    reviewer_artifact: Path | None
    report_path: Path


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def resolve_inputs(
    repo_root: Path,
    workspace_root: Path,
    target_name: str,
    goal: str | None,
    planned_task: tuple[Path, str] | None = None,
    explicit_task: str | None = None,
) -> TesterInputs:
    if explicit_task:
        task_path = (workspace_root / explicit_task).resolve()
        task_content = _read_text(task_path)
    else:
        task_path, task_content = select_developer_task(
            repo_root=repo_root,
            goal=goal,
            workspace_root=workspace_root,
            target_name=target_name,
            planned_task=planned_task,
        )

    task_code = extract_task_code(task_path).lower()
    developer_artifact = developer_handoff_path(workspace_root, target_name, task_code)
    implementation_artifact = developer_implementation_path(workspace_root, target_name, task_code)
    reviewer_artifact = reviewer_report_path(workspace_root, target_name, task_code)
    report_path = tester_report_path(workspace_root, target_name, task_code)

    return TesterInputs(
        task_path=task_path,
        task_content=task_content,
        developer_artifact=developer_artifact if developer_artifact.exists() else None,
        implementation_artifact=implementation_artifact if implementation_artifact.exists() else None,
        reviewer_artifact=reviewer_artifact if reviewer_artifact.exists() else None,
        report_path=report_path,
    )


def build_report(
    *,
    repo_root: Path,
    workspace_root: Path,
    target_name: str,
    goal: str | None,
    inputs: TesterInputs,
) -> str:
    task_content = inputs.task_content
    mvp_path = workspace_root / "docs" / "mvp.md"
    current_analysis_path = analysis_path(workspace_root, target_name)

    developer_status = (
        f"Found: `{inputs.developer_artifact.relative_to(workspace_root)}`"
        if inputs.developer_artifact
        else "Missing developer artifact."
    )
    implementation_status = (
        f"Found: `{inputs.implementation_artifact.relative_to(workspace_root)}`"
        if inputs.implementation_artifact
        else "Missing implementation artifact."
    )
    reviewer_status = (
        f"Found: `{inputs.reviewer_artifact.relative_to(workspace_root)}`"
        if inputs.reviewer_artifact
        else "Missing reviewer artifact."
    )

    outcome = (
        "READY"
        if inputs.developer_artifact and inputs.implementation_artifact and inputs.reviewer_artifact
        else "NOT READY"
    )
    verdict = (
        "Pass: developer, implementation, and reviewer artifacts are available for tester handoff."
        if outcome == "READY"
        else "Fail: tester handoff is not ready because one or more prerequisite artifacts are missing."
    )

    task_title = task_content.splitlines()[0].strip()

    return "\n".join(
        [
            f"# Tester Report for {task_title}",
            "",
            "## Selected Task",
            f"- Task file: `{inputs.task_path.relative_to(workspace_root)}`",
            f"- Goal: {goal or 'No explicit goal provided; using current workflow context.'}",
            "",
            "## Artifact Check",
            f"- Developer artifact: {developer_status}",
            f"- Implementation artifact: {implementation_status}",
            f"- Reviewer artifact: {reviewer_status}",
            "",
            "## Workflow Grounding",
            f"- MVP reference: `{mvp_path.relative_to(workspace_root)}` expects tester validation before human acceptance.",
            f"- Repository analysis: `{current_analysis_path.relative_to(workspace_root)}` notes later workflow phases still need integration points and output contracts.",
            "",
            "## Outcome",
            f"- Status: {outcome}",
            f"- Verdict: {verdict}",
            "",
            "## Notes",
            "- This tester report is file-based so the local multi-agent loop can hand off a task-level validation artifact.",
            "- The tester phase is currently scoped to a single-cycle readiness check using the selected task plus available developer and reviewer outputs.",
        ]
    ).rstrip() + "\n"


def run_tester_phase(
    *,
    goal: str | None,
    repo_root: Path,
    workspace_root: Path,
    target_name: str,
    dry_run: bool,
    planned_task: tuple[Path, str] | None = None,
    explicit_task: str | None = None,
) -> Path:
    inputs = resolve_inputs(
        repo_root=repo_root,
        workspace_root=workspace_root,
        target_name=target_name,
        goal=goal,
        planned_task=planned_task,
        explicit_task=explicit_task,
    )
    report = build_report(
        repo_root=repo_root,
        workspace_root=workspace_root,
        target_name=target_name,
        goal=goal,
        inputs=inputs,
    )

    if dry_run:
        print(f"[dry-run] Would write tester report: {inputs.report_path}")
        print(report)
        return inputs.report_path

    inputs.report_path.parent.mkdir(parents=True, exist_ok=True)
    inputs.report_path.write_text(report, encoding="utf-8")
    print(f"Wrote tester report: {inputs.report_path.relative_to(workspace_root)}")
    return inputs.report_path


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo).resolve()
    workspace_root = Path(".").resolve()
    target_name = repo_root.name
    run_tester_phase(
        goal=args.goal,
        repo_root=repo_root,
        workspace_root=workspace_root,
        target_name=target_name,
        dry_run=args.dry_run,
        explicit_task=args.task,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
