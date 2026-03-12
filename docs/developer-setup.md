# Developer Setup

This document explains how to run the current local agent scripts in this repository.

---

# Prerequisites

Required tools:

- Linux / WSL
- Git
- Python 3.11+
- OpenAI API key for the OpenAI-backed scripts

---

# 1. Clone the Repository

```bash
git clone https://github.com/palit-consulting/ai-automated-development.git
cd ai-automated-development
```

---

# 2. Create Python Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

# 3. Configure Environment Variables

Copy the example file:

```bash
cp .env.example .env
```

Minimum `.env` values:

```bash
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4o
```

Variable reference:

| Variable | Required | Description |
|--------|--------|--------|
| OPENAI_API_KEY | yes for `run_analyst.py` and `run_planner.py` | API key for OpenAI models |
| OPENAI_MODEL | no | Model name passed to the OpenAI Responses API |
| TARGET_REPOSITORY_CONFIG | no | Target repository config name from `config/targets/`. Defaults to `default` when present. |

---

# 4. Available Entry Points

The simplest entry point is:

- `./run-agents.sh`
- `./run-agents.sh "Your goal here"`

Other available scripts:

- `python3 scripts/run_analyst.py`
- `python3 scripts/run_planner.py`
- `python3 scripts/run_developer.py`
- `python3 scripts/run_developer.py --execute`
- `python3 scripts/run_cycle.py --phase planner`

What they do:

- `run-agents.sh` defaults to `scripts/run_cycle.py --phase tester --execute` and forwards any extra arguments
- `run_analyst.py` reads `prompts/agents/analyst.md` and writes `agents/<target-name>/analysis/repo-analysis.md`
- `run_planner.py` reads `agents/<target-name>/analysis/repo-analysis.md` and writes one grounded backlog task when needed
- `run_developer.py` writes a developer handoff and an implementation prompt artifact for the selected task, and can optionally apply repo changes with `--execute`
- `run_cycle.py` is the thin-slice local orchestrator for analyst, planner, developer, reviewer, and tester phases

If no goal is provided to `run-agents.sh`, `run_cycle.py`, or `run_developer.py`, the runner uses `docs/mvp.md` as context and selects the next eligible backlog task automatically.

---

# 5. Run the Analyst

```bash
python3 scripts/run_analyst.py
```

Output:

```text
agents/<target-name>/analysis/repo-analysis.md
```

This script uses the OpenAI API.

---

# 6. Run the Planner

```bash
python3 scripts/run_planner.py
```

Output:

```text
agents/<target-name>/backlog/tasks/TASK-###-short-description.md
```

The planner expects `agents/<target-name>/analysis/repo-analysis.md` to already exist.

---

# 7. Run the Thin-Slice Local CLI

Use this when you want a simple end-to-end analyst + planner + developer + reviewer + tester execution pass from one command:

```bash
./run-agents.sh
./run-agents.sh "Improve onboarding documentation"
```

Useful options:

```bash
./run-agents.sh --phase tester --execute
./run-agents.sh "Improve onboarding documentation" --phase analyst
./run-agents.sh "Improve onboarding documentation" --phase developer --execute
./run-agents.sh "Improve onboarding documentation" --phase tester --execute
./run-agents.sh "Improve onboarding documentation" --dry-run
./run-agents.sh "Improve onboarding documentation" --repo /path/to/target-repo
```

Notes:

- `--phase analyst` runs only the analyst phase
- `--phase developer` runs analyst, planner, and developer
- `--phase reviewer` runs analyst, planner, developer, and reviewer
- `--phase tester` runs analyst, planner, developer, reviewer, and tester
- `run-agents.sh` defaults to tester execution so a normal run can reach reviewer and tester in the same cycle
- without a goal prompt, the runner reuses the backlog and selects the next eligible task automatically
- `--dry-run` prints outputs without writing files
- the developer phase writes artifacts under `agents/<target-name>/handoff/developer/` and `agents/<target-name>/implementation/developer/`
- reviewer outputs are written under `agents/<target-name>/review/reviewer/`
- tester outputs are written under `agents/<target-name>/test/`
- `run-agents.sh` already includes `--execute`; use the Python entry points directly if you want artifact-only behavior
- in `MVP`, an explicit `--phase tester` run performs a single-cycle validation pass; repeated tester-gated iteration still requires `--auto-continue`
- use `--target-config <name>` to switch to another configured target repository

---

# 8. Running in a Loop

If you want to re-run the thin-slice planner loop every 5 minutes:

```bash
while true
do
  ./run-agents.sh "Improve onboarding documentation"
  sleep 300
done
```

---

# 9. Current Workflow Model

The current implementation is local and file-based.

It does not currently include:

- GitHub issue polling
- automatic branch creation
- automatic pull request creation
- MS Teams notifications

For the current workflow modes, see `docs/running-the-system.md` and `docs/workflow.md`.

---

# 10. Troubleshooting

## Missing API key

If you run `run_analyst.py` or `run_planner.py` without an API key, the scripts fail with:

```text
OPENAI_API_KEY is not set.
```

Set the key in `.env` or export it in your shell.

## Planner fails because analysis is missing

Generate the analysis first:

```bash
python3 scripts/run_analyst.py
```

## Python dependencies missing

Reinstall:

```bash
pip install -r requirements.txt
```

---

# 11. Recommended Workflow

1. Configure `.env`
2. Run `python3 scripts/run_analyst.py`
3. Review `agents/<target-name>/analysis/repo-analysis.md`
4. Run `python3 scripts/run_planner.py`
5. Review the generated files in `agents/<target-name>/backlog/tasks/`
6. Continue with the human-supervised implementation workflow

---

# Directory Overview

```text
ai-automated-development
|
|- agents/
|  `- <target-name>/
|     |- analysis/
|     |- backlog/tasks/
|     |- handoff/developer/
|     |- implementation/developer/
|     |- review/reviewer/
|     |- test/
|     |- orchestrator/stop-reasons/
|     `- logs/
|- docs/
|- prompts/
|  `- agents/
`- scripts/
```
