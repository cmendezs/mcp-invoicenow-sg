"""Tests for SGDocumentValidator / PINT-SG + IRAS C5 Schematron wiring."""

from __future__ import annotations

from pathlib import Path

import pytest

from mcp_invoicenow_sg.models import SGInvoice
from mcp_invoicenow_sg.validators.schematron import (
    SUPPORTED_SG_RULESETS,
    SGDocumentValidator,
    UnsupportedSgRulesetError,
    get_sg_validator,
)
from mcp_invoicenow_sg.wire_formats import SGUBLSerializer

_SAMPLE_INVOICE = (
    Path(__file__).parent.parent
    / "specs"
    / "pint-sg"
    / "trn-invoice"
    / "example"
    / "PINT-SG INV example 02 - full valid invoice 1.xml"
)


def test_all_bundled_rulesets_resolve() -> None:
    for ruleset in SUPPORTED_SG_RULESETS:
        validator = get_sg_validator(ruleset)
        assert validator is not None


def test_unsupported_ruleset_raises() -> None:
    with pytest.raises(UnsupportedSgRulesetError):
        get_sg_validator("not-a-real-ruleset")


@pytest.mark.skipif(not _SAMPLE_INVOICE.exists(), reason="PINT-SG sample invoice not present")
def test_official_sample_passes_pint_sg_but_fails_iras_c5() -> None:
    """The official PINT-SG example has no buyer UEN — PINT-SG-valid, IRAS-rejected.

    Matches the documented worked example in the third-party "Invoice
    Packaging" AI Skill this ruleset was sourced from (see
    validators/schematron.py's module docstring): PINT-SG-conformant does not
    imply IRAS-C5-acceptable.
    """
    result = SGDocumentValidator().validate(_SAMPLE_INVOICE.read_bytes())
    assert result.metadata["rulesets_run"] == ["base", "jurisdiction", "iras_c5"]
    assert result.valid is False
    assert any("IRASC5-034" in e for e in result.errors)
    assert not any("[base]" in e or "[jurisdiction]" in e for e in result.errors)


def test_generated_invoice_round_trips_clean(sg_invoice: SGInvoice) -> None:
    xml = SGUBLSerializer().serialize(sg_invoice)
    result = SGDocumentValidator().validate(xml)
    assert result.valid is True, result.errors


def test_invoice_missing_required_uuid_fails_jurisdiction_rule(sg_invoice_data: dict) -> None:
    del sg_invoice_data["invoice_uuid"]
    invoice = SGInvoice.model_validate(sg_invoice_data)
    xml = SGUBLSerializer().serialize(invoice)
    result = SGDocumentValidator().validate(xml)
    assert result.valid is False
    assert any("BR-108-GST-SG" in e for e in result.errors)


def test_invoice_missing_buyer_uen_fails_iras_c5(sg_invoice_data: dict) -> None:
    del sg_invoice_data["buyer"]["uen"]
    invoice = SGInvoice.model_validate(sg_invoice_data)
    xml = SGUBLSerializer().serialize(invoice)
    result = SGDocumentValidator().validate(xml)
    assert result.valid is False
    assert any("IRASC5-034" in e for e in result.errors)


def test_get_schema_version() -> None:
    assert (
        SGDocumentValidator().get_schema_version()
        == "PINT-SG 1.4.1 + IRAS C5 non_peppol_doc_validation v0.3.4"
    )
