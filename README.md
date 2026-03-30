# accord-agent

Agentic workflow for drafting Accord Project templates from natural language requirements.

Built as a proof-of-work prototype for GSoC 2026 — Accord Project / Agentic Workflow for Drafting Templates.

## What It Does

Takes natural language contract requirements and runs a three-agent pipeline:

1. **DrafterAgent** — converts requirements into a Concerto model and TemplateMark template
2. **ValidatorAgent** — validates the Concerto model using the real `concerto` CLI
3. **ReviewerAgent** — reviews for legal completeness and produces the final template
```
python main.py "Draft a payment agreement for freelancers"
```

## Architecture
```
accord-agent/
├── main.py              ← CLI entry point (click)
├── agents/
│   ├── drafter.py       ← DrafterAgent: natural language → Concerto + TemplateMark
│   ├── validator.py     ← ValidatorAgent: concerto CLI validation
│   └── reviewer.py      ← ReviewerAgent: legall.py ← subprocess wrapper for concerto CLI (real validation)
│   └── template_tool.py ← TemplateMark generation and syntax checking
├── models/
│   └── payment.cto      ← Example Concerto model (payment agreement)
└── tests/
    └── test_agents.py   ← 6/6 passing unit tests
```

## Installation
```bash
git clone https://github.com/mbilgesu/accord-agent
cd accord-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
npm install -g @accordproject/concerto-cli
```

## Usage
```bash
python main.py "Draft a payment agreement for freelancers"
python main.py "NDA between two companies" --model claude-3-5-sonnet
python main.py "Service agreement" --output output/service.json
```

## Tests
```bash
PYTHONPATH=. pytest tests/test_agents.py -v
# 6/6 passed
```

## GSoC 2026

Proof-of-work prototype for Accord Project GSoC 2026 — Agentic Workflow for Drafting Templates.
