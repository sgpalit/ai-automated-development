from __future__ import annotations

from pathlib import Path

ARTIFACTS_DIRNAME = "agents"


def artifacts_root(repo_root: Path) -> Path:
    return repo_root / ARTIFACTS_DIRNAME


def analysis_path(repo_root: Path) -> Path:
    return artifacts_root(repo_root) / "analysis" / "repo-analysis.md"


def generated_tasks_dir(repo_root: Path) -> Path:
    return artifacts_root(repo_root) / "backlog" / "tasks"


def developer_handoff_path(repo_root: Path, task_code: str) -> Path:
    return artifacts_root(repo_root) / "handoff" / "developer" / f"{task_code.lower()}-developer-handoff.md"


def developer_implementation_path(repo_root: Path, task_code: str) -> Path:
    return artifacts_root(repo_root) / "implementation" / "developer" / f"{task_code.lower()}-implementation.md"


def reviewer_report_path(repo_root: Path, task_code: str) -> Path:
    return artifacts_root(repo_root) / "review" / "reviewer" / f"{task_code.lower()}-review.md"


def tester_report_path(repo_root: Path, task_code: str) -> Path:
    return artifacts_root(repo_root) / "test" / f"{task_code.lower()}-test.md"


def logs_dir(repo_root: Path) -> Path:
    return artifacts_root(repo_root) / "logs"
