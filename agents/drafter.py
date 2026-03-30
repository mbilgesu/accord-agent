"""
agents/drafter.py
=================
DrafterAgent: Converts natural language requirements into
Accord Project Concerto models and TemplateMark templates.
Uses Groq (free) with Llama 3 — no OpenAI key required.
"""

import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are an expert in legal contract drafting and the Accord Project framework.
You understand Concerto modeling language and TemplateMark syntax.
Always respond with valid JSON only — no markdown, no explanation outside JSON.

When asked to draft a template, return this exact structure:
{
  "contract_type": "string",
  "parties": ["Party1", "Party2"],
  "key_terms": ["term1", "term2"],
  "concerto_model": "namespace org.accordproject...",
  "templatemark": "# Title\\n...",
  "sample_data": {}
}"""


def draft_template(requirements: str) -> dict:
    """
    DrafterAgent: takes natural language requirements,
    returns structured Accord Project template draft.
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Draft an Accord Project template for: {requirements}"}
        ],
        temperature=0.3,
        max_tokens=2000,
    )

    content = response.choices[0].message.content.strip()

    # strip markdown fences if present
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]

    return json.loads(content)