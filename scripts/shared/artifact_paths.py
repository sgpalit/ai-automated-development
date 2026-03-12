from __future__ import annotations

from pathlib import Path

ARTIFACTS_DIRNAME = "agents"


def artifacts_root(workspace_root: Path) -> Path:
    return workspace_root / ARTIFACTS_DIRNAME


def target_artifacts_root(workspace_root: Path, target_name: str) -> Path:
    return artifacts_root(workspace_root) / target_name


def analysis_path(workspace_root: Path, target_name: str) -> Path:
    return target_artifacts_root(workspace_root, target_name) / "analysis" / "repo-analysis.md"


def generated_tasks_dir(workspace_root: Path, target_name: str) -> Path:
    return target_artifacts_root(workspace_root, target_name) / "backlog" / "tasks"


def developer_handoff_path(workspace_root: Path, target_name: str, task_code: str) -> Path:
    return target_artifacts_root(workspace_root, target_name) / "handoff" / "developer" / f"{task_code.lower()}-developer-handoff.md"


def developer_implementation_path(workspace_root: Path, target_name: str, task_code: str) -> Path:
    return target_artifacts_root(workspace_root, target_name) / "implementation" / "developer" / f"{task_code.lower()}-implementation.md"


def reviewer_report_path(workspace_root: Path, target_name: str, task_code: str) -> Path:
    return target_artifacts_root(workspace_root, target_name) / "review" / "reviewer" / f"{task_code.lower()}-review.md"


def tester_report_path(workspace_root: Path, target_name: str, task_code: str) -> Path:
    return target_artifacts_root(workspace_root, target_name) / "test" / f"{task_code.lower()}-test.md"


def logs_dir(workspace_root: Path, target_name: str) -> Path:
    return target_artifacts_root(workspace_root, target_name) / "logs"
