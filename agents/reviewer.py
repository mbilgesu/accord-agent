"""
agents/reviewer.py
==================
ReviewerAgent: Reviews the validated template for legal clarity,
completeness, and Accord Project best practices.
"""

import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a senior legal engineer with deep expertise in smart contracts
and the Accord Project ecosystem. You review templates for legal soundness,
missing clauses, and compliance with industry standards.
Always respond with valid JSON only.

Return this structure:
{
  "production_ready": true/false,
  "review_notes": ["note1", "note2"],
  "improvements_made": ["improvement1"],
  "final_concerto_model": "namespace...",
  "final_templatemark": "# Title...",
  "final_sample_data": {}
}"""


def review_template(draft: dict, validation: dict) -> dict:
    """
    ReviewerAgent: reviews validated template for legal completeness
    and produces the final production-ready template.
    """
    context = f"""
Draft template:
{json.dumps(draft, indent=2)}

Validation results:
{json.dumps(validation, indent=2)}

Review for:
1. Legal completeness — are all essential clauses present?
2. Clarity — are terms unambiguous?
3. Accord Project best practices
4. Missing fields for production use
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": context}
        ],
        temperature=0.2,
        max_tokens=2000,
    )

    content = response.choices[0].message.content.strip()
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]

    return json.loads(content)