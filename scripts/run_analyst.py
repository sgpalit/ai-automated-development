from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from llm import run_prompt

MAX_FILES = 120
MAX_FILE_CHARS = 5000


SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
}


def build_repo_snapshot(repo_path: Path) -> str:
    lines: list[str] = []
    count = 0

    for path in sorted(repo_path.rglob("*")):
        if count >= MAX_FILES:
            break
        if path.is_dir():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue

        rel = path.relative_to(repo_path)
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        count += 1
        trimmed = text[:MAX_FILE_CHARS]
        if len(text) > MAX_FILE_CHARS:
            trimmed += "\n... [truncated]"

        lines.append(f"\n--- FILE: {rel} ---\n{trimmed}")

    if not lines:
        return "(No readable text files found.)"

    return "\n".join(lines)


def main() -> None:
    load_dotenv()

    repo_path = Path(os.getenv("TARGET_REPO_PATH", ".")).resolve()
    prompt_path = repo_path / "prompts" / "agents" / "analyst.md"

    analyst_prompt = prompt_path.read_text(encoding="utf-8")
    repo_snapshot = build_repo_snapshot(repo_path)

    full_prompt = (
        f"{analyst_prompt}\n\n"
        "Repository context (truncated for token limits):\n"
        f"{repo_snapshot}\n\n"
        "Write the final analysis content for analysis/repo-analysis.md."
    )

    output = run_prompt(full_prompt)

    analysis_dir = repo_path / "analysis"
    analysis_dir.mkdir(parents=True, exist_ok=True)
    output_path = analysis_dir / "repo-analysis.md"
    output_path.write_text(output, encoding="utf-8")

    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
