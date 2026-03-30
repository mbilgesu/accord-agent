"""
agents/validator.py
===================
ValidatorAgent: Validates generated Concerto models using
the real Accord Project concerto CLI and checks TemplateMark syntax.
"""

from crewai import Agent, Task
from tools.concerto_tool import validate_concerto_model
from tools.template_tool import validate_template_syntax


def create_validator_agent(llm_model: str = "gpt-4o") -> Agent:
    return Agent(
        role="Accord Project Validator",
        goal=(
            "Validate Concerto models and TemplateMark templates for "
            "correctness, completeness, and compliance with Accord Project standards."
        ),
        backstory=(
            "You are a technical expert in the Accord Project ecosystem. "
            "You use the concerto CLI to validate data models and check "
            "TemplateMark syntax. You provide precise, actionable feedback "
            "when validation fails and confirm when output is production-ready."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm_model,
    )


def create_validation_task(agent: Agent, draft_output: str) -> Task:
    return Task(
        description=f"""
        Validate the following Accord Project template draft:

        {draft_output}

        Steps:
        1. Extract the concerto_model string from the draft
        2. Run concerto CLI validation on the model
        3. Check TemplateMark syntax for balanced clause tags
        4. Verify sample_data keys match model fields
        5. Report all errors with specific line references if possible

        Use the validate_concerto_model tool for step 2.
        Use the validate_template_syntax tool for step 3.
        """,
        agent=agent,
        expected_output=(
            "A JSON object with keys: 'concerto_valid' (bool), "
            "'template_valid' (bool), 'errors' (list of strings), "
            "'warnings' (list of strings), 'ready_for_review' (bool)"
        ),
    )