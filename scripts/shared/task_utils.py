from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from shared.artifact_paths import generated_tasks_dir

TASK_FILE_RE = re.compile(r"^TASK-(\d{3})-[a-z0-9-]+\.md$")
TASK_CODE_RE = re.compile(r"(TASK-\d{3})-")
TASK_NUMBER_RE = re.compile(r"TASK-(\d{3})-")
SECTION_RE_TEMPLATE = r"^## {heading}\n(.*?)(?=^## |\Z)"

PRIORITY_RANK = {
    "high": 0,
    "medium": 1,
    "low": 2,
}


@dataclass(frozen=True)
class TaskRecord:
    path: Path
    content: str
    code: str
    number: int
    status: str
    priority: str
    dependencies: tuple[str, ...]


def extract_task_number(path: Path) -> int | None:
    match = TASK_NUMBER_RE.match(path.name)
    return int(match.group(1)) if match else None


def extract_task_code(path: Path) -> str:
    match = TASK_CODE_RE.match(path.name)
    if match is None:
        raise ValueError(f"Could not extract task code from: {path.name}")
    return match.group(1)


def next_task_number(tasks_dir: Path) -> int:
    numbers: list[int] = []
    for path in tasks_dir.glob("TASK-*.md"):
        task_number = extract_task_number(path)
        if task_number is not None:
            numbers.append(task_number)
    return (max(numbers) + 1) if numbers else 1


def slugify(value: str, max_words: int = 6) -> str:
    words = re.sub(r"[^a-zA-Z0-9\s-]", "", value.lower()).split()
    trimmed = words[:max_words] if words else ["planned-work"]
    return "-".join(trimmed)


def extract_section(markdown: str, heading: str) -> str:
    pattern = SECTION_RE_TEMPLATE.format(heading=re.escape(heading))
    match = re.search(pattern, markdown, flags=re.MULTILINE | re.DOTALL)
    if match is None:
        return ""
    return match.group(1).strip()


def candidate_task_dirs(workspace_root: Path, target_name: str) -> list[Path]:
    candidates = [
        generated_tasks_dir(workspace_root, target_name),
        workspace_root / "backlog" / "tasks",
    ]
    return [path for path in candidates if path.exists()]


def parse_task_dependencies(markdown: str) -> tuple[str, ...]:
    section = extract_section(markdown, "Dependencies")
    if not section or section.lower() == "none":
        return ()

    dependencies = tuple(
        match
        for match in re.findall(r"TASK-\d{3}", section.upper())
    )
    return dependencies


def load_task_records(workspace_root: Path, target_name: str) -> list[TaskRecord]:
    records: list[TaskRecord] = []

    for task_dir in candidate_task_dirs(workspace_root, target_name):
        for path in sorted(task_dir.glob("TASK-*.md")):
            task_number = extract_task_number(path)
            if task_number is None:
                continue

            content = path.read_text(encoding="utf-8")
            status = extract_section(content, "Status").strip().lower()
            priority = extract_section(content, "Priority").strip().lower() or "medium"
            records.append(
                TaskRecord(
                    path=path,
                    content=content,
                    code=extract_task_code(path),
                    number=task_number,
                    status=status,
                    priority=priority,
                    dependencies=parse_task_dependencies(content),
                )
            )

    return records


def select_next_task(workspace_root: Path, target_name: str) -> tuple[Path, str]:
    records = load_task_records(workspace_root, target_name)
    if not records:
        raise FileNotFoundError(
            "No backlog tasks were found in agents/backlog/tasks or backlog/tasks."
        )

    status_by_code = {record.code: record.status for record in records}

    def dependencies_done(record: TaskRecord) -> bool:
        return all(status_by_code.get(code) == "done" for code in record.dependencies)

    def pick(status: str) -> TaskRecord | None:
        candidates = [
            record
            for record in records
            if record.status == status and dependencies_done(record)
        ]
        if not candidates:
            return None
        return min(
            candidates,
            key=lambda record: (
                PRIORITY_RANK.get(record.priority, PRIORITY_RANK["low"]),
                record.number,
            ),
        )

    selected = pick("todo") or pick("in-progress")
    if selected is None:
        raise FileNotFoundError(
            "No eligible backlog task is available. Expected a task with status "
            "`todo`, or an `in-progress` task to resume, with dependencies marked `done`."
        )

    return selected.path, selected.content


def find_task_by_marker(task_dir: Path, marker: str) -> tuple[Path, str] | None:
    for path in sorted(task_dir.glob("TASK-*.md")):
        content = path.read_text(encoding="utf-8")
        if marker in content:
            return path, content
    return None


def find_latest_task(task_dir: Path) -> Path | None:
    candidates: list[tuple[int, Path]] = []
    for path in task_dir.glob("TASK-*.md"):
        task_number = extract_task_number(path)
        if task_number is not None:
            candidates.append((task_number, path))
    if not candidates:
        return None
    return max(candidates, key=lambda item: item[0])[1]
