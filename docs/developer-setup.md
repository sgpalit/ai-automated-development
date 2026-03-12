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
TARGET_REPO_PATH=.
```

Variable reference:

| Variable | Required | Description |
|--------|--------|--------|
| OPENAI_API_KEY | yes for `run_analyst.py` and `run_planner.py` | API key for OpenAI models |
| OPENAI_MODEL | no | Model name passed to the OpenAI Responses API |
| TARGET_REPO_PATH | no | Repository to analyze and plan against. Defaults to the current repo. |

---

# 4. Available Entry Points

The simplest entry point is:

- `./run-agents.sh "Your goal here"`

Other available scripts:

- `python3 scripts/run_analyst.py`
- `python3 scripts/run_planner.py`
- `python3 scripts/run_cycle.py "Your goal here" --phase planner`

What they do:

- `run-agents.sh` forwards arguments to `scripts/run_cycle.py`
- `run_analyst.py` reads `prompts/agents/analyst.md` and writes `analysis/repo-analysis.md`
- `run_planner.py` reads `analysis/repo-analysis.md` and writes one or more backlog tasks
- `run_cycle.py` is a thin-slice local runner for the analyst and planner phases

---

# 5. Run the Analyst

```bash
python3 scripts/run_analyst.py
```

Output:

```text
analysis/repo-analysis.md
```

This script uses the OpenAI API.

---

# 6. Run the Planner

```bash
python3 scripts/run_planner.py
```

Output:

```text
backlog/tasks/TASK-###-short-description.md
```

The planner expects `analysis/repo-analysis.md` to already exist.

---

# 7. Run the Thin-Slice Local CLI

Use this when you want a simple end-to-end analyst + planner pass from one command:

```bash
./run-agents.sh "Improve onboarding documentation"
```

Useful options:

```bash
./run-agents.sh "Improve onboarding documentation" --phase analyst
./run-agents.sh "Improve onboarding documentation" --dry-run
./run-agents.sh "Improve onboarding documentation" --repo /path/to/target-repo
```

Notes:

- `--phase analyst` runs only the analyst phase
- default behavior runs analyst and planner
- `--dry-run` prints outputs without writing files

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

For the current human-supervised workflow, see `docs/running-the-system.md` and `docs/workflow.md`.

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
3. Review `analysis/repo-analysis.md`
4. Run `python3 scripts/run_planner.py`
5. Review the generated files in `backlog/tasks/`
6. Continue with the human-supervised implementation workflow

---

# Directory Overview

```text
ai-automated-development
|
|- analysis/
|- backlog/
|  `- tasks/
|- docs/
|- prompts/
|  `- agents/
`- scripts/
```
