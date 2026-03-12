# Target Repository Context

## Purpose

This document explains how agents should understand and interact with a target repository.

The system is designed to run agents against an external repository to analyze, plan, implement, review, and validate improvements.

Agents must first build a clear understanding of the target repository before performing any changes.

---

## Repository Intake Checklist

Use this checklist to gather the minimum context needed for reliable planning.

### 1. Repository Purpose
Determine:

- what the repository does
- what problem it solves
- who the expected users are
- the overall maturity of the project

Evidence to capture:

- README summary
- docs overview
- product or project description
- visible indicators of maturity such as release notes, badges, or roadmap items

### 2. Technology Stack
Identify:

- programming languages
- frameworks
- build systems
- package managers
- testing frameworks
- infrastructure tools

Evidence to capture:

- manifest files
- lockfiles
- CI configs
- Docker or deployment files
- top-level build/test configuration

Understanding the stack helps prevent incompatible changes.

### 3. Repository Structure
Inspect the directory structure to understand how the project is organized.

Important things to identify:

- source code directories
- documentation directories
- configuration files
- test directories
- scripts or automation

Evidence to capture:

- top-level directories
- notable modules or apps
- important configuration locations
- generated vs source-managed folders

Agents should infer the architectural structure from the directory layout.

### 4. Architecture Understanding
Summarize the architecture.

Examples:

- monolithic application
- layered architecture
- microservices
- modular system
- frontend/backend separation

Evidence to capture:

- major components
- boundaries between components
- integration points
- data flow or deployment shape, if visible

The analysis should describe the major components and their relationships.

### 5. Conventions
Identify project conventions such as:

- naming conventions
- directory patterns
- testing practices
- documentation style
- dependency management

Evidence to capture:

- lint/format config
- existing file naming patterns
- test naming/location patterns
- contribution guidance
- examples of preferred documentation structure

Agents should respect these conventions when making changes.

### 6. Quality Signals
Evaluate project maturity by looking for signals such as:

- presence of automated tests
- documentation completeness
- CI/CD configuration
- linting or formatting tools
- dependency management practices

Evidence to capture:

- test directories and commands
- CI workflow files
- static analysis tools
- coverage or quality badges
- signs of stale or missing automation

These signals help guide improvement priorities.

### 7. Risks and Gaps
Identify potential weaknesses such as:

- missing documentation
- missing tests
- unclear architecture
- inconsistent code structure
- duplicated logic

Evidence to capture:

- absent or incomplete guides
- ambiguous ownership
- conflicting conventions
- broken or missing setup instructions
- areas with unclear impact or verification paths

These findings should be highlighted in the analysis.

### 8. Improvement Opportunities
Identify areas where the project can improve.

Examples:

- missing developer documentation
- unclear project structure
- lack of examples
- missing contributor guidance
- missing automation

Evidence to capture:

- direct linkage from observed gap to proposed improvement
- likely user/developer impact
- whether the work can be sliced into a small task

These observations will be used by the Planner agent to generate backlog tasks.

---

## Analyst Output Expectations

The Analyst agent must produce a structured report stored in:

    agents/analysis/repo-analysis.md

The report should contain:

- repository overview
- technology stack
- architecture summary
- key components
- conventions
- quality signals
- risks
- improvement opportunities

The report should be based on observable repository evidence, not assumptions alone.

This output becomes the primary input for the Planner agent.
