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
        if len(suggestions) >= limit:
            return suggestions

    if explicit_paths:
        return suggestions

    scored_candidates: list[tuple[int, Path]] = []

    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue
        if path == task_path:
            continue
        if any(part in SKIP_PATH_PARTS for part in path.parts):
            continue
        if path.suffix.lower() not in TEXT_FILE_SUFFIXES:
            continue

        rel_path = path.relative_to(repo_root)
        rel_text = str(rel_path).lower()
        score = 0

        if rel_path == Path(".env") or rel_path.name.startswith(".env."):
            continue

        try:
            preview = path.read_text(encoding="utf-8")[:4000].lower()
        except (OSError, UnicodeDecodeError):
            preview = ""

        if rel_path == Path("README.md"):
            score += 2
        if "docs" in rel_path.parts:
            score += 2

        if any(token in {"docs", "documentation", "onboarding", "guide", "readme", "setup"} for token in keywords):
            if rel_path == Path("README.md"):
                score += 4
            if "docs" in rel_path.parts:
                score += 4

        for token in keywords:
            if token in rel_path.stem.lower():
                score += 8
            if token in rel_text:
                score += 4
            if preview and token in preview:
                score += 2

        if score <= 0:
            continue

        scored_candidates.append((score, path))

    for _score, path in sorted(scored_candidates, key=lambda item: (-item[0], str(item[1]))):
        if path not in suggestions:
            suggestions.append(path)
        if len(suggestions) >= limit:
            break

    return suggestions


def build_step_plan(task_path: Path, likely_files: list[Path], repo_root: Path) -> list[str]:
    plan = [
        f"Review `{task_path.relative_to(repo_root)}` and confirm the task is still in scope.",
        f"Update `{task_path.relative_to(repo_root)}` status from `todo` to `in-progress` before making changes.",
    ]

    if len(likely_files) > 1:
        target_paths = ", ".join(f"`{path.relative_to(repo_root)}`" for path in likely_files[1:])
        plan.append(f"Apply the required repository changes in {target_paths}.")
    else:
        plan.append("Identify the minimum repository files needed to satisfy the task objective and acceptance criteria.")

    plan.extend(
        [
            "Run the smallest relevant verification commands for the changed files.",
            f"Update `{task_path.relative_to(repo_root)}` to `done` only after the acceptance criteria are met.",
            "Prepare a concise developer completion report for the reviewer with changed files, assumptions, and verification results.",
        ]
    )
    return plan


def build_coding_agent_prompt(
    developer_prompt: str,
    goal: str,
    repo_root: Path,
    task_path: Path,
    task_content: str,
    likely_files: list[Path],
    constraints: str,
    acceptance_criteria: str,
    step_plan: list[str],
) -> str:
    likely_files_text = "\n".join(
        f"- `{path.relative_to(repo_root)}`" for path in likely_files
    )
    step_plan_text = "\n".join(f"{idx}. {step}" for idx, step in enumerate(step_plan, start=1))

    return f"""{developer_prompt}

Repository path: `{repo_root}`
Goal: {goal}
Selected task file: `{task_path.relative_to(repo_root)}`

Files likely to change:
{likely_files_text}

Constraints:
{constraints}

Acceptance criteria:
{acceptance_criteria}

Implementation plan:
{step_plan_text}

Selected task content:
```md
{task_content}
```
"""


def build_implementation_prompt_markdown(
    goal: str,
    repo_root: Path,
    task_path: Path,
    task_content: str,
) -> str:
    today = dt.date.today().isoformat()
    task_code = extract_task_code(task_path)
    objective = extract_section(task_content, "Objective")
    out_of_scope_items = section_items(task_content, "Out of Scope")
    acceptance_criteria_items = section_items(task_content, "Acceptance Criteria")
    developer_prompt = read_developer_prompt(repo_root)
    likely_files = suggest_likely_files(
        repo_root=repo_root,
        task_path=task_path,
        goal=goal,
        task_content=task_content,
    )

    likely_files_text = "\n".join(
        f"- `{path.relative_to(repo_root)}`" for path in likely_files
    )
    constraints_items = [
        "Implement exactly one approved backlog task in a focused change set.",
        f"Keep changes scoped to the selected task `{task_path.relative_to(repo_root)}`.",
        "Avoid unrelated refactors.",
        "Update task status from `todo` to `in-progress` before implementation and to `done` only after verification.",
        "If blocked, set the task status to `blocked` and explain why.",
    ]
    constraints_items.extend(f"Out of scope: {item}" for item in out_of_scope_items)
    constraints = "\n".join(f"- {item}" for item in constraints_items)
    acceptance_criteria_text = "\n".join(
        f"- {item}" for item in acceptance_criteria_items
    ) or "- None"
    step_plan = build_step_plan(task_path=task_path, likely_files=likely_files, repo_root=repo_root)
    step_plan_text = "\n".join(f"{idx}. {step}" for idx, step in enumerate(step_plan, start=1))
    coding_agent_prompt = build_coding_agent_prompt(
        developer_prompt=developer_prompt,
        goal=goal,
        repo_root=repo_root,
        task_path=task_path,
        task_content=task_content,
        likely_files=likely_files,
        constraints=constraints,
        acceptance_criteria=acceptance_criteria_text,
        step_plan=step_plan,
    )

    return f"""# Developer Implementation Prompt

## Date
{today}

## Selected Task
- Code: `{task_code}`
- File: `{task_path.relative_to(repo_root)}`
- Goal: {goal}

## Implementation Objective
{objective}

## Exact Files Likely To Change
{likely_files_text}

## Exact Constraints
{constraints}

## Exact Acceptance Criteria
{acceptance_criteria_text}

## Step-by-Step Implementation Plan
{step_plan_text}

## Copy-Paste Prompt For The Coding Agent
````text
{coding_agent_prompt}
````
"""


def build_file_snapshot(path: Path, repo_root: Path, max_chars: int = 8000) -> str:
    rel_path = path.relative_to(repo_root)
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return f"===CURRENT FILE: {rel_path}===\n<unreadable>\n===END CURRENT FILE==="

    trimmed = content[:max_chars]
    if len(content) > max_chars:
        trimmed += "\n... [truncated]"

    return f"===CURRENT FILE: {rel_path}===\n{trimmed}\n===END CURRENT FILE==="


def build_execution_prompt(
    goal: str,
    repo_root: Path,
    task_path: Path,
    task_content: str,
    implementation_content: str,
    likely_files: list[Path],
) -> str:
    current_files = "\n\n".join(
        build_file_snapshot(path=path, repo_root=repo_root)
        for path in likely_files
        if path.exists()
    )

    return f"""{read_developer_prompt(repo_root)}

You are executing the selected backlog task inside this repository:
`{repo_root}`

Goal:
{goal}

Selected task file:
`{task_path.relative_to(repo_root)}`

Current selected task content:
```md
{task_content}
```

Implementation brief:
```md
{implementation_content}
```

Current file snapshots:
{current_files}

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
"""


def parse_file_blocks(text: str) -> list[tuple[str, str]]:
    return [(name.strip(), body.strip() + "\n") for name, body in FILE_BLOCK_RE.findall(text)]


def validate_output_path(repo_root: Path, task_path: Path, relative_path: str) -> Path:
    path = (repo_root / relative_path).resolve()
    if repo_root not in path.parents and path != repo_root:
        raise ValueError(f"Developer execution attempted to write outside the repository: {relative_path}")

    rel_path = path.relative_to(repo_root)
    if any(part in {".git", "handoff", "implementation", "artifacts", "analysis"} for part in rel_path.parts):
        raise ValueError(f"Developer execution attempted to write a protected path: {relative_path}")

    if rel_path == Path(".env") or rel_path.name.startswith(".env."):
        raise ValueError(f"Developer execution attempted to modify a protected local environment file: {relative_path}")

    if rel_path.parts and rel_path.parts[0] == "backlog" and path != task_path:
        raise ValueError(f"Developer execution attempted to modify an unexpected backlog file: {relative_path}")

    return path


def apply_file_blocks(
    repo_root: Path,
    task_path: Path,
    blocks: list[tuple[str, str]],
    dry_run: bool,
) -> list[Path]:
    written_paths: list[Path] = []
    seen_paths: set[Path] = set()

    for relative_path, body in blocks:
        target = validate_output_path(repo_root=repo_root, task_path=task_path, relative_path=relative_path)
        if target in seen_paths:
            raise ValueError(f"Developer execution returned duplicate file blocks for: {relative_path}")
        seen_paths.add(target)

        if target == task_path:
            body = normalize_executed_task_content(body)

        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(body, encoding="utf-8")
        written_paths.append(target)

    return written_paths


def execute_developer_changes(
    goal: str,
    repo_root: Path,
    task_path: Path,
    task_content: str,
    implementation_content: str,
    dry_run: bool,
) -> list[Path]:
    likely_files = suggest_likely_files(
        repo_root=repo_root,
        task_path=task_path,
        goal=goal,
        task_content=task_content,
    )
    execution_prompt = build_execution_prompt(
        goal=goal,
        repo_root=repo_root,
        task_path=task_path,
        task_content=task_content,
        implementation_content=implementation_content,
        likely_files=likely_files,
    )

    if dry_run:
        print("[dry-run] Would execute coding agent with the generated implementation prompt.")
        return []

    from llm import run_prompt

    output = run_prompt(execution_prompt)
    blocks = parse_file_blocks(output)
    if not blocks:
        raise RuntimeError("Developer execution returned no file blocks to apply.")

    return apply_file_blocks(
        repo_root=repo_root,
        task_path=task_path,
        blocks=blocks,
        dry_run=dry_run,
    )


def build_developer_handoff_markdown(
    goal: str,
    repo_root: Path,
    workspace_root: Path,
    target_name: str,
    task_path: Path,
    task_content: str,
    pushed_commit_hash: str | None = None,
) -> str:
    today = dt.date.today().isoformat()
    task_code = extract_task_code(task_path)
    source_task_path = task_path.relative_to(repo_root)
    objective = extract_section(task_content, "Objective")

    required_inputs = [
        f"`{source_task_path}`",
        f"`{analysis_path(workspace_root, target_name).relative_to(workspace_root)}`",
        "`AGENTS.md`",
        "`docs/agent-workflow.md`",
        "`docs/agent-handoff-contract.md`",
    ]
    implementation_rules = [
        "Implement exactly one approved backlog task in a focused change set.",
        "Set the selected task status to `in-progress` before implementation.",
        "Implement only in-scope changes required by the task.",
        "Keep unrelated refactors out of scope.",
        "Run relevant checks before completion.",
        "Set task status to `done` when acceptance criteria are met, or `blocked` if work cannot proceed.",
    ]
    expected_output = [
        "A small, working repository change set that implements the selected task.",
        "The selected backlog task updated through the required status transitions.",
        "A developer handoff/report aligned with `docs/agent-handoff-contract.md` and ready for reviewer follow-up.",
        f"Pushed commit hash for reviewer reference: `{pushed_commit_hash or 'pending'}`",
    ]
    commit_notes = [
        "- Reviewer should inspect the pushed commit referenced below, not only the local worktree."
        if pushed_commit_hash
        else "- No pushed commit is recorded yet. A successful `--execute` run should update this handoff with the pushed commit hash."
    ]

    required_inputs_text = "\n".join(f"- {item}" for item in required_inputs)
    implementation_rules_text = "\n".join(f"- {item}" for item in implementation_rules)
    expected_output_text = "\n".join(f"- {item}" for item in expected_output)
    commit_notes_text = "\n".join(commit_notes)

    return f"""# Developer Handoff

## Goal
{goal}

## Date
{today}

## Repository Path
`{repo_root}`

## Selected Task Code
`{task_code}`

## Source Task File Path
`{source_task_path}`

## Objective
{objective}

## Required Inputs
{required_inputs_text}

## Implementation Rules
{implementation_rules_text}

## Expected Output
{expected_output_text}

## Commit Reference
- Pushed commit hash: `{pushed_commit_hash or 'pending'}`
{commit_notes_text}

## Full Task Content
```md
{task_content}
```
"""


def git_output(repo_root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def is_git_ignored(repo_root: Path, path: Path) -> bool:
    rel_path = path.relative_to(repo_root)
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", str(rel_path)],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def read_local_env_value(repo_root: Path, key: str) -> str | None:
    env_path = repo_root / ".env"
    if not env_path.exists():
        return None

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        if name.strip() != key:
            continue
        cleaned = value.strip().strip("'").strip('"')
        return cleaned or None

    return None


def resolve_github_token(repo_root: Path) -> str | None:
    token = os.getenv("GITHUB_TOKEN")
    if token:
        return token
    return read_local_env_value(repo_root, "GITHUB_TOKEN")


def github_https_push_url(remote_url: str) -> str | None:
    remote = remote_url.strip()
    if remote.startswith("git@github.com:"):
        return f"https://github.com/{remote.removeprefix('git@github.com:')}"
    if remote.startswith("ssh://git@github.com/"):
        return f"https://github.com/{remote.removeprefix('ssh://git@github.com/')}"
    if remote.startswith("https://github.com/") or remote.startswith("http://github.com/"):
        return remote
    return None


def push_with_github_token(repo_root: Path, branch: str) -> None:
    token = resolve_github_token(repo_root)
    if not token:
        raise RuntimeError(
            "GITHUB_TOKEN is required for HTTPS push because the origin remote uses GitHub and SSH authentication is unavailable."
        )

    remote_url = git_output(repo_root, "remote", "get-url", "origin")
    push_url = github_https_push_url(remote_url)
    if push_url is None:
        raise RuntimeError(
            f"Could not derive an HTTPS GitHub push URL from origin remote: {remote_url}"
        )

    basic_auth = base64.b64encode(f"x-access-token:{token}".encode("utf-8")).decode("ascii")
    result = subprocess.run(
        [
            "git",
            "-c",
            f"http.https://github.com/.extraheader=AUTHORIZATION: basic {basic_auth}",
            "push",
            push_url,
            branch,
        ],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
        env={
            **os.environ,
            "GIT_TERMINAL_PROMPT": "0",
        },
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Authenticated git push failed")


def unique_existing_paths(repo_root: Path, paths: list[Path]) -> list[Path]:
    unique: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        resolved = path.resolve()
        if resolved in seen:
            continue
        if repo_root not in resolved.parents and resolved != repo_root:
            continue
        if not resolved.exists():
            continue
        if is_git_ignored(repo_root, resolved):
            continue
        seen.add(resolved)
        unique.append(resolved)
    return unique


def create_and_push_commit(
    repo_root: Path,
    task_path: Path,
    changed_paths: list[Path],
    dry_run: bool = False,
) -> str:
    staged_paths = unique_existing_paths(repo_root, changed_paths)
    if not staged_paths:
        raise RuntimeError("Developer commit/push workflow has no repository paths to stage.")

    if dry_run:
        print("[dry-run] Would stage paths for commit:")
        for path in staged_paths:
            print(f"- {path.relative_to(repo_root)}")
        print("[dry-run] Would create a focused git commit and push it to origin on the current branch.")
        return "DRY-RUN-COMMIT-HASH"

    relative_paths = [str(path.relative_to(repo_root)) for path in staged_paths]
    git_output(repo_root, "add", "--", *relative_paths)
    commit_message = f"{extract_task_code(task_path)}: complete task"
    git_output(repo_root, "commit", "-m", commit_message)
    pushed_hash = git_output(repo_root, "rev-parse", "HEAD")
    branch = git_output(repo_root, "rev-parse", "--abbrev-ref", "HEAD")
    push_with_github_token(repo_root, branch)
    return pushed_hash


def run_developer_phase(
    goal: str | None,
    repo_root: Path,
    workspace_root: Path,
    target_name: str,
    dry_run: bool,
    execute: bool = False,
    planned_task: tuple[Path, str] | None = None,
) -> tuple[Path, Path, bool]:
    task_path, task_content = select_developer_task(
        repo_root=repo_root,
        goal=goal,
        workspace_root=workspace_root,
        target_name=target_name,
        planned_task=planned_task,
    )
    task_code = extract_task_code(task_path)
    resolved_goal = goal or extract_section(task_content, "Objective") or f"Implement {task_code}"
    handoff_path = developer_handoff_path(workspace_root, target_name, task_code)
    implementation_path = developer_implementation_path(workspace_root, target_name, task_code)
    implementation_dir = implementation_path.parent
    handoff_dir = handoff_path.parent
    implementation_content = build_implementation_prompt_markdown(
        goal=resolved_goal,
        repo_root=repo_root,
        task_path=task_path,
        task_content=task_content,
    )
    pending_handoff = build_developer_handoff_markdown(
        goal=resolved_goal,
        repo_root=repo_root,
        workspace_root=workspace_root,
        target_name=target_name,
        task_path=task_path,
        task_content=task_content,
        pushed_commit_hash=None,
    )
    repo_changes_applied = False
    execution_written_paths: list[Path] = []

    print(f"Developer task selected: {task_path}")

    if dry_run:
        print(f"[dry-run] Would write developer handoff: {handoff_path}")
        print(pending_handoff)
        print(f"[dry-run] Would write implementation prompt: {implementation_path}")
        print(implementation_content)
        if execute:
            in_progress_content = update_task_status(task_content, "in-progress")
            if in_progress_content != task_content:
                print(f"[dry-run] Would update task status to in-progress: {task_path}")
            execute_developer_changes(
                goal=resolved_goal,
                repo_root=repo_root,
                task_path=task_path,
                task_content=in_progress_content,
                implementation_content=implementation_content,
                dry_run=True,
            )
            create_and_push_commit(
                repo_root=repo_root,
                task_path=task_path,
                changed_paths=[task_path, implementation_path],
                dry_run=True,
            )
        print("[dry-run] Actual code changes applied: no")
        return handoff_path, implementation_path, repo_changes_applied

    implementation_dir.mkdir(parents=True, exist_ok=True)
    handoff_dir.mkdir(parents=True, exist_ok=True)
    implementation_path.write_text(implementation_content, encoding="utf-8")
    print(f"Implementation prompt written: {implementation_path}")

    if not execute:
        handoff_path.write_text(pending_handoff, encoding="utf-8")
        print(f"Developer handoff written: {handoff_path}")
        print("Actual code changes applied: no")
        return handoff_path, implementation_path, repo_changes_applied

    in_progress_content = update_task_status(task_content, "in-progress")
    if in_progress_content != task_content:
        task_path.write_text(in_progress_content, encoding="utf-8")
        print(f"Task status updated to in-progress: {task_path}")

    execution_written_paths = execute_developer_changes(
        goal=resolved_goal,
        repo_root=repo_root,
        task_path=task_path,
        task_content=in_progress_content,
        implementation_content=implementation_content,
        dry_run=False,
    )
    repo_changes_applied = any(path != task_path for path in execution_written_paths)
    if execution_written_paths:
        print("Developer execution wrote files:")
        for path in execution_written_paths:
            print(f"- {path}")

    final_task_text = task_path.read_text(encoding="utf-8")
    final_task_text = update_task_status(final_task_text, "done")
    task_path.write_text(final_task_text, encoding="utf-8")

    pushed_commit_hash = create_and_push_commit(
        repo_root=repo_root,
        task_path=task_path,
        changed_paths=execution_written_paths + [task_path, implementation_path],
        dry_run=False,
    )

    handoff_content = build_developer_handoff_markdown(
        goal=resolved_goal,
        repo_root=repo_root,
        workspace_root=workspace_root,
        target_name=target_name,
        task_path=task_path,
        task_content=final_task_text,
        pushed_commit_hash=pushed_commit_hash,
    )
    handoff_path.write_text(handoff_content, encoding="utf-8")
    print(f"Developer handoff written: {handoff_path}")
    print(f"Pushed commit hash: {pushed_commit_hash}")
    print(f"Actual code changes applied: {'yes' if repo_changes_applied else 'no'}")
    return handoff_path, implementation_path, repo_changes_applied


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo).resolve()
    workspace_root = Path(".").resolve()
    target_name = repo_root.name
    run_developer_phase(
        goal=args.goal,
        repo_root=repo_root,
        workspace_root=workspace_root,
        target_name=target_name,
        dry_run=args.dry_run,
        execute=args.execute,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
