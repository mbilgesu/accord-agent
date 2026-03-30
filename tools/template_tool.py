"""
tools/template_tool.py
======================
Helpers for generating and validating TemplateMark templates.
"""

import json
import re


def generate_template_structure(
    contract_type: str,
    parties: list[str],
    key_terms: list[str],
) -> dict:
    """
    Generate a minimal TemplateMark template structure as a dict.
    This is the starting point that DrafterAgent refines.
    """
    template = {
        "contract_type": contract_type,
        "parties": parties,
        "key_terms": key_terms,
        "templatemark": _build_templatemark(contract_type, parties, key_terms),
        "sample_data": _build_sample_data(parties, key_terms),
    }
    return template


def _build_templatemark(
    contract_type: str, parties: list[str], key_terms: list[str]
) -> str:
    """Build a minimal TemplateMark text template."""
    party_lines = "\n".join(
        f'{{{{#clause {p.lower()}Info}}}}Party: {{{{{p.lower()}Name}}}}'
        f'{{{{/clause}}}}' for p in parties
    )
    terms_lines = "\n".join(f"- {term}: {{{{{term.replace(' ', '_')}}}}}" for term in key_terms)

    return f"""# {contract_type}

{party_lines}

## Key Terms

{terms_lines}

## Agreement

This agreement is entered into by the parties listed above under the
terms and conditions described herein.
"""


def _build_sample_data(parties: list[str], key_terms: list[str]) -> dict:
    """Build minimal sample JSON data for the template."""
    data = {}
    for party in parties:
        data[f"{party.lower()}Name"] = f"Sample {party}"
    for term in key_terms:
        data[term.replace(" ", "_")] = f"<{term} value>"
    return data


def validate_template_syntax(template_text: str) -> dict:
    """
    Basic syntax validation for TemplateMark templates.
    Checks for balanced clause tags.
    """
    open_tags = re.findall(r"\{\{#clause\s+\w+\}\}", template_text)
    close_tags = re.findall(r"\{\{/clause\}\}", template_text)

    if len(open_tags) != len(close_tags):
        return {
            "valid": False,
            "errors": f"Unbalanced clause tags: {len(open_tags)} open, {len(close_tags)} close",
        }
    return {"valid": True, "errors": ""}


def export_template(template: dict, output_path: str) -> None:
    """Save template structure to JSON."""
    with open(output_path, "w") as f:
        json.dump(template, f, indent=2)