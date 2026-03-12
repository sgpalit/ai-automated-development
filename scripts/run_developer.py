#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import datetime as dt
import os
import re
import subprocess
from pathlib import Path
from textwrap import dedent

from shared.artifact_paths import (
    analysis_path,
    developer_handoff_path,
    developer_implementation_path,
    generated_tasks_dir,
)
from shared.task_utils import (
    extract_section,
    extract_task_code,
    find_latest_task,
    find_task_by_marker,
    select_next_task,
)

SKIP_PATH_PARTS = {
    ".git",
    ".venv",
    ".idea",
    "__pycache__",
    "analysis",
    "backlog",
    "handoff",
    "implementation",
    "artifacts",
    "templates",
}
TEXT_FILE_SUFFIXES = {".md", ".py", ".sh", ".txt", ".yml", ".yaml", ".json", ".env"}
STOP_WORDS = {
    "about",
    "above",
    "aligned",
    "and",
    "analysis",
    "are",
    "backlog",
    "be",
    "can",
    "concrete",
    "current",
    "define",
    "dependencies",
    "documentation",
    "done",
    "each",
    "exactly",
    "findings",
    "focus",
    "focused",
    "for",
    "from",
    "goal",
    "high",
    "implementation",
    "improve",
    "improving",
    "input",
    "into",
    "introducing",
    "itself",
    "keep",
    "latest",
    "listed",
    "none",
    "one",
    "out",
    "phase",
    "planner",
    "planning",
    "priority",
    "refactors",
    "repository",
    "scope",
    "should",
    "single",
    "specific",
    "task",
    "tasks",
    "testable",
    "that",
    "the",
    "this",
    "through",
    "todo",
    "translate",
    "unrelated",
    "use",
    "with",
    "work",
}
FILE_BLOCK_RE = re.compile(
    r"===FILE:\s*([^\n]+?)\s*===\n(.*?)\n===END===",
    re.DOTALL,
)
STATUS_SECTION_RE = re.compile(r"(^## Status\s*\n)(\S+)", re.MULTILINE)
NOTES_SECTION_RE = re.compile(r"(^## Notes\s*\n)(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate local developer artifacts for a selected backlog task. "
            "This writes a handoff and an implementation prompt; it does not apply repo changes."
        )
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
        help="Print the developer artifacts without writing files.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Use the local OpenAI prompt utility to generate and apply repository changes.",
    )
    return parser.parse_args()


def select_developer_task(
    repo_root: Path,
    goal: str | None,
    workspace_root: Path,
    target_name: str,
    planned_task: tuple[Path, str] | None = None,
) -> tuple[Path, str]:
    if planned_task is not None and not goal:
        return planned_task

    if not goal:
        return select_next_task(workspace_root, target_name)

    marker = f"Planner Follow-up: {goal}"

    if planned_task is not None and marker in planned_task[1]:
        return planned_task

    candidate_dirs = [generated_tasks_dir(workspace_root, target_name), workspace_root / "backlog" / "tasks"]
    for task_dir in candidate_dirs:
        matching_task = find_task_by_marker(task_dir, marker)
        if matching_task is not None:
            return matching_task

    for task_dir in candidate_dirs:
        latest_task = find_latest_task(task_dir)
        if latest_task is not None:
            return latest_task, latest_task.read_text(encoding="utf-8")

    if planned_task is not None:
        return planned_task
    raise FileNotFoundError("Developer phase requires at least one backlog task in the target-scoped workspace backlog.")


def update_task_status(markdown: str, status: str) -> str:
    if STATUS_SECTION_RE.search(markdown) is None:
        return markdown
    return STATUS_SECTION_RE.sub(rf"\1{status}", markdown, count=1)


def append_task_note(markdown: str, note: str) -> str:
    formatted_note = f"- {note.strip()}"

    match = NOTES_SECTION_RE.search(markdown)
    if match is None:
        trimmed = markdown.rstrip()
        return f"{trimmed}\n\n## Notes\n{formatted_note}\n"

    existing = match.group(2).rstrip()
    replacement = f"{match.group(1)}{existing}\n{formatted_note}\n"
    return NOTES_SECTION_RE.sub(replacement, markdown, count=1)


def normalize_executed_task_content(markdown: str) -> str:
    current_status = extract_section(markdown, "Status").strip().lower()
    if current_status == "blocked":
        return update_task_status(markdown, "blocked")
    return update_task_status(markdown, "in-progress")


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


def read_developer_prompt(repo_root: Path) -> str:
    prompt_path = repo_root / "prompts" / "agents" / "developer.md"
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8").strip()

    return dedent(
        """\
        # Developer Agent Prompt

        You are the Developer Agent.
        Implement exactly one approved backlog task in a focused change set.
        """
    ).strip()


def build_keyword_set(*values: str) -> list[str]:
    keywords: list[str] = []
    seen: set[str] = set()

    for value in values:
        for token in re.findall(r"[a-z0-9]+", value.lower()):
            if len(token) < 4 or token in STOP_WORDS:
                continue
            if token not in seen:
                seen.add(token)
                keywords.append(token)

    return keywords


def extract_explicit_repo_paths(
    repo_root: Path,
    task_path: Path,
    task_content: str,
) -> list[Path]:
    explicit_paths: list[Path] = []
    seen: set[Path] = set()

    for raw_value in re.findall(r"`([^`\n]+)`", task_content):
        candidate_text = raw_value.strip()
        if (
            not candidate_text
            or " " in candidate_text
            or candidate_text.endswith("/")
            or candidate_text.startswith("TASK-")
        ):
            continue

        candidate = (repo_root / candidate_text).resolve()
        if repo_root not in candidate.parents and candidate != repo_root:
            continue
        if candidate == task_path:
            continue

        rel_candidate = candidate.relative_to(repo_root)
        if not rel_candidate.suffix and not candidate.exists():
            continue

        if rel_candidate == Path(".env") or rel_candidate.name.startswith(".env."):
            continue

        if any(part in SKIP_PATH_PARTS for part in rel_candidate.parts):
            continue

        if candidate not in seen:
            seen.add(candidate)
            explicit_paths.append(candidate)

    return explicit_paths


def suggest_likely_files(
    repo_root: Path,
    task_path: Path,
    goal: str,
    task_content: str,
    limit: int = 5,
) -> list[Path]:
    objective = extract_section(task_content, "Objective")
    scope = extract_section(task_content, "Scope")
    keywords = build_keyword_set(goal, objective, scope, task_path.stem.replace("-", " "))

    suggestions: list[Path] = [task_path]
    explicit_paths = extract_explicit_repo_paths(
        repo_root=repo_root,
        task_path=task_path,
        task_content=scope,
    )

    for path in explicit_paths:
        if path not in suggestions:
            suggestions.append(path)

    scored: list[tuple[int, str, Path]] = []
    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue
        rel_path = path.relative_to(repo_root)
        if path == task_path:
            continue
        if rel_path == Path(".env") or rel_path.name.startswith(".env."):
            continue
        if path.suffix.lower() not in TEXT_FILE_SUFFIXES:
            continue
        if any(part in SKIP_PATH_PARTS for part in rel_path.parts):
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        lowered = f"{rel_path.as_posix()}\n{text}".lower()
        score = 0
        for keyword in keywords:
            if keyword in lowered:
                score += lowered.count(keyword)
        if score <= 0:
            continue

        scored.append((score, rel_path.as_posix(), path))

    scored.sort(key=lambda item: (-item[0], item[1]))
    for _, _, path in scored:
        if path not in suggestions:
            suggestions.append(path)
        if len(suggestions) >= limit:
            break

    return suggestions[:limit]


def build_task_summary(task_content: str) -> str:
    summary_parts: list[str] = []

    objective = extract_section(task_content, "Objective").strip()
    if objective:
        summary_parts.append(f"Objective: {objective}")

    scope_items = section_items(task_content, "Scope")
    if scope_items:
        summary_parts.append("Scope:\n" + "\n".join(f"- {item}" for item in scope_items))

    acceptance_items = section_items(task_content, "Acceptance Criteria")
    if acceptance_items:
        summary_parts.append("Acceptance Criteria:\n" + "\n".join(f"- {item}" for item in acceptance_items))

    return "\n\n".join(summary_parts).strip()


def build_file_snapshot(repo_root: Path, path: Path) -> str:
    rel_path = path.relative_to(repo_root).as_posix()
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = path.read_text(encoding="utf-8", errors="replace")
    return f"===CURRENT FILE: {rel_path}===\n{content}\n===END CURRENT FILE==="


def build_developer_prompt(
    repo_root: Path,
    task_path: Path,
    task_content: str,
    goal: str,
    workspace_root: Path,
    target_name: str,
) -> str:
    developer_prompt = read_developer_prompt(repo_root)
    implementation_plan = "\n".join(
        [
            "1. Review `{task_path}` and confirm the task is still in scope.".format(
                task_path=task_path.relative_to(repo_root).as_posix()
            ),
            "2. Update `{task_path}` status from `todo` to `in-progress` before making changes.".format(
                task_path=task_path.relative_to(repo_root).as_posix()
            ),
            "3. Apply the required repository changes in the listed likely files.",
            "4. Run the smallest relevant verification commands for the changed files.",
            "5. Update `{task_path}` to `done` only after the acceptance criteria are met.".format(
                task_path=task_path.relative_to(repo_root).as_posix()
            ),
            "6. Prepare a concise developer completion report for the reviewer with changed files, assumptions, and verification results.",
        ]
    )

    likely_files = suggest_likely_files(repo_root, task_path, goal, task_content)
    likely_files_text = "\n".join(
        f"- {path.relative_to(repo_root).as_posix()}" for path in likely_files
    ) or "- (determine during implementation)"

    acceptance = section_items(task_content, "Acceptance Criteria")
    acceptance_text = "\n".join(f"- {item}" for item in acceptance) or "- (none listed)"

    snapshot_paths: list[Path] = []
    for candidate in [task_path, *likely_files]:
        if candidate not in snapshot_paths:
            snapshot_paths.append(candidate)
    file_snapshots = "\n\n".join(build_file_snapshot(repo_root, path) for path in snapshot_paths)

    return dedent(
        f"""\
        # Developer Implementation Prompt

        ## Date
        {dt.datetime.now(dt.timezone.utc).date().isoformat()}

        ## Selected Task
        - Code: {extract_task_code(task_path)}
        - File: `{task_path.relative_to(repo_root).as_posix()}`
        - Goal: {goal}

        ## Implementation Objective
        {extract_section(task_content, "Objective").strip()}

        ## Exact Files Likely To Change
        {likely_files_text}

        ## Exact Constraints
        - Implement exactly one approved backlog task in a focused change set.
        - Keep changes scoped to the selected task `{task_path.relative_to(repo_root).as_posix()}`.
        - Avoid unrelated refactors.
        - Update task status from `todo` to `in-progress` before implementation and to `done` only after verification.
        - If blocked, set the task status to `blocked` and explain why.
        {chr(10).join(f"- Out of scope: {item}" for item in section_items(task_content, "Out of Scope"))}

        ## Exact Acceptance Criteria
        {acceptance_text}

        ## Step-by-Step Implementation Plan
        {implementation_plan}

        ## Copy-Paste Prompt For The Coding Agent
        ````text
        {developer_prompt}

        Repository path: `{repo_root}`
        Goal: {goal}
        Selected task file: `{task_path.relative_to(repo_root).as_posix()}`

        Files likely to change:
        {likely_files_text}

        Constraints:
        - Implement exactly one approved backlog task in a focused change set.
        - Keep changes scoped to the selected task `{task_path.relative_to(repo_root).as_posix()}`.
        - Avoid unrelated refactors.
        - Update task status from `todo` to `in-progress` before implementation and to `done` only after verification.
        - If blocked, set the task status to `blocked` and explain why.
        {chr(10).join(f"- Out of scope: {item}" for item in section_items(task_content, "Out of Scope"))}

        Acceptance criteria:
        {acceptance_text}

        Implementation plan:
        {implementation_plan}

        Selected task content:
        ```md
        {task_content.strip()}
        ```

        Current file snapshots:
        {file_snapshots}

        Return only file blocks in this exact format:
        ===FILE: relative/path/from/repo/root===
        <full file contents>
        ===END===

        Execution rules:
        - Apply the minimum repository changes needed to implement the task.
        - Keep changes small and focused.
        - Avoid unrelated refactors.
        - You may update the selected task file if needed, but do not set it to `done`.
        - Prefer the likely files already listed in the implementation brief.
        - Do not output explanations, markdown fences, or any text outside the file blocks.
        ````
        """
    ).strip() + "\n"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def parse_coding_agent_response(response_text: str) -> list[tuple[Path, str]]:
    matches = FILE_BLOCK_RE.findall(response_text)
    parsed: list[tuple[Path, str]] = []
    for raw_path, body in matches:
        parsed.append((Path(raw_path.strip()), body))
    return parsed


def run_openai_prompt(prompt_text: str, repo_root: Path) -> str:
    encoded_prompt = base64.b64encode(prompt_text.encode("utf-8")).decode("ascii")
    command = (
        "python - <<'PY'\n"
        "import base64, os, subprocess, sys\n"
        "prompt = base64.b64decode(os.environ['DEVELOPER_PROMPT_B64']).decode('utf-8')\n"
        "proc = subprocess.run(['opencode', 'prompt', prompt], capture_output=True, text=True)\n"
        "sys.stdout.write(proc.stdout)\n"
        "sys.stderr.write(proc.stderr)\n"
        "sys.exit(proc.returncode)\n"
        "PY"
    )
    result = subprocess.run(
        ["bash", "-lc", command],
        cwd=repo_root,
        env={**os.environ, "DEVELOPER_PROMPT_B64": encoded_prompt},
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "Developer execution failed with exit code "
            f"{result.returncode}: {result.stderr.strip() or result.stdout.strip()}"
        )
    return result.stdout


def git_has_staged_changes(repo_root: Path) -> bool:
    result = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=repo_root,
        check=False,
    )
    return result.returncode == 1


def git_commit(repo_root: Path, message: str) -> None:
    subprocess.run(["git", "commit", "-m", message], cwd=repo_root, check=True)


def git_push(repo_root: Path) -> None:
    subprocess.run(["git", "push"], cwd=repo_root, check=True)


def git_head_commit_hash(repo_root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def stage_paths(repo_root: Path, paths: list[Path]) -> None:
    if not paths:
        return
    rel_paths = [path.relative_to(repo_root).as_posix() for path in paths]
    subprocess.run(["git", "add", *rel_paths], cwd=repo_root, check=True)


def build_developer_handoff(
    *,
    goal: str,
    task_path: Path,
    task_content: str,
    implementation_path: Path,
    changed_files: list[Path],
    verification_commands: list[str],
    verification_outcomes: list[str],
    assumptions: list[str] | None = None,
    open_questions: list[str] | None = None,
    risks: list[str] | None = None,
    recommended_next_step: str = "Reviewer should inspect the pushed commit and verify acceptance criteria against the committed task snapshot.",
    pushed_commit_hash: str = "pending",
) -> str:
    changed_files_text = "\n".join(f"- {path.as_posix()}" for path in changed_files) if changed_files else "- None recorded"
    assumptions_text = "\n".join(f"- {item}" for item in (assumptions or ["No additional assumptions recorded."]))
    verification_text = "\n".join(
        f"- `{command}` — {outcome}"
        for command, outcome in zip(verification_commands, verification_outcomes)
    ) or "- No verification commands recorded."
    open_questions_text = "\n".join(f"- {item}" for item in (open_questions or ["None."]))
    risks_text = "\n".join(f"- {item}" for item in (risks or ["None beyond normal reviewer validation."]))

    return dedent(
        f"""\
        ## Context
        - Goal: {goal}
        - Selected task: `{task_path.as_posix()}`
        - Task status at handoff time: `{extract_section(task_content, "Status").strip()}`

        ## Decisions
        - Kept the change set focused to the selected backlog task scope.
        - Prepared reviewer-facing artifacts in the target-scoped workspace layout before final push so review can use a coherent committed snapshot.

        ## Artifacts
        - Changed files:
        {changed_files_text}
        - Developer implementation prompt: `{implementation_path.as_posix()}`
        - Assumptions:
        {assumptions_text}
        - Verification commands:
        {verification_text}
        - Pushed commit hash: `{pushed_commit_hash}`

        ## Open Questions / Risks
        {open_questions_text}
        {risks_text}

        ## Recommended Next Step
        - {recommended_next_step}
        """
    ).strip() + "\n"


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo).resolve()
    workspace_root = repo_root / "agents"
    target_name = repo_root.name

    planned_task = None
    planner_task_dir = generated_tasks_dir(workspace_root, target_name)
    try:
        planned_task_path, planned_task_content = select_next_task(workspace_root, target_name)
        planned_task = (planned_task_path, planned_task_content)
    except FileNotFoundError:
        planned_task = None

    task_path, original_task_content = select_developer_task(
        repo_root=repo_root,
        goal=args.goal,
        workspace_root=workspace_root,
        target_name=target_name,
        planned_task=planned_task,
    )
    goal = args.goal or extract_section(original_task_content, "Objective").strip() or task_path.stem

    normalized_task_content = normalize_executed_task_content(original_task_content)
    implementation_text = build_developer_prompt(
        repo_root=repo_root,
        task_path=task_path,
        task_content=normalized_task_content,
        goal=goal,
        workspace_root=workspace_root,
        target_name=target_name,
    )

    task_code = extract_task_code(task_path).lower()
    implementation_path = developer_implementation_path(workspace_root, target_name, task_code)
    handoff_path = developer_handoff_path(workspace_root, target_name, task_code)

    preflight_handoff = build_developer_handoff(
        goal=goal,
        task_path=task_path.relative_to(repo_root),
        task_content=normalized_task_content,
        implementation_path=implementation_path.relative_to(repo_root),
        changed_files=[],
        verification_commands=[],
        verification_outcomes=[],
    )

    if args.dry_run:
        print("===TASK===")
        print(normalized_task_content.rstrip())
        print("===IMPLEMENTATION===")
        print(implementation_text.rstrip())
        print("===HANDOFF===")
        print(preflight_handoff.rstrip())
        return 0

    write_text(task_path, normalized_task_content)
    write_text(implementation_path, implementation_text)
    write_text(handoff_path, preflight_handoff)

    if not args.execute:
        print(f"Updated task status to in-progress: {task_path.relative_to(repo_root)}")
        print(f"Wrote implementation prompt: {implementation_path.relative_to(repo_root)}")
        print(f"Wrote developer handoff: {handoff_path.relative_to(repo_root)}")
        return 0

    response_text = run_openai_prompt(implementation_text, repo_root)
    parsed_files = parse_coding_agent_response(response_text)
    if not parsed_files:
        raise RuntimeError("Developer execution did not return any file blocks to apply.")

    changed_repo_files: list[Path] = []
    for relative_path, content in parsed_files:
        destination = (repo_root / relative_path).resolve()
        if repo_root not in destination.parents and destination != repo_root:
            raise RuntimeError(f"Refusing to write outside repository: {relative_path}")
        write_text(destination, content)
        changed_repo_files.append(destination.relative_to(repo_root))

    final_task_text = task_path.read_text(encoding="utf-8")
    final_task_text = update_task_status(final_task_text, "done")
    write_text(task_path, final_task_text)

    verification_commands = [
        "python -m py_compile scripts/run_developer.py scripts/run_reviewer.py",
    ]
    verification_outcomes: list[str] = []
    for command in verification_commands:
        result = subprocess.run(
            ["bash", "-lc", command],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            verification_outcomes.append("passed")
        else:
            details = result.stderr.strip() or result.stdout.strip() or f"failed with exit code {result.returncode}"
            verification_outcomes.append(f"failed: {details}")

    artifacts_to_commit = {
        task_path,
        implementation_path,
        handoff_path,
    }
    stage_paths(repo_root, sorted(artifacts_to_commit))

    if not git_has_staged_changes(repo_root):
        raise RuntimeError("Developer execution produced no staged changes to commit.")

    commit_message = f"{extract_task_code(task_path)} complete"
    git_commit(repo_root, commit_message)
    pushed_commit_hash = git_head_commit_hash(repo_root)

    final_handoff = build_developer_handoff(
        goal=goal,
        task_path=task_path.relative_to(repo_root),
        task_content=task_path.read_text(encoding="utf-8"),
        implementation_path=implementation_path.relative_to(repo_root),
        changed_files=sorted(changed_repo_files),
        verification_commands=verification_commands,
        verification_outcomes=verification_outcomes,
        pushed_commit_hash=pushed_commit_hash,
    )
    write_text(handoff_path, final_handoff)
    stage_paths(repo_root, [handoff_path])
    if git_has_staged_changes(repo_root):
        subprocess.run(["git", "commit", "--amend", "--no-edit"], cwd=repo_root, check=True)
        pushed_commit_hash = git_head_commit_hash(repo_root)
        final_handoff = build_developer_handoff(
            goal=goal,
            task_path=task_path.relative_to(repo_root),
            task_content=task_path.read_text(encoding="utf-8"),
            implementation_path=implementation_path.relative_to(repo_root),
            changed_files=sorted(changed_repo_files),
            verification_commands=verification_commands,
            verification_outcomes=verification_outcomes,
            pushed_commit_hash=pushed_commit_hash,
        )
        write_text(handoff_path, final_handoff)
        stage_paths(repo_root, [handoff_path])
        if git_has_staged_changes(repo_root):
            subprocess.run(["git", "commit", "--amend", "--no-edit"], cwd=repo_root, check=True)
            pushed_commit_hash = git_head_commit_hash(repo_root)

    git_push(repo_root)

    print(f"Applied developer changes for {task_path.relative_to(repo_root)}")
    print(f"Implementation prompt: {implementation_path.relative_to(repo_root)}")
    print(f"Developer handoff: {handoff_path.relative_to(repo_root)}")
    print(f"Pushed commit hash: {pushed_commit_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
