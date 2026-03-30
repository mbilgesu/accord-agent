"""
agents/drafter.py
=================
DrafterAgent: Converts natural language requirements into
Accord Project Concerto models and TemplateMark templates.
"""

from crewai import Agent, Task
from tools.template_tool import generate_template_structure, validate_template_syntax


def create_drafter_agent(llm_model: str = "gpt-4o") -> Agent:
    return Agent(
        role="Legal Template Drafter",
        goal=(
            "Convert natural language contract requirements into valid "
            "Accord Project Concerto data models and TemplateMark templates."
        ),
        backstory=(
            "You are an expert in legal contract drafting and the Accord Project "
            "framework. You understand Concerto modeling language, TemplateMark "
            "syntax, and how to translate business requirements into structured "
            "legal templates. You always produce syntactically correct output."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm_model,
    )


def create_draft_task(agent: Agent, requirements: str) -> Task:
    return Task(
        description=f"""
        Draft an Accord Project template for the following requirements:

        {requirements}

        You must produce:
        1. A Concerto model (.cto) defining the contract data structure
        2. A TemplateMark template text
        3. Sample JSON data matching the model

        Follow Accord Project conventions exactly:
        - Use proper namespace (org.accordproject.<contracttype>)
        - Extend Contract from accordproject contract model
        - Use correct TemplateMark clause syntax
        """,
        agent=agent,
        expected_output=(
            "A JSON object with keys: 'concerto_model' (string), "
            "'templatemark' (string), 'sample_data' (dict), "
            "'contract_type' (string), 'parties' (list), 'key_terms' (list)"
        ),
    )