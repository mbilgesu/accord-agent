"""
main.py
=======
CLI entry point for accord-agent.

Usage:
    python main.py "Draft a payment agreement for freelancers"
    python main.py "NDA between two companies" --output output/nda.json
"""

import click
import json
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from agents.drafter import draft_template
from agents.validator import validate_draft
from agents.reviewer import review_template

console = Console()


@click.command()
@click.argument("requirements")
@click.option("--output", default=None, help="Output file path (JSON)")
@click.option("--verbose", is_flag=True, default=False)
def main(requirements: str, output: str, verbose: bool):
    """Generate an Accord Project template from natural language requirements."""

    console.print(Panel.fit(
        f"[bold blue]Accord Agent[/bold blue]\n"
        f"Requirements: [italic]{requirements}[/italic]\n"
        f"Model: [green]llama-3.3-70b-versatile (Groq)[/green]",
        title="Starting"
    ))

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:

        # Stage 1: Draft
        task = progress.add_task("Stage 1/3  DrafterAgent — generating template...", total=None)
        draft = draft_template(requirements)
        progress.remove_task(task)
        console.print("[green]✓[/green] Stage 1 complete — template drafted")

        if verbose:
            console.print_json(json.dumps(draft, indent=2))

        # Stage 2: Validate
        task = progress.add_task("Stage 2/3  ValidatorAgent — running concerto CLI...", total=None)
        validation = validate_draft(draft)
        progress.remove_task(task)
        console.print(
            f"[green]✓[/green] Stage 2 complete — "
            f"concerto: {'✓' if validation.get('concerto_cli_valid') else '✗'}  "
            f"template syntax: {'✓' if validation.get('template_syntax_valid') else '✗'}"
        )

        if verbose:
            console.print_json(json.dumps(validation, indent=2))

        # Stage 3: Review
        task = progress.add_task("Stage 3/3  ReviewerAgent — legal review...", total=None)
        review = review_template(draft, validation)
        progress.remove_task(task)
        console.print("[green]✓[/green] Stage 3 complete — review done")

    # Final output
    console.print(Panel.fit(
        f"[bold]Contract Type:[/bold] {draft.get('contract_type', 'Unknown')}\n"
        f"[bold]Parties:[/bold] {', '.join(draft.get('parties', []))}\n"
        f"[bold]Production Ready:[/bold] {'✓ Yes' if review.get('production_ready') else '✗ No'}\n"
        f"[bold]Review Notes:[/bold]\n" +
        "\n".join(f"  • {n}" for n in review.get("review_notes", [])),
        title="[bold green]Final Template[/bold green]"
    ))

    if output:
        out_path = Path(output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        final = {"draft": draft, "validation": validation, "review": review}
        out_path.write_text(json.dumps(final, indent=2))
        console.print(f"\n[green]Saved to {output}[/green]")


if __name__ == "__main__":
    main()