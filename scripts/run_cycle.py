#!/usr/bin/env python3
"""Thin orchestrator for the local multi-agent workflow phases."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from run_analyst import run_analyst_phase
from run_developer import run_developer_phase
from run_planner import PlannerPhaseResult, run_planner_phase
from run_reviewer import run_reviewer_phase
from run_tester import run_tester_phase
from shared.artifact_paths import logs_dir, tester_report_path
from shared.target_repo_config import (
    SUPPORTED_REPOSITORY_STATES,
    resolve_target_repo_config,
)
from shared.task_utils import extract_task_code

PHASE_ORDER = ["analyst", "planner", "developer", "reviewer", "tester"]
DEFAULT_AUTOMATION_GOAL = (
    "Advance the next missing MVP item from docs/mvp.md using the next eligible backlog task."
)
AUTO_CONTINUE_PHASES = {"planner", "developer", "reviewer", "tester"}
AUTO_CONTINUE_STOP_REASONS = {
    "single-cycle-requested",
    "repository-state-not-mvp",
    "planner-stopped-no-grounded-next-task",
    "planner-stopped-policy",
    "planner-stopped-other",
    "phase-policy-adjusted",
    "max-cycles-reached",
    "tester-outcome-retry",
    "tester-outcome-blocked",
    "tester-outcome-missing",
    "tester-outcome-unrecognized",
}


@dataclass(frozen=True)
class ContinuationDecision:
    continue_running: bool
    reason: str
    summary: str
    details: dict[str, object]


TESTER_OUTCOME_PATTERN = re.compile(r"^Outcome:\s*(READY|RETRY|BLOCKED)\s*$", re.MULTILINE)


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
            "planner/developer/reviewer/tester cycles until a grounded stop condition is reached."
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

    if state == "MVP" and args.phase == "tester" and not args.auto_continue:
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


def execute_cycle(
    *,
    args: argparse.Namespace,
    analyst_goal: str,
    repo_root: Path,
    workspace_root: Path,
    target_name: str,
) -> PlannerPhaseResult | None:
    phase_sequence = PHASE_ORDER[: PHASE_ORDER.index(args.phase) + 1]

    print("Running phase: analyst")
    run_analyst_phase(
        goal=analyst_goal,
        target_repo_root=repo_root,
        workspace_root=workspace_root,
        target_name=target_name,
        dry_run=args.dry_run,
    )

    planner_result: PlannerPhaseResult | None = None
    if "planner" in phase_sequence:
        print("Running phase: planner")
        planner_result = run_planner_phase(
            goal=args.goal,
            target_repo_root=repo_root,
            workspace_root=workspace_root,
            target_name=target_name,
            dry_run=args.dry_run,
        )
        if not planner_result.continue_to_implementation:
            return planner_result

    if "developer" in phase_sequence:
        print("Running phase: developer")
        run_developer_phase(
            goal=analyst_goal,
            repo_root=repo_root,
            workspace_root=workspace_root,
            target_name=target_name,
            dry_run=args.dry_run,
            execute=args.execute,
            planned_task=planner_result.task_artifact if planner_result else None,
        )

    if "reviewer" in phase_sequence:
        print("Running phase: reviewer")
        run_reviewer_phase(
            goal=analyst_goal,
            repo_root=repo_root,
            workspace_root=workspace_root,
            target_name=target_name,
            dry_run=args.dry_run,
            planned_task=planner_result.task_artifact if planner_result else None,
        )

    if "tester" in phase_sequence:
        print("Running phase: tester")
        run_tester_phase(
            goal=analyst_goal,
            repo_root=repo_root,
            workspace_root=workspace_root,
            target_name=target_name,
            dry_run=args.dry_run,
            planned_task=planner_result.task_artifact if planner_result else None,
        )

    return planner_result


def parse_tester_outcome(report_content: str) -> str | None:
    match = TESTER_OUTCOME_PATTERN.search(report_content)
    if not match:
        return None
    return match.group(1)


def read_tester_outcome(
    *,
    workspace_root: Path,
    target_name: str,
    planner_result: PlannerPhaseResult | None,
) -> tuple[str | None, Path | None]:
    if planner_result is None or planner_result.task_artifact is None:
        return None, None

    task_path, _task_content = planner_result.task_artifact
    task_code = extract_task_code(task_path).lower()
    report_path = tester_report_path(workspace_root, target_name, task_code)
    if not report_path.exists():
        return None, report_path

    report_content = report_path.read_text(encoding="utf-8")
    return parse_tester_outcome(report_content), report_path


def determine_continuation_decision(
    *,
    args: argparse.Namespace,
    repository_state: str,
    phase_adjusted: bool,
    planner_result: PlannerPhaseResult | None,
    requested_phase: str,
    effective_phase: str,
    workspace_root: Path,
    target_name: str,
) -> ContinuationDecision:
    if repository_state != "MVP":
        return ContinuationDecision(
            continue_running=False,
            reason="repository-state-not-mvp",
            summary=(
                "Stopped auto-continuation because the target repository state is "
                f"{repository_state}, not MVP."
            ),
            details={"repository_state": repository_state},
        )

    if phase_adjusted and requested_phase != effective_phase:
        return ContinuationDecision(
            continue_running=False,
            reason="phase-policy-adjusted",
            summary=(
                "Stopped auto-continuation because repository state policy adjusted "
                f"the requested phase from {requested_phase} to {effective_phase}."
            ),
            details={
                "requested_phase": requested_phase,
                "effective_phase": effective_phase,
            },
        )

    if effective_phase not in AUTO_CONTINUE_PHASES:
        return ContinuationDecision(
            continue_running=False,
            reason="planner-stopped-policy",
            summary=(
                "Stopped auto-continuation because the effective phase "
                f"{effective_phase!r} is not eligible for repeated cycles."
            ),
            details={"effective_phase": effective_phase},
        )

    if planner_result is None:
        return ContinuationDecision(
            continue_running=False,
            reason="planner-stopped-other",
            summary="Stopped auto-continuation because planner output was unavailable.",
            details={},
        )

    if planner_result.task_artifact is None:
        return ContinuationDecision(
            continue_running=False,
            reason="planner-stopped-no-grounded-next-task",
            summary=(
                "Stopped auto-continuation because the planner did not select a grounded "
                "next task from the backlog."
            ),
            details={},
        )

    if not planner_result.continue_to_implementation:
        return ContinuationDecision(
            continue_running=False,
            reason="planner-stopped-other",
            summary=(
                "Stopped auto-continuation because the planner produced a task artifact "
                "but did not continue to implementation."
            ),
            details={"planner_task": str(planner_result.task_artifact[0])},
        )

    if effective_phase == "tester":
        tester_outcome, report_path = read_tester_outcome(
            workspace_root=workspace_root,
            target_name=target_name,
            planner_result=planner_result,
        )
        if tester_outcome is None:
            reason = "tester-outcome-missing" if report_path and not report_path.exists() else "tester-outcome-unrecognized"
            summary = (
                "Stopped auto-continuation because no deterministic tester outcome was available."
                if reason == "tester-outcome-missing"
                else "Stopped auto-continuation because the tester report did not contain a recognized deterministic outcome."
            )
            return ContinuationDecision(
                continue_running=False,
                reason=reason,
                summary=summary,
                details={"tester_report": str(report_path) if report_path else None},
            )

        if tester_outcome != "READY":
            lowered = tester_outcome.lower()
            return ContinuationDecision(
                continue_running=False,
                reason=f"tester-outcome-{lowered}",
                summary=(
                    "Stopped auto-continuation because the tester result was "
                    f"{tester_outcome}, not READY."
                ),
                details={
                    "tester_outcome": tester_outcome,
                    "tester_report": str(report_path) if report_path else None,
                },
            )

    return ContinuationDecision(
        continue_running=True,
        reason="continue",
        summary="Continuing to the next cycle because planner selected a grounded task.",
        details={"effective_phase": effective_phase},
    )


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
) -> Path:
    artifact_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = artifact_dir / f"{run_id}-cycle-{cycle_number:02d}.json"
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
        "planner": None
        if planner_result is None
        else {
            "continue_to_implementation": planner_result.continue_to_implementation,
            "task_artifact": None
            if planner_result.task_artifact is None
            else str(planner_result.task_artifact[0]),
        },
    }

    if dry_run:
        print(f"[dry-run] Would write continuation artifact: {artifact_path}")
        print(json.dumps(payload, indent=2, sort_keys=True))
        return artifact_path

    artifact_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote continuation artifact: {artifact_path}")
    return artifact_path


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
        planner_result = execute_cycle(
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
            planner_result=planner_result,
            dry_run=args.dry_run,
        )
        return 0

    if repository_state != "MVP":
        planner_result = execute_cycle(
            args=args,
            analyst_goal=analyst_goal,
            repo_root=repo_root,
            workspace_root=workspace_root,
            target_name=target_config.name,
        )
        decision = determine_continuation_decision(
            args=args,
            repository_state=repository_state,
            phase_adjusted=phase_adjusted,
            planner_result=planner_result,
            requested_phase=requested_phase,
            effective_phase=args.phase,
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
            decision=decision,
            planner_result=planner_result,
            dry_run=args.dry_run,
        )
        return 0

    cycle_number = 0
    while cycle_number < args.max_cycles:
        cycle_number += 1
        print(f"=== Auto-continue cycle {cycle_number} / {args.max_cycles} ===")
        planner_result = execute_cycle(
            args=args,
            analyst_goal=analyst_goal,
            repo_root=repo_root,
            workspace_root=workspace_root,
            target_name=target_config.name,
        )
        decision = determine_continuation_decision(
            args=args,
            repository_state=repository_state,
            phase_adjusted=phase_adjusted,
            planner_result=planner_result,
            requested_phase=requested_phase,
            effective_phase=args.phase,
            workspace_root=workspace_root,
            target_name=target_config.name,
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

        print(f"Auto-continue decision: {decision.summary}")
        if not decision.continue_running:
            return 0

    final_decision = ContinuationDecision(
        continue_running=False,
        reason="max-cycles-reached",
        summary=(
            "Stopped auto-continuation because the configured maximum number "
            f"of cycles ({args.max_cycles}) was reached."
        ),
        details={"max_cycles": args.max_cycles},
    )
    write_continuation_artifact(
        artifact_dir=artifact_dir,
        run_id=loop_run_id,
        cycle_number=cycle_number,
        repository_state=repository_state,
        requested_phase=requested_phase,
        effective_phase=args.phase,
        decision=final_decision,
        planner_result=None,
        dry_run=args.dry_run,
    )
    print(f"Auto-continue decision: {final_decision.summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
