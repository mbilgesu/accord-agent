"""
agents/reviewer.py
==================
ReviewerAgent: Reviews the validated template for legal clarity,
completeness, and Accord Project best practices.
"""

from crewai import Agent, Task


def create_reviewer_agent(llm_model: str = "gpt-4o") -> Agent:
    return Agent(
        role="Legal Template Reviewer",
        goal=(
            "Review validated Accord Project templates for legal clarity, "
            "completeness, and alignment with best practices. Suggest "
            "improvements and produce the final template package."
        ),
        backstory=(
            "You are a senior legal engineer with deep expertise in smart "
            "contracts and the Accord Project ecosystem. You review templates "
            "for legal soundness, missing clauses, ambiguous terms, and "
            "compliance with industry standards. Your output is always "
            "production-ready and well-documented."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm_model,
    )


def create_review_task(agent: Agent, validation_output: str) -> Task:
    return Task(
        description=f"""
        Review the following validated Accord Project template:

        {validation_output}

        Your review must cover:
        1. Legal completeness — are all essential clauses present?
        2. Clarity — are terms unambiguous and well-defined?
        3. Accord Project best practices — naming, structure, conventions
        4. Missing fields — what should be added for production use?
        5. Final verdict — is this template ready to publish?

        Produce an improved final version if changes are needed.
        """,
        agent=agent,
        expected_output=(
            "A JSON object with keys: 'final_concerto_model' (string), "
            "'final_templatemark' (string), 'final_sample_data' (dict), "
            "'review_notes' (list of strings), 'production_ready' (bool), "
            "'improvements_made' (list of strings)"
        ),
    )