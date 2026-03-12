from __future__ import annotations

import argparse
import datetime as dt
import os
from pathlib import Path

from shared.artifact_paths import analysis_path, generated_tasks_dir
from shared.target_repo_config import resolve_target_repo_config

MAX_FILES = 120
MAX_FILE_CHARS = 5000


SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the analyst phase against this repository."
    )
    parser.add_argument(
        "goal",
        nargs="?",
        help="Human goal for the local file-based analyst phase.",
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Target repository path. Defaults to current repository.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the analyst output without writing files.",
    )
    return parser.parse_args()


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


def collect_repo_snapshot(target_repo_root: Path, workspace_root: Path, target_name: str) -> dict[str, object]:
    files = [path for path in target_repo_root.rglob("*") if path.is_file() and ".git" not in path.parts]
    top_level_dirs = sorted(
        [path.name for path in target_repo_root.iterdir() if path.is_dir() and path.name != ".git"]
    )

    def read_if_exists(path: str) -> str:
        candidate = target_repo_root / path
        return candidate.read_text(encoding="utf-8") if candidate.exists() else ""

    readme = read_if_exists("README.md")
    mvp = read_if_exists("docs/mvp.md")
    onboarding = read_if_exists("docs/target-repo-onboarding.md")
    context = read_if_exists("docs/target-repo-context.md")

    return {
        "file_count": len(files),
        "top_level_dirs": top_level_dirs,
        "has_backlog": generated_tasks_dir(workspace_root, target_name).exists(),
        "has_prompts": (workspace_root / "prompts/agents").exists(),
        "readme_preview": "\n".join(readme.splitlines()[:12]),
        "mvp_preview": "\n".join(mvp.splitlines()[:12]),
        "onboarding_preview": "\n".join(onboarding.splitlines()[:12]),
        "context_preview": "\n".join(context.splitlines()[:12]),
    }


def build_analysis_markdown(
    goal: str,
    target_repo_root: Path,
    workspace_root: Path,
    target_name: str,
) -> str:
    snapshot = collect_repo_snapshot(target_repo_root, workspace_root, target_name)
    today = dt.date.today().isoformat()
    analysis_rel_path = analysis_path(workspace_root, target_name).relative_to(workspace_root)

    return f"""## Context
- Goal: {goal}
- Current step: Repository analysis
- Date: {today}
- Inputs reviewed:
  - README.md
  - docs/mvp.md
  - docs/agent-handoff-contract.md
  - docs/target-repo-onboarding.md
  - docs/target-repo-context.md
  - Repository structure under {target_repo_root.resolve()}

## Decisions
- The analysis follows the onboarding and repository-context guidance so planning is grounded in explicit repository evidence.
- A local CLI should keep outputs file-based to preserve human review and easy iteration.
- Analyst output should be regenerated each run to keep planning grounded in current state.

## Artifacts
- {analysis_rel_path}: This analysis snapshot.
- Repository snapshot summary: file count, top-level directories, and documentation previews supporting onboarding intake.

## Open Questions / Risks
- Future phases (developer/reviewer/tester) still need integration points and output contracts.
- Planner output quality is heuristic in this thin-slice and should be reviewed by a human.
- If repository docs are sparse, analyst findings may require human validation before planning.

## Recommended Next Step
- Next agent: Planner
- Instruction: Convert analysis into small, dependency-safe backlog tasks informed by the onboarding checklist and repository-context evidence.

---

## Repository Snapshot
- File count (excluding .git): {snapshot['file_count']}
- Top-level directories: {", ".join(snapshot['top_level_dirs'])}
- agents/backlog/tasks present: {snapshot['has_backlog']}
- prompts/agents present: {snapshot['has_prompts']}

## Analysis Expectations
Use the repository snapshot and reviewed docs to capture:
- repository purpose and expected users
- technology stack and tooling
- structure and architecture clues
- conventions and quality signals
- risks, gaps, and small-slice improvement opportunities

### README.md (preview)
```
{snapshot['readme_preview']}
```

### docs/mvp.md (preview)
```
{snapshot['mvp_preview']}
```

### docs/target-repo-onboarding.md (preview)
```
{snapshot['onboarding_preview']}
```

### docs/target-repo-context.md (preview)
```
{snapshot['context_preview']}
```
"""


def run_analyst_phase(
    goal: str,
    target_repo_root: Path,
    workspace_root: Path,
    target_name: str,
    dry_run: bool,
) -> Path:
    output_path = analysis_path(workspace_root, target_name)
    content = build_analysis_markdown(
        goal=goal,
        target_repo_root=target_repo_root,
        workspace_root=workspace_root,
        target_name=target_name,
    )

    if dry_run:
        print(f"[dry-run] Would write analyst output: {output_path}")
        print(content)
        return output_path

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    print(f"Analyst output written: {output_path}")
    return output_path


def run_llm_analyst(target_repo_root: Path, workspace_root: Path, target_name: str) -> Path:
    from llm import run_prompt

    prompt_path = workspace_root / "prompts" / "agents" / "analyst.md"
    analyst_prompt = prompt_path.read_text(encoding="utf-8")
    repo_snapshot = build_repo_snapshot(target_repo_root)

    full_prompt = (
        f"{analyst_prompt}\n\n"
        "Repository context (truncated for token limits):\n"
        f"{repo_snapshot}\n\n"
        "Write the final analysis content for agents/analysis/repo-analysis.md."
    )

    output = run_prompt(full_prompt)

    output_path = analysis_path(workspace_root, target_name)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output, encoding="utf-8")
    return output_path


def main() -> None:
    args = parse_args()
    if args.goal:
        workspace_root = Path(".").resolve()
        target_repo_root = Path(args.repo).resolve()
        target_name = target_repo_root.name
        run_analyst_phase(
            goal=args.goal,
            target_repo_root=target_repo_root,
            workspace_root=workspace_root,
            target_name=target_name,
            dry_run=args.dry_run,
        )
        return

    from dotenv import load_dotenv

    load_dotenv()
    workspace_root = Path(".").resolve()
    target_config = resolve_target_repo_config(
        workspace_root,
        cli_repo=None,
        cli_state=None,
        config_name=os.getenv("TARGET_REPOSITORY_CONFIG"),
    )
    workspace_root = Path(".").resolve()
    output_path = run_llm_analyst(
        target_repo_root=target_config.path,
        workspace_root=workspace_root,
        target_name=target_config.name,
    )
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
