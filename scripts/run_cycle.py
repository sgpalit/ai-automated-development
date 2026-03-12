#!/usr/bin/env python3
"""Thin orchestrator for the local multi-agent workflow phases."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Callable

from run_analyst import run_analyst_phase
from run_developer import run_developer_phase
from run_planner import PlannerPhaseResult, run_planner_phase
from run_reviewer import run_reviewer_phase
from run_tester import run_tester_phase
from shared.target_repo_config import (
    DEFAULT_REPOSITORY_STATE,
    SUPPORTED_REPOSITORY_STATES,
    resolve_target_repo_config,
)

PHASE_ORDER = ["analyst", "planner", "developer", "reviewer", "tester"]
DEFAULT_AUTOMATION_GOAL = (
    "Advance the next missing MVP item from docs/mvp.md using the next eligible backlog task."
)
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a thin-slice AI-dev cycle against this repository."
    )
    parser.add_argument(
        "goal",
        nargs="?",
        help=(
            "Human goal for this cycle. If omitted, the runner uses docs/mvp.md as "
            "context and selects the next eligible backlog task automatically."
        ),
    )
    parser.add_argument(
        "--phase",
        choices=["analyst", "planner", "developer", "reviewer", "tester"],
        default="planner",
        help=(
            "Last phase to run. analyst runs analyst only; planner runs analyst+planner; "
            "developer runs analyst+planner+developer; "
            "reviewer runs analyst+planner+developer+reviewer; "
            "tester runs analyst+planner+developer+reviewer+tester."
        ),
    )
    parser.add_argument(
        "--repo",
        default=None,
        help="Explicit target repository path. Overrides the selected target config.",
    )
    parser.add_argument(
        "--target-config",
        default=None,
        help=(
            "Target repository config name or .properties path. "
            "If omitted, config/targets/default.properties is used when present."
        ),
    )
    parser.add_argument(
        "--target-repository-state",
        choices=SUPPORTED_REPOSITORY_STATES,
        default=None,
        help=(
            "Explicit target repository state for this run. Overrides the selected target config."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print outputs without writing files.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="When the developer phase runs, use the local execution mode to apply repository changes.",
    )
    return parser.parse_args()
def apply_repository_state_rules(args: argparse.Namespace, state: str) -> None:
    if state == "PROD" and args.execute:
        raise ValueError(
            "Execution mode is disabled for PROD target repository state. "
            "Re-run without --execute."
        )

    if state == "MVP" and args.phase == "tester":
        print(
            "Repository state MVP limits the local runner to reviewer phase while "
            "MVP delivery is still in progress. Adjusting --phase tester to reviewer."
        )
        args.phase = "reviewer"

    if state == "MVP_DONE" and args.phase in {"reviewer", "tester"}:
        print(
            "Repository state MVP_DONE limits the local runner to developer phase "
            "until explicit TEST validation is requested. Adjusting the target phase "
            f"from {args.phase} to developer."
        )
        args.phase = "developer"

    if state == "TEST" and args.phase == "analyst":
        print(
            "Repository state TEST selected. Analyst-only runs are allowed, "
            "but downstream dry-run verification is recommended."
        )

    if state == "PROD" and args.phase in {"developer", "reviewer", "tester"}:
        print(
            "Repository state PROD limits the local runner to planner phase to avoid "
            "implementation or validation changes against a production target. "
            f"Adjusting the target phase from {args.phase} to planner."
        )
        args.phase = "planner"

    if state == "MVP_DONE" and not args.goal:
        print(
            "Repository state MVP_DONE indicates MVP delivery is complete. "
            "Default automation goal remains available for follow-on backlog work."
        )


def main() -> int:
    args = parse_args()
    workspace_root = Path(".").resolve()
    target_config = resolve_target_repo_config(
        workspace_root,
        cli_repo=args.repo,
        cli_state=args.target_repository_state,
        config_name=args.target_config,
    )
    repo_root = target_config.path
    repository_state = target_config.repository_state
    apply_repository_state_rules(args, repository_state)

    planner_result: PlannerPhaseResult | None = None
    analyst_goal = args.goal or DEFAULT_AUTOMATION_GOAL

    if target_config.source_path is not None:
        print(
            f"Target repository config: {target_config.name} "
            f"({target_config.source_path.relative_to(workspace_root)})"
        )
    else:
        print("Target repository config: ad-hoc CLI/default settings")
    print(f"Target repository path: {repo_root}")
    print(f"Target repository state: {repository_state}")

    if not args.goal:
        print(
            "No goal provided. Defaulting to docs/mvp.md context and the next eligible backlog task."
        )

    def analyst_handler() -> None:
        run_analyst_phase(
            goal=analyst_goal,
            target_repo_root=repo_root,
            workspace_root=workspace_root,
            target_name=target_config.name,
            dry_run=args.dry_run,
        )

    def planner_handler() -> None:
        nonlocal planner_result
        planner_result = run_planner_phase(
            goal=args.goal,
            target_repo_root=repo_root,
            workspace_root=workspace_root,
            target_name=target_config.name,
            dry_run=args.dry_run,
        )

    def developer_handler() -> None:
        run_developer_phase(
            goal=args.goal,
            repo_root=repo_root,
            workspace_root=workspace_root,
            target_name=target_config.name,
            dry_run=args.dry_run,
            execute=args.execute,
            planned_task=planner_result.task_artifact if planner_result else None,
        )

    def reviewer_handler() -> None:
        run_reviewer_phase(
            goal=args.goal,
            repo_root=repo_root,
            workspace_root=workspace_root,
            target_name=target_config.name,
            dry_run=args.dry_run,
            planned_task=planner_result.task_artifact if planner_result else None,
        )

    def tester_handler() -> None:
        run_tester_phase(
            goal=args.goal,
            repo_root=repo_root,
            workspace_root=workspace_root,
            target_name=target_config.name,
            dry_run=args.dry_run,
            planned_task=planner_result.task_artifact if planner_result else None,
        )

    handlers: dict[str, Callable[[], None]] = {
        "analyst": analyst_handler,
        "planner": planner_handler,
        "developer": developer_handler,
        "reviewer": reviewer_handler,
        "tester": tester_handler,
    }

    stop_idx = PHASE_ORDER.index(args.phase)
    for phase in PHASE_ORDER[: stop_idx + 1]:
        if phase in handlers:
            print(f"Running phase: {phase}")
            run_phase(phase, handlers)
            if (
                phase == "planner"
                and planner_result is not None
                and not planner_result.continue_to_implementation
            ):
                break
        else:
            print(f"Skipping unimplemented phase: {phase}")

    return 0


def run_phase(phase: str, handlers: dict[str, Callable[[], None]]) -> None:
    handler = handlers.get(phase)
    if handler is None:
        raise ValueError(f"Phase '{phase}' is not implemented yet.")
    handler()


if __name__ == "__main__":
    raise SystemExit(main())
