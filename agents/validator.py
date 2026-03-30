"""
agents/validator.py
===================
ValidatorAgent: Validates generated Concerto models using
the real Accord Project concerto CLI and checks TemplateMark syntax.
"""

import os
import json
from groq import Groq
from dotenv import load_dotenv
from tools.concerto_tool import validate_concerto_model
from tools.template_tool import validate_template_syntax

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a technical expert in the Accord Project ecosystem.
You receive validation results and provide clear, actionable feedback.
Always respond with valid JSON only.

Return this structure:
{
  "concerto_valid": true/false,
  "template_valid": true/false,
  "errors": ["error1", "error2"],
  "warnings": ["warning1"],
  "ready_for_review": true/false,
  "feedback": "short summary"
}"""


def validate_draft(draft: dict) -> dict:
    """
    ValidatorAgent: validates the draft using real concerto CLI
    then asks LLM to interpret results and provide feedback.
    """
    # Run real concerto CLI validation
    concerto_result = validate_concerto_model(draft.get("concerto_model", ""))
    template_result = validate_template_syntax(draft.get("templatemark", ""))

    validation_context = f"""
Concerto CLI result:
- valid: {concerto_result['valid']}
- output: {concerto_result['output']}
- errors: {concerto_result['errors']}

TemplateMark syntax check:
- valid: {template_result['valid']}
- errors: {template_result['errors']}

Draft contract type: {draft.get('contract_type', 'unknown')}
Parties: {draft.get('parties', [])}
Key terms: {draft.get('key_terms', [])}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Interpret these validation results:\n{validation_context}"}
        ],
        temperature=0.1,
        max_tokens=500,
    )

    content = response.choices[0].message.content.strip()
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]

    result = json.loads(content)
    result["concerto_cli_valid"] = concerto_result["valid"]
    result["template_syntax_valid"] = template_result["valid"]
    return result