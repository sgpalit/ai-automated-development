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
from shared.artifact_paths import (
    logs_dir,
    stop_reason_latest_path,
    stop_reason_timestamped_path,
    tester_report_path,
)
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


def determine_continuation(
    *,
    args: argparse.Namespace,
    repository_state: str,
    planner_result: PlannerPhaseResult | None,
    workspace_root: Path,
    target_name: str,
) -> ContinuationDecision:
    if not args.auto_continue:
        return ContinuationDecision(
            continue_running=False,
            reason="single-cycle-requested",
            summary="Auto-continue disabled; stopping after a single cycle.",
            details={},
        )

    if repository_state != "MVP":
        return ContinuationDecision(
            continue_running=False,
            reason="repository-state-not-mvp",
            summary=(
                "Auto-continue only runs repeatedly for MVP target repositories; "
                f"stopping for state {repository_state}."
            ),
            details={"repository_state": repository_state},
        )

    if planner_result is not None and not planner_result.continue_to_implementation:
        planner_stop_reason = getattr(planner_result, "stop_reason", None)
        planner_summary = getattr(planner_result, "summary", None)
        if planner_stop_reason == "no-grounded-next-task":
            return ContinuationDecision(
                continue_running=False,
                reason="planner-stopped-no-grounded-next-task",
                summary=planner_summary
                or "Planner could not derive a grounded next task after backlog exhaustion.",
                details={
                    "planner_stop_reason": planner_stop_reason,
                    "task_artifact": str(planner_result.task_artifact)
                    if planner_result.task_artifact
                    else None,
                },
            )
        if planner_stop_reason == "policy-stop":
            return ContinuationDecision(
                continue_running=False,
                reason="planner-stopped-policy",
                summary=planner_summary or "Planner reported a policy stop.",
                details={
                    "planner_stop_reason": planner_stop_reason,
                    "task_artifact": str(planner_result.task_artifact)
                    if planner_result.task_artifact
                    else None,
                },
            )
        return ContinuationDecision(
            continue_running=False,
            reason="planner-stopped-other",
            summary=planner_summary or "Planner stopped before implementation.",
            details={
                "planner_stop_reason": planner_stop_reason,
                "task_artifact": str(planner_result.task_artifact)
                if planner_result.task_artifact
                else None,
            },
        )

    if args.phase != "tester":
        return ContinuationDecision(
            continue_running=False,
            reason="single-cycle-requested",
            summary=(
                "Auto-continue requested, but the selected phase does not include tester; "
                "stopping after one cycle."
            ),
            details={"phase": args.phase},
        )

    task_code = (
        extract_task_code(planner_result.task_artifact)
        if planner_result and planner_result.task_artifact
        else None
    )
    if not task_code:
        return ContinuationDecision(
            continue_running=False,
            reason="tester-outcome-missing",
            summary="Unable to infer task code from planner output for tester continuation.",
            details={},
        )

    report_path = tester_report_path(workspace_root, target_name, task_code)
    if not report_path.exists():
        return ContinuationDecision(
            continue_running=False,
            reason="tester-outcome-missing",
            summary=f"Tester report not found at {report_path}.",
            details={"report_path": str(report_path)},
        )

    report_text = report_path.read_text(encoding="utf-8")
    match = TESTER_OUTCOME_PATTERN.search(report_text)
    if not match:
        return ContinuationDecision(
            continue_running=False,
            reason="tester-outcome-unrecognized",
            summary=f"Tester report at {report_path} did not contain an Outcome line.",
            details={"report_path": str(report_path)},
        )

    outcome = match.group(1)
    if outcome == "READY":
        return ContinuationDecision(
            continue_running=True,
            reason="tester-outcome-ready",
            summary="Tester reported READY; continuing to the next cycle.",
            details={"report_path": str(report_path)},
        )

    if outcome == "RETRY":
        return ContinuationDecision(
            continue_running=False,
            reason="tester-outcome-retry",
            summary="Tester reported RETRY; stopping auto-continue for manual follow-up.",
            details={"report_path": str(report_path)},
        )

    if outcome == "BLOCKED":
        return ContinuationDecision(
            continue_running=False,
            reason="tester-outcome-blocked",
            summary="Tester reported BLOCKED; stopping auto-continue for manual follow-up.",
            details={"report_path": str(report_path)},
        )

    return ContinuationDecision(
        continue_running=False,
        reason="tester-outcome-unrecognized",
        summary=f"Tester outcome {outcome} is not recognized for continuation.",
        details={"report_path": str(report_path), "outcome": outcome},
    )


def write_continuation_log(
    *,
    workspace_root: Path,
    target_name: str,
    cycle_count: int,
    repository_state: str,
    phase: str,
    decision: ContinuationDecision,
    dry_run: bool,
) -> Path:
    timestamp = datetime.now(timezone.utc)
    timestamp_slug = timestamp.strftime("%Y%m%dT%H%M%SZ")
    log_directory = logs_dir(workspace_root, target_name) / "continuation"
    log_path = log_directory / f"{timestamp_slug}-cycle-{cycle_count:02d}.json"
    payload = {
        "timestamp": timestamp.isoformat(),
        "target_name": target_name,
        "repository_state": repository_state,
        "phase": phase,
        "cycle_count": cycle_count,
        "continue_running": decision.continue_running,
        "reason": decision.reason,
        "summary": decision.summary,
        "details": decision.details,
    }
    if dry_run:
        print(f"[dry-run] Would write continuation log: {log_path}")
        print(json.dumps(payload, indent=2, sort_keys=True))
        return log_path

    log_directory.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote continuation log: {log_path}")
    return log_path


def write_stop_reason_artifact(
    *,
    workspace_root: Path,
    target_name: str,
    repository_state: str,
    phase: str,
    cycle_count: int,
    decision: ContinuationDecision,
    dry_run: bool,
) -> tuple[Path, Path]:
    timestamp = datetime.now(timezone.utc)
    timestamp_iso = timestamp.isoformat()
    timestamp_slug = timestamp.strftime("%Y%m%dT%H%M%SZ")
    reason_slug = re.sub(r"[^a-z0-9-]+", "-", decision.reason.lower()).strip("-") or "stop"
    latest_path = stop_reason_latest_path(workspace_root, target_name)
    timestamped_path = stop_reason_timestamped_path(
        workspace_root,
        target_name,
        timestamp_slug,
        reason_slug,
    )

    content_lines = [
        f"# Stop Reason Artifact: {decision.reason}",
        "",
        "## Context",
        f"- Target: `{target_name}`",
        f"- Repository State: `{repository_state}`",
        f"- Phase: `{phase}`",
        f"- Cycle Count: `{cycle_count}`",
        f"- Timestamp: `{timestamp_iso}`",
        "",
        "## Decision",
        f"- Reason: `{decision.reason}`",
        f"- Summary: {decision.summary}",
        "",
        "## Details",
    ]

    if decision.details:
        for key, value in sorted(decision.details.items()):
            content_lines.append(f"- {key}: `{value}`")
    else:
        content_lines.append("- None")

    content = "\n".join(content_lines) + "\n"

    if dry_run:
        print(f"[dry-run] Would write stop reason artifact: {timestamped_path}")
        print(f"[dry-run] Would update latest stop reason artifact: {latest_path}")
        return timestamped_path, latest_path

    timestamped_path.parent.mkdir(parents=True, exist_ok=True)
    timestamped_path.write_text(content, encoding="utf-8")
    latest_path.write_text(content, encoding="utf-8")
    print(f"Wrote stop reason artifact: {timestamped_path}")
    print(f"Updated latest stop reason artifact: {latest_path}")
    return timestamped_path, latest_path


def main() -> int:
    args = parse_args()
    workspace_root = Path(__file__).resolve().parents[1]
    config = resolve_target_repo_config(
        workspace_root=workspace_root,
        target_config_arg=args.target_config,
        repo_override=args.repo,
        repository_state_override=args.target_repository_state,
    )

    args.repo = str(config.repo_path)
    if args.target_repository_state is None:
        args.target_repository_state = config.repository_state
    target_name = config.name
    repo_root = config.repo_path.resolve()
    analyst_goal = args.goal or DEFAULT_AUTOMATION_GOAL

    print(f"Target config: {config.config_path}")
    print(f"Target name: {target_name}")
    print(f"Target repository: {repo_root}")
    print(f"Target repository state: {config.repository_state}")

    phase_adjusted = apply_repository_state_rules(args, config.repository_state)

    if phase_adjusted:
        print("Phase policy adjusted for target repository state; continuing with updated phase.")

    cycle_limit = max(1, args.max_cycles)
    cycle_count = 0

    while True:
        cycle_count += 1
        print(f"=== Cycle {cycle_count}/{cycle_limit} ===")
        planner_result = execute_cycle(
            args=args,
            analyst_goal=analyst_goal,
            repo_root=repo_root,
            workspace_root=workspace_root,
            target_name=target_name,
        )

        decision = determine_continuation(
            args=args,
            repository_state=config.repository_state,
            planner_result=planner_result,
            workspace_root=workspace_root,
            target_name=target_name,
        )

        write_continuation_log(
            workspace_root=workspace_root,
            target_name=target_name,
            cycle_count=cycle_count,
            repository_state=config.repository_state,
            phase=args.phase,
            decision=decision,
            dry_run=args.dry_run,
        )

        if decision.reason == "planner-stopped-no-grounded-next-task":
            write_stop_reason_artifact(
                workspace_root=workspace_root,
                target_name=target_name,
                repository_state=config.repository_state,
                phase=args.phase,
                cycle_count=cycle_count,
                decision=decision,
                dry_run=args.dry_run,
            )

        if not decision.continue_running:
            print(f"Stopping auto-continue: {decision.reason}")
            print(decision.summary)
            break

        if cycle_count >= cycle_limit:
            limit_decision = ContinuationDecision(
                continue_running=False,
                reason="max-cycles-reached",
                summary=f"Reached max cycle limit ({cycle_limit}); stopping auto-continue.",
                details={"max_cycles": cycle_limit},
            )
            write_continuation_log(
                workspace_root=workspace_root,
                target_name=target_name,
                cycle_count=cycle_count,
                repository_state=config.repository_state,
                phase=args.phase,
                decision=limit_decision,
                dry_run=args.dry_run,
            )
            print(f"Stopping auto-continue: {limit_decision.reason}")
            print(limit_decision.summary)
            break

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
