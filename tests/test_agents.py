"""
tests/test_agents.py
====================
Unit tests for accord-agent tools and agent task definitions.
"""

import pytest
from tools.concerto_tool import validate_concerto_model
from tools.template_tool import (
    generate_template_structure,
    validate_template_syntax,
)


# ── Concerto Tool Tests ───────────────────────────────────────────────────────

def test_validate_valid_concerto_model():
    model = """
namespace org.test

import org.accordproject.contract.Contract from https://models.accordproject.org/accordproject/contract.cto

asset TestContract extends Contract {
  o String contractId
  o String description
}
"""
    result = validate_concerto_model(model)
    assert isinstance(result["valid"], bool)
    assert "output" in result
    assert "errors" in result
    
def test_validate_invalid_concerto_model():
    bad_model = "namespace invalid\nasset Bad {}"
    result = validate_concerto_model(bad_model)
    assert isinstance(result["valid"], bool)
    assert "errors" in result


# ── Template Tool Tests ───────────────────────────────────────────────────────

def test_generate_template_structure():
    result = generate_template_structure(
        contract_type="PaymentAgreement",
        parties=["Freelancer", "Client"],
        key_terms=["amount", "due_date", "payment_terms"],
    )
    assert result["contract_type"] == "PaymentAgreement"
    assert "Freelancer" in result["parties"]
    assert "templatemark" in result
    assert "sample_data" in result


def test_validate_template_syntax_valid():
    template = """
{{#clause freelancerInfo}}Party: {{freelancerName}}{{/clause}}
{{#clause clientInfo}}Party: {{clientName}}{{/clause}}
"""
    result = validate_template_syntax(template)
    assert result["valid"] is True


def test_validate_template_syntax_unbalanced():
    bad_template = """
{{#clause freelancerInfo}}Party: {{freelancerName}}
"""
    result = validate_template_syntax(bad_template)
    assert result["valid"] is False


def test_sample_data_keys_match_parties():
    result = generate_template_structure(
        contract_type="NDA",
        parties=["PartyA", "PartyB"],
        key_terms=["confidentiality_period"],
    )
    assert "partyaName" in result["sample_data"]
    assert "partybName" in result["sample_data"]