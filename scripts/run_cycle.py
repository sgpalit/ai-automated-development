#!/usr/bin/env python3
"""Thin orchestrator for the local multi-agent workflow phases."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from run_analyst import run_analyst_phase
from run_developer import run_developer_phase
from run_planner import PlannerPhaseResult, run_planner_phase
from run_reviewer import run_reviewer_phase
from run_tester import run_tester_phase
from shared.artifact_paths import logs_dir
from shared.target_repo_config import (
    SUPPORTED_REPOSITORY_STATES,
    resolve_target_repo_config,
)

PHASE_ORDER = ["analyst", "planner", "developer", "reviewer", "tester"]
DEFAULT_AUTOMATION_GOAL = (
    "Advance the next missing MVP item from docs/mvp.md using the next eligible backlog task."
)
AUTO_CONTINUE_PHASES = {"planner", "developer", "reviewer"}
AUTO_CONTINUE_STOP_REASONS = {
    "single-cycle-requested",
    "repository-state-not-mvp",
    "planner-stopped-no-grounded-next-task",
    "planner-stopped-policy",
    "planner-stopped-other",
    "phase-policy-adjusted",
    "max-cycles-reached",
}


@dataclass(frozen=True)
class ContinuationDecision:
    continue_running: bool
    reason: str
    summary: str
    details: dict[str, object]


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
    parser.add_argument(
        "--auto-continue",
        action="store_true",
        help=(
            "When the target repository state is MVP, continue running eligible "
            "planner/developer/reviewer cycles until a grounded stop condition is reached."
        ),
    )
    parser.add_argument(
        "--max-cycles",
        type=int,
        default=25,
        help="Safety limit for repeated auto-continue cycles. Default: 25.",
    )
    return parser.parse_args()


def apply_repository_state_rules(args: argparse.Namespace, state: str) -> bool:
    phase_adjusted = False

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
        phase_adjusted = True

    if state == "MVP_DONE" and args.phase in {"reviewer", "tester"}:
        print(
            "Repository state MVP_DONE limits the local runner to developer phase "
            "until explicit TEST validation is requested. Adjusting the target phase "
            f"from {args.phase} to developer."
        )
        args.phase = "developer"
        phase_adjusted = True

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
        phase_adjusted = True

    if state == "MVP_DONE" and not args.goal:
        print(
            "Repository state MVP_DONE indicates MVP delivery is complete. "
            "Default automation goal remains available for follow-on backlog work."
        )

    return phase_adjusted


def main() -> int:
    args = parse_args()
    if args.max_cycles < 1:
        raise ValueError("--max-cycles must be at least 1.")

    workspace_root = Path(".").resolve()
    target_config = resolve_target_repo_config(
        workspace_root,
        cli_repo=args.repo,
        cli_state=args.target_repository_state,
        config_name=args.target_config,
    )
    repo_root = target_config.path
    repository_state = target_config.repository_state
    requested_phase = args.phase
    phase_adjusted = apply_repository_state_rules(args, repository_state)

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

    artifact_dir = logs_dir(workspace_root, target_config.name) / "continuation"
    loop_run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    if not args.auto_continue:
        execute_cycle(
            args=args,
            analyst_goal=analyst_goal,
            repo_root=repo_root,
            workspace_root=workspace_root,
            target_name=target_config.name,
        )
        write_continuation_artifact(
            artifact_dir=artifact_dir,
            run_id=loop_run_id,
            cycle_number=1,
            repository_state=repository_state,
            requested_phase=requested_phase,
            effective_phase=args.phase,
            decision=ContinuationDecision(
                continue_running=False,
                reason="single-cycle-requested",
                summary="Stopped after a single cycle because --auto-continue was not requested.",
                details={},
            ),
            planner_result=None,
            dry_run=args.dry_run,
        )
        return 0

    if repository_state != "MVP":
        execute_cycle(
            args=args,
            analyst_goal=analyst_goal,
            repo_root=repo_root,
            workspace_root=workspace_root,
            target_name=target_config.name,
        )
        write_continuation_artifact(
            artifact_dir=artifact_dir,
            run_id=loop_run_id,
            cycle_number=1,
            repository_state=repository_state,
            requested_phase=requested_phase,
            effective_phase=args.phase,
            decision=ContinuationDecision(
                continue_running=False,
                reason="repository-state-not-mvp",
                summary=(
                    "Stopped after one cycle because auto-continue only runs repeatedly "
                    "while the target repository state is MVP."
                ),
                details={"resolved_repository_state": repository_state},
            ),
            planner_result=None,
            dry_run=args.dry_run,
        )
        return 0

    if args.phase not in AUTO_CONTINUE_PHASES:
        execute_cycle(
            args=args,
            analyst_goal=analyst_goal,
            repo_root=repo_root,
            workspace_root=workspace_root,
            target_name=target_config.name,
        )
        write_continuation_artifact(
            artifact_dir=artifact_dir,
            run_id=loop_run_id,
            cycle_number=1,
            repository_state=repository_state,
            requested_phase=requested_phase,
            effective_phase=args.phase,
            decision=ContinuationDecision(
                continue_running=False,
                reason="phase-policy-adjusted",
                summary=(
                    "Stopped after one cycle because MVP auto-continue only supports "
                    "planner/developer/reviewer target phases."
                ),
                details={"effective_phase": args.phase},
            ),
            planner_result=None,
            dry_run=args.dry_run,
        )
        return 0

    if phase_adjusted:
        execute_cycle(
            args=args,
            analyst_goal=analyst_goal,
            repo_root=repo_root,
            workspace_root=workspace_root,
            target_name=target_config.name,
        )
        write_continuation_artifact(
            artifact_dir=artifact_dir,
            run_id=loop_run_id,
            cycle_number=1,
            repository_state=repository_state,
            requested_phase=requested_phase,
            effective_phase=args.phase,
            decision=ContinuationDecision(
                continue_running=False,
                reason="phase-policy-adjusted",
                summary=(
                    "Stopped after one cycle because repository-state policy adjusted "
                    "the effective target phase."
                ),
                details={"requested_phase": requested_phase, "effective_phase": args.phase},
            ),
            planner_result=None,
            dry_run=args.dry_run,
        )
        return 0

    for cycle_number in range(1, args.max_cycles + 1):
        planner_result = execute_cycle(
            args=args,
            analyst_goal=analyst_goal,
            repo_root=repo_root,
            workspace_root=workspace_root,
            target_name=target_config.name,
        )
        decision = evaluate_continuation(
            planner_result=planner_result,
            cycle_number=cycle_number,
            max_cycles=args.max_cycles,
        )
        write_continuation_artifact(
            artifact_dir=artifact_dir,
            run_id=loop_run_id,
            cycle_number=cycle_number,
            repository_state=repository_state,
            requested_phase=requested_phase,
            effective_phase=args.phase,
            decision=decision,
            planner_result=planner_result,
            dry_run=args.dry_run,
        )
        if not decision.continue_running:
            break

    return 0


def execute_cycle(
    *,
    args: argparse.Namespace,
    analyst_goal: str,
    repo_root: Path,
    workspace_root: Path,
    target_name: str,
) -> PlannerPhaseResult | None:
    planner_result: PlannerPhaseResult | None = None

    def analyst_handler() -> None:
        run_analyst_phase(
            goal=analyst_goal,
            target_repo_root=repo_root,
            workspace_root=workspace_root,
            target_name=target_name,
            dry_run=args.dry_run,
        )

    def planner_handler() -> None:
        nonlocal planner_result
        planner_result = run_planner_phase(
            goal=args.goal,
            target_repo_root=repo_root,
            workspace_root=workspace_root,
            target_name=target_name,
            dry_run=args.dry_run,
        )

    def developer_handler() -> None:
        run_developer_phase(
            goal=args.goal,
            repo_root=repo_root,
            workspace_root=workspace_root,
            target_name=target_name,
            dry_run=args.dry_run,
            execute=args.execute,
            planned_task=planner_result.task_artifact if planner_result else None,
        )

    def reviewer_handler() -> None:
        run_reviewer_phase(
            goal=args.goal,
            repo_root=repo_root,
            workspace_root=workspace_root,
            target_name=target_name,
            dry_run=args.dry_run,
            planned_task=planner_result.task_artifact if planner_result else None,
        )

    def tester_handler() -> None:
        run_tester_phase(
            goal=args.goal,
            repo_root=repo_root,
            workspace_root=workspace_root,
            target_name=target_name,
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

    return planner_result


def evaluate_continuation(
    *,
    planner_result: PlannerPhaseResult | None,
    cycle_number: int,
    max_cycles: int,
) -> ContinuationDecision:
    if planner_result is not None and not planner_result.continue_to_implementation:
        details = extract_planner_details(planner_result)
        stop_reason_text = details.get("planner_stop_reason_text", "").lower()
        if "no grounded next task" in stop_reason_text or "no eligible task" in stop_reason_text:
            return ContinuationDecision(
                continue_running=False,
                reason="planner-stopped-no-grounded-next-task",
                summary=(
                    "Stopped because the planner did not identify a grounded next task "
                    "that can continue implementation."
                ),
                details=details,
            )
        if "policy" in stop_reason_text or "state" in stop_reason_text:
            return ContinuationDecision(
                continue_running=False,
                reason="planner-stopped-policy",
                summary=(
                    "Stopped because the planner result indicates repository policy/state "
                    "prevented further implementation in this loop."
                ),
                details=details,
            )
        return ContinuationDecision(
            continue_running=False,
            reason="planner-stopped-other",
            summary=(
                "Stopped because the planner did not permit continuation to implementation."
            ),
            details=details,
        )

    if cycle_number >= max_cycles:
        return ContinuationDecision(
            continue_running=False,
            reason="max-cycles-reached",
            summary="Stopped because the configured auto-continue safety limit was reached.",
            details={"max_cycles": max_cycles},
        )

    return ContinuationDecision(
        continue_running=True,
        reason="continue",
        summary="Continuing because the planner still produced an implementation-eligible task.",
        details=extract_planner_details(planner_result),
    )


def extract_planner_details(planner_result: PlannerPhaseResult | None) -> dict[str, object]:
    if planner_result is None:
        return {}

    task_artifact = planner_result.task_artifact
    details: dict[str, object] = {
        "continue_to_implementation": planner_result.continue_to_implementation,
    }

    artifact_path: Path | None = None
    artifact_text = ""
    if task_artifact is not None:
        artifact_path, artifact_text = task_artifact
        details["planner_task_path"] = str(artifact_path)
        details["planner_task_name"] = artifact_path.name
        details["planner_task_slug"] = artifact_path.stem

    if not artifact_text:
        artifact_text = read_text_if_exists(artifact_path)
    if artifact_text:
        summary_line = next((line.strip() for line in artifact_text.splitlines() if line.strip()), "")
        details["planner_task_summary_line"] = summary_line
        lowered = artifact_text.lower()
        if "no grounded next task" in lowered:
            details["planner_stop_reason_text"] = "no grounded next task"
        elif "no eligible" in lowered and "task" in lowered:
            details["planner_stop_reason_text"] = "no eligible task"
        elif "policy" in lowered or "repository state" in lowered:
            details["planner_stop_reason_text"] = "policy or repository state"
        elif summary_line:
            details["planner_stop_reason_text"] = summary_line

    return details


def write_continuation_artifact(
    *,
    artifact_dir: Path,
    run_id: str,
    cycle_number: int,
    repository_state: str,
    requested_phase: str,
    effective_phase: str,
    decision: ContinuationDecision,
    planner_result: PlannerPhaseResult | None,
    dry_run: bool,
) -> None:
    payload = {
        "run_id": run_id,
        "cycle_number": cycle_number,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "repository_state": repository_state,
        "requested_phase": requested_phase,
        "effective_phase": effective_phase,
        "decision": {
            "continue_running": decision.continue_running,
            "reason": decision.reason,
            "summary": decision.summary,
            "details": decision.details,
        },
        "planner": extract_planner_details(planner_result),
    }

    status = "continue" if decision.continue_running else "stop"
    artifact_path = artifact_dir / f"run-cycle-{run_id}-cycle-{cycle_number:02d}-{status}.json"

    if dry_run:
        print(f"[dry-run] Would write continuation artifact: {artifact_path}")
        print(json.dumps(payload, indent=2, sort_keys=True))
        return

    artifact_dir.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote continuation artifact: {artifact_path}")
def read_text_if_exists(path: Path | None) -> str:
    if path is None or not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def run_phase(phase: str, handlers: dict[str, Callable[[], None]]) -> None:
    handler = handlers.get(phase)
    if handler is None:
        raise ValueError(f"Unsupported phase: {phase}")
    handler()


if __name__ == "__main__":
    raise SystemExit(main())
