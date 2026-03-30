"""
main.py
=======
CLI entry point for accord-agent.

Usage:
    python main.py "Draft a payment agreement for freelancers"
    python main.py "NDA between two companies" --model claude-3-5-sonnet
    python main.py "Service agreement" --output output/service.json
"""

import click
import json
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from crewai import Crew, Process

from agents.drafter import create_drafter_agent, create_draft_task
from agents.validator import create_validator_agent, create_validation_task
from agents.reviewer import create_reviewer_agent, create_review_task

console = Console()


@click.command()
@click.argument("requirements")
@click.option(
    "--model",
    default="gpt-4o",
    help="LLM model to use: gpt-4o, claude-3-5-sonnet, gemini-pro",
)
@click.option(
    "--output",
    default=None,
    help="Output file path for the final template (JSON)",
)
@click.option(
    "--verbose",
    is_flag=True,
    default=False,
    help="Show detailed agent reasoning",
)
def main(requirements: str, model: str, output: str, verbose: bool):
    """
    Generate an Accord Project template from natural language requirements.

    Example:
        python main.py "Draft a payment agreement for freelancers"
    """
    console.print(
        Panel.fit(
            f"[bold blue]Accord Agent[/bold blue]\n"
            f"Requirements: [italic]{requirements}[/italic]\n"
            f"Model: [green]{model}[/green]",
            title="Starting",
        )
    )

    # ── Build agents ──────────────────────────────────────────────────────────
    drafter   = create_drafter_agent(llm_model=model)
    validator = create_validator_agent(llm_model=model)
    reviewer  = create_reviewer_agent(llm_model=model)

    # ── Build tasks ───────────────────────────────────────────────────────────
    draft_task      = create_draft_task(drafter, requirements)
    validation_task = create_validation_task(validator, "{draft_task.output}")
    review_task     = create_review_task(reviewer, "{validation_task.output}")

    # ── Run crew ──────────────────────────────────────────────────────────────
    crew = Crew(
        agents=[drafter, validator, reviewer],
        tasks=[draft_task, validation_task, review_task],
        process=Process.sequential,
        verbose=verbose,
    )

    console.print("\n[bold]Running agent workflow...[/bold]\n")
    result = crew.kickoff()

    # ──