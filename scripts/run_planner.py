from __future__ import annotations

import os
import re
from pathlib import Path

from dotenv import load_dotenv

from llm import run_prompt

FILE_BLOCK_RE = re.compile(
    r"===FILE:\s*(TASK-\d{3}-[a-z0-9-]+\.md)\s*===\n(.*?)\n===END===",
    re.DOTALL,
)
TASK_FILE_RE = re.compile(r"^TASK-(\d{3})-[a-z0-9-]+\.md$")


def next_task_number(tasks_dir: Path) -> int:
    numbers: list[int] = []
    for path in tasks_dir.glob("TASK-*.md"):
        match = TASK_FILE_RE.match(path.name)
        if match:
            numbers.append(int(match.group(1)))
    return (max(numbers) + 1) if numbers else 1


def parse_file_blocks(text: str) -> list[tuple[str, str]]:
    return [(name, body.strip() + "\n") for name, body in FILE_BLOCK_RE.findall(text)]


def main() -> None:
    load_dotenv()

    repo_path = Path(os.getenv("TARGET_REPO_PATH", ".")).resolve()
    analysis_path = repo_path / "analysis" / "repo-analysis.md"
    planner_prompt_path = repo_path / "prompts" / "agents" / "planner.md"
    tasks_dir = repo_path / "backlog" / "tasks"

    analysis_text = analysis_path.read_text(encoding="utf-8")
    planner_prompt = planner_prompt_path.read_text(encoding="utf-8")

    instruction = """
Return one or more task files in this exact format:
===FILE: TASK-###-short-description.md===
<full markdown content of that task file>
===END===

Rules:
- Use lowercase kebab-case for short-description.
- Use unique task numbers that do not conflict with existing files.
- Only output these file blocks.
""".strip()

    existing_files = "\n".join(sorted(p.name for p in tasks_dir.glob("TASK-*.md")))

    full_prompt = (
        f"{planner_prompt}\n\n"
        f"Existing task files:\n{existing_files}\n\n"
        f"Analysis:\n{analysis_text}\n\n"
        f"{instruction}"
    )

    output = run_prompt(full_prompt)
    blocks = parse_file_blocks(output)

    if not blocks:
        number = next_task_number(tasks_dir)
        fallback_name = f"TASK-{number:03d}-planner-generated-task.md"
        blocks = [(fallback_name, output.strip() + "\n")]

    tasks_dir.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    used_names: set[str] = set()
    next_number = next_task_number(tasks_dir)

    for name, body in blocks:
        if not TASK_FILE_RE.match(name) or name in used_names or (tasks_dir / name).exists():
            name = f"TASK-{next_number:03d}-planner-generated-task.md"
            next_number += 1

        used_names.add(name)
        path = tasks_dir / name
        path.write_text(body, encoding="utf-8")
        written.append(path)

    print("Wrote task files:")
    for path in written:
        print(f"- {path}")


if __name__ == "__main__":
    main()
